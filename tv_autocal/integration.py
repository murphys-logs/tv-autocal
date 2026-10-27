"""One offline measurement composed from explicit, synthetic interface evidence.

No device adapter, command dispatch, process launch or display API exists here.
Unlike the earlier toy cycle, this boundary never reads a TV's hidden state.
It cannot detect a real overlay or certify an observation supplied by a caller.
"""

from dataclasses import dataclass, field
from enum import Enum

from .meter_output import MeterOutput, parse_meter_output
from .presentation import ManualPresenter, PresentationReceipt
from .sender_audit import AuditEvent, CandidateCommand, SenderAudit
from .simulation import FakeClock


@dataclass(frozen=True)
class MenuObservation:
    """Authored fixture evidence, not automatic setting/menu readback."""

    inspected_ms: int
    exited_ms: int
    exit_confirmed: bool
    observed_level: int | None = None
    simulated: bool = field(default=True, init=False)

    def __post_init__(self) -> None:
        if any(type(v) is not int or v < 0 for v in (self.inspected_ms, self.exited_ms)):
            raise ValueError("Observation times must be nonnegative integers")
        if self.exited_ms < self.inspected_ms or type(self.exit_confirmed) is not bool:
            raise ValueError("Exit must follow inspection and its confirmation must be bool")
        if self.observed_level is not None and (
            type(self.observed_level) is not int or not 0 <= self.observed_level <= 100
        ):
            raise ValueError("Fixture setting must be an integer in 0..100 or unknown")


class IntegrationState(Enum):
    NEW = "not started"
    WAITING = "waiting after explicit exit and patch receipt"
    READING = "awaiting a complete synthetic process transcript"
    COMPLETE = "accepted diagnostic simulation only"
    STOPPED = "stopped; no retry or automatic restoration"


@dataclass(frozen=True)
class IntegrationRecord:
    presentation: PresentationReceipt
    observation: MenuObservation
    command: CandidateCommand | None
    command_accepted: bool | None
    command_events: tuple[AuditEvent, ...]
    command_closed_ms: int | None
    started_ms: int
    read_started_ms: int | None
    read_deadline_ms: int | None
    completed_ms: int
    meter: MeterOutput | None
    accepted: bool
    reason: str
    simulated: bool = field(default=True, init=False)
    purpose: str = field(default="synthetic diagnostic only; never calibration data", init=False)


