# 画风配方库

每段是该画风的提示词模板。按 SKILL.md 的流程:填好占位符 → 按规则处理比例 → 整段作为最终 prompt 输出。比例行已统一移除,改由调用时按规则处理。

---

## 1. 纯人类手绘儿童涂色页

> 纯风格,无内置版式。比例:不传则不注入。

```
白纸上的纯人类手绘儿童涂色风格,不是数字插画。
画面结构是"大人或老师先画好的粗黑涂色线稿 + 5-8 岁儿童自己填色"。
粗黑马克笔/勾线笔轮廓,外轮廓粗、黑、圆钝、轻重有变化,线条少、粗、断、抖,允许轻微歪斜、重复描边和接缝不齐。
彩笔/蜡笔来回涂色,低到中饱和,露白,深浅不均、轻重不均、笔画断续,稀疏和密集没有规律,必须有局部涂出边界。
同一个色块里要有重压深线、轻扫浅线、短而断的笔画、大片露白和少量越界色痕,像孩子没有计划地涂色;不要均匀密集地填满。
至少一个主色块保留约 25%-35% 露白或浅涂区;至少 2-3 个主要色块出现 1-5mm 明显手误越界,边缘毛糙但不越界不算通过。
形状不要太标准,圆形、手脚、家具边缘可以有儿童画式小误差,但主体和动作必须清楚。
白纸可见少量不规律纸张褶皱、压痕和纸纤维感,大量留白;褶皱不要太多,不要做成装饰纸纹。
不要精修儿童绘本、商业插画、平滑数字线稿、矢量线、渐变、3D、复杂背景、漂亮细节。
如果有中文,必须是清楚可读的粗黑手写中文,允许大小不齐,但不能错字、漏字、乱码或伪文字。
画面内容:【主体】
```

---

## 2. 极简黑白线条讲解漫画(xkcd 火柴人)

> 带版式(网格多格讲解图)。比例:不传则注入软结构提示"多格网格排版",不写数字。占位符 `【N】【分镜列表】` 自动推断(拆不出多步默认 3–4 格)。
>
> 注意:硬性负向约束必须前置,否则模型会自动渲染成厚黑块/氛围插画(已踩过坑)。

```
xkcd 风格的极简黑白火柴人讲解漫画,画在米白/奶油色纸上。
【最重要·硬性负向约束】严禁实心黑色填充、严禁剪影、严禁排线与阴影、严禁明暗与体积感、严禁厚涂或氛围渲染。人物与物体一律只用细线描边。
角色:简单火柴人——圆圈头 + 极简点线五官,身体四肢是细单线;用小道具(帽子、杯子、书等)表示身份,不画细节。
线条:细、均匀、略带手抖的黑色钢笔线,纯轮廓线稿,平面二维,无透视。
版式:【N】格面板组成网格,每格用手绘略歪的圆角矩形框住,面板之间大量留白。
色彩:纯黑白单色,黑线 + 米白纸,无任何其它颜色,无灰阶。
文字:每格顶部加粗手写中文小标题,下方一句手写中文说明;可加简短对话气泡。中文清楚可读,不得错字、乱码或伪中文。
调性:概念化、示意图式、略带幽默的讲解感,像 xkcd / 技术科普涂鸦。
分镜:
【分镜列表】
```

---

## 3. 蜡笔童涂(5岁小孩坏画)

> 接近纯风格。比例:不传则不注入。占位符 `【主体】【主色调】【标题词】` 自动推断。

