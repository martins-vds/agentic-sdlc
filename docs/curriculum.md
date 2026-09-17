# Workshop curriculum

## Delivery model

Use a short concept briefing, a guided terminal demonstration, an individual or pair lab, and a debrief for each module. Keep the repository open in a Codespace throughout. The intended rhythm is **explain -> inspect -> run -> modify -> validate -> discuss**.

Use [`source-coverage.md`](source-coverage.md) to trace every Microsoft Learn unit and GH-600 exam domain to workshop material.

## Module 1 - Foundations of Agentic AI in GitHub

**Purpose:** Establish a shared vocabulary and a lifecycle model.

**Concepts:** assistant versus agent, goal decomposition, tools, context, state, policy, evaluator, plan -> act -> observe -> evaluate, GitHub as system of record.

**Student outcome:** A written agent contract for a repository task, including objective, allowed tools, inputs, outputs, stop conditions, and human escalation.

**Lab:** `docs/modules/01-foundations.md`

## Module 2 - Designing Agent Architecture and SDLC Integration

**Purpose:** Turn a vague automation request into composable responsibilities and workflow gates.

**Concepts:** single-responsibility agents, handoff schemas, idempotency, artifact contracts, pull-request integration, branch protection, deterministic versus model-driven steps.

**Student outcome:** A plan contract and a plan -> implement handoff that exchanges versioned JSON artifacts.

**Lab:** `docs/modules/02-sdlc-integration.md`

## Module 3 - Tooling, MCP, and Agent Execution Environments

**Purpose:** Make authority visible and constrained at the tool boundary.

**Concepts:** MCP as a protocol boundary, read/write separation, input validation, Codespaces versus Actions, timeouts, permissions, provenance, and safe defaults.

**Student outcome:** A tool policy and a runnable boundary checker that denies an unapproved write operation.

**Lab:** `docs/modules/03-tooling-mcp.md`

## Module 4 - Multi-Agent Systems and Orchestration

**Purpose:** Practice specialist delegation, concurrency, fan-in, and cross-agent validation.

**Concepts:** orchestrator, specialist roles, independent work, fan-in, conflict resolution, partial failure, and final acceptance criteria.

**Student outcome:** A merged implementation plan built from a spec analyzer and risk reviewer running concurrently.

**Lab:** `docs/modules/04-multi-agent.md`

**Required Project Pulse exercise:** Complete the embedded [Build an AI dream team](../labs/04-multi-agent/project-pulse/README.md) lab. Learners use the included Orchestrator, Planner, Designer, and Coder definitions to create Mona's Project Pulse dashboard, launch it in Codespaces, run deterministic validation, and document the final handoff. The deterministic fan-in lab remains a complementary exercise for inspecting artifact coordination without model variability.

## Module 5 - Memory, State, and Evaluation

**Purpose:** Preserve useful context without turning state into an unbounded or unverifiable transcript.

**Concepts:** event log, snapshots, provenance, state compaction, deterministic quality gates, evaluation datasets, regression checks, and human review.

**Student outcome:** A state file with a verifiable hash and an evaluation report with pass/fail reasons.

**Lab:** `docs/modules/05-memory-evaluation.md`

## Module 6 - Governance, Guardrails, and Operations

**Purpose:** Make agentic automation safe to operate in a real repository.

**Concepts:** least privilege, protected branches, approval gates, secret boundaries, audit events, metrics, rollback, recovery, and incident handling.

**Student outcome:** A guardrail decision, approval record, audit trail, and rollback plan for a proposed change.

**Lab:** `docs/modules/06-governance-operations.md`

## Capstone

Learners propose one repository workflow and submit:

- an agent contract;
- a tool and permission policy;
- a plan artifact;
- at least two specialist outputs and a merged result;
- a state snapshot and evaluation report;
- an approval/audit record and rollback procedure.

The facilitator grades the artifacts for bounded authority, reproducibility, observability, and explicit failure handling rather than for model quality.

