---
name: wechat-article-hunter
description: Orchestrate an evidence-based, original WeChat Official Account article from topic discovery through research, outline, writing, originality review, editing, image direction, layout, and draft-box delivery. Use for a complete公众号内容流水线, multi-stage production, or resuming an existing article workspace; use a child skill for a clearly requested single stage.
---

# WeChat Article Hunter

Coordinate the suite without duplicating child-skill details. Preserve the user's topic, audience, position, voice, source restrictions, output length, and publishing boundary in `article-brief.json`.

## Route the Request

- Full workflow, “从选题到文章”, “图文并茂”, or uncertain starting point: use this skill.
- A clearly isolated task on an existing artifact: use the matching child skill directly.
- If the user requests only topic candidates, stop after presenting topic cards and wait for selection.
- If the user supplies a final topic, begin at research unless they explicitly want an outline or draft without research.
- If a workspace exists, inspect its artifacts and resume from the first incomplete or stale stage. Never silently overwrite user edits.

## Child Skills

Read the relevant child `SKILL.md` immediately before that stage:

1. `wechat-topic-hunter`
2. `wechat-content-research`
3. `wechat-article-outline`
4. `wechat-article-writer`
5. `wechat-originality-gate`
6. `wechat-article-editor`
7. `wechat-image-director`
8. `wechat-layout`
9. `wechat-draft-publisher`

## Establish the Brief

Infer fields already given. Ask only when a missing choice would materially change the result, usually audience or account positioning. For a new article, use `scripts/init_article.py` or create an equivalent brief conforming to [references/artifact-contract.md](references/artifact-contract.md).

Required brief fields: topic or discovery direction, target audience, communication objective, account positioning and voice when known, source policy and time window, desired length and delivery scope, and user-supplied materials.

Default source policy: prefer primary, authoritative, globally accessible sources; avoid content farms and unattributed aggregation. Exclude Chinese-language web sources when the brief requests it. Never weaken a source restriction silently.

Do not make bulk WeChat scraping, session-token extraction, CAPTCHA bypass, client impersonation, proxy rotation, or access-control evasion part of the workflow. WeChat competitor material must be public, user-provided, or obtained through an authorized export/integration. The pipeline creates original analysis; it does not perform synonym substitution or “洗稿”.

## Run the Workflow

For each stage, confirm required inputs, read the child skill, produce its named artifact, apply its gate, and record assumptions or unresolved items.

| Stage | Input | Output | Gate |
|---|---|---|---|
| Topic | brief/direction | `topic-cards.json` | scores justified; sources and Why Now included |
| Research | selected topic | `research-pack.md`, `source-ledger.json` | material claims trace to credible sources |
| Outline | research pack | `outline.md` | one thesis; section purpose and evidence explicit |
| Writing | outline + research | `draft.md` | complete article; no fabricated facts or citations |
| Originality | draft + ledger + references | `originality-report.json` | provenance complete; original value present; no blocking reuse risk |
| Editing | draft + ledger | `review-report.md`, `article.md` | blocking issues resolved or visibly flagged |
| Images | final article | `image-plan.md`, `images/` | visuals have purpose and rights status |
| Layout | article + images | `article.html`, `article.txt` | no internal notes; mobile-readable; links preserved |
| Draft delivery | HTML + cover | `publish-receipt.json` | account confirmed; scope authorized |

## Human Checkpoints

Pause after topic cards unless autonomous selection was authorized. Pause before changing an approved thesis. A failed originality gate returns the article to research, outline, or writing; never “lower similarity” mechanically. Draft-box delivery requires explicit intent and account confirmation. Public publishing or mass-send always requires separate explicit authorization and is outside the default workflow.

## Completion

Report title, completed stages, artifact locations, unresolved risks, and next action. Claim success only when an artifact exists and passes its gate. A draft-box receipt is not proof of public publication.
