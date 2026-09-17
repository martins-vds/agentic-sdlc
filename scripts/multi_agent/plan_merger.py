#!/usr/bin/env python3
"""Merge specialist reports into one reviewable implementation plan."""

import argparse
import json
from pathlib import Path
from typing import Any


def read(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis", type=Path, required=True)
    parser.add_argument("--risks", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    analysis = read(args.analysis)
    risks = read(args.risks)
    if analysis.get("agent") != "spec-analyzer" or risks.get("agent") != "risk-reviewer":
        raise ValueError("unexpected specialist artifact")
    plan = {
        "schema_version": "1.0",
        "project": analysis.get("project"),
        "goal": analysis.get("goal"),
        "work_items": [
            {
                "id": concern["id"],
                "description": concern["requirement"],
                "evidence": concern["evidence"],
            }
            for concern in analysis["concerns"]
        ],
        "risks": risks["risks"],
        "risk_score": risks["risk_score"],
        "decision": "human_review_required" if risks["recommendation"] == "proceed_with_review" else "ready_for_validation",
        "handoff": {
            "from": ["spec-analyzer", "risk-reviewer"],
            "to": "implementer",
            "fan_in": True,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(plan, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
