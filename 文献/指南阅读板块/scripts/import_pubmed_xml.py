#!/usr/bin/env python3
"""Import local PubmedArticle XML into an explicitly unverified candidate ledger."""
import argparse
import hashlib
import json
import platform
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


def text(node):
    return '' if node is None else ''.join(node.itertext()).strip()


def field(node, path):
    return text(node.find(path))


def date_fields(node):
    return {} if node is None else {c.tag: text(c) for c in node}


def parse(data):
    if re.search(br'<!ENTITY\b', data, re.I):
        raise ValueError('Custom XML entities are not accepted')
    root = ET.fromstring(data)
    if root.tag == 'PubmedArticle':
        articles = [root]
    elif root.tag == 'PubmedArticleSet':
        if any(c.tag != 'PubmedArticle' for c in root):
            raise ValueError('Unsupported record type; split books/deletions/other objects rather than silently dropping them')
        articles = list(root)
    else:
        raise ValueError('Require PubmedArticleSet or PubmedArticle (journal records only)')
    if not articles:
        raise ValueError('No journal records')
    records = []
    seen = set()
    for node in articles:
        med = node.find('MedlineCitation')
        if med is None:
            raise ValueError('Missing MedlineCitation')
        art = med.find('Article')
        pmid = field(med, 'PMID')
        if art is None or not re.fullmatch(r'[1-9][0-9]*', pmid):
            raise ValueError('Each record requires Article and a positive PMID')
        if pmid in seen:
            raise ValueError('Duplicate PMID; verify differing versions before import')
        seen.add(pmid)
        authors = []
        for a in art.findall('AuthorList/Author'):
            if a.find('CollectiveName') is not None:
                authors.append({'collective_name': field(a, 'CollectiveName')})
            else:
                authors.append({'last_name': field(a, 'LastName'), 'fore_name': field(a, 'ForeName'),
                    'initials': field(a, 'Initials'), 'suffix': field(a, 'Suffix')})
        ids = [{'type': e.get('IdType', ''), 'value': text(e)} for e in node.findall('PubmedData/ArticleIdList/ArticleId')]
        # Include DOI from ELocationID while retaining the original source tag.
        for e in art.findall('ELocationID'):
            ids.append({'type': e.get('EIdType', ''), 'value': text(e), 'source_tag': 'ELocationID', 'valid_yn': e.get('ValidYN', '')})
        doi_values = list(dict.fromkeys(i['value'] for i in ids if i['type'].lower() == 'doi' and i['value']))
        doi_candidates = list(dict.fromkeys(i['value'] for i in ids if i['type'].lower() == 'doi' and i['value'] and i.get('valid_yn') != 'N'))
        abstracts = [{'label': e.get('Label', ''), 'nlm_category': e.get('NlmCategory', ''), 'text': text(e)} for e in art.findall('Abstract/AbstractText')]
        publication_types = [text(e) for e in art.findall('PublicationTypeList/PublicationType')]
        relations = []
        for rel in med.findall('CommentsCorrectionsList/CommentsCorrections'):
            relations.append({'ref_type': rel.get('RefType', ''), 'pmid': field(rel, 'PMID'),
                'ref_source': field(rel, 'RefSource'), 'note': field(rel, 'Note')})
        pub_date = date_fields(art.find('Journal/JournalIssue/PubDate'))
        article_dates = [{'date_type': d.get('DateType', ''), **date_fields(d)} for d in art.findall('ArticleDate')]
        warnings = ['Imported metadata/abstract only; identity, status, source version and claim support still require verification.']
        if len({v.casefold() for v in doi_candidates}) > 1:
            warnings.append('Multiple distinct DOI values: resolve source identity before choosing a DOI.')
        if any(i.get('valid_yn') == 'N' and i['type'].lower() == 'doi' for i in ids):
            warnings.append('DOI marked invalid by source retained in raw identifiers but not chosen from that tag.')
        if art.find('AuthorList') is not None and art.find('AuthorList').get('CompleteYN') == 'N':
            warnings.append('Author list marked incomplete; obtain full byline before final citation.')
        if relations or any('retract' in t.casefold() or 'concern' in t.casefold() for t in publication_types):
            warnings.append('Update/retraction relation or publication type present: review direction and linked notice; status not auto-classified.')
        title = field(art, 'ArticleTitle')
        if not title:
            warnings.append('Missing ArticleTitle; do not fabricate it from other fields.')
        records.append({
            'record_id': 'PMID-' + pmid, 'title': title, 'source_type': 'journal_article',
            'authors': authors, 'author_list_complete': None if art.find('AuthorList') is None else art.find('AuthorList').get('CompleteYN'),
            'journal': field(art, 'Journal/Title'), 'journal_iso_abbreviation': field(art, 'Journal/ISOAbbreviation'),
            'volume': field(art, 'Journal/JournalIssue/Volume'), 'issue': field(art, 'Journal/JournalIssue/Issue'),
            'pagination': field(art, 'Pagination/MedlinePgn'), 'publication_date_raw': pub_date,
            'article_dates_raw': article_dates, 'year': pub_date.get('Year') or None,
            'doi': doi_candidates[0] if len({v.casefold() for v in doi_candidates}) == 1 else '',
            'doi_values_raw': doi_values, 'pmid': pmid, 'identifiers_raw': ids,
            'url': 'https://pubmed.ncbi.nlm.nih.gov/' + pmid + '/',
            'abstract_sections': abstracts, 'publication_types_raw': publication_types,
            'comments_corrections_raw': relations, 'publication_stage_raw': field(node, 'PubmedData/PublicationStatus'),
            'identity_status': 'unverified', 'identity_sources': [],
            'read_scope': 'metadata',
            'available_content_scope': 'abstract' if any(a['text'] for a in abstracts) else 'metadata',
            'publication_status': 'unchecked', 'status_checked_at': '', 'status_sources': [],
            'import_warnings': warnings,
        })
    return records


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', required=True, help='Local PubmedArticleSet/PubmedArticle XML, not an ESearch JSON')
    p.add_argument('--out', required=True)
    a = p.parse_args()
    try:
        out = Path(a.out)
        if out.exists() or out.resolve() in {Path(a.input).resolve(), Path(__file__).resolve()}:
            raise ValueError('Output must be new and cannot overwrite input or script')
        raw = Path(a.input).read_bytes()
        records = parse(raw)
        result = {'schema_version': 1, 'references': records, 'claims': [],
            'provenance': {'utc': datetime.now(timezone.utc).isoformat(), 'input_sha256': hashlib.sha256(raw).hexdigest(),
                'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'argv': sys.argv, 'python': platform.python_version()},
            'scope': 'candidate_metadata_only_not_full_text_or_citation_validation'}
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open('x', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2, allow_nan=False)
            f.write('\n')
        print(f'Imported {len(records)} candidate records: {out}; verification is pending')
    except (ValueError, OSError, ET.ParseError) as e:
        p.exit(2, f'XML import refused: {e}\n')


if __name__ == '__main__':
    main()
