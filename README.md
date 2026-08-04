# hand-drawn-styles

> 一套**工具无关**的手绘画风提示词配方。把你想画的内容,套进内置画风,产出可直接复制去喂图像模型的**最终提示词(prompt)**。适用于任意能读自定义指令的 AI Agent——Claude Code、Cursor、Codex CLI、Gemini CLI、Cline、Windsurf 等。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 这是什么

好用的"手绘风"提示词散落各处,每次生图都要翻找、拼凑,还容易把比例、版式等无关约束混进去。

本项目把 **18 种已验证的整数编号画风 + 1 个稳定变体(3.1),共 19 套配方**沉淀成可复用配方。你只管说"画什么",Agent 负责:

- 帮你选画风(没指定就列菜单,指定了就直接用);
- 把你的内容自动填进该画风的提示词模板;
- 按规则处理出图比例(不硬锁);
- 输出一段干净的最终 prompt,复制即用。

**它只产出 prompt 文本,本身不生图**——生图交给你惯用的图像模型(gpt-image、即梦、Midjourney 等皆可)。

## 内置画风

> 八大分组:**拟真手绘**(3/3.1/7/10)· **线条·讲解·速写**(1/4/6)· **故意画烂**(2/5)· **传统·复古质感**(8/9)· **动画·概念设定**(11/12/16/17)· **纸艺·立体手工**(13)· **绘本·扁平与北欧**(14/18)· **3D·潮玩**(15)。现有编号为 1–18，另含稳定变体 3.1，共 19 套配方。

| 组 | 编号 | 名称 | 调性 | 英文别名 |
|----|------|------|------|----------|
| 线条讲解 | 1 | 极简黑白线条讲解漫画(xkcd 火柴人) | 纯细线火柴人、圆角分镜、标题+说明,讲解示意图 | `xkcd` `stickman` `minimal-line` |
| 故意画烂 | 2 | 蜡笔童涂 | 5 岁小孩用蜡笔画的笨拙"坏画",歪扭出框、引人发笑 | `crayon` `kid-crayon` |
| 拟真手绘 | 3 | 吉卜力风 | 柔和水彩、暖光、治愈梦幻的手绘动画感 | `ghibli` |
| 拟真手绘 | 3.1 | 蜡笔童涂-潦草自画版 | 普通大人歪线稿 + 孩子粗乱蜡笔涂抹,固定小点眼红脸蛋、明亮白底和大留白;正式生产强制锚点与三阶段 workflow | `rawkid` `kid-scrawl` `stick-kid` `family-crayon-card` |
| 线条讲解 | 4 | 小豆人涂鸦信息图 | 黑色圆豆人讲解图,单橙点缀、手绘箭头标注,竖版多格 | `bean` `blob` |
| 故意画烂 | 5 | MS Paint 烂涂鸦 | 鼠标硬画的病毒级"故意画烂"风,越烂越好笑 | `ms-paint` `bad-doodle` `ugly` |
| 线条讲解 | 6 | 圆珠笔单线涂鸦 | 黑色圆珠笔缠绕线速写,艺术手稿感,适合肖像 / 动物 | `scribble` `pen-scribble` `ballpoint` |
| 拟真手绘 | 7 | 蜡笔实拍 | 像一张真蜡笔纸的照片,强制露白 / 蜡质笔触,一眼真人手涂 | `real-crayon` `crayon-photo` |
| 传统复古 | 8 | 水墨写意 | 毛笔黑墨、墨分五色、飞白留白、朱红印章,中国画手绘感 | `ink-wash` `ink` `shuimo` `chinese-painting` |
| 传统复古 | 9 | 复古像素 | 8/16-bit 老游戏精灵图,硬方块像素、有限调色板、零抗锯齿 | `pixel` `pixel-art` `8-bit` `16-bit` |
| 拟真手绘 | 10 | 情绪叙事淡彩速写 | 靛蓝松散速写线 + 大片留白 + 全画一处橙色点缀,催泪家庭故事感 | `emo-sketch` `story-sketch` `watercolor-sketch` `light-watercolor` |
| 动画概念 | 11 | 二维水彩风格(复古动画概念稿) | 1950s 中古动画概念设定稿:水粉厚涂+奶油暖底光晕+橙蓝互补+铅笔起稿线 | `retro-concept` `mid-century` `concept-art` `gouache-concept` |
| 动画概念 | 12 | 暖光童画(动画概念暖绘) | 现代动画 vis-dev 水粉童画:大眼大虹膜+蓬软发团飞丝+青橙互补+干擦留白纸边 | `sunlit-storybook` `vis-dev` `storybook-visdev` |
| 纸艺立体 | 13 | 北欧纸雕 | 层叠纸雕塑+斯堪的纳维亚民俗+暖调珠宝色编辑设计 | `paper-folk` `papercraft` `nordic-papercraft` `quilling` |
| 绘本北欧 | 14 | 北欧绘本水粉 | 整画纸纹+大留白、丹宁蓝×芥末黄低饱和、极简小点眼人物 | `nordic-storybook` `scandi-gouache` `scandinavian-storybook` `soft-gouache` |
| 3D潮玩 | 15 | 大鼻软偶 | 光滑哑光软胶+超大垂管鼻+眯缝小眼+街头穿搭 | `softnose` `softnose-vinyl` `bignose-toy` `vinyl-toy` `art-toy` |
| 动画概念 | 16 | 聚光水粉立绘 | 满幅单色刷底+人物身后聚光晕+夸张比例大眼角色 | `gouache-spotlight` `spotlight-gouache` `character-spotlight` |
| 动画概念 | 17 | 墨线绘本 | 钢笔速写线稿×绘本淡彩,墨线定形、轻薄透亮上色 | `inked-storybook` `ink-storybook` `sketch-storybook` |
| 绘本扁平 | 18 | 暖色扁平绘本 | 圆润几何大色块+几乎无外轮廓线,蓝橙限定色板+暖白大留白 | `warm-flat-storybook` `flat-storybook` `geometric-storybook` `warm-flat` |

