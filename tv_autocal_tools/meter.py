"""One manually requested meter attempt; hardware use requires an explicit permit.

Import and TranscriptCapture are inert. Offline run_meter tests substitute inert
process and file boundaries. A rejected deadline does not kill a
driver: supervision and bounded draining continue through process exit/EOF.
"""

from dataclasses import dataclass
from hashlib import sha256 as digest_sha256
from os import getpid
from pathlib import Path, PureWindowsPath
from re import fullmatch
from sys import platform
from time import monotonic, sleep

from tv_autocal.meter_output import MAX_OUTPUT_BYTES, parse_meter_output
from .permission import HardwarePermit


CHUNK_BYTES = 2048
_CORRECTION_KEYS = {"ARGYLL_COLMTER_CAL_SPEC_SET", "ARGYLL_COLMTER_COR_MATRIX"}


@dataclass(frozen=True)
class MeterResult:
    stdout: bytes
    stderr: bytes
    exit_code: int | None
    accepted: bool
    reason: str
    xyz: tuple[float, float, float] | None
    output_format: str | None
    timed_out: bool
    cancelled: bool
    capture_complete: bool
    log_complete: bool
    stdout_dropped: int
    stderr_dropped: int
    simulated: bool
    purpose: str = "component diagnostic only; never calibration data"
    wrapper_pid: int | None = None
    child_pid: int | None = None
    child_exit_confirmed: bool | None = None
    readers_complete: bool | None = None

    def as_dict(self) -> dict:
        return {**self.__dict__, "stdout": self.stdout.hex(), "stderr": self.stderr.hex(),
                "encoding": "hex bytes"}


