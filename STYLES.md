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

## 1.1 儿童涂色页-低饱和克制版

> #1 的变体。纯风格(可选顶部手写中文标题)。比例:不传则不注入。占位符 `【主体】【文字】` 自动推断。
>
> 和 #1 的区别:在"大人粗黑线稿 + 孩子填色"基础上,加了两条更硬的纪律——①**极简留白背景**(只留一条地面线 + 极少线索,不画完整场景)②**低饱和 ≤4 色 + 单一橙红强调色**(冷静叙事感,不再是 #1 的自由多色)。
> 命门:gpt-image 会自动把线画得又稳又漂亮、把脸画成商业绘本萌娃、把色填得又满又匀——三条负向(线要糙抖/脸要笨/色要露白越界)必须写死,否则出"精致插画"而不是"普通人亲手糙画"。
> `【文字】` 填法:要标题就写"画面顶部写手写中文标题,逐字为 …… 像儿童绘本手写字,笔画粗圆钝、轻重不均、结构宽松,但必须准确可读,不要乱码错字伪文字";不要就写"不加任何文字"。

```
白纸上的纯人类手绘儿童涂色画,不是数字插画、不是插画师作品、不是商业绘本。画面结构是"普通大人徒手画的粗黑涂色线稿 + 5-8 岁儿童自己填色"。
主体:【主体】。
线稿(最重要):粗黑马克笔外轮廓,是普通大人徒手画的、不是插画师——线条粗细明显不匀、明显抖动歪扭、好几处描了两三遍留下重复线、拐角接不齐有豁口或出头;圆形、家具腿、桌边都不许画标准,透视可以是错的,主体可以偏离中心。内部细线越少越好,绝不允许细密漂亮稳定的线稿。
脸/造型:人物比例儿童画式简化——头略大、手脚简单;五官简单甚至有点笨,眼睛就是小圆点、嘴一条线,不要大眼睛萌脸、不要卡通可爱、不要商业绘本脸;头发、衣褶不许画精细。
填色(最重要):彩笔/蜡笔儿童式乱涂——每个主要色块都留下大片没涂到的白(约 25%–35% 露白)、深浅明显不匀、有断续笔画和乱方向;必须有 2–3 处颜色明显涂到黑线外面(越界约 1–5mm),且出现在头发、衣服等一眼看得见的地方,不是只在边缘做毛刺。
背景:极简,只有一条歪歪的地面线加极少线索,不要完整装修、不要家具堆叠、不要漂亮细节。
纸面:亮白真实纸,少量不规律褶皱、压痕与纸纤维感,大量留白,不要满屏纸纹滤镜。
配色(严格):低到中饱和,像蜡笔轻涂;全页有彩色不超过 4 种,不要艳丽纯色、不要多色平均用力;典型用色可从雾蓝、暖棕木色、芥末黄、豆沙粉紫里挑(压住的低饱和色);强调色只有一个=橙红,每页最多出现一处,只用于情绪焦点或关键道具(脸颊红晕、红圈、关键小物、橘色小动物)。
严禁:平滑稳定等粗的数字线稿、完美圆、完美透视、完美对称、商业绘本精致可爱人物、渐变、阴影建模、3D、体积光、颜色平滑均匀填满、均匀蜡笔噪点滤镜、背景装修完整。整体像普通人随手画在纸上的投稿,笨拙、不完美、有明显手误,不是 AI 手绘滤镜。
文字:【文字】
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

## 3.1 蜡笔童涂-潦草自画版

> #3 的变体。纯风格(可选顶部手写中文标题)。比例:不传则不注入。占位符 `【主体】【文字】` 自动推断。
>
> 和 #3 的区别:#3 是"画得歪但还认得出主体"的坏画;3.1 更极端——**整张像 5-6 岁孩子完全自己画的简笔画**(大圆脸、点眼睛、火柴四肢、土豆身子),再叠一层**低饱和 ≤4 色 + 单一橙红强调色**的配色纪律。比 #3 更潦草、更冷静。
> 命门:同 [#3](#3-蜡笔童涂5岁小孩坏画),模型爱把它画精致——脸/线/涂色三处都要压烂;配色纪律必须写死,否则出彩虹多色。
> `【文字】` 填法:要标题就写"画面顶部写手写中文标题,逐字为 …… 像认真写字的儿童笔迹,笔画粗、歪歪扭扭、大小不一,但每个字必须准确可读,不要乱码错字伪文字";不要就写"不加任何文字"。

```
白纸上的一张画,整张画像一个 5-6 岁孩子完全自己画的——孩子自己起稿自己涂,不是大人画的线稿。
主体:【主体】。
造型:所有人物都是儿童简笔画——大圆脸、两个点当眼睛、一条线当嘴,身体是歪歪的方块或土豆形,手脚是细线条,手指画成小叉子或干脆不画;头身比例失调(头大)。家具画得歪歪扭扭、腿长短不一、透视错误;物件简化成歪方块和圆圈。
线条:严重抖动、断线、接不上、重复描;蜡笔涂色大面积涂出边界、大量露白、有蜡笔戳点、乱向来回涂;构图偏斜,东西大小随意。
纸面:亮白真实纸,少量褶皱,大量留白。
配色(严格):低到中饱和,像蜡笔轻涂;全页有彩色不超过 4 种,不要艳丽纯色、不要多色平均用力;典型用色可从雾蓝、暖棕木色、芥末黄、豆沙粉紫里挑;强调色只有一个=橙红,每页最多一处,只用于情绪焦点或关键道具。
严禁:精致可爱绘本脸、稳定线条、均匀涂色、正确透视、完整背景、渐变、3D、彩虹式多色。整体要像孩子自己画的画,不是插画师作品、不是 AI 手绘滤镜。
文字:【文字】
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

