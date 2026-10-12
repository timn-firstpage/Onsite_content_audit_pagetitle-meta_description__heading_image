# Output contract

File: `{site name}_content_audit_{YYYY-MM-DD}.xlsx`. Name from supplied site.name/--site-name, otherwise hostname without www. Date from --date/output.audit_date or output.timezone; never silently use another host's local date. Repeated audit uses a new run/content directory, never overwrites.

One to thirteen worksheets: Checklist first, followed only by detail tabs for checks with result X, in numeric order. √ and Human Check do not create detail tabs. No X means Checklist only. All twelve checks remain in Checklist and findings.json. Titles/capitalization match the owner's table exactly. Headers are **row 1, data from row 2**, aligning with the standalone onsite series rather than the old whole-onsite template's row-3 headers.

Checklist: `Item No. | Item Name | Initial Check | Findings | Instruction`. All twelve original English questions appear once. √/X/Human Check, no Yes/No, Coverage or extra history columns. Findings is the short observed conclusion; Instruction is the person's next action, `—` if none. Known issues with gaps remain X and disclose the incomplete part. Pure gaps stay on Checklist, not issue tabs. H1 presence and decorative-image caveats are explicit.

Detail schema:

| Sheet | Columns |
| --- | --- |
| 17.1 Page titles - Missing | Address, New Title, Remarks |
| 17.2 Page titles - Duplicate | Address, Title 1, New Title, Remarks |
| 17.3 Page titles - Too Long | Address, Title 1, Title 1 Pixel Width, Revised Title |
| 17.4 Page titles - Multiple | Address, Title 1, Title 2, Remarks |
| 18.1 Descriptions - Missing | Address, Instruction |
| 18.2 Descriptions - Duplicate | Address, Meta Description 1 |
| 18.3 Descriptions - Too Long | Address, Meta Description 1, Character Count |
| 19.1 H1 - Missing | Address, Instruction |
| 19.2 H1 - Duplicate | Address, H1-1, Remarks |
| 19.3 H1 - Multiple | Address, H1-1, H1-2 |
| 20.1 Image - Alt Text Missing | Source, Destination, Screenshots (If have) |
| 20.2 Image - Oversize | Source, Destination, Size (Bytes) |

New Title/Revised Title/Remarks/Instruction/screenshot fields are blank for human work; do not fabricate replacement copy or screenshots. This generator doesn't embed images or carry old annotations. Clean/unknown-only sheets are omitted. Existing findings.json keys and detail headers/rows are unchanged; an omitted sheet still has its check metadata, empty rows and any gaps in JSON. All problem rows are preserved, duplicates grouped and widths/sizes sorted descending. Image rows are references; report unique asset/page counts separately. Store any supplied formula-looking text as literal strings; no website text may execute Excel formulas.

findings.json is machine-readable: schema_version, language, site_name, site_url, audit_date and checks. Each check contains id/item_name/sheet/headers/result/finding/action, rows/row_count, sources and gaps. Image checks also carry unique_assets and affected_pages. The renderer validates all twelve IDs, schema, counts and result/gap consistency, reopens XLSX and verifies every value and the absence of formulas.

manifest.json stores export paths, states, hashes, headers/counts, thresholds, target exclusions, observed hosts, source metadata and local operation counts. Keep raw evidence ignored. Missing native-filter files, field errors and unknown sizes stay explicit in gaps; no synthetic clean CSVs. run-status.json says complete only after report read-back. Generation failure leaves evidence for troubleshooting and must not be reported as completed.

manifest.config_input records the selected runtime JSON path/hash and explicit/environment/cli_only selection. manifest.shared_handover is null when absent, otherwise path/hash/record/note for the shared SF context; it does not certify crawl identity or coverage. These additive provenance fields leave findings.json unchanged.

Render/inspect Checklist and representative detail tabs before customer delivery. Long values remain in raw exports and must not be shortened silently. The fixed workbook has wrapped cells, frozen headers and status fills. If unusually large text cannot fit a readable row, shorten reviewed narrative only or produce a separate view while retaining evidence; don't truncate source values.
