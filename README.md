# hand-drawn-styles

[![hand-drawn-styles × Infistar.cc 赞助横幅](https://hand-drawn-images.pages.dev/hand-drawn/assets/sponsors/infistar-2026-11-lossless.webp)](https://infistar.ai/register?aff=HANDDRAWNSTYLES&ref_source=link)

hand-drawn-styles × Infistar.cc

低至官方 0.1 折，省 99%；Claude、GPT、Gemini、Grok、DeepSeek 等一个 Key 使用。官方渠道，模型可验真；200+ 模型、16 个品牌，文本、图片、视频一个 Key 全搞定。

hand-drawn-styles 用户通过[专属链接](https://infistar.ai/register?aff=HANDDRAWNSTYLES&ref_source=link)注册直接送 ¥5。

专属链接：[https://infistar.ai/register?aff=HANDDRAWNSTYLES&ref_source=link](https://infistar.ai/register?aff=HANDDRAWNSTYLES&ref_source=link)

---

**23 套手绘与插画画风配方，先看效果，再按编号使用。** 覆盖蜡笔、水墨、线条漫画、水粉绘本、纸雕、像素与软胶潮玩。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

告诉 Agent 要画什么、用哪种画风，它会填入内容、处理比例，输出完整提示词或带参考图的 JSON 调用包。**本项目默认不生图**，由你的图像工具执行。

[全部画风](#全部画风) · [安装](#安装) · [开始使用](#开始使用) · [调用与参考图要求](#调用与参考图要求) · [维护与贡献](#维护与贡献)

## 全部画风

当前共 **23 套**：编号 **1–20、22、23**，另含 **3.1** 变体。21 号已移除，不复用旧编号。点击样图可查看原图；详细输入示例见 [样例页](examples/README.md)，用途与相近画风区别见 [选型说明](docs/style-selection.md)。

<table>
<tr>
<td width="20%" align="center" valign="top">
<strong>1 · 极简黑白线条讲解漫画</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/01-minimal-line.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/01-minimal-line.png" alt="1 极简黑白线条讲解漫画" width="150"></a><br>
<sub>细线火柴人、网格分镜，用于步骤与概念讲解。<br><code>minimal-line</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>2 · 蜡笔童涂</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/02-crayon.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/02-crayon.png" alt="2 蜡笔童涂" width="150"></a><br>
<sub>孩子自己画的笨拙造型，歪线、出框和粗蜡笔。<br><code>crayon</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>3 · 吉卜力风</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/03-ghibli.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/03-ghibli.png" alt="3 吉卜力风" width="150"></a><br>
<sub>柔和水彩、暖光与手绘动画叙事。<br><code>ghibli</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>3.1 · 蜡笔童涂－潦草自画版</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/assets/style-3.1/anchor-family.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/assets/style-3.1/anchor-family.png" alt="3.1 蜡笔童涂－潦草自画版" width="150"></a><br>
<sub>大人歪线稿加孩子乱涂色，明亮白底与亲子动作。<br><code>family-crayon-card</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>4 · 小豆人涂鸦信息图</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/04-bean-doodle.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/04-bean-doodle.png" alt="4 小豆人涂鸦信息图" width="150"></a><br>
<sub>实心黑豆人、单橙点缀与竖向分格。<br><code>bean</code></sub>
</td>
</tr>
<tr>
<td width="20%" align="center" valign="top">
<strong>5 · MS Paint 烂涂鸦</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/05-ms-paint.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/05-ms-paint.png" alt="5 MS Paint 烂涂鸦" width="150"></a><br>
<sub>鼠标硬画的粗糙数字感，故意画得笨拙好笑。<br><code>ms-paint</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>6 · 圆珠笔单线涂鸦</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/06-pen-scribble.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/06-pen-scribble.png" alt="6 圆珠笔单线涂鸦" width="150"></a><br>
<sub>用缠绕线的疏密表现体积，适合肖像与动物。<br><code>pen-scribble</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>7 · 蜡笔实拍</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/07-real-crayon.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/07-real-crayon.png" alt="7 蜡笔实拍" width="150"></a><br>
<sub>像拍下来的儿童蜡笔纸页，保留纸面与蜡质笔触。<br><code>real-crayon</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>8 · 水墨写意</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/08-ink-wash.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/08-ink-wash.png" alt="8 水墨写意" width="150"></a><br>
<sub>毛笔浓淡、飞白与宣纸渗化，保留写意留白。<br><code>ink-wash</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>9 · 复古像素</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/09-pixel-art.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/09-pixel-art.png" alt="9 复古像素" width="150"></a><br>
<sub>硬边方块像素与有限调色板，呈现老游戏观感。<br><code>pixel-art</code></sub>
</td>
</tr>
<tr>
<td width="20%" align="center" valign="top">
<strong>10 · 情绪叙事淡彩速写</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/10-emo-sketch.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/10-emo-sketch.png" alt="10 情绪叙事淡彩速写" width="150"></a><br>
<sub>靛蓝松散速写线、大留白与一处橙色。<br><code>emo-sketch</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>11 · 二维水彩风格</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/11-retro-concept.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/11-retro-concept.png" alt="11 二维水彩风格" width="150"></a><br>
<sub>复古动画概念稿，白纸、粉彩与少量形状阴影。<br><code>retro-concept</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>12 · 暖光童画</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/12-sunlit-storybook.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/12-sunlit-storybook.png" alt="12 暖光童画" width="150"></a><br>
<sub>动画概念水粉笔触，可选留白纸边或满幅场景。<br><code>sunlit-storybook</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>13 · 北欧纸雕</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/13-paper-folk.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/13-paper-folk.png" alt="13 北欧纸雕" width="150"></a><br>
<sub>层叠厚纸、立体纸艺和柔和投影。<br><code>paper-folk</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>14 · 北欧绘本水粉</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/14-nordic-storybook.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/14-nordic-storybook.png" alt="14 北欧绘本水粉" width="150"></a><br>
<sub>整画纸纹、水粉颗粒与低饱和蓝黄。<br><code>nordic-storybook</code></sub>
</td>
</tr>
<tr>
<td width="20%" align="center" valign="top">
<strong>15 · 大鼻软偶</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/15-softnose-vinyl.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/15-softnose-vinyl.png" alt="15 大鼻软偶" width="150"></a><br>
<sub>哑光软胶、夸张垂管鼻与小眼睛潮玩角色。<br><code>softnose-vinyl</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>16 · 聚光水粉立绘</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/16-gouache-spotlight.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/16-gouache-spotlight.png" alt="16 聚光水粉立绘" width="150"></a><br>
<sub>满幅抽象刷底、人物身后聚光晕与夸张比例。<br><code>gouache-spotlight</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>17 · 墨线绘本</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/17-inked-storybook.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/17-inked-storybook.png" alt="17 墨线绘本" width="150"></a><br>
<sub>钢笔墨线定形，轻薄淡彩与局部排线。<br><code>inked-storybook</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>18 · 暖色扁平绘本</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/18-warm-flat-storybook.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/18-warm-flat-storybook.png" alt="18 暖色扁平绘本" width="150"></a><br>
<sub>圆润几何色块、蓝橙对比与流畅动作弧线。<br><code>warm-flat-storybook</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>19 · 圆头红线极简童画</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/assets/style-19/anchor-roundhead-redline.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/assets/style-19/anchor-roundhead-redline.png" alt="19 圆头红线极简童画" width="150"></a><br>
<sub>大圆头、双竖眼、细石墨四肢与珊瑚红。<br><code>roundhead-redline</code></sub>
</td>
</tr>
<tr>
<td width="20%" align="center" valign="top">
<strong>20 · 暖黄墨线情绪小剧场</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/assets/style-20/anchor-warm-yellow-ink-story.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/assets/style-20/anchor-warm-yellow-ink-story.png" alt="20 暖黄墨线情绪小剧场" width="150"></a><br>
<sub>紧凑形体、黑墨排线与芥末黄，聚焦一个动作。<br><code>warm-yellow-ink-story</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>22 · 朱墨写意转绘</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/assets/style-22/anchor-vermilion-ink-wash.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/assets/style-22/anchor-vermilion-ink-wash.png" alt="22 朱墨写意转绘" width="150"></a><br>
<sub>纸白漫画五官、游丝长线、完整墨团与少量朱红。<br><code>vermilion-ink-wash</code></sub>
</td>
<td width="20%" align="center" valign="top">
<strong>23 · 皮影彩染</strong><br>
<a href="https://hand-drawn-images.pages.dev/hand-drawn/examples/23-shadow-puppet.png"><img src="https://hand-drawn-images.pages.dev/hand-drawn/examples/23-shadow-puppet.png" alt="23 皮影彩染：持扇女伶" width="150"></a><br>
<sub>灵感来自：DAAI(@daaihq)</sub><br>
<sub>镂刻偶片、平面铆接、半透明彩染与整幅暖幕光。<br><code>shadow-puppet</code><br><a href="docs/style-23-review.md">试作记录</a></sub>
</td>
<td width="20%"></td>
<td width="20%"></td>
</tr>
</table>

23号采用本轮已认可的持扇女伶图展示；全部23套画风均保留独立效果图。

样图题材不同，用于展示已有画风，不代表同题对照实验或所有场景都已验证。3.1、19、20、22 展示的是正式调用所用画风锚点；审核与隐私记录见 [样例页](examples/README.md) 和各画风说明。

## 安装

使用本页全部 23 套画风（含 22 号朱墨写意转绘与 23 号皮影彩染试作），可让 Agent 从当前源码安装：

```text
帮我安装 https://github.com/threerocks/hand-drawn-styles 的 main 分支，
保留完整 Skill 目录，并运行 scripts/check_skill.py 验证安装。
```

也可以自行浅克隆，避免下载 Git 历史中的旧图片。运行脚本需要 **Python 3.10+**，无需第三方 Python 依赖：

```bash
git clone --depth 1 https://github.com/threerocks/hand-drawn-styles.git
cd hand-drawn-styles
python3 -B scripts/check_skill.py
```

| 工具 | 接入方式 |
| --- | --- |
| Codex | 将完整目录以 `hand-drawn/` 名称放入 `~/.codex/skills/` |
| Claude Code | 将完整目录以 `hand-drawn/` 名称放入 `~/.claude/skills/` |
| Cursor / Gemini CLI / Jules | 让项目规则指向完整目录中的 `AGENTS.md` 和 `PROTOCOL.md` |
| Cline / Windsurf / Continue | 让 rules / custom instructions 指向完整目录中的协议与配方 |
| 直接对话 | 普通文本配方可复制；需要锚点的调用须同时传入真实参考图与完整调用包 |

[Release 轻量安装包](https://github.com/threerocks/hand-drawn-styles/releases/latest/download/hand-drawn-skill.zip) 对应已发布版本，**可能落后于本页 main 分支**；校验文件见 [SHA256SUMS](https://github.com/threerocks/hand-drawn-styles/releases/latest/download/SHA256SUMS)。完整安装与验证方式见 [INSTALL.md](INSTALL.md)。

## 开始使用

### 对 Agent 说清楚内容和画风

中文名、编号或英文别名都可以：

```text
用吉卜力风画一只在下雨天打伞的猫。
用 3 号画风画一只在下雨天打伞的猫。
用 ghibli 画一只在下雨天打伞的猫。
```

“家庭蜡笔画”“亲子手绘”等已登记的自然语言表达直接采用 3.1。未指定画风时，Agent 根据用途提供 2–3 个候选供你选择；用途不清楚时展示完整菜单。指定比例就使用该比例，不指定时不额外锁定数字比例。

### 用脚本输出提示词

```bash
python3 -B scripts/render_prompt.py \
  --style ink-wash \
  --subject '一只鸟停在细枝上' \
  --aspect 3:4
```

其余参数用 `--var '名称=内容'` 填入；完整编号、别名和必需参数可这样查询：

```bash
python3 -B scripts/render_prompt.py --list
python3 -B scripts/render_prompt.py --catalog
```

`--catalog` 另含适用任务、识别差异、限制与来源，仅查询本地文本，不需要图片缓存。配方的唯一真源是 [STYLES.md](STYLES.md)，渲染器原样提取；选型建议不覆盖配方。

### 用 22 号转绘原图

```bash
python3 -B scripts/render_prompt.py \
  --style vermilion-ink-wash \
  --subject '原图人物扶着自行车，保留眼镜、姿态和车架连接' \
  --source-image /absolute/path/source.jpg \
  --text '只保留球衣上的10'
```

22 号采用用户认可的 `sweety-ink-wash v1.1.0` 第一风格，与 8 号传统水墨分开保留。默认返回画风锚点、内容原图和完整 [sweety-image-art-direction 预处理说明](docs/image-art-direction.md)。调用端先执行预处理，再把实际图片按角色传入图像工具：**原图决定内容，锚点决定画法**，不复制锚点中的人物、自行车或号码。选择范围与既有验证见 [迁入记录](docs/style-22-review.md)。

### 用 23 号创作独立皮影

灵感来自：DAAI(@daaihq)

```bash
python3 -B scripts/render_prompt.py --style shadow-puppet \
  --subject '一只白鹤抬起一只脚，展开一侧翅膀' --aspect 3:4
```

23号为 v0.1 首版，无需原片，输出完整皮影画面而非照片对照海报。内部保留轮廓提炼、偶件拆分与颜色选择，成图只呈现半透明彩染偶片和暖幕。默认无字；配色可用 `--var '配色=琥珀黄与橄榄绿'` 指定。来源与试作边界见 [23号记录](docs/style-23-review.md)。

## 调用与参考图要求

普通画风默认输出纯文本；**3.1、19、20、22 默认输出 JSON 调用包**。拿到 JSON 只是完成提示词准备，调用端还须实际传入图片并执行相应流程。

```bash
python3 -B scripts/render_prompt.py \
  --style 3.1 \
  --subject '爸爸把零食袋放回柜子，男孩站在旁边看着' \
  --text '不加任何文字' \
  --aspect 3:4
```

| 画风 | 调用要求 |
| --- | --- |
| 3.1 | 每张携带锚点；执行基础生成、两次递进编辑与独立验收，通过后才可成为 final。准确标题用 `--title`，详见 [验收说明](docs/style-3.1-review.md) |
| 19 | 携带原创锚点，满足调用包中的模型快照与高保真参考要求；按既有审核和硬失败条件放行 |
| 20 | 携带原创锚点，直接生成候选，再执行验收器；失败候选拒收，不用通用风格编辑修补 |
| 22 | 先执行内置美术指导预处理，再传入画风锚点与可选内容原图；核对关键主体、姿态与物件连接 |

3.1、19、20 的候选状态、精确模型要求与放行条件以正式调用包为准。缺参考图、模型能力或审核证据时，停止对应正式调用。3.1/19/20/22 只有显式添加 `--format text --text-only-preview` 才能输出非生产文字预览。

图片托管于 **Cloudflare Pages**。首次使用参考图需要联网下载并校验大小和 SHA-256；有效缓存可离线复用。2026-10-23，图库全部 77 张图片已通过匿名下载校验，运行所需 6 张参考图已通过空缓存下载验证。图片迁移不改变历史隐私审计与视觉审核结论。

工程检查、实际看图审核和用户认可分别记录。历史样图的证据范围、三组相近画风的差异与失败案例见 [画风对照](docs/style-comparison.md)；其中规划的小规模同题实验尚未执行。

## 维护与贡献

```bash
python3 -B scripts/hosted_images.py fetch
python3 -B -m unittest discover -s scripts -p 'test_*.py'
python3 -B scripts/check_skill.py
python3 -B scripts/build_skill_package.py
```

构建脚本在独立目录解压并验证全部画风，成功才标为 `verified`；默认产物 `dist/hand-drawn-skill.zip` 不含图片且不超过 1 MiB。`--skip-verify` 仅生成候选包。

`HAND_DRAWN_IMAGE_CACHE` 指定图片缓存；`HAND_DRAWN_OFFLINE=1` 禁止自动下载。业务项目提供内容、准确文字、比例和可选角色参考，不另写一套画风配方。

新增画风须固定参考图、同构与跨主体场景，记录判定依据和可复核候选；新增图片须先完成隐私清理、登记、完整图库部署与匿名校验。完整规则见 [AGENTS.md](AGENTS.md) 和 [图片托管说明](docs/image-hosting.md)。

| 文件 / 目录 | 内容 |
| --- | --- |
| [STYLES.md](STYLES.md) | 全部配方的唯一真源 |
| [PROTOCOL.md](PROTOCOL.md) | 选型、参数与输出协议 |
| [SKILL.md](SKILL.md) / [AGENTS.md](AGENTS.md) | Skill 与跨工具入口 |
| [catalog/](catalog/) / [docs/](docs/) | 选型数据、对照、验收与托管说明 |
| [scripts/](scripts/) | 渲染、验收、安装、打包与检查 |
| [assets/image-manifest.json](assets/image-manifest.json) | 图片地址、大小和 SHA-256 |
| [examples/](examples/) / [benchmarks/](benchmarks/) | 编号样例与历史研发记录，不进入轻量包 |

## License

[MIT](LICENSE) © liulei
