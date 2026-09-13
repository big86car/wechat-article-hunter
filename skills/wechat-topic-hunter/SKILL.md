---
name: wechat-topic-hunter
description: Discover, evaluate, and rank WeChat Official Account article topics using current evidence, audience fit, and differentiation. Use for 热点选题, topic ideation, editorial planning, title directions, or evaluating whether a proposed topic is worth writing; do not draft the full article.
---

# WeChat Topic Hunter

Produce decision-ready topic cards, not a list of generic headlines. Read `article-brief.json` when present and preserve its audience and source policy.

## Choose the Mode

- **Defined topic:** test the topic and propose 3–4 differentiated angles.
- **Defined domain:** discover and rank 5–10 candidates within the domain.
- **Open discovery:** first establish account positioning and audience; ask one focused question if neither can be inferred.
- **Editorial series:** create a coherent learning or narrative sequence, not unrelated posts.

## Discover Signals

Search across several relevant signal classes: primary announcements, product or policy changes, credible reporting, research, developer communities, search interest, and sustained practitioner discussion. Match the brief's time window and source-language/domain restrictions. For current topics, verify event date separately from publication date.

Do not equate virality with fit. Remove duplicates, rumors without independent confirmation, topics whose value is only a translated recap, and topics the account cannot add insight to.

## Score Candidates

Read [references/scoring-model.md](references/scoring-model.md). Score each dimension 1–5 with a one-sentence justification. Compute `weighted_score` on a 100-point scale. Add confidence based on evidence quality and signal agreement.

## Produce Topic Cards

Write `topic-cards.json` following [references/topic-card-schema.md](references/topic-card-schema.md). Each card must contain:

- a concrete angle rather than a broad subject
- `why_now` with dated evidence
- reader problem or tension
- differentiated thesis and what competing coverage misses
- 3–5 title directions spanning at least two styles
- evidence leads, counterargument, effort estimate, shelf life, and risks
- dimension scores and weighted score

Present the top candidates in a compact comparison and recommend one with reasoning. Unless autonomous selection is authorized, stop for the user's choice before research or drafting.

## Validate

Run `scripts/validate_topic_cards.py topic-cards.json`. Fix structural errors before handing off. A passing schema does not replace editorial judgment.
