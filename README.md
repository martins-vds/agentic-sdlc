# GitHub Certified: Agentic AI Developer Workshop

This repository is a hands-on workshop companion for the **GitHub Certified: Agentic AI Developer** learning experience. It adapts the themes of the six Microsoft Learn modules into original explanations, runnable local labs, facilitator notes, and GitHub Actions examples. It does **not** reproduce Microsoft Learn content; use the linked Microsoft pages for the authoritative curriculum and certification requirements.

## Workshop overview

Learners move from agent fundamentals to a governed, observable multi-agent SDLC:

1. **Foundations of Agentic AI in GitHub** - distinguish assistants from agents and model the plan -> act -> evaluate loop.
2. **Designing Agent Architecture and SDLC Integration** - define bounded responsibilities, contracts, handoffs, and workflow gates.
3. **Tooling, MCP, and Agent Execution Environments** - make tool boundaries explicit and run agents safely in Codespaces and Actions.
4. **Multi-Agent Systems and Orchestration** - coordinate specialist agents with concurrency, fan-in, and deterministic validation.
5. **Memory, State, and Evaluation** - persist useful state, preserve provenance, and enforce quality gates.
6. **Governance, Guardrails, and Operations** - apply least privilege, human approval, observability, rollback, and recovery.

## Prerequisites

- A GitHub account with access to GitHub Codespaces and GitHub Copilot CLI.
- Basic Git, Markdown, JSON, Bash, and Python 3 knowledge.
- A repository fork or copy opened in a Codespace.
- No API key is required for the deterministic labs in this repository.

Start in a Codespace, open the integrated terminal, and run:

```bash
chmod +x scripts/validate_workshop.sh scripts/run_multi_agent.sh
./scripts/validate_workshop.sh
```

