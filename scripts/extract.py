"""Extract only onsite 17.1–20.2 from native SF exports; no crawling or HTTP."""
import collections
import csv
import hashlib
import math
from pathlib import Path

ITEMS = {
    '17.1': ('Does each URL have a title? (excluding target pages)', '17.1 Page titles - Missing', ['Address', 'New Title', 'Remarks']),
    '17.2': ('Is the site free of any page title duplication?', '17.2 Page titles - Duplicate', ['Address', 'Title 1', 'New Title', 'Remarks']),
    '17.3': ('Are page titles using the 580 pixel maximum width effectively?', '17.3 Page titles - Too Long', ['Address', 'Title 1', 'Title 1 Pixel Width', 'Revised Title']),
    '17.4': ('Are there multiple page titles', '17.4 Page titles - Multiple', ['Address', 'Title 1', 'Title 2', 'Remarks']),
    '18.1': ('Does each URL have a description? (excluding target pages)', '18.1 Descriptions - Missing', ['Address', 'Instruction']),
    '18.2': ('Is the site free of any meta description duplication?', '18.2 Descriptions - Duplicate', ['Address', 'Meta Description 1']),
    '18.3': ('Are meta descriptions using the 155 character limit effectively?', '18.3 Descriptions - Too Long', ['Address', 'Meta Description 1', 'Character Count']),
    '19.1': ('Do all pages contain a single, keyword-optimised H1?', '19.1 H1 - Missing', ['Address', 'Instruction']),
    '19.2': ('Are there H1 duplicates?', '19.2 H1 - Duplicate', ['Address', 'H1-1', 'Remarks']),
    '19.3': ('Are there multiple H1s tags in a single page?', '19.3 H1 - Multiple', ['Address', 'H1-1', 'H1-2']),
    '20.1': ('Do images contain alt text', '20.1 Image - Alt Text Missing', ['Source', 'Destination', 'Screenshots (If have)']),
    '20.2': ('Oversized images', '20.2 Image - Oversize', ['Source', 'Destination', 'Size (Bytes)']),
}

REPORTS = {
    'title_all': (('page_titles', 'all'), ['Address']),
    'title_missing': (('page_titles', 'missing'), ['Address']),
    'title_duplicate': (('page_titles', 'duplicate'), ['Address', 'Title 1']),
    'title_multiple': (('page_titles', 'multiple'), ['Address', 'Title 1', 'Title 2']),
    'description_all': (('meta_description', 'all'), ['Address']),
    'description_missing': (('meta_description', 'missing'), ['Address']),
    'description_duplicate': (('meta_description', 'duplicate'), ['Address', 'Meta Description 1']),
    'h1_missing': (('h1', 'missing'), ['Address']),
    'h1_duplicate': (('h1', 'duplicate'), ['Address', 'H1-1', 'H1-2']),
    'h1_multiple': (('h1', 'multiple'), ['Address', 'H1-1', 'H1-2']),
    'images_all': (('images_all',), ['Address']),
    'alt': (('missing_alt_attribute',), ['Source', 'Destination']),
    'inlinks': (('all_image_inlinks',), ['Source', 'Destination']),
}


