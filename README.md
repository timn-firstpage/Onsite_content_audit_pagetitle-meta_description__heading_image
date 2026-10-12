# Onsite Content Audit — Page Titles / Descriptions / H1 / Images

<p align="center"><img src="assets/onsite-audit-cover.png" alt="Onsite audit cover showing HTTPS security, website inspection, crawl connections, hostname redirects, and an audit report" width="640"></p>

独立的 **`onsite-audit-content`** skill，检查 **17.1–20.2**。基于你已跑通的 Multica 提取逻辑整理，与 HTTPS、robots、sitemap 系列共用 SF session、saved crawl、配置和运行目录。当前版本 **1.0.2**。

## 审核范围

| Item | 检查 | 原生 SF 数据 |
| --- | --- | --- |
| 17.1 | 缺 Title，排除已明确的 target pages | Page Titles:Missing |
| 17.2 | Title 重复 | Page Titles:Duplicate |
| 17.3 | Title >580px，仅 Indexable | Page Titles:All |
| 17.4 | 多个 Title | Page Titles:Multiple |
| 18.1 | 缺 Description，排除已明确的 target pages | Meta Description:Missing |
| 18.2 | Description 重复 | Meta Description:Duplicate |
| 18.3 | Description **>155 字符**，仅 Indexable | Meta Description:All |
| 19.1 | 缺 H1；关键词优化需人工判断 | H1:Missing |
| 19.2 | 跨页面 H1 重复，剔除纯同页重复 | H1:Duplicate |
| 19.3 | 同页多个 H1 | H1:Multiple |
| 20.1 | 缺 Alt/空 Alt 的图片引用 | Missing Alt Attribute & Text Inlinks |
| 20.2 | 图片 >204800 bytes，包含外部 CDN | All Image Inlinks |

17.1/18.1 先去当前 SF session 的原生 Missing filter 找出页面。只有已有任务/session 明确标识的 target 清单才排除；没有清单就检查所有 Missing 行，并注明未应用排除。不按缺失结果反推 target pages。装饰图可用空 Alt，需人工排除；行数、独立图片数、受影响页面数分开。

## 判定矩阵（Judgment Matrix）

下面描述当前脚本实际执行的规则，判断范围是所提供的 SF 导出样本。各项独立判断：**有确认问题行 → X；没有确认问题但有证据缺口 → Human Check；证据可用且没有问题 → √**。有问题同时缺证据时仍为 X，并记录未确认范围。当前脚本不自动生成 NA；缺导出或没抓到图片不能当作不适用。

