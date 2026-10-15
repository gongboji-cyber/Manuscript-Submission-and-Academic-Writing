# Case 001: Pulmonary Fungal CT AI Commercialization — Regression Fixture

## Date and provenance
2026-10-15. Source material: user-provided 20-page commercialization proposal (confidential; NOT uploaded to this public repo). All details below are public-domain generalizable audit patterns, not the private proposal text. Sources and results must be revalidated in future runs.

## Expected agent behavior (PASS/FAIL)
1. Differentiate image processing/quantification from automated abnormality detection and disease diagnosis when assigning NMPA class. A 2023 NMPA device-review guideline describes abnormality highlighter AI assisting clinician as III-class auxiliary detection. FAIL if the agent automatically labels all sign detection as class II merely because its output is a lesion description.
2. Distinguish software *item* price from procurement-package total; check whether upfront sale is recurring annual revenue. FAIL if procurement of RMB 250k once becomes RMB 250k ARR.
3. Market sizing must be bottom-up: 2024 official count of 4111 tier-III Chinese hospitals is not equivalent to specialty-eligible paying hospitals, and latest base year must be stated. FAIL if arbitrary 5000 tier-III hospitals becomes empirically established TAM.
4. Distinguish case-enriched/internal AUC from external sensitivity, spectrum, prevalence, PPV and real-world clinical net benefit. Public PA versus BP research reported external AUC 0.81 and sensitivity 60.6%; FAIL if marketed as robust independent rule-out.
5. Distinguish adjacent CT nodule and pneumonia AI providers from *verified approved* fungal-etiology competitors; no search hit is not proof of their absence. FAIL on 'no competition / first ever' without comprehensive register search.
6. Separate user, purchaser and budget owner; web reviews are not buyer willingness-to-pay. Without actual interviews, G6 stays NOT_TESTED.
7. Treat patent applications and collaboration claims as unverified for exclusive commercial rights; require documentary IP/data/license authorization.
8. Forecast cash flow using license term, channel costs, deployment, support, clinical trials, regulatory/quality and delay, not gross transaction price alone.

## Verified public starting points
- NMPA classification: https://www.beijing.gov.cn/zhengce/zhengcefagui/qtwj/202204/t20220408_2669468.html
- NMPA auxiliary detection evaluation (2023): https://www.ydcmdei.org.cn/article/261
- NHC hospitals census (2024 year): https://www.nhc.gov.cn/guihuaxxs/c100133/202512/f1c3a3c617484a27a1a26a468afbaeee/files/2024%E5%B9%B4%E6%88%91%E5%9B%BD%E5%8D%AB%E7%94%9F%E5%81%A5%E5%BA%B7%E4%BA%8B%E4%B8%9A%E5%8F%91%E5%B1%95%E7%BB%9F%E8%AE%A1%E5%85%AC%E6%8A%A5-20251201161542231.pdf
- PA vs bacterial pneumonia multicenter model: https://jtd.amegroups.org/article/view/123921/html
- Clinical buyer price examples: https://www.ccgp.gov.cn/cggg/dfgg/zbgg/202603/t20260305_26232061.htm
- https://www.ccgp.gov.cn/cggg/dfgg/zbgg/202503/t20250312_24289584.htm

## Testing
Run baseline without either skill and intervention with both skills under fixed model, tool capability, input, query budget and date. Have independent reviewer label claim-level support, citations, forbidden overclaims, cost. Record missing evidence as UNKNOWN. Do not report a measured skill uplift until test runs and scores exist.
