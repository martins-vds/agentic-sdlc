#!/usr/bin/env python3
"""Append provenance-bearing events and create a deterministic state snapshot."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--path", type=Path, required=True)
    append = sub.add_parser("append")
    append.add_argument("--path", type=Path, required=True)
    append.add_argument("--event", type=Path, required=True)
    snapshot = sub.add_parser("snapshot")
    snapshot.add_argument("--path", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "init":
        args.path.parent.mkdir(parents=True, exist_ok=True)
        args.path.write_text("", encoding="utf-8")
        return 0
    if args.command == "append":
        with args.event.open(encoding="utf-8") as handle:
            event: dict[str, Any] = json.load(handle)
        current = events(args.path)
        record = {
            "sequence": len(current) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event["event_type"],
            "source": event["source"],
            "payload": event["payload"],
        }
        args.path.parent.mkdir(parents=True, exist_ok=True)
        with args.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
        return 0
    current = events(args.path)
    canonical = json.dumps(current, sort_keys=True, separators=(",", ":")).encode()
    snapshot = {
        "schema_version": "1.0",
        "event_count": len(current),
        "last_sequence": current[-1]["sequence"] if current else 0,
        "state_hash": hashlib.sha256(canonical).hexdigest(),
        "events": current,
    }
    output = args.path.with_suffix(args.path.suffix + ".snapshot.json")
    with output.open("w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=2)
        handle.write("\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
