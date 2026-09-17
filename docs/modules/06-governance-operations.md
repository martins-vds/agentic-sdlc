# Module 6 lab: Governance, guardrails, and operations

## Goal

Evaluate a proposed file change with least privilege, approval, audit, and rollback evidence.

## Steps

1. Read `examples/governance_request.json`.
2. Run the guardrail evaluator:

   ```bash
   python3 scripts/governance/guardrails.py \
     --request examples/governance_request.json \
     --output /tmp/guardrail-decision.json
   ```

3. Run the approval and audit demo:

   ```bash
   python3 scripts/governance/approval_audit.py \
     --decision /tmp/guardrail-decision.json \
     --output /tmp/audit.json
   ```

4. Inspect why the request is `approval_required` rather than silently executed.
5. Create a rollback manifest:

   ```bash
   python3 scripts/governance/rollback_recovery.py \
     --request examples/governance_request.json \
     --output /tmp/rollback.json
   ```

6. Discuss observability fields: run ID, actor, decision, changed paths, policy version, timestamps, and recovery reference.

## Operational rule

Consequential actions must have a reversible change, an approval boundary, and an audit event. A failed guardrail is a safe result, not an exception to hide.

