#!/usr/bin/env python3
"""Demonstrate an MCP-shaped request with an explicit authorization boundary."""

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_TOOLS = {"repository.read"}
ALLOWED_OPERATIONS = {"read_file"}
ALLOWED_PREFIXES = ("examples/", "docs/")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.request.open(encoding="utf-8") as handle:
        request: dict[str, Any] = json.load(handle)
    reasons = []
    if request.get("tool") not in ALLOWED_TOOLS:
        reasons.append("tool is not allowlisted")
    if request.get("operation") not in ALLOWED_OPERATIONS:
        reasons.append("operation is not read-only")
    path = request.get("path", "")
    if not isinstance(path, str) or not path.startswith(ALLOWED_PREFIXES) or ".." in Path(path).parts:
        reasons.append("path is outside the read boundary")
    allowed = not reasons
    response = {
        "jsonrpc": "2.0",
        "id": request.get("id"),
        "decision": "allow" if allowed else "deny",
        "tool": request.get("tool"),
        "operation": request.get("operation"),
        "audit": {
            "policy": "repository-read-v1",
            "reasons": reasons,
            "network_calls": 0,
            "writes": 0,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(response, handle, indent=2)
        handle.write("\n")
    if not allowed:
        raise SystemExit("tool request denied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
