#!/usr/bin/env python3
"""Record an explicit approval decision and audit event."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.decision.open(encoding="utf-8") as handle:
        decision: dict[str, Any] = json.load(handle)
    result = {
        "event_type": "guardrail.decision",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": decision.get("run_id"),
        "actor": "workshop-policy-engine",
        "decision": decision.get("decision"),
        "approval_required": decision.get("decision") == "approval_required",
        "reasons": decision.get("reasons", []),
        "rollback_reference": f"rollback/{decision.get('run_id')}.json",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