Open the instructor deck at `slides/github-agentic-ai-developer-workshop.pptx`, or regenerate it with:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/presentation/generate_workshop_deck.py
```

The deck uses the GitHub Developer Training reference style and short, conversational instructor notes. Its reusable styling and font requirements are documented in [`docs/slides.md`](docs/slides.md#repository-powerpoint-style).

## Learning objectives

By the end of the workshop, learners can:

- Describe an agent as a bounded system with goals, tools, state, policies, and evaluation.
- Design an agent contract with explicit inputs, outputs, success criteria, and failure handling.
- Explain why MCP-style tool boundaries reduce accidental authority and improve auditability.
- Build a plan -> implement handoff using GitHub Actions artifacts.
- Run specialist agents concurrently, merge their outputs, and validate a fan-in result.
- Persist state with provenance and evaluate outputs against deterministic quality gates.
- Add least-privilege policies, approval gates, telemetry, and recovery paths to agentic workflows.
- Use GitHub Copilot CLI in Codespaces to inspect and coordinate custom agents.

## Suggested schedule

| Time | Activity |
| --- | --- |
| 00:00-00:20 | Welcome, environment check, and Module 1 |
| 00:20-00:55 | Module 2: contracts and SDLC integration |
| 00:55-01:35 | Module 3: tools, MCP boundaries, and execution |
| 01:35-02:50 | Module 4: deterministic fan-in and 45-minute Project Pulse lab |
| 02:50-03:30 | Module 5: memory and evaluation |
| 03:30-04:10 | Module 6: governance and operations |
| 04:10-04:40 | Capstone review, debrief, and certification mapping |

## Repository map

| Path | Purpose |
| --- | --- |
| `docs/curriculum.md` | Full six-module curriculum and delivery flow |
| `docs/source-coverage.md` | Unit-by-unit Microsoft Learn and GH-600 coverage map |
| `docs/facilitator-guide.md` | Instructor preparation, prompts, timing, and troubleshooting |
| `docs/slides.md` | Presentation narrative and regeneration instructions |
| `slides/github-agentic-ai-developer-workshop.pptx` | Editable 38-slide PowerPoint deck with speaker notes |
| `scripts/presentation/` | Reproducible PowerPoint generator |
| `docs/modules/` | Student-facing module guides and step-by-step labs |
| `labs/` | Lab-specific explanations and expected outcomes |
| `scripts/plan/` | Deterministic plan producer |
| `scripts/implement/` | Deterministic plan consumer and implementation manifest producer |
| `scripts/multi_agent/` | Spec analyzer, risk reviewer, plan merger, and validation |
| `scripts/project_pulse/` | Deterministic validator for the embedded Project Pulse lab |
| `.github/agents/` | Orchestrator, Planner, Designer, and Coder definitions used by the lab |
| `scripts/mcp/` | MCP-style tool-boundary demonstration |
| `scripts/memory/` | State persistence and quality evaluation |
| `scripts/governance/` | Guardrails, approvals, audit, and rollback examples |
| `.github/workflows/` | Runnable plan -> implement and multi-agent Actions workflows |
| `.devcontainer/` | Codespaces configuration |
| `examples/` | Input JSON documents used by the labs |

## Authoritative learning and certification links

- [GitHub Certified: Agentic AI Developer](https://learn.microsoft.com/en-us/credentials/certifications/agentic-ai-developer/)
- [Study guide for Exam GH-600](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600)
- [Developing in Agentic AI Systems, Part 1](https://learn.microsoft.com/en-us/training/paths/gh-developing-agentic-systems-1)
- [Developing in Agentic AI Systems, Part 2](https://learn.microsoft.com/en-us/training/paths/github-agentic-systems-part-two/github-agentic-systems-part-two)
- [Foundations of Agentic AI in GitHub](https://learn.microsoft.com/en-us/training/modules/foundations-agentic-ai/)
- [Designing Agent Architecture and SDLC Integration](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/)
- [Tooling, MCP, and Agent Execution Environments](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/)
- [Multi-Agent systems and orchestration](https://learn.microsoft.com/en-us/training/modules/multi-agent-systems-orchestration/)
- [Memory, State, and Evaluation](https://learn.microsoft.com/en-us/training/modules/memory-state-evaluation/)
- [Governance, Guardrails, and Operations](https://learn.microsoft.com/en-us/training/modules/governance-guardrails-operations/)
- [Multi-agent systems and orchestration exercise](https://learn.microsoft.com/en-us/training/modules/multi-agent-systems-orchestration/exercise)
- [Upstream Agent Orchestration template](https://github.com/skills/agent-orchestration-build-your-ai-dream-team)

The first three modules belong to Part 1 and the remaining three belong to Part 2.

## Required Project Pulse custom-agent lab

The Microsoft Learn **Build an AI dream team** exercise is embedded at [`labs/04-multi-agent/project-pulse/README.md`](labs/04-multi-agent/project-pulse/README.md). It includes the four custom-agent definitions, the Project Pulse brief, exact orchestration prompts, required dashboard outputs, launch instructions, and a local validator. Learners complete it directly in this repository rather than creating a separate template repository.

## Run the complete local demonstrations

```bash
./scripts/validate_workshop.sh
python3 scripts/mcp/tool_boundary.py \
  --request examples/mcp_request.json \
  --output /tmp/mcp-response.json
python3 scripts/memory/state_store.py init --path /tmp/agent-state.jsonl
python3 scripts/memory/state_store.py append --path /tmp/agent-state.jsonl \
  --event examples/state_event.json
python3 scripts/memory/state_store.py snapshot --path /tmp/agent-state.jsonl
./scripts/run_multi_agent.sh examples/project_spec.json /tmp/agent-run
# After completing the Project Pulse lab:
python3 scripts/project_pulse/validate_exercise.py --root .
```

The Actions workflows use the same scripts and exchange concrete JSON files through artifacts. They are safe by default: no model invocation, network access, repository mutation, or secret is required.
