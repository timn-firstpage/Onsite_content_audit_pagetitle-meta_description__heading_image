import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))


class SharedConfigTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, name, data):
        path = self.root / name
        path.write_text(json.dumps(data), encoding='utf-8')
        return path

    def test_global_environment_and_defaults_preserve_original(self):
        from shared_config import load_config
        original = {'site': {'start_url': 'https://example.com'}, 'budget': {'max_mcp_calls': 7},
                    'checks': {'robots': True}, 'custom': {'keep': 1}}
        path = self.write('global.json', original)
        with patch.dict(os.environ, {'ONSITE_AUDIT_CONFIG': str(path)}):
            config, base, metadata = load_config()
        self.assertEqual(base, self.root)
        self.assertEqual(config['budget'], original['budget'])
        self.assertEqual(config['custom'], original['custom'])
        self.assertTrue(config['checks']['robots'])
        self.assertEqual(config['content']['description_chars'], 155)
        self.assertEqual(metadata['selection'], 'environment')
        self.assertEqual(json.loads(path.read_text()), original)

    def test_explicit_config_wins_and_false_is_preserved(self):
        from shared_config import load_config
        path = self.write('run.json', {'checks': {'content': False}, 'content': {'target_urls': ['https://example.com/a']}})
        with patch.dict(os.environ, {'ONSITE_AUDIT_CONFIG': str(self.root / 'missing.json')}):
            config, _, metadata = load_config(path)
        self.assertFalse(config['checks']['content'])
        self.assertEqual(config['content']['target_urls'], ['https://example.com/a'])
        self.assertEqual(metadata['selection'], 'explicit')

    def test_invalid_global_config_fails_without_fallback(self):
        from shared_config import load_config
        with patch.dict(os.environ, {'ONSITE_AUDIT_CONFIG': str(self.root / 'missing.json')}):
            with self.assertRaises(OSError):
                load_config()
        path = self.write('bad.json', {'source': []})
        with self.assertRaises(ValueError):
            load_config(path)

    def test_handover_is_context_not_merge_and_wrong_site_rejected(self):
        from shared_config import read_handover
        data = {'site_url': 'https://example.com/', 'phase': 'handover',
                'crawl': {'id': 'record-only'}, 'gaps': ['Unverified exports']}
        path = self.write('sf-handover.json', data)
        record = read_handover(path, {'example.com'})
        self.assertEqual(record['record'], data)
        self.assertTrue(record['sha256'])
        with self.assertRaises(ValueError):
            read_handover(path, {'other.example'})


if __name__ == '__main__':
    unittest.main()
