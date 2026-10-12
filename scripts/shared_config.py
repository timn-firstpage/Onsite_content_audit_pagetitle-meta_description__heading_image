"""Read shared onsite inputs without modifying global configuration or budgets."""
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlsplit


def read_object(path):
    raw = path.read_bytes()
    data = json.loads(raw.decode('utf-8-sig'))
    if not isinstance(data, dict):
        raise ValueError(f'Expected JSON object: {path}')
    return data, hashlib.sha256(raw).hexdigest()


def load_config(path=None):
    selection = 'explicit' if path is not None else 'environment'
    chosen = path if path is not None else os.environ.get('ONSITE_AUDIT_CONFIG')
    if chosen:
        chosen = Path(chosen).expanduser().resolve()
        config, digest = read_object(chosen)
        base = chosen.parent
        metadata = {'path': str(chosen), 'sha256': digest, 'selection': selection}
    else:
        config, base = {}, Path.cwd()
        metadata = {'path': None, 'sha256': None, 'selection': 'cli_only'}
    for key in ('site', 'source', 'mcp', 'budget', 'cache', 'output', 'checks', 'content'):
        if key in config and not isinstance(config[key], dict):
            raise ValueError(f'Config {key} must be an object')
    config.setdefault('checks', {}).setdefault('content', True)
    content = config.setdefault('content', {})
    for key, value in (('target_urls', []), ('target_urls_file', None),
                       ('title_px', 580), ('description_chars', 155), ('image_kib', 200)):
        content.setdefault(key, value)
    return config, base, metadata


def read_handover(path, allowed_hosts):
    path = Path(path).resolve()
    record, digest = read_object(path)
    url = record.get('site_url')
    if url:
        parsed = urlsplit(url)
        if parsed.scheme not in ('http', 'https') or parsed.hostname not in allowed_hosts:
            raise ValueError('Shared SF handover site does not match this audit')
    return {'path': str(path), 'sha256': digest, 'record': record,
            'note': 'Coordination context only; source identity and export completeness require independent verification.'}
