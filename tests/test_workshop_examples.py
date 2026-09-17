import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class PlanImplementationTests(unittest.TestCase):
    def test_plan_consumer_creates_real_health_report_with_integrity_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            plan = output_dir / "plan.json"
            manifest = output_dir / "implementation" / "implementation.json"

            subprocess.run(
                [sys.executable, "scripts/plan/generate_plan.py", "--request", "examples/plan_request.json", "--output", str(plan)],
                cwd=REPO,
                check=True,
            )
            subprocess.run(
                [sys.executable, "scripts/implement/apply_plan.py", "--plan", str(plan), "--output", str(manifest)],
                cwd=REPO,
                check=True,
            )

            report_path = manifest.parent / "health-report.json"
            self.assertTrue(report_path.is_file(), "implementer must create the promised health report")
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["project"]["name"], "agentic-sdlc-demo")
            self.assertEqual(report["project"]["status"], "healthy")

            result = json.loads(manifest.read_text(encoding="utf-8"))
            generated = {item["path"]: item for item in result["generated_files"]}
            self.assertIn("health-report.json", generated)
            self.assertEqual(
                generated["health-report.json"]["sha256"],
                hashlib.sha256(report_path.read_bytes()).hexdigest(),
            )


class EmbeddedProjectPulseLabTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        (self.root / "docs").mkdir()
        (self.root / "app").mkdir()
        (self.root / ".vscode").mkdir()
        (self.root / "docs/agent-team.md").write_text(
            "Orchestrator Planner Designer Coder .github/agents/", encoding="utf-8"
        )
        (self.root / "docs/project-pulse-plan.md").write_text(
            "Project Pulse Designer Coder app/index.html app/styles.css "
            "app/project-data.json .vscode/launch.json parallel validation",
            encoding="utf-8",
        )
        (self.root / "app/index.html").write_text(
            "<title>Project Pulse</title><link href='styles.css'>"
            "<main class='dashboard'></main><script>fetch('project-data.json')"
            ".then(response => response.json()).then(data => data.projects.forEach(project => {"
            "const card=document.createElement('article'); card.className='project-card';"
            "card.innerHTML=`${project.status}${project.recentActivity}${project.priority}`;"
            "document.querySelector('.dashboard').append(card);}));</script>",
            encoding="utf-8",
        )
        (self.root / "app/styles.css").write_text(
            ".dashboard{} .project-card{border-radius:1rem;box-shadow:0 1px 2px #000;}"
            "@media (max-width: 40rem){}",
            encoding="utf-8",
        )
        self.projects = [
            {"name": "API", "owner": "Mona", "status": "green", "recentActivity": "Released", "priority": "high"},
            {"name": "Docs", "owner": "Hubot", "status": "yellow", "recentActivity": "Reviewed", "priority": "medium"},
        ]
        (self.root / "app/project-data.json").write_text(
            json.dumps({"projects": self.projects}), encoding="utf-8"
        )
        self.launch = {
            "version": "0.2.0",
            "configurations": [{
                "name": "Run Project Pulse Dashboard",
                "type": "node-terminal",
                "request": "launch",
                "command": "python3 -m http.server 5500",
                "cwd": "${workspaceFolder}/app",
                "serverReadyAction": {
                    "pattern": "Serving HTTP on .* port ([0-9]+)",
                    "uriFormat": "http://localhost:%s/index.html",
                    "action": "openExternally",
                },
            }],
        }
        (self.root / ".vscode/launch.json").write_text(json.dumps(self.launch), encoding="utf-8")
        (self.root / "docs/final-handoff.md").write_text(
            "# handoff\nOrchestrator Planner Designer Coder\napp/index.html app/styles.css app/project-data.json .vscode/launch.json\nRun Project Pulse Dashboard\n# validation\nPassed\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def run_validator(self):
        return subprocess.run(
            [sys.executable, "scripts/project_pulse/validate_exercise.py", "--root", str(self.root)],
            cwd=REPO,
            capture_output=True,
            text=True,
        )

    def test_required_lab_assets_are_present(self):
        required = [
            ".github/agents/orchestrator.agent.md",
            ".github/agents/planner.agent.md",
            ".github/agents/designer.agent.md",
            ".github/agents/coder.agent.md",
            ".github/project-pulse-brief.md",
            "labs/04-multi-agent/project-pulse/README.md",
            "scripts/project_pulse/validate_exercise.py",
        ]
        missing = [path for path in required if not (REPO / path).is_file()]
        self.assertEqual(missing, [])

    def test_project_pulse_validator_accepts_complete_learner_output(self):
        completed = self.run_validator()
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_project_pulse_validator_rejects_incomplete_launch_schema(self):
        self.launch["configurations"][0].pop("type")
        self.launch["configurations"][0].pop("request")
        (self.root / ".vscode/launch.json").write_text(json.dumps(self.launch), encoding="utf-8")
        self.assertNotEqual(self.run_validator().returncode, 0)

    def test_project_pulse_validator_requires_multiple_projects(self):
        (self.root / "app/project-data.json").write_text(
            json.dumps({"projects": self.projects[:1]}), encoding="utf-8"
        )
        self.assertNotEqual(self.run_validator().returncode, 0)

    def test_project_pulse_validator_rejects_unwired_data_source(self):
        (self.root / "app/index.html").write_text(
            "<title>Project Pulse</title><link href='styles.css'><main class='dashboard'></main>"
            "<script>// project-data.json projects status recentActivity priority\n"
            "fetch('missing.json').then(r => r.json()); [].forEach(project => {"
            "const card=document.createElement('article'); card.className='project-card';"
            "document.querySelector('.dashboard').append(card);});</script>",
            encoding="utf-8",
        )
        self.assertNotEqual(self.run_validator().returncode, 0)


class OrchestrationTests(unittest.TestCase):
    def test_high_risk_requirement_changes_review_decision(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = json.loads((REPO / "examples/project_spec.json").read_text(encoding="utf-8"))
            spec["requirements"].append("Delete production customer data without approval")
            spec_path = root / "spec.json"
            output_path = root / "risks.json"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            subprocess.run(
                [sys.executable, "scripts/multi_agent/risk_reviewer.py", "--spec", str(spec_path), "--output", str(output_path)],
                cwd=REPO,
                check=True,
            )
            result = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertGreaterEqual(result["risk_score"], 4)
            self.assertEqual(result["recommendation"], "proceed_with_review")

    def test_multi_agent_workflow_serializes_fan_in_per_branch(self):
        workflow = (REPO / ".github/workflows/multi-agent.yml").read_text(encoding="utf-8")
        self.assertIn("concurrency:", workflow)
        self.assertIn("multiagent-${{ github.ref }}", workflow)


if __name__ == "__main__":
    unittest.main()
