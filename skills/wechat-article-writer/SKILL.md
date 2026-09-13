---
name: wechat-article-writer
description: Write or rewrite a source-grounded Chinese WeChat Official Account article from an approved brief, research pack, and outline. Use for 公众号正文, long-form drafting, converting supplied material into an article, or continuing an existing draft; do not invent research or silently change an approved thesis.
---

# WeChat Article Writer

Create `draft.md` as a native Chinese article optimized for mobile reading and professional credibility. Read the brief, outline, research pack, and source ledger. If a required claim is unverified, qualify or omit it rather than filling the gap from memory.

Use sources as evidence, not as a template. Do not preserve a source article's distinctive headline logic, section order, examples, metaphors, or conclusion and then merely change its wording. When supplied material dominates the brief, identify the new thesis, new evidence combination, or new audience application before drafting.

## Writing Priorities

1. Accuracy and intellectual honesty.
2. A clear, defensible point of view.
3. Reader value and information density.
4. Natural Chinese rhythm and scanability.
5. Shareability without clickbait.

## Draft

- Lead with the tension, result, or surprising fact; avoid ceremonial introductions.
- Keep most paragraphs to one idea and vary sentence length naturally.
- Use concrete examples, comparisons, and numbers when the ledger supports them.
- Distinguish reported fact from the author's inference with explicit wording.
- Cite material claims near the claim using readable Markdown links or compact source notes.
- Use headings as an argument map, not decorative labels.
- Explain technical terms at the reader's altitude; retain necessary precision.
- End with a synthesized judgment or useful action, not generic encouragement.

Read [references/style-guide.md](references/style-guide.md) for detailed language constraints. Preserve the author's stated voice. Do not claim first-hand testing, interviews, or personal experience unless supplied by the user.

## Titles and Visual Markers

Provide one recommended title plus 5 alternatives after the draft in a clearly marked editorial-notes section. Insert visual markers only where the outline requested them:

`<!-- IMAGE: purpose | suggested format -->`

Keep editorial notes and image markers out of the final reader-facing article; the editor and image director consume them later.

## Gate

Verify that the article follows the approved thesis, contains no rejected ledger claim, meets the requested length approximately, and has no invented citation. Then hand off `draft.md`, the source ledger, and all material provenance to `wechat-originality-gate` before editorial finalization.
