---
name: wechat-originality-gate
description: Audit a draft WeChat article for provenance, attribution, distinctive-expression reuse, structural imitation, and genuine added value. Use before final editing when a draft relies on third-party articles, transcripts, research, or competitor content; do not use to evade plagiarism or platform-originality detection.
---

# WeChat Originality Gate

Decide whether the article is independently defensible, not whether superficial similarity can be reduced. Read `draft.md`, `source-ledger.json`, `research-pack.md`, `outline.md`, and every substantial source artifact available to the workspace.

## Audit

Read [references/originality-rubric.md](references/originality-rubric.md) and evaluate:

1. **Provenance:** every source has a known acquisition mode, rights basis, and permitted use.
2. **Attribution:** quotations, source-specific facts, graphics, anecdotes, and ideas are credited where needed.
3. **Expression:** no distinctive phrase, metaphor, example, or creative presentation is copied or closely paraphrased without permission.
4. **Structure:** the title logic, section order, evidence sequence, and conclusion do not reproduce a source article's creative arrangement.
5. **Original value:** the draft adds a defensible thesis, new evidence combination, original framework, first-party experience, or materially different audience application.
6. **Independence:** after removing any one reference article, the draft still has a coherent purpose and evidence base.

Text-similarity tools may identify passages for review, but a low similarity score is not proof of originality and a high score may be legitimate for names, facts, or attributed quotations. Never recommend synonym substitution, sentence shuffling, homoglyphs, translation loops, or other evasion tactics.

## Verdict

Create `originality-report.json` according to [references/originality-report-schema.md](references/originality-report-schema.md). Use:

- `pass`: provenance is complete, no blocking reuse remains, and original value is concrete.
- `revise`: issues can be corrected through attribution, independent restructuring, or new analysis.
- `block`: rights are missing, substantial distinctive expression/structure is reproduced, or the article has no meaningful independent value.

For `revise` or `block`, route each finding to `research`, `outline`, or `writing`. Do not directly produce a “lower similarity” rewrite.

## Validate

Run `scripts/validate_originality_report.py originality-report.json`. A structurally valid report still requires editorial judgment. Only a `pass` report may proceed to final editing when this gate applies.
