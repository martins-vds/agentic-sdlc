#!/usr/bin/env python3
"""Generate the editable Agentic AI Developer workshop PowerPoint deck."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "slides/github-agentic-ai-developer-workshop.pptx"

WIDTH = Inches(13.333)
HEIGHT = Inches(7.5)

BG = RGBColor(13, 17, 23)
PANEL = RGBColor(22, 27, 34)
PANEL_2 = RGBColor(33, 38, 45)
TEXT = RGBColor(240, 246, 252)
MUTED = RGBColor(139, 148, 158)
GREEN = RGBColor(63, 185, 80)
BLUE = RGBColor(88, 166, 255)
PURPLE = RGBColor(163, 113, 247)
ORANGE = RGBColor(210, 153, 34)
RED = RGBColor(248, 81, 73)
BORDER = RGBColor(48, 54, 61)
WHITE = RGBColor(255, 255, 255)

TITLE_FONT = "Aptos Display"
BODY_FONT = "Aptos"
CODE_FONT = "Aptos Mono"


def set_background(slide, color=BG):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text(slide, text, x, y, w, h, size=24, color=TEXT, bold=False,
             font=BODY_FONT, align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP,
             margin=0.05):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    frame.vertical_anchor = valign
    paragraph = frame.paragraphs[0]
    paragraph.text = text
    paragraph.alignment = align
    paragraph.font.name = font
    paragraph.font.size = Pt(size)
    paragraph.font.bold = bold
    paragraph.font.color.rgb = color
    return box


def add_bullets(slide, items, x, y, w, h, size=21, color=TEXT, accent=BLUE,
                spacing=10):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(0.12)
    frame.margin_right = Inches(0.06)
    for index, item in enumerate(items):
        if isinstance(item, tuple):
            text, level = item
        else:
            text, level = item, 0
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = text
        paragraph.level = level
        paragraph.font.name = BODY_FONT
        paragraph.font.size = Pt(size - level * 2)
        paragraph.font.color.rgb = color if level == 0 else MUTED
        paragraph.space_after = Pt(spacing)
        paragraph.bullet = True
    return box


def add_rect(slide, x, y, w, h, fill=PANEL, line=BORDER, radius=True):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line
    shape.line.width = Pt(1)
    return shape


def add_card(slide, title, body, x, y, w, h, accent=BLUE, number=None):
    add_rect(slide, x, y, w, h)
    slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.08), Inches(h)
    ).fill.solid()
    stripe = slide.shapes[-1]
    stripe.fill.fore_color.rgb = accent
    stripe.line.fill.background()
    if number is not None:
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(x + 0.25), Inches(y + 0.25), Inches(0.55), Inches(0.55)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = accent
        circle.line.fill.background()
        add_text(slide, str(number), x + 0.25, y + 0.25, 0.55, 0.55, 17, BG, True,
                 align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        title_x = x + 0.95
        title_w = w - 1.2
    else:
        title_x = x + 0.3
        title_w = w - 0.55
    add_text(slide, title, title_x, y + 0.22, title_w, 0.5, 19, TEXT, True)
    add_text(slide, body, x + 0.3, y + 0.85, w - 0.55, h - 1.05, 14, MUTED)


def add_code(slide, code, x, y, w, h, size=13, label=None):
    add_rect(slide, x, y, w, h, fill=RGBColor(1, 4, 9), line=BORDER)
    if label:
        add_text(slide, label.upper(), x + 0.2, y + 0.12, w - 0.4, 0.25, 10, BLUE, True)
        code_y = y + 0.45
        code_h = h - 0.58
    else:
        code_y = y + 0.18
        code_h = h - 0.3
    add_text(slide, code, x + 0.2, code_y, w - 0.4, code_h, size, TEXT, False,
             font=CODE_FONT, margin=0)


def add_header(slide, title, section=None, number=None):
    if section:
        add_text(slide, section.upper(), 0.62, 0.28, 5.8, 0.3, 11, BLUE, True)
    add_text(slide, title, 0.62, 0.68, 12.0, 0.7, 28, TEXT, True, TITLE_FONT)
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.62), Inches(1.43), Inches(12.05), Inches(0.025)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER
    line.line.fill.background()
    if number is not None:
        add_text(slide, f"{number:02d}", 12.1, 0.22, 0.55, 0.35, 10, MUTED, True,
                 align=PP_ALIGN.RIGHT)


def add_footer(slide, section, number):
    add_text(slide, "GitHub Certified: Agentic AI Developer Workshop", 0.62, 7.15,
             6.0, 0.2, 9, MUTED)
    add_text(slide, section, 8.0, 7.15, 4.65, 0.2, 9, MUTED,
             align=PP_ALIGN.RIGHT)
    add_text(slide, str(number), 12.75, 7.15, 0.25, 0.2, 9, MUTED,
             align=PP_ALIGN.RIGHT)


def add_notes(slide, notes):
    slide.notes_slide.notes_text_frame.text = notes


def base_slide(prs, title, section, notes):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    number = len(prs.slides)
    add_header(slide, title, section, number)
    add_footer(slide, section, number)
    add_notes(slide, notes)
    return slide


def title_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    for x, y, size, color in (
        (10.8, -0.4, 2.4, PURPLE), (11.7, 0.65, 1.25, BLUE),
        (9.85, 5.75, 2.0, GREEN), (-0.7, 5.9, 1.7, ORANGE),
    ):
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(size), Inches(size))
        circle.fill.solid()
        circle.fill.fore_color.rgb = color
        circle.fill.transparency = 28
        circle.line.fill.background()
    add_text(slide, "GITHUB CERTIFIED", 0.75, 0.78, 4.0, 0.35, 12, BLUE, True)
    add_text(slide, "Agentic AI\nDeveloper Workshop", 0.75, 1.45, 9.8, 2.2, 42, TEXT, True,
             TITLE_FONT)
    add_text(slide, "From prompts to a governed, observable agentic SDLC", 0.8, 4.05,
             8.9, 0.65, 22, MUTED)
    add_rect(slide, 0.8, 5.25, 7.3, 0.9, fill=PANEL_2)
    add_text(slide, "6 modules  |  2 runnable workflows  |  7 hands-on labs  |  1 capstone",
             1.05, 5.49, 6.8, 0.35, 16, TEXT, True)
    add_text(slide, "Workshop companion for GH-600", 0.8, 6.65, 4.5, 0.3, 11, MUTED)
    add_notes(slide, "Welcome learners and frame this as an engineering workshop. The goal is not maximum autonomy; it is bounded authority, observable work, and verifiable evidence.")


def section_slide(prs, module_number, title, subtitle, color, notes):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    number = len(prs.slides)
    add_text(slide, f"MODULE {module_number}", 0.8, 0.75, 3.0, 0.4, 13, color, True)
    add_text(slide, title, 0.8, 1.55, 10.9, 1.5, 38, TEXT, True, TITLE_FONT)
    add_text(slide, subtitle, 0.85, 3.55, 9.9, 0.9, 21, MUTED)
    add_rect(slide, 0.85, 5.15, 11.7, 0.15, fill=color, line=color, radius=False)
    add_text(slide, f"{module_number:02d}", 10.75, 5.42, 1.65, 1.1, 56, color, True,
             TITLE_FONT, PP_ALIGN.RIGHT)
    add_footer(slide, f"Module {module_number}", number)
    add_notes(slide, notes)


def flow(slide, labels, x, y, total_w, node_h=0.95, colors=None, arrows=True):
    gap = 0.32
    node_w = (total_w - gap * (len(labels) - 1)) / len(labels)
    colors = colors or [BLUE] * len(labels)
    centers = []
    for index, label in enumerate(labels):
        node_x = x + index * (node_w + gap)
        add_rect(slide, node_x, y, node_w, node_h, fill=PANEL_2, line=colors[index])
        add_text(slide, label, node_x + 0.08, y + 0.12, node_w - 0.16, node_h - 0.2,
                 16, TEXT, True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        centers.append((node_x + node_w / 2, y + node_h / 2))
        if arrows and index:
            previous_right = x + (index - 1) * (node_w + gap) + node_w
            connector = slide.shapes.add_connector(
                MSO_CONNECTOR.STRAIGHT,
                Inches(previous_right + 0.04), Inches(y + node_h / 2),
                Inches(node_x - 0.04), Inches(y + node_h / 2),
            )
            connector.line.color.rgb = MUTED
            connector.line.width = Pt(1.5)
    return centers


def make_deck():
    prs = Presentation()
    prs.slide_width = WIDTH
    prs.slide_height = HEIGHT
    prs.core_properties.title = "GitHub Certified: Agentic AI Developer Workshop"
    prs.core_properties.subject = "Instructor-ready workshop deck aligned to GH-600"
    prs.core_properties.author = "Agentic SDLC Workshop"
    prs.core_properties.keywords = "GitHub, Copilot, agentic AI, GH-600, SDLC, MCP"

    title_slide(prs)

    slide = base_slide(prs, "What learners will be able to do", "Workshop outcomes",
                       "Review the outcomes and ask learners which area is most relevant to their current role. Emphasize that every outcome produces inspectable evidence.")
    outcomes = [
        ("BOUND", "Define goals, tools, state, policies, stop conditions, and escalation."),
        ("CONNECT", "Exchange versioned artifacts between planning and implementation."),
        ("CONTROL", "Apply allowlists, least privilege, approvals, and protected paths."),
        ("ORCHESTRATE", "Coordinate specialists with concurrency, fan-in, and recovery."),
        ("EVALUATE", "Persist state and enforce deterministic quality gates."),
        ("OPERATE", "Audit, observe, roll back, and improve agent workflows."),
    ]
    for i, (head, body) in enumerate(outcomes):
        col, row = i % 3, i // 3
        add_card(slide, head, body, 0.68 + col * 4.16, 1.78 + row * 2.35, 3.8, 1.95,
                 [BLUE, PURPLE, GREEN, ORANGE, BLUE, RED][i])

    slide = base_slide(prs, "A 4 hour 40 minute learning journey", "Agenda",
                       "Walk through timing and explain that Module 4 intentionally receives the largest block because it contains both deterministic fan-in and the 45-minute Project Pulse lab.")
    agenda = [
        ("00:00", "Foundations", "20 min"), ("00:20", "Architecture", "35 min"),
        ("00:55", "Tools + MCP", "40 min"), ("01:35", "Orchestration", "75 min"),
        ("02:50", "Memory + evaluation", "40 min"), ("03:30", "Governance", "40 min"),
        ("04:10", "Capstone", "30 min"),
    ]
    y = 1.72
    for index, (time, label, duration) in enumerate(agenda):
        color = [BLUE, PURPLE, ORANGE, GREEN, BLUE, RED, PURPLE][index]
        add_text(slide, time, 0.75, y, 1.0, 0.38, 15, color, True)
        add_rect(slide, 1.75, y - 0.02, 9.7, 0.53, fill=PANEL, line=BORDER)
        add_text(slide, label, 2.0, y + 0.07, 6.4, 0.28, 16, TEXT, True)
        add_text(slide, duration, 9.55, y + 0.07, 1.5, 0.28, 14, MUTED, True, align=PP_ALIGN.RIGHT)
        y += 0.72

    slide = base_slide(prs, "GH-600 certification domains", "Certification map",
                       "Explain the exam weighting as ranges, not exact question counts. The workshop follows the same progression from architecture through accountability.")
    domains = [
        ("Architecture + SDLC", "15–20%", BLUE), ("Tools + environment", "20–25%", PURPLE),
        ("Memory + state", "10–15%", ORANGE), ("Evaluation + tuning", "15–20%", GREEN),
        ("Multi-agent coordination", "15–20%", BLUE), ("Guardrails + accountability", "10–15%", RED),
    ]
    for i, (name, weight, color) in enumerate(domains):
        col, row = i % 2, i // 2
        x, y = 0.78 + col * 6.2, 1.75 + row * 1.67
        add_rect(slide, x, y, 5.75, 1.28, fill=PANEL)
        add_text(slide, name, x + 0.25, y + 0.22, 3.9, 0.35, 18, TEXT, True)
        add_text(slide, weight, x + 4.35, y + 0.19, 1.05, 0.4, 18, color, True, align=PP_ALIGN.RIGHT)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + 0.25), Inches(y + 0.83), Inches(5.0), Inches(0.12))
        bar.fill.solid(); bar.fill.fore_color.rgb = BORDER; bar.line.fill.background()
        value = float(weight.split("–")[1].replace("%", "")) / 25
        active = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + 0.25), Inches(y + 0.83), Inches(5.0 * value), Inches(0.12))
        active.fill.solid(); active.fill.fore_color.rgb = color; active.line.fill.background()

    slide = base_slide(prs, "The six-module journey", "Learning path",
                       "Use the progression to show that governance is not an add-on. Every earlier technical choice creates the evidence and boundaries that governance later depends on.")
    flow(slide, ["1\nFoundations", "2\nArchitecture", "3\nTools", "4\nOrchestration", "5\nMemory", "6\nGovernance"],
         0.72, 2.18, 11.9, 1.25, [BLUE, PURPLE, ORANGE, GREEN, BLUE, RED])
    add_text(slide, "Vocabulary", 0.9, 4.25, 1.4, 0.35, 14, MUTED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "Contracts", 2.95, 4.25, 1.4, 0.35, 14, MUTED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "Authority", 4.95, 4.25, 1.4, 0.35, 14, MUTED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "Coordination", 6.95, 4.25, 1.6, 0.35, 14, MUTED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "Continuity", 9.0, 4.25, 1.4, 0.35, 14, MUTED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "Accountability", 10.9, 4.25, 1.7, 0.35, 14, MUTED, True, align=PP_ALIGN.CENTER)
    add_rect(slide, 1.2, 5.35, 10.9, 0.78, fill=PANEL_2, line=GREEN)
    add_text(slide, "Every module produces an artifact that the next module can inspect.",
             1.45, 5.57, 10.4, 0.35, 20, TEXT, True, align=PP_ALIGN.CENTER)

    section_slide(prs, 1, "Foundations of Agentic AI", "Move from one-shot assistance to bounded systems that plan, act, observe, evaluate, and escalate.", BLUE,
                  "Introduce the shared vocabulary. Ask learners to avoid defining an agent by personality or chat interface; define it by its control loop and authority.")

    slide = base_slide(prs, "Assistant versus agent", "Module 1 — Foundations",
                       "Contrast recommendation with action. The risk change occurs when a system can call tools, mutate state, or continue without a fresh human prompt.")
    add_card(slide, "ASSISTANT", "Responds to a prompt\nProposes content\nHuman initiates each step\nUsually has limited state", 0.8, 1.9, 5.55, 3.7, BLUE)
    add_card(slide, "AGENT", "Pursues a goal\nSelects and calls tools\nObserves results\nMaintains state\nStops or escalates by policy", 6.95, 1.9, 5.55, 3.7, PURPLE)
    add_text(slide, "Key question: what can this system do without another human decision?", 1.15, 6.15, 11.0, 0.45, 20, ORANGE, True, align=PP_ALIGN.CENTER)

    slide = base_slide(prs, "The bounded agent lifecycle", "Module 1 — Foundations",
                       "Walk clockwise through the loop. Evaluation can terminate, retry, re-plan, or escalate. A completion message is not evidence; artifacts and checks are evidence.")
    flow(slide, ["GOAL", "PLAN", "ACT", "OBSERVE", "EVALUATE"], 0.8, 2.1, 11.7, 1.08,
         [BLUE, PURPLE, ORANGE, BLUE, GREEN])
    add_rect(slide, 3.2, 4.15, 6.9, 1.05, fill=PANEL_2, line=RED)
    add_text(slide, "STOP / RETRY / RE-PLAN / ESCALATE", 3.45, 4.46, 6.4, 0.35, 19, RED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "Policy surrounds the loop: scope • permissions • timeout • evidence • human control",
             1.2, 5.75, 10.9, 0.45, 17, MUTED, align=PP_ALIGN.CENTER)

    slide = base_slide(prs, "GitHub is the system of record and control plane", "Module 1 — Foundations",
                       "Map each GitHub primitive to a control function. The repository is not only where code lives; it is where intent, evidence, review, and enforcement converge.")
    cards = [
        ("ISSUE", "Intent + acceptance criteria", BLUE), ("BRANCH", "Isolated execution", PURPLE),
        ("PULL REQUEST", "Reviewable change set", GREEN), ("CHECK", "Deterministic evidence", ORANGE),
        ("ARTIFACT", "Durable handoff", BLUE), ("RULESET", "Enforced policy", RED),
    ]
    for i, (head, body, color) in enumerate(cards):
        col, row = i % 3, i // 3
        add_card(slide, head, body, 0.72 + col * 4.18, 1.78 + row * 2.25, 3.84, 1.8, color)

    slide = base_slide(prs, "Agent contract: make authority explicit", "Module 1 — Foundations",
                       "Read the contract fields before the JSON. The most dangerous omissions are usually forbidden actions, stop conditions, and escalation rules.")
    contract = '''{
  "objective": "Generate a project health report",
  "inputs": ["project metadata"],
  "allowed_tools": ["repository.read", "artifact.write"],
  "forbidden": ["push to protected branch", "read secrets"],
  "success": ["valid JSON", "SHA-256 recorded"],
  "timeout_minutes": 10,
  "escalate_when": ["risk is high", "validation fails"]
}'''
    add_code(slide, contract, 0.75, 1.75, 7.15, 4.95, 13, "agent-contract.json")
    add_card(slide, "LAB 1", "Write a bounded contract, generate a plan artifact, and identify one field that would be unsafe to leave implicit.", 8.35, 1.75, 4.2, 2.1, BLUE)
    add_card(slide, "COMPLETION EVIDENCE", "Point to objective, tools, stop condition, and escalation in an inspectable artifact.", 8.35, 4.18, 4.2, 2.05, GREEN)

    section_slide(prs, 2, "Agent Architecture and SDLC Integration", "Separate responsibilities and connect them through versioned, validated handoff contracts.", PURPLE,
                  "Transition from vocabulary to architecture. The design goal is composability: one process should be able to continue another process's work without guessing.")

    slide = base_slide(prs, "Single responsibility, explicit ownership", "Module 2 — Architecture",
                       "Discuss why role boundaries reduce prompt complexity and make failures diagnosable. File ownership is also a concurrency control.")
    roles = [
        ("PLANNER", "Turns intent into ordered work\nOwns plan.json", PURPLE),
        ("IMPLEMENTER", "Creates requested payload\nOwns health-report.json", BLUE),
        ("VALIDATOR", "Checks contract + evidence\nOwns validation.json", GREEN),
        ("HUMAN REVIEWER", "Approves consequential changes\nOwns the decision", ORANGE),
    ]
    for i, (head, body, color) in enumerate(roles):
        col, row = i % 2, i // 2
        add_card(slide, head, body, 0.8 + col * 6.15, 1.8 + row * 2.35, 5.55, 1.95, color, i + 1)

    slide = base_slide(prs, "A versioned plan is an API", "Module 2 — Architecture",
                       "Show how request hash, schema version, and acceptance criteria prevent silent drift. The downstream implementer rejects unsupported or incomplete plans.")
    plan = '''{
  "schema_version": "1.0",
  "request_id": "demo-plan-001",
  "request_hash": "16c8…d421",
  "project_metadata": {
    "name": "agentic-sdlc-demo",
    "status": "healthy",
    "owner": "platform-engineering"
  },
  "acceptance_criteria": [
    "The report contains project name and status",
    "The report is valid JSON"
  ],
  "handoff": {
    "producer": "deterministic-planner",
    "consumer": "deterministic-implementer"
  }
}'''
    add_code(slide, plan, 0.72, 1.7, 7.7, 5.15, 11.5, "plan.json")
    add_bullets(slide, ["Stable schema version", "Canonical request hash", "Explicit producer + consumer", "Acceptance criteria travel with work", "Risk determines human approval"], 8.78, 1.9, 3.8, 4.6, 17)

    slide = base_slide(prs, "Concrete plan → implement handoff", "Module 2 — Architecture",
                       "This is executable workflow code from the repository, not pseudocode. The plan job uploads plan.json; the implementation job downloads it and creates a real health report plus integrity manifest.")
    workflow = '''jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          python3 scripts/plan/generate_plan.py \\
            --request examples/plan_request.json \\
            --output artifacts/plan/plan.json
      - uses: actions/upload-artifact@v4
        with:
          name: agent-plan
          path: artifacts/plan/plan.json

  implement:
    needs: plan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: agent-plan
          path: artifacts/plan
      - run: |
          python3 scripts/implement/apply_plan.py \\
            --plan artifacts/plan/plan.json \\
            --output artifacts/implementation/implementation.json'''
    add_code(slide, workflow, 0.72, 1.66, 8.35, 5.3, 10.4, ".github/workflows/plan-implement.yml")
    add_card(slide, "NOT A PLACEHOLDER", "The consumer writes health-report.json and records its SHA-256 digest and byte size.", 9.42, 1.75, 3.2, 2.2, GREEN)
    add_card(slide, "BOUNDARY", "Jobs exchange immutable artifacts instead of hidden process memory.", 9.42, 4.22, 3.2, 2.0, PURPLE)

    slide = base_slide(prs, "Evidence: payload + integrity manifest", "Module 2 — Architecture",
                       "Demonstrate sha256sum during the lab. If the report changes after handoff, the recorded digest no longer matches and downstream validation can reject it.")
    flow(slide, ["request.json", "plan.json", "health-report.json", "implementation.json"],
         0.75, 2.0, 11.85, 1.15, [BLUE, PURPLE, GREEN, ORANGE])
    add_code(slide, '''"generated_files": [
  {
    "path": "health-report.json",
    "sha256": "cc7e6b…ec7c",
    "bytes": 742
  }
]''', 1.0, 4.0, 5.4, 2.2, 14, "implementation.json")
    add_bullets(slide, ["Artifact exists", "JSON parses", "Required fields are present", "Digest matches exact bytes", "Protected paths remain untouched"], 7.0, 3.95, 5.0, 2.4, 18)

    slide = base_slide(prs, "Pull-request governance belongs in the architecture", "Module 2 — Architecture",
                       "These controls are not cleanup after implementation. Design the PR path before granting write authority to an agent.")
    controls = [
        ("TEMPLATE", "Required context and test plan"), ("CHECKS", "Objective machine evidence"),
        ("CODEOWNERS", "Domain-specific human review"), ("RULESET", "No bypass of protected branch"),
        ("ENVIRONMENT", "Approval before deployment"), ("ROLLBACK", "Known recovery reference"),
    ]
    for i, (head, body) in enumerate(controls):
        col, row = i % 3, i // 3
        add_card(slide, head, body, 0.72 + col * 4.18, 1.8 + row * 2.25, 3.84, 1.78,
                 [BLUE, GREEN, PURPLE, RED, ORANGE, BLUE][i])

    section_slide(prs, 3, "Tooling, MCP, and Execution Environments", "Expose narrow capabilities through explicit protocol, authorization, and runtime boundaries.", ORANGE,
                  "Make the distinction between connectivity and authority. MCP can describe and invoke a tool, but policy still decides whether the action is allowed.")

    slide = base_slide(prs, "A tool boundary has four layers", "Module 3 — Tools + MCP",
                       "Walk from protocol inward to audit. A valid JSON-RPC request can still be denied by operation, path, or permission policy.")
    layers = [
        ("1", "PROTOCOL", "Shape, identity, arguments", BLUE),
        ("2", "CAPABILITY", "Named tool + operation", PURPLE),
        ("3", "AUTHORIZATION", "Allowlists + path scope", ORANGE),
        ("4", "EVIDENCE", "Decision + reason + provenance", GREEN),
    ]
    for i, (num, head, body, color) in enumerate(layers):
        add_card(slide, head, body, 1.0 + i * 3.02, 2.0, 2.65, 2.55, color, num)
    add_text(slide, "Protocol compatibility ≠ permission to act", 1.2, 5.45, 10.9, 0.55, 24, RED, True, align=PP_ALIGN.CENTER)

    slide = base_slide(prs, "Concrete MCP-style request and decision", "Module 3 — Tools + MCP",
                       "Run the allow case, then change operation to write_file. The same request envelope produces a nonzero process exit and a denied audit record.")
    request = '''{
  "jsonrpc": "2.0",
  "id": "mcp-demo-001",
  "tool": "repository.read",
  "operation": "read_file",
  "path": "examples/project_spec.json",
  "arguments": {"encoding": "utf-8"}
}'''
    denied = '''{
  "decision": "deny",
  "reason": "operation is not allowed",
  "tool": "repository.read",
  "operation": "write_file",
  "path": "examples/project_spec.json"
}'''
    add_code(slide, request, 0.72, 1.72, 5.85, 4.8, 13, "request.json")
    add_code(slide, denied, 6.88, 1.72, 5.72, 4.8, 13, "denied response")

    slide = base_slide(prs, "Choose the execution environment deliberately", "Module 3 — Tools + MCP",
                       "Codespaces optimizes interactive learning and inspection. Actions optimizes repeatability and policy enforcement. Production agents often need both patterns with different authority.")
    add_card(slide, "CODESPACES", "Interactive\nHuman present\nRich repository context\nGood for exploration\nUse scoped CLI permissions", 0.85, 1.9, 5.55, 3.65, BLUE)
    add_card(slide, "GITHUB ACTIONS", "Repeatable\nEvent-driven\nExplicit token permissions\nArtifacts + logs\nEnvironment approval gates", 6.92, 1.9, 5.55, 3.65, PURPLE)
    add_text(slide, "Network, secrets, write scope, timeout, and retention must be explicit in both.", 1.0, 6.05, 11.2, 0.45, 18, ORANGE, True, align=PP_ALIGN.CENTER)

    section_slide(prs, 4, "Multi-Agent Systems and Orchestration", "Coordinate specialist agents through isolated work, observable artifacts, fan-in, and safe recovery.", GREEN,
                  "This module has two labs: deterministic fan-in and the faithful Project Pulse custom-agent exercise. Explain why orchestration is more than calling multiple prompts.")

    slide = base_slide(prs, "Deterministic multi-agent topology", "Module 4 — Orchestration",
                       "The two specialists are independent and may run concurrently. The merger cannot start until both artifacts exist. Validation is a separate responsibility.")
    add_rect(slide, 0.85, 2.45, 2.25, 1.0, fill=PANEL_2, line=BLUE)
    add_text(slide, "ORCHESTRATOR", 1.05, 2.75, 1.85, 0.3, 17, TEXT, True, align=PP_ALIGN.CENTER)
    add_rect(slide, 4.0, 1.6, 2.55, 1.0, fill=PANEL_2, line=PURPLE)
    add_text(slide, "SPEC ANALYZER", 4.2, 1.9, 2.15, 0.3, 16, TEXT, True, align=PP_ALIGN.CENTER)
    add_rect(slide, 4.0, 3.55, 2.55, 1.0, fill=PANEL_2, line=ORANGE)
    add_text(slide, "RISK REVIEWER", 4.2, 3.85, 2.15, 0.3, 16, TEXT, True, align=PP_ALIGN.CENTER)
    add_rect(slide, 7.45, 2.45, 2.2, 1.0, fill=PANEL_2, line=GREEN)
    add_text(slide, "PLAN MERGER", 7.65, 2.75, 1.8, 0.3, 16, TEXT, True, align=PP_ALIGN.CENTER)
    add_rect(slide, 10.55, 2.45, 1.9, 1.0, fill=PANEL_2, line=RED)
    add_text(slide, "VALIDATOR", 10.72, 2.75, 1.55, 0.3, 16, TEXT, True, align=PP_ALIGN.CENTER)
    for x1, y1, x2, y2 in [(3.1,2.95,4.0,2.1),(3.1,2.95,4.0,4.05),(6.55,2.1,7.45,2.95),(6.55,4.05,7.45,2.95),(9.65,2.95,10.55,2.95)]:
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        line.line.color.rgb = MUTED; line.line.width = Pt(2)
    add_text(slide, "parallel", 4.68, 5.05, 1.2, 0.3, 13, PURPLE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "fan-in", 7.85, 4.05, 1.3, 0.3, 13, GREEN, True, align=PP_ALIGN.CENTER)
    add_text(slide, "quality gate", 10.65, 4.05, 1.65, 0.3, 13, RED, True, align=PP_ALIGN.CENTER)

    slide = base_slide(prs, "Concrete parallel specialists and fan-in", "Module 4 — Orchestration",
                       "This workflow replaces missing shell placeholders with real Python executors. Each matrix child uploads a named report; the fan-in job downloads both and validates the merged plan.")
    multi = '''jobs:
  specialists:
    strategy:
      fail-fast: false
      matrix:
        role: [spec-analyzer, risk-reviewer]
    steps:
      - uses: actions/checkout@v4
      - name: Run specialist
        run: |
          if [ "${{ matrix.role }}" = "spec-analyzer" ]; then
            python3 scripts/multi_agent/spec_analyzer.py \\
              --spec examples/project_spec.json \\
              --output artifacts/${{ matrix.role }}/report.json
          else
            python3 scripts/multi_agent/risk_reviewer.py \\
              --spec examples/project_spec.json \\
              --output artifacts/${{ matrix.role }}/report.json
          fi

  fan-in:
    needs: specialists
    concurrency:
      group: multiagent-${{ github.ref }}
    steps:
      - run: python3 scripts/multi_agent/plan_merger.py ...'''
    add_code(slide, multi, 0.72, 1.66, 8.7, 5.33, 10.5, ".github/workflows/multi-agent.yml")
    add_card(slide, "ISOLATION", "Separate artifact directory per specialist.", 9.73, 1.75, 2.85, 1.45, PURPLE)
    add_card(slide, "RECOVERY", "fail-fast: false preserves independent evidence.", 9.73, 3.45, 2.85, 1.45, ORANGE)
    add_card(slide, "SERIALIZATION", "One branch-scoped merge job at a time.", 9.73, 5.15, 2.85, 1.45, GREEN)

    slide = base_slide(prs, "Failures are orchestration outcomes", "Module 4 — Orchestration",
                       "Ask learners which failures can retry automatically and which require escalation. Recovery depends on idempotent steps and durable artifacts.")
    failures = [
        ("SPECIALIST FAILS", "Preserve other output\nRetry bounded times\nEscalate with logs", RED),
        ("OUTPUT IS STALE", "Record input hash\nReject mismatched provenance", ORANGE),
        ("AGENTS DISAGREE", "Use deterministic arbitration\nRoute unresolved conflict to human", PURPLE),
        ("MERGE OVERLAPS", "Concurrency group\nBranch isolation\nIdempotent fan-in", GREEN),
    ]
    for i, (head, body, color) in enumerate(failures):
        col, row = i % 2, i // 2
        add_card(slide, head, body, 0.8 + col * 6.15, 1.8 + row * 2.35, 5.55, 1.95, color)

    slide = base_slide(prs, "Project Pulse: build an AI dream team", "Module 4 — Required lab",
                       "Introduce the faithful in-repository adaptation of the Microsoft Learn and GitHub Skills exercise. Learners work in Copilot CLI and inspect every generated artifact.")
    add_text(slide, "45 MINUTES", 0.8, 1.78, 2.2, 0.4, 15, GREEN, True)
    add_text(slide, "Plan, design, build, run, and validate Mona's Project Pulse dashboard.", 0.8, 2.28, 11.2, 0.75, 26, TEXT, True)
    deliverables = ["docs/agent-team.md", "docs/project-pulse-plan.md", "app/index.html", "app/styles.css", "app/project-data.json", ".vscode/launch.json", "docs/final-handoff.md"]
    for i, item in enumerate(deliverables):
        col, row = i % 2, i // 2
        add_rect(slide, 0.85 + col * 6.05, 3.4 + row * 0.68, 5.55, 0.48, fill=PANEL_2)
        add_text(slide, item, 1.08 + col * 6.05, 3.51 + row * 0.68, 5.1, 0.25, 14, BLUE if i < 2 else TEXT, True, font=CODE_FONT)

    slide = base_slide(prs, "The custom agent team", "Module 4 — Project Pulse",
                       "Inspect the definitions under .github/agents before using them. Models are less important than explicit role, tools, file scope, and handoff rules.")
    team = [
        ("ORCHESTRATOR", "Coordinates phases\nDelegates; does not implement", GREEN),
        ("PLANNER", "Researches + sequences\nDefines ownership + dependencies", PURPLE),
        ("DESIGNER", "UX + accessibility\nOwns visual decisions", ORANGE),
        ("CODER", "Implements files\nValidates runnable behavior", BLUE),
    ]
    for i, (head, body, color) in enumerate(team):
        add_card(slide, head, body, 0.65 + i * 3.15, 1.95, 2.85, 3.15, color, i + 1)
    add_text(slide, "Orchestrator grants explicit file scope; specialists report files touched and validation evidence.", 1.0, 5.75, 11.2, 0.55, 18, MUTED, align=PP_ALIGN.CENTER)

    slide = base_slide(prs, "Project Pulse orchestration sequence", "Module 4 — Project Pulse",
                       "Have learners select Orchestrator with /agent. The Planner works first; design and implementation follow the approved file boundaries; validation failures return to the responsible specialist.")
    flow(slide, ["INSPECT TEAM", "PLAN", "DESIGN", "IMPLEMENT", "RUN", "VALIDATE", "HANDOFF"],
         0.55, 2.0, 12.25, 1.08, [BLUE, PURPLE, ORANGE, BLUE, GREEN, RED, PURPLE])
    add_card(slide, "PROMPT CONTRACT", "Name the desired outcome, exact files, required fields, launch behavior, and validation command.", 0.82, 4.0, 5.65, 1.75, BLUE)
    add_card(slide, "HUMAN EVIDENCE", "Inspect the rendered dashboard at narrow and wide viewports and verify a clean browser console.", 6.86, 4.0, 5.65, 1.75, GREEN)

    slide = base_slide(prs, "Project Pulse completion evidence", "Module 4 — Project Pulse",
                       "The local validator performs static source and schema checks; it does not execute browser JavaScript. Runtime and visual inspection remain human evidence.")
    add_code(slide, '''python3 scripts/project_pulse/validate_exercise.py --root .

PASS: project data has at least two projects
PASS: dashboard source fetches project-data.json
PASS: launch configuration is runnable
PASS: launch configuration opens index.html
PASS: final handoff names every agent and deliverable
All Project Pulse validation checks passed.''', 0.72, 1.72, 7.4, 4.85, 13, "terminal")
    add_card(slide, "STATIC CHECKS", "Files • JSON • source wiring • required fields • launch schema", 8.52, 1.85, 3.95, 1.75, BLUE)
    add_card(slide, "HUMAN CHECKS", "Rendered cards • responsive layout • accessibility • browser errors", 8.52, 3.95, 3.95, 1.75, ORANGE)

    section_slide(prs, 5, "Memory, State, and Evaluation", "Preserve useful continuity with provenance while detecting drift and enforcing explicit success signals.", BLUE,
                  "Explain that memory is a product and governance decision. More retained context is not automatically better; durable state should improve recovery and accountability.")

    slide = base_slide(prs, "Three memory horizons", "Module 5 — Memory + evaluation",
                       "Differentiate ephemeral reasoning context from durable, auditable state. Sensitive or stale context should not become long-term memory by accident.")
    add_card(slide, "SHORT-TERM", "Current task context\nTool outputs\nWorking hypotheses\nDiscard or compact quickly", 0.78, 1.9, 3.78, 3.45, BLUE)
    add_card(slide, "LONG-TERM", "Stable conventions\nValidated decisions\nReusable preferences\nRetention policy required", 4.78, 1.9, 3.78, 3.45, PURPLE)
    add_card(slide, "EXTERNAL STATE", "Issues + PRs\nArtifacts + logs\nJSONL event history\nSystem of record", 8.78, 1.9, 3.78, 3.45, GREEN)
    add_text(slide, "Persist: facts + provenance. Avoid: secrets, unsupported inference, and unbounded transcripts.", 1.0, 5.95, 11.2, 0.45, 18, ORANGE, True, align=PP_ALIGN.CENTER)

    slide = base_slide(prs, "Event log → snapshot → continuity", "Module 5 — Memory + evaluation",
                       "Run the state_store commands and inspect sequence, source, timestamp, and hash. A snapshot is useful only if its provenance is retained.")
    state = '''{
  "sequence": 1,
  "event_type": "implementation.accepted",
  "source": "scripts/implement/apply_plan.py",
  "payload": {
    "request_id": "demo-plan-001",
    "status": "ready_for_review",
    "changed_files": ["artifacts/health-report.json"]
  }
}'''
    add_code(slide, state, 0.72, 1.72, 6.4, 4.95, 13, "state event")
    flow(slide, ["APPEND", "ORDER", "HASH", "SNAPSHOT"], 7.48, 2.0, 4.8, 0.95,
         [BLUE, PURPLE, ORANGE, GREEN])
    add_bullets(slide, ["Source identifies producer", "Sequence preserves order", "Hash detects mutation", "Snapshot supports recovery", "Retention prevents stale context"], 7.6, 3.5, 4.55, 2.7, 17)

    slide = base_slide(prs, "Evaluation signals and quality gates", "Module 5 — Memory + evaluation",
                       "Separate checks that code can prove from judgments that require a human. A model score must not replace schema checks, tests, or required review.")
    add_card(slide, "DETERMINISTIC", "Schema parses\nFiles exist\nHashes match\nTests pass\nRisk threshold is respected", 0.8, 1.85, 5.55, 3.55, GREEN)
    add_card(slide, "JUDGMENT", "Design quality\nRequirement ambiguity\nUser value\nAcceptable tradeoffs\nNovel failure analysis", 6.95, 1.85, 5.55, 3.55, PURPLE)
    add_rect(slide, 2.35, 5.85, 8.65, 0.6, fill=PANEL_2, line=RED)
    add_text(slide, "A failed quality gate is an explicit outcome — never a detail to hide.", 2.55, 6.02, 8.25, 0.3, 18, RED, True, align=PP_ALIGN.CENTER)

    section_slide(prs, 6, "Governance, Guardrails, and Operations", "Scale autonomy according to risk, preserve human control, and make every consequential action reversible and auditable.", RED,
                  "Close the technical journey by combining authority, approval, evidence, and recovery. Governance should be encoded in GitHub controls, not left only in prompt prose.")

    slide = base_slide(prs, "Risk-based autonomy ladder", "Module 6 — Governance",
                       "Ask learners to classify one task at each level. Higher consequence means narrower permissions, stronger approval, and more complete recovery evidence.")
    levels = [
        ("1", "READ + SUMMARIZE", "Auto", GREEN),
        ("2", "PROPOSE CHANGE", "Auto + validate", BLUE),
        ("3", "OPEN PULL REQUEST", "Review required", PURPLE),
        ("4", "DEPLOY / MUTATE DATA", "Environment approval", ORANGE),
        ("5", "IRREVERSIBLE ACTION", "Deny or exceptional process", RED),
    ]
    y = 1.65
    for num, action, control, color in levels:
        add_rect(slide, 1.0, y, 11.3, 0.82, fill=PANEL)
        add_text(slide, num, 1.2, y + 0.16, 0.45, 0.35, 18, color, True, align=PP_ALIGN.CENTER)
        add_text(slide, action, 1.9, y + 0.16, 5.2, 0.35, 17, TEXT, True)
        add_text(slide, control, 7.6, y + 0.16, 4.2, 0.35, 16, color, True, align=PP_ALIGN.RIGHT)
        y += 1.0

    slide = base_slide(prs, "Guardrail → approval → audit → recovery", "Module 6 — Governance",
                       "Use the sample request to show least privilege. The protected-branch request has the correct narrow permissions but no approval, so it becomes approval_required rather than executing silently.")
    flow(slide, ["REQUEST", "POLICY", "APPROVAL", "AUDIT", "ROLLBACK"], 0.75, 1.85, 11.85, 1.05,
         [BLUE, RED, ORANGE, GREEN, PURPLE])
    guard = '''{
  "requested_action": "open_pull_request",
  "permissions": [
    "contents:read",
    "pull-requests:write"
  ],
  "protected_branch": true,
  "approval": {"required": true, "present": false}
}

→ decision: "approval_required"'''
    add_code(slide, guard, 0.95, 3.7, 5.75, 2.65, 13, "governance request")
    add_bullets(slide, ["Narrow required permissions", "Human gate for protected branch", "Run ID + actor + policy version", "Changed paths recorded", "Rollback reference prepared"], 7.15, 3.7, 4.9, 2.6, 17)

    slide = base_slide(prs, "Capstone: prove the whole system", "Workshop capstone",
                       "Learners submit artifacts, not a narrative claim. Grade bounded authority, reproducibility, observability, and explicit failure handling rather than model eloquence.")
    artifacts = [
        "Agent contract", "Tool + permission policy", "Versioned plan", "Two specialist outputs",
        "Merged plan", "State snapshot", "Evaluation report", "Approval + audit record", "Rollback procedure",
    ]
    for i, item in enumerate(artifacts):
        col, row = i % 3, i // 3
        add_card(slide, item.upper(), "Inspectable evidence", 0.62 + col * 4.2, 1.65 + row * 1.65, 3.85, 1.32,
                 [BLUE, PURPLE, ORANGE, GREEN, BLUE, PURPLE, RED, ORANGE, GREEN][i])
    add_text(slide, "Rubric: bounded • reproducible • observable • reversible", 1.2, 6.65, 10.9, 0.35, 18, TEXT, True, align=PP_ALIGN.CENTER)

    slide = base_slide(prs, "Use the workshop as a GH-600 study map", "Certification preparation",
                       "Encourage learners to connect every exam domain to a runnable artifact. The source-coverage document maps all 52 Microsoft Learn units to workshop material.")
    mappings = [
        ("Architecture + SDLC", "Agent contract + plan handoff", BLUE),
        ("Tool interaction", "MCP boundary + execution environments", ORANGE),
        ("Memory + state", "Event log + snapshot", PURPLE),
        ("Evaluation", "Quality gates + failure analysis", GREEN),
        ("Multi-agent", "Fan-in workflow + Project Pulse", BLUE),
        ("Guardrails", "Approval + audit + rollback", RED),
    ]
    for i, (domain, evidence, color) in enumerate(mappings):
        col, row = i % 2, i // 2
        x, y = 0.78 + col * 6.18, 1.73 + row * 1.72
        add_rect(slide, x, y, 5.7, 1.32, fill=PANEL)
        add_text(slide, domain, x + 0.25, y + 0.2, 5.1, 0.35, 18, color, True)
        add_text(slide, evidence, x + 0.25, y + 0.7, 5.1, 0.35, 15, MUTED)
    add_text(slide, "docs/source-coverage.md", 4.4, 6.35, 4.5, 0.35, 16, BLUE, True, font=CODE_FONT, align=PP_ALIGN.CENTER)

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    number = len(prs.slides)
    add_text(slide, "EVIDENCE OVER AUTONOMY", 0.75, 0.9, 7.5, 0.4, 13, GREEN, True)
    add_text(slide, "Build agents you can\ninspect, stop, and trust.", 0.75, 1.65, 10.8, 1.8, 40, TEXT, True, TITLE_FONT)
    add_rect(slide, 0.8, 4.2, 11.75, 1.2, fill=PANEL_2, line=GREEN)
    add_text(slide, "What is one action you would never allow an agent to perform without human approval?",
             1.15, 4.48, 11.05, 0.65, 22, TEXT, True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    add_text(slide, "Run the labs  •  inspect the artifacts  •  practice the recovery path",
             0.9, 6.3, 11.5, 0.4, 16, MUTED, align=PP_ALIGN.CENTER)
    add_footer(slide, "Close", number)
    add_notes(slide, "Close by collecting examples of actions that require human approval. Reinforce that reliable agentic systems are designed for interruption, review, and recovery—not only successful execution.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT)
    print(f"Generated {OUTPUT} with {len(prs.slides)} slides")


if __name__ == "__main__":
    make_deck()