样图与每种画风的示例提示词见 [examples/](examples/)。

| | | | |
|:--:|:--:|:--:|:--:|
| <img src="examples/01-minimal-line.png" width="200"><br>**1** 极简线条 xkcd 火柴人 | <img src="examples/02-crayon.png" width="200"><br>**2** 蜡笔童涂 | <img src="examples/03-ghibli.png" width="200"><br>**3** 吉卜力 | <img src="assets/style-3.1/anchor-family.png" width="200"><br>**3.1** 蜡笔童涂-潦草自画版 |
| <img src="examples/04-bean-doodle.png" width="200"><br>**4** 小豆人信息图 | <img src="examples/05-ms-paint.png" width="200"><br>**5** MS Paint 烂涂鸦 | <img src="examples/06-pen-scribble.png" width="200"><br>**6** 圆珠笔单线涂鸦 | <img src="examples/07-real-crayon.png" width="200"><br>**7** 蜡笔实拍 |
| <img src="examples/08-ink-wash.png" width="200"><br>**8** 水墨写意 | <img src="examples/09-pixel-art.png" width="200"><br>**9** 复古像素 | <img src="examples/10-emo-sketch.png" width="200"><br>**10** 情绪叙事淡彩速写 | <img src="examples/11-retro-concept.png" width="200"><br>**11** 二维水彩风格 |
| <img src="examples/12-sunlit-storybook.png" width="200"><br>**12** 暖光童画 | <img src="examples/13-paper-folk.png" width="200"><br>**13** 北欧纸雕 | <img src="examples/14-nordic-storybook.png" width="200"><br>**14** 北欧绘本水粉 | <img src="examples/15-softnose-vinyl.png" width="200"><br>**15** 大鼻软偶 |
| <img src="examples/16-gouache-spotlight.png" width="200"><br>**16** 聚光水粉立绘 | <img src="examples/17-inked-storybook.png" width="200"><br>**17** 墨线绘本 | <img src="examples/18-warm-flat-storybook.png" width="200"><br>**18** 暖色扁平绘本 | |

> 每种画风的输入示例与完整提示词见 [examples/](examples/)。

## 接入各 Agent 工具

核心是工具无关的 [`PROTOCOL.md`](PROTOCOL.md)(执行流程)+ [`STYLES.md`](STYLES.md)(画风配方)。对风格 3.1,还必须保留 `assets/style-3.1/anchor-family.png`;正式生产建议安装完整仓库,不要只复制文本片段。

```bash
git clone https://github.com/threerocks/hand-drawn-styles.git
```

| 工具 | 接入方式 |
|------|----------|
| **Claude Code** | 整个仓库作为 skill:`git clone <repo> ~/.claude/skills/hand-drawn`。`SKILL.md` 会被自动识别并触发。 |
| **Cursor** | 把 `PROTOCOL.md` + `STYLES.md` 放进项目 `.cursor/rules/`(或拷进 `.cursorrules`)。 |
| **Codex CLI / Gemini CLI / Jules** | 把 `AGENTS.md`(或 `GEMINI.md`)指向本仓库的 `PROTOCOL.md` + `STYLES.md`,或直接拷进你项目的 `AGENTS.md`。 |
| **Cline / Windsurf / Continue** | 把 `PROTOCOL.md` + `STYLES.md` 内容并入各自的 rules / custom instructions。 |
| **任意其他工具 / 直接对话** | 把这两个文件的内容粘进系统提示词 / 规则文件即可。 |

