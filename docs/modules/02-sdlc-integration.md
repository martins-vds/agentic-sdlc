# Module 2 lab: Designing agent architecture and SDLC integration

## Goal

Connect a planner and implementer through a versioned artifact contract.

## Steps

1. Read `scripts/plan/generate_plan.py` and identify its input and output schema.
2. Generate a plan:

   ```bash
   mkdir -p /tmp/agentic-sdlc-plan
   python3 scripts/plan/generate_plan.py \
     --request examples/plan_request.json \
     --output /tmp/agentic-sdlc-plan/plan.json
   ```

3. Consume the plan:

   ```bash
   python3 scripts/implement/apply_plan.py \
     --plan /tmp/agentic-sdlc-plan/plan.json \
     --output /tmp/agentic-sdlc-plan/implementation.json
   ```

4. Inspect `plan.json`, `implementation.json`, and the generated `health-report.json` beside the manifest. The implementer performs the requested work, then records the report's SHA-256 digest and byte size so the handoff can verify exactly what was produced.
5. Run `sha256sum /tmp/agentic-sdlc-plan/health-report.json` and compare it with `generated_files[0].sha256` in the manifest.
6. Change the project status or an acceptance criterion in a copy of the request, rerun the scripts, and observe that the report and plan hashes change.
7. Open `.github/workflows/plan-implement.yml` and identify the artifact upload/download boundary between jobs.
8. Discuss how this handoff maps to an issue, pull request, Actions artifact, or required status check.

## Design takeaway

A handoff is an API. A downstream agent should not infer intent from prose when a producer can provide explicit fields, stable identifiers, and validation rules.

