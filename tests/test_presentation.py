import unittest
from pathlib import Path

from pptx import Presentation

REPO = Path(__file__).resolve().parents[1]
DECK = REPO / "slides/github-agentic-ai-developer-workshop.pptx"


class WorkshopPresentationTests(unittest.TestCase):
    def test_deck_is_complete_and_editable(self):
        self.assertTrue(DECK.is_file(), "PowerPoint deck must be generated")
        presentation = Presentation(DECK)
        self.assertGreaterEqual(len(presentation.slides), 30)

        all_text = []
        slides_with_notes = 0
        for slide in presentation.slides:
            slide_text = "\n".join(
                shape.text for shape in slide.shapes if hasattr(shape, "text")
            )
            all_text.append(slide_text)
            notes = slide.notes_slide.notes_text_frame.text.strip()
            if notes:
                slides_with_notes += 1

        deck_text = "\n".join(all_text)
        for required in (
            "Foundations of Agentic AI",
            "Agent Architecture and SDLC Integration",
            "Tooling, MCP, and Execution Environments",
            "Multi-Agent Systems and Orchestration",
            "Memory, State, and Evaluation",
            "Governance, Guardrails, and Operations",
            "Project Pulse",
            "GH-600",
        ):
            self.assertIn(required, deck_text)
        self.assertNotIn("TODO", deck_text)
        self.assertNotIn("plan=...", deck_text)
        self.assertGreaterEqual(slides_with_notes, len(presentation.slides) - 1)


if __name__ == "__main__":
    unittest.main()
