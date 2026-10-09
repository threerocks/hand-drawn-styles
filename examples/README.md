# 画风样例

这里按正式编号顺序展示样图与调用示例。完整配方只以根目录 [`STYLES.md`](../STYLES.md) 为准,避免示例页复制配方后发生漂移。

原来的 `1`、`1.1`、`1.2` 三套配方已从旧位置删除;原 `2` 起的整数配方整体前移,因此下面的 `1` 是原 `2` 重编号后的新身份。用户认可的家庭蜡笔画风迁入 `3.1 蜡笔童涂-潦草自画版`。

## 1. 极简黑白线条讲解漫画

![极简线条 xkcd 火柴人](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/01-minimal-line.png)

> 输入示例:「用 1 号画风讲解番茄工作法」

## 2. 蜡笔童涂

![蜡笔童涂](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/02-crayon.png)

> 输入示例:「用 2 号画风画 OCEAN 主题:小孩戴泳镜潜水、一头大鲸鱼、几条小鱼」

## 3. 吉卜力风

![吉卜力风](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/03-ghibli.png)

> 输入示例:「用 3 号画风画下雨天打伞的猫」

## 3.1 蜡笔童涂-潦草自画版

![蜡笔童涂-潦草自画版画风锚点](https://gentle-starburst-99bd99.netlify.app/hand-drawn/assets/style-3.1/anchor-family.png)

> 输入示例:「用 3.1 画爸爸把零食袋放回柜子,男孩站在旁边看着,不加文字」
>
> 正式生产、连续故事和多页作品必须把 [assets/style-3.1/anchor-family.png](https://gentle-starburst-99bd99.netlify.app/hand-drawn/assets/style-3.1/anchor-family.png) 作为纯画风参考随每一张请求传入,并完整执行 `family-crayon-card-v3` 的三阶段 workflow。

## 4. 小豆人涂鸦信息图

![小豆人涂鸦信息图](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/04-bean-doodle.png)

## 5. MS Paint 烂涂鸦

![MS Paint 烂涂鸦](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/05-ms-paint.png)

## 6. 圆珠笔单线涂鸦

![圆珠笔单线涂鸦](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/06-pen-scribble.png)

## 7. 蜡笔实拍

![蜡笔实拍](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/07-real-crayon.png)

## 8. 水墨写意

![水墨写意](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/08-ink-wash.png)

## 9. 复古像素

![复古像素](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/09-pixel-art.png)

## 10. 情绪叙事淡彩速写

![情绪叙事淡彩速写](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/10-emo-sketch.png)

## 11. 二维水彩风格

![二维水彩风格](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/11-retro-concept.png)

## 12. 暖光童画

![暖光童画](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/12-sunlit-storybook.png)

## 13. 北欧纸雕

![北欧纸雕](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/13-paper-folk.png)

## 14. 北欧绘本水粉

![北欧绘本水粉](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/14-nordic-storybook.png)

## 15. 大鼻软偶

![大鼻软偶](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/15-softnose-vinyl.png)

## 16. 聚光水粉立绘

![聚光水粉立绘](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/16-gouache-spotlight.png)

## 17. 墨线绘本

![墨线绘本](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/17-inked-storybook.png)

## 18. 暖色扁平绘本

![暖色扁平绘本](https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/18-warm-flat-storybook.png)

## 19. 圆头红线极简童画

![圆头红线极简童画](https://gentle-starburst-99bd99.netlify.app/hand-drawn/assets/style-19/anchor-roundhead-redline.png)

> 输入示例：「用 19 号画风画一只幼象用鼻子提起一盏珊瑚红纸灯笼，不加文字」。正式调用必须携带这张画风参考图，并执行调用包中的验收流程。

## 20. 暖黄墨线情绪小剧场

![暖黄墨线情绪小剧场](https://gentle-starburst-99bd99.netlify.app/hand-drawn/assets/style-20/anchor-warm-yellow-ink-story.png)

> 输入示例：「用 20 号画风画两个孩子一起搬一只暖黄色坐垫，不加文字」。正式调用必须携带这张画风参考图，直接生成候选图，再运行机读验收器。

两张图均保留原始字节与 OpenAI C2PA/JUMBF 内容凭证。隐私审计状态为「已审计，未清理」，记录保留在 `assets/style-19/` 与 `assets/style-20/` 下的 `.privacy.json` 和 `.provenance.json`。图片迁移未改变此状态。
