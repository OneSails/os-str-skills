# os-str-skills

星轨纵横技能库。这个仓库保存可发布、可安装、可校验的 skill 源码；当前重点是 AI 友好 docs 标准相关技能。

## Skills

| Skill | Path | Purpose |
| --- | --- | --- |
| `docs-scaffold` | `docs-scaffold/` | 初始化 AI 友好 docs 目录、根 AI 指南、ADR 模板，并按项目类型固化校验入口 |
| `docs-check` | `docs-check/` | 审查项目 docs 目录是否符合 AI 友好 docs 标准 |
| `docs-new-adr` | `docs-new-adr/` | 按规范创建编号 ADR，并维护 superseded 链 |

仓库根目录的 `skills.manifest.json` 是发布清单；每个 skill 目录必须包含 `SKILL.md`，并推荐包含 `agents/openai.yaml`。

## Install From GitHub

安装到 Codex：

```bash
python3 /Users/randy/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo OneSails/os-str-skills \
  --path docs-scaffold docs-check docs-new-adr \
  --ref main
```

安装单个 skill：

```bash
python3 /Users/randy/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/OneSails/os-str-skills/tree/main/docs-scaffold
```

安装后重启 Codex，让新技能进入可发现列表。

## Install From Local Checkout

从当前 checkout 安装到默认 Codex skills 目录：

```bash
python3 scripts/install-local.py
```

安装指定技能：

```bash
python3 scripts/install-local.py docs-check
```

覆盖已有本地技能：

```bash
python3 scripts/install-local.py docs-scaffold docs-check docs-new-adr --replace
```

默认目标目录是 `${CODEX_HOME}/skills`；未设置 `CODEX_HOME` 时使用 `~/.codex/skills`。也可以显式指定：

```bash
python3 scripts/install-local.py --dest ~/.cc-switch/skills --replace
```

## Validate

```bash
task skills:validate
```

或直接运行：

```bash
python3 scripts/validate-skills.py
```

校验覆盖：

- `SKILL.md` frontmatter 只包含 `name` 和 `description`
- skill 目录名与 `name` 一致
- `references/...` 引用文件存在
- `agents/openai.yaml` 存在且 `default_prompt` 包含 `$skill-name`
- `skills.manifest.json` 与实际 skill 目录一致

## Repository Rules

- 一个 skill 一个目录，目录名使用小写 hyphen-case。
- 仓库根目录保存安装、发布、校验说明；skill 目录内不放 `README.md`。
- 长模板、清单、领域资料放在 `references/`，保持 `SKILL.md` 精简。
- 发布到 GitHub 前必须跑 `python3 scripts/validate-skills.py`（或便捷入口 `task skills:validate`）。
