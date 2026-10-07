# Slide/deck outline

The editable 38-slide PowerPoint deck is available at [`slides/github-agentic-ai-developer-workshop.pptx`](../slides/github-agentic-ai-developer-workshop.pptx). It includes speaker notes, editable vector diagrams, concrete workflow code, the Project Pulse lab, capstone guidance, and GH-600 mapping.

Regenerate it after changing workshop content:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/presentation/generate_workshop_deck.py
```

## Repository PowerPoint style

Use the supplied **Offering - GitHub Developer Training** deck as the styling reference for all repository presentations. The workshop generator preserves that style without requiring the original file in `temp/`:

- Black title and closing slides with the reference's dotted artwork and GitHub mark.
- Solid `#1658C5` blue module dividers with large white, left-aligned titles.
- White content slides, `#F6F8FA` light-gray panels, `#24292E` text, and `#0366D6` blue accents. Use open spacing, flat shapes, and editable diagrams rather than dark dashboard cards, decorative stripes, or shadows.
- Helvetica Neue for headings and body text; Roboto Mono for code and small title-slide labels. Install these fonts on the presentation/rendering machine for matching typography; otherwise the viewer substitutes available fonts.
- Widescreen 16:9 geometry. The workshop uses a 13.333 × 7.5-inch canvas, proportionally equivalent to the reference's 10 × 5.625-inch canvas.

Reuse the palette, theme, artwork, and layout helpers in `scripts/presentation/generate_workshop_deck.py` for future decks. The two PNGs in `scripts/presentation/assets/` are extracted title artwork from the supplied reference; they do not contain workshop slide text. Keep teaching content, diagrams, and code editable.

Speaker notes follow the reference's facilitator cadence: short lines, conversational explanations, direct demo steps, occasional questions, and blank lines between beats. Write what the instructor can say or do, not a polished summary or a repeated script formula. Preserve exact commands, lab paths, validation limits, and troubleshooting cues. For example:

```text
Run the read request first
Look at the allowed decision

Change the operation to write_file and run it again
Same request format, different permission outcome
Check the nonzero exit code and the denied audit record
```

All 38 workshop slides include notes in this style. Regeneration preserves both the branding and the notes; it does not read or modify the reference deck.

The headings below are the original concise narrative outline.

## 1. Title: From prompts to governed agentic SDLC

Speaker cues:

```text
We will be building and inspecting agent workflows today
Not trying to give an agent unlimited autonomy
We want to know what it can do, when it should stop, and how we check its work
```

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
