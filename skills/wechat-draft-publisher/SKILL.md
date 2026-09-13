---
name: wechat-draft-publisher
description: Prepare or submit a finalized WeChat article to an Official Account draft box with explicit authorization and auditable receipts. Use only when the user asks to prepare, upload, or deliver a completed article to 微信公众号草稿箱; never infer permission to publish publicly or mass-send.
---

# WeChat Draft Publisher

This is a controlled external-mutation stage. Draft-box upload is the maximum default scope. It does not authorize public publication, mass-send, scheduled release, credential changes, or deletion of existing drafts.

## Preconditions

Require `article.html`, final title, author when required, digest, and a valid cover asset. Inspect the output from the layout skill and confirm there are no local-only image URLs, placeholders, scripts, or private notes.

Before any network mutation:

1. Confirm the target Official Account when more than one account may exist.
2. Confirm the user wants an actual draft-box submission, not merely a package or dry run.
3. Use only credentials already configured for the relevant publishing tool. Never request that secrets be pasted into chat or write them into artifacts/logs.
4. Validate image upload requirements and platform limits with the current connector or official API documentation.

If no authenticated publishing capability is available, create a handoff package and precise next steps; do not claim submission.

## Submission

Upload inline images through the supported publishing path and replace local references with returned hosted URLs. Upload the cover as required, then create one draft using the final title, author, digest, source URL when applicable, and HTML body.

Do not retry indefinitely. For authentication, permission, IP allowlist, quota, or validation failures, stop after one safe diagnostic retry at most and preserve the prepared package.

## Receipt

Write `publish-receipt.json` following [references/receipt-schema.md](references/receipt-schema.md). Redact tokens and secrets. Report “draft created” only when the platform returns a successful draft identifier. Explicitly state that the item is not publicly published.

Public publication or mass-send is outside this skill's default scope and requires a separate, explicit user request immediately before that action.
