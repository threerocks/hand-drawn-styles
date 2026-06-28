---
name: hand-drawn
description: 生成手绘/插画风格的生图提示词(prompt)。内置 7 种已验证画风——①纯人类手绘儿童涂色页 ②极简黑白线条讲解漫画(xkcd火柴人) ③蜡笔童涂(5岁小孩坏画) ④吉卜力 ⑤小豆人黑色涂鸦信息图 ⑥MS Paint 烂涂鸦(the worse the better) ⑦圆珠笔单线涂鸦。用户没指定画风就列菜单让其选;也可用中文名/编号/英文别名显式指定。只产出最终 prompt 纯文本,不负责生图、不锁定出图比例。触发词:手绘、画风、用XX风格画、生成手绘提示词、童涂色、极简线条、火柴人、xkcd、蜡笔风、吉卜力、ghibli、小豆人、MS Paint、烂涂鸦、圆珠笔、scribble、doodle、hand-drawn style。
---

# 手绘风格 prompt 生成器(Claude Code 适配)

本文件是 Claude Code skill 的入口。完整指令与画风配方是工具无关的,放在同目录:

1. **执行流程**见 [PROTOCOL.md](PROTOCOL.md)——确定画风 → 取配方 → 自动填占位符 → 处理比例 → 输出 prompt。
2. **画风配方**见 [STYLES.md](STYLES.md)。

收到生图请求时:读 PROTOCOL.md 并严格按其 5 步流程执行,画风模板从 STYLES.md 取。只输出最终 prompt,不生图。
