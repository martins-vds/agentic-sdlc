# Lab: Build an AI dream team with GitHub Copilot CLI

**Duration:** 45 minutes  
**Source exercise:** [Microsoft Learn](https://learn.microsoft.com/en-ca/training/modules/multi-agent-systems-orchestration/exercise) and [GitHub Skills](https://github.com/skills/agent-orchestration-build-your-ai-dream-team)

This in-repository adaptation preserves the upstream exercise's four-agent sequence and Project Pulse deliverables while replacing its issue-driven grader with a local validator.

## Outcome

Use the custom agents in `.github/agents/` to plan, design, implement, validate, and hand off Mona's Project Pulse dashboard. You will create:

- `docs/agent-team.md`
- `docs/project-pulse-plan.md`
- `app/index.html`
- `app/styles.css`
- `app/project-data.json`
- `.vscode/launch.json`
- `docs/final-handoff.md`

## Prerequisites

- A GitHub account with GitHub Copilot access
- GitHub Codespaces or a local environment with GitHub Copilot CLI
- Basic Git and Markdown knowledge

Open this repository in a Codespace. If Copilot CLI is not already running, authenticate and start it:

```bash
copilot
```

Grant only the permissions needed for the lab. The upstream exercise uses `--allow-all --enable-all-github-mcp-tools` for convenience; review that broader authority before using it.

## Step 1: Meet the agent team

Inspect `.github/agents/` and ask Copilot CLI:

```text
Inspect .github/agents/ and summarize the custom agent team I will use to build
Mona's Project Pulse dashboard.

Create docs/agent-team.md. Include each agent's name, model, responsibility,
definition file, and how the team will work together.
```

Confirm the document covers **Orchestrator**, **Planner**, **Designer**, and **Coder**.

## Step 2: Plan with Orchestrator and Planner

Run `/agent` in Copilot CLI, select **Orchestrator**, and submit:

```text
Ask the Planner to create an implementation plan for the Project Pulse dashboard
using .github/project-pulse-brief.md.

Save the plan in docs/project-pulse-plan.md.
Include app/index.html, app/styles.css, app/project-data.json, and
.vscode/launch.json in the file assignments.
Include Designer and Coder responsibilities, dependencies, parallel work
decisions, edge cases, and validation expectations.
Do not implement the dashboard yet.
```

Review the plan. File ownership must not overlap, data must exist before integration is validated, and the launch configuration must depend on the final app path.

## Step 3: Delegate design and implementation

Keep **Orchestrator** selected and submit:

```text
Use docs/project-pulse-plan.md and .github/project-pulse-brief.md.
Delegate visual structure and accessibility decisions to Designer, then delegate
implementation to Coder using the file boundaries in the plan.

Create app/index.html, app/styles.css, and app/project-data.json.
Use the exact page title "Project Pulse". Load styles.css and
project-data.json, render visible elements with class project-card, and show each
project's status, recentActivity, and priority.

In styles.css include .dashboard and .project-card selectors, border-radius,
box-shadow, readable contrast, keyboard-visible focus styles, and a responsive
@media rule.

In project-data.json use a top-level projects array. Every project must include
name, owner, status, recentActivity, and priority.

Create .vscode/launch.json as strict JSON. Add a configuration named
"Run Project Pulse Dashboard" that runs python3 -m http.server 5500 with cwd
${workspaceFolder}/app and serverReadyAction opening
http://localhost:%s/index.html.

Validate JSON syntax and report every file changed.
```

Inspect the files instead of accepting the completion message as evidence.

## Step 4: Run and inspect the dashboard

In VS Code, open **Run and Debug**, choose **Run Project Pulse Dashboard**, and start it. Verify:

- the browser opens `index.html`, not a directory listing;
- multiple project cards are visible;
- name, owner, status, recent activity, and priority appear;
- the layout remains readable at narrow and wide viewport sizes;
- browser developer tools show no load or JavaScript errors.

Stop the preview server after inspection.

## Step 5: Validate and hand off

With **Orchestrator** selected, submit:

```text
Review docs/agent-team.md, docs/project-pulse-plan.md, app/, and
.vscode/launch.json. Run:
python3 scripts/project_pulse/validate_exercise.py --root .

Fix validation failures by delegating to the responsible specialist. Then write
docs/final-handoff.md. Name Orchestrator, Planner, Designer, and Coder; list
app/index.html, app/styles.css, app/project-data.json, and .vscode/launch.json;
include the launch name "Run Project Pulse Dashboard"; and include headings
containing the lowercase words "validation" and "handoff".
```

Run the validator yourself as final evidence:

```bash
python3 scripts/project_pulse/validate_exercise.py --root .
```

The validator checks file structure, JSON schemas, source wiring, required fields, and launch configuration. It does not execute browser JavaScript, so visual inspection and a clean browser console remain required evidence. The lab is complete only when all checks pass and the rendered dashboard has been inspected.

## Debrief

- Which tasks could run in parallel without overlapping file ownership?
- What artifact let one specialist safely continue another specialist's work?
- What did deterministic validation prove, and what still required human judgment?
- Which permissions could be removed from each agent without blocking its role?

## Attribution

Adapted from GitHub's **Agent Orchestration: Build Your AI Dream Team** exercise and its Microsoft Learn unit, accessed September 16, 2026. The upstream repository identifies its exercise materials as MIT licensed. Upstream automation and grading workflows are intentionally not copied because this workshop uses local validation and does not run as a GitHub Skills course.
