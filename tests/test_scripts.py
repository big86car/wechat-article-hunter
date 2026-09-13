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
            source.write_text("# 标题\n\n正文内容。\n\n## 分析\n\n> 关键判断\n", encoding="utf-8")
            result = subprocess.run([
                sys.executable,
                str(ROOT / "skills/wechat-layout/scripts/markdown_to_wechat_html.py"),
                str(source), str(output),
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            html = output.read_text(encoding="utf-8")
            self.assertIn("<section style=", html)
            self.assertIn("<h2 style=", html)
            self.assertNotIn("<script", html)

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


if __name__ == "__main__":
    unittest.main()
