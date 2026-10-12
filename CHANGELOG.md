# Changes

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
