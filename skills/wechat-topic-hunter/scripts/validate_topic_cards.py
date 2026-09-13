#!/usr/bin/env python3
"""Validate topic-card structure and weighted scoring."""

import json
import sys
from pathlib import Path

WEIGHTS = {
    "audience_fit": 25, "why_now": 20, "insight_potential": 20,
    "evidence_depth": 15, "share_save_value": 10, "competition_gap": 10,
}
REQUIRED = {"id", "topic", "angle", "why_now", "reader_tension", "thesis",
            "differentiation", "title_candidates", "evidence_leads", "scores",
            "weighted_score", "confidence"}


def main(path: str) -> int:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = []
    topics = data.get("topics")
    if not isinstance(topics, list) or not topics:
        errors.append("topics must be a non-empty array")
    else:
        ids = set()
        for i, topic in enumerate(topics):
            label = f"topics[{i}]"
            missing = REQUIRED - set(topic)
            if missing:
                errors.append(f"{label}: missing {sorted(missing)}")
                continue
            if topic["id"] in ids:
                errors.append(f"{label}: duplicate id {topic['id']}")
            ids.add(topic["id"])
            if len(topic["title_candidates"]) < 3:
                errors.append(f"{label}: needs at least 3 title candidates")
            scores = topic["scores"]
            if set(scores) != set(WEIGHTS):
                errors.append(f"{label}: score dimensions do not match schema")
                continue
            if any(not isinstance(v, (int, float)) or not 1 <= v <= 5 for v in scores.values()):
                errors.append(f"{label}: every score must be between 1 and 5")
                continue
            expected = round(sum(scores[k] / 5 * w for k, w in WEIGHTS.items()), 1)
            if abs(float(topic["weighted_score"]) - expected) > 0.11:
                errors.append(f"{label}: weighted_score should be {expected}")
        if data.get("recommended_topic_id") not in ids:
            errors.append("recommended_topic_id must reference a topic id")
    if errors:
        print("INVALID\n" + "\n".join(f"- {e}" for e in errors))
        return 1
    print(f"VALID: {len(topics)} topic card(s)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_topic_cards.py topic-cards.json")
    raise SystemExit(main(sys.argv[1]))
