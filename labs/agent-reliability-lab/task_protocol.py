"""Validate task manifests before any agent is given work.

Validation only; this module never executes submitted code.
"""
import json
from pathlib import Path

class ManifestError(ValueError):
    pass

def validate_manifest(obj):
    if not isinstance(obj, dict):
        raise ManifestError("manifest must be an object")
    required = {"task_id", "revision", "repository", "base_commit", "time_limit_seconds",
                "cost_limit_usd", "evaluation"}
    if set(obj) != required:
        raise ManifestError("unexpected or missing manifest fields")
    for key in ("task_id", "revision", "repository", "base_commit"):
        if not isinstance(obj[key], str) or not obj[key].strip():
            raise ManifestError(f"{key} must be nonempty")
    if any(ch in obj["task_id"] for ch in "/\\\\"):
        raise ManifestError("task_id cannot contain path separators")
    if type(obj["time_limit_seconds"]) is not int or not 1 <= obj["time_limit_seconds"] <= 7200:
        raise ManifestError("time limit must be 1..7200 seconds")
    cost = obj["cost_limit_usd"]
    if type(cost) not in (int, float) or not 0 < cost <= 5:
        raise ManifestError("cost limit must be (0, 5] USD")
    evaluation = obj["evaluation"]
    if not isinstance(evaluation, dict) or set(evaluation) != {"test_command", "network"}:
        raise ManifestError("invalid evaluation policy")
    if evaluation["network"] != "deny":
        raise ManifestError("network must be denied for phase 1")
    if not isinstance(evaluation["test_command"], list) or not evaluation["test_command"] or any(
        not isinstance(x, str) or not x for x in evaluation["test_command"]
    ):
        raise ManifestError("test_command must be a nonempty argv array")
    # No shell execution in phase 1. This is a *policy* check, not sandboxing.
    if evaluation["test_command"][0] not in ("python3", "pytest"):
        raise ManifestError("unapproved evaluator executable")
    return obj

def load_manifest(path):
    return validate_manifest(json.loads(Path(path).read_text(encoding="utf-8")))