---

## 12. 复古动画概念稿

> 纯风格。比例:不传则不注入。占位符 `【主体】【背景浓度】【焦点物件】【构图】【文字】` 自动推断:【背景浓度】默认"白纸上人物身后一侧轻扫几笔淡奶油/杏色干刷痕"(可从"几乎全白"到"七成琥珀晕染"按情绪调),【焦点物件】默认"无"(指定则该物件成为全画唯一高饱和暖色区),【构图】默认"单人或双人半身立绘,视线亲和"。
>
> 命门(2026-07-13 同题四图对照 OscarAI 标杆 v4 定稿):**①白纸高调**——纸底几乎是白的,背景只有干刷扫痕,绝不满铺(除非指定高浓度)、绝不画光环圈;**②奶白透粉的脸+桃色形状阴影**——肤色绝不能偏深,但脸也不能留成纸白:整脸罩淡桃色暖光,颧骨/眼窝/鼻侧/下巴底/脖子下用边缘略干脆的大块 form shadow 塑形(复古海报式),不做柔和体积渲染;**③少画多留**——衣服=干湿水粉大块平扫+两三根定型线,大量露纸,禁纽扣缝线细节;**④粉彩+单点强色**——全画低中饱和粉彩(粉蓝/长春花蓝,不是深钴蓝),只有【焦点物件】一处高饱和。
> 最常踩的坑:①背景涂满变"黄底画"、肤色画成小麦色(第一版翻车原因,画面立刻闷脏)②脸留纸白没有暖光(粉笔感)③衣服涂满加细节④到处高饱和。试色块/铅笔外框线不是本风格要素,不要加。
> 出身:1950s 美式中古动画(Disney/UPA 血统)概念设定稿;天然适配 i2v 动画(角色立绘即动画锚图);多角色跨张一致性靠写死发型+服色。

```
一张1950年代美式中古动画(mid-century Disney/UPA 血统)的角色概念画,传统水粉+彩铅在白纸上的手绘质感,不是3D渲染、不是矢量插画、不是数字厚涂、不是照片。
主体:【主体】。
高调画面(最重要):整幅是明亮的高调(high-key)画面,纸底几乎就是白的——背景大面积留白露纸,背景晕染按【背景浓度】执行,但笔触必须是干刷扫痕(方向可见、边缘毛糙),绝不均匀填色、绝不在人物四周画出一圈"光环"。
肤色与面部光(最重要):底色是极浅的奶白透粉(绝不是小麦色/古铜色),但脸绝不能留成纸白——整张脸罩一层淡淡的桃色暖光,并用干净的大块桃粉色形状阴影(form shadow)塑形:颧骨侧面、眼窝、鼻侧、下巴底、脖子下方各一块,阴影边缘略干脆像复古海报,不做柔和渐变;额头和鼻梁留最亮;鼻尖、脸颊、耳朵点粉橙腮红。
脸部造型:图形化极简——眼睛大而明亮(琥珀色/棕色虹膜几乎占满眼眶,上眼睑一道粗深色睫毛线,一个小圆高光),鼻子小而尖,嘴就是一条极简的曲线;眉毛粗黑有表情。
衣服(少画多留):干湿结合的水粉大块平扫——颜色可以饱满湿润、同一色块里有明显深浅笔触变化,但边缘毛糙露纸、局部扫白,加两三根深色定型线勾出领口翻领;下缘笔触扫散融进白纸;绝不涂满到边、绝不画纽扣缝线口袋等细节。
线条:深棕色软彩铅/炭笔线,只在头发丝、五官、领口局部收形,松而断续;没有整圈外轮廓线、没有铅笔框、没有试色块。
配色:全画低到中饱和的粉彩调——粉蓝/长春花蓝(不是深钴蓝)、奶油、杏色、暖棕;深色只出现在头发/眉毛/领带/睫毛线,做全画的明度锚点。焦点物件:按【焦点物件】指定——该物件用高饱和暖色湿润厚涂,是全画唯一的高饱和区;若为"无",全画保持粉彩。
质感:干刷水粉,颜料薄、纸纹隐约透出,色块边缘毛糙露纸,像画在热压水彩纸上。
构图:【构图】。
严禁:满铺背景、光环圈、深肤色、体积感渲染、3D、厚涂油亮、细节堆砌、纽扣缝线、外框线、试色块、深钴蓝、日系动漫脸。
文字:【文字】
```