```
A drawing made by a real 5-year-old child with crayons on white paper.
NOT made by an artist. It should look clumsy, messy, and "bad" on purpose.

Subject: 【主体】.

MANDATORY childlike flaws (do not clean these up):
- shaky wobbly outlines that wander, overshoot corners, and never close neatly
- often double-drawn lines where the kid went over the same edge twice
- proportions clumsy and wrong; arms and legs are thin crooked stick-lines with no volume
- face uneven and asymmetric: eyes different sizes and not level, crooked smile, features off-center
- coloring is messy and goes OUTSIDE the outlines; large patches of white paper left unfilled; scribble strokes in random directions
- bright flat primary crayon colors (【主色调】, and red, yellow, green, purple, black), no shading, no gradient, no blending
- hand-lettered title "【标题词】" at the top in uneven wobbly capital letters, each a different color, on a crooked baseline, letters different sizes

Flat naïve composition, objects floating with no perspective, plain white background.
Look genuinely crude — avoid anything cute, polished, symmetric, balanced, or professional.
```

---

## 4. 吉卜力风

> 纯风格。比例:不传则不注入。

```
Studio Ghibli style hand-drawn anime illustration of 【主体】.
Soft hand-painted watercolor aesthetic with gentle cel-shaded coloring; warm cinematic lighting with sunlight softly diffusing from above and a tender glow.
Bright yet harmonious, lightly saturated color palette; lush, detailed natural environments and dreamy, nostalgic atmosphere.
Expressive Ghibli-inspired character features, gentle emotional tone, whimsical and heartwarming mood.
Soft shading and atmospheric depth, clean delicate linework, painterly hand-drawn feel — not 3D, not photoreal, not a digital vector look.
```

---

## 5. 小豆人黑色涂鸦信息图

> 带版式(竖版 N 格信息图)。比例:不传则注入软结构提示"竖版、多格自上而下堆叠",不写数字。占位符 `【N】【分镜列表】` 自动推断(拆不出多步默认 3–4 格)。

```
A hand-drawn black marker doodle explainer illustration on off-white paper,
vertical infographic with 【N】 stacked panels separated by thin hand-drawn lines.

Character: a simple solid-black round blob person with two white dot eyes,
a small curved smile, and thin black stick arms and legs. The body is solid
flat black with smooth edges (no sketchy texture). The SAME character appears
in every panel doing a different action.

Style: clean black marker/pen outlines, slightly wobbly but fully closed
hand-drawn lines. All objects are OUTLINE-ONLY black line-art with white
interiors, no shading, no fill. Everything is monochrome black & white EXCEPT
one orange accent color used ONLY for the single key item in each panel.
Hand-drawn curved arrows in red or blue point at key spots, each with a short
handwritten Chinese label. Each panel has a bold hand-written marker-style
Chinese title at the top. Minimalist composition, lots of white space.

Panels:
【分镜列表】
```

---

## 6. MS Paint 烂涂鸦(the worse, the better)

> 纯风格。比例:不传则不注入。占位符 `【主体】` 自动推断。
>
> 这是 OpenAI 官方模板那个病毒级"故意画烂"风(被称「第二个吉卜力」)。**它的最强效果来自图生图**:把第一句换成「把这张照片重画成…」并随 prompt 附一张真实照片,效果远胜纯文生图。文生图也成立(见样图)。

```
把【主体】画成极其笨拙、潦草、可怜兮兮的烂涂鸦,像是用鼠标在 MS Paint 里一笔一笔硬画出来的。
线条歪扭、抖动、断断续续;比例荒谬地不对,该圆的不圆、该直的不直。
填色是大块粗糙的纯色,明显涂出边界、有像素锯齿、低质量数字感。
整体"明明想画对却处处不对劲",越烂越好笑;纯白背景,构图随意。
不要任何专业感、精修、写实光影、渐变或漂亮细节——刻意地丑、刻意地业余。
```

---

## 7. 圆珠笔单线涂鸦(scribble)

> 纯风格。比例:不传则不注入。占位符 `【主体】` 自动推断。偏艺术速写向,适合肖像/动物。

```
用单一黑色圆珠笔画的潦草涂鸦速写,描绘【主体】。
大量快速、随性、来回缠绕的细线条,线条不闭合、带偶然性,靠线的疏密缠绕表现明暗与体积,一气呵成的速写感。
纯单色——黑色墨线 + 白纸,无平涂色块,无数字渐变。
自由、即兴、艺术化的手稿气质,而非工整插画。
```
