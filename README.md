# Onsite Content Audit — Page Titles / Descriptions / H1 / Images

独立的 **`onsite-audit-content`** skill，检查 **17.1–20.2**。基于你已跑通的 Multica 提取逻辑整理，与 HTTPS、robots、sitemap 系列共用 SF session、saved crawl、配置和运行目录。当前版本 **1.0.0**。

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

## 与 onsite 系列衔接

- [SF shared config](https://github.com/timn-firstpage/On-_site_SF_shared_config)：新 crawl 准备、手动 Start、saved-crawl 交接。
- [HTTPS](https://github.com/timn-firstpage/Onsite_audit_HTTPS_related_checking)：9.x，由独立模块负责。
- [Robots](https://github.com/timn-firstpage/Onsite_robot_txt_checking)：10.x，由独立模块负责。
- [Sitemap](https://github.com/timn-firstpage/Onsite_audit_sitemap_check) 负责 11.x；本模块不执行 canonical、HTTPS、robots、sitemap、分页和 PageSpeed。

使用同一份 resolved config 的 `site/source/mcp/budget/cache/output`，添加 `checks.content` 和 `content`。同一个 SF 实例串行操作，适用导出只取一次、共用预算；已有 saved crawl 不重新加载配置、不自动重爬。[详细约定](references/shared-config.md)

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

- `{site name}_content_audit_{YYYY-MM-DD}.xlsx`：Checklist + 12 个问题明细 tab。
- findings.json：十二项结果与全部确认问题行，供总流程复用。
- manifest.json：来源、哈希、阈值、排除、计数和缺口。
- raw/：可选完整 CSV 归档，默认开启。
- run-status.json：XLSX 读回验证成功后写 complete。

Checklist：Item No. / Item Name / Initial Check / Findings / Instruction。结果 **√ / X / Human Check**；有确认问题且同时缺证据仍 X，明确缺口。明细只列确认问题，无问题保留表头；第 1 行表头、第 2 行数据。[完整输出契约](references/output-contract.md)

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
