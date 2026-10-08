# 安装与验证

本目录是可独立使用的手绘画风 Skill。配方只以 [STYLES.md](STYLES.md) 为准，执行流程见 [PROTOCOL.md](PROTOCOL.md)。

将 `hand-drawn/` 整个目录放入 Agent 的技能目录，保留目录结构。Claude Code 使用 `~/.claude/skills/hand-drawn/`，Codex 使用 `~/.codex/skills/hand-drawn/`。其他 Agent 可以把自定义指令指向本目录的 `AGENTS.md`。

默认只输出提示词或正式调用包，不生成图片。运行脚本需要 Python 3.10 或更高版本；无需安装 Python 第三方依赖。

在安装目录执行一次检查。脚本汇总缺失文件、资源引用和别名错误，并在目录外测试全部画风：

```bash
python3 -B scripts/check_skill.py
```

输出以 `pass` 开头且退出码为 0 才表示安装检查通过。检查不调用图像模型，不验证成图视觉效果。

查看画风编号、别名、参数和参考图：

```bash
python3 -B scripts/render_prompt.py --list
```

普通画风调用示例：

```bash
python3 -B scripts/render_prompt.py --style minimal-line \
  --var 'N=3' \
  --var '分镜列表=第一格：设置计时器。第二格：专注工作。第三格：休息。'
```

正式画风调用示例：

```bash
python3 -B scripts/render_prompt.py --style 3.1 \
  --subject '妈妈和孩子一起看书' --text '不加任何文字'
```

画风 3.1、19、20 的调用包必须携带目录内的锚点，并执行各自的生产与验收流程。锚点图片及其现有隐私审计记录按原字节保留；目录检查通过不表示图片完成了隐私清理。

其他画风仍默认输出纯文本；风格 13 使用 `--format json` 时，`references` 会包含两张北欧纸雕参考图的绝对路径。脚本只负责替换参数，其他画风的内容与参数默认值由 Agent 按协议填齐；`--list` 可查看需要填写的参数。

画风 21 的本机直接出图入口是 `scripts/generate_monologue_card_with_codex.sh`。该可选功能还需要已登录且支持图像生成的 Codex CLI、bun 和 `sweety-image-privacy`；默认输出归一尺寸需要 macOS 的 `sips`。脚本会先检查依赖，再生图、归一尺寸、执行隐私清理与审计。缺少隐私技能或审计未通过时，脚本停止交付。

脚本会在相邻技能目录和常见技能安装目录查找 `sweety-image-privacy/scripts/main.ts`，也可以用 `--privacy-script PATH` 指定。`--keep-metadata` 已取消。成功后图片旁会保存 `.privacy.json`；审计可能记录系统管理的 `com.apple.provenance`，不能把这个状态描述成所有来源信息均已清除。

`PACKAGE-MANIFEST.json` 记录文件大小和 SHA-256。安装检查会发现包内文件缺失或被改动。轻量包保留北欧纸雕的两张参考图和三张正式锚点，其他展示样图与研发对照图保留在维护仓库。
