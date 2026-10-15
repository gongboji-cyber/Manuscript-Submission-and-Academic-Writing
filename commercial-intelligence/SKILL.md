---
name: commercial-intelligence
description: >-
  Source-traceable web-based market research, competitive intelligence and translational commercialization triage. Use for 商业调研、成果转化、竞品分析、用户需求、TAM/SAM/SOM、市场进入、定价与付费者、医疗软件或生信产品商业化、监管与知识产权初筛. Separate evidence, assumptions, forecasts and hypotheses; never treat web research as proof of willingness to pay.
---

# Commercial Intelligence | 商业情报与成果转化

## Core principle
A technically interesting result is not automatically a sellable product. Optimize for a *commercial decision*, not for a polished market report. First use `adaptive-evidence-retrieval` to define sources, query families, adversarial searches and audit logs. Avoid unsupported market-size and revenue claims. Web signals are only proxies for real customer interviews or transactions.

## 1. Freeze the commercialization question
Specify technology maturity (idea/prototype/validated product), exact use case, target geography, customer and **payer** (may differ from user), alternatives including doing nothing, target workflow and integration, intended regulatory classification, IP ownership/permission, data privacy/hosting constraints and expected decision horizon. Missing facts are UNKNOWN, not favorable assumptions. Do not reveal unpublished invention claims or confidential code through external search.

## 2. Seven evidence lenses
1. Pain and customer: named job-to-be-done; whose time/money/risk; source-backed frequency/severity; actual purchasing actor and procurement pathway. Public complaints do not establish willingness to pay.
2. Competitors and substitutes: direct, adjacent, internal build, manual workflow, no-purchase; feature, independent validation, buyer segment, deployment, price *publication date*, procurement access. Unknown transaction price remains unknown.
3. Demand signals: public tenders, clinical/software adoption reports, customer postings, regulations, buyer reviews and observed deployments. Separate self-published claims from independently checked adoption.
4. Market size: bottom-up eligible buyers × addressable units × defensible achievable spend; TAM, SAM and SOM as explicit scenarios, not three percentages of a headline industry report. State geography, time and units; do not mix software revenue with healthcare expenditure.
5. Economics: setup, security, maintenance, serving compute, support, clinical validation, distribution, contract length, gross margins and procurement friction; scenarios, not facts when inputs are assumptions.
6. Moat and freedom to operate: prior patents, published algorithms, software licenses, datasets, trademarks, institutional ownership, patent status, IP diligence. Public search is preliminary and **not** a legal FTO opinion.
7. Regulation and safety: medical-device/SaMD/CDS scope by intended use and jurisdiction, evidence burden, quality system, privacy, reimbursement, security; flag need for qualified professional review. Claims about approval require official registry verification.

## 3. Research execution
Use official company documents, archived or dated pricing, filings, procurement notices, regulatory registries, patent databases and independently identified buyer evidence. Every factual cell has a source/locator/date. Seek disconfirming evidence: why an apparently strong product failed, low adoption, competitor parity, integration barriers, unpaid pilots, inaccessible reimbursement, weak data rights. Do not scrape paywalled or gated systems, forge accounts, or collect personal details.

The competitor matrix must separate MARKETING CLAIM, INDEPENDENT EVIDENCE, CURRENT PRICE, UNKNOWN and OBSERVED PRODUCT. Price quotes distinguish list, tender, paid invoice and modeled values. Never infer market share from search results or stars.

## 4. Decision gates
G0 USE_CASE: specific buyer/user/problem and measurable improvement.
G1 DEMAND: credible buyer signal and path to interviews; demand on the web alone is provisional.
G2 COMPETITION: differentiated benefit versus strongest substitute on same outcome.
G3 IMPLEMENTATION: feasible productization, data/license/access, workflow and operating cost.
G4 IP_REGULATION: preliminary risk register, blockers and required specialist confirmation.
G5 ECONOMICS: auditable bottom-up sizing, explicit assumptions, scenarios, unit economics.
G6 VALIDATION: actual interviews, willingness-to-pay experiments, pilots or contracts; NOT_RUN if absent.

Each gate PASS / FAIL / UNKNOWN / NOT_TESTED with evidence. Verdicts: EXPLORE, HOLD_NEED_CUSTOMER_EVIDENCE, HOLD_IP_OR_REGULATORY, GO_CUSTOMER_DISCOVERY, GO_CONTROLLED_PILOT, or STOP. A desktop-web scan alone cannot pass G6 or justify GO_SCALE. Missing source or customer data never silently becomes PASS or structural FAIL.

## Required deliverables
Commercial hypothesis one-pager; customer/payer map; ranked competitor/substitute matrix; evidence ledger and contradictory sources; bottoms-up TAM/SAM/SOM sensitivity table with formulae and currency/time; deployment/regulatory/IP risk register; top three falsification experiments; gate-by-gate verdict and stop conditions. Use [commercial research protocol](references/market-validation-protocol.md) and [sources](references/sources-and-adaptations.md). Cross-reference scientific evidence via existing `research-topic-selection` and literature modules, but keep clinical efficacy claims distinct from commercial viability.
