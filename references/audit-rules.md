# Rules for 17–20

The item questions and tab names in scripts/extract.py are fixed to the owner's checklist. The sections are 17.0 titles, 18.0 descriptions, 19.0 headings, 20.0 images; the report has twelve individual checks, not extra aggregate decisions.

| Item | Decision and source |
| --- | --- |
| 17.1 | SF Page Titles:Missing, minus exact explicitly identified target URLs. |
| 17.2 | SF Page Titles:Duplicate → Indexable → retain groups with at least two distinct URLs sharing Title 1. Largest groups first; never derive candidates from All. |
| 17.3 | Page Titles:All, Indexability=Indexable, Title 1 Pixel Width >580. Descending width. |
| 17.4 | SF Page Titles:Multiple. |
| 18.1 | SF Meta Description:Missing, minus the same exact target URLs. |
| 18.2 | SF Meta Description:Duplicate → Indexable → retain groups with at least two distinct URLs sharing Meta Description 1, largest groups first. |
| 18.3 | Meta Description:All, Indexability=Indexable, length of Meta Description 1 >155 Unicode code points. Exactly 155 passes. Use exported text, no trimming, byte count, pixel estimate or markup parsing. 880px from the old Multica version is retired. |
| 19.1 | SF H1:Missing. This verifies missing H1 only; keyword optimization is human judgment and multiple H1 is 19.3. Keep the original question and explain that boundary. |
| 19.2 | SF H1:Duplicate → Indexable → retain H1-1 groups with at least two distinct URLs. Pure same-page repetitions are not cross-page duplication; check multiple H1 in 19.3. |
| 19.3 | SF H1:Multiple. |
| 20.1 | Images Missing Alt Attribute & Text Inlinks. Includes alt=""; inspect decorative images before prescribing fixes. One image on ten pages can yield ten rows. |
| 20.2 | All Image Inlinks Size (Bytes), fallback Size, >204800 bytes. Include external CDN images directly from inlinks; never inner-join Images:All or use SF's config-dependent Over X kB filter. Largest sizes first. |

## Duplicate review and Findings (17.2 / 18.2 / 19.2)

Follow the matching SF tab (Page Titles / Meta Description / H1), select its native Duplicate filter, then filter Indexability=Indexable. The owner's current policy excludes all known Non-Indexable candidates, including Canonicalised/noindex/etc.; Indexability Status supplies the recorded reason, not an additional eligibility condition. Missing status reasons are recorded as Unspecified. Do not treat an SF Canonicalised label as proof that Google selected that canonical or that canonical configuration is correct.

Recheck groups only inside these native candidates after filtering. A group needs at least two distinct exact URL strings (outer whitespace removed). Repeated rows for one URL do not count as two pages; an Indexable original left alone after its Non-Indexable variants are excluded is not a duplicate issue. Title/description group values use outer-whitespace trimming with exact case; H1-1 grouping is case-insensitive, preserving the previous H1 matching convention. Keep all confirmed rows in qualifying groups. Do not infer cross-page matches from All, infer missing language classifications or exclude target pages here.

Nonempty Duplicate exports need usable Indexability per candidate. Unknown/missing values and blank eligible identities/content leave evidence gaps and are not confirmed issue rows. With no confirmed groups this is Human Check; known groups remain X alongside gaps. A valid header-only issue export still means zero native candidates; missing/invalid exports remain Human Check.

Findings must state the named SF tab, Duplicate → Indexable route, native row count (unknown if export unavailable), Indexable row count, excluded Non-Indexable count/reasons, group-review removals and final confirmed row count. Include unknown-evidence limitations. On X add a reminder that Chinese/English site versions were not automatically excluded and require human review; do not claim language detection or automatically waive multilingual duplicates. If both language versions are Indexable and share the checked value, they remain flagged. The check's duplicate_review metadata records counts plus excluded/unknown URL records; raw exports remain intact. These are sample/crawl-based decisions, not Google index verification.

## Targets and evidence

Inspect the existing SF session's native Missing filters first. An explicitly identified target inventory in current task/session records is usable; record its source and exact URL values. SF's Missing filter does not itself identify the business's target pages. Without an explicit list apply no exclusions and disclose this on 17.1/18.1. Match exact URL strings with outer whitespace removed; keep case, query and trailing slash differences. Do not exclude targets from duplicates, widths, H1 or images.

An available, valid header-only issue report means zero matches in the supplied sample. Missing, malformed, ambiguous CSVs, missing required columns and blank issue identities produce an item-specific evidence gap. Page Titles:All must contain data or the run fails. All-based thresholds need explicit Indexability and usable metric/text columns; unknown Indexability/numeric values cannot pass.

No captured images across image reports makes both image checks Human Check. Available image/alt records can establish capture even with empty Images:All. Missing Alt report makes 20.1 unknown unless known rows establish failure. Missing/invalid/zero sizes make 20.2 incomplete. Keep known oversize rows and X while disclosing remaining unknown sizes. Do not treat some known image sizes as complete coverage of all images.

Results: √ = usable evidence with no issue; X = one or more confirmed rows; Human Check = no confirmed rows and an evidence gap. No automatic NA for absent exports or disabled image crawling. Known X survives gaps. Images have row_count, unique_assets and affected_pages in findings.json. Scope means the supplied export sample, never a promise that SF captured the entire site.

Template-aligned display does not change these decisions. 18.3 Pixel Width shows the actual Meta Description 1 Pixel Width from the same SF row, retained separately as pixel_widths while JSON rows still hold character counts. Missing pixel widths create display_gaps and blank cells, not a fabricated count or an additional judgment requirement. Template prose about 880px, 100KB or excluding WebP is not adopted.
