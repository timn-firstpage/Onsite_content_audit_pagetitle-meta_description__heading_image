# Integration with the onsite series

Use the existing resolved config and run from the HTTPS/robots/sitemap coordinator. The same `site`, `source`, `mcp`, `budget`, `cache` and `output` fields are accepted. This module adds `checks.content` and `content` only; ignore sibling checks without changing them.

The concrete [config component](config-component.md) uses the existing separately installed sf-shared-config skill for SF preparation/handover and scripts/shared_config.py for read-only runtime JSON adaptation. --config takes priority over optional ONSITE_AUDIT_CONFIG. Preserve the current shared run with --run-dir; its optional sf-handover.json is retained as unverified coordination context, not merged into source identity. Both inputs' paths/hashes appear in manifest, without writing global settings or usage.

Read the installed [sf-shared-config](https://github.com/timn-firstpage/On-_site_SF_shared_config) SKILL.md when SF preparation is needed. It is a separate dependency, not copied or auto-installed here. Shared [saved-crawl entry](https://github.com/timn-firstpage/On-_site_SF_shared_config/blob/main/references/saved-crawl-entry.md) applies to this caller too:

1. Explicitly supplied saved file/session wins over stale config. Use source.mode=saved_crawl and source.crawl_file, or the verified session crawl_id. `.seospiderconfig` is not a crawl.
2. Preflight readable stable file/output runtime once; reuse source-file.json. Verify site, timestamp, completion/partial scope and fields from supported metadata. Do not deserialize arbitrary binary crawls in Python.
3. Preserve active/unsaved sessions. Open at most once through discovered supported tools. No sf_crawl/Start/Resume or global config load for saved-crawl analysis. source.allow_new_crawl=false permits supported saved-crawl Open/export.
4. No reader/import failure: request File → Open of the saved crawl plus only required exports. Capture failure once; no setup loop or speculative recrawl.
5. Serialize operations on one SF instance. Reuse cached complete exports keyed by unchanged source/session/filter/fields/context. Do not export the same unchanged data again for another flow. Append acquisition usage to the coordinator's existing usage.json; do not reset budgets or pretend config limits enforce themselves.
6. New crawl preparation, if explicitly permitted and needed, goes to shared configuration and the user's manual Start. This module is not an independent crawler. Missing unrelated sitemap/robots evidence does not block content checks.

Python processes source.export_directory only, without accessing SF or the website. Acquisition via MCP/CLI/GUI is the agent's responsibility. No macOS-only hardcoded launcher remains. Checks.live_checks=false does not prohibit local parsing or supported remote MCP export transport, subject to actual permissions and cumulative MCP budget.

Config paths resolve against the config file's directory. CLI --exports-dir overrides source.export_directory. Supply target URLs through current task/session's explicitly identified inventory; content.target_urls_file can be Address/URL CSV or one URL per line. Site allowed_hosts is an explicit list; absent list defaults to start host plus its www/non-www counterpart. Unexpected exported page hosts cause a source mismatch, not a report for the wrong site. External image destinations remain allowed.

The shared run keeps sf-handover.json/source-file.json/usage.json. Content artifacts are isolated under `<shared-run>/content/`: findings.json, manifest.json, raw/ (when archive_raw=true), run-status.json and workbook. Source timestamps come from supplied source.crawl_timestamp, never filesystem modification time. No previous onsite workbook/template is required. No D/E historical column operations here; a master workbook coordinator owns merging and history once.

Rows cannot carry unverified pass decisions between flows. The content findings schema is documented separately; a coordinator maps only 17.1–20.2. This repository does not implement the coordinator or silently modify siblings.
