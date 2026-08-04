---
name: hand-drawn
description: Use when users ask for a hand-drawn or illustrated image prompt, name one of the repository's 19 numbered styles or 3 variants, or mention triggers such as 儿童涂色、亲子手绘、家庭蜡笔画、亲子蜡笔故事、亲子投稿蜡笔故事卡、家庭蜡笔卡、蜡笔、吉卜力、水墨、像素、淡彩速写、动画概念、水粉、北欧绘本、纸雕、软胶潮玩、墨线绘本、暖色扁平绘本、family-crayon-card、parent-child-crayon、flat-storybook、warm-flat-storybook. Produces prompt text or a formal reference-bearing call bundle and does not generate images.
---

# 手绘风格 prompt 生成器

完整指令与画风配方是工具无关的,放在同目录:

1. 按 [PROTOCOL.md](PROTOCOL.md) 的 5 步流程执行:确定画风 → 取配方 → 自动填占位符 → 处理比例 → 输出 prompt。
2. 从 [STYLES.md](STYLES.md) 取对应编号的完整模板。
3. 能执行脚本时优先调用 `scripts/render_prompt.py`,不得手工缩写、同义改写或与业务项目的画风段落混配。
4. 风格 1.2 用于正式生产、连续故事或多页作品时,必须使用渲染器 JSON 中的 `references`,把内置画风锚点随每张请求一起传入;锚点不可用就停止正式生产。
5. 其他画风默认只输出最终 prompt;风格 1.2 的正式生产默认输出 JSON 调用包,纯文本只允许显式 `--text-only-preview`。不生图;仓库维护者新增或验收画风时,按 `AGENTS.md` 的维护者验证例外执行。
