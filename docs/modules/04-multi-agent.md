# Module 4 lab: Multi-agent systems and orchestration

## Goal

Run two independent specialist agents concurrently, merge their reports, and validate the fan-in result.

## Local lab

1. Inspect `examples/project_spec.json`.
2. Run the orchestrator:

   ```bash
   ./scripts/run_multi_agent.sh examples/project_spec.json /tmp/multi-agent-run
   ```

3. Inspect `spec_analysis.json`, `risk_review.json`, `merged_plan.json`, and `validation.json`.
4. Confirm that the analyzer and risk reviewer ran independently, the merger consumed both artifacts, and validation rejected no required field.
5. Change the project spec to add a high-risk requirement and rerun the lab. Observe the risk score and merged plan change.
6. Open `.github/workflows/multi-agent.yml` and map the local steps to the Actions jobs: parallel matrix, artifact upload, fan-in download, merge, and validation.

## Required Project Pulse exercise

Complete the embedded [Build an AI dream team with GitHub Copilot CLI](../../labs/04-multi-agent/project-pulse/README.md) lab. It faithfully preserves the Microsoft Learn exercise's Orchestrator → Planner → Designer/Coder → validation/handoff sequence and required Project Pulse files.

The custom agents are available in `.github/agents/`, the product brief is `.github/project-pulse-brief.md`, and the local completion check is:

```bash
python3 scripts/project_pulse/validate_exercise.py --root .
```

The [Microsoft Learn unit](https://learn.microsoft.com/en-ca/training/modules/multi-agent-systems-orchestration/exercise) and [GitHub Skills template](https://github.com/skills/agent-orchestration-build-your-ai-dream-team) remain the authoritative upstream sources. The GitHub Skills issue-driven grading workflows are intentionally replaced here by the local validator so the lab can coexist with the workshop workflows.

## Debrief

Concurrency is useful only when the fan-in contract is explicit. Ask what happens if one specialist fails, produces stale output, or disagrees with another specialist.

