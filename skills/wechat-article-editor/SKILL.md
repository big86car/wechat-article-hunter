---
name: wechat-article-editor
description: Review and revise a Chinese WeChat article for factual support, reasoning, structure, native style, reader value, and publication readiness. Use for 审稿, 润色, fact-checking, removing AI-like prose, or producing a final article from a draft and evidence ledger.
---

# WeChat Article Editor

Edit with an auditable two-output workflow: `review-report.md` records decisions; `article.md` is the clean reader-facing final. Preserve intentional author voice and do not rewrite merely to make wording different.

## Review Passes

1. **Evidence:** map every material claim to `source-ledger.json`; reject fabricated or overstated support.
2. **Reasoning:** test causal jumps, false binaries, inconsistent comparisons, missing counterarguments, and conclusions stronger than premises.
3. **Structure:** check that opening, section order, transitions, and ending serve the thesis.
4. **Reader value:** remove repetition and add only evidence-backed context needed by the target reader.
5. **Language:** remove translation patterns, formulaic AI phrasing, empty emphasis, excessive headings, and monotonous sentence rhythm.
6. **Publication:** check title/claim alignment, links, image markers, sensitive assertions, disclosure needs, and unresolved placeholders.

Read [references/review-rubric.md](references/review-rubric.md). Classify findings as `blocking`, `major`, or `minor`.

## Outputs

`review-report.md` must summarize verdict, scorecard, claim-level issues, structural changes, style changes, remaining risks, and evidence gaps. State which changes were applied.

`article.md` must contain only recommended title, optional deck, and final body. Remove alternative titles, internal notes, source-ledger IDs, prompt text, and unresolved placeholders. Preserve reader-facing citations.

## Validate

Run `scripts/validate_article.py article.md`. Fix mechanical failures, then perform human judgment on evidence and tone. If a blocking claim cannot be verified, remove or qualify it and record the decision.
