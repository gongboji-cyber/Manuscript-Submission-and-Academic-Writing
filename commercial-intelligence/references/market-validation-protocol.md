# Commercial research protocol

## Explicit evidence classes
- VERIFIED_PRIMARY: first-party registry/filing/tender/product documentation showing the claimed fact.
- VERIFIED_INDEPENDENT: independent verifiable confirmation.
- VENDOR_CLAIM: self-reported marketing (not independently validated).
- PROXY: search interest, posts, downloads, review count, job openings, etc.
- ASSUMPTION: declared model input not confirmed by evidence.
- UNKNOWN: source inaccessible or no verified data.

## Market sizing
TAM = total relevant potential buyers × plausible annual spend (units, geography and product scope explicit).
SAM = buyers product can legally and operationally serve × relevant annual spend.
SOM = reachable contracted customers under stated channels/capacity/adoption scenario × net annual revenue.
These are modelling definitions, not empirical universal identities. Cross-check top-down reports only after reconciling scopes and units; list low/base/high with reasons. Never quote exact currency estimates unsupported by inputs; unknown inputs yield ranges or an unquantified verdict.

## Competitor record
competitor_id,organization,product,target_user,payer,region,use_case,direct_or_substitute,feature_claim,independent_verification,price_value,price_basis,price_as_of,source_url,source_locator,uncertainty

## Translation-specific questions
Who legally owns invention and source code? Are source data/model weights commercially licensable? Is software research-use-only? Does intended use trigger medical device obligations? Who bears data protection and cybersecurity compliance? Is there a reimbursement code, direct procurement line or budget owner? What validation is required for clinical adoption? What is the cheapest real prospective customer contact to refute demand?

## Tests before build
- 5–10 hypothesis-driven interviews across at least two buyer archetypes; not a statistically representative market survey.
- Workflow shadowing or documentary procurement verification.
- Landing page / pilot proposal / letter of intent as graded demand signals, never equivalent to paid contract.
- Predefined success and abandonment thresholds; no shifting target after feedback.
A count is a suggested pilot design, not evidence that interviews occurred.

## Output status logic
Web-only market scan => at most GO_CUSTOMER_DISCOVERY (if G0–G5 sufficiently supported, G6 NOT_TESTED).
GO_CONTROLLED_PILOT requires actual evidence of willing test site, authorized data and legal/safety feasibility. GO_SCALE is deliberately outside this skill; separate diligence required.