| Item | 怎么检查 | 结果判断 |
| --- | --- | --- |
| **17.1 Does each URL have a title? (excluding target pages)** | 读取 SF **Page Titles:Missing**，只排除任务／session 中明确提供的 target URL。URL 去掉首尾空白后精确匹配，保留大小写、query 和结尾斜线。 | **√**：有效 Missing 导出排除后没有记录。**X**：仍有缺 Title 的 URL。**Human Check**：导出缺失、无效或问题行 Address 为空。没有 target 清单时不排除，注明检查全部 Missing 行；清单缺失本身不使结果变为 Human Check。 |
| **17.2 Is the site free of any page title duplication?** | 读取 SF **Page Titles:Duplicate**，按 Title 1 分组显示，较大组在前；不从 All 自行重算重复。 | **√**：有效原生 Duplicate 导出无问题行。**X**：有重复 Title 记录。**Human Check**：缺导出、必要字段缺失，或 Address／Title 1 为空。 |
| **17.3 Are page titles using the 580 pixel maximum width effectively?** | 读取 **Page Titles:All**，仅检查 `Indexability=Indexable`；使用 **Title 1 Pixel Width**，按宽度降序列出超限页面。 | **√**：所查可索引页面均 ≤580px，且没有证据缺口。**X**：至少一页 **>580px**；恰好 580px 不超限。**Human Check**：无确认超限，但缺字段、Address 为空、Indexability 未知或可索引页面宽度无效。本项只判断超宽，不判断标题过短或关键词质量。 |
| **17.4 Are there multiple page titles** | 读取 SF **Page Titles:Multiple**，保留 Address、Title 1、Title 2。 | **√**：有效 Multiple 导出无问题行。**X**：有同页多个 Title 的记录。**Human Check**：缺导出、缺字段，或问题行 Address／Title 1／Title 2 为空。 |
| **18.1 Does each URL have a description? (excluding target pages)** | 读取 SF **Meta Description:Missing**，应用与 17.1 相同的明确 target URL 排除清单。 | **√**：有效 Missing 导出排除后没有记录。**X**：仍有缺 Description 的 URL。**Human Check**：缺导出、无效导出或问题行 Address 为空。没有 target 清单时检查全部 Missing 行，并注明未排除。 |
| **18.2 Is the site free of any meta description duplication?** | 读取 SF **Meta Description:Duplicate**，按 Meta Description 1 分组显示，较大组在前；不从 All 自行重算重复。 | **√**：有效原生 Duplicate 导出无问题行。**X**：有重复 Description 记录。**Human Check**：缺导出、缺字段，或 Address／Meta Description 1 为空。 |
| **18.3 Are meta descriptions using the 155 character limit effectively?** | 读取 **Meta Description:All**，仅检查 `Indexability=Indexable`；直接计算导出文本的 Unicode 字符数，不裁掉空白，不使用字节数或旧版 880px。 | **√**：所查可索引页面均 ≤155 字符，且没有证据缺口。**X**：至少一页 **>155 字符**；恰好 155 不超限。**Human Check**：无确认超限，但 All 没有数据、缺字段、Address 为空或 Indexability 未知。本项不判断描述过短或文案质量；缺描述另见 18.1。 |
| **19.1 Do all pages contain a single, keyword-optimised H1?** | 读取 SF **H1:Missing**。当前自动逻辑只检查缺失；多个 H1 由 19.3 检查，关键词优化由人工判断。 | **√**：有效 Missing 导出无问题行，仅表示未发现缺 H1。**X**：有缺 H1 的 URL。**Human Check**：导出缺失、无效或问题行 Address 为空。√ 不代表已验证关键词优化或每页恰好一个 H1。 |
| **19.2 Are there H1 duplicates?** | 从 SF **H1:Duplicate** 开始；只有同页 H1-1 与 H1-2 去首尾空白后相同，且该 H1-1 在原生重复集合中只出现一次时，才剔除该行。出现次数按去首尾空白、不区分大小写计数；跨行共享仍保留。 | **√**：有效 Duplicate 导出在剔除后无问题行。**X**：仍有重复 H1 记录。**Human Check**：缺导出、缺 Address／H1-1／H1-2 列，或问题行 Address／H1-1 为空。纯同页多个 H1 仍由 19.3 检查。 |
| **19.3 Are there multiple H1s tags in a single page?** | 读取 SF **H1:Multiple**，保留 Address、H1-1、H1-2。 | **√**：有效 Multiple 导出无问题行。**X**：有同页多个 H1 的记录。**Human Check**：缺导出、缺字段，或问题行 Address／H1-1／H1-2 为空。 |
| **20.1 Do images contain alt text** | 读取 **Missing Alt Attribute & Text Inlinks**，列出 Source 页面和 Destination 图片。缺 Alt 属性及空 `alt=""` 都会入表；同一图片在多个页面出现可产生多行。 | **√**：有效 Alt 问题导出无记录，且图片导出证明已抓到图片。**X**：有缺失／空 Alt 的引用记录；当前脚本不会自动豁免装饰图片，修复前需人工确认用途。**Human Check**：缺 Alt 导出、引用身份字段无效，或全部图片导出都没有抓到图片。 |
| **20.2 Oversized images** | 从 **All Image Inlinks** 读取 Size (Bytes)，没有该列时使用 Size；包含外部 CDN 图片，不与 Images:All 做内连接。核对 Images:All／Alt 中已观察图片是否有已知 inlink 大小，按大小降序列出。 | **√**：有可用图片大小观察，已观察图片的大小证据完整，且均 ≤204800 bytes。**X**：至少一张 **>204800 bytes（200KiB）**；恰好等于阈值不超限。**Human Check**：无确认超限，但缺大小列、大小无效／为 0、没有可用引用，或已观察图片缺对应大小。只验证已观察范围，不保证动态／未抓取图片已覆盖。 |

