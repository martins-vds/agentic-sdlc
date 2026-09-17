#!/usr/bin/env python3
"""Validate the learner-created Project Pulse orchestration lab outputs."""

import argparse
import json
import re
from pathlib import Path
from typing import Any


class Validation:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.passes: list[str] = []

    def check(self, condition: bool, message: str) -> None:
        (self.passes if condition else self.failures).append(message)


def read_text(path: Path, result: Validation) -> str:
    if not path.is_file():
        result.check(False, f"{path} exists")
        return ""
    result.check(True, f"{path} exists")
    return path.read_text(encoding="utf-8")


def load_json(path: Path, result: Validation) -> Any:
    text = read_text(path, result)
    if not text:
        return None
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        result.check(False, f"{path} contains valid JSON: {error}")
        return None
    result.check(True, f"{path} contains valid JSON")
    return value


def contains_all(text: str, values: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return all(value.lower() in lowered for value in values)


def validate(root: Path) -> Validation:
    result = Validation()

    agent_team = read_text(root / "docs/agent-team.md", result)
    result.check(
        contains_all(agent_team, ("Orchestrator", "Planner", "Designer", "Coder", ".github/agents/")),
        "agent-team.md identifies all agents and their definition directory",
    )

    plan = read_text(root / "docs/project-pulse-plan.md", result)
    result.check(
        contains_all(
            plan,
            (
                "Project Pulse",
                "Designer",
                "Coder",
                "app/index.html",
                "app/styles.css",
                "app/project-data.json",
                ".vscode/launch.json",
                "parallel",
                "validation",
            ),
        ),
        "project plan covers ownership, dependencies, parallelism, and validation",
    )

    html = read_text(root / "app/index.html", result)
    result.check(
        contains_all(html, ("Project Pulse", "styles.css", "project-data.json", "project-card", "status", "recentActivity", "priority")),
        "dashboard HTML references the data source and required project fields",
    )
    executable_html = re.sub(r"<!--.*?-->|/\*.*?\*/|//[^\n]*", "", html, flags=re.DOTALL)
    fetches_project_data = bool(
        re.search(r"fetch\s*\(\s*['\"](?:\./)?project-data\.json['\"]", executable_html)
    )
    iterates_projects = bool(
        re.search(r"\b\w+\.projects\s*\.\s*(?:forEach|map)\s*\(", executable_html)
        or re.search(r"for\s*\([^)]*\bof\s+\w+\.projects\b", executable_html)
    )
    inserts_cards = (
        "project-card" in executable_html
        and any(token in executable_html for token in ("append(", "appendChild(", "innerHTML"))
    )
    result.check(
        fetches_project_data and iterates_projects and inserts_cards,
        "dashboard source fetches project-data.json, iterates projects, and inserts project cards",
    )

    css = read_text(root / "app/styles.css", result)
    result.check(
        contains_all(css, (".dashboard", ".project-card", "border-radius", "box-shadow", "@media")),
        "dashboard CSS provides card styling and a responsive rule",
    )

    data = load_json(root / "app/project-data.json", result)
    projects = data.get("projects") if isinstance(data, dict) else None
    result.check(
        isinstance(projects, list) and len(projects) >= 2,
        "project data has at least two projects for multiple visible cards",
    )
    if isinstance(projects, list):
        required_fields = {"name", "owner", "status", "recentActivity", "priority"}
        result.check(
            all(isinstance(project, dict) and required_fields <= project.keys() for project in projects),
            "every project contains name, owner, status, recentActivity, and priority",
        )

    launch = load_json(root / ".vscode/launch.json", result)
    configurations = launch.get("configurations", []) if isinstance(launch, dict) else []
    dashboard_launch = next(
        (
            item
            for item in configurations
            if isinstance(item, dict) and item.get("name") == "Run Project Pulse Dashboard"
        ),
        None,
    )
    result.check(dashboard_launch is not None, "launch configuration is named Run Project Pulse Dashboard")
    if dashboard_launch:
        command = dashboard_launch.get("command")
        if not command:
            command = " ".join(
                str(value)
                for value in (dashboard_launch.get("program"), *dashboard_launch.get("args", []))
                if value is not None
            )
        server_ready = dashboard_launch.get("serverReadyAction", {})
        uri = server_ready.get("uriFormat", "")
        result.check(dashboard_launch.get("type") == "node-terminal", "launch configuration uses the node-terminal debugger")
        result.check(dashboard_launch.get("request") == "launch", "launch configuration is runnable")
        result.check(dashboard_launch.get("cwd") == "${workspaceFolder}/app", "launch configuration serves from app/")
        result.check("python3" in command and "http.server" in command and "5500" in command, "launch configuration starts Python HTTP server on port 5500")
        result.check(server_ready.get("action") == "openExternally", "launch configuration opens the dashboard externally")
        result.check(bool(server_ready.get("pattern")), "launch configuration defines a server-ready pattern")
        result.check(bool(re.search(r"localhost:%s/index\.html", uri)), "launch configuration opens index.html")

    handoff = read_text(root / "docs/final-handoff.md", result)
    result.check(
        contains_all(
            handoff,
            (
                "Orchestrator",
                "Planner",
                "Designer",
                "Coder",
                "app/index.html",
                "app/styles.css",
                "app/project-data.json",
                ".vscode/launch.json",
                "Run Project Pulse Dashboard",
            ),
        ),
        "final handoff names every agent and deliverable",
    )
    headings = [line.lower() for line in handoff.splitlines() if line.startswith("#")]
    result.check(any("validation" in line for line in headings), "final handoff has a validation heading")
    result.check(any("handoff" in line for line in headings), "final handoff has a handoff heading")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    result = validate(args.root.resolve())
    for message in result.passes:
        print(f"PASS: {message}")
    for message in result.failures:
        print(f"FAIL: {message}")
    if result.failures:
        print(f"{len(result.failures)} validation check(s) failed.")
        return 1
    print("All Project Pulse validation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
