# Round 1 forward outputs

The X/Y mapping was hidden from reviewers. X is the no-skill baseline; Y is PR #7 at commit `a94e000f023076de542b709546afc6131a8a2e39`.

## Output X — baseline

### Case A
Decision: do not fund three months of full development or claim a national market; validate evidence and commercial assumptions first. Known: only a single-center retrospective result and plan. Unknown: user, buyer, willingness to pay, data rights, deployment cost, device class and code ownership. Minimum next step: interview imaging users and hospital procurement/information/device staff; verify data/code rights and regulation; design a small prospective validation and cost estimate. Stop if rights/compliance cannot be solved, prospective performance is inadequate, or no buyer/real need exists. Do not enter a formal pilot or scale; at most bounded discovery validation.

### Case B
Decision: a controlled paid pilot may begin, with human-genomic-cloud compliance as a prerequisite. Known: public code, three replications, dated paid contract, defined user/payer and preliminary license review. Unknown: cloud-genomic-data compliance. Minimum next step: legal/ethics/security review of authorization, region, storage, transfer, access and deletion; use synthetic/de-identified data or compliant local deployment until confirmed. Stop if no lawful basis, a material license conflict or failed replication. Controlled pilot allowed; scale not allowed before compliance and acceptance close.

### Case C
Decision: use the literature-verification workflow and add no market judgment. Obtain the five claims, full citations and originals, then record identity, evidence match and conclusion. If authoritative metadata or full text cannot be accessed, mark unable to verify rather than guess. Pilot/scale does not apply.

### Case D
Decision: do not conclude that no global competitor exists; say only that the initial search did not confirm a peer. Snippets are the only known evidence. Verify official sites, registries, papers, code and procurement records; expand synonyms, indications and regions. Stop making an exclusionary claim while evidence remains snippets. No scale decision is supported.

## Output Y — candidate

### Case A
Decision: `HOLD_NEED_CUSTOMER_EVIDENCE`, retaining `HOLD_IP_OR_REGULATORY`; do not fund full development or claim a national market. Known: prototype, single-center retrospective result and plan. Unknown: real user/payer, procurement, demand/payment, data authorization, deployment cost, device class, code ownership and serviceable market. Minimum next step: 5–10 hypothesis-driven interviews across at least two buying roles; verify procurement, rights, regulatory path and deployment cost; predefine prospective thresholds. Stop if no budget owner/payment signal, an unresolvable rights/regulatory block, or failed prospective threshold. No pilot or scale; a controlled pilot requires a willing site, authorized data and legal/safety feasibility.

### Case B
Decision: hold; after closing compliance, `GO_CONTROLLED_PILOT` may be considered. Known: public code, three replications, dated paid-trial contract, clear user/payer and preliminary license review. Unknown: lawful human-genomic-cloud processing, authorization, hosting and security. Minimum next step: professional compliance review, data-processing agreement, approved hosting plan and predefined success/exit measures. Stop if no lawful path or authorized data, or the pilot misses replication, value or safety thresholds. A controlled paid pilot is conditional; scale requires separate diligence.

### Case C
Decision: `FACT_CHECK/LITERATURE`; route to reference verification, not commercial intelligence. Verify identity via publisher, Crossref and PubMed and classify each sentence as supported, conditionally supported or unsupported at the available read depth. Stop when all five have traceable conclusions or an uncircumventable evidence block occurs. Pilot/scale does not apply.

### Case D
Decision: `INSUFFICIENT`; do not assert global absence. Two snippets are discovery leads only; official product, regulatory, paper, code and procurement evidence and global/language coverage are unknown. Define region, time and competitor criteria; search synonyms, adjacent solutions and counterevidence, and verify authoritative/original sources. Stop when decision-critical claims reach the required depth, marginal gain vanishes, budget is exhausted or a block occurs. The competition gate remains `UNKNOWN`; no pilot or scale.
