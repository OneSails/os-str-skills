# docs-scaffold 模板全集

> 本文件是 `docs-scaffold` 的按需参考资料：所有可直接拷贝的文件骨架、目录 README 三段式、ADR 模板、脚本。
> 来源：《AI 编码友好型 Docs 目录结构与命令入口固化方案》v5.1。
>
> **按需读取**：scaffold 时只读取当前 Step 用到的章节，无需整篇常驻上下文。

## 目录

- [1. 根入口模板](#1-根入口模板)
- [2. docs/README.md 模板](#2-docsreadmemd-模板)
- [3. 十一个目录 README 三段式](#3-十一个目录-readme-三段式)
- [4. 必选文件骨架](#4-必选文件骨架)
- [5. docs/templates/adr.md](#5-docstemplatesadrmd)
- [6. 命令入口适配原则](#6-命令入口适配原则)
- [7. scripts/docs/new-adr.sh](#7-scriptsdocsnew-adrsh)

---

## 1. 根入口模板

### AGENTS.md（canonical AI 指令源）

```markdown
# AGENTS.md - {Project Name}

> canonical AI agent guide. CLAUDE.md / GEMINI.md 引用本文件。
> 本仓库遵循 docs/ 目录规范，开始任务前必须先读 docs/README.md。

## Project
一句话说明项目。

## Tech Stack
固定技术栈与版本。

## Commands
标准启动/测试命令（按项目类型使用 npm/make/just/task/scripts 等原生命令入口）。

## Constraints
硬约束与禁止事项（详见 docs/00-context/constraints.md）。

## Security
密钥、合规、日志边界。

## Read First
docs/README.md 的读取顺序。
```

> 第二行的强制声明是落地的第一道闸——它把「遵守 docs 规范」写进 AI 看到的首句之一，执行率最高。

### CLAUDE.md（桥接）

```markdown
# CLAUDE.md

This repository uses AGENTS.md as the canonical guide. Read it first.
```

### GEMINI.md（桥接）

```markdown
# GEMINI.md

This repository uses AGENTS.md as the canonical guide. Read it first.
```

### README.md（给人）

```markdown
# {Project Name}

一句话说明项目价值。

## Quick Start
\`\`\`bash
task dev:infra   # 启动依赖（PostgreSQL / Redis 等）
task migrate     # 应用数据库迁移
task dev:api     # 启动服务
\`\`\`

## Commands
见 docs/30-engineering/commands.md，或项目原生命令入口（package.json / Makefile / justfile / Taskfile.yml / scripts/）。

## Docs
入口见 docs/README.md。
```

### .env.example（只放占位值）

```text
DATABASE_URL=postgres://user:pass@localhost:5432/db?sslmode=disable
REDIS_ADDR=localhost:6379
# 只放占位值，真实密钥绝不提交
```

### .gitignore（补齐关键项）

```text
# 密钥与本地配置
.env
*.key
*.pem

# 本地数据与日志
data/
logs/
*.log

# 构建产物
dist/
build/
```

---

## 2. docs/README.md 模板

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# Docs Index

## Project
一句话说明项目。

## Current Phase
- 当前阶段：______
- 当前重点：______
- 当前禁止：______

## Read First（AI 与新人按此顺序，不得跳读）
1. AGENTS.md
2. docs/00-context/constraints.md
3. docs/00-context/project-brief.md
4. docs/20-architecture/overview.md
5. docs/30-engineering/commands.md
6. docs/30-engineering/ai-coding-guide.md

## Directory Map
见各目录的 README.md（目标说明）。
```

---

## 3. 十一个目录 README 三段式

> 通用三段式骨架：`## 目标（Purpose）` / `## 放什么（Includes）` / `## 不放什么（Excludes）`。
> 「不放什么 + 指明去向」是关键——消除归类歧义，让 AI 创建文档时不会乱放。

### 00-context/README.md

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 00-context — 目标说明

## 目标
记录项目为什么存在、要满足什么需求、绝对不能违反什么约束。

## 放什么
项目简介、需求清单、硬约束、术语表。

## 不放什么
- 实现与架构 → 20-architecture/
- 命令与开发流程 → 30-engineering/
- 编码过程中的临时问题分析/方案 → 80-dev/
```

### 10-product/README.md

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 10-product — 目标说明

## 目标
从产品视角说明：为谁服务、核心业务流程、怎样算验收通过。

## 放什么
用户与角色、业务流程、验收标准、产品路线。

## 不放什么
- 技术实现与架构 → 20-architecture/
- 对外市场文案 → 60-marketing/
```

### 20-architecture/README.md

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 20-architecture — 目标说明

## 目标
说明系统如何构成、关键设计决策及其理由。

## 放什么
架构概览（含图）、数据模型、架构决策记录（ADR）。

## 不放什么
- 产品需求与流程 → 10-product/
- 运维手册与监控 → 40-operations/
- 编码过程中的临时修复方案 → 80-dev/
```

### 30-engineering/README.md

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 30-engineering — 目标说明

## 目标
让任何开发者（含 AI）能快速搭环境、跑通命令、按规范写代码。

## 放什么
本地搭建、命令清单、编码规范、AI 编码指南。

## 不放什么
- 架构决策 → 20-architecture/decisions/
- 生产环境与运维 → 40-operations/
- 临时问题分析与验证记录 → 80-dev/
```

### 40-operations/README.md

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 40-operations — 目标说明

## 目标
说明如何部署、观测、处理故障与日常运维。

## 放什么
环境配置、监控告警、运维手册（runbook）、故障与排障记录。

## 不放什么
- 本地开发命令 → 30-engineering/commands.md
- 产品路线 → 50-planning/
```

### 50-planning/README.md

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 50-planning — 目标说明

## 目标
记录现在进行到哪、接下来做什么、每个阶段改了什么。

## 放什么
路线图/阶段、实施计划、变更记录（changelog）。

## 不放什么
- 产品验收标准 → 10-product/acceptance-criteria.md
- 架构决策 → 20-architecture/decisions/
- 编码过程中的临时问题分析 → 80-dev/
```

### 60-marketing/README.md

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 60-marketing — 目标说明

## 目标
从市场视角说明产品定位、目标受众、对外文案与发布信息。

## 放什么
产品定位与价值主张、目标受众、发布说明、竞品参考。

## 不放什么
- 内部需求细节 → 00-context/
- 技术实现 → 20-architecture/
```

### 70-research/README.md

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 70-research — 目标说明

## 目标
沉淀调研过程、参考资料与备选方案对比，供未来决策追溯。

## 放什么
参考资料与链接、技术选型对比、备选方案、调研记录。

## 不放什么
- 已采纳的架构决策 → 20-architecture/decisions/
- 当前有效规范 → 30-engineering/coding-standards.md
- 编码现场临时排障和实施方案 → 80-dev/
```

### 80-dev/README.md

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 80-dev — 目标说明

## 目标
存放编码过程中临时产生的问题分析、排障记录、实施方案和验证记录，作为当日工作的可追溯草稿区。

## 放什么
带日期的问题分析、临时方案、验证记录、未完全定稿但需要保留上下文的开发过程文档。文件名必须以 `YYYY-MM-DD-` 开头，例如 `2026-06-15-parser-selector 的方案.md`。

## 不放什么
- 已确认且影响系统边界、数据模型、接口契约、部署/运行拓扑或核心流程的结论 → 当日收尾抽取到 20-architecture/（必要时 ADR）
- 长期有效的开发规范、命令、工程实践和 AI 工作规则 → 30-engineering/
- 路线图、阶段计划、正式变更记录 → 50-planning/
- 已废弃的历史方案 → 99-archive/

## 与 30-engineering 的区别
`30-engineering/` 是稳定工程知识，回答「以后开发者应该怎么做」；`80-dev/` 是开发现场工作区，回答「今天为了解决某个具体问题分析了什么、试了什么、暂定什么」。`80-dev/` 中沉淀出可复用工程实践后，再抽取到 `30-engineering/`。

## 收尾规则
每天结束前按日期前缀复盘当天文件：已确认或已实施且具备架构影响的方案，必须抽取为当前事实并更新到 `20-architecture/`；沉淀为长期工程规则的内容更新到 `30-engineering/`；只服务当前阶段推进、验收或剩余事项的内容更新到 `50-planning/`；没有复用价值的一次性过程留在 `80-dev/` 后续归档或删除，不要硬塞进架构目录。
```

### 90-ui-ux/README.md

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 90-ui-ux — 目标说明

## 目标
说明界面结构、页面清单与交互约定。

## 放什么
信息架构、页面/屏幕清单、交互模式、组件约定。

## 不放什么
- 产品业务流程与验收 → 10-product/
- 对外营销文案 → 60-marketing/
```

### 99-archive/README.md

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 99-archive — 目标说明

## 目标
存放被取代或废弃的历史文档，保留可追溯性。

## 放什么
被取代的旧版文档、废弃方案、历史记录。每份文档须在 frontmatter 标注 `status: historical`/`deprecated`，并声明 `superseded-by`。

## 不放什么
- 当前有效文档 → 对应的标准目录（00–90）
```

---

## 4. 必选文件骨架

> 每个文件至少含 frontmatter + 标题 + 占位提示。下列两个为「重点写实」，其余给最小骨架。

### 00-context/constraints.md（★ 硬约束，最关键）

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# 硬约束（Constraints）

## Technology
- {后端语言/框架必须用 X}
- {数据库是唯一事实来源}

## Security
- 绝不提交密钥、Token、Cookie。
- 绝不绕过 robots.txt、ToS、鉴权、付费墙。

## Architecture
- 所有写操作必须幂等。
- Web 进程不得跑后台任务。
```

### 30-engineering/ai-coding-guide.md（★ AI 编码指南）

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# AI 编码指南

## Before Any Task
1. 读 AGENTS.md 与 docs/README.md。
2. 读 docs/00-context/constraints.md（硬约束，不可违反）。
3. 改架构前读 docs/20-architecture/overview.md。
4. 新建文档前先读目标目录的 README.md，确认放对位置。

## Verification
- 代码改动：跑项目原生测试命令（例如 `npm test` / `pytest` / `go test ./...` / `cargo test`）。
- 文档改动：跑项目原生 docs 校验命令（例如 `npm run docs:check` / `make docs-check` / `just docs-check` / `task docs:check` / `scripts/docs/check.sh`）。

## Boundaries
- 只改与任务相关的代码，不顺手重构。
- 不引入未经 ADR 批准的新技术。
- 重大架构决策必须新增 ADR。
- 编码过程临时问题分析/方案放 `docs/80-dev/`；每日结束前把已确认且具备架构影响的结论抽取更新到 `docs/20-architecture/`。
- `docs/80-dev/` 草稿文件必须以 `YYYY-MM-DD-` 开头；沉淀为长期工程实践才进入 `docs/30-engineering/`，沉淀为阶段推进/验收记录才进入 `docs/50-planning/`。

## Review Checklist（完成任务前自检）
- [ ] 改了架构，是否补了 ADR？
- [ ] 改了硬约束，是否更新 constraints.md？
- [ ] 新增文档是否放对了目录（对照该目录 README）？
- [ ] 新增 `80-dev/` 草稿是否使用 `YYYY-MM-DD-` 日期前缀？
- [ ] `80-dev/` 中已确认或已实施的架构影响结论，是否已同步到 `20-architecture/`？
- [ ] 跑通项目原生测试命令与 docs 校验命令？
```

### 其余必选文件最小骨架（逐个建，替换 {占位}）

每个文件套用此骨架，标题与占位提示按文件语义替换：

```markdown
---
status: current
owner: Dev Team
last-reviewed: 2026-06-13
---

# {文件主题}

> TODO: 在此填写 {该文件应回答的问题}。详见所在目录 README 的目标说明。
```

需建清单（标题语义）：
- `00-context/project-brief.md` — 项目是什么、为谁、不做什么
- `00-context/requirements.md` — 核心需求
- `00-context/glossary.md`（建议）— 术语表
- `10-product/workflows.md` — 核心业务流程
- `10-product/acceptance-criteria.md` — 验收标准
- `10-product/users-and-roles.md`（建议）— 用户与角色
- `20-architecture/overview.md` — 架构概览 + 一张图
- `20-architecture/data-model.md`（有存储则必选）— 数据模型
- `30-engineering/setup.md` — 本地环境搭建
- `30-engineering/commands.md` — 命令清单
- `30-engineering/coding-standards.md`（建议）— 编码规范
- `40-operations/environments.md` — 环境配置
- `40-operations/runbooks.md` — 运维手册
- `40-operations/monitoring.md`（建议）— 监控告警
- `50-planning/roadmap.md` — 阶段/路线图
- `50-planning/changelog.md` — 变更记录
- `60-marketing/positioning.md` — 产品定位与价值主张
- `60-marketing/release-notes.md` — 对外发布说明
- `70-research/references.md` — 参考资料、链接、书籍
- `70-research/alternatives.md` — 技术选型与备选方案对比
- `80-dev/` — 不强制固定业务文件；按 `YYYY-MM-DD-主题.md` 创建临时问题分析/方案文档
- `90-ui-ux/screens.md` — 页面/屏幕清单与信息架构
- `90-ui-ux/interaction-patterns.md` — 交互模式与组件约定

---

## 5. docs/templates/adr.md

```markdown
---
adr: 0000
status: proposed        # proposed | accepted | deprecated | superseded
date: YYYY-MM-DD
superseded-by: ""
---

# ADR-NNNN: {标题}

## Context
为什么需要这个决策（背景、驱动因素、约束）。

## Decision
决定怎么做（具体方案）。

## Consequences
收益、代价、风险、后续约束。

## Alternatives Considered
考虑过但未采用的方案，及未采用的原因。
```

---

## 6. 命令入口适配原则

不要为了 docs 标准强行引入 `Taskfile.yml` 或其它新 runner。优先使用项目已经采用的命令体系，把 docs 标准挂成同等公民：

- Node / 前端项目：优先补 `package.json` scripts。
- 已有 `Makefile`：补 `docs-check`、`ai-check`、`docs-new-adr` target。
- 已有 `justfile`：补同名 recipe。
- 已有 `Taskfile.yml`：补 `docs:check`、`ai:check`、`docs:new-adr` task。
- 无统一 runner：创建 `scripts/docs/check.sh`、`scripts/docs/ai-check.sh`、`scripts/docs/new-adr.sh`，并在 `docs/30-engineering/commands.md` 记录调用方式。

具体可拷贝片段见 `references/command-adapters.md`。`scripts/docs/*.sh` 是通用兜底逻辑，其它 runner 只负责转调用。

---

## 7. scripts/docs/new-adr.sh

> 创建到 `scripts/docs/new-adr.sh`，并 `chmod +x`。

```bash
#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ] || [ -z "${1:-}" ]; then
  echo "Usage: $0 \"decision title\"" >&2
  exit 1
fi

ADR_DIR="docs/20-architecture/decisions"
mkdir -p "$ADR_DIR"
LAST=$(ls "$ADR_DIR"/*.md 2>/dev/null | sed -E 's#.*/([0-9]+)-.*#\1#' | sort -n | tail -1 || true)
NEXT=$((10#${LAST:-0} + 1))
NUM=$(printf "%04d" "$NEXT")
SLUG=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' '-' | sed 's/^-*//;s/-*$//')
TARGET="$ADR_DIR/$NUM-$SLUG.md"
cp docs/templates/adr.md "$TARGET"
sed -i.bak "s/^adr: .*/adr: $NUM/" "$TARGET" && rm -f "$TARGET.bak"
sed -i.bak "s/^date: .*/date: $(date +%F)/" "$TARGET" && rm -f "$TARGET.bak"
sed -i.bak "s/^# ADR-NNNN:.*/# ADR-$NUM: $1/" "$TARGET" && rm -f "$TARGET.bak"
echo "Created $TARGET"
```
