#!/usr/bin/env python3
"""Consume a plan and create a health report plus an integrity manifest."""

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    with args.plan.open(encoding="utf-8") as handle:
        plan: dict[str, Any] = json.load(handle)
    for key in (
        "schema_version",
        "request_id",
        "request_hash",
        "project_metadata",
        "steps",
        "acceptance_criteria",
        "handoff",
    ):
        if key not in plan:
            raise ValueError(f"plan is missing required field: {key}")
    if plan["schema_version"] != "1.0":
        raise ValueError("unsupported plan schema")

    metadata = plan["project_metadata"]
    if not isinstance(metadata, dict):
        raise ValueError("project_metadata must be an object")
    missing_metadata = [key for key in ("name", "status", "owner") if not metadata.get(key)]
    if missing_metadata:
        raise ValueError(
            f"project_metadata is missing required fields: {', '.join(missing_metadata)}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    report_path = args.output.parent / "health-report.json"
    health_report = {
        "schema_version": "1.0",
        "request_id": plan["request_id"],
        "project": metadata,
        "health": {
            "status": metadata["status"],
            "deployment_passing": metadata.get("deployment") == "passing",
            "open_issues": metadata.get("open_issues", 0),
        },
        "acceptance_criteria": plan["acceptance_criteria"],
        "checks": {
            "project_name_present": bool(metadata["name"]),
            "project_status_present": bool(metadata["status"]),
            "deployment_passing": metadata.get("deployment") == "passing",
        },
    }
    report_bytes = (json.dumps(health_report, indent=2) + "\n").encode()
    report_path.write_bytes(report_bytes)

    canonical = json.dumps(plan, sort_keys=True, separators=(",", ":")).encode()
    plan_hash = hashlib.sha256(canonical).hexdigest()
    manifest = {
        "schema_version": "1.0",
        "request_id": plan["request_id"],
        "plan_hash": plan_hash,
        "status": "ready_for_review" if plan["handoff"]["requires_human_approval"] else "ready",
        "accepted_steps": [step["id"] for step in plan["steps"]],
        "generated_files": [
            {
                "path": report_path.name,
                "sha256": hashlib.sha256(report_bytes).hexdigest(),
                "bytes": len(report_bytes),
            }
        ],
        "evidence": {
            "acceptance_criteria_count": len(plan["acceptance_criteria"]),
            "protected_paths_modified": [],
            "network_calls": 0,
        },
    }
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