---

## 13. 暖光童画(动画概念暖绘)

> 纯风格。比例:不传则不注入。占位符 `【主体】【背景元素】【构图】【文字】` 自动推断:【背景元素】默认为空(整个占位符直接删掉);要加景物时填成英文接续短语,如" and sketchy green plant strokes"(必须是这类松散干刷笔触,保持概念稿式潦草),【构图】默认"waist-up portrait"半身像,【文字】默认"No text anywhere."。
>
> 出身:Midjourney 双 --sref 组合画风的 gpt-image 复刻(2026-07-16 四张标杆图对照定稿)。本质是"现代动画电影视觉开发稿(vis-dev)× 绘本水粉":大眼大虹膜角色 + 蓬软发团飞丝 + 青蓝×橙红互补 + 干擦留白纸边,Pixar/Disney 概念设定稿气质。天然适配角色立绘、故事绘本、i2v 动画锚图。
> 命门(第一版翻车点,三条都必须写死):**①头发**必须写"少数大块柔软体积 + 轮廓上叠少量单根飞丝",否则出满头细密小卷,画面变琐碎;**②脸部渲染**必须写"干净柔滑、皮肤禁画布纹理",纹理只许留在背景和衣服,否则全画油画布纹路过重;**③虹膜**必须写"占满眼眶、只留眼角少量眼白",否则眼白过多神韵全失。**④身份特征**:四边露白纸的"未画完"边框 + 粉蓝底奶油黄干擦背景,这两样丢了就不是这个风格。
> 模板为已验证的英文原文,不要转译成中文(转译等于换了一套未验证配方)。

```
Character concept art in a modern animated-feature visual-development style, painterly digital gouache illustration.
Subject: 【主体】, 【构图】.
STYLE RECIPE (follow exactly): digital gouache painting with soft clean rendering on the face (smooth soft airbrushed shading, NO canvas texture on the skin), while the background and clothing keep loose visible dry-brush strokes; background is loosely scumbled pastel sky-blue with soft cream-yellow dry-brush patches【背景元素】, deliberately unfinished with raw white paper showing around the border like a concept sketch; EYES: enormous round expressive eyes, the dark irises are VERY large and fill most of the eye with only small white sclera corners, one bright white highlight dot per eye, thick dark painterly upper lash line, bold expressive eyebrows; tiny pointed chin, slender neck, rosy blush cheeks, subtle freckles; HAIR: painted as a few BIG soft volumetric masses with simple smooth shading (NOT detailed ringlet curls), then a moderate number of fine individual flyaway strands drawn on top of the silhouette, warm golden rim light glowing on the hair edges; palette: complementary teal and denim blue against warm orange, soft pastel overall, gentle warm lighting, storybook charm, Pixar-Disney visual development art quality.
【文字】
```

---

## 附录 A · 实拍纸质感增强层(可叠加)

> 2026-07-13 经 Midjourney V7 标杆对照实测定稿(全过程见 `benchmarks/`)。适用对象:一切"画在纸上"的画风——#1/#1.1/#3/#3.1/#8 直接叠加;#11 用文末轻量版;#4/#9/#10 等非纸面画风不适用。
> 背景:gpt-image 默认出"干净数字纸+均匀笔触",与真实纸上画作的差距集中在**纸的摄影感**(纸纹牙口、蜡质结块反光、运笔压力深浅、蹭脏痕)。把下面这段**整段追加**在画风配方之后,即可把材质拉到接近 MJ 实拍水准,同时保留 gpt-image 的叙事服从优势。
> 用法:整段照抄追加,禁止转写精简;与配方原有的"纸面"行冲突时以本层为准。

```
【材质增强层·最重要】整张图必须像"用手机在明亮柔和日光下拍摄的、画在真实纸上的画作照片",不是数字图:
- 纸面有微距可见的纸纹颗粒(纸的凹凸牙口),纸有轻微起伏和一两道很淡的折痕;
- 颜料有真实材料感:蜡笔/彩笔重压处颜料结块、有轻微蜡质反光,轻扫处颜料只挂在纸纹凸起上、露出大量纸白点;马克笔线有渗墨感,起笔收笔略粗;
- 每个色块内部深浅明显不均,能看清一笔一笔的运笔方向、起笔收笔和折返;
- 笔画边缘因纸面凹凸而毛糙断续,不是干净的边;
- 纸上有极少量真实使用痕迹:一两处轻微蹭脏或指蹭痕;
- 光照:明亮均匀,白纸干净发亮,只有极淡的纸面起伏阴影,无暗角。
严禁:均匀的数字噪点滤镜、平滑均匀填色、干净矢量线、任何数字插画感。
```

**#11 淡彩速写专用轻量版**(整层太重会破坏其轻盈感,只加两句):

```
画在带细腻纸纹颗粒的白色水彩纸上(纸的牙口微距可见,笔线穿过纸纹微微断续);水彩颜料在纸纹里有细小沉淀颗粒。
```
