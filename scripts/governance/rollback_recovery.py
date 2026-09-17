#!/usr/bin/env python3
"""Create a concrete rollback and recovery manifest for a proposed change."""

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.request.open(encoding="utf-8") as handle:
        request: dict[str, Any] = json.load(handle)
    changed_paths = request.get("changed_paths", [])
    manifest = {
        "run_id": request.get("run_id"),
        "rollback": {
            "trigger": "failed_validation_or_incident",
            "action": "revert_the_reviewed_pull_request",
            "protected_paths": changed_paths,
            "verification": "rerun_scripts/validate_workshop.sh_and_required_checks",
        },
        "recovery": {
            "owner": "repository-maintainer",
            "checkpoint": hashlib.sha256(json.dumps(changed_paths, sort_keys=True).encode()).hexdigest(),
            "escalation": "open_an_incident_and_pause_agent_runs",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
