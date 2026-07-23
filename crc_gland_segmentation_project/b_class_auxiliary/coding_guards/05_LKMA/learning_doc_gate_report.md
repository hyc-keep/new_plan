# Learning Doc Gate Report

## 1. 输入文件
- `project_root`: `/home/featurize/work/Paper/crc_gland_segmentation_project`
- `precheck_guard`: `b_class_auxiliary/coding_guards/05_LKMA/Pre-check Guard.md`
- `post_qc_guard`: `b_class_auxiliary/coding_guards/05_LKMA/Post-QC Guard.md`

## 2. 检查范围
- 检查 Post-QC `实际创建/修改文件` 表中的正式对象是否进入学习型说明文映射。
- 检查 Pre-check `预期文档映射` 与 Post-QC `对象-说明文映射回填` 是否前后对齐。
- 检查说明文路径是否真实存在，且是否位于 `reports/stage_reports/implementation_tracking/` 下。
- 检查 `append_version` 是否真的落到 `## 版本更新记录`。
- 检查当某个阶段本轮新增学习型说明文或重写验收入口时，对应 `README.md` 与 `implementation_status.md` 是否同步更新。
- 检查说明文体量是否达到当前规程的最小要求（核心脚本文档 `120` 行，工具脚本文档 `80` 行，正式资产文档 `60` 行，薄配置资产 `50` 行，验收说明文 `80` 行）。
- 检查脚本说明文、资产说明文、验收说明文是否缺少当前规程要求的关键章节骨架。
- 检查阶段入口 `README.md` / `implementation_status.md` 是否也达到最小正文、口语化解释、诚实边界和联读收口要求。
- 检查 7 问是否以显式结构或强信号真正落盘，而不是只靠零散关键词蹭命中。
- 检查说明文中的反引号路径是否能解析到真实存在的文件，而不是只写一个看起来像路径的字符串。
- 检查说明文是否包含数值级物理证据、验证步骤和设计取舍说明。
- 检查关键章节是否真的写入了非占位、非空壳的正文，而不是只有标题或几行模板残留。
- 检查脚本说明文是否保留了明显的口语化解释信号，避免只剩审计术语和 checklist。
- 检查脚本说明文是否至少命中融合版示范稿中的多组风格信号，而不是只有一两句口语化点缀。
- 检查资产说明文和验收说明文是否也保留最小口语化解释、联读收口和误判风险提示，避免只有结构过关。
- 检查说明文是否保留最小视觉层次信号：标题层次、短段落留白、表格或编号链，避免整篇退化成密集长段落。
- 对脚本说明文额外检查 `## 结构化溯源卡片` 是否存在、字段是否完整、路径是否真实存在。
- 检查 Post-QC `## 3. 协议级质检结果` 与 `## 4.3 学习型说明文人工审稿回填` 是否一致，并在需要时强制要求人工终审回填。
- 检查人工终审是否回填 `学习型说明文人工审稿清单.md`、`TCGA原始标杆对齐清单.md` 与真实 TCGA 原始文档对照锚点。
- 说明: 本报告会检查人工终审是否真正落盘，但它仍不能替代人工阅读本身。

## 3. 结论
- `learning_doc_gate_status`: `partial`
- `tcga_reference_mode`: `external_tcga_required`
- `external_tcga_reference_status`: `not_declared`
- `internal_template_paths`: `['reports/stage_reports/implementation_tracking/01_数据协议/当前阶段为什么能pass以及下一步怎么看.md', 'reports/stage_reports/implementation_tracking/02_UNet流程验证/当前阶段为什么能pass以及下一步怎么看.md', 'reports/stage_reports/implementation_tracking/03_UNet稳定性/当前阶段为什么能pass以及下一步怎么看.md']`
- `conditional_requirements`: `['正式 TCGA 原始资料恢复可访问后仍需完成真实人工复核（当前仅记录 conditional_notice）', 'fallback 下仍检查对象映射、说明文存在性、基本路径以及代码/配置/正式结果锚点', '内部模板不代表 TCGA 原始证据，不能声称外部 TCGA 已访问']`
- `learning_doc_gate_mode`: `external_tcga_required`
- `tcga_external_blocking`: `true`
- `conditional_notice`: 内部阶段模板模式下，TCGA 外部资料不可访问仅作透明记录；被降级的文档深度/风格/外部对照项不会阻断，但对象、映射、文件存在性和真实项目证据硬错误仍会阻断。

## 4. 检查摘要

- `映射与同步`: `partial=4`

## 5. 详细结果
- [partial] 对象 `reports/tables/lkma_per_seed_summary.csv` 未在 Pre-check 映射表中提前声明。
- [partial] 对象 `reports/tables/baseline_vs_lkma_mean_std.csv` 未在 Pre-check 映射表中提前声明。
- [partial] 对象 `reports/tables/lkma_cost_comparison.csv` 未在 Pre-check 映射表中提前声明。
- [partial] 对象 `reports/tables/lkma_stage_manifest.csv` 未在 Pre-check 映射表中提前声明。
