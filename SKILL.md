---
name: hand-drawn
description: 生成手绘/插画风格的生图提示词(prompt)。内置 13 种主画风 + 2 个变体(共 15 套已验证配方)——①纯人类手绘儿童涂色页(含 1.1 低饱和克制版:极简留白+≤4低饱和色+单橙红) ②极简黑白线条讲解漫画(xkcd火柴人) ③蜡笔童涂(5岁小孩坏画,含 3.1 潦草自画版:全自画简笔火柴娃+低饱和单橙红) ④吉卜力 ⑤小豆人黑色涂鸦信息图 ⑥MS Paint 烂涂鸦(the worse the better) ⑦圆珠笔单线涂鸦 ⑧蜡笔实拍(像真蜡笔纸照片) ⑨水墨写意 ⑩复古像素 ⑪情绪叙事淡彩速写(靛蓝松散线+大片留白+一处橙色点缀的催泪家庭故事风) ⑫复古动画概念稿(1950s中古动画水粉设定稿:奶油暖底光晕+橙蓝互补+铅笔起稿线,亲和力强,适配i2v动画) ⑬暖光童画(现代动画vis-dev水粉童画:大眼大虹膜+蓬软发团飞丝+青橙互补+干擦留白纸边,Pixar概念稿感,适合角色立绘/绘本/i2v锚图)。用户没指定画风就列菜单让其选;也可用中文名/编号/英文别名显式指定。只产出最终 prompt 纯文本,不负责生图、不锁定出图比例。触发词:手绘、画风、用XX风格画、生成手绘提示词、童涂色、描线填色、极简线条、火柴人、xkcd、蜡笔风、吉卜力、ghibli、小豆人、MS Paint、烂涂鸦、圆珠笔、scribble、蜡笔实拍、real-crayon、水墨、写意、国画、ink-wash、像素、pixel-art、8-bit、doodle、潦草自画、简笔涂鸦、rawkid、情绪叙事、淡彩速写、速写讲故事、emo-sketch、story-sketch、复古动画、概念稿、概念设定、retro-concept、mid-century、水粉厚涂、gouache、暖光童画、动画概念暖绘、sunlit-storybook、vis-dev、visual development、皮克斯风、hand-drawn style。
---

# 手绘风格 prompt 生成器(Claude Code 适配)

本文件是 Claude Code skill 的入口。完整指令与画风配方是工具无关的,放在同目录:

1. **执行流程**见 [PROTOCOL.md](PROTOCOL.md)——确定画风 → 取配方 → 自动填占位符 → 处理比例 → 输出 prompt。
2. **画风配方**见 [STYLES.md](STYLES.md)。

收到生图请求时:读 PROTOCOL.md 并严格按其 5 步流程执行,画风模板从 STYLES.md 取。只输出最终 prompt,不生图。
