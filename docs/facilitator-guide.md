# Facilitator guide

## Before the session

1. Open this repository in a GitHub Codespace and run `./scripts/validate_workshop.sh`.
2. Confirm that Python 3, Bash, Git, and the GitHub Copilot CLI are available.
3. Review the included custom agents in `.github/agents/` and run through `labs/04-multi-agent/project-pulse/README.md` once in a disposable branch or copy.
4. Review `.github/workflows/plan-implement.yml` and `.github/workflows/multi-agent.yml` so you can show the artifact handoff.
5. Prepare a projector view of `docs/slides.md` or convert it into the deck format used by your organization.

## Facilitation principles

- Keep asking: **What can this agent do, and what is it explicitly unable to do?**
- Prefer an observable artifact over a claim that an agent completed work.
- Separate deterministic checks from model judgment.
- Treat a failed or denied action as a useful learning outcome.
- Never ask learners to paste secrets into a prompt or workflow.

## Suggested prompts

| Moment | Prompt |
| --- | --- |
| Foundations | "What evidence would convince you that this was an agent action rather than a completion message?" |
| Architecture | "Which fields must be in a handoff so a different process can continue safely?" |
| Tooling | "If the agent can call a tool, what is the narrowest permission that tool needs?" |
| Orchestration | "Which steps can run concurrently, and where must we fan in?" |
| Memory | "What state is worth retaining, and how will you detect stale state?" |
| Governance | "Who can stop, approve, or recover this workflow?" |

## Timing and checkpoints

- **20 minutes:** Every learner has run the validator and can identify the six module folders.
- **55 minutes:** Every learner has generated a plan and consumed it through the implementation script.
- **150 minutes:** Every learner has run the deterministic fan-in and completed or reached validation in the 45-minute Project Pulse exercise.
- **220 minutes:** Every learner has produced a state snapshot, evaluation report, guardrail decision, and audit event.
- **End:** Each learner explains one denied action and one recovery path.

## Troubleshooting

**The validator says a script is not executable.** Run `chmod +x scripts/validate_workshop.sh scripts/run_multi_agent.sh` and rerun the validator.

**A workflow does not appear in Actions.** Push the repository to GitHub, confirm the workflow file is under `.github/workflows/`, and use the Actions tab. The workflows need no secrets.

**Copilot CLI does not list the custom agents.** Confirm the learner opened the repository root, the four definitions exist under `.github/agents/`, and the CLI session was started after those files were available. Restart Copilot CLI, run `/agent`, and select **Orchestrator**.

**A learner wants to add a live model.** Keep the deterministic scripts as the acceptance baseline. A model-backed step may propose text, but it must still produce the same schema and pass the same validators.

## Assessment rubric

| Area | Meets expectations when the learner... |
| --- | --- |
| Architecture | Defines a bounded role, schema, stop condition, and escalation path |
| Tool safety | Denies an unapproved tool or parameter and records the decision |
| Orchestration | Runs independent specialists concurrently and merges their outputs |
| State | Stores events with timestamps, source, and a verifiable snapshot |
| Evaluation | Uses explicit checks and reports failures rather than silently accepting output |
| Governance | Applies least privilege, human approval, observability, and rollback |

