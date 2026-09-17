#!/usr/bin/env python3
"""Analyze project requirements into deterministic implementation concerns."""

import argparse
import json
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.spec.open(encoding="utf-8") as handle:
        spec: dict[str, Any] = json.load(handle)
    requirements = spec.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        raise ValueError("spec requires a non-empty requirements list")
    concerns = []
    for index, requirement in enumerate(requirements, start=1):
        concerns.append({
            "id": f"req-{index:02d}",
            "requirement": requirement,
            "implementation_area": "data" if "JSON" in requirement else "ui" if "dashboard" in requirement or "HTML" in requirement else "validation",
            "evidence": f"Add a test or artifact proving: {requirement}",
        })
    result = {
        "agent": "spec-analyzer",
        "project": spec.get("project"),
        "goal": spec.get("goal"),
        "requirements_count": len(requirements),
        "concerns": concerns,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
