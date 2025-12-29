import json
from pathlib import Path
import re

# This script reads data/latest_submissions.json and writes data/submission_urls.json
# It extracts entries that are URL analyses or whose submit_name looks like a URL.

URL_RE = re.compile(r"^https?://", re.IGNORECASE)

def is_url_entry(item):
    # Some entries include a boolean 'url_analysis': true
    if item.get('url_analysis'):
        return True
    # Or the submit_name may be a url
    name = item.get('submit_name', '') or ''
    if URL_RE.match(name):
        return True
    # Also check presence of domains list
    if item.get('domains'):
        return True
    return False


def main():
    base = Path(__file__).parent
    data_dir = base / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    in_file = data_dir / 'latest_submissions.json'
    out_file = data_dir / 'submission_urls.json'

    if not in_file.exists():
        print(f"Input file not found: {in_file}")
        return

    with in_file.open('r', encoding='utf-8') as f:
        doc = json.load(f)

    entries = doc.get('data') if isinstance(doc, dict) else doc
    if entries is None:
        print('No entries found in input JSON')
        entries = []

    urls = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        if is_url_entry(e):
            urls.append({
                'job_id': e.get('job_id'),
                'url': e.get('submit_name') if URL_RE.match(str(e.get('submit_name', ''))) else None,
                'domains': e.get('domains', []),
                'hosts': e.get('hosts', []),
                'environment_id': e.get('environment_id'),
                'threat_score': e.get('threat_score'),
                'threat_level_human': e.get('threat_level_human')
            })

    with out_file.open('w', encoding='utf-8') as f:
        json.dump({'submission_urls': urls}, f, indent=2, ensure_ascii=False)

    print(f'Wrote {len(urls)} URL entries to {out_file}')

if __name__ == '__main__':
    main()
