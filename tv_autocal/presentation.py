"""Manual in-memory patch presentation, with no display or device access.

Targets are supplied fixtures, not enumerated monitors. A receipt identifies
software bytes only: it never proves that a screen showed them. The approved
centred 6.25% geometry is supplied by the unchanged renderer.
"""

from dataclasses import dataclass, field
from hashlib import sha256

from .renderer import HEIGHT, WIDTH, RGBFrame, render_patch
from .simulation import FakeClock


def _integer(value: int, minimum: int, maximum: int, name: str) -> None:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(name + " must be an integer in the permitted range")


def _rgb(value: tuple[int, int, int]) -> None:
    if type(value) is not tuple or len(value) != 3:
        raise ValueError("Patch RGB must be an immutable three-channel tuple")
    for channel in value:
        _integer(channel, 0, 255, "RGB channel")


@dataclass(frozen=True)
class DisplayTarget:
    """A named synthetic display fixture, never an operating-system handle."""

    name: str
    width: int = WIDTH
    height: int = HEIGHT

    def __post_init__(self) -> None:
        if type(self.name) is not str or not 1 <= len(self.name) <= 64 or not self.name.isprintable():
            raise ValueError("Fixture name must contain 1-64 printable characters")
        if self.name != self.name.strip():
            raise ValueError("Fixture name cannot have surrounding whitespace")
        _integer(self.width, 1, 16_384, "Fixture width")
        _integer(self.height, 1, 16_384, "Fixture height")


@dataclass(frozen=True)
class PresentationReceipt:
    """Identity and fake time of a generated buffer, not physical presentation."""

    sequence: int
    target: DisplayTarget
    patch_rgb: tuple[int, int, int]
    presented_ms: int
    frame_sha256: str
    simulated: bool = field(default=True, init=False)
    displayed_on_hardware: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        _integer(self.sequence, 1, 256, "Presentation sequence")
        if type(self.target) is not DisplayTarget:
            raise TypeError("Target must be a concrete DisplayTarget fixture")
        if (self.target.width, self.target.height) != (WIDTH, HEIGHT):
            raise ValueError("Receipt target must have native geometry")
        _rgb(self.patch_rgb)
        if type(self.presented_ms) is not int or self.presented_ms < 0:
            raise ValueError("Presentation time must be nonnegative fake milliseconds")
        if (type(self.frame_sha256) is not str or len(self.frame_sha256) != 64
                or any(character not in "0123456789abcdef" for character in self.frame_sha256)):
            raise ValueError("Frame hash must be a lowercase SHA-256 hex digest")


class ManualPresenter:
    """Explicitly select, confirm and advance a bounded synthetic patch list.

    Only the current immutable frame is retained. Receipts retain identity,
    hash and fake time without retaining every large pixel buffer. A hold
    prevents advancement during a measurement. Each acquisition has a fresh
    token, so a stale consumer cannot release a later hold on the same frame.
    Close/cancel clears the buffer; an integrating controller must observe it.
    """

    def __init__(self, clock: FakeClock, targets: tuple[DisplayTarget, ...],
                 patches: tuple[tuple[int, int, int], ...]) -> None:
        if type(clock) is not FakeClock:
            raise TypeError("Only a concrete in-memory FakeClock is supported")
        if (type(targets) is not tuple or not 1 <= len(targets) <= 16
                or any(type(target) is not DisplayTarget for target in targets)):
            raise ValueError("Targets must be a tuple of 1-16 concrete display fixtures")
        if len({target.name for target in targets}) != len(targets):
            raise ValueError("Display fixture names must be unique")
        if type(patches) is not tuple or not 1 <= len(patches) <= 256:
            raise ValueError("Patches must be a tuple of 1-256 RGB tuples")
        for patch in patches:
            _rgb(patch)
        self._clock = clock
        self._targets = targets
        self._patches = patches
        self._selected: DisplayTarget | None = None
        self._confirmed = False
        self._closed = False
        self._held_sequence: int | None = None
        self._held_token: int | None = None
        self._next_hold_token = 0
        self._frame: RGBFrame | None = None
        self._receipts: list[PresentationReceipt] = []

    @property
    def clock(self) -> FakeClock:
        """Shared fake clock identity for composing offline components."""
        return self._clock

    @property
    def selected_target(self) -> DisplayTarget | None:
        return self._selected

    @property
    def confirmed(self) -> bool:
        return self._confirmed

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def held_sequence(self) -> int | None:
        return self._held_sequence

    @property
    def held_token(self) -> int | None:
        return self._held_token

    @property
    def frame(self) -> RGBFrame | None:
        return self._frame

    @property
    def receipts(self) -> tuple[PresentationReceipt, ...]:
        return tuple(self._receipts)

    @property
    def current_receipt(self) -> PresentationReceipt | None:
        return self._receipts[-1] if self._frame is not None else None

    def _require_open(self) -> None:
        if self._closed:
            raise RuntimeError("The synthetic presenter is closed")

    def select(self, name: str) -> DisplayTarget:
        self._require_open()
        if self._receipts:
            raise RuntimeError("Target cannot change after the first presentation")
        if type(name) is not str:
            raise ValueError("Select a supplied fixture by its exact name")
        selected = next((target for target in self._targets if target.name == name), None)
        if selected is None:
            raise ValueError("Unknown synthetic display fixture")
        if (selected.width, selected.height) != (WIDTH, HEIGHT):
            raise ValueError("Only native 3840x2160 targets are supported; no scaling")
        self._selected = selected
        self._confirmed = False
        return selected

    def confirm(self, name: str) -> None:
        self._require_open()
        if self._receipts:
            raise RuntimeError("Confirmation is fixed after the first presentation")
        if self._selected is None or type(name) is not str or name != self._selected.name:
            raise ValueError("Explicit confirmation must name the selected fixture")
        self._confirmed = True

    def advance(self) -> PresentationReceipt:
        self._require_open()
        if not self._confirmed:
            raise RuntimeError("Select and explicitly confirm a target before advancing")
        if self._held_sequence is not None:
            raise RuntimeError("Current presentation is held for a measurement")
        index = len(self._receipts)
        if index >= len(self._patches):
            raise RuntimeError("The synthetic patch sequence is exhausted")
        rgb = self._patches[index]
        frame = render_patch(rgb)
        receipt = PresentationReceipt(index + 1, self._selected, rgb,
                                      self._clock.milliseconds, sha256(frame.pixels).hexdigest())
        self._frame = frame
        self._receipts.append(receipt)
        return receipt

    def hold(self, sequence: int) -> int:
        self._require_open()
        _integer(sequence, 1, 256, "Presentation sequence")
        current = self.current_receipt
        if current is None or current.sequence != sequence:
            raise ValueError("Hold must identify the current presentation")
        if self._held_sequence is not None:
            raise RuntimeError("Current presentation is already held")
        self._next_hold_token += 1
        self._held_sequence = sequence
        self._held_token = self._next_hold_token
        return self._held_token

    def release(self, sequence: int, token: int) -> None:
        self._require_open()
        _integer(sequence, 1, 256, "Presentation sequence")
        _integer(token, 1, self._next_hold_token, "Hold token")
        if self._held_sequence != sequence or self._held_token != token:
            raise ValueError("Release must identify the held presentation and its current token")
        self._held_sequence = None
        self._held_token = None

    def close(self) -> None:
        """End the fixture session without advancing or displaying anything."""
        self._frame = None
        self._held_sequence = None
        self._held_token = None
        self._closed = True

    def cancel(self) -> None:
        self.close()
