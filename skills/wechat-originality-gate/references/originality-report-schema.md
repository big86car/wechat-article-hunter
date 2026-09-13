# Originality Report Schema

```json
{
  "schema_version": "1.0",
  "article": "draft.md",
  "reviewed_at": "ISO-8601",
  "verdict": "pass|revise|block",
  "scores": {
    "provenance_completeness": 1,
    "attribution_integrity": 1,
    "expression_independence": 1,
    "structural_independence": 1,
    "original_value": 1
  },
  "original_contributions": [
    {"type": "thesis|synthesis|framework|first_party|audience_application|counterargument", "description": "", "evidence": ""}
  ],
  "findings": [
    {
      "severity": "blocking|major|minor",
      "category": "provenance|attribution|expression|structure|original_value",
      "source_id": "S01 or null",
      "article_location": "",
      "explanation": "",
      "route_to": "research|outline|writing",
      "required_change": ""
    }
  ],
  "manual_review_required": false,
  "notes": []
}
```

Set `manual_review_required` when source artifacts are unavailable, rights cannot be established, or automated comparison cannot evaluate the relevant visual/structural reuse.
