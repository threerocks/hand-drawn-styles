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
>
> 这是"小孩自己画的坏画"(偏插画/图形感)。要"像真蜡笔涂在纸上的照片、一眼真人手涂"请用 [#8 蜡笔实拍](#8-蜡笔实拍真儿童手涂纸张)。

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
>
> 注意:gpt-image(Codex/ChatGPT)上若用"lush/detailed"会出"稀碎感"(过度堆细节、天空云朵零碎)。已改为反堆细节——单一焦点、简化背景、大色块平滑渐变、云少而整(经 gpt-image 实测)。

```
Studio Ghibli style hand-drawn anime illustration of 【主体】.
Clean, uncluttered composition with ONE clear focal subject; simplified background, generous calm negative space — avoid busy, fragmented, over-detailed or scattered compositions.
Render any large areas (sky, water, fields, walls) as smooth, even watercolor gradients — no patchy, mottled, speckled or grainy texture. Any clouds should be a few large, simple, soft, cohesive shapes — not many small scattered puffs or broken fragments.
Soft hand-painted watercolor look with smooth gentle gradients and soft cel-shading; warm cinematic light diffusing softly from above with a tender glow.
Bright yet harmonious, lightly saturated palette; dreamy, nostalgic, heartwarming mood.
Clean delicate linework, painterly hand-drawn feel — not 3D, not photoreal, not a digital vector, not cluttered, not fragmented.
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

---

## 8. 蜡笔实拍(真·儿童手涂纸张)

> 纯风格。比例:不传则不注入。占位符 `【主体】【主色调】【标题词】` 自动推断。
>
> 和 [#3 蜡笔童涂](#3-蜡笔童涂5岁小孩坏画) 的区别:#3 是"小孩自己画的坏画"(偏插画);#8 是"一张真蜡笔纸的照片",命门在实拍纸感 + 强制露白(每块色露白约 40–50%) + 蜡质方向笔触 + 反数字滤镜(经 gpt-image 实测)。

```
A cellphone PHOTO of a real drawing made by a 5-year-old with wax crayons on a slightly wrinkled sheet of white printer paper. It must look photographed on real paper — visible paper texture and faint wrinkles, clean bright white paper — NOT a digital illustration.
Brightly and evenly lit, shot in soft bright daylight, well-exposed and high-key: the white paper reads clean and bright and FILLS almost the whole frame, with little or no surrounding desk or surface visible; only very soft barely-there wrinkle shadows, NO dark or moody shadows, NO underexposure, NO dim indoor lighting, NO grey or yellow cast.
Flat naive composition. Subject: 【主体】.

Genuinely crude and childish, like a real 5-year-old who can barely draw — NOT a skilled adult imitating a child: shaky wobbly outlines that wander and don't close; clumsy wrong proportions; lumpy, barely-recognizable shapes; if there is a face, eyes different sizes and a crooked smile.

The CRAYON COLORING must look genuinely real (most important):
- a real kid has NO control over pressure — some strokes pressed hard and dark, others barely touch the paper, with no consistency; waxy build-up in the heavy spots, faint streaks in the light ones, small smudges
- coloring is sparse and scribbly — bare white paper shows THROUGH everywhere, even inside the colored shapes (roughly 50–65% of each colored area left unfilled, white and streaky)
- black crayon is used mainly for the thin wobbly outlines rather than filling big solid areas
- strokes go in different directions, overlapping and broken, like a kid scribbling with no plan; color clearly overflows past the outlines in several places
- bright primary crayon colors (【主色调】, red, yellow, blue, green, orange, pink); absolutely NO smooth even fill, NO gradient, NO blending, NO uniform digital crayon-filter texture
- a wobbly hand-lettered title "【标题词】" in uneven multicolor capital letters on a crooked baseline

Avoid anything cute, polished, symmetric or professionally illustrated. It must look like a genuine photo of a real child's messy, sparse crayon page.
```

---

## 9. 水墨写意

> 纯风格,无内置版式。比例:不传则不注入。占位符 `【主体】` 自动推断。
>
> 命门:墨分五色的浓淡干湿 + 飞白枯笔 + 宣纸渗化(墨晕) + 大量留白 + 一枚朱红印章。最常踩的坑是模型出"均匀灰度数字滤镜"——硬性负向约束必须写死。默认只盖印章不写题字,避免伪中文(若要题款须用户明确给字)。

```
中国传统写意水墨画,画在生宣纸上,纯手绘毛笔笔触,不是数字插画、不是照片。
主体:【主体】。
用墨:以黑墨为主,讲究"墨分五色"——焦、浓、重、淡、清并存,同一笔里有浓淡干湿变化;见飞白枯笔(干笔擦出丝丝露白)与湿墨在宣纸上自然渗化晕开(墨晕),浓淡过渡靠水分,不是均匀灰度。
笔法:写意、概括、一笔成形,寥寥数笔抓住神态,容许偶然的飞溅与断笔;不勾死板轮廓线,不填涂均匀色块。
留白:大量空白宣纸作为画面主体,疏可走马、密不透风,主体偏置一侧,构图空灵。
设色:以水墨为主,至多极少量淡赭石或花青点染;不要浓艳饱和的颜色,不要彩色铺底。
点睛:画面一角一枚小小的朱红方形印章。
纸感:能看出宣纸纤维与墨在纸上微微洇开的质感。
严禁:照片写实、3D、数字矢量、均匀灰度滤镜、平滑渐变、密集琐碎的细节、厚涂、卡通描边、艳俗配色。
```

---

## 10. 复古像素

> 纯风格,无内置版式。比例:不传则不注入。占位符 `【主体】【主色调】` 自动推断。
>
> 命门:硬方块像素 + 统一像素网格 + 有限调色板 + 抖动(dithering)代替渐变 + 零抗锯齿。最常踩的坑是模型出"高清图套像素滤镜"的假像素(柔边、渐变、上千色)——负向约束必须写死。

```
复古像素风(pixel art)插画,像 8-bit / 16-bit 老游戏里的精灵图(sprite),由一颗颗清晰的方形像素手工摆出来,不是高清插画加像素滤镜。
主体:【主体】。
像素:低分辨率观感,所有边缘都是硬朗的方块像素阶梯,像素大小一致、对齐同一网格;绝对没有抗锯齿、没有模糊、没有平滑渐变。
配色:有限调色板(retro 风,约 8–16 色,以【主色调】为主),色块平涂;需要明暗过渡时用"抖动(dithering)"棋盘点阵,而不是渐变。
轮廓:用清晰的深色像素描边或高对比色块区分主体;造型简洁、辨识度高,像素图标 / 游戏角色感。
背景:单一平涂纯色或极简像素背景,不喧宾夺主。
严禁:抗锯齿、柔边、模糊、平滑渐变、高清写实、3D 渲染、矢量光滑曲线、把高清图直接套像素滤镜的假像素感。
```

---

## 11. 情绪叙事淡彩速写

> 纯风格(可选侧边手写中文)。比例:不传则不注入。占位符 `【主体】【橙色关键物】【文字】` 自动推断。
>
> 命门:靛蓝松散速写线(画头发/发髻/圆形/气泡等用来回缠绕的"圈状搜索线"叠画)+ 大面积留白(约六七成纯白、绝大部分只有线不上色)+ **全画只有一处高饱和橙色**点缀(通常是一件关键衣物/物体)+ 脸颊淡腮红 + 情绪抖动线 + 侧边深蓝手写短句。
> 最常踩的坑:模型会①把线画密(排线/交叉线/涂阴影)②把水彩铺满整件衣服③把脸画写实变老④点缀色乱加好几种——四条负向必须写死。多人场景也必须守住"只有一处橙色"。
> `【文字】` 填法:要配文就写"画面留白一侧写 N 行深蓝色手写中文,逐字为:第一行 …… 中文必须清楚可读、不得错字乱码。";不要文字就写"不加任何文字"。中文只写短句最稳,长句或生僻字仍可能翻车(必要时留白后期贴字)。

```
一张情绪叙事风格的极简淡彩速写插画,画在干净白纸上,轻盈通透、略带稚拙的手绘感,不是数字精修插画、不是写实照片、不是水彩习作、不是日系动漫。
主体:【主体】。
线条(最重要):用靛蓝/藏青色钢笔画松弛速写线,线条少而肯定、清爽通透,轮廓偶尔不闭合、带轻微手抖;画头发、发髻、圆形、蓬松或环形的东西时用来回缠绕的圈状"搜索线"叠画,而不是一根干净闭合线;绝不密集排线、绝不交叉排线、绝不用线涂黑或堆阴影。
造型:真人比例与神态,情绪到位、有故事感;大人画得半写实而简约,小孩画得更圆润可爱;都不是Q版大头、不是写实照片、不是动漫脸;脸颊轻点一小块淡淡腮红。
上色(最重要):整幅以大面积白纸留白为主(约六到七成纯白),绝大部分只有蓝线、不上色;只给【橙色关键物】平涂一处高饱和橙色,作为全画唯一的暖色焦点,顶多在个别小处点一点点淡蓝绿;水彩薄、边缘不均匀、可露白,绝不铺满、绝不厚涂、绝不整件深涂。
细节:主体旁寥寥几笔短促抖动线,暗示情绪或动作。
构图:单一主体或场景,主体偏置一侧,另一侧留大量空白,极简。
调性:怀旧、温柔、略带心酸的家庭叙事感,画面干净轻盈。
严禁:密集排线、交叉排线、厚涂、满铺水彩、写实肖像刻画、皱纹与琐碎细节、浓艳配色、多种颜色乱入、3D、照片、日系动漫脸、卡通粗描边、精细背景。
文字:【文字】
```
