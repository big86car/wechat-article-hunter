import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScriptTests(unittest.TestCase):
    def test_topic_card_validator_accepts_correct_score(self):
        payload = {
            "recommended_topic_id": "topic-01",
            "topics": [{
                "id": "topic-01", "topic": "Agent", "angle": "enterprise adoption",
                "why_now": "dated release", "reader_tension": "uncertain ROI",
                "thesis": "adoption depends on workflow redesign", "differentiation": "focus on operating model",
                "title_candidates": ["a", "b", "c"], "evidence_leads": [],
                "counterargument": "model capability dominates", "shelf_life": "weeks",
                "effort": "medium", "risks": [],
                "scores": {"audience_fit": 5, "why_now": 4, "insight_potential": 5,
                           "evidence_depth": 4, "share_save_value": 4, "competition_gap": 3},
                "weighted_score": 87.0, "confidence": "high"
            }]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cards.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = subprocess.run([
                sys.executable,
                str(ROOT / "skills/wechat-topic-hunter/scripts/validate_topic_cards.py"),
                str(path),
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_layout_emits_inline_styled_fragment(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "article.md"
            output = Path(directory) / "article.html"
            text_output = Path(directory) / "article.txt"
            source.write_text("# 标题\n\n正文[来源](https://example.com)。\n\n## 分析\n\n> 关键判断\n", encoding="utf-8")
            result = subprocess.run([
                sys.executable,
                str(ROOT / "skills/wechat-layout/scripts/markdown_to_wechat_html.py"),
                str(source), str(output), "--text-output", str(text_output),
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            html = output.read_text(encoding="utf-8")
            self.assertIn("<section style=", html)
            self.assertIn("<h2 style=", html)
            self.assertNotIn("<script", html)
            self.assertIn("https://example.com", text_output.read_text(encoding="utf-8"))

    def test_article_validator_rejects_editorial_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "article.md"
            path.write_text("# 标题\n\n<!-- IMAGE: unresolved -->\n", encoding="utf-8")
            result = subprocess.run([
                sys.executable,
                str(ROOT / "skills/wechat-article-editor/scripts/validate_article.py"),
                str(path),
            ], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)

    def test_originality_gate_accepts_supported_pass(self):
        payload = {
            "schema_version": "1.0", "article": "draft.md", "reviewed_at": "2026-09-13T00:00:00Z",
            "verdict": "pass",
            "scores": {"provenance_completeness": 5, "attribution_integrity": 4,
                       "expression_independence": 5, "structural_independence": 4, "original_value": 5},
            "original_contributions": [{"type": "framework", "description": "new framework", "evidence": "outline"}],
            "findings": [], "manual_review_required": False, "notes": []
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "originality-report.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = subprocess.run([
                sys.executable,
                str(ROOT / "skills/wechat-originality-gate/scripts/validate_originality_report.py"),
                str(path),
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_publisher_dry_run_is_non_networked_and_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            html = base / "article.html"
            cover = base / "cover.jpg"
            receipt = base / "receipt.json"
            html.write_text('<section><h1>标题</h1><p>正文</p></section>', encoding="utf-8")
            cover.write_bytes(b"test-cover")
            command = [
                sys.executable,
                str(ROOT / "skills/wechat-draft-publisher/scripts/publish_draft.py"),
                "--html", str(html), "--cover", str(cover), "--title", "标题",
                "--receipt", str(receipt),
            ]
            result = subprocess.run(command, capture_output=True, text=True, env={})
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(data["status"], "prepared")
            self.assertFalse(data["publicly_published"])


if __name__ == "__main__":
    unittest.main()