有效、只有表头的 **Missing／Duplicate／Multiple／Alt 问题导出**可以表示零问题。All 导出另有要求：**Page Titles:All 必须可读且有数据，否则整个运行停止**；Meta Description:All 没有数据时 18.3 为 Human Check。文件匹配不唯一、CSV 无效或必要字段缺失均记录证据缺口。17.3／18.3 明确排除 Non-Indexable 行；其余项目沿用原生问题 filter 的结果，不额外添加统一 Indexable 筛选。

## 与 onsite 系列衔接

- [SF shared config](https://github.com/timn-firstpage/On-_site_SF_shared_config)：新 crawl 准备、手动 Start、saved-crawl 交接。
- [HTTPS](https://github.com/timn-firstpage/Onsite_audit_HTTPS_related_checking)：9.x，由独立模块负责。
- [Robots](https://github.com/timn-firstpage/Onsite_robot_txt_checking)：10.x，由独立模块负责。
- [Sitemap](https://github.com/timn-firstpage/Onsite_audit_sitemap_check) 负责 11.x；本模块不执行 canonical、HTTPS、robots、sitemap、分页和 PageSpeed。

使用同一份 resolved config 的 `site/source/mcp/budget/cache/output`，添加 `checks.content` 和 `content`。同一个 SF 实例串行操作，适用导出只取一次、共用预算；已有 saved crawl 不重新加载配置、不自动重爬。[详细约定](references/shared-config.md)

已提供 [配置衔接组件](references/config-component.md)：agent 调用现有 `sf-shared-config` 完成必要准备和交接，Python 的 `scripts/shared_config.py` 读取共用运行 JSON。优先 `--config`，未指定时使用可选 `ONSITE_AUDIT_CONFIG`；仅在内存补 content 默认值。共享 run 的 `sf-handover.json` 自动记录到 manifest，也可通过 `--sf-handover` 指定；它是来源记录，不是审核通过证明。原配置、交接文件和累计预算不修改。这个 shared skill 仓库中的 SF profile 与运行 JSON 是两种文件，不把 GitHub URL 当文件路径。

本模块输出独立报告，不修改整份 onsite 模板。若将来合并 master workbook，由总流程一次性处理历史 D/E 列及各模块映射；本模块只提供十二项 findings。没有旧版 Begin/Review/template 问答或模板下载。

## 运行

Python **3.10+**，Windows/macOS/Linux。当前运行脚本不调用 SF CLI，也不固定 Mac 路径或 MCP 端口。配置 SF MCP 和准备 Python 是独立工作，导入 skill 不会自动安装它们。

```bash
python -m venv .venv
# Windows: .venv/Scripts/python.exe；macOS/Linux: .venv/bin/python
python -m pip install -r requirements.txt
```

上面的 python 使用已激活虚拟环境的解释器，或改为其实际路径/AUDIT_PYTHON。

复制 config.template.json 到本次 run/config.json，填写 `site.start_url`、`source.export_directory`、`output.audit_date` 或 timezone。相对路径从 config 文件目录解析。

```bash
python scripts/onsite_checklist.py --config <run/config.json> --run-dir <shared-run>
```

不使用配置的示例：

```bash
python scripts/onsite_checklist.py --exports-dir <sf-csv-folder> \
  --site-url https://example.com/ --site-name Example \
  --date 2026-10-12 --run-dir <unique-run>
```

target 清单通过 config 的 content.target_urls、content.target_urls_file 或 `--target-urls` 指定；文件是 Address/URL 表头 CSV 或每行一个 URL 的文本。阈值固定为本版本的 580px / 155 字符 / 200KiB。

只有 saved crawl 没有导出时，agent 用已验证 SF 能力打开并导出；没有 reader 就手动 File → Open 后提供[这些 CSV](references/exports.md)。Python 不解析 `.seospider` 二进制、不启动 crawl。至少 Page Titles:All 有有效数据才生成报告；其他缺失字段按项 Human Check，不伪造全通过。

## 输出

`<shared-run>/content/`：

- `{site name}_content_audit_{YYYY-MM-DD}.xlsx`：Checklist + 仅结果为 X 的问题明细 tab（最多 12 个）。
- findings.json：十二项结果与全部确认问题行，供总流程复用。
- manifest.json：来源、哈希、阈值、排除、计数和缺口。
- raw/：可选完整 CSV 归档，默认开启。
- run-status.json：XLSX 读回验证成功后写 complete。

Checklist：Item No. / Item Name / Initial Check / Findings / Instruction。结果 **√ / X / Human Check**；有确认问题且同时缺证据仍 X，明确缺口。Checklist 始终保留十二项；仅 X 创建对应问题明细 tab，√ 和 Human Check 不创建空白明细 tab，全通过时只有 Checklist。明细沿用原来的 JSON headers/rows 和各项列结构，第 1 行表头、第 2 行数据。findings.json 仍保留全部十二项，空问题数组及证据缺口不删除。[完整输出契约](references/output-contract.md)

不覆盖旧文件；同日更新使用新的 run 目录。日期按用户时区或明确 audit_date。所有客户资料在 ignored runs/，不要提交 GitHub。英文原始 checklist 问题保留，Findings/Instruction 支持 zh/en。

## Multica / 本地 agent

仓库根目录就是 SKILL.md，可以从本仓库 URL 导入：
https://github.com/timn-firstpage/Onsite_content_audit_pagetitle-meta_description__heading_image

若 URL 导入不包含所需 supporting files，打包后通过 Import from local 上传 ZIP：

```bash
python scripts/package_skill.py --output dist/onsite-audit-content.zip
```

包根目录直接包含 SKILL.md、references、scripts、requirements.txt、config.template.json 和 agents。不是 GitHub 整仓库 ZIP。可选 agent 指令见 references/multica-agent-instructions.md；替换旧 canonical 扩展版指令，避免冲突。导入后绑定 agent，并确认运行机的 Python、openpyxl 及真实 SF 工具可用。代码包不会带走另一台机器的 Python/端口配置。

本地安装可把此 repo 作为名为 onsite-audit-content 的目录链接到客户端支持的 skills 目录；保持 Git 仓库为唯一源。本次整理不自动修改全局 skills。Multica Update from source 会替换远端导入内容；今后在 Git 分支修改、验证并提交后再更新。

## 验证与来源

```bash
python -m unittest discover -s tests -v
```

CI 在 Windows/Linux、Python 3.10/3.12 上运行离线测试并检查导入包。测试覆盖原生过滤、H1 碰撞、阈值、target 排除、缺字段、CDN 图片、配置/站点/时区、禁止覆盖和 Excel 字面文本。脚本读回验证每个单元格与 tab。

提取设计来自 [FirstPage 原始 skill](https://github.com/firstpage-seo/onsite-checking-AI-workflows/tree/main/.claude/skills/onsite-canonical-meta-images-extraction-multica) 和仓库所有者提供的 Multica 修改版。保留成熟判断，拆除其他审核/整表 Review，并按所有者确认将 18.3 改成字符数。当前实现没有复制客户数据或上游 Excel 模板；[版本记录](CHANGELOG.md)说明有意变化。

本地离线测试和合成 CSV→XLSX 可以验证数据处理；它们不证明真实 Multica 导入、SF session 导出、动态图片抓取完整或 macOS runtime 已验证。正式使用时按 session 交接记录确认实际范围。
