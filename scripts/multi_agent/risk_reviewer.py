#!/usr/bin/env python3
"""Review a project specification for deterministic delivery risks."""

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
    requirements = spec.get("requirements", [])
    constraints = spec.get("constraints", [])
    risks = []
    if not any("JSON" in item for item in requirements):
        risks.append({"id": "R-001", "severity": "medium", "message": "Data format is unspecified"})
    if not any("validation" in item.lower() for item in requirements):
        risks.append({"id": "R-002", "severity": "high", "message": "No explicit validation requirement"})
    if not any("server" in item.lower() for item in constraints):
        risks.append({"id": "R-003", "severity": "low", "message": "Runtime hosting assumptions are unspecified"})
    high_risk_terms = {
        "delete": "destructive deletion",
        "production": "production environment impact",
        "secret": "secret access",
        "credential": "credential access",
        "deploy": "deployment authority",
        "payment": "financial operation",
    }
    requirement_text = " ".join(str(item).lower() for item in requirements)
    matched_risks = sorted({label for term, label in high_risk_terms.items() if term in requirement_text})
    if matched_risks:
        risks.append({
            "id": "R-004",
            "severity": "high",
            "message": "High-risk requirement requires human approval",
            "signals": matched_risks,
        })
    result = {
        "agent": "risk-reviewer",
        "project": spec.get("project"),
        "risk_count": len(risks),
        "risk_score": sum({"low": 1, "medium": 2, "high": 4}[risk["severity"]] for risk in risks),
        "risks": risks,
        "recommendation": "proceed_with_review" if any(r["severity"] == "high" for r in risks) else "proceed",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
