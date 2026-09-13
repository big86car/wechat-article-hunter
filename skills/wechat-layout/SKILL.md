---
name: wechat-layout
description: Convert a finalized Markdown article and image plan into clean, mobile-readable WeChat-compatible HTML and plain text. Use for 微信排版, HTML export, typography cleanup, or preparing content for the Official Account editor; do not alter the article's argument during layout.
---

# WeChat Layout

Lay out the approved `article.md`; do not introduce new claims or silently rewrite it. Read the image replacement map when present.

## Prepare

Remove internal comments, alternative-title blocks, workflow notes, and unresolved image markers. Confirm one final title is available separately from the body when the publishing method requires it.

## Render

Use `scripts/markdown_to_wechat_html.py article.md article.html` for the default theme. The script emits an HTML fragment with inline styles suitable for copying into a WeChat editor. Also create `article.txt` by preserving readable text and source URLs.

For custom styling, follow [references/layout-rules.md](references/layout-rules.md). Keep semantic structure and use inline CSS rather than external stylesheets, scripts, forms, iframes, or complex positioning.

## Visual QA

Inspect the result at a narrow mobile width. Check heading hierarchy, paragraph rhythm, list indentation, quote contrast, image width, captions, tables, link preservation, and end-of-article spacing. Tables wider than a phone should be simplified or rendered as an accessible image with an accompanying text summary.

## Gate

`article.html` must contain only reader-facing body content, resolve every local image reference, preserve material citations, and include no script or secret. Ensure the result remains understandable if images fail to load.
