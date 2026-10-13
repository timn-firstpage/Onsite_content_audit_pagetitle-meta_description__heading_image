---
name: onsite-audit-content
description: Use when auditing onsite checklist items 17.1–20.2 for page titles, meta descriptions, H1 headings and images using an existing Screaming Frog session, saved crawl or CSV exports, including reuse alongside the other onsite audit skills.
---

# Onsite Content Audit

Produce four Excel reports for **17.1–20.2 only**: `{site name}_page_titles_audit_{YYYY-MM-DD}.xlsx`, `{site name}_meta_descriptions_audit_{YYYY-MM-DD}.xlsx`, `{site name}_headings_audit_{YYYY-MM-DD}.xlsx`, `{site name}_images_audit_{YYYY-MM-DD}.xlsx`. Reuse the working Multica native-filter extraction logic with the owner's confirmed description rule: **>155 characters**, title **>580px**, image **>200 × 1024 bytes**. No canonical, HTTPS, robots, sitemap, pagination, PageSpeed or 20.3 checks.

## Inputs and shared crawl

- Obtain the site URL/name and existing session, saved `.seospider`/`.dbseospider` or exports. Reuse the current task's resolved onsite config; [config.template.json](config.template.json) is a standalone fallback. Do not ask again for already supplied evidence or require the old Begin/Review/template intake.
- Read [shared integration](references/shared-config.md) for source selection, saved-crawl Open, session serialization, cumulative budgets and new-crawl routing. Discover the actual SF tools; do not invent names or reuse an unverified session/crawl ID.
- Use the existing `sf-shared-config` dependency via [config component](references/config-component.md). Its GitHub repository provides profiles and handover, not a runtime JSON. Resolve its installed entry/resources, reuse existing evidence, and route necessary new preparation to it. Pass the shared run/config and run directory to this module. Python reads optional ONSITE_AUDIT_CONFIG only when --config is absent; never use the GitHub URL as a config file.
- Inspect the current session's **Page Titles → Missing** and **Meta Description → Missing** for 17.1 and 18.1. Export the complete native filtered results, not an LLM-generated page scrape or a tool preview. Check existing task/session records for an explicitly identified **target-page URL list**. If available, put it in content.target_urls or content.target_urls_file. Do not infer targets from Missing rows, keywords, a project name or arbitrary pages. With no target list, audit all native Missing rows and disclose that no exclusions were applied; this does not block delivery.
- Verify Python 3.10+ with this repository's requirements and a writable output directory before retrieval. Use the actual runtime or AUDIT_PYTHON; no machine-specific paths, fixed MCP port, licence assumptions or second MCP server. Tools run on the agent's host, not necessarily the user's laptop.
- For a missing local environment, use [portable runtime](references/runtime.md) and scripts/setup_runtime.py --venv <writable-environment-directory> on that actual host. Mac/Linux bootstrap with python3; subsequent commands use the created bin/python, Windows uses Scripts/python.exe. Resolve all paths dynamically; never reuse a Windows venv on Mac. Reuse verified environments (--check-only) and do not claim another machine has been configured.
- If an existing binary has no supported reader, request saved-crawl **File → Open** plus the required exports once. Do not load global config or recrawl as a fallback. If new SF preparation is actually needed and already permitted, installed `sf-shared-config` owns profile preparation, site/sitemap confirmation and manual Start. This module never starts a crawl.

## Audit and report

1. Read [audit rules](references/audit-rules.md) and [CSV contract](references/exports.md). Only request missing reports/fields. Native issue reports may validly contain just headers; absent/invalid reports remain unknown, not clean.
2. Archive/reuse the matching complete exports. Ensure source host/date/scope match the intended run, including partial/JS/image capture context. Keep full files local; show at most five examples in chat.
3. Run the deterministic local command, substituting actual paths:

   ```bash
   python scripts/onsite_checklist.py --config <run/config.json> --run-dir <shared-run>
   ```

   `source.export_directory` supplies CSVs. Alternatively add `--exports-dir`, `--site-url`, `--site-name`, `--date YYYY-MM-DD` and `--target-urls <file>` without a config. Relative paths resolve against the config directory, or CWD when there is no config. Output lives under `<shared-run>/content/` and never overwrites prior content output. No workbook template/download is required.
   The adapter reads existing `<shared-run>/sf-handover.json` as coordination context, or --sf-handover when provided. Preserve its gaps in manifest; do not treat it as proof of source identity, complete exports or passing checks. The original config, handover and cumulative usage remain untouched.
4. Inspect findings.json, manifest.json and all four verified workbooks using [output contract](references/output-contract.md). Each workbook's Checklist contains its own theme's checks; together they cover all twelve, retained in the single findings.json. `√` means no problem in the supplied usable evidence, `X` means confirmed issue rows, `Human Check` means evidence insufficient. Known issues plus gaps remain X with the limitation and next action in Checklist. When a theme has X, merge its confirmed rows into exactly one named detail tab: `17. Page Title`, `18. meta_description`, `19. Heading`, `20. Image`. Add Item No. and map the existing JSON headers/rows by field name; preserve all original values. No X means that theme's workbook has Checklist only. Keep all twelve JSON checks and their gaps; legacy per-check sheet values are metadata, not physical tab names. Never produce the old combined workbook or twelve separate issue tabs.
5. Review all four Checklists and representative detail layouts before delivery. Verify run-status.json reports lists all four files. Summarize results, asset versus inlink counts, exclusions and material gaps. H1 keyword relevance and decorative empty-alt decisions remain human judgments. Do not describe a partial/sampled result as a full-site guarantee.

## Composition boundaries

- Shared evidence/config/session belong to the onsite coordinator. This flow consumes them and writes only its own content results; never reset shared usage.json, re-export the same unchanged data per flow or manipulate one SF instance concurrently.
- This is a fresh standalone audit, not the expanded Multica whole-onsite Review subsystem. It does not insert D/E history columns, merge prior annotations or clear unrelated results. A coordinator may import the twelve decisions and detail rows into a master workbook once, with a separate user-authorized merge.
- No live website repair, publishing, GSC submission, new paid API calls or automatic installation is part of invoking this skill. Ordinary missing evidence yields a deliverable with Human Check; a local parse failure of Page Titles:All prevents a false empty-crawl report. Preserve errors and findings on an export failure, do not rerun the crawl.

For a Multica agent's optional instructions use [agent instructions](references/multica-agent-instructions.md); they point to these same rules. Repository background, installation and import packaging are in [README.md](README.md).
