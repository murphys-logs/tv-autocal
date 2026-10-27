"""Deterministic, software-only measurement cycles with a manually advanced clock.

The toy ``level`` is not a Samsung control or protocol value. Meter samples are
literal test inputs, never predictions computed from that level. There is no
transport, display presenter, subprocess, device access or real clock here.
"""

from dataclasses import dataclass, field
from enum import Enum
from math import isfinite

from .simulation import FakeClock


def _integer(value: int, minimum: int, maximum: int, name: str) -> None:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(name + " is outside its integer range")


def _rgb(value: tuple[int, int, int]) -> None:
    if type(value) is not tuple or len(value) != 3:
        raise ValueError("RGB must be an immutable three-channel tuple")
    for channel in value:
        _integer(channel, 0, 255, "RGB channel")


class CommandReply(Enum):
    ACK = "synthetic acknowledgement"
    NACK = "synthetic rejection"
    UNKNOWN = "unknown synthetic result"


class CycleState(Enum):
    NEW = "not started"
    WAITING = "waiting after confirmed menu exit"
    READING = "waiting for a scripted meter sample"
    READY = "accepted simulation sample; awaiting explicit next action"
    COMPLETE = "normal simulated restoration cycle completed"
    STOPPED = "stopped; no automatic recovery"


class Phase(Enum):
    BASELINE = "baseline"
    CHANGE = "change"
    REPEAT = "repeat"
    RESTORE = "restore"


@dataclass(frozen=True)
class TVStep:
    """One cycle's independent fake command, menu and exit behaviours.

    ``apply`` and ``reply`` are deliberately independent: an ACK can accompany
    no change, and an unclear response can accompany a changed toy setting.
    ``menu_value=None`` reports the fake's actual level; ``menu_available`` can
    make that observation unavailable instead.
    """

    reply: CommandReply = CommandReply.ACK
    apply: bool = True
    menu_value: int | None = None
    menu_available: bool = True
    exit_confirmed: bool = True

    def __post_init__(self) -> None:
        if type(self.reply) is not CommandReply:
            raise TypeError("reply must be CommandReply")
        for value in (self.apply, self.menu_available, self.exit_confirmed):
            if type(value) is not bool:
                raise TypeError("TV fault switches must be bool")
        if self.menu_value is not None:
            _integer(self.menu_value, 0, 100, "Scripted menu value")


class SimulatedTV:
    """In-memory scalar setting and normal-menu state; no real-device adapter."""

    def __init__(self, initial_level: int = 50, steps: tuple[TVStep, ...] = ()) -> None:
        _integer(initial_level, 0, 100, "Initial toy level")
        if type(steps) is not tuple or len(steps) > 256 or any(type(s) is not TVStep for s in steps):
            raise ValueError("TV steps must be a tuple of at most 256 TVStep records")
        self._level = initial_level
        self._steps = steps
        self._next_step = 0
        self._active = TVStep()
        self._menu_open = False
        self._commands: list[int] = []

    @property
    def level(self) -> int:
        return self._level

    @property
    def menu_open(self) -> bool:
        return self._menu_open

    @property
    def commands(self) -> tuple[int, ...]:
        return tuple(self._commands)

    def prepare(self, target: int | None) -> CommandReply | None:
        if target is not None:
            _integer(target, 0, 100, "Toy level")
        self._active = self._steps[self._next_step] if self._next_step < len(self._steps) else TVStep()
        self._next_step += 1
        self._menu_open = True
        if target is None:
            return None
        self._commands.append(target)
        if self._active.apply:
            self._level = target
        return self._active.reply

    def inspect(self) -> int | None:
        if not self._menu_open or not self._active.menu_available:
            return None
        return self._level if self._active.menu_value is None else self._active.menu_value

    def exit_menu(self) -> bool:
        if self._active.exit_confirmed:
            self._menu_open = False
        return self._active.exit_confirmed


@dataclass(frozen=True)
class MeterSample:
    """A literal synthetic result, available after ``after_ms`` fake milliseconds.

    Non-finite numbers and missing XYZ are allowed as rejection fixtures.
    Values are never created by transforming the requested setting or patch.
    """

    xyz: tuple[float, float, float] | None
    after_ms: int = 0
    error: str = ""

    def __post_init__(self) -> None:
        _integer(self.after_ms, 0, 3_600_000, "Sample delay")
        if type(self.error) is not str or len(self.error) > 200:
            raise ValueError("Sample error must be a short string")
        if self.xyz is not None:
            if type(self.xyz) is not tuple or len(self.xyz) != 3:
                raise ValueError("XYZ must be an immutable triple or None")
            if any(type(value) not in (float, int) for value in self.xyz):
                raise ValueError("XYZ components must be numbers, excluding bool")
            if any(type(value) is int and value.bit_length() > 1023 for value in self.xyz):
                raise ValueError("Integer XYZ fixture exceeds the numeric model's range")


