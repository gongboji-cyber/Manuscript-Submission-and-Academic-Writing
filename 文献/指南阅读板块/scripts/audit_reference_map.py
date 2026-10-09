#!/usr/bin/env python3
"""Offline structural/declared-scope citation audit. Never verifies scientific support."""
import argparse
from collections import defaultdict
from datetime import date, datetime, timezone
import hashlib
import json
import platform
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


READ = {'none', 'metadata', 'abstract', 'full_text_partial', 'full_text_and_relevant_supplement'}
SUPPORT = {'direct', 'qualified', 'background', 'contradicts', 'unsupported', 'unassessed'}
ROLE = {'background', 'method', 'recommendation', 'comparison', 'counterevidence', 'historical_retraction'}
ACTION = {'adopt', 'narrow', 'background_only', 'report_counterevidence', 'remove', 'hold'}
STATUS = {'unchecked', 'no_notice_found', 'corrected', 'expression_of_concern', 'retracted'}
TYPES = {'journal_article', 'guideline', 'preprint', 'method', 'resource', 'other'}


def nonblank(v):
    return isinstance(v, str) and bool(v.strip())


def normalize_doi(raw):
    v = raw.strip()
    v = re.sub(r'^doi:\s*', '', v, flags=re.I)
    if v.lower().startswith(('http://', 'https://')):
        u = urlsplit(v)
        if u.netloc.lower() in {'doi.org', 'dx.doi.org'}:
            v = unquote(u.path.lstrip('/'))
    return v.casefold()


