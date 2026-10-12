# Onsite content audit implementation plan

> For agentic workers: execute directly in this session. User authorized organizing the new repository and reusing the working 17–20 logic.

**Goal:** Portable, independently reusable content audit aligned with the onsite series.
**Architecture:** validated native exports → findings.json/manifest.json → standalone XLSX. Shared SF acquisition stays with the agent and sf-shared-config.
**Tech stack:** Python standard library and openpyxl, unittest, GitHub Actions.
**Spec:** ../specs/2026-10-12-content-audit-design.md

## Constraints and decisions
- Fresh dedicated clone of an empty repository; no additional worktree needed or existing files changed.
- Scope twelve checks only. No runtime-specific absolute paths or customer data committed.
- Owner confirmed >155 characters for descriptions; session-native Missing filters determine 17.1/18.1.
- Reuse working extraction decisions, not the expanded whole-onsite Review subsystem.

## Review focus
Partial evidence, missing numeric headers, target exclusions, image inlink versus asset counts, no-overwrite/literal Excel content are tested at their owning boundaries.

## Tasks
- [x] Write tests first for `extract.audit(exports_dir, targets, thresholds, language)` and `report.build_report(findings, output_dir)`; confirm unsupported behavior fails.
- [x] Implement strict per-report parsing, native SF bucketing and per-item judgments, retaining full evidence metadata.
- [x] Implement standalone validated Excel rendering and CLI/config resolution; test synthetic end-to-end and date/source behavior.
- [x] Write concise skill, references, root config and repository README; include provenance, packaging and CI. Compare packaging/dependency discovery with sibling repositories.
- [x] Validate skill, run regressions, inspect workbook output and have an independent scoped review. Fix supported findings.
- [x] Commit and push the new repository, verify remote content and report actual local/live validation limits.

## Verification ledger

- Baseline: old Multica documents conflicted on scope, Review and description metric; independently inspected by skill reviewer.
- Red: twelve core tests failed before extraction existed; six config/CLI tests failed before CLI existed. Environment TEMP redirected to ignored runs/test-tmp after Windows sandbox default temp permissions failed.
- Green: extraction/config/report tests passed; independent review found four evidence bugs. Five new regression tests reproduced them, then all 23 passed after corrections.
- Skill forward review: scenario now uses saved session exports, only 17–20, 155 characters, no inferred targets/recrawl or Review rollover. Re-review found no remaining blocking issue.
- Package verified with root SKILL.md and fourteen files; frontmatter validator passed using a temporary local PyYAML dependency, not a shared runtime modification.
- Synthetic workbook generated and read back; inspected local rendered Checklist and oversize-image previews. All customer/source archives ignored.
- Ruling: coordinator owns master workbook/history; this module publishes fresh standalone content artifacts to avoid duplicate mutations across onsite flows.
- Limit: no live SF MCP tool/session was available here; Multica import and SF export coverage remain runtime checks, not locally verified claims.
- Published implementation d1b3c53 on main; GitHub SKILL.md and remote branch SHA verified. CI triggered for Windows/Linux × Python 3.10/3.12. Final CI result is reported separately from this initial publication record.