class SimulatedMeter:
    """Bounded literal sample queue, independent of the fake TV and RGB patch."""

    def __init__(self, samples: tuple[MeterSample, ...]) -> None:
        if type(samples) is not tuple or len(samples) > 256 or any(type(s) is not MeterSample for s in samples):
            raise ValueError("Samples must be a tuple of at most 256 MeterSample records")
        self._samples = samples
        self._reads = 0

    @property
    def reads(self) -> int:
        return self._reads

    def begin_read(self) -> MeterSample:
        index = self._reads
        self._reads += 1
        if index >= len(self._samples):
            return MeterSample(None, error="script exhausted")
        return self._samples[index]


@dataclass(frozen=True)
class CycleEvent:
    timestamp_ms: int
    action: str
    phase: Phase | None
    detail: str
    simulated: bool = field(default=True, init=False)


@dataclass(frozen=True)
class MeasurementRecord:
    """An observed outcome, with scripted arrival separate from polling time.

    ``sample_due_ms`` and ``read_deadline_ms`` are None before a read starts.
    ``completed_ms`` records actual finalisation, including a delayed poll.
    """

    attempt: int
    phase: Phase
    target_level: int
    patch_rgb: tuple[int, int, int]
    started_ms: int
    read_started_ms: int | None
    sample_due_ms: int | None
    read_deadline_ms: int | None
    completed_ms: int
    xyz: tuple[float, float, float] | None
    accepted: bool
    reason: str
    simulated: bool = field(default=True, init=False)
    purpose: str = field(default="simulation diagnostic only; never calibration data", init=False)
    correction: str = field(default="none; synthetic input, no correction applied", init=False)


