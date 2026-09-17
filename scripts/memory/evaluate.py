#!/usr/bin/env python3
"""Run deterministic quality gates over a plan and an implementation/state file."""

import argparse
import json
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--implementation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.plan.open(encoding="utf-8") as handle:
        plan: dict[str, Any] = json.load(handle)
    checks = {
        "has_objective": bool(plan.get("objective")),
        "has_acceptance_criteria": bool(plan.get("acceptance_criteria")),
        "implementation_exists": args.implementation.exists(),
        "implementation_is_nonempty": args.implementation.stat().st_size > 0,
    }
    result = {"valid": all(checks.values()), "checks": checks, "evaluator": "deterministic-quality-gate-v1"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    if not result["valid"]:
        raise SystemExit("quality evaluation failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
