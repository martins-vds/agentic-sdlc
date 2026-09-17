# Module 1 lab: Foundations of Agentic AI in GitHub

## Goal

Model a repository task as a bounded agent rather than as an unconstrained chatbot request.

## Steps

1. Open the repository in a Codespace and inspect `README.md`, `docs/curriculum.md`, and `examples/plan_request.json`.
2. Write down the task's goal, inputs, expected output, allowed tools, forbidden actions, stop condition, and human escalation.
3. Compare your contract with the plan request. Identify one field that would be unsafe to leave implicit.
4. Run `python3 scripts/plan/generate_plan.py --request examples/plan_request.json --output /tmp/foundations-plan.json`.
5. Open `/tmp/foundations-plan.json`. Find the objective, acceptance criteria, risk level, and generated steps.
6. Explain which parts are deterministic and which parts would normally be model-assisted.

## Discussion

An agent is not defined by a friendly persona. It is defined by a control loop and the policies around that loop. A useful GitHub agent leaves evidence in files, commits, checks, reviews, or workflow artifacts.

## Completion check

You can point to the plan artifact and state exactly what the agent may do, what it may not do, and when a human must take over.

