# 安装与验证

本目录是可独立使用的手绘画风 Skill。配方只以 [STYLES.md](STYLES.md) 为准，执行流程见 [PROTOCOL.md](PROTOCOL.md)。

将 `hand-drawn/` 整个目录放入 Agent 的技能目录，保留目录结构。Claude Code 使用 `~/.claude/skills/hand-drawn/`，Codex 使用 `~/.codex/skills/hand-drawn/`。其他 Agent 可以把自定义指令指向本目录的 `AGENTS.md`。

默认只输出提示词或正式调用包，不生成图片。运行脚本需要 Python 3.10 或更高版本；无需安装 Python 第三方依赖。

在安装目录联网执行一次检查。脚本按需下载 5 张运行参考图，核对大小和 SHA-256，汇总缺失文件、资源引用和别名错误，并在目录外测试全部画风：

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

画风 3.1、19、20 的调用包必须携带已校验的缓存锚点，并执行各自的生产与验收流程。锚点图片与现有隐私审计记录按原字节保留；安装检查通过不表示图片完成了隐私清理。

其他画风仍默认输出纯文本，无需下载图片；风格 13 使用 `--format json` 时，`references` 会包含两张北欧纸雕参考图。所有画风参考图同时提供公开 `url`、文件 `sha256` 和缓存绝对 `path`。脚本只负责替换参数，其他画风的内容与参数默认值由 Agent 按协议填齐；`--list` 可查看需要填写的参数。

`PACKAGE-MANIFEST.json` 记录安装文件大小和 SHA-256。安装检查会发现包内文件缺失或被改动。`assets/image-manifest.json` 记录远端图片的大小和 SHA-256；安装包不含图片二进制。

运行 `python3 -B scripts/hosted_images.py fetch` 可提前下载全部运行参考图。默认缓存位于 `~/.cache/hand-drawn/images`，可通过 `HAND_DRAWN_IMAGE_CACHE` 指定目录。缓存有效时可设置 `HAND_DRAWN_OFFLINE=1` 离线调用；缓存缺失或损坏时停止调用。完整规则见 [docs/image-hosting.md](docs/image-hosting.md)。
