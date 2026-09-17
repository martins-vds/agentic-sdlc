# Slide/deck outline

The editable 38-slide PowerPoint deck is available at [`slides/github-agentic-ai-developer-workshop.pptx`](../slides/github-agentic-ai-developer-workshop.pptx). It includes speaker notes, editable vector diagrams, concrete workflow code, the Project Pulse lab, capstone guidance, and GH-600 mapping.

Regenerate it after changing workshop content:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/presentation/generate_workshop_deck.py
```

The headings below are the original concise narrative outline.

## 1. Title: From prompts to governed agentic SDLC

Speaker note: Set the expectation that this is an engineering workshop. The goal is not to make an agent appear autonomous; it is to make its authority and evidence explicit.

## 2. The six-module journey

Show the progression: foundations -> architecture -> tools -> orchestration -> memory/evaluation -> governance/operations.

## 3. What makes a system agentic?

Goal, plan, tool calls, observation, state, evaluation, and a stop/escalate policy. Contrast a one-shot assistant response with a bounded loop.

## 4. GitHub as the system of record

Issues, pull requests, workflow runs, artifacts, reviews, and protected branches make agent work inspectable.

## 5. Agent contracts

Display an example contract: inputs, outputs, allowed tools, forbidden actions, success criteria, timeout, and human escalation.

## 6. Plan -> implement handoff

Show `plan.json` moving between Actions jobs as an artifact. Emphasize schema validation and deterministic scripts.

## 7. Tool boundaries and MCP

Explain that a protocol boundary does not grant authority. The server/tool policy still needs allowlists, input validation, and read/write separation.

## 8. Execution environments

Compare Codespaces for interactive learning with Actions for repeatable automation. Discuss permissions and network assumptions.

## 9. Multi-agent topology

Draw Orchestrator -> Spec Analyzer and Risk Reviewer in parallel -> Plan Merger -> Validator. Mark the fan-in point.

## 10. The Project Pulse dream-team exercise

Open `labs/04-multi-agent/project-pulse/README.md`. Show the included Orchestrator, Planner, Designer, and Coder definitions, then explain the plan → delegate → implement → validate → handoff sequence and the local completion validator.

## 11. Memory is a product decision

Event log, snapshot, provenance, retention, and compaction. State should make recovery easier, not hide unexplained behavior.

## 12. Quality gates

Separate deterministic checks (schema, required files, risk thresholds) from subjective review. A failed gate is an explicit outcome.

## 13. Governance in practice

Least privilege, human approval for consequential actions, audit events, metrics, rollback, and recovery.

## 14. Capstone artifact set

Agent contract, tool policy, plan, specialist reports, merged plan, state snapshot, evaluation report, approval record, and rollback evidence.

## 15. Close: evidence over autonomy

Ask learners to name one action they would never allow an agent to perform without human approval.

