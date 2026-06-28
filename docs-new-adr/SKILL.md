---
name: docs-new-adr
description: >
  按标准规范新建一条 ADR（Architecture Decision Record）：先判定是否真需要 ADR（防滥用），
  再自动生成序号（现有最大序号+1，4 位补零）、kebab slug、填充 frontmatter，并引导填写
  Context / Decision / Consequences / Alternatives 四段；若取代旧决策，自动更新旧 ADR 的
  status=superseded + superseded-by 链。Use when user asks to "新建 ADR", "记录架构决策",
  "写个 ADR", "记录这个技术决策", "create ADR", "document architecture decision", "技术选型记录",
  or mentions "docs-new-adr" / "architecture decision record".
---

# docs-new-adr — 按规范新建架构决策记录（ADR）

> ADR 是「为什么这么决定」的留痕。标准要求：序号制命名、frontmatter 记状态、四段正文。本 skill 确保每条 ADR 都符合规范，并且只在该写的时候写。

## 这个 Skill 做什么

把「记录一个架构决策」变成确定性流程：判定必要性 → 算序号 → 生成文件 → 填四段 → 处理取代链。避免人工算序号出错、漏写 frontmatter、或滥用 ADR 记录琐碎事项。

## 何时该写 ADR（先判定，防滥用）

**满足以下任一条件才写 ADR**：
- 更换核心技术栈或数据库
- 改变系统边界或事实来源（source of truth）
- 改变安全或鉴权策略
- 做出明确的技术债妥协（并说明为何接受）

如果用户的决策只是「实现细节」「常规选型」「可逆的小改动」，**先提示**：「这个决策可能不需要 ADR——它更像实现细节。确认仍要记录吗？」让用户决定，不擅自写。

> 判定依据详见 `references/adr-template.md` 的「ADR 触发条件与写法」。

## Critical Rules

1. **序号 = 现有最大序号 + 1**：扫描 `docs/20-architecture/decisions/*.md`，取最大序号 +1，`printf "%04d"` 补零。用 `10#` 前缀防前导零被当八进制。
2. **slug = kebab-case**：标题转小写、非字母数字转 `-`、去首尾 `-`。
3. **文件名 = `NNNN-slug.md`**：与 ADR 模板标题 `ADR-NNNN` 一致，便于追溯 supersede 链。
4. **优先用项目原生命令或脚本**：若项目已有 `docs:new-adr`/`docs-new-adr` 命令入口，按其原生命令体系调用；若已有 `scripts/docs/new-adr.sh`，直接调用脚本；都没有则本 skill 内联等价逻辑生成。
5. **填充 frontmatter**：`adr=<序号>`、`status: proposed`（默认，除非用户明确 accepted）、`date=<今天>`、`superseded-by: ""`。
6. **取代旧决策时更新链**：若新 ADR 取代旧 ADR，把旧 ADR 的 `status` 改为 `superseded`、`superseded-by` 指向新序号。
7. **不回收序号**：序号只增不减，即便某 ADR 被废弃。

## 执行流程

### Step 1 — 判定必要性
按「何时该写 ADR」与用户确认。不必要时劝退（用户坚持则照写，但 `status` 留 proposed）。

### Step 2 — 生成序号与文件名
```bash
# 若已有项目原生命令入口，按实际项目类型调用其中一种：
npm run docs:new-adr -- "{决策标题}"
make docs-new-adr title="{决策标题}"
just docs-new-adr "{决策标题}"
task docs:new-adr -- title="{决策标题}"

# 若只有脚本入口：
scripts/docs/new-adr.sh "{决策标题}"

# 否则内联等价：
ADR_DIR="docs/20-architecture/decisions"
mkdir -p "$ADR_DIR"
LAST=$(ls "$ADR_DIR"/*.md 2>/dev/null | sed -E 's#.*/([0-9]+)-.*#\1#' | sort -n | tail -1 || true)
NEXT=$((10#${LAST:-0} + 1))
NUM=$(printf "%04d" "$NEXT")
```

### Step 3 — 套模板写文件
从 `references/adr-template.md` 取模板，填 frontmatter（`adr: $NUM`、`status: proposed`、`date: <今天>`、`superseded-by: ""`），写 `$NUM-$SLUG.md`。

### Step 4 — 引导填四段
向用户提问（或据上下文推断）填实：
- **Context**：为什么需要这个决策？背景、驱动因素、约束。
- **Decision**：决定怎么做？具体方案。
- **Consequences**：收益、代价、风险、后续约束。
- **Alternatives Considered**：考虑过但没采用的方案，及原因（这条最能防止未来重蹈覆辙）。

### Step 5 — 处理取代链（如适用）
若新 ADR 取代旧 ADR-`OLDNUM`：
- 旧文件 `status: accepted` → `superseded`
- 旧文件 `superseded-by: "ADR-{NEWNUM}"`
- 新文件正文 Context 里说明「取代 ADR-{OLDNUM}，因为……」

### Step 6 — 验证
```bash
# 运行项目原生 docs:check 入口，例如：
npm run docs:check
make docs-check
just docs-check
task docs:check
scripts/docs/check.sh

ls docs/20-architecture/decisions/   # 确认序号连续
```

## 完成判据

- 文件名 `NNNN-kebab-title.md`，序号连续。
- frontmatter 含 `adr / status / date / superseded-by`。
- 四段正文非空（至少 Context + Decision 有实质内容）。
- 若取代旧 ADR，旧 ADR 的状态与 `superseded-by` 已更新。

## 详细模板与写法

ADR 模板全文、四段写作指引、触发条件详述见 `references/adr-template.md`——按需读取。