class TranscriptCapture:
    """Bounded raw evidence. Timeout/cancel never discard later supplied bytes.

    This class is used serially, or with the runner's lock. Raw capture and log
    completeness are separate. A log error or overflow can never be accepted.
    """

    def __init__(self, started_ms: int, *, timeout_ms: int = 60000,
                 simulated: bool = True, log=None) -> None:
        if type(started_ms) is not int or started_ms < 0:
            raise ValueError("Start time must be nonnegative integer milliseconds")
        if type(timeout_ms) is not int or not 1 <= timeout_ms <= 60000:
            raise ValueError("Read deadline must be in 1..60000 milliseconds")
        if type(simulated) is not bool or log is not None and not callable(log):
            raise TypeError("Invalid provenance or log callback")
        self.started_ms, self.deadline_ms = started_ms, started_ms + timeout_ms
        self.simulated, self.log = simulated, log
        self.buffers = {"stdout": bytearray(), "stderr": bytearray()}
        self.dropped = {"stdout": 0, "stderr": 0}
        self.eof = {"stdout": False, "stderr": False}
        self.read_errors: set[str] = set()
        self.timed_out = self.cancelled = False
        self.log_complete = True
        self._last_ms = started_ms
        # None means no process lifecycle was observed (pure transcript use).
        self.wrapper_pid = self.child_pid = None
        self.child_exit_confirmed = self.readers_complete = None

    def _emit(self, kind: str, **fields) -> None:
        if self.log is not None and self.log_complete:
            try:
                self.log(kind, simulated=self.simulated, **fields)
            except Exception:
                self.log_complete = False

    def tick(self, now_ms: int) -> None:
        if type(now_ms) is not int or now_ms < self._last_ms:
            raise ValueError("Capture time must be monotonic integer milliseconds")
        self._last_ms = now_ms
        if now_ms >= self.deadline_ms and not self.timed_out:
            self.timed_out = True
            self._emit("meter_timeout", time_ms=now_ms,
                       detail="rejected; continue draining, no kill/retry")

    def feed(self, stream: str, data: bytes, now_ms: int) -> None:
        if stream not in self.buffers or type(data) is not bytes:
            raise TypeError("Capture needs named stdout/stderr and bytes")
        if self.eof[stream]:
            raise RuntimeError("Output supplied after stream EOF")
        self.tick(now_ms)
        available = MAX_OUTPUT_BYTES - len(self.buffers[stream])
        retained = data[:available]
        self.buffers[stream].extend(retained)
        # Log fixed-size pieces even when a synthetic caller supplies a large chunk.
        for offset in range(0, len(retained), CHUNK_BYTES):
            self._emit("meter_output", stream=stream, time_ms=now_ms,
                       data_hex=retained[offset:offset + CHUNK_BYTES].hex())
        omitted = len(data) - len(retained)
        if omitted and self.dropped[stream] == 0:
            self._emit("meter_overflow", stream=stream, time_ms=now_ms,
                       detail="capture truncated; subsequent bytes drained and counted")
        self.dropped[stream] += omitted

    def end_stream(self, stream: str, now_ms: int, *, error: bool = False) -> None:
        if stream not in self.buffers or type(error) is not bool:
            raise TypeError("Invalid stream completion")
        self.tick(now_ms)
        self.eof[stream] = not error
        if error:
            self.read_errors.add(stream)
        self._emit("meter_stream_end", stream=stream, time_ms=now_ms, error=error)

    def cancel(self, now_ms: int) -> None:
        self.tick(now_ms)
        if not self.cancelled:
            self.cancelled = True
            self._emit("meter_cancel", time_ms=now_ms,
                       detail="rejected; capture remains attached until exit/EOF")

    def result(self, exit_code: int | None, now_ms: int) -> MeterResult:
        self.tick(now_ms)
        raw = {name: bytes(value) for name, value in self.buffers.items()}
        complete = all(self.eof.values()) and not self.read_errors and not any(self.dropped.values())
        parsed = parse_meter_output(raw["stdout"], raw["stderr"], exit_code,
                                    timed_out=self.timed_out, cancelled=self.cancelled)
        accepted = (parsed.accepted and complete and self.log_complete
                    and parsed.output_format == "Yxy")
        if not complete:
            reason = "incomplete stream capture; diagnostic attempt rejected"
        elif not self.log_complete:
            reason = "incomplete audit log; diagnostic attempt rejected"
        elif parsed.accepted and parsed.output_format != "Yxy":
            reason = "output format does not match the fixed -x invocation"
        elif accepted:
            reason = "complete Yxy diagnostic transcript; never calibration data"
        else:
            reason = parsed.reason
        # Legacy parser is a grammar check only: its synthetic provenance is not
        # copied onto physical bytes. The runner supplies hardware provenance.
        return MeterResult(raw["stdout"], raw["stderr"], exit_code, accepted, reason,
                           parsed.xyz if accepted else None, parsed.output_format,
                           self.timed_out, self.cancelled, complete, self.log_complete,
                           self.dropped["stdout"], self.dropped["stderr"], self.simulated,
                           wrapper_pid=self.wrapper_pid, child_pid=self.child_pid,
                           child_exit_confirmed=self.child_exit_confirmed,
                           readers_complete=self.readers_complete)


def isolated_environment(environ: dict[str, str]) -> dict[str, str]:
    """Copy the supplied environment without either correction default."""
    return {key: value for key, value in environ.items() if key.upper() not in _CORRECTION_KEYS}


def _verified_executable(executable: str, expected: str) -> str:
    if type(executable) is not str or type(expected) is not str:
        raise TypeError("Executable path and expected SHA-256 must be strings")
    path = PureWindowsPath(executable)
    if (not path.is_absolute() or not fullmatch(r"[A-Za-z]:", path.drive)
            or path.name.lower() != "spotread.exe"
            or fullmatch(r"[0-9a-f]{64}", expected) is None):
        raise ValueError("Use a drive-absolute spotread.exe path and full lowercase SHA-256")
    actual_path = Path(executable).resolve(strict=True)
    if (actual_path.name.lower() != "spotread.exe"
            or not fullmatch(r"[A-Za-z]:", PureWindowsPath(str(actual_path)).drive)
            or not actual_path.is_file()):
        raise ValueError("Resolved executable must be a regular spotread.exe file")
    digest = digest_sha256()
    count = 0
    with actual_path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            count += len(chunk)
            if count > 128 * 1024 * 1024:
                raise ValueError("Executable exceeds the verification size limit")
            digest.update(chunk)
    if digest.hexdigest() != expected:
        raise ValueError("Executable hash differs from the reviewed local identity")
    return str(actual_path)


