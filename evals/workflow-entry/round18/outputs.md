# Round 18 verbatim outputs

Mapping was concealed from reviewers until scoring: System X = candidate, System Y = baseline.

## System X, replication 1

### Case A

1. **Selected skills:** `coordinate-research-workflow`; `adaptive-evidence-retrieval`.
2. **Ordered first actions:** Freeze package, parser, old/new versions, wrapper commit, input schema, and observed discrepancy. Form three competing hypotheses: release change, malformed input, wrapper defect. Inspect official documentation, changelog/release notes, repository code/tests, and relevant issues for the pinned versions. Create one minimal synthetic file varying only the suspected field; run it through the package directly and through the wrapper using already-approved environments.
3. **Stopping/hold condition:** Stop once the direct-versus-wrapper and old-versus-new results distinguish the three hypotheses. Hold if versions cannot be reproduced or testing would require an unknown dependency; report the smallest missing evidence.
4. **Artifacts:** Versioned evidence ledger; hypothesis/test matrix; synthetic-file specification; command/result record; contradiction log; bounded cause verdict; four-part change-impact record.

### Case B

1. **Selected skills:** `coordinate-research-workflow`; `adaptive-evidence-retrieval`; `commercial-intelligence`.
2. **Ordered first actions:** Freeze intended clinical use, jurisdictions, hospital user, payer, workflow, genomic-data route, decision horizon, and pilot success metric. Build source/query families for competitors, dated pricing, procurement, bottom-up market sizing, regulatory classification, privacy/security, IP/data rights, and contrary evidence. Separate buyers from users and validate demand through customer interviews and willingness-to-pay testing.
3. **Stopping/hold condition:** Current verdict: `HOLD_IP_OR_REGULATORY`; G6 validation is `NOT_RUN`. Do not start a paid hospital pilot next month until jurisdiction-specific privacy review and credible customer interviews are complete.
4. **Artifacts:** Commercial hypothesis; customer/payer map; competitor matrix; pricing evidence; TAM/SAM/SOM sensitivity model; regulatory/IP/privacy risk register; interview plan; falsification experiments; gate-by-gate verdict.

### Case C

1. **Selected skills:** `coordinate-research-workflow`; `retrieve-and-match-references`.
2. **Ordered first actions:** Lock the cited reference and manuscript sentence. Resolve DOI and publication identity across publisher, PubMed, and Crossref metadata; check version, correction, or retraction status. Read the relevant Results text/table. Split the sentence into two claims: improved sensitivity and no reduction in specificity; verify comparator, denominators, estimates, intervals, and inferential basis separately.
3. **Stopping/hold condition:** Stop when DOI identity, exact passage location, and both subclaims can be classified. Hold unsupported components if only abstract-level evidence or inaccessible full text is available.
4. **Artifacts:** Verified citation record; Results passage locator with a brief compliant excerpt; two-row claim–evidence map; verdict of direct, conditional, unsupported, or contradicted; narrower replacement sentence if required.

### Case D

1. **Selected skills:** `coordinate-research-workflow`; `audit-and-polish-manuscript`.
2. **Ordered first actions:** Lock `147`, `1,460`, `82%`, `91%`, and the sensitivity/specificity pairing. Apply a conservative sentence-level edit, then compare every protected item and ensure no evidentiary claim was added.
3. **Stopping/hold condition:** Stop after the single-sentence fidelity check passes; do not expand into manuscript, statistical, or reference review.
4. **Artifacts:** “Sensitivity was 82% among 147 cancers, and specificity was 91% among 1,460 negative examinations.” Minimal change note confirming unchanged numbers and no added evidence.

## System X, replication 2

### Case A

1. **Selected stable skill:** `adaptive-evidence-retrieval`
2. **Ordered first actions:**
   1. Freeze three competing explanations: release behavior change, malformed input, or wrapper defect.
   2. Record exact package/runtime/wrapper versions, input bytes, configuration, observed output, and expected output.
   3. Compare official documentation, release notes/changelog, and relevant parser code for the current and preceding versions.
   4. Run one minimal synthetic fixture through the parser directly and through the wrapper, varying only the disputed field; use existing trusted environments and install no unknown dependency.
   5. Map each observation to predictions from the three explanations and seek one disconfirming observation for the leading explanation.
3. **Stopping/hold condition:** Stop once the observations distinguish the alternatives, or hold when unavailable historical binaries/source or an unreproducible environment prevents discrimination. Do not broaden after the decision-critical gap closes.
4. **Artifacts:** Version/environment record; source and search log; synthetic fixture specification; direct-versus-wrapper result table; evidence/contradiction ledger; bounded verdict (`SUPPORTED`, `CONDITIONAL`, `INSUFFICIENT`, or `CONTRADICTED`) with minimal next test.

### Case B