class OfflineMeasurement:
    """Explicit start/poll/finish for one frame; never advances a playlist.

    A successful attempt releases its hold so a caller may explicitly advance
    or construct a fresh attempt for a repeat. Failure closes a presentation
    still owned by this attempt; a replacement owner's hold is never released.
    There is no running process to kill or TV setting to restore.
    """

    def __init__(self, clock: FakeClock, presenter: ManualPresenter, *, wait_ms: int = 2000,
                 read_timeout_ms: int = 60000) -> None:
        if type(clock) is not FakeClock or type(presenter) is not ManualPresenter:
            raise TypeError("Only concrete offline clock and presenter are supported")
        if presenter.clock is not clock:
            raise ValueError("All fixtures must share the same fake clock")
        if any(type(v) is not int or not 1 <= v <= 3_600_000 for v in (wait_ms, read_timeout_ms)):
            raise ValueError("Wait and read timeout must be bounded positive integer milliseconds")
        self._clock, self._presenter = clock, presenter
        self._wait_ms, self._timeout_ms = wait_ms, read_timeout_ms
        self._state = IntegrationState.NEW
        self._record: IntegrationRecord | None = None
        self._receipt: PresentationReceipt | None = None
        self._hold_token: int | None = None
        self._observation: MenuObservation | None = None
        self._command: CandidateCommand | None = None
        self._command_accepted: bool | None = None
        self._command_events: tuple[AuditEvent, ...] = ()
        self._command_closed_ms: int | None = None
        self._started_ms = 0
        self._read_started_ms: int | None = None

    @property
    def state(self) -> IntegrationState:
        return self._state

    @property
    def record(self) -> IntegrationRecord | None:
        return self._record

    def begin(self, observation: MenuObservation, *, command: SenderAudit | None = None) -> None:
        if self._state is not IntegrationState.NEW:
            raise RuntimeError("An attempt cannot be restarted")
        if type(observation) is not MenuObservation:
            raise TypeError("An explicit synthetic menu observation is required")
        if command is not None and type(command) is not SenderAudit:
            raise TypeError("Command evidence must be a concrete offline audit")
        if command is not None and command.clock is not self._clock:
            raise ValueError("Command evidence must share the fake clock")
        receipt = self._presenter.current_receipt
        if receipt is None or self._presenter.closed:
            raise RuntimeError("An explicitly confirmed, buffered patch is required")
        # Acquire the hold before changing this attempt; an occupied presenter
        # rejects a competing attempt without disturbing its current owner.
        self._hold_token = self._presenter.hold(receipt.sequence)
        self._receipt, self._observation = receipt, observation
        self._started_ms = self._clock.milliseconds
        self._state = IntegrationState.WAITING
        if command is not None:
            self._command = command.command
            self._command_accepted = command.accepted
            self._command_events = command.events
            self._command_closed_ms = command.closed_ms
        if not observation.exit_confirmed or observation.exited_ms > self._started_ms:
            self._finish(False, "Menu exit is unconfirmed or dated in the future")
            return
        if command is not None:
            if not command.accepted:
                self._finish(False, "Command audit must close with one ACK and a complete byte log")
                return
            if observation.inspected_ms < command.closed_ms:
                self._finish(False, "Menu observation predates the closed command audit")
                return
            target = {CandidateCommand.CONTRAST94: 94, CandidateCommand.RESTORE95: 95}.get(command.command)
            if target is not None and observation.observed_level != target:
                self._finish(False, "ACK does not establish the independently observed setting")

    def _presentation_intact(self) -> bool:
        return (not self._presenter.closed and self._presenter.current_receipt == self._receipt
                and self._presenter.held_sequence == self._receipt.sequence
                and self._presenter.held_token == self._hold_token)

    def _finish(self, accepted: bool, reason: str, meter: MeterOutput | None = None) -> None:
        self._record = IntegrationRecord(
            self._receipt, self._observation, self._command, self._command_accepted,
            self._command_events, self._command_closed_ms,
            self._started_ms, self._read_started_ms,
            None if self._read_started_ms is None else self._read_started_ms + self._timeout_ms,
            self._clock.milliseconds,
            meter, accepted, reason,
        )
        if accepted:
            self._presenter.release(self._receipt.sequence, self._hold_token)
            self._state = IntegrationState.COMPLETE
        else:
            if self._presenter.held_token == self._hold_token:
                self._presenter.close()
            self._state = IntegrationState.STOPPED

    def poll(self) -> IntegrationState:
        if self._state not in (IntegrationState.WAITING, IntegrationState.READING):
            return self._state
        if not self._presentation_intact():
            self._finish(False, "Buffered presentation was closed, replaced or released")
            return self._state
        now = self._clock.milliseconds
        if self._state is IntegrationState.WAITING and now >= self._started_ms + self._wait_ms:
            self._read_started_ms = now
            self._state = IntegrationState.READING
        elif self._state is IntegrationState.READING and now >= self._read_started_ms + self._timeout_ms:
            self._finish(False, "No complete transcript before the read deadline")
        return self._state

    def finish(self, stdout: bytes, stderr: bytes, exit_code: int | None) -> IntegrationRecord:
        if self._state is not IntegrationState.READING:
            raise RuntimeError("A complete transcript is only accepted during a reading")
        # Validate/parse first so a malformed API call cannot silently consume
        # the attempt. Process failures are returned as evidence, not exceptions.
        late = self._clock.milliseconds >= self._read_started_ms + self._timeout_ms
        result = parse_meter_output(stdout, stderr, exit_code, timed_out=late)
        if not self._presentation_intact():
            self._finish(False, "Buffered presentation changed during the transcript", result)
        else:
            self._finish(result.accepted, result.reason, result)
        return self._record

    def cancel(self) -> None:
        if self._state in (IntegrationState.COMPLETE, IntegrationState.STOPPED):
            return
        if self._state is IntegrationState.NEW:
            self._state = IntegrationState.STOPPED
            return
        self._finish(False, "Cancelled; no automatic command, retry or restoration")
