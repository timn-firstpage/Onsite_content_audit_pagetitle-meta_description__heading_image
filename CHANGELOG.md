# Changes

## 1.1.2 — 2026-10-13

- Replace the aggregate title issue tab with X-only individual 17.1–17.4 tabs, using the owner's exact sheet names/columns.
- Preserve JSON detail fields and manual values through display-column mappings; keep four report files and other themes unchanged.

## 1.1.1 — 2026-10-13

- Fix Windows CI path comparison to normalize 8.3 temporary-directory aliases.
- Add a portable local-venv setup/check helper and MacBook runtime instructions without machine-specific paths.
- Include macOS Python 3.10/3.12 in CI and smoke-test environment setup/check-only across platforms.

## 1.1.0 — 2026-10-13

- Split Excel delivery into page_titles, meta_descriptions, headings and images workbooks, each with its theme Checklist.
- Merge each theme's confirmed X rows into a single named detail tab: 17. Page Title, 18. meta_description, 19. Heading, 20. Image. Preserve fields by name and add Item No.
- Keep the shared twelve-check findings.json unchanged; use reports (four paths) in run-status.json instead of report.
- Precheck every destination and verify all four reports; handled generation failures remove only newly created workbooks.

## 1.0.2 — 2026-10-12

- Add a read-only shared configuration adapter with explicit config precedence and optional ONSITE_AUDIT_CONFIG.
- Read shared SF handover as provenance, reject mismatched sites, and preserve original config/budgets.
- Document composition with the existing separate sf-shared-config skill; include the adapter in portable packaging.

## 1.0.1 — 2026-10-12

- Create Excel detail tabs only for X checks; retain all twelve checks in Checklist and the existing findings.json schema.
- Add the shared onsite cover and the twelve-item judgment matrix to README.

## 1.0.0 — 2026-10-12

- Extract the working Multica content rules as the standalone onsite-audit-content module, scoped to 17.1–20.2.
- Owner-confirmed description maximum: 155 characters, replacing 880px.
- Preserve SF native duplicates, pure same-page H1 refinement and external CDN image inlink sizing.
- Align shared config/saved-crawl acquisition and standalone Checklist/report conventions with the onsite series.
- Add exact optional target exclusions, per-report evidence gaps, literal Excel strings and no-overwrite behavior.
- Remove expanded canonical/HTTPS/robots/sitemap/etc. checks, whole-onsite template downloading and Review history operations from this module.
