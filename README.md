# hand-drawn-styles

> 一套**工具无关**的手绘画风提示词配方。把你想画的内容,套进内置画风,产出可直接复制去喂图像模型的**最终提示词(prompt)**。适用于任意能读自定义指令的 AI Agent——Claude Code、Cursor、Codex CLI、Gemini CLI、Cline、Windsurf 等。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 这是什么

好用的"手绘风"提示词散落各处,每次生图都要翻找、拼凑,还容易把比例、版式等无关约束混进去。

本项目把 **5 种已验证的手绘画风**沉淀成可复用配方。你只管说"画什么",Agent 负责:

- 帮你选画风(没指定就列菜单,指定了就直接用);
- 把你的内容自动填进该画风的提示词模板;
- 按规则处理出图比例(不硬锁);
- 输出一段干净的最终 prompt,复制即用。

**它只产出 prompt 文本,本身不生图**——生图交给你惯用的图像模型(gpt-image、即梦、Midjourney 等皆可)。

## 内置画风

| 编号 | 名称 | 调性 | 英文别名 |
|------|------|------|----------|
| 1 | 纯人类手绘儿童涂色页 | 大人画粗黑线稿 + 孩子填色,真实纸面拍摄感,适合讲故事 / 亲子 | `handmade` `childlike-coloring` |
| 2 | 极简黑白线条讲解漫画(xkcd 火柴人) | 纯细线火柴人、圆角分镜、标题+说明,讲解示意图 | `xkcd` `stickman` `minimal-line` |
| 3 | 蜡笔童涂 | 5 岁小孩用蜡笔画的笨拙"坏画",歪扭出框、引人发笑 | `crayon` `kid-crayon` |
| 4 | 吉卜力风 | 柔和水彩、暖光、治愈梦幻的手绘动画感 | `ghibli` |
| 5 | 小豆人涂鸦信息图 | 黑色圆豆人讲解图,单橙点缀、手绘箭头标注,竖版多格 | `bean` `blob` |
| 6 | MS Paint 烂涂鸦 | 鼠标硬画的病毒级"故意画烂"风(第二个吉卜力),越烂越好笑 | `ms-paint` `bad-doodle` `ugly` |
| 7 | 圆珠笔单线涂鸦 | 黑色圆珠笔缠绕线速写,艺术手稿感,适合肖像 / 动物 | `scribble` `pen-scribble` `ballpoint` |
| 8 | 蜡笔实拍 | 像一张真蜡笔纸的照片,强制露白 / 蜡质笔触,一眼真人手涂(比 #3 更真实) | `real-crayon` `crayon-photo` |

样图与每种画风的示例提示词见 [examples/](examples/)。

| | | | |
|:--:|:--:|:--:|:--:|
| <img src="examples/01-childlike-coloring.png" width="200"><br>**1** 纯人类手绘儿童涂色 | <img src="examples/02-minimal-line.png" width="200"><br>**2** 极简线条 xkcd 火柴人 | <img src="examples/03-crayon.png" width="200"><br>**3** 蜡笔童涂 | <img src="examples/04-ghibli.png" width="200"><br>**4** 吉卜力 |
| <img src="examples/05-bean-doodle.png" width="200"><br>**5** 小豆人信息图 | <img src="examples/06-ms-paint.png" width="200"><br>**6** MS Paint 烂涂鸦 | <img src="examples/07-pen-scribble.png" width="200"><br>**7** 圆珠笔单线涂鸦 | <img src="examples/08-real-crayon.png" width="200"><br>**8** 蜡笔实拍 |

> 每种画风的输入示例与完整提示词见 [examples/](examples/)。

## 接入各 Agent 工具

核心是两个工具无关的文件:[`PROTOCOL.md`](PROTOCOL.md)(执行流程)+ [`STYLES.md`](STYLES.md)(8 段画风配方)。任何 Agent 只要"读到"这两个文件即可。

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
       1. 纯人类手绘儿童涂色页 …
       2. 极简黑白线条漫画手稿 …
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
- 你**没传**:纯风格(1、3、4)不注入任何比例;版式风格(2、5)只注入"竖版多格堆叠"这类软结构提示,不写死数字。

### 占位符自动推断

配方里的 `【主体】【标题词】【主色调】【N】【分镜列表】` 由 Agent 从你的描述里自动推断填好,无需手填。

## 设计原则

- **只产 prompt,不生图**——保持轻量、可移植,不绑定任何图像后端。
- **工具无关**——核心是纯文本协议 + 配方;Claude Code 的 `SKILL.md`、跨工具的 `AGENTS.md` 都只是薄适配层,不重复内容。
- **配方库,而非统一调色板**——每种画风保留它原生的版式 / 结构(如风格 5 的竖版 N 格信息图),忠于已验证的效果,而不是强行抹平成"可互换的滤镜"。
- **不锁比例**——比例是可选参数;版式风格仅给软结构提示,把画布自由度留给用户。

## 目录结构

```
hand-drawn-styles/
├── README.md
├── LICENSE
├── PROTOCOL.md        # 核心协议:选风格 / 比例 / 占位符 / 输出(工具无关)
├── STYLES.md          # 核心配方:5 种画风的提示词模板(工具无关)
├── SKILL.md           # Claude Code 适配层(薄,指向上面两个文件)
├── AGENTS.md          # Codex / Gemini / Cursor 等适配层(薄)
└── examples/          # 样图 + 每种画风的示例提示词
```

## 贡献新画风

欢迎 PR 提交你验证过的画风。一种画风 = 在 `STYLES.md` 增加一段配方 + 在 `PROTOCOL.md` 的菜单、别名表里登记。建议:

- 配方用你实测满意的语言原文(中英不限),不要替换成未验证的措辞;
- 移除比例硬约束(`1:1` / `3:4` 等),交由比例规则处理;
- 把内容相关的部分抽象成 `【占位符】`;
- 在 `examples/` 附 1–2 张该配方的出图样例,便于评审。

## License

[MIT](LICENSE) © liulei