class MeasurementController:
    """Explicit baseline/change/repeat/restore cycles, permanently stopped on error.

    ``poll`` never advances time. It starts a read only after confirmed exit
    and the configured wait. Successful samples need another explicit action.
    Restoration is permitted only on the normal successful path; cancellation
    and errors never initiate a setter, retry or recovery. This simulator is
    not a transport implementation or a guarantee about a real menu/overlay.
    """

    def __init__(
        self,
        clock: FakeClock,
        tv: SimulatedTV,
        meter: SimulatedMeter,
        *,
        wait_ms: int = 2000,
        read_timeout_ms: int = 60_000,
        max_attempts: int = 16,
    ) -> None:
        if type(clock) is not FakeClock or type(tv) is not SimulatedTV or type(meter) is not SimulatedMeter:
            raise TypeError("Only concrete in-memory fakes are supported")
        _integer(wait_ms, 1, 3_600_000, "Wait")
        _integer(read_timeout_ms, 1, 3_600_000, "Read timeout")
        _integer(max_attempts, 1, 256, "Attempt limit")
        self._clock, self._tv, self._meter = clock, tv, meter
        self._wait_ms, self._read_timeout_ms, self._max_attempts = wait_ms, read_timeout_ms, max_attempts
        self._state = CycleState.NEW
        self._events: list[CycleEvent] = []
        self._records: list[MeasurementRecord] = []
        self._original: int | None = None
        self._restoration_required = False
        self._phase: Phase | None = None
        self._target = 0
        self._patch = (0, 0, 0)
        self._baseline_patch = (0, 0, 0)
        self._started_ms = 0
        self._read_started_ms: int | None = None
        self._wait_until = 0
        self._sample: MeterSample | None = None
        self._pending = False

    @property
    def state(self) -> CycleState:
        return self._state

    @property
    def events(self) -> tuple[CycleEvent, ...]:
        return tuple(self._events)

    @property
    def records(self) -> tuple[MeasurementRecord, ...]:
        return tuple(self._records)

    @property
    def original_level(self) -> int | None:
        return self._original

    @property
    def restoration_required(self) -> bool:
        """Conservative flag: an unverified setter can have changed toy state."""
        return self._restoration_required

    def _event(self, action: str, detail: str = "") -> None:
        self._events.append(CycleEvent(self._clock.milliseconds, action, self._phase, detail))

    def _require(self, state: CycleState) -> None:
        if self._state is not state:
            raise RuntimeError("Action is not allowed while " + self._state.value)

    def _begin(self, phase: Phase, target: int, patch_rgb: tuple[int, int, int]) -> None:
        if len(self._records) >= self._max_attempts:
            self._stop("attempt limit reached")
            return
        self._phase, self._target, self._patch = phase, target, patch_rgb
        self._started_ms = self._clock.milliseconds
        self._read_started_ms = None
        self._sample = None
        self._pending = True
        self._event("begin", "RGB " + str(patch_rgb))
        if phase is Phase.REPEAT:
            if self._tv.menu_open or self._tv.level != target:
                self._stop("simulated state changed since the preceding exit")
                return
        else:
            command = None if phase is Phase.BASELINE else target
            if command is not None:
                self._restoration_required = True
            reply = self._tv.prepare(command)
            if command is not None:
                self._event("set", str(target))
                self._event("reply", reply.value)
                if reply is not CommandReply.ACK:
                    self._stop("setter did not receive a synthetic ACK")
                    return
            observed = self._tv.inspect()
            self._event("inspect", str(observed))
            if observed != target:
                self._stop("simulated menu value is unavailable or differs from target")
                return
            exited = self._tv.exit_menu()
            self._event("exit", "confirmed" if exited else "unconfirmed")
            if not exited:
                self._stop("menu exit was not confirmed")
                return
        self._wait_until = self._clock.milliseconds + self._wait_ms
        self._state = CycleState.WAITING
        self._event("wait", str(self._wait_ms) + " ms")

    def start_baseline(self, patch_rgb: tuple[int, int, int] = (128, 128, 128)) -> None:
        self._require(CycleState.NEW)
        _rgb(patch_rgb)
        self._original = self._tv.level
        self._baseline_patch = patch_rgb
        self._event("capture_original", str(self._original))
        self._begin(Phase.BASELINE, self._original, patch_rgb)

    def measure_change(self, level: int, patch_rgb: tuple[int, int, int] = (128, 128, 128)) -> None:
        self._require(CycleState.READY)
        _integer(level, 0, 100, "Toy level")
        _rgb(patch_rgb)
        self._begin(Phase.CHANGE, level, patch_rgb)

    def repeat(self) -> None:
        """Re-use the confirmed exit, but require a fresh inter-reading wait."""
        self._require(CycleState.READY)
        self._begin(Phase.REPEAT, self._target, self._patch)

    def restore(self) -> None:
        """Explicit normal-path restoration, including exit/wait/read checks."""
        self._require(CycleState.READY)
        self._begin(Phase.RESTORE, self._original, self._baseline_patch)

    def _record(self, accepted: bool, reason: str, xyz: tuple[float, float, float] | None = None) -> None:
        if self._pending:
            due_ms = None if self._read_started_ms is None else self._read_started_ms + self._sample.after_ms
            deadline_ms = None if self._read_started_ms is None else self._read_started_ms + self._read_timeout_ms
            self._records.append(MeasurementRecord(
                len(self._records) + 1, self._phase, self._target, self._patch,
                self._started_ms, self._read_started_ms, due_ms, deadline_ms, self._clock.milliseconds,
                xyz, accepted, reason,
            ))
            self._pending = False

    def _stop(self, reason: str, xyz: tuple[float, float, float] | None = None) -> None:
        if self._original is not None and self._tv.level != self._original:
            self._restoration_required = True
        self._record(False, reason, xyz)
        self._state = CycleState.STOPPED
        self._event("stop", reason)

    def cancel(self) -> None:
        if self._state not in (CycleState.STOPPED, CycleState.COMPLETE):
            self._stop("cancelled; no automatic restoration or further reads")

    def poll(self) -> CycleState:
        """Observe fake time; the exact read deadline is a timeout boundary.

        If polling is delayed, a literal sample scheduled before the deadline
        remains timely. A sample exactly at the deadline is late. No future
        reading or restoration is started merely because a reading completes.
        """
        if self._state not in (CycleState.WAITING, CycleState.READING):
            return self._state
        if self._tv.menu_open or self._tv.level != self._target:
            self._stop("simulated menu or setting changed during wait/read")
            return self._state
        now = self._clock.milliseconds
        if self._state is CycleState.WAITING:
            if now < self._wait_until:
                return self._state
            self._read_started_ms = now
            self._sample = self._meter.begin_read()
            self._state = CycleState.READING
            self._event("read", "literal synthetic XYZ requested")
        elapsed = now - self._read_started_ms
        if self._sample.after_ms < self._read_timeout_ms and elapsed >= self._sample.after_ms:
            xyz = self._sample.xyz
            if self._sample.error:
                self._stop("meter error: " + self._sample.error, xyz)
            elif xyz is None:
                self._stop("missing XYZ measurement")
            elif any(not isfinite(value) for value in xyz):
                self._stop("non-finite XYZ measurement", xyz)
            else:
                self._record(True, "accepted simulation sample only", xyz)
                self._event("accepted", "not equipment evidence or calibration data")
                if self._phase is Phase.RESTORE:
                    self._restoration_required = False
                    self._state = CycleState.COMPLETE
                else:
                    self._state = CycleState.READY
        elif elapsed >= self._read_timeout_ms:
            self._stop("meter deadline reached without a timely sample")
        return self._state
