#!/usr/bin/env python3
"""Generate a deterministic implementation plan from a JSON request."""

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    request = load_json(args.request)
    required = (
        "request_id",
        "objective",
        "project_metadata",
        "constraints",
        "acceptance_criteria",
        "risk_level",
    )
    missing = [key for key in required if key not in request]
    if missing:
        raise ValueError(f"request is missing required fields: {', '.join(missing)}")
    if not isinstance(request["acceptance_criteria"], list) or not request["acceptance_criteria"]:
        raise ValueError("acceptance_criteria must be a non-empty list")
    metadata = request["project_metadata"]
    if not isinstance(metadata, dict):
        raise ValueError("project_metadata must be an object")
    missing_metadata = [key for key in ("name", "status", "owner") if not metadata.get(key)]
    if missing_metadata:
        raise ValueError(
            f"project_metadata is missing required fields: {', '.join(missing_metadata)}"
        )
    canonical = json.dumps(request, sort_keys=True, separators=(",", ":")).encode()
    request_hash = hashlib.sha256(canonical).hexdigest()
    steps = [
        {"id": "inspect", "description": "Inspect repository context and protected paths", "owner": "planner"},
        {"id": "implement", "description": request["objective"], "owner": "implementer"},
        {"id": "validate", "description": "Run every acceptance criterion and record evidence", "owner": "validator"},
    ]
    plan = {
        "schema_version": "1.0",
        "request_id": request["request_id"],
        "request_hash": request_hash,
        "objective": request["objective"],
        "project_metadata": request["project_metadata"],
        "risk_level": request["risk_level"],
        "constraints": request["constraints"],
        "acceptance_criteria": request["acceptance_criteria"],
        "steps": steps,
        "handoff": {
            "producer": "deterministic-planner",
            "consumer": "deterministic-implementer",
            "requires_human_approval": request["risk_level"] in {"high", "critical"},
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(plan, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
