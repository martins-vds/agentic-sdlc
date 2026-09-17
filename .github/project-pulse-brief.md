# Project Pulse dashboard brief

Mona's team needs a lightweight Project Pulse dashboard for contributors.

The dashboard should help the team quickly understand:

- which projects are active;
- who owns each project;
- each project's current status;
- recent activity;
- priority or risk level;
- a short contributor-friendly summary;
- a polished visual layout with project cards, status badges, and readable spacing.

The final dashboard must contain:

- `app/index.html`
- `app/styles.css`
- `app/project-data.json`
- `.vscode/launch.json`

The launch configuration must be named **Run Project Pulse Dashboard**, serve from `app/`, and open `index.html` rather than a directory listing.

Use a top-level `projects` array in `app/project-data.json`. Every project must include `name`, `owner`, `status`, `recentActivity`, and `priority`.

Use the custom agents in `.github/agents/`: Orchestrator coordinates, Planner creates phases and ownership, Designer defines the experience, and Coder implements the dashboard. The learner should use GitHub Copilot CLI to practice orchestration instead of submitting one undifferentiated implementation prompt.
