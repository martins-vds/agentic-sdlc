# Module 5 lab: Memory, state, and evaluation

## Goal

Persist a compact event history with provenance, create a snapshot hash, and evaluate an implementation artifact.

## Steps

1. Initialize state:

   ```bash
   rm -f /tmp/agent-state.jsonl
   python3 scripts/memory/state_store.py init --path /tmp/agent-state.jsonl
   ```

2. Append the sample event and create a snapshot:

   ```bash
   python3 scripts/memory/state_store.py append \
     --path /tmp/agent-state.jsonl \
     --event examples/state_event.json
   python3 scripts/memory/state_store.py snapshot --path /tmp/agent-state.jsonl
   ```

3. Run the quality evaluator:

   ```bash
   python3 scripts/memory/evaluate.py \
     --plan examples/plan_request.json \
     --implementation /tmp/agent-state.jsonl \
     --output /tmp/evaluation.json
   cat /tmp/evaluation.json
   ```

4. Inspect the event source, timestamp, sequence number, and snapshot hash.
5. Explain what should be retained, redacted, compacted, or deleted in a production system.

## Completion check

You can distinguish durable state from ephemeral context and can name at least two deterministic quality gates.

