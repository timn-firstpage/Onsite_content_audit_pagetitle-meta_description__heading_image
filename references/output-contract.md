# Output contract

Four files are always produced on a successful run, even when a theme has no issues:

| File | Checklist scope | X-only detail tab |
| --- | --- | --- |
| `{site name}_page_titles_audit_{YYYY-MM-DD}.xlsx` | 17.1–17.4 | Separate 17.1–17.4 tabs below |
| `{site name}_meta_descriptions_audit_{YYYY-MM-DD}.xlsx` | 18.1–18.3 | `18. meta_description` |
| `{site name}_headings_audit_{YYYY-MM-DD}.xlsx` | 19.1–19.3 | `19. Heading` |
| `{site name}_images_audit_{YYYY-MM-DD}.xlsx` | 20.1–20.2 | `20. Image` |

Name from supplied site.name/--site-name, otherwise hostname without www. Date from --date/output.audit_date or output.timezone; never silently use another host's local date. Repeated audit uses a new run/content directory, never overwrites. The old combined content_audit workbook is no longer generated.

The titles workbook has Checklist first, followed by a separate detail tab for each X check in 17.1–17.4, in numeric order (one to five sheets total). The other three workbooks retain one or two sheets: Checklist first, then their single named theme tab when at least one check is X. Merge 18/19/20 X rows by field name and add Item No. to identify subchecks. √ and Human Check do not create detail tabs or rows. No X in a theme means that workbook contains Checklist only. Headers are **row 1, data from row 2**.

Titles use exactly these physical tab names and columns, without an added Item No. column:

| Title detail tab | Columns |
| --- | --- |
| 17.1 Page title -Missing | Address, New Title, Remarks |
| 17.2 Page title - Duplicate | Address, Titles, New Title, Instructions (If have) |
| 17.3 Page title -Too Long | Address, Title - 1, Pixel Width ( max 580 pixels), Revised Title |
| 17.4 Page title - Multiple | Address, Title - 1, Title - 2, Instructions |

Map JSON Title 1 to Titles (17.2) or Title - 1 (17.3/17.4), Title 2 to Title - 2, and Title 1 Pixel Width to Pixel Width ( max 580 pixels). Map the existing Remarks field to Instructions (If have) for 17.2 and Instructions for 17.4. Manual fields remain blank unless supplied; no invented replacements or instructions. The old combined 17. Page Title tab is no longer generated.

Checklist: `Item No. | Item Name | Initial Check | Findings | Instruction`. Each theme's original English questions appear once; together the four Checklists cover all twelve checks. √/X/Human Check, no Yes/No, Coverage or extra history columns. Findings is the short observed conclusion; Instruction is the person's next action, `—` if none. Known issues with gaps remain X and disclose the incomplete part. Pure gaps stay on Checklist, not issue tabs. H1 presence and decorative-image caveats are explicit.

For 18/19/20, merged detail headers are Item No. followed by the ordered union of that theme's existing JSON headers. Map cells by header name; leave fields absent from a row blank. Do not align mixed issue rows by raw column position or discard metrics/manual fields.

| Theme detail tab | Columns |
| --- | --- |
| 18. meta_description | Item No., Address, Instruction, Meta Description 1, Character Count |
| 19. Heading | Item No., Address, Instruction, H1-1, Remarks, H1-2 |
| 20. Image | Item No., Source, Destination, Screenshots (If have), Size (Bytes) |

Existing per-check JSON detail schema (the `sheet` values remain legacy per-check metadata for compatibility; they no longer name physical workbook tabs):

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

New Title/Revised Title/Remarks/Instruction/screenshot fields are blank for human work; do not fabricate replacement copy or screenshots. This generator doesn't embed images or carry old annotations. Existing findings.json keys and per-check headers/rows are unchanged; every check retains its metadata, rows and gaps in JSON. All problem rows are preserved, duplicates grouped and widths/sizes sorted descending. Image rows are references; report unique asset/page counts separately. Store any supplied formula-looking text as literal strings; no website text may execute Excel formulas.

findings.json is machine-readable: schema_version, language, site_name, site_url, audit_date and checks. Each check contains id/item_name/sheet/headers/result/finding/action, rows/row_count, sources and gaps. Image checks also carry unique_assets and affected_pages. The renderer validates all twelve IDs, schema, counts and result/gap consistency, reopens XLSX and verifies every value and the absence of formulas.

manifest.json stores export paths, states, hashes, headers/counts, thresholds, target exclusions, observed hosts, source metadata and local operation counts. Keep raw evidence ignored. Missing native-filter files, field errors and unknown sizes stay explicit in gaps; no synthetic clean CSVs. run-status.json says complete only after report read-back. Generation failure leaves evidence for troubleshooting and must not be reported as completed.

Shared output is four XLSX files + findings.json + manifest.json + run-status.json, plus optional raw/ CSVs. run-status.json uses `reports` (four paths in theme order), replacing the old singular `report`, and retains state=complete/items=12. Verify all four buffers before file creation, precheck all destination paths, and reopen all four saved files. Handled write/read-back failure removes only this invocation's newly created workbooks, leaving JSON/raw evidence and unrelated files. No complete status is written on failure. A process interruption may still leave partial files; use a fresh run directory.

manifest.config_input records the selected runtime JSON path/hash and explicit/environment/cli_only selection. manifest.shared_handover is null when absent, otherwise path/hash/record/note for the shared SF context; it does not certify crawl identity or coverage. These additive provenance fields leave findings.json unchanged.

Render/inspect Checklist and representative detail tabs before customer delivery. Long values remain in raw exports and must not be shortened silently. The fixed workbook has wrapped cells, frozen headers and status fills. If unusually large text cannot fit a readable row, shorten reviewed narrative only or produce a separate view while retaining evidence; don't truncate source values.
