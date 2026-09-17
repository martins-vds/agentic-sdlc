# Microsoft Learn source coverage

This map keeps the workshop aligned with the six public Microsoft Learn modules without reproducing their prose. Each source topic points to an explanation, executable example, or learner activity in this repository.

## Part 1

### Foundations of Agentic AI in GitHub — 8 units

| Source unit/topic | Workshop coverage |
| --- | --- |
| Introduction | `README.md`, `docs/curriculum.md` |
| Define agentic AI in the SDLC | `docs/modules/01-foundations.md` agent contract activity |
| Plan → act → evaluate lifecycle | `scripts/plan/generate_plan.py`, `scripts/implement/apply_plan.py`, `scripts/memory/evaluate.py` |
| GitHub as system of record and control plane | Artifact-based workflows in `.github/workflows/` |
| Responsibilities, risks, anti-patterns, traceability | Contract fields in `examples/plan_request.json` and governance artifacts |
| Contributor model for agent-generated work | Human approval, evidence, and review prompts in Modules 1 and 6 |
| Knowledge check | Facilitator prompts and capstone rubric |
| Summary | Module completion check and debrief |

### Designing Agent Architecture and SDLC Integration — 9 units

| Source unit/topic | Workshop coverage |
| --- | --- |
| Introduction | `docs/modules/02-sdlc-integration.md` |
| Map agent responsibilities to the SDLC | Planner/implementer/validator ownership in generated plans |
| Define inputs, outputs, and success criteria | Versioned JSON request and plan contracts |
| Separate planning, reasoning, and execution | Separate plan and implementation scripts/jobs |
| PR governance controls | Module discussion of checks, CODEOWNERS, rules, and environments |
| Reliable workflows and cross-job handoffs | `plan-implement.yml` artifact upload/download implementation |
| Agent operations, observability, tools, secrets, hooks, reliability | Evidence fields, hashes, read-only permissions, and validation |
| Knowledge check | Lab inspection questions |
| Summary | Design takeaway and completion output |

### Tooling, MCP, and Agent Execution Environments — 8 units

| Source unit/topic | Workshop coverage |
| --- | --- |
| Introduction | `docs/modules/03-tooling-mcp.md` |
| GitHub APIs and workflows | Tool request schema and Actions examples |
| MCP servers, registries, and allowlists | `scripts/mcp/tool_boundary.py` |
| Execution context and boundaries | Repository, operation, and path allowlists |
| Execution limits and protections | Denied-write exercise and least-privilege workflow permissions |
| Agentic Workflows exercise theme | Concrete workflow files and local equivalents |
| Module assessment | Allowed/denied request evidence |
| Summary | Protocol-versus-authorization debrief |

## Part 2

### Multi-Agent Systems and Orchestration — 10 units

| Source unit/topic | Workshop coverage |
| --- | --- |
| Introduction | `docs/modules/04-multi-agent.md` |
| Define multi-agent responsibilities | Specialist schemas and `.github/agents/` role definitions |
| Orchestrate with GitHub workflows | Matrix specialists and fan-in job in `multi-agent.yml` |
| Isolate branches, workflows, permissions, and concurrency | Read-only permissions and branch-scoped concurrency group |
| Detect and resolve conflicts | Explicit merger and validation contracts |
| Attribution, evidence, and handoffs | Named agent outputs and uploaded artifacts |
| Diagnose failures and recover safely | `fail-fast: false`, required artifacts, and nonzero validators |
| Project Pulse exercise | `labs/04-multi-agent/project-pulse/README.md` |
| Knowledge check | Lab debrief questions |
| Summary | Merged-plan and final-handoff outcomes |

### Memory, State, and Evaluation — 8 units

| Source unit/topic | Workshop coverage |
| --- | --- |
| Introduction | `docs/modules/05-memory-evaluation.md` |
| Agent memory strategies | Event log and snapshot model |
| Persist state and manage context drift | `scripts/memory/state_store.py` sequence and hash checks |
| Continuity across tools and environments | Portable JSONL state and provenance fields |
| Evaluation signals and quality gates | `scripts/memory/evaluate.py` |
| Analyze failures and improve behavior | Failed checks remain explicit in evaluation output |
| Knowledge check | Retention and stale-state discussion |
| Summary | Module completion check |

### Governance, Guardrails, and Operations — 9 units

| Source unit/topic | Workshop coverage |
| --- | --- |
| Introduction | `docs/modules/06-governance-operations.md` |
| Risk-based autonomy and action boundaries | `scripts/governance/guardrails.py` |
| GitHub-native governance controls | Ruleset, check, CODEOWNERS, and environment discussion |
| Human-in-the-loop workflows | Approval-required decision and audit record |
| Least-privilege capabilities | Explicit allowed actions and protected paths |
| Observable, traceable, auditable actions | `scripts/governance/approval_audit.py` |
| Governance reliability and recovery | `scripts/governance/rollback_recovery.py` |
| Knowledge check | Operational evidence discussion |
| Summary | Reversible-change operational rule |

## Certification-domain mapping

| GH-600 domain | Primary workshop modules |
| --- | --- |
| Prepare agent architecture and SDLC processes | Modules 1–2 |
| Implement tool use and environment interaction | Module 3 |
| Manage memory, state, and execution | Module 5 plus workflow artifacts |
| Perform evaluation, error analysis, and tuning | Module 5 and all deterministic validators |
| Orchestrate multi-agent coordination | Module 4 and Project Pulse lab |
| Implement guardrails and accountability | Module 6 |
