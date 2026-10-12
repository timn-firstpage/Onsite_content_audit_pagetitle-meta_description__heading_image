import importlib.util
import csv
import json
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


class ContentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)

    def write(self, name, headers, rows):
        with (self.path / name).open('w', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f)
            w.writerow(headers)
            w.writerows(rows)

    def full_exports(self):
        self.write('page_titles_all.csv', ['Address', 'Indexability', 'Title 1', 'Title 1 Pixel Width'],
                   [['https://example.com/a', 'Indexable', 'Title', '580']])
        self.write('meta_description_all.csv', ['Address', 'Indexability', 'Meta Description 1', 'Meta Description 1 Pixel Width'],
                   [['https://example.com/a', 'Indexable', 'description', '880']])
        for name, headers in {
            'page_titles_missing.csv': ['Address'], 'page_titles_duplicate.csv': ['Address', 'Title 1'],
            'page_titles_multiple.csv': ['Address', 'Title 1', 'Title 2'],
            'meta_description_missing.csv': ['Address'], 'meta_description_duplicate.csv': ['Address', 'Meta Description 1'],
            'h1_missing.csv': ['Address'], 'h1_duplicate.csv': ['Address', 'H1-1', 'H1-2'],
            'h1_multiple.csv': ['Address', 'H1-1', 'H1-2'],
            'images_missing_alt_attribute_and_text_inlinks.csv': ['Source', 'Destination'],
        }.items():
            self.write(name, headers, [])
        self.write('images_all.csv', ['Address'], [['https://cdn.example.com/a.png']])
        self.write('all_image_inlinks.csv', ['Source', 'Destination', 'Size (Bytes)'],
                   [['https://example.com/a', 'https://cdn.example.com/a.png', '204800']])

    def audit(self, **kwargs):
        if not (ROOT / 'scripts' / 'extract.py').exists():
            self.fail('Content extraction interface has not been implemented')
        import extract
        return extract.audit(self.path, **kwargs)

    def check(self, data, item):
        return next(c for c in data['checks'] if c['id'] == item)

    def test_native_empty_exports_pass_and_scope_is_twelve(self):
        self.full_exports()
        data = self.audit()
        self.assertEqual(len(data['checks']), 12)
        self.assertEqual({c['result'] for c in data['checks']}, {'√'})

    def test_native_duplicates_not_recomputed_from_all(self):
        self.full_exports()
        self.write('page_titles_all.csv', ['Address', 'Indexability', 'Title 1', 'Title 1 Pixel Width'],
                   [['https://example.com/a', 'Indexable', 'Same', 100], ['https://example.com/b', 'Non-Indexable', 'Same', 100]])
        self.assertEqual(self.check(self.audit(), '17.2')['result'], '√')

    def test_h1_drops_only_pure_same_page_collision(self):
        self.full_exports()
        self.write('h1_duplicate.csv', ['Address', 'H1-1', 'H1-2'],
                   [['a', 'Unique', 'Unique'], ['b', 'Shared', 'Shared'], ['c', 'Shared', 'Other']])
        self.assertEqual(self.check(self.audit(), '19.2')['row_count'], 2)

    def test_thresholds_indexability_and_description_characters(self):
        self.full_exports()
        self.write('page_titles_all.csv', ['Address', 'Indexability', 'Title 1', 'Title 1 Pixel Width'],
                   [['a', 'Indexable', 'Long', 581], ['b', 'Non-Indexable', 'Long', 900]])
        self.write('meta_description_all.csv', ['Address', 'Indexability', 'Meta Description 1', 'Meta Description 1 Pixel Width'],
                   [['a', 'Indexable', 'x' * 156, 100], ['b', 'Indexable', 'short', 881]])
        self.assertEqual(self.check(self.audit(), '17.3')['row_count'], 1)
        self.assertEqual(self.check(self.audit(), '18.3')['rows'][0][0], 'a')

    def test_exact_targets_only_exclude_missing_title_description(self):
        self.full_exports()
        self.write('page_titles_missing.csv', ['Address'], [['https://example.com/a'], ['https://example.com/a?x=1']])
        self.write('meta_description_missing.csv', ['Address'], [['https://example.com/a']])
        self.write('h1_missing.csv', ['Address'], [['https://example.com/a']])
        data = self.audit(targets=['https://example.com/a'])
        self.assertEqual(self.check(data, '17.1')['row_count'], 1)
        self.assertEqual(self.check(data, '18.1')['row_count'], 0)
        self.assertEqual(self.check(data, '19.1')['row_count'], 1)

    def test_missing_and_invalid_exports_are_unknown_not_clean(self):
        self.full_exports()
        (self.path / 'h1_missing.csv').unlink()
        self.write('page_titles_all.csv', ['Address', 'Indexability', 'Title 1'], [['a', 'Indexable', 'Title']])
        data = self.audit()
        self.assertEqual(self.check(data, '19.1')['result'], 'Human Check')
        self.assertEqual(self.check(data, '17.3')['result'], 'Human Check')

    def test_known_oversize_survives_partial_cdn_size_evidence(self):
        self.full_exports()
        self.write('images_all.csv', ['Address'], [])
        self.write('all_image_inlinks.csv', ['Source', 'Destination', 'Size (Bytes)'],
                   [['a', 'https://cdn.example.com/big.png', 204801], ['b', 'https://cdn.example.com/big.png', 204801],
                    ['a', 'https://cdn.example.com/unknown.png', '']])
        c = self.check(self.audit(), '20.2')
        self.assertEqual((c['result'], c['row_count'], c['unique_assets']), ('X', 2, 1))
        self.assertTrue(c['gaps'])

    def test_images_without_capture_or_missing_alt_report_unknown(self):
        self.full_exports()
        (self.path / 'images_missing_alt_attribute_and_text_inlinks.csv').unlink()
        self.assertEqual(self.check(self.audit(), '20.1')['result'], 'Human Check')
        self.write('images_all.csv', ['Address'], [])
        self.write('all_image_inlinks.csv', ['Source', 'Destination', 'Size (Bytes)'], [])
        self.assertEqual(self.check(self.audit(), '20.2')['result'], 'Human Check')

    def test_invalid_numbers_do_not_prove_pass(self):
        self.full_exports()
        self.write('all_image_inlinks.csv', ['Source', 'Destination', 'Size (Bytes)'], [['a', 'img', 'bad']])
        self.assertEqual(self.check(self.audit(), '20.2')['result'], 'Human Check')

    def test_captured_asset_missing_from_inlinks_is_unknown(self):
        self.full_exports()
        self.write('images_all.csv', ['Address'], [['https://cdn.example.com/a.png'], ['https://cdn.example.com/b.png']])
        self.assertEqual(self.check(self.audit(), '20.2')['result'], 'Human Check')

    def test_header_only_description_all_cannot_prove_clean(self):
        self.full_exports()
        self.write('meta_description_all.csv', ['Address', 'Indexability', 'Meta Description 1'], [])
        self.assertEqual(self.check(self.audit(), '18.3')['result'], 'Human Check')

    def test_empty_crawl_is_rejected(self):
        self.full_exports()
        self.write('page_titles_all.csv', ['Address', 'Indexability', 'Title 1 Pixel Width'], [])
        with self.assertRaisesRegex(ValueError, 'Page Titles:All'):
            self.audit()

    def test_ambiguous_report_is_not_silently_selected(self):
        self.full_exports()
        self.write('old_h1_missing.csv', ['Address'], [])
        self.assertEqual(self.check(self.audit(), '19.1')['result'], 'Human Check')

    def test_report_exact_tabs_literal_values_and_no_overwrite(self):
        self.full_exports()
        self.write('page_titles_duplicate.csv', ['Address', 'Title 1'], [['a', '=1+1'], ['b', '=1+1']])
        data = self.audit()
        import report
        data.update(site_name='Example', site_url='https://example.com/', audit_date='2026-10-12')
        output = report.build_report(data, self.path / 'reports')
        import openpyxl
        wb = openpyxl.load_workbook(output)
        self.addCleanup(wb.close)
        self.assertEqual(wb.sheetnames, ['Checklist', '17.2 Page titles - Duplicate'])
        self.assertEqual(wb.sheetnames[0], 'Checklist')
        self.assertEqual(wb['17.2 Page titles - Duplicate']['B2'].value, '=1+1')
        self.assertEqual(wb['17.2 Page titles - Duplicate']['B2'].data_type, 's')
        self.assertNotIn('20.2 Image - Oversize', wb.sheetnames)
        with self.assertRaises(FileExistsError):
            report.build_report(data, self.path / 'reports')

    def test_report_clean_and_unknown_checks_stay_on_checklist(self):
        self.full_exports()
        import report
        import openpyxl
        for unknown in (False, True):
            if unknown:
                (self.path / 'h1_missing.csv').unlink()
            data = self.audit()
            data.update(site_name='Example', site_url='https://example.com/', audit_date='2026-10-12')
            output = report.build_report(data, self.path / str(unknown))
            with output.open('rb') as source:
                wb = openpyxl.load_workbook(source)
                try:
                    self.assertEqual(wb.sheetnames, ['Checklist'])
                    self.assertEqual(wb['Checklist'].max_row, 13)
                    self.assertEqual(len(data['checks']), 12)
                    self.assertTrue(all(not c['rows'] for c in data['checks']))
                    self.assertEqual(wb['Checklist']['C9'].value, 'Human Check' if unknown else '√')
                finally:
                    wb.close()

    def cli(self, config, run='run'):
        script = ROOT / 'scripts' / 'onsite_checklist.py'
        self.assertTrue(script.exists(), 'Config/CLI interface has not been implemented')
        return subprocess.run([sys.executable, str(script), '--config', str(config), '--run-dir', str(self.path / run)],
                              capture_output=True, text=True, encoding='utf-8')

    def config(self, site='https://example.com/', extra=None):
        data = {'site': {'name': 'Example', 'start_url': site},
                'source': {'mode': 'exports', 'export_directory': '.'},
                'output': {'audit_date': '2026-10-12', 'timezone': 'Asia/Hong_Kong', 'language': 'en'}}
        data.update(extra or {})
        path = self.path / 'config.json'
        path.write_text(json.dumps(data), encoding='utf-8')
        return path

    def test_cli_shared_config_relative_paths_and_no_overwrite(self):
        self.full_exports()
        config = self.config()
        result = self.cli(config)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.path / 'run' / 'content' / 'findings.json').read_text(encoding='utf-8'))
        self.assertEqual(data['audit_date'], '2026-10-12')
        self.assertTrue((self.path / 'run' / 'content' / 'manifest.json').exists())
        self.assertNotEqual(self.cli(config).returncode, 0)

    def test_cli_rejects_other_site_exports(self):
        self.full_exports()
        result = self.cli(self.config(site='https://wrong.example/'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('host', result.stderr.lower())
        self.assertFalse((self.path / 'run' / 'content' / 'findings.json').exists())

    def test_cli_rejects_mixed_site_filtered_exports(self):
        self.full_exports()
        self.write('h1_missing.csv', ['Address'], [['https://wrong.example/a']])
        self.assertNotEqual(self.cli(self.config()).returncode, 0)

    def test_cli_rejects_wrong_image_source_not_external_destination(self):
        self.full_exports()
        self.write('all_image_inlinks.csv', ['Source', 'Destination', 'Size (Bytes)'],
                   [['https://wrong.example/a', 'https://cdn.example.com/a.png', 204800]])
        self.assertNotEqual(self.cli(self.config()).returncode, 0)

    def test_export_override_clears_unverified_old_crawl_identity(self):
        self.full_exports()
        config = self.config(extra={'source': {'mode': 'saved_crawl', 'export_directory': 'old', 'crawl_file': 'old.seospider',
                                              'crawl_id': 'old', 'crawl_timestamp': '2000-01-01'}})
        script = ROOT / 'scripts' / 'onsite_checklist.py'
        result = subprocess.run([sys.executable, str(script), '--config', str(config), '--exports-dir', str(self.path),
                                 '--run-dir', str(self.path / 'override')], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((self.path / 'override' / 'content' / 'manifest.json').read_text(encoding='utf-8'))
        self.assertIsNone(manifest['crawl_timestamp'])
        self.assertEqual(manifest['source']['export_directory'], str(self.path.resolve()))
        self.assertIsNone(manifest['source'].get('crawl_id'))

    def test_saved_crawl_without_exports_requests_open_not_recrawl(self):
        config = self.config(extra={'source': {'mode': 'saved_crawl', 'crawl_file': 'example.seospider', 'allow_new_crawl': False}})
        result = self.cli(config)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('saved crawl', result.stderr.lower())

    def test_cli_disable_flow_does_not_read_exports(self):
        config = self.config(extra={'checks': {'content': False}})
        result = self.cli(config)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('disabled', result.stdout)
        self.assertFalse((self.path / 'run').exists())

    def test_cli_target_file_and_explicit_date(self):
        self.full_exports()
        self.write('page_titles_missing.csv', ['Address'], [['https://example.com/a']])
        self.write('targets.csv', ['Address'], [['https://example.com/a']])
        result = self.cli(self.config(extra={'content': {'target_urls_file': 'targets.csv'}}))
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.path / 'run' / 'content' / 'findings.json').read_text(encoding='utf-8'))
        self.assertEqual(self.check(data, '17.1')['result'], '√')

    def test_cli_timezone_required_when_date_not_supplied(self):
        self.full_exports()
        result = self.cli(self.config(extra={'output': {'language': 'en'}}))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('timezone', result.stderr.lower())


if __name__ == '__main__':
    unittest.main()