def read_report(directory, keywords, required):
    paths = sorted(p for p in directory.glob('*.csv') if all(k in p.name.lower() for k in keywords))
    info = {'path': None, 'state': 'missing', 'row_count': 0, 'headers': [], 'gaps': []}
    if len(paths) != 1:
        info['state'] = 'ambiguous' if paths else 'missing'
        info['gaps'] = [f"Report {'/'.join(keywords)}: {info['state']} ({len(paths)} matching files)."]
        return [], info
    path = paths[0]
    info['path'] = str(path.resolve())
    try:
        info['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        with path.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f, strict=True)
            headers = reader.fieldnames or []
            if not headers or len(headers) != len(set(headers)):
                raise ValueError('missing or duplicate column headers')
            missing = set(required) - set(headers)
            if missing:
                raise ValueError(f'missing columns: {sorted(missing)}')
            data = list(reader)
            if any(None in row or any(v is None for v in row.values()) for row in data):
                raise ValueError('CSV row length differs from its header')
        info.update(state='available', headers=headers, row_count=len(data))
        return data, info
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        info.update(state='invalid', gaps=[f'{path.name}: {exc}'])
        return [], info


def number(value):
    try:
        n = float(str(value).replace(',', ''))
        return n if math.isfinite(n) and n >= 0 else None
    except (TypeError, ValueError):
        return None


def grouped(rows, field):
    # Keep SF's Duplicate filter as the source; do not regroup the All export.
    counts = collections.Counter(r[field].strip() for r in rows)
    return sorted(rows, key=lambda r: (-counts[r[field].strip()], r[field].strip(), r['Address']))


def audit(exports_dir, targets=None, title_px=580, description_chars=155, image_kib=200, language='zh'):
    directory = Path(exports_dir)
    if not directory.is_dir():
        raise ValueError(f'Export directory does not exist: {directory}')
    if language not in ('zh', 'en'):
        raise ValueError('language must be zh or en')
    for value in (title_px, description_chars, image_kib):
        if number(value) is None or float(value) <= 0:
            raise ValueError('Thresholds must be positive finite numbers')
    targets = set(targets or [])
    exports, records = {}, {}
    for name, (words, headers) in REPORTS.items():
        exports[name], records[name] = read_report(directory, words, headers)
    if not exports['title_all']:
        raise ValueError('Page Titles:All must be readable and contain data rows. ' + ' '.join(records['title_all']['gaps']))
    checks = []

    def add(item, rows, sources, extra_gaps=None, note=''):
        gaps = [gap for source in sources for gap in records[source]['gaps']] + (extra_gaps or [])
        label, sheet, headers = ITEMS[item]
        result = 'X' if rows else ('Human Check' if gaps else '√')
        finding = (f'发现 {len(rows)} 条问题记录。' if rows else ('证据不足，暂不能判断。' if gaps else '所提供样本中未发现该问题。')) if language == 'zh' else (
            f'{len(rows)} issue row(s) found.' if rows else ('Insufficient evidence to judge.' if gaps else 'No issue found in the supplied sample.'))
        if gaps:
            finding += ' ' + ('部分证据缺失，已确认问题仍保留。' if language == 'zh' and rows else 'Evidence incomplete.' if rows else '')
        if note:
            finding += ' ' + note
        actions_zh = {'17.1': '补充缺失的页面标题。', '17.2': '为重复页面编写不同的标题。', '17.3': f'将标题调整至 {title_px:g}px 以内。',
                      '17.4': '每页保留一个有效 title 元素。', '18.1': '补充缺失的描述。', '18.2': '为重复页面编写不同的描述。',
                      '18.3': f'将描述调整至 {description_chars:g} 字符以内。', '19.1': '补充页面的 H1。', '19.2': '按页面主题调整重复 H1。',
                      '19.3': '检查并调整同页多个 H1。', '20.1': '先排除装饰图片，再为内容图片补充 Alt。', '20.2': '压缩或替换超出大小限制的图片。'}
        action = (actions_zh[item] if language == 'zh' else 'Review and correct the listed issue(s).') if rows else '—'
        if gaps:
            action += (' 补充缺少或无效的 SF 导出字段。' if language == 'zh' else ' Supply the missing/invalid SF exports or fields.')
        check = dict(id=item, item_name=label, sheet=sheet, headers=headers, result=result,
                     finding=finding.strip(), action=action, rows=rows, row_count=len(rows), gaps=gaps, sources=sources)
        if item.startswith('20.'):
            check['unique_assets'] = len({r[1] for r in rows})
            check['affected_pages'] = len({r[0] for r in rows})
            if rows:
                check['finding'] += (f" 涉及 {check['unique_assets']} 张图片、{check['affected_pages']} 个页面。" if language == 'zh' else
                                     f" {check['unique_assets']} unique image(s) on {check['affected_pages']} page(s).")
        checks.append(check)

    def clean(source, fields):
        valid, gaps = [], []
        for row in exports[source]:
            if any(not row.get(field, '').strip() for field in fields):
                gaps.append(f'{source}: issue row has blank required values ({", ".join(fields)}).')
            else:
                valid.append(row)
        return valid, gaps

    for item, source, fields in (
        ('17.1', 'title_missing', ['Address']), ('17.2', 'title_duplicate', ['Address', 'Title 1']),
        ('17.4', 'title_multiple', ['Address', 'Title 1', 'Title 2']),
        ('18.1', 'description_missing', ['Address']), ('18.2', 'description_duplicate', ['Address', 'Meta Description 1']),
        ('19.1', 'h1_missing', ['Address']), ('19.2', 'h1_duplicate', ['Address', 'H1-1']),
        ('19.3', 'h1_multiple', ['Address', 'H1-1', 'H1-2'])):
        rows, gaps = clean(source, fields)
        note = ''
        if item in ('17.1', '18.1'):
            rows = [r for r in rows if r['Address'].strip() not in targets]
            if not targets:
                note = '未提供明确 target pages 清单，未应用排除。' if language == 'zh' else 'No explicit target-page list; no exclusions applied.'
        if item == '19.2':
            counts = collections.Counter(r['H1-1'].strip().lower() for r in rows)
            rows = [r for r in rows if r['H1-1'].strip() != r.get('H1-2', '').strip() or counts[r['H1-1'].strip().lower()] > 1]
        if item in ('17.2', '18.2', '19.2'):
            rows = grouped(rows, fields[1])
        if item == '19.1':
            note = '本项检查 H1 缺失；关键词优化由人工判断，多个 H1 见 19.3。' if language == 'zh' else 'Presence only; keyword relevance requires human review. Multiple H1s: 19.3.'
        add(item, [[r[f] for f in fields] for r in rows], [source], gaps, note)

    for item, source, text_field, metric_field, threshold in (
        ('17.3', 'title_all', 'Title 1', 'Title 1 Pixel Width', title_px),
        ('18.3', 'description_all', 'Meta Description 1', None, description_chars)):
        needed = {'Indexability', text_field} | ({metric_field} if metric_field else set())
        missing = needed - set(records[source]['headers'])
        rows, gaps = [], []
        if not exports[source]:
            gaps.append(f'{source}: All report has no observations; an empty issue filter is different.')
        if missing:
            gaps.append(f'{source}: missing columns {sorted(missing)}.')
        else:
            for row in exports[source]:
                if not row['Address'].strip() or row.get('Indexability') not in ('Indexable', 'Non-Indexable'):
                    gaps.append(f'{source}: blank Address or unknown Indexability.')
                    continue
                if row['Indexability'] != 'Indexable':
                    continue
                width = number(row[metric_field]) if metric_field else len(row[text_field])
                if width is None:
                    gaps.append(f'{source}: invalid numeric width for {row["Address"]}.')
                elif width > threshold:
                    rows.append([row['Address'], row[text_field], int(width)])
        rows.sort(key=lambda r: -r[2])
        add(item, rows, [source], gaps)

    captured = any(exports[s] for s in ('images_all', 'alt', 'inlinks'))
    alt_rows, alt_gaps = clean('alt', ['Source', 'Destination'])
    if not captured:
        alt_gaps.append('No images captured across the image exports; enable image/render capture as appropriate.')
    add('20.1', [[r['Source'], r['Destination']] for r in alt_rows], ['alt'], alt_gaps,
        '含空 Alt 的图片，装饰图片需人工排除。' if language == 'zh' else 'Includes empty alt; decorative images require review.')
    oversized, size_gaps = [], []
    size_field = next((h for h in ('Size (Bytes)', 'Size') if h in records['inlinks']['headers']), None)
    if size_field is None:
        size_gaps.append('All Image Inlinks is missing Size (Bytes)/Size.')
    usable, identity_gaps = clean('inlinks', ['Source', 'Destination'])
    size_gaps.extend(identity_gaps)
    sized_assets = set()
    for row in usable:
        size = number(row.get(size_field))
        if size is None or size == 0:
            size_gaps.append(f'Image size unknown: {row["Destination"]}.')
        else:
            sized_assets.add(row['Destination'])
            if size > image_kib * 1024:
                oversized.append([row['Source'], row['Destination'], int(size)])
    captured_assets = {r['Address'] for r in exports['images_all'] if r.get('Address', '').strip()}
    captured_assets.update(r['Destination'] for r in alt_rows)
    for asset in sorted(captured_assets - sized_assets):
        size_gaps.append(f'Captured image has no known inlink size: {asset}.')
    if not captured or not usable:
        size_gaps.append('No usable image size observations; cannot establish a clean image audit.')
    oversized.sort(key=lambda r: -r[2])
    add('20.2', oversized, ['inlinks'], size_gaps)
    checks.sort(key=lambda c: tuple(map(int, c['id'].split('.'))))
    return {'schema_version': 1, 'language': language, 'checks': checks,
            'manifest': {'exports': records, 'scope': list(ITEMS), 'target_urls': sorted(targets),
                         'thresholds': {'title_px': title_px, 'description_chars': description_chars,
                                        'image_bytes': image_kib * 1024},
                         'page_count': len(exports['title_all']),
                         'page_addresses': [r['Address'] for name, data in exports.items()
                                            if name not in ('images_all', 'alt', 'inlinks') for r in data if r.get('Address')]
                                           + [r['Source'] for name in ('alt', 'inlinks') for r in exports[name] if r.get('Source')]}}
