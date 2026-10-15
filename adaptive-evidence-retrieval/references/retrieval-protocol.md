# Search protocol and reusable schemas

## Search plan
Record task_id; decision; as_of_date; jurisdictions; populations; source classes; evidence depth; query families; budget (calls/pages/full texts); exclusions; stop rule.

## Query construction
Represent each query as concept blocks; include exact quoted terms, controlled vocabulary (e.g. MeSH when applicable), orthographic and field synonyms, mechanisms, predecessor terminology, implementation aliases and language variants. Avoid asserting that a term absent from one platform means absent universally.

## Log schema (CSV fields)
task_id,pass_id,timestamp_utc,engine_or_database,query,filters,language,results_reported,results_inspected,unique_relevant,decision_relevant_new,source_ids,limitations,tool_cost_if_known

Do not fabricate result counts. Use UNKNOWN when unreported.

## Evidence schema (CSV fields)
claim_id,claim_text,source_id,source_url,publication_date,retrieval_date,source_type,read_depth,locator,direction,verification_status,independence_group,notes

read_depth: SNIPPET | METADATA | ABSTRACT | PARTIAL_FULLTEXT | FULLTEXT | SUPPLEMENT.
verification_status: VERIFIED | PARTIAL | CONFLICTED | UNKNOWN.

## Retrieval prioritization
Score possible next moves qualitatively on:
- decision impact: would this source alter GO/HOLD/STOP?
- expected reliability and directness;
- remaining uncertainty;
- access/legal/monetary cost;
- novelty relative to already seen evidence.

Low impact, repetitive searches should stop before expensive searches. A fresh official page can be necessary even when an old paper appears authoritative.

## Adversarial queries
Use: "earlier method", "replication", "negative study", "correction", "retraction", "known limitation", "benchmark leakage", "issue", "pricing", "customer complaint", and topic-specific competing terminology. Independently examine the strongest contradicting source; never fabricate an opposition case.

## Regression mini-benchmark
Use at least 10 fixed cases before claiming improved retrieval skill; recommended later 30+ across literature, code, guidelines, market and known false-negative cases. Compare with baseline agent under identical model, tools, budget, dates. Measure evidence recall against human-labeled gold sources, citation correctness, contradiction discovery, search cost, unsupported-claim rate, and abstention when sources are unavailable. Do not optimize to report verbosity. 
