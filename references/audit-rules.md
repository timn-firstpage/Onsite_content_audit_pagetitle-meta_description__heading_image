# Rules for 17–20

The item questions and tab names in scripts/extract.py are fixed to the owner's checklist. The sections are 17.0 titles, 18.0 descriptions, 19.0 headings, 20.0 images; the report has twelve individual checks, not extra aggregate decisions.

| Item | Decision and source |
| --- | --- |
| 17.1 | SF Page Titles:Missing, minus exact explicitly identified target URLs. |
| 17.2 | SF Page Titles:Duplicate, grouping identical Title 1 values, largest groups first. Do not recreate duplicates from All. |
| 17.3 | Page Titles:All, Indexability=Indexable, Title 1 Pixel Width >580. Descending width. |
| 17.4 | SF Page Titles:Multiple. |
| 18.1 | SF Meta Description:Missing, minus the same exact target URLs. |
| 18.2 | SF Meta Description:Duplicate; group identical Meta Description 1, largest groups first. |
| 18.3 | Meta Description:All, Indexability=Indexable, length of Meta Description 1 >155 Unicode code points. Exactly 155 passes. Use exported text, no trimming, byte count, pixel estimate or markup parsing. 880px from the old Multica version is retired. |
| 19.1 | SF H1:Missing. This verifies missing H1 only; keyword optimization is human judgment and multiple H1 is 19.3. Keep the original question and explain that boundary. |
| 19.2 | Start from SF H1:Duplicate. Remove a same-page H1-1==H1-2 row only if that H1-1 occurs once within the native duplicate set. A row may repeat H1 locally AND share it across pages: retain it. |
| 19.3 | SF H1:Multiple. |
| 20.1 | Images Missing Alt Attribute & Text Inlinks. Includes alt=""; inspect decorative images before prescribing fixes. One image on ten pages can yield ten rows. |
| 20.2 | All Image Inlinks Size (Bytes), fallback Size, >204800 bytes. Include external CDN images directly from inlinks; never inner-join Images:All or use SF's config-dependent Over X kB filter. Largest sizes first. |

## Targets and evidence

Inspect the existing SF session's native Missing filters first. An explicitly identified target inventory in current task/session records is usable; record its source and exact URL values. SF's Missing filter does not itself identify the business's target pages. Without an explicit list apply no exclusions and disclose this on 17.1/18.1. Match exact URL strings with outer whitespace removed; keep case, query and trailing slash differences. Do not exclude targets from duplicates, widths, H1 or images.

An available, valid header-only issue report means zero matches in the supplied sample. Missing, malformed, ambiguous CSVs, missing required columns and blank issue identities produce an item-specific evidence gap. Page Titles:All must contain data or the run fails. All-based thresholds need explicit Indexability and usable metric/text columns; unknown Indexability/numeric values cannot pass.

No captured images across image reports makes both image checks Human Check. Available image/alt records can establish capture even with empty Images:All. Missing Alt report makes 20.1 unknown unless known rows establish failure. Missing/invalid/zero sizes make 20.2 incomplete. Keep known oversize rows and X while disclosing remaining unknown sizes. Do not treat some known image sizes as complete coverage of all images.

Results: √ = usable evidence with no issue; X = one or more confirmed rows; Human Check = no confirmed rows and an evidence gap. No automatic NA for absent exports or disabled image crawling. Known X survives gaps. Images have row_count, unique_assets and affected_pages in findings.json. Scope means the supplied export sample, never a promise that SF captured the entire site.
