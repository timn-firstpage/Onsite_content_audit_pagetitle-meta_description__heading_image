# Repository instructions

Maintain only onsite content audit items 17.1–20.2. Read SKILL.md and references/audit-rules.md before changing judgments. The owner confirmed description >155 characters; do not restore 880px. Native SF issue filters are authoritative, target-page exclusions need an explicit inventory, and missing evidence must not pass.

Keep root SKILL.md portable for Multica URL import. Do not add other onsite checks, hardcoded runtime paths, automatic crawling or master-workbook Review/history operations. Shared SF source/config/budgets belong to sf-shared-config and the coordinator.

Run `python -m unittest discover -s tests -v` before committing changes. Verify CSV→findings→XLSX behavior, literal spreadsheet text, no-overwrite and portable packaging. Preserve customer evidence under ignored runs/ only. Do not alter other onsite repositories or user-global installations as part of this repo task.
