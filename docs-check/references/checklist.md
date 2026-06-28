# docs-check 完整检查清单

> 逐项可勾选。每项标注：✅ 通过 / ❌ 必须修 / ⚠️ 建议。

## A. 根入口

- [ ] `AGENTS.md` 存在且非空
- [ ] `AGENTS.md` 顶部含「本仓库遵循 docs/ 目录规范，开始任务前必须先读 docs/README.md」声明（落地的第一道闸）
- [ ] `CLAUDE.md` 存在且引用 `AGENTS.md`
- [ ] `GEMINI.md` 存在且引用 `AGENTS.md`
- [ ] `README.md` 存在且非空（给人看的入口）
- [ ] 存在项目原生命令入口，含 docs 结构校验、AI 入口校验、ADR 创建入口：`package.json` scripts / `Makefile` / `justfile` / `Taskfile.yml` / `scripts/docs/*.sh` 任一可用
- [ ] `.env.example` 存在（只占位值）
- [ ] `.gitignore` 排除密钥 / 本地数据 / 日志 / 构建产物

## B. 目录齐全性（十一个全必选）

- [ ] `docs/00-context/`
- [ ] `docs/10-product/`
- [ ] `docs/20-architecture/`
- [ ] `docs/30-engineering/`
- [ ] `docs/40-operations/`
- [ ] `docs/50-planning/`
- [ ] `docs/60-marketing/`
- [ ] `docs/70-research/`
- [ ] `docs/80-dev/`
- [ ] `docs/90-ui-ux/`
- [ ] `docs/99-archive/`

> 缺一即 ❌。`80-dev/` 是编码过程临时问题分析、方案和验证记录的工作区，不再空置。

## C. 每目录 README 三段式

对每个目录的 `README.md` 检查是否含三段：

| 目录 | 目标(Purpose) | 放什么(Includes) | 不放什么+去向(Excludes) |
| --- | --- | --- | --- |
| 00-context | ☐ | ☐ | ☐ |
| 10-product | ☐ | ☐ | ☐ |
| 20-architecture | ☐ | ☐ | ☐ |
| 30-engineering | ☐ | ☐ | ☐ |
| 40-operations | ☐ | ☐ | ☐ |
| 50-planning | ☐ | ☐ | ☐ |
| 60-marketing | ☐ | ☐ | ☐ |
| 70-research | ☐ | ☐ | ☐ |
| 80-dev | ☐ | ☐ | ☐ |
| 90-ui-ux | ☐ | ☐ | ☐ |
| 99-archive | ☐ | ☐ | ☐ |

> 缺「不放什么 + 指明去向」= 边界没写清，记 ⚠️（影响分类准确性）。

## C2. 80-dev 工作区治理

- [ ] `docs/80-dev/README.md` 明确 `30-engineering/` 是长期工程知识，`80-dev/` 是开发现场草稿区。
- [ ] `docs/80-dev/README.md` 要求草稿文件以 `YYYY-MM-DD-` 开头，例如 `2026-06-15-parser-selector 的方案.md`。
- [ ] `docs/80-dev/README.md` 明确每日按日期前缀复盘：架构影响抽到 `20-architecture/`，长期工程实践抽到 `30-engineering/`，阶段推进/验收抽到 `50-planning/`，无复用价值的过程留待归档或删除。
- [ ] `docs/80-dev/` 下的 Markdown 草稿文件名符合 `YYYY-MM-DD-*.md`；`README.md` 除外。

## D. 必选文件非空且有效

> 非空指：有 frontmatter + 标题 + 实质内容，不是 TODO 占位空壳。

- [ ] `00-context/project-brief.md`
- [ ] `00-context/requirements.md`
- [ ] `00-context/constraints.md`（★ 最关键，须有 Technology/Security/Architecture 实质约束）
- [ ] `10-product/workflows.md`
- [ ] `10-product/acceptance-criteria.md`
- [ ] `20-architecture/overview.md`（★ 最好含一张架构图）
- [ ] `30-engineering/setup.md`
- [ ] `30-engineering/commands.md`
- [ ] `30-engineering/ai-coding-guide.md`（★ 须有 Before/Verification/Boundaries/Checklist 四段）
- [ ] `40-operations/environments.md`
- [ ] `40-operations/runbooks.md`
- [ ] `50-planning/roadmap.md`
- [ ] `50-planning/changelog.md`
- [ ] `60-marketing/positioning.md`
- [ ] `60-marketing/release-notes.md`
- [ ] `70-research/references.md`
- [ ] `70-research/alternatives.md`
- [ ] `90-ui-ux/screens.md`
- [ ] `90-ui-ux/interaction-patterns.md`

## E. frontmatter 齐全

- [ ] 「当前有效」文档顶部带 `status / owner / last-reviewed`
- [ ] `99-archive/` 内文档带 `status: historical` 或 `deprecated`，并声明 `superseded-by`（指向取代者）
- [ ] `last-reviewed` 不是未来日期；超 6 个月未更新记 ⚠️（建议 review 或降级）

## F. ADR 规范（docs/20-architecture/decisions/）

- [ ] 每个文件命名 `NNNN-kebab-title.md`（4 位序号 + kebab）
- [ ] 序号连续无跳号、无重复
- [ ] 每个文件 frontmatter 含 `adr / status / date`（`status`: proposed|accepted|deprecated|superseded）
- [ ] `status: superseded` 的 ADR 有 `superseded-by` 指向新 ADR
- [ ] `docs/templates/adr.md` 存在（供 `docs:new-adr` 使用）

## G. 分类正确性（抽样 3–5 篇）

对抽查的每篇文档：
- [ ] 正文内容符合所在目录 README 的「放什么」
- [ ] 不符合所在目录 README 的「不放什么」
- [ ] 若放错，报告给出「应移至 XX 目录」
- [ ] `80-dev/` 中已确认或已实施且影响系统边界、数据模型、接口契约、部署/运行拓扑、核心流程的结论，已在当日收尾时抽取同步到 `20-architecture/` 或 ADR；纯实现细节没有硬塞进架构目录。

## 报告汇总公式

- 总项数 = A(8) + B(11) + C(33) + C2(4) + D(19) + E(3) + F(5) + G(抽样数×4)
- 达标率 = ✅ 项 / 总项数
- 阻断合规 = 任何 ❌（尤其 B 目录缺失、D 关键文件空壳、A 声明缺失）
