---
name: adaptive-evidence-retrieval
description: >-
  Evidence-first adaptive web and academic retrieval for scientific novelty, methods, guidelines, technical investigations and decision research. Use for 智能检索、深度研究、找证据、检索策略优化、反证检索、跨语言查询、来源追溯、搜索何时停止、GitHub与论文交叉核验. Route queries by decision and source; log search coverage, uncertainties and costs. This skill is not an automatic systematic review.
---

# Adaptive Evidence Retrieval | 自适应证据检索

## Contract
The objective is not maximum search volume but minimum defensible evidence for a decision. Use only actually available tools. Never claim a full-text read from a snippet, a comprehensive search from a few web results, a verified absence from failure to locate, or a successful tool call without a result. Do not upload private clinical data, manuscripts or unpublished IP to external services without permission. No automatic API purchases, package installs or bulk scraping.

### Routing
1. Convert request into a falsifiable decision question. Specify population/domain, geography, time window, language, scope, hard budget, expected decision and necessary evidence.
2. Classify intent: FACT_CHECK, LITERATURE, NOVELTY, GUIDELINE, SOFTWARE, MARKET, BROAD_SYNTHESIS. A single request may have multiple intents. Invoke established downstream skills rather than replacing them:
   - `retrieve-and-match-references` for bibliographic identity, literature reading and claim matching;
   - `research-topic-selection` for G0–G5 feasibility gates;
   - `critically-read-literature` for design and evidence appraisal;
   - `commercial-intelligence` for actual customer/competitor/market decisions.
3. Create query families: exact/official; controlled vocabulary and synonyms; broad adjacent concepts; competing hypotheses; negative and skeptical terms; forward/backward citation chains. Translate conceptual terms into English/Chinese where appropriate, not literal translation alone.
4. Route to source classes: publisher/DOI/PubMed/Crossref/OpenAlex; regulator/guideline institution; GitHub repository, code, issues, releases and changelogs; official company/product/pricing; filings and procurement; independent assessments. A search-engine summary is discovery, not proof.

## Adaptive search loop
For each pass: STATE a gap -> CHOOSE the query/source most likely to close it -> RETRIEVE -> EXTRACT an atomic claim with source location -> CROSS-CHECK -> UPDATE coverage and remaining unknowns. Prefer primary documents for decisive claims. Track whether a result is metadata-only, abstract-only, methods/results read, full-text read or supplement verified. Keep source ID, title, persistent URL/DOI, date of publication, retrieval date, version, page/section and quotation or tightly localized paraphrase.

Apply opposing-view searches before strong verdicts, e.g. earliest direct predecessor, contradictory estimates, corrections and retractions, alternative causal mechanisms, outdated software documentation, competitor with identical functionality. Multi-perspective questioning is a *query generation heuristic*, not independent validation. Duplicate syndications never count as independent corroboration.

Do not call multiple agents for trivial lookups. Parallel searches are justified only if source families are genuinely independent and time saved outweighs token/tool cost. Reuse cached source notes; avoid repetitive keyword permutations without measurable retrieval gain.

## Stop / escalate
Stop when (a) each decision-critical claim is supported at the required depth, (b) an explicit blocking unknown prevents a verdict and no permitted next step closes it, (c) new search passes return no new decision-relevant evidence, or (d) cost/time/source budget is reached. Record which condition fired. Do not call budget-exhausted research exhaustive. For time-sensitive findings, include as-of date and revalidation triggers.

## Mandatory output
- Decision question, date window and source coverage, including uncovered databases/regions.
- Search log (query, source, date, filters, retrieved/assessed counts if known, useful yields, errors, read depth).
- Evidence ledger: C-ID, atomic claim, source ID/URL, exact location, primary/secondary, for/against, verification state, confidence rationale.
- Contradiction ledger, critical unknowns, minimum next evidence needed.
- A bounded verdict: SUPPORTED / CONDITIONAL / INSUFFICIENT / CONTRADICTED, never equating no-find with nonexistence.
- Reusable search terms and next-run delta; do not reveal private or copyrighted full-text content.

Use [protocol](references/retrieval-protocol.md) and [source attribution](references/sources-and-adaptations.md). This is a cross-cutting retrieval engine; downstream scientific or commercial judgment retains its own gates.
