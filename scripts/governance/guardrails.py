#!/usr/bin/env python3
"""Evaluate least privilege and approval requirements for a proposed action."""

import argparse
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
    permissions = set(request.get("permissions", []))
    reasons = []
    if "contents:write" in permissions:
        reasons.append("contents:write is broader than required for pull request creation")
    if "pull-requests:write" not in permissions:
        reasons.append("pull request write permission is missing")
    approval = request.get("approval", {})
    if request.get("protected_branch") and not approval.get("present", False):
        reasons.append("protected branch requires human approval")
    decision = "deny" if any("broader" in reason or "missing" in reason for reason in reasons) else "approval_required" if reasons else "allow"
    result = {
        "run_id": request.get("run_id"),
        "decision": decision,
        "reasons": reasons,
        "policy_version": request.get("policy_version"),
        "required_permissions": ["contents:read", "pull-requests:write"],
        "changed_paths": request.get("changed_paths", []),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