1. **Selected stable skills:** `adaptive-evidence-retrieval` → `commercial-intelligence`
2. **Ordered first actions:**
   1. Freeze intended use, jurisdiction, hospital user, payer/procurement owner, deployment/hosting model, clinical claim, decision horizon, and data/IP ownership.
   2. Build adversarial source families covering direct and substitute competitors, official pricing/procurement evidence, buyer demand, bottom-up market size, patents/licenses, regulatory classification, privacy, security, reimbursement, and failure/adoption barriers.
   3. Separate observed facts from marketing claims, forecasts, assumptions, and unknowns.
   4. Score G0–G6; explicitly mark customer interviews and willingness-to-pay validation `NOT_RUN`.
   5. Design privacy/legal review and customer-discovery tests before any identifiable genomic upload or paid clinical pilot.
3. **Stopping/hold condition:** **HOLD_IP_OR_REGULATORY** and **HOLD_NEED_CUSTOMER_EVIDENCE**. Do not recommend a paid hospital pilot next month until jurisdiction-specific privacy/regulatory review and credible buyer interviews are completed.
4. **Artifacts:** Commercial hypothesis; customer/payer map; competitor and pricing matrix; bottom-up TAM/SAM/SOM scenarios; evidence/contradiction ledger; regulatory/privacy/IP risk register; falsification experiments; gate table and dated hold verdict.

### Case C

1. **Selected stable skill:** `retrieve-and-match-references`
2. **Ordered first actions:**
   1. Assign one claim ID and split the sentence into two subclaims: improved sensitivity and no reduction in specificity.
   2. Verify title, authors, journal, publication version, DOI/PMID, and correction/retraction status using authoritative metadata and the publisher record.
   3. Read the paper’s relevant Results text/table, recording exact location, comparator, population, thresholds, denominators, estimates, and intervals.
   4. Test each subclaim against the reported comparison; do not infer preserved specificity from silence, nonsignificance, or a different threshold.
3. **Stopping/hold condition:** Stop after identity and both subclaims are resolved. Hold the support verdict if the Results passage or necessary comparator data are inaccessible; label reading depth accurately.
4. **Artifacts:** Verified bibliographic record; short compliant Results excerpt with page/section/table locator; two-row claim–evidence map; verdict for each subclaim (`directly supports`, `conditionally supports`, `contradicts`, `does not support`, or `not evaluated`); narrower replacement sentence if needed.

### Case D

1. **Selected stable skill:** `audit-and-polish-manuscript`
2. **Ordered first actions:**
   1. Limit scope to the supplied sentence.
   2. Lock the protected elements: 147 cancers, 1,460 negative examinations, 82% sensitivity, and 91% specificity.
   3. Improve concision and parallel structure.
   4. Recheck every number, denominator label, metric, and direction against the original.
3. **Stopping/hold condition:** Stop after one conservative revision and fidelity check. Hold only if “147 cancers” is intended to mean patients, lesions, or examinations, because clarification would require author input.
4. **Artifacts:** Polished sentence: “Among 147 cancers and 1,460 negative examinations, sensitivity and specificity were 82% and 91%, respectively.” Brief change note confirming that no number or evidentiary claim was added or altered.

## System Y, replication 1

### Case A

1. **Workflow/tool:** Minimal differential-reproduction workflow using official documentation/release notes, parser source or version diff, wrapper inspection, and one synthetic input.

2. **Ordered first actions:**
   1. Record the package, current and last-known-good versions, runtime, wrapper revision, exact command, and observed error.
   2. Reduce the disputed construct to one synthetic file.
   3. Run a controlled matrix: direct parser versus wrapper, on both versions if trusted official builds are already available.
   4. Compare behavior with official syntax documentation and release notes; inspect the relevant parser and wrapper code paths.
   5. Change only the suspected input feature once to test malformed-input behavior.

3. **Stopping/hold condition:** Stop when the matrix separates: version-dependent behavior, rejection by both paths indicating malformed input, or wrapper-only divergence. Hold if reproducing requires untrusted dependencies or unavailable versions.

4. **Artifacts:** Reproduction manifest, synthetic file, command/output matrix, official-evidence log, relevant code-diff notes, and a bounded conclusion with unresolved items.

### Case B

1. **Workflow/tool:** Staged commercial, clinical, regulatory/privacy, and IP diligence with a pilot-readiness gate.

2. **Ordered first actions:**
   1. Define intended use, jurisdictions, genomic data flow, clinical claims, and hospital users.
   2. Map competitors, buyers, procurement routes, and verifiable pricing models.
   3. Build bottom-up and top-down market-size ranges with explicit assumptions.
   4. Obtain jurisdiction-specific privacy, security, genomic-consent, regulatory-classification, and data-residency review.
   5. Conduct buyer/customer interviews and test willingness to pay.
   6. Have qualified counsel conduct focused patent/contract and freedom-to-operate review.
   7. Assess analytical/clinical validity and hospital integration requirements.

3. **Stopping/hold condition:** Do not start a paid hospital pilot next month until privacy/regulatory review, customer discovery, security contracting, intended-use boundaries, and clinical-validation gates are cleared. A synthetic-data, non-clinical evaluation may be considered separately.

4. **Artifacts:** Competitor/pricing matrix, buyer map, market-sizing model, regulatory/privacy/IP risk register, interview guide and findings, pilot gate checklist, and go/defer recommendation memo.

### Case C

1. **Workflow/tool:** `retrieve-and-match-references` plus targeted diagnostic-study critical appraisal.

