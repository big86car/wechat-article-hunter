# Artifact Contract

Use `wechat-articles/YYYY-MM-DD-<ascii-slug>/` unless the user supplies another location. Keep generated artifacts inside it and preserve source files.

## `article-brief.json`

```json
{
  "schema_version": "1.0",
  "title": "",
  "topic_direction": "",
  "target_audience": "",
  "objective": "",
  "account_positioning": "",
  "voice": ["专业", "有判断", "清晰"],
  "source_policy": {
    "languages": ["en"],
    "exclude_domains": [],
    "prefer_primary_sources": true,
    "time_window_days": 7
  },
  "article": {"type": "auto", "target_chinese_characters": 3000, "call_to_action": ""},
  "delivery": {"scope": ["topic", "research", "outline", "article", "images", "html"], "draft_box_only": true},
  "materials": [],
  "status": "initialized"
}
```

`source_policy.languages` controls source language, not article language. Empty means no language restriction. Record unavailable evidence rather than weakening policy silently.

Treat a downstream artifact as stale when an approved upstream artifact changes materially. Preserve old files by versioning; do not overwrite user edits without inspection.
