---
name: wechat-content-research
description: Build a source-grounded research pack and claim ledger for a Chinese WeChat article. Use after a topic is selected, when evaluating supplied links or documents, or when an article needs current facts, counterarguments, comparisons, and traceable citations; do not write the polished article.
---

# WeChat Content Research

Transform a selected topic into a defensible evidence base. Read the brief's source policy before searching. If a specific page, repository, paper, or current event is involved, open and inspect the primary material rather than relying on snippets.

Before acquiring competitor or WeChat-native material, read [references/content-acquisition-policy.md](references/content-acquisition-policy.md). If acquisition would require bypassing authentication, session controls, CAPTCHA, rate limits, client protocols, or another access control, stop and request a compliant input method.

## Route by Content Type

Read [references/research-routes.md](references/research-routes.md) and apply only the relevant route. For mixed topics, combine routes but maintain one claim ledger.

## Research Method

1. Translate the proposed thesis into research questions and possible falsifiers.
2. Gather primary sources first, then credible independent analysis for context and challenge.
3. For time-sensitive facts, record both event and publication dates.
4. Triangulate consequential or disputed claims. A single company statement supports what the company said, not necessarily that the claim is objectively true.
5. Separate `fact`, `inference`, `estimate`, and `opinion` in the ledger.
6. Capture the strongest counterargument and evidence that would change the conclusion.
7. Stop when the thesis can be supported and challenged without repetitive sources.

Do not cite search-result pages, fabricate URLs, or retain a claim after its source fails to support it. Respect source-language and excluded-domain rules from the brief. Record whether each user-supplied or competitor source may be quoted, summarized, or used only as an idea lead.

## Outputs

Create `research-pack.md` containing executive synthesis, timeline/context, confirmed facts, competing interpretations, counterarguments, implications for the reader, unresolved questions, and promising examples.

Create `source-ledger.json` using [references/source-ledger-schema.md](references/source-ledger-schema.md). Every material numeric, causal, comparative, legal, medical, financial, product, or time-sensitive claim intended for the article needs a ledger entry.

Also record `materials` provenance when the article is derived from supplied articles, transcripts, screenshots, or exports. The downstream originality gate needs this to distinguish public facts from source-specific expression and argument structure.

## Gate

Before handoff, test whether the proposed thesis overstates the evidence. Clearly flag low-confidence claims and exclude unsupported ones from the writing pack. Use links next to claims in the research pack so downstream writers can cite accurately.