2. **Ordered first actions:**
   1. Identify the paper from its full citation.
   2. Triangulate the DOI using the publisher record and bibliographic databases; check version, correction, and retraction status.
   3. Read the authorized full text and locate the exact Results passage, table, or figure.
   4. Record a brief exact excerpt and precise location.
   5. Determine whether sensitivity and specificity use the same cohort, threshold, comparator, and reference standard.
   6. Test whether “improves” is supported by a direct comparison and whether preserved specificity is demonstrated rather than inferred from nonsignificance.

3. **Stopping/hold condition:** Stop after DOI identity, passage, and support verdict are resolved. Hold the verdict if full Results text or necessary comparison details are inaccessible.

4. **Artifacts:** Verified DOI/citation record, passage with location, claim-to-evidence assessment, support verdict, and narrower replacement wording if needed.

### Case D

1. **Workflow/tool:** Conservative sentence-level academic polishing with a protected-numbers check.

2. **Ordered first actions:**
   1. Lock `147`, `1,460`, `82%`, `91%`, sensitivity, specificity, and their denominator associations.
   2. Improve parallelism and clarify which denominator belongs to each metric.
   3. Recheck every protected element against the original.

3. **Stopping/hold condition:** Stop after one meaning-preserving revision. Hold rather than reinterpret if “147 cancers” does not mean 147 cancer cases/examinations.

4. **Artifacts:** Revised sentence: “Sensitivity was 82% among 147 cancers, and specificity was 91% among 1,460 negative examinations.”

## System Y, replication 2

### Case A

1. **Workflow/tool:** Minimal parser-regression investigation using official documentation/release notes, source inspection, and a controlled synthetic reproduction.

2. **First actions:**
   1. Record package, parser, wrapper, runtime, and exact versions/configuration.
   2. Preserve the failing input and error/output without modifying it.
   3. Review official parser documentation and release notes between the last known-good and current versions.
   4. Inspect wrapper preprocessing and parser options.
   5. Create one synthetic file containing the smallest relevant construct.
   6. Run it directly through the parser and through the wrapper in available known-good/current environments.
   7. Compare raw bytes, normalized input, options, outputs, and errors.

3. **Stop/hold condition:** Stop once results distinguish version-dependent behavior, invalid input, or wrapper transformation. Hold if comparison requires installing an untrusted dependency or unavailable historical environment.

4. **Artifacts:** Reproduction matrix, synthetic fixture, minimal test command/script specification, evidence-linked root-cause memo, and targeted remediation recommendation.

### Case B

1. **Workflow/tool:** Staged commercial, regulatory, privacy, clinical-risk, and IP diligence—not an immediate launch recommendation.

2. **First actions:**
   1. Define jurisdiction, intended use, users, data flow, and clinical claims.
   2. Map direct/adjacent competitors, buyers, workflows, pricing models, and procurement cycles.
   3. Estimate market using transparent bottom-up assumptions.
   4. Obtain qualified analysis of privacy, genomic-data rules, medical-device regulation, security, consent, data residency, and IP freedom-to-operate.
   5. Conduct buyer/customer interviews and test willingness to pay.
   6. Assess analytical/clinical validation, liability, integration, and hospital contracting requirements.
   7. Apply explicit pilot readiness gates.

3. **Stop/hold condition:** Hold any paid hospital pilot involving human genomic data until jurisdiction-specific privacy/regulatory review, security controls, validation boundaries, contracts, and buyer evidence are complete. Consider only synthetic-data discovery work meanwhile.

4. **Artifacts:** Competitor/pricing matrix, buyer map, market model with assumptions, regulatory/privacy/IP risk register, interview guide, pilot-readiness checklist, and conditional go/no-go memo.

### Case C

1. **Workflow/tool:** Targeted reference verification and claim-to-evidence matching.

2. **First actions:**
   1. Resolve the cited paper from its existing bibliographic details.
   2. Cross-check DOI metadata against authoritative DOI, bibliographic, and publisher records.
   3. Confirm article version and retrieve the Results section.
   4. Locate the exact relevant passage, table, cohort, comparator, estimates, and confidence intervals.
   5. Determine whether sensitivity increased and whether specificity was statistically and clinically preserved.
   6. Classify support as direct, partial, unsupported, or contradicted.

3. **Stop/hold condition:** Stop after paper identity and the narrow manuscript claim are adjudicated. Hold if full text or the relevant results are inaccessible; do not infer from the abstract alone.

4. **Artifacts:** Verified DOI/citation, exact passage with page/table locator and compliant excerpt, extracted estimates, and a concise support verdict with any qualified replacement wording.

### Case D

1. **Workflow/tool:** Constraint-preserving academic sentence polish.

2. **First actions:**
   1. Lock all numbers and claims.
   2. Improve grammatical flow only.
   3. Check that no interpretation or evidence was added.

3. **Stop/hold condition:** Stop after one faithful revision; hold if “cancers” is intended to mean patients, lesions, or examinations because that would require author clarification.

4. **Artifacts:** “Among 147 cancers and 1,460 negative examinations, sensitivity was 82%, and specificity was 91%.”
