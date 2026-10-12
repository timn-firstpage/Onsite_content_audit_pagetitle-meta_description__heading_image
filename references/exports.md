# Screaming Frog CSV contract

Export these native tabs/filters from the selected existing crawl:

```text
Page Titles:All
Page Titles:Missing
Page Titles:Duplicate
Page Titles:Multiple
Meta Description:All
Meta Description:Missing
Meta Description:Duplicate
H1:Missing
H1:Duplicate
H1:Multiple
Images:All
```

Bulk exports:

```text
Images:Images Missing Alt Attribute & Text Inlinks
Images:All Image Inlinks
```

No Canonicals, Security, Pagination, Response Codes, PageSpeed or sitemap exports are needed. H1:All is not needed because duplicates must come from the native filter. Keep all native fields, not only the minimal fields below. UTF-8 with optional BOM, comma delimiter, header first, standard CSV quoting. Valid issue reports with zero matches retain their headers. Empty/nonempty issue rows are not the same as absent/unreadable files.

| Report | Fields used |
| --- | --- |
| Page Titles:All | Address, Indexability, Title 1, Title 1 Pixel Width |
| Page Titles:Missing | Address |
| Page Titles:Duplicate | Address, Title 1 |
| Page Titles:Multiple | Address, Title 1, Title 2 |
| Meta Description:All | Address, Indexability, Meta Description 1 |
| Meta Description:Missing | Address |
| Meta Description:Duplicate | Address, Meta Description 1 |
| H1:Missing | Address |
| H1:Duplicate / Multiple | Address, H1-1, H1-2 |
| Images:All | Address (capture evidence) |
| Missing Alt inlinks | Source, Destination |
| All Image Inlinks | Source, Destination, Size (Bytes) or Size |

Reports sit in one directory. Match native filename keywords, e.g. page_titles_missing.csv, meta_description_duplicate.csv, h1_multiple.csv, images_all.csv, images_missing_alt_attribute_and_text_inlinks.csv, all_image_inlinks.csv. Multiple matching old/new files are ambiguous: separate them by run or supply the correct directory. Preserve full export row counts/truncation context in the shared handover; model previews and SF MCP summaries do not substitute for files.

After exporting inspect Page Titles:All for nonempty records, intended site and crawl identity. CSV headers do not prove session completeness. Match source timestamp/scope against shared sf-handover.json and manifest; the local script cannot independently verify SF session metadata or whether a tool truncated its export.