接入后,说"用手绘风画……"或"用吉卜力风画……"就能触发。

## 用法要点

### 不指定画风 → 列菜单让你选

```
你：用手绘风画一只在下雨天打伞的猫
Agent：请选择画风(回复编号或名字)：
       1. 极简黑白线条漫画手稿 …
       2. 蜡笔童涂 …
       …
```

### 显式指定 → 中文名 / 编号 / 英文别名,任一即可

```
用吉卜力风画一只在下雨天打伞的猫
用 3 号画风画……
用 ghibli 画……
```

### 出图比例(不硬锁)

- 你**传了**比例(如 `16:9` / 竖版 / 方图)→ 用你的。
- 你**没传**:纯风格(2、3、3.1、5…18)不注入任何比例;版式风格(1、4)只注入"多格网格"或"竖版多格堆叠"这类软结构提示,不写死数字。

### 占位符自动推断

配方里的 `【主体】【标题词】【主色调】【N】【分镜列表】` 由 Agent 从你的描述里自动推断填好,无需手填。

### 稳定生产调用(推荐)

能运行 Python 时,用渲染器原样提取配方,避免 Agent 自行缩写或混配:

```bash
python3 scripts/render_prompt.py \
  --style 3.1 \
  --subject '爸爸把零食袋放回柜子,男孩站在旁边看着' \
  --text '不加任何文字' \
  --aspect 3:4 \
  --format json
```

风格 3.1 默认输出 `family-crayon-card-v3` 正式 JSON,其中包含 `prompt`、输入回放信息、每张必传的 `references` 与强制三阶段 `workflow`:基础生成后依次执行 `scribble-correction` 和 `scribble-chaos-correction`,前两阶段都只是中间图,第三阶段输出才是 final。锚点会校验固定尺寸和解码后的像素 SHA-256,元数据变化不改变画风身份。业务项目只负责内容、准确标题、比例和可选角色参考,不得再维护第二套线条、五官、配色、纸面或涂抹修正规则。无字页用 `--text '不加任何文字'`,有标题用 `--title '准确标题原文'`;纯文本只允许显式 `--format text --text-only-preview`,不得用于正式生图。

## 设计原则

- **只产 prompt 或正式调用包,不生图**——保持轻量、可移植,不绑定任何图像后端。
- **工具无关**——核心是纯文本协议 + 配方;Claude Code 的 `SKILL.md`、跨工具的 `AGENTS.md` 都只是薄适配层,不重复内容。
- **配方库,而非统一调色板**——每种画风保留它原生的版式 / 结构(如风格 5 的竖版 N 格信息图),忠于已验证的效果,而不是强行抹平成"可互换的滤镜"。
- **不锁比例**——比例是可选参数;版式风格仅给软结构提示,把画布自由度留给用户。

## 目录结构

```
hand-drawn-styles/
├── README.md
├── LICENSE
├── PROTOCOL.md        # 核心协议:选风格 / 比例 / 占位符 / 输出(工具无关)
├── STYLES.md          # 核心配方:18 种整数编号画风 + 3.1 变体(工具无关)
├── SKILL.md           # Claude Code 适配层(薄,指向上面两个文件)
├── AGENTS.md          # Codex / Gemini / Cursor 等适配层(薄)
├── assets/            # 需要参考锚点的稳定画风资产
├── scripts/           # 无改写配方渲染器与回归测试
└── examples/          # 样图 + 每种画风的示例提示词
```

## 贡献新画风

欢迎 PR 提交你验证过的画风。一种画风 = 在 `STYLES.md` 增加一段配方 + 在 `PROTOCOL.md` 的菜单、别名表里登记。建议:

- 配方用你实测满意的语言原文(中英不限),不要替换成未验证的措辞;
- 移除比例硬约束(`1:1` / `3:4` 等),交由比例规则处理;
- 把内容相关的部分抽象成 `【占位符】`;
- 在 `examples/` 附 1–2 张该配方的出图样例,便于评审。
- 新增或升级画风时至少验证“参考图同构场景 + 一个跨主体场景”;维护者可按 `AGENTS.md` 的验证例外调用图像模型,但最终入库样图必须先完成隐私元数据清理与审计。

## License

[MIT](LICENSE) © liulei
