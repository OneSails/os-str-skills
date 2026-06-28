# 标准目录树与必选文件清单

> 来源：《AI 编码友好型 Docs 目录结构与命令入口固化方案》v5.1。**十一个目录全必选**。数字前缀只控制排序、不代表重要性；`80-dev/` 用于编码过程中的临时问题分析、方案记录与收尾抽取。

## 根目录文件（必需）

| 文件 | 必需 | 职责 |
| --- | --- | --- |
| `README.md` | 是 | 给人：项目价值、快速开始、主要命令、文档入口 |
| `AGENTS.md` | 是 | 给 AI：项目摘要、技术栈、命令、硬约束、安全边界（canonical 指令源） |
| 项目原生命令入口 | 是 | 按项目类型使用已有命令体系：`package.json` scripts、`Makefile`、`justfile`、`Taskfile.yml`，或 `scripts/docs/*.sh` 兜底 |
| `.env.example` | 是 | 环境变量模板，只放占位值 |
| `.gitignore` | 是 | 排除密钥、本地数据、日志、构建产物 |
| `CLAUDE.md` | 是 | Claude Code 桥接入口，引用 AGENTS.md |
| `GEMINI.md` | 是 | Gemini CLI 桥接入口，引用 AGENTS.md |

## docs/ 完整结构

```text
.
├── AGENTS.md            # 给 AI：命令、约束、边界（canonical）
├── CLAUDE.md            # Claude Code 桥接，引用 AGENTS.md
├── GEMINI.md            # Gemini CLI 桥接，引用 AGENTS.md
├── README.md            # 给人：项目是什么、怎么跑
├── <command entrypoint> # 项目原生命令入口：package.json / Makefile / justfile / Taskfile.yml / scripts/docs/*.sh
└── docs/
    ├── README.md        # 文档总入口 + AI 读取顺序
    ├── 00-context/      # 背景、需求、约束、术语
    ├── 10-product/      # 用户、流程、验收、产品路线
    ├── 20-architecture/ # 架构概览、决策(ADR)、数据模型
    ├── 30-engineering/  # 环境、命令、规范、AI 指南
    ├── 40-operations/   # 环境、监控、运维手册、故障
    ├── 50-planning/     # 路线图、阶段、变更记录
    ├── 60-marketing/    # 定位、受众、文案、发布信息
    ├── 70-research/     # 调研、参考、备选方案对比
    ├── 80-dev/          # 编码过程临时问题分析、方案与验证记录（YYYY-MM-DD- 前缀）
    ├── 90-ui-ux/        # 页面、交互、信息架构
    └── 99-archive/      # 历史/废弃文档
```

## docs/ 目录职责与必选文件一览

| 目录 | 回答的问题 | 必选文件 |
| --- | --- | --- |
| `00-context/` | 项目是什么？需求是什么？绝不能违反什么？ | README、project-brief、requirements、constraints |
| `10-product/` | 为谁服务？核心流程？怎样算做完了？ | README、workflows、acceptance-criteria |
| `20-architecture/` | 系统怎么构成？关键决策为什么这么做？ | README、overview、decisions/（有存储加 data-model） |
| `30-engineering/` | 怎么搭环境、跑命令、写代码？AI 怎么干活？ | README、setup、commands、ai-coding-guide |
| `40-operations/` | 怎么部署、观测、处理故障？ | README、environments、runbooks |
| `50-planning/` | 现在到哪了？接下来做什么？改了什么？ | README、roadmap、changelog |
| `60-marketing/` | 对外怎么说？定位与受众是什么？ | README、positioning、release-notes |
| `70-research/` | 调研了什么？参考了什么？备选方案为什么没选？ | README、references、alternatives |
| `80-dev/` | 编码过程中临时发现的问题、分析、方案和验证记录放哪？ | README（草稿文件用 `YYYY-MM-DD-` 前缀） |
| `90-ui-ux/` | 有哪些页面？交互约定是什么？ | README、screens、interaction-patterns |
| `99-archive/` | 历史/废弃文档在哪？被什么取代？ | README |

## docs:check 校验项清单（共 33 项 test -s，必须全部非空）

根入口（2）：
- `AGENTS.md`、`README.md`

总入口（1）：
- `docs/README.md`

十一个目录 README（11）：
- `docs/00-context/README.md` … `docs/99-archive/README.md`（十一个全校验，含 `docs/80-dev/README.md`）

必选业务文件（19）：
- `00-context/`: project-brief.md、requirements.md、constraints.md
- `10-product/`: workflows.md、acceptance-criteria.md
- `20-architecture/`: overview.md
- `30-engineering/`: setup.md、commands.md、ai-coding-guide.md
- `40-operations/`: environments.md、runbooks.md
- `50-planning/`: roadmap.md、changelog.md
- `60-marketing/`: positioning.md、release-notes.md
- `70-research/`: references.md、alternatives.md
- `90-ui-ux/`: screens.md、interaction-patterns.md

> 注：上述业务文件按目录归组列出，合计 19 个业务文件 + 2 根 + 1 总入口 + 11 目录 README = 33 项。`80-dev/` 不强制固定业务文件，避免制造空壳开发日志；它的命名、收尾和归档约束写在目录 README 中。