def _reserve_attempt_log(attempt_log: str, plan: str) -> str:
    if type(attempt_log) is not str:
        raise TypeError("An explicit fresh local attempt logfile is required")
    root = Path(__file__).resolve().parent.parent
    base = (root / "local" / plan).resolve()
    candidate = Path(attempt_log).resolve()
    if (not base.is_relative_to(root) or not candidate.is_relative_to(base)
            or candidate.parent != base
            or fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\.log", candidate.name) is None
            or candidate.stem.upper() in {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
            or fullmatch(r"(?:COM|LPT)[1-9]", candidate.stem.upper())):
        raise ValueError("Attempt log must be a simple fresh file directly in local/<plan>/")
    base.mkdir(parents=True, exist_ok=True)
    with candidate.open("xb"):
        pass
    return str(candidate)


def _spawn(argv: list[str], env: dict[str, str]):
    from subprocess import CREATE_NEW_PROCESS_GROUP, CREATE_NO_WINDOW, DEVNULL, PIPE, Popen
    return Popen(argv, shell=False, stdin=DEVNULL, stdout=PIPE, stderr=PIPE,
                 env=env, bufsize=0, creationflags=CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW)


class _DeferredStop:
    """Latch SIGINT without raising inside a lock, launch or cleanup operation.

    This is installed before launch and retained through child exit and reader
    cleanup. It does not handle console closure, termination, or OS shutdown.
    Signal delivery timing on the owner's Windows installation is untested.
    """

    def __init__(self):
        self.requested = False

    def request(self, signum=None, frame=None):
        # A signal handler must not acquire the readers' lock or write logs.
        self.requested = True

    def __enter__(self):
        from signal import SIGINT, signal
        self.previous = signal(SIGINT, self.request)
        return self

    def __exit__(self, exc_type, exc, traceback):
        from signal import SIGINT, signal
        try:
            signal(SIGINT, self.previous)
        except Exception as restore_error:
            if exc is None:
                raise
            exc.add_note("Restoring the SIGINT handler also failed: " + type(restore_error).__name__)

    def apply(self, capture):
        # The caller owns the capture lock (or all readers have joined).
        if self.requested and not capture.cancelled:
            capture.cancel(_now_ms())


def _now_ms() -> int:
    return int(monotonic() * 1000)


class _PipeReaders:
    """Allocate both reader threads before permitting any child launch."""

    def __init__(self, capture):
        from threading import Event, Lock, Thread
        self.capture = capture
        self.lock, self.ready = Lock(), Event()
        self.process = None
        self.done = {"stdout": False, "stderr": False}
        self.threads = [Thread(target=self._reader, args=(name,), daemon=False,
                               name="component-meter-" + name) for name in self.done]

    def start(self):
        try:
            for thread in self.threads:
                thread.start()
        except BaseException:
            self.abort()
            raise

    def attach(self, process):
        self.process = process
        self.ready.set()

    def abort(self):
        # With no process attached, even partially started workers simply exit.
        self.ready.set()
        for thread in self.threads:
            try:
                thread.join()
            except RuntimeError:
                pass  # A thread that never started has nothing to drain.

    def join(self):
        for thread in self.threads:
            thread.join()

    def _reader(self, name):
        self.ready.wait()
        if self.process is None:
            return
        pipe = getattr(self.process, name)
        failed = False
        try:
            while True:
                data = pipe.read(CHUNK_BYTES)
                if not data:
                    break
                with self.lock:
                    self.capture.feed(name, data, _now_ms())
        except Exception:
            failed = True
        finally:
            with self.lock:
                self.capture.end_stream(name, _now_ms(), error=failed)
                self.done[name] = True


def _notify(capture, notify, message):
    try:
        notify(message)
    except Exception:
        capture.read_errors.add("notification")
        capture._emit("meter_notification_error", detail="status output failed; capture remains attached")


def _supervise(process, capture: TranscriptCapture, notify, *, readers, stop=None) -> MeterResult:
    lock, done = readers.lock, readers.done
    stop = stop if stop is not None else _DeferredStop()
    warned = False
    status_failed = False
    exit_code = None
    capture.child_exit_confirmed = capture.readers_complete = False
    while True:
        try:
            with lock:
                stop.apply(capture)
                capture.tick(_now_ms())
                if (capture.timed_out or capture.cancelled or capture.read_errors
                        or not capture.log_complete) and not warned:
                    _notify(capture, notify,
                            "Attempt rejected; meter child/output may still be outstanding "
                            "(child PID " + str(capture.child_pid) + ", wrapper PID "
                            + str(capture.wrapper_pid) + "). Capture remains attached. "
                            "No kill, retry or further reading is sent.")
                    warned = True
            try:
                if exit_code is None:
                    exit_code = process.poll()
            except Exception:
                with lock:
                    capture.read_errors.add("process-status")
                    if not status_failed:
                        capture._emit("meter_status_error", detail="process completion unconfirmed")
                        status_failed = True
                exit_code = None
            with lock:
                stop.apply(capture)
                if exit_code is not None and not capture.child_exit_confirmed:
                    capture.child_exit_confirmed = True
                    capture._emit("meter_child_exit", child_pid=capture.child_pid,
                                  exit_code=exit_code, time_ms=_now_ms(),
                                  readers_complete=False)
                    if not all(done.values()):
                        _notify(capture, notify,
                                "Meter child exit confirmed; output readers are still outstanding. "
                                "Keep the wrapper and held patch in place until final completion.")
                if exit_code is not None and all(done.values()):
                    break
            sleep(0.05)
        except KeyboardInterrupt:
            # Defensive fallback for an explicitly raised KeyboardInterrupt.
            # Ordinary SIGINT uses the non-raising handler throughout this call.
            stop.request()
    while True:
        try:
            readers.join()
            capture.readers_complete = True
            break
        except KeyboardInterrupt:
            stop.request()
    stop.apply(capture)
    capture._emit("meter_readers_complete", child_pid=capture.child_pid,
                  time_ms=_now_ms(), child_exit_confirmed=True)
    for name in done:
        while True:
            try:
                getattr(process, name).close()
                break
            except KeyboardInterrupt:
                stop.request()
            except Exception:
                capture.read_errors.add(name + "-close")
                capture._emit("meter_pipe_close_error", stream=name)
                break
        stop.apply(capture)
    capture._emit("meter_exit", exit_code=exit_code, time_ms=_now_ms(),
                  wrapper_pid=capture.wrapper_pid, child_pid=capture.child_pid,
                  child_exit_confirmed=capture.child_exit_confirmed,
                  readers_complete=capture.readers_complete,
                  stdout_dropped=capture.dropped["stdout"],
                  stderr_dropped=capture.dropped["stderr"])
    stop.apply(capture)
    return capture.result(exit_code, _now_ms())


def run_meter(permit: HardwarePermit, *, executable: str, sha256: str, attempt_log: str,
              log, isolated: bool = False, exit_confirmed: bool = False,
              discovery_confirmed: bool = False, wait_ms: int = 2000,
              timeout_ms: int = 60000, notify=print) -> MeterResult:
    """Future physical entry point. Never call this in offline verification.

    Attestations are owner assertions, not device checks. The authorised owner
    must supervise the fixed patch throughout the wait and capture. No display
    observation, instrument discovery or cross-process serial lock is inferred.
    A timeout stops acceptance, while this call remains attached until exit and
    reader completion. Closing the wrapper externally does not prove child exit;
    forced termination or shutdown remains an unresolved physical procedure.
    """
    if type(permit) is not HardwarePermit:
        raise TypeError("An explicit component permit is required")
    permit.require("meter")
    if platform != "win32":
        raise RuntimeError("The physical meter runner is Windows-only")
    if any(value is not True for value in (isolated, exit_confirmed, discovery_confirmed)):
        raise PermissionError("Confirm both Ex-Link ends disconnected, no other serial devices/tools, "
                              "recorded unambiguous Spyder5 discovery and stable patch/menu exit")
    if type(wait_ms) is not int or not 2000 <= wait_ms <= 60000:
        raise ValueError("A fresh wait of 2000..60000 milliseconds is required")
    if type(timeout_ms) is not int or not 1 <= timeout_ms <= 60000:
        raise ValueError("Deadline must be 1..60000 milliseconds")
    if not callable(log) or not callable(notify):
        raise TypeError("Audit log and status notification callbacks are required")
    checked = _verified_executable(executable, sha256)
    destination = _reserve_attempt_log(attempt_log, permit.plan)
    from os import environ
    environment = isolated_environment(dict(environ))
    argv = [checked, "-O", "-e", "-x", "-Y", "n", destination]
    log("meter_preflight", simulated=False, executable=checked, sha256=sha256,
        argv=argv, isolated=True, discovery_confirmed=True, exit_confirmed=True,
        correction_defaults_removed=sorted(_CORRECTION_KEYS), wait_ms=wait_ms)
    wait_start = _now_ms()
    while _now_ms() - wait_start < wait_ms:
        sleep(0.05)
    started_ms = _now_ms()
    log("meter_launch_intent", simulated=False, argv=argv, time_ms=started_ms,
        wait_started_ms=wait_start, wait_completed_ms=started_ms)
    capture = TranscriptCapture(started_ms, timeout_ms=timeout_ms, simulated=False, log=log)
    readers = _PipeReaders(capture)
    try:
        readers.start()
    except BaseException:
        log("meter_capture_start_failed", simulated=False,
            detail="no process launched; reader resources unavailable")
        raise
    # Install failure is pre-launch. Keep the non-raising handler installed
    # until supervision, reader joins and pipe cleanup have actually completed.
    process = None
    try:
        with _DeferredStop() as stop:
            if stop.requested:
                raise KeyboardInterrupt("Meter attempt cancelled before process launch")
            process = _spawn(argv, environment)
            readers.attach(process)
            with readers.lock:
                capture.wrapper_pid, capture.child_pid = getpid(), getattr(process, "pid", None)
                capture.child_exit_confirmed = capture.readers_complete = False
                stop.apply(capture)
                capture._emit("meter_started", pid=capture.child_pid,
                              wrapper_pid=capture.wrapper_pid, child_pid=capture.child_pid,
                              time_ms=_now_ms(), child_exit_confirmed=False,
                              readers_complete=False)
                _notify(capture, notify,
                        "Wrapper PID " + str(capture.wrapper_pid) + " is supervising meter child PID "
                        + str(capture.child_pid) + ". Ctrl+C rejects the attempt and keeps capture "
                        "attached. Wrapper closure does not establish child exit.")
            result = _supervise(process, capture, notify, readers=readers, stop=stop)
        # A signal can arrive while the result is being built or the previous
        # handler is being restored. The child/readers are already finished,
        # but that late stop must still reject this attempt's returned result.
        if stop.requested and not result.cancelled:
            stop.apply(capture)
            result = capture.result(result.exit_code, _now_ms())
        return result
    except BaseException as error:
        if process is None:
            readers.abort()
            log("meter_launch_failed", simulated=False, error_type=type(error).__name__)
        # An unexpected post-launch failure is not reported as successful child
        # closure. Console/OS termination and arbitrary interpreter failures are
        # outside this bounded SIGINT policy; no termination/retry is attempted.
        raise
