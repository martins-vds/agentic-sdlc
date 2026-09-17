#!/usr/bin/env python3
"""Validate the multi-agent fan-in artifact."""

import argparse
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
    checks = {
        "schema_version": plan.get("schema_version") == "1.0",
        "has_work_items": bool(plan.get("work_items")),
        "has_risk_review": isinstance(plan.get("risks"), list),
        "has_fan_in": plan.get("handoff", {}).get("fan_in") is True,
        "decision_is_known": plan.get("decision") in {"ready_for_validation", "human_review_required"},
    }
    result = {
        "valid": all(checks.values()),
        "checks": checks,
        "project": plan.get("project"),
        "risk_score": plan.get("risk_score"),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    if not result["valid"]:
        raise SystemExit("multi-agent validation failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
