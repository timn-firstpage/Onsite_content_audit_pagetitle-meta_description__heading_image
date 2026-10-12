# Shared SF component

The dependency is the existing `sf-shared-config` skill from https://github.com/timn-firstpage/On-_site_SF_shared_config. That repository contains SF `.seospiderconfig` profiles and agent instructions, not a global runtime JSON. Keep it separately installed/imported alongside this content skill; do not copy its profiles or introduce a second configuration owner.

## Agent composition

1. Read the installed shared skill's SKILL.md and references/saved-crawl-entry.md. Resolve its resources on the host running SF. Repository URLs are not local profile paths.
2. Reuse suitable current exports/session first. For an explicit saved crawl, follow supported Open + export once; do not load a profile or start a new crawl. Preserve an active session. A handover record does not prove successful SF loading or complete evidence.
3. Only when new preparation is necessary and permitted, invoke `sf-shared-config`: bundled main for full-site preparation, targeted-content only for a concrete follow-up. It owns profile delivery, sitemap confirmation, manual Start and saved-file handover. Follow its actual installed instructions, including failure fallback.
4. Reuse the common run directory, source-file.json, sf-handover.json, cache and cumulative usage.json. Acquire just the missing [content exports](exports.md) through discovered supported tools or manual export. Record partial/JS/image scope; never generate fake clean files.
5. The coordinating agent supplies site.start_url, source.export_directory, source identity/timestamp when independently verified, and output.audit_date or timezone in its existing run/config.json. Add content settings in memory; other sections remain unchanged. Invoke the command below.

```bash
python scripts/onsite_checklist.py --config <shared-run/config.json> --run-dir <shared-run>
```

If no run JSON is needed, use explicit inputs with the same shared run:

```bash
python scripts/onsite_checklist.py --exports-dir <verified-csv-directory> \
  --site-url https://example.com/ --site-name Example \
  --date 2026-10-12 --run-dir <shared-run>
```

This is composition performed by the agent, not a Python-to-skill API. Python never installs another skill, opens SF, loads profiles, exports a crawl or starts crawling. If the shared skill is unavailable, use existing usable exports or identify that dependency and concrete manual Open/export steps; do not claim it was invoked.

## Python adapter: scripts/shared_config.py

- `--config` wins over optional `ONSITE_AUDIT_CONFIG`. With neither, explicit CLI inputs remain supported. The environment variable is only a local JSON path, never the GitHub URL or a `.seospiderconfig` file. No filesystem-wide scanning or guessed global path.
- Read UTF-8 JSON, validate section object types, preserve unknown keys and all shared settings. Default only checks.content and missing content fields (580px / 155 characters / 200KiB, no inferred targets). Preserve explicit false and reject conflicting thresholds through the audit CLI. Invalid explicit/environment input fails without silent fallback.
- Relative JSON paths resolve from that JSON's directory; CLI paths retain the same convention. Reuse `--run-dir` to share the run; without it the existing unique-run behavior remains.
- Read `<shared-run>/sf-handover.json` if present, or the explicitly supplied `--sf-handover <path>`. Wrong-site or invalid records fail before writing content output. An explicitly supplied missing record fails; an absent optional record does not block usable exports.
- Store config path/hash/selection and handover path/hash/record in content/manifest.json. Handover gaps and completion claims are provenance only: they do not become passes, do not auto-populate a crawl ID, and do not prove export coverage. Verify actual CSVs independently. Treat the full manifest as local customer evidence.
- Never write the original config, handover or usage.json. These additions do not change findings.json schema, filenames or the X-only detail-tab rule.

For repeated use, set the optional variable in the actual execution environment:

```powershell
$env:ONSITE_AUDIT_CONFIG = 'C:\path\to\shared-run\config.json'
python scripts/onsite_checklist.py --run-dir 'C:\path\to\shared-run'
```

```bash
export ONSITE_AUDIT_CONFIG=/path/to/shared-run/config.json
python scripts/onsite_checklist.py --run-dir /path/to/shared-run
```

Use current task config explicitly when switching sites; a stale environment path must not select another site's evidence. No user-global environment settings are changed by this repository.
