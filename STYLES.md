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

## 2. 极简黑白线条漫画手稿

> 带版式(多格漫画页)。比例:不传则注入软结构提示"竖版多格漫画页排版",不写数字。

```
极简主义黑白漫画手稿风格。原生、粗糙、稀疏、表现主义的速写气质,强调留白与高对比度视觉张力,带独立图画小说的艺术实验感。
构图:多格漫画页面排版,用带圆角的手绘不规则边框把画面分割成不同面板(Panel)。
空间:极其平面化的二维视角,不追求透视准确,通过线条疏密和剪影暗示空间关系,大量负空间(Negative Space)构成画面主体。
线条:极具手感和偶然性的线条,线条不闭合,边缘粗糙。
质感:高对比度,无中间调。
色彩:单色系统。背景为米白/灰白纸张基调,前景为灰黑色。
严禁任何彩色或灰阶。严禁平滑矢量线条、数字渐变或喷枪效果。避免精确几何形状、直线尺规作图痕迹,以及写实风格的光影和细节描绘。
画面内容:【主体】
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
