---
name: hand-drawn
description: Use when users ask for a hand-drawn or illustrated image prompt, name one of the repository's 21 numbered styles or the 3.1 stable variant, or mention triggers such as 亲子手绘、家庭蜡笔画、蜡笔、吉卜力、水墨、像素、淡彩速写、动画概念、水粉、北欧绘本、纸雕、软胶潮玩、墨线绘本、暖色扁平绘本、圆头红线、暖黄墨线、手写独白、彩铅独白、独白卡、family-crayon-card、warm-flat-storybook、roundhead-redline、warm-yellow-ink-story、pencil-monologue. Produces prompt text or a formal reference-bearing call bundle and does not generate images.
---

# 手绘风格 prompt 生成器

完整指令与画风配方是工具无关的,放在同目录:

1. 按 [PROTOCOL.md](PROTOCOL.md) 的 5 步流程执行:确定画风 → 取配方 → 自动填占位符 → 处理比例 → 输出 prompt。
2. 从 [STYLES.md](STYLES.md) 取对应编号的完整模板。
3. 能执行脚本时优先调用 `scripts/render_prompt.py`,不得手工缩写、同义改写或与业务项目的画风段落混配。
4. 风格 3.1 用于正式生产、连续故事或多页作品时,必须完整执行渲染器 JSON 的三阶段 `workflow`:基础生成 → `scribble-correction` → `scribble-chaos-correction`;前两阶段都只能算中间产物。锚点或任一修正阶段不可用就停止正式生产。
5. 风格 19 正式生产必须消费 `roundhead-redline-v1` JSON 调用包:每张携带原创锚点,锁定模型快照和高保真参考图输入,基础图只标为 `candidate-only`,通过 `acceptance_contract` 后才能标为 final;任一条件不可用时停止正式生产。
6. 风格 20 正式生产必须消费 `warm-yellow-ink-story-v3` JSON 调用包:使用固定原创锚点生成 `final-candidate`,再运行机读验收器;失败候选整张拒收并重新生成,禁止用通用画风迁移编辑修补。
7. 风格 21 手写独白彩铅自带文案且只定义风格:`--text` 必填(文案原文,渲染器自动分行,空行分段),`--subject` 可省略(默认由模型按文案决定内容与构图),画幅默认 3:4 可用 `--aspect` 覆盖,默认输出纯文本 prompt;本机有 codex 时可用 `scripts/generate_monologue_card_with_codex.sh` 直接出图。
8. 其他画风默认只输出最终 prompt;风格 3.1/19/20 的纯文本只允许显式 `--text-only-preview`。不生图;仓库维护者新增或验收画风时,按 `AGENTS.md` 的维护者验证例外执行。

安装方法见 [INSTALL.md](INSTALL.md)。安装后先运行 `python3 -B scripts/check_skill.py` 汇总检查文件、参考图、别名和全部画风调用；检查不生图。使用 `python3 -B scripts/render_prompt.py --list` 取得菜单与参数，保持整个安装包的目录结构。
