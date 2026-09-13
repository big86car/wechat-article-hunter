#!/usr/bin/env python3
"""Initialize a recoverable WeChat article workspace."""

import argparse
import json
import re
from datetime import date
from pathlib import Path


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower().strip()).strip("-") or "article"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default="")
    parser.add_argument("--topic-direction", default="")
    parser.add_argument("--audience", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--slug", default="")
    parser.add_argument("--root", default="wechat-articles")
    parser.add_argument("--source-languages", default="en")
    parser.add_argument("--time-window-days", type=int, default=7)
    parser.add_argument("--target-characters", type=int, default=3000)
    args = parser.parse_args()
    slug = slugify(args.slug or args.title or args.topic_direction)
    workspace = Path(args.root) / f"{date.today().isoformat()}-{slug}"
    workspace.mkdir(parents=True, exist_ok=False)
    (workspace / "images").mkdir()
    brief = {
        "schema_version": "1.0", "title": args.title,
        "topic_direction": args.topic_direction, "target_audience": args.audience,
        "objective": args.objective, "account_positioning": "",
        "voice": ["专业", "有判断", "清晰"],
        "source_policy": {
            "languages": [x.strip() for x in args.source_languages.split(",") if x.strip()],
            "exclude_domains": [], "prefer_primary_sources": True,
            "time_window_days": args.time_window_days
        },
        "article": {"type": "auto", "target_chinese_characters": args.target_characters, "call_to_action": ""},
        "delivery": {"scope": ["topic", "research", "outline", "article", "images", "html"], "draft_box_only": True},
        "materials": [], "status": "initialized"
    }
    (workspace / "article-brief.json").write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(workspace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
