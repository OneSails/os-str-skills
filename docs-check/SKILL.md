---
name: docs-check
description: >
  审查当前项目 docs/ 是否符合「AI 友好 docs 目录标准」（v5.1），输出分级合规报告与具体修复动作。
  覆盖比项目原生 `docs:check` 更深：不只校验文件存在性，还检查①十一个目录齐全②每目录 README 是否三段式
  （目标/放什么/不放什么）③关键文件 frontmatter（status/owner/last-reviewed）齐全④ADR 命名序号连续
  ⑤文档是否放对目录（对照各目录边界）⑥80-dev 日期前缀与每日收尾规则⑦根三件套引用链。Use when user asks to "检查文档结构",
  "docs 合规审查", "docs 结构对不对", "审查目录规范", "docs 健康检查", "review docs structure",
  "文档合规", or mentions "docs-check".
---

# docs-check — AI 友好 Docs 标准合规审查

> 判断标准只有一个：AI 或新成员能否在 3 分钟内自主找到需求、约束、命令与禁止事项，并把新内容放对目录。
> 本 skill 用这个标准反向审查现有 `docs/`，把不达标项逐条揪出来。

## 这个 Skill 做什么

项目原生 `docs:check` 通常只验证「文件存在且非空」，会漏掉空壳 README、缺失 frontmatter、放错目录、ADR 命名错乱等问题。本 skill 做深度内容审查，输出一份**分级报告**：哪些必须修、哪些建议修、哪些已达标，每条都给可执行的修复动作。

## 审查维度（七个）

1. **目录齐全性**：十一个必选目录是否都在（`00-context / 10-product / 20-architecture / 30-engineering / 40-operations / 50-planning / 60-marketing / 70-research / 80-dev / 90-ui-ux / 99-archive`）。
2. **README 三段式**：每个目录的 README 是否含「目标 / 放什么 / 不放什么」。缺「不放什么 + 指明去向」等于边界没写清，记为不达标。
3. **关键文件非空且有效**：必选文件不能是空壳——至少有 frontmatter + 标题 + 实质内容（不是 TODO 占位）。重点查 `00-context/constraints.md`、`30-engineering/ai-coding-guide.md`。
4. **frontmatter 齐全**：「当前有效」文档顶部是否带 `status / owner / last-reviewed`；归档文档是否带 `status: historical|deprecated` + `superseded-by`。
5. **ADR 规范**：命名是否 `NNNN-kebab-title.md`、序号是否连续无跳号/重复、frontmatter 是否含 `adr / status / date`。
6. **分类正确性**（抽样）：抽查若干文档正文，对照其所在目录 README 的「放什么/不放什么」，判断是否放错位置；放错的指明应去哪个目录。重点检查 `80-dev/` 是否只放编码过程临时问题分析/方案，已确认且具备架构影响的结论是否在收尾时同步到 `20-architecture/`（必要时 ADR）。
7. **80-dev 工作区治理**：`80-dev/README.md` 是否明确 engineering/dev 生命周期区别；草稿文件是否以 `YYYY-MM-DD-` 开头；是否说明每日按日期前缀复盘、抽取到 `20-architecture/30-engineering/50-planning` 或留待归档/删除。

> 另含根入口审查：`AGENTS.md` 顶部是否有「遵循 docs 规范、先读 docs/README.md」声明；`CLAUDE.md / GEMINI.md` 是否引用 `AGENTS.md`。

## 执行流程

### Step 1 — 先跑结构闸门
```bash
# 按项目已有命令体系运行，例如：
npm run docs:check && npm run ai:check
make docs-check ai-check
just docs-check && just ai-check
task docs:check && task ai:check
scripts/docs/check.sh && scripts/docs/ai-check.sh
```
把失败项记入报告的「❌ 必须修」区。若项目没有任何 docs 校验入口，也记为必须修：按项目类型补 `package.json` scripts、`Makefile`/`justfile`/`Taskfile.yml` target，或 `scripts/docs/*.sh` 兜底脚本。

### Step 2 — 按六维逐项审查
对照 `references/checklist.md` 的完整清单，逐项检查。对每个不达标项，记录：
- 位置（文件/目录路径）
- 问题（缺什么 / 错什么）
- 级别（❌ 必须修 / ⚠️ 建议 / ✅ 通过）
- 修复动作（具体到「建这个文件」「补这段 frontmatter」「移到 X 目录」）

### Step 3 — 抽样分类核查
随机抽 3–5 篇文档，读正文，对照其目录 README 的边界判定是否放对。放错的在报告里给出「应移至 XX 目录」的建议。

### Step 4 — 输出分级报告
用固定模板输出（见下）。报告要让用户一眼看到「还差多少才能达标」与「下一步做什么」。

## 报告模板（必须用此结构）

```markdown
# Docs 合规审查报告

## 总览
- 审查时间：______
- 总项数：__ / 达标：__ / 必须修：__ / 建议：__

## ❌ 必须修（阻断合规）
- [位置] 问题 → 修复动作
  - 例：`docs/40-operations/README.md` 缺「不放什么」段 → 补三段式（参考 docs-scaffold 模板）

## ⚠️ 建议（不阻断，但影响可用性）
- [位置] 问题 → 建议

## ✅ 已达标
- 简述达标的维度（给用户正反馈）

## 下一步
1. 最优先修的 3 项（按对「3 分钟可发现性」的影响排序）
```

## 完成判据

- 报告覆盖全部七个维度 + 根入口。
- 每个 ❌ 项都有可执行的修复动作（不是泛泛的「改进文档」）。
- 「下一步」给出优先级排序，用户知道先做什么。
- 如果用户同意，可直接调用 `docs-scaffold` 补齐缺失项、调用 `docs-new-adr` 补 ADR。

## 详细检查清单

完整的逐项检查表（可勾选）见 `references/checklist.md`——按需读取。
