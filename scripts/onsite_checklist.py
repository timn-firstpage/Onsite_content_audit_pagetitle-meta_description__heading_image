#!/usr/bin/env python3
"""Audit onsite content items 17–20 from an existing SF export directory."""
import argparse
import csv
import datetime
import json
from pathlib import Path
import shutil
import sys
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from extract import audit
from report import build_report


def resolve(value, base):
    path = Path(value)
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def target_urls(path):
    if path.suffix.lower() == '.csv':
        with path.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f, strict=True)
            field = next((key for key in ('Address', 'URL') if key in (reader.fieldnames or [])), None)
            if field is None:
                raise ValueError('Target CSV must have Address or URL header')
            values = []
            for row in reader:
                if None in row or row.get(field) is None:
                    raise ValueError('Malformed target CSV row')
                if row[field].strip():
                    values.append(row[field].strip())
    else:
        values = [line.strip() for line in path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
    return values


def run(args):
    base = args.config.resolve().parent if args.config else Path.cwd()
    config = json.loads(args.config.read_text(encoding='utf-8-sig')) if args.config else {}
    if config.get('checks', {}).get('content') is False:
        print('Content audit disabled by checks.content=false')
        return
    source = dict(config.get('source', {}))
    output = config.get('output', {})
    content = config.get('content', {})
    site = config.get('site', {})
    exports_value = args.exports_dir or source.get('export_directory')
    if not exports_value:
        raise ValueError('Supply the native CSV exports from the existing session/saved crawl. '
                         'Open the saved crawl once with supported SF tools, or use File > Open and export the required reports; do not recrawl.')
    exports = resolve(exports_value, base)
    prior_directory = source.get('export_directory')
    if args.exports_dir and (not prior_directory or resolve(prior_directory, base) != exports):
        # An explicit new export source is not evidence for the old crawl's identity.
        source = {'mode': 'exports', 'export_directory': str(exports), 'crawl_id': None,
                  'crawl_file': None, 'crawl_timestamp': None, 'allow_new_crawl': False,
                  'override_note': 'CLI export override; prior crawl identity is unverified and was not inherited.'}
    else:
        source['export_directory'] = str(exports)
    site_url = args.site_url or site.get('start_url')
    parsed = urlsplit(site_url or '')
    if parsed.scheme not in ('http', 'https') or not parsed.hostname:
        raise ValueError('Supply site.start_url or --site-url as an absolute HTTP(S) URL')
    host = parsed.hostname.lower()
    site_name = args.site_name or site.get('name') or host.removeprefix('www.')
    allowed = site.get('allowed_hosts') or [host, host[4:] if host.startswith('www.') else 'www.' + host]
    allowed = {str(h).strip().lower() for h in allowed}
    if host not in allowed:
        raise ValueError('site.allowed_hosts must include site.start_url host')
    date_value = args.date or output.get('audit_date')
    if date_value:
        date = datetime.date.fromisoformat(date_value)
        if date_value != date.isoformat():
            raise ValueError('audit_date/--date must be YYYY-MM-DD')
    else:
        zone = output.get('timezone')
        if not zone:
            raise ValueError('Supply output.timezone or an explicit audit_date; do not use the host timezone silently')
        try:
            date = datetime.datetime.now(ZoneInfo(zone)).date()
        except ZoneInfoNotFoundError as exc:
            raise ValueError('Timezone database unavailable or unknown timezone; install requirements.txt or provide audit_date') from exc
    targets = list(content.get('target_urls') or [])
    if not isinstance(content.get('target_urls', []), (list, type(None))):
        raise ValueError('content.target_urls must be a list of exact URLs')
    targets_path = args.target_urls or content.get('target_urls_file')
    if targets_path:
        targets.extend(target_urls(resolve(targets_path, base)))
    if any(not isinstance(u, str) or urlsplit(u).scheme not in ('http', 'https') or not urlsplit(u).hostname for u in targets):
        raise ValueError('Target list must contain absolute HTTP(S) URLs')
    if content.get('description_chars', 155) != 155 or content.get('title_px', 580) != 580 or content.get('image_kib', 200) != 200:
        raise ValueError('This version uses fixed thresholds: title 580px, description 155 characters, image 200KiB')
    language = output.get('language', 'zh')
    data = audit(exports, targets=[u.strip() for u in targets], language=language)
    addresses = data['manifest'].pop('page_addresses')
    observed = {urlsplit(address).hostname.lower() for address in addresses if urlsplit(address).hostname}
    if not observed or observed - allowed:
        raise ValueError(f'Export host mismatch: observed={sorted(observed)}, allowed={sorted(allowed)}')
    data.update(site_name=site_name, site_url=site_url, audit_date=date.isoformat())
    data['manifest'].update(observed_hosts=sorted(observed), source=source,
                            crawl_timestamp=source.get('crawl_timestamp'),
                            note='Crawl timestamp is supplied evidence, never inferred from file mtime.')
    run_value = args.run_dir
    if run_value is None:
        root = resolve(output.get('run_root') or 'runs', base)
        run_dir = root / (date.isoformat() + '-' + datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S-%f'))
    else:
        run_dir = resolve(run_value, base)
    destination = run_dir / 'content'
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f'Content output exists: {destination}; choose a new run directory')
    destination.mkdir(parents=True, exist_ok=True)
    if output.get('archive_raw', True):
        raw = destination / 'raw'
        raw.mkdir()
        for record in data['manifest']['exports'].values():
            if record['path']:
                original = Path(record['path'])
                target = raw / original.name
                shutil.copyfile(original, target)
                record['archived_path'] = str(target)
    manifest = data.pop('manifest')
    # This flow has no MCP/live calls; it does not reset shared usage.json budgets.
    manifest['local_operations'] = {'mcp_calls': 0, 'live_requests': 0, 'paid_api_calls': 0}
    with (destination / 'findings.json').open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with (destination / 'manifest.json').open('x', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    report = build_report(data, destination)
    with (destination / 'run-status.json').open('x', encoding='utf-8') as f:
        json.dump({'state': 'complete', 'report': str(report), 'items': 12}, f, indent=2)
    print('ITEM  ROWS  RESULT')
    for c in data['checks']:
        print(f"{c['id']:<5} {c['row_count']:>5}  {c['result']}")
    print(f'WROTE: {report}')


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, help='Shared onsite JSON config')
    parser.add_argument('--exports-dir', type=Path, help='Native CSV exports; overrides config source')
    parser.add_argument('--site-url')
    parser.add_argument('--site-name')
    parser.add_argument('--date', help='Explicit YYYY-MM-DD in the user timezone')
    parser.add_argument('--target-urls', type=Path, help='Explicit target list: Address/URL CSV or one URL per line')
    parser.add_argument('--run-dir', type=Path, help='Shared run directory; output is in content/')
    args = parser.parse_args()
    try:
        run(args)
    except (OSError, ValueError, KeyError, TypeError, csv.Error) as exc:
        print(f'Content audit failed: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
