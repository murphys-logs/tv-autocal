"""Explicit, owner-supplied execution attestation; not an approval authority."""

from dataclasses import dataclass
from re import fullmatch


@dataclass(frozen=True)
class HardwarePermit:
    plan: str
    revision: str
    authorisation: str
    steps: str
    evidence: str
    actions: tuple[str, ...]
    hardware: bool = False

    def require(self, action: str) -> None:
        if self.hardware is not True:
            raise PermissionError("Hardware is disabled; simulation is the default")
        permitted = {"T-003": {"present", "meter"},
                     "T-005": {"present", "meter"}, "T-006": {"serial"}}
        if self.plan not in permitted or action not in permitted[self.plan]:
            raise PermissionError("Action does not belong to this component plan")
        if type(self.actions) is not tuple or not self.actions or any(
            type(item) is not str or item not in permitted[self.plan] for item in self.actions
        ) or action not in self.actions:
            raise PermissionError("Action is outside the explicitly authorised scope")
        if type(self.revision) is not str or fullmatch(r"[0-9a-f]{40}", self.revision) is None:
            raise PermissionError("A full reviewed plan commit is required")
        for value in (self.authorisation, self.steps, self.evidence):
            if type(value) is not str or not 1 <= len(value.strip()) <= 4096:
                raise PermissionError("Owner authorisation, steps and prerequisite evidence are required")


def permit_from_dict(value: dict, *, hardware: bool, confirmation: str) -> HardwarePermit:
    if type(value) is not dict or set(value) != {
        "plan", "revision", "authorisation", "steps", "evidence", "actions"
    }:
        raise ValueError("Permit needs exactly the documented fields")
    if type(value["actions"]) is not list:
        raise ValueError("Permit actions must be a list")
    permit = HardwarePermit(**{**value, "actions": tuple(value["actions"])}, hardware=hardware)
    if confirmation != "RUN " + str(permit.plan) + " " + str(permit.revision):
        raise PermissionError("Exact plan/commit confirmation is required")
    return permit
