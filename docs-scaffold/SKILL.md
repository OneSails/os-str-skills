---
name: docs-scaffold
description: >
  一键初始化「AI 友好 docs 目录标准」的完整结构：根目录三件套（AGENTS.md/CLAUDE.md/GEMINI.md）+
  docs/ 十一个必选目录 + 每目录 README（三段式目标说明）+ 必选文件骨架 + docs/templates/adr.md +
  按项目类型固化原生命令入口（docs:check / ai:check / docs:new-adr）。建完即跑校验自证合规。
  Use when user asks to "初始化文档结构", "建 docs 目录", "按标准建文档", "scaffold docs",
  "初始化十目录", "初始化十一目录", "docs 脚手架", or mentions "docs-scaffold" / "AI 友好 docs".
---

# docs-scaffold — AI 友好 Docs 标准结构脚手架

> 把《AI 编码友好型 Docs 目录结构与命令入口固化方案》（v5.1）一次性落地到任意项目根目录。**十一个目录全必选**，照抄即用。
>
> 判断标准始终只有一个：AI 或新成员能否在 3 分钟内自主找到需求、约束、命令与禁止事项，并把新内容放对目录。

## 这个 Skill 做什么

在项目根创建标准约定的全部文件与目录，让上述判断标准从结构上成立，并按项目类型固化 `docs:check` / `ai:check` 校验闸门。建完即自证合规。

## Critical Rules（必须遵守）

1. **在项目根执行**：必须有 `.git`、`package.json`、`pyproject.toml`、`go.mod`、`Cargo.toml`、`Makefile`、`justfile`、`Taskfile.yml` 等根标志之一。不在根则先向用户确认目标目录，绝不盲目在子目录建。
2. **幂等、不覆盖**：已存在的同名文件**跳过**并报告，只创建缺失项。绝不破坏用户已有内容。
3. **一次建齐**：根入口三件套 + `docs/README.md` + 十一个目录 + 每目录 README + 全部必选文件骨架 + `docs/templates/adr.md`，缺一不可（标准要求 `80-dev/` 用于编码过程临时问题分析与方案沉淀）。
4. **目录 README 必须三段式**：每个一级目录的 README 只写「目标（Purpose）/ 放什么（Includes）/ 不放什么（Excludes）+ 指明去向」，正文内容绝不写进 README。
5. **区分 engineering 与 dev**：`30-engineering/` 是长期有效的工程手册；`80-dev/` 是编码现场草稿区。临时分析沉淀成长期规则才进入 `30-engineering/`。
6. **80-dev 日期前缀**：`80-dev/` 下草稿文件必须以 `YYYY-MM-DD-` 开头，例如 `2026-06-15-parser-selector 的方案.md`，便于每日 AI 自动归档、抽取和清理。
7. **按项目类型固化校验**：必须优先使用项目已有命令体系，不为 docs 标准强行引入新 runner。Node 用 `package.json` scripts；已有 `Makefile`/`justfile`/`Taskfile.yml` 则沿用；Python/Rust/Go 项目若无统一 runner，使用 `scripts/docs/*.sh` 兜底。创建可执行脚本 `scripts/docs/new-adr.sh`。
8. **必选文件非空**：每个骨架文件至少含 YAML frontmatter（`status / owner / last-reviewed`）+ 标题 + 占位提示，杜绝「touch 空文件」的虚假合规。
9. **建完即验**：最后运行刚固化的项目原生 `docs:check` 与 `ai:check` 入口，两绿才算完成。

## 执行流程

### Step 1 — 定位与盘点
- 确认当前目录是项目根（含根标志文件）。
- 扫描已存在的 `AGENTS.md / CLAUDE.md / GEMINI.md / README.md / docs/`，记录已存在项（后续 Step 中跳过）。

### Step 2 — 根目录入口（仅缺失才建）
按 `references/templates.md`「根入口模板」创建：
- `AGENTS.md`（canonical AI 指令源；**顶部第二行必须**写「本仓库遵循 docs/ 目录规范，开始任务前必须先读 docs/README.md」——这是落地的第一道闸）。
- `CLAUDE.md`、`GEMINI.md`（各一行桥接，引用 AGENTS.md）。
- `README.md`（给人：价值 + 快速开始 + 命令 + 文档入口）。
- `.env.example`（只放占位值）、`.gitignore`（补密钥 / 本地数据 / 日志 / 构建产物）。

### Step 3 — docs/README.md
按模板创建，含 `Read First` 固定读取顺序：`AGENTS.md → 00-context/constraints.md → 00-context/project-brief.md → 20-architecture/overview.md → 30-engineering/commands.md → 30-engineering/ai-coding-guide.md`。

### Step 4 — 十一个目录 + 各 README（三段式）
对照 `references/directory-tree.md` 的完整目录树，创建十一个目录，每个放一个三段式 README（内容取自 `references/templates.md`「目录 README 三段式」）。十一个目录：`00-context / 10-product / 20-architecture / 30-engineering / 40-operations / 50-planning / 60-marketing / 70-research / 80-dev / 90-ui-ux / 99-archive`。

### Step 5 — 必选文件骨架（非空）
对照 `references/directory-tree.md`「必选文件清单」，每个文件至少含 frontmatter + 标题 + 占位提示。两个重点写实的：
- `00-context/constraints.md`：硬约束骨架（Technology / Security / Architecture 三段）。
- `30-engineering/ai-coding-guide.md`：Before Any Task / Verification / Boundaries / Review Checklist 四段。

### Step 6 — 决策目录与 ADR 模板
- 建 `docs/20-architecture/decisions/`（用于 ADR，命名 `NNNN-kebab-title.md`）。
- 建 `docs/templates/adr.md`（ADR 模板，序号制 frontmatter）。

### Step 7 — 固化项目原生命令入口
按 `references/command-adapters.md` 的选择规则，优先把 `docs:check`、`ai:check`、`docs:new-adr` 合并进项目已有命令体系；没有统一 runner 时创建 `scripts/docs/check.sh`、`scripts/docs/ai-check.sh`、`scripts/docs/new-adr.sh` 作为兜底入口（全部 `chmod +x`）。

### Step 8 — 自证合规
```bash
# 运行项目原生命令入口，例如：
npm run docs:check && npm run ai:check
make docs-check ai-check
just docs-check && just ai-check
task docs:check && task ai:check
scripts/docs/check.sh && scripts/docs/ai-check.sh
```
两绿则完成；有红则按报错回到对应 Step 补齐。

## 完成判据

- 十一个目录齐全，各有非空三段式 README。
- `80-dev/README.md` 明确 engineering/dev 生命周期区别、日期前缀命名、每日收尾抽取规则。
- 必选文件全部非空，关键文件 frontmatter 齐全。
- 项目原生命令入口中的 `docs:check` + `ai:check` 通过。
- `AGENTS.md` 顶部含「遵循 docs/ 目录规范、先读 docs/README.md」的强制声明。

## 详细模板

文件骨架、目录树见 `references/templates.md` 与 `references/directory-tree.md`；项目类型命令适配见 `references/command-adapters.md`——**按需读取**，避免常驻上下文（践行本标准倡导的最小上下文原则）。