def checked_date(v):
    if not nonblank(v):
        return False
    try:
        if len(v) == 10:
            date.fromisoformat(v)
        else:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def audit(obj):
    if not isinstance(obj, dict) or obj.get('schema_version') != 1 or isinstance(obj.get('schema_version'), bool):
        raise ValueError('Require schema_version: 1 object')
    refs, claims = obj.get('references'), obj.get('claims')
    if not isinstance(refs, list) or not isinstance(claims, list):
        raise ValueError('references and claims must be lists')
    errors, warnings = [], []
    def issue(target, code, where, detail):
        target.append({'code': code, 'location': where, 'detail': detail})
    def strings(record, fields):
        for key in fields:
            if key in record and not isinstance(record[key], str):
                raise ValueError(f'{key} must be a string')
    def source_list(record, field):
        vals = record.get(field, [])
        if not isinstance(vals, list) or not all(nonblank(x) for x in vals):
            raise ValueError(f'{field} must be a list of nonempty source URL strings')
        if any(urlsplit(x).scheme not in {'http', 'https'} or not urlsplit(x).netloc for x in vals):
            raise ValueError(f'{field} must contain HTTP(S) URLs')
        return vals
    by_id = {}
    doi_groups, pmid_groups, title_groups, study_groups = (defaultdict(list) for _ in range(4))
    for ref in refs:
        if not isinstance(ref, dict):
            raise ValueError('Every reference must be an object')
        strings(ref, ['record_id','title','source_type','identity_status','read_scope','publication_status','doi','pmid','url','study_id','status_checked_at'])
        rid = ref.get('record_id')
        if not nonblank(rid) or rid in by_id:
            raise ValueError('record_id must be nonempty and unique')
        if any(not nonblank(ref.get(k)) for k in ('title','source_type','identity_status','read_scope','publication_status')):
            raise ValueError(f'Reference {rid} missing required fields')
        if ref['source_type'] not in TYPES or ref['identity_status'] not in {'verified','unverified','conflict'} or ref['read_scope'] not in READ or ref['publication_status'] not in STATUS:
            raise ValueError(f'Reference {rid} has an unknown enum')
        by_id[rid] = ref
        identity_sources = source_list(ref, 'identity_sources')
        status_sources = source_list(ref, 'status_sources')
        if ref['identity_status'] != 'verified' or not identity_sources:
            issue(warnings, 'IDENTITY_PENDING', rid, 'Identity not verified with recorded source URLs')
        if ref['publication_status'] == 'unchecked' or not checked_date(ref.get('status_checked_at')) or not status_sources:
            issue(warnings, 'STATUS_PENDING', rid, 'Publication/update status, check date or recorded channels incomplete')
        if ref.get('doi'):
            d = normalize_doi(ref['doi'])
            doi_groups[d].append(rid)
            if not re.fullmatch(r'10\.[0-9]{4,9}/\S+', d):
                issue(warnings, 'DOI_SHAPE', rid, 'Check original DOI; shape warning is not a registration verdict')
        if ref.get('pmid'):
            raw = ref['pmid'].strip()
            if raw.isascii() and raw.isdigit() and int(raw)>0:
                pmid_groups[str(int(raw))].append(rid)
            else:
                issue(warnings, 'PMID_SHAPE', rid, 'Check PMID; no identity guessed')
        title = re.sub(r'\W+', '', ref['title'].casefold())
        if title:
            title_groups[title].append(rid)
        if nonblank(ref.get('study_id')):
            study_groups[ref['study_id']].append(rid)
        if ref['source_type'] == 'guideline':
            g = ref.get('guideline')
            required = ['organisation','version','official_url','checked_at','recommendation_locator']
            if g is not None and not isinstance(g, dict):
                raise ValueError('guideline must be an object')
            if g is None or any(not nonblank(g.get(k)) for k in required) or not checked_date(g.get('checked_at')):
                issue(warnings, 'GUIDELINE_METADATA', rid, 'Guideline version, official source, date or locator incomplete')
            if g is not None:
                if not isinstance(g.get('currency_status'), str) or g.get('currency_status') not in {'current','historical','superseded','unclear'}:
                    raise ValueError('Unknown guideline currency_status')
                if g.get('currency_status') in {'superseded','unclear'}:
                    issue(warnings, 'GUIDELINE_CURRENCY', rid, 'Check applicability and intended historical/current use')
    for kind, groups in [('DOI',doi_groups),('PMID',pmid_groups)]:
        for _, ids in groups.items():
            if len(ids)>1:
                issue(errors, 'DUPLICATE_'+kind, ','.join(ids), 'Same normalized identifier; reconcile rather than silently merge')
    for kind, groups in [('TITLE_CANDIDATE',title_groups),('SAME_STUDY_REPORTS',study_groups)]:
        for _, ids in groups.items():
            if len(ids)>1:
                issue(warnings, kind, ','.join(ids), 'Review record/report/study relationships; not automatic duplicate removal')
    seen_claims, used = set(), set()
    links_n = 0
    for claim in claims:
        if not isinstance(claim, dict):
            raise ValueError('Every claim must be an object')
        strings(claim, ['claim_id','text','location'])
        cid = claim.get('claim_id')
        if not nonblank(cid) or cid in seen_claims or not nonblank(claim.get('text')) or not nonblank(claim.get('location')):
            raise ValueError('Claims require unique claim_id and nonempty text/location')
        seen_claims.add(cid)
        if not isinstance(claim.get('requires_full_text'), bool) or not isinstance(claim.get('links'), list):
            raise ValueError('requires_full_text must be bool and links must be list')
        if not claim['links']:
            issue(errors, 'CLAIM_WITHOUT_SOURCE', cid, 'No link; remove/narrow/hold the claim or provide evidence')
        seen_links = set()
        for link in claim['links']:
            links_n += 1
            if not isinstance(link, dict):
                raise ValueError('Every link must be an object')
            strings(link, ['record_id','support','role','action','source_locator','evidence_note','limits','reading_scope_note','recommendation_strength','evidence_certainty'])
            rid = link.get('record_id')
            if not nonblank(rid) or rid in seen_links:
                raise ValueError('Claim links need unique nonempty record_id')
            seen_links.add(rid)
            if link.get('support') not in SUPPORT or link.get('role') not in ROLE or link.get('action') not in ACTION:
                raise ValueError('Unknown link support/role/action enum')
            loc = cid + '->' + rid
            if rid not in by_id:
                issue(errors, 'DANGLING_REFERENCE', loc, 'No matching reference record')
                continue
            used.add(rid)
            ref = by_id[rid]
            sup, action, role = link['support'], link['action'], link['role']
            use = action in {'adopt','narrow','background_only','report_counterevidence'}
            if use and ref['identity_status'] != 'verified':
                issue(errors, 'USE_UNVERIFIED_IDENTITY', loc, 'Do not adopt a conflicted/unverified identity')
            if sup == 'unassessed':
                issue(warnings, 'SUPPORT_UNASSESSED', loc, 'Source support still needs actual reading')
            if action in {'adopt','narrow'} and sup not in {'direct','qualified'}:
                issue(errors, 'SUPPORT_ACTION_MISMATCH', loc, 'Adoption/narrowing requires declared direct/qualified support')
            if action == 'background_only' and sup not in {'background','direct','qualified'}:
                issue(errors, 'SUPPORT_ACTION_MISMATCH', loc, 'Background use contradicts declared support')
            if action == 'report_counterevidence' and sup != 'contradicts' and role != 'historical_retraction':
                issue(errors, 'SUPPORT_ACTION_MISMATCH', loc, 'Counterevidence not declared')
            if use and (not nonblank(link.get('source_locator')) or not nonblank(link.get('evidence_note'))):
                issue(errors, 'EVIDENCE_LOCATION_MISSING', loc, 'Record actual section/page/table/recommendation and evidence note')
            if sup == 'qualified' and not nonblank(link.get('limits')):
                issue(errors, 'QUALIFICATION_MISSING', loc, 'State limitation and narrowed wording')
            if use and ref['read_scope'] in {'none','metadata'}:
                issue(errors, 'CONTENT_NOT_READ', loc, 'Identity metadata cannot support a substantive claim')
            if use and claim['requires_full_text'] and ref['read_scope'] not in {'full_text_partial','full_text_and_relevant_supplement'}:
                issue(errors, 'FULL_TEXT_REQUIRED', loc, 'Necessary full-text material not read')
            if use and ref['read_scope'] == 'full_text_partial' and not nonblank(link.get('reading_scope_note')):
                issue(warnings, 'PARTIAL_READING_SCOPE', loc, 'Explain whether the read sections cover all necessary evidence and limitations')
            if use and ref['read_scope'] == 'abstract':
                issue(warnings, 'ABSTRACT_ONLY', loc, 'Only narrow abstract-explicit claims; preserve this reading limit')
            if use and ref['publication_status'] == 'retracted' and role != 'historical_retraction':
                issue(errors, 'RETRACTED_AS_EVIDENCE', loc, 'Retracted results cannot be adopted as valid scientific evidence')
            if use and ref['publication_status'] in {'corrected','expression_of_concern'}:
                issue(warnings, 'UPDATE_IMPACT_REVIEW', loc, 'Read notice and document which results/claims are affected')
            if use and ref['publication_status'] == 'unchecked':
                issue(warnings, 'USE_STATUS_PENDING', loc, 'Current source status not checked')
            if use and role == 'recommendation':
                if ref['source_type'] != 'guideline':
                    issue(warnings, 'RECOMMENDATION_SOURCE_TYPE', loc, 'Clarify whether reporting a guideline or an author suggestion')
                if not nonblank(link.get('recommendation_strength')) or not nonblank(link.get('evidence_certainty')):
                    issue(warnings, 'RECOMMENDATION_GRADES_PENDING', loc, 'Copy original strength/certainty labels or explicitly mark not graded')
    for rid in by_id.keys()-used:
        issue(warnings, 'UNLINKED_REFERENCE', rid, 'Candidate or uncited record; do not force a citation')
    if not claims:
        issue(warnings, 'NO_MANUSCRIPT_CLAIMS', 'claims', 'No claims audited; metadata ledger alone is not citation matching')
    return {'schema_version':1,'scientific_support_verified_by_script':False,
        'scope':'offline_structural_and_declared_scope_only',
        'inventory':{'references':len(refs),'claims':len(claims),'links':links_n},
        'errors':errors,'warnings':warnings,
        'limitations':['No network lookup, no manuscript parsing, no full-text reading, no semantic or current-guideline verification.']}


def no_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('Duplicate JSON object key: ' + key)
        obj[key] = value
    return obj


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True)
    p.add_argument('--out',required=True)
    a=p.parse_args()
    try:
        out=Path(a.out)
        if out.exists() or out.resolve() in {Path(a.input).resolve(),Path(__file__).resolve()}:
            raise ValueError('Output must be new and cannot overwrite input or script')
        raw=Path(a.input).read_bytes()
        obj=json.loads(raw,object_pairs_hook=no_duplicate_keys)
        report=audit(obj)
        report['provenance']={'utc':datetime.now(timezone.utc).isoformat(),'input_sha256':hashlib.sha256(raw).hexdigest(),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'argv':sys.argv,'python':platform.python_version()}
        out.parent.mkdir(parents=True,exist_ok=True)
        with out.open('x',encoding='utf-8') as f:
            json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
        print(f'Audit written: {out}; {len(report["errors"])} errors, {len(report["warnings"])} warnings; semantic support not verified')
    except (ValueError,OSError) as e:
        p.exit(2,f'Reference audit refused: {e}\n')


if __name__=='__main__':
    main()
