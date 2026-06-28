# 项目类型命令入口适配

> 目标：docs 标准必须可校验，但不能绑定到单一 runner。先复用项目已有命令体系；没有统一 runner 时，用 `scripts/docs/*.sh` 兜底。

## 选择顺序

1. 看项目已有事实：`package.json`、`Makefile`、`justfile`、`Taskfile.yml`、`pyproject.toml`、`go.mod`、`Cargo.toml`、CI 配置、README 命令。
2. 若已有统一 runner，沿用它，不新增并行入口。
3. 若存在多个 runner，优先选 README/CI/AGENTS.md 已经使用的那个。
4. 若没有统一 runner，创建 `scripts/docs/check.sh`、`scripts/docs/ai-check.sh`、`scripts/docs/new-adr.sh`，并在 `docs/30-engineering/commands.md` 记录。
5. 所有 runner 都尽量转调用 `scripts/docs/*.sh`，避免多处复制校验逻辑。

## package.json scripts

适用于 Node、Next.js、React、Vue、Svelte、前端工具库，或本身已经用 npm/pnpm/yarn 管命令的项目。

```json
{
  "scripts": {
    "docs:check": "bash scripts/docs/check.sh",
    "ai:check": "bash scripts/docs/ai-check.sh",
    "docs:new-adr": "bash scripts/docs/new-adr.sh"
  }
}
```

运行：

```bash
npm run docs:check
npm run ai:check
npm run docs:new-adr -- "my decision"
```

如果项目使用 pnpm/yarn，保持 `package.json` scripts 不变，运行时使用 `pnpm docs:check` 或 `yarn docs:check`。

## Makefile

适用于已有 `Makefile` 的 Go、C/C++、Python、通用服务项目。

```makefile
.PHONY: docs-check ai-check docs-new-adr

docs-check:
	bash scripts/docs/check.sh

ai-check:
	bash scripts/docs/ai-check.sh

docs-new-adr:
	test -n "$(title)"
	bash scripts/docs/new-adr.sh "$(title)"
```

运行：

```bash
make docs-check
make ai-check
make docs-new-adr title="my decision"
```

## justfile

适用于已有 `justfile` 的项目。

```makefile
docs-check:
    bash scripts/docs/check.sh

ai-check:
    bash scripts/docs/ai-check.sh

docs-new-adr title:
    bash scripts/docs/new-adr.sh "{{title}}"
```

运行：

```bash
just docs-check
just ai-check
just docs-new-adr "my decision"
```

## Taskfile.yml

仅适用于已经采用 go-task 的项目；不要为了 docs 标准新建 Taskfile。

```yaml
version: "3"

tasks:
  docs:check:
    desc: Check docs structure
    cmds:
      - bash scripts/docs/check.sh

  ai:check:
    desc: Check AI guide files
    cmds:
      - bash scripts/docs/ai-check.sh

  docs:new-adr:
    desc: Create a numbered ADR. Usage: task docs:new-adr -- title=my-decision
    cmds:
      - test -n "{{.title}}"
      - bash scripts/docs/new-adr.sh "{{.title}}"
```

运行：

```bash
task docs:check
task ai:check
task docs:new-adr -- title="my decision"
```

## scripts/docs/check.sh

```bash
#!/usr/bin/env bash
set -euo pipefail

test -s AGENTS.md
test -s README.md
test -s docs/README.md

test -s docs/00-context/README.md
test -s docs/10-product/README.md
test -s docs/20-architecture/README.md
test -s docs/30-engineering/README.md
test -s docs/40-operations/README.md
test -s docs/50-planning/README.md
test -s docs/60-marketing/README.md
test -s docs/70-research/README.md
test -s docs/80-dev/README.md
test -s docs/90-ui-ux/README.md
test -s docs/99-archive/README.md

test -s docs/00-context/project-brief.md
test -s docs/00-context/requirements.md
test -s docs/00-context/constraints.md
test -s docs/10-product/workflows.md
test -s docs/10-product/acceptance-criteria.md
test -s docs/20-architecture/overview.md
test -s docs/30-engineering/setup.md
test -s docs/30-engineering/commands.md
test -s docs/30-engineering/ai-coding-guide.md
test -s docs/40-operations/environments.md
test -s docs/40-operations/runbooks.md
test -s docs/50-planning/roadmap.md
test -s docs/50-planning/changelog.md
test -s docs/60-marketing/positioning.md
test -s docs/60-marketing/release-notes.md
test -s docs/70-research/references.md
test -s docs/70-research/alternatives.md
test -s docs/90-ui-ux/screens.md
test -s docs/90-ui-ux/interaction-patterns.md
```

## scripts/docs/ai-check.sh

```bash
#!/usr/bin/env bash
set -euo pipefail

test -f AGENTS.md
test -f CLAUDE.md
test -f GEMINI.md
grep -q "AGENTS.md" CLAUDE.md
grep -q "AGENTS.md" GEMINI.md
grep -q "docs/README.md" AGENTS.md
```

## scripts/docs/new-adr.sh

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
