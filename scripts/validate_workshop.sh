#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

required_files=(
  README.md
  .devcontainer/postCreate.sh
  docs/curriculum.md
  docs/source-coverage.md
  docs/facilitator-guide.md
  docs/slides.md
  slides/github-agentic-ai-developer-workshop.pptx
  scripts/presentation/generate_workshop_deck.py
  requirements-dev.txt
  docs/modules/01-foundations.md
  docs/modules/02-sdlc-integration.md
  docs/modules/03-tooling-mcp.md
  docs/modules/04-multi-agent.md
  docs/modules/05-memory-evaluation.md
  docs/modules/06-governance-operations.md
  .github/workflows/plan-implement.yml
  .github/workflows/multi-agent.yml
  .github/agents/orchestrator.agent.md
  .github/agents/planner.agent.md
  .github/agents/designer.agent.md
  .github/agents/coder.agent.md
  .github/project-pulse-brief.md
  labs/04-multi-agent/project-pulse/README.md
  scripts/project_pulse/validate_exercise.py
  scripts/plan/generate_plan.py
  scripts/implement/apply_plan.py
  scripts/multi_agent/spec_analyzer.py
  scripts/multi_agent/risk_reviewer.py
  scripts/multi_agent/plan_merger.py
  scripts/multi_agent/validate_artifacts.py
  scripts/mcp/tool_boundary.py
  scripts/memory/state_store.py
  scripts/memory/evaluate.py
  scripts/governance/guardrails.py
  scripts/governance/approval_audit.py
  scripts/governance/rollback_recovery.py
)

for file in "${required_files[@]}"; do
  [[ -f "$file" ]] || { echo "missing required file: $file" >&2; exit 1; }
done

python3 - <<'PY'
from pathlib import Path

for path in Path("scripts").rglob("*.py"):
    compile(path.read_text(encoding="utf-8"), str(path), "exec")
PY
python3 -m json.tool examples/plan_request.json >/dev/null
python3 -m json.tool examples/project_spec.json >/dev/null
python3 -m json.tool examples/mcp_request.json >/dev/null
python3 -m json.tool examples/state_event.json >/dev/null
python3 -m json.tool examples/governance_request.json >/dev/null
bash -n scripts/validate_workshop.sh scripts/run_multi_agent.sh .devcontainer/postCreate.sh
python3 -m unittest discover -s tests

python3 - <<'PY'
from pathlib import Path

workflow_refs = {
    ".github/workflows/plan-implement.yml": (
        "scripts/plan/generate_plan.py",
        "scripts/implement/apply_plan.py",
    ),
    ".github/workflows/multi-agent.yml": (
        "scripts/multi_agent/spec_analyzer.py",
        "scripts/multi_agent/risk_reviewer.py",
        "scripts/multi_agent/plan_merger.py",
        "scripts/multi_agent/validate_artifacts.py",
    ),
}
for workflow, references in workflow_refs.items():
    text = Path(workflow).read_text(encoding="utf-8")
    for reference in references:
        if not Path(reference).is_file() or reference not in text:
            raise SystemExit(f"{workflow} has an invalid script reference: {reference}")
PY

python3 scripts/plan/generate_plan.py \
  --request examples/plan_request.json --output /tmp/workshop-plan.json
python3 scripts/implement/apply_plan.py \
  --plan /tmp/workshop-plan.json --output /tmp/workshop-implementation.json
python3 scripts/mcp/tool_boundary.py \
  --request examples/mcp_request.json --output /tmp/workshop-mcp.json
python3 scripts/memory/state_store.py init --path /tmp/workshop-state.jsonl
python3 scripts/memory/state_store.py append \
  --path /tmp/workshop-state.jsonl --event examples/state_event.json
python3 scripts/memory/state_store.py snapshot --path /tmp/workshop-state.jsonl >/dev/null
python3 scripts/memory/evaluate.py \
  --plan examples/plan_request.json \
  --implementation /tmp/workshop-state.jsonl \
  --output /tmp/workshop-evaluation.json
python3 scripts/governance/guardrails.py \
  --request examples/governance_request.json \
  --output /tmp/workshop-guardrail.json
python3 scripts/governance/approval_audit.py \
  --decision /tmp/workshop-guardrail.json \
  --output /tmp/workshop-audit.json
python3 scripts/governance/rollback_recovery.py \
  --request examples/governance_request.json \
  --output /tmp/workshop-rollback.json
./scripts/run_multi_agent.sh examples/project_spec.json /tmp/workshop-multi-agent >/dev/null

python3 - <<'PY'
import hashlib
import json
from pathlib import Path

for path in (
    Path("/tmp/workshop-implementation.json"),
    Path("/tmp/health-report.json"),
    Path("/tmp/workshop-mcp.json"),
    Path("/tmp/workshop-evaluation.json"),
    Path("/tmp/workshop-guardrail.json"),
    Path("/tmp/workshop-audit.json"),
    Path("/tmp/workshop-rollback.json"),
    Path("/tmp/workshop-multi-agent/validation.json"),
):
    with path.open(encoding="utf-8") as handle:
        json.load(handle)

manifest = json.loads(Path("/tmp/workshop-implementation.json").read_text())
report_path = Path("/tmp/health-report.json")
assert manifest["generated_files"][0]["path"] == "health-report.json"
assert manifest["generated_files"][0]["sha256"] == hashlib.sha256(report_path.read_bytes()).hexdigest()
assert json.loads(report_path.read_text())["project"]["status"] == "healthy"
assert json.loads(Path("/tmp/workshop-mcp.json").read_text())["decision"] == "allow"
assert json.loads(Path("/tmp/workshop-evaluation.json").read_text())["valid"] is True
assert json.loads(Path("/tmp/workshop-multi-agent/validation.json").read_text())["valid"] is True
print("Workshop validation passed")
PY
