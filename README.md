# hand-drawn-styles

hand-drawn-styles 是一套**工具无关的手绘画风提示词配方**。把想画的内容套进内置画风，就能得到可直接交给图像模型使用的最终提示词（prompt）。

适用于能读取自定义指令的 AI Agent，包括 Claude Code、Cursor、Codex CLI、Gemini CLI、Cline、Windsurf 等。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**默认安装：[下载轻量包 hand-drawn-skill.zip](https://github.com/threerocks/hand-drawn-styles/releases/latest/download/hand-drawn-skill.zip)**（约 9.5 MiB）。包含全部 21 套配方、运行脚本和必要参考图。完整仓库用于维护与查看样图，安装 Skill 使用轻量包即可。

## 这是什么

常用的手绘风格集中在一个配方库里，不用每次生图都重新翻找、拼凑提示词。

- **常用画风，随时取用**：按编号、中文名或英文别名调用，配方和样图放在一起，方便挑选。
- **围绕原始内容补充画风**：把主体、动作、文案等内容要求填入配方，减少反复拼接提示词的工作。
- **固定配方，减少漂移**：复用已验证的画风描述，通过渲染器原样提取，减少临时改写带来的风格变化。
- **只处理画风相关的事**：负责选画风、填入内容和输出提示词，不接管文章写作、发布等无关流程。

本项目收录 **20 种已验证的整数编号画风，以及稳定变体 3.1，共 21 套配方**。只需说明“画什么”，Agent 就会：

- 使用指定的画风；未指定时，列出菜单供选择；
- 将内容要求填入对应配方，并按规则处理比例；
- 输出干净的最终 prompt，方便整段复制。

**默认只输出提示词，不生图。** 生图交给惯用的图像模型，例如 gpt-image、即梦或 Midjourney。需要参考锚点的画风在正式生产时会输出 JSON 调用包，须由支持相应参考图和流程的工具执行，详见下文“稳定生产调用”。

## 安装 Skill

直接把下面这句话发给 Agent 工具：

```markdown
帮我安装这个 Skill 的轻量包：https://github.com/threerocks/hand-drawn-styles/releases/latest/download/hand-drawn-skill.zip
解压后保留 hand-drawn/ 的完整目录结构，并运行 scripts/check_skill.py 验证安装。
```

优先下载 [Release 轻量包](https://github.com/threerocks/hand-drawn-styles/releases/latest/download/hand-drawn-skill.zip)，解压后保留 `hand-drawn/` 的目录结构。轻量包不包含 Git 历史、展示图库或研发对照图。安装方式与检查命令见 [INSTALL.md](INSTALL.md)；完整文件校验值见 [SHA256SUMS](https://github.com/threerocks/hand-drawn-styles/releases/latest/download/SHA256SUMS)。需要从源码安装时，可使用下文的部分克隆命令。

## 内置画风

> 八大分组:**拟真手绘**(3/3.1/7/10)· **线条·讲解·速写**(1/4/6/19/20)· **故意画烂**(2/5)· **传统·复古质感**(8/9)· **动画·概念设定**(11/12/16/17)· **纸艺·立体手工**(13)· **绘本·扁平与北欧**(14/18)· **3D·潮玩**(15)。现有编号为 1–20，另含稳定变体 3.1，共 21 套配方。

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
| 线条速写 | 19 | 圆头红线极简童画 | 大圆头双竖眼+极细石墨四肢+黑红白限色+大留白;正式生产强制原创锚点、模型快照和拒收检查 | `roundhead-redline` `redline-roundhead` `graphite-redline` |
| 线条速写 | 20 | 暖黄墨线情绪小剧场 | 暖白负空间+干性黑墨排线+芥末黄+淡腮红+单动作情绪叙事;正式生产强制原创锚点和失败关闭验收 | `warm-yellow-ink-story` `yellow-ink-story` `mustard-ink-story` |

样图与每种画风的示例提示词见 [examples/](examples/)。

| | | | |
|:--:|:--:|:--:|:--:|
| <img src="examples/01-minimal-line.png" width="200"><br>**1** 极简线条 xkcd 火柴人 | <img src="examples/02-crayon.png" width="200"><br>**2** 蜡笔童涂 | <img src="examples/03-ghibli.png" width="200"><br>**3** 吉卜力 | <img src="assets/style-3.1/anchor-family.png" width="200"><br>**3.1** 蜡笔童涂-潦草自画版 |
| <img src="examples/04-bean-doodle.png" width="200"><br>**4** 小豆人信息图 | <img src="examples/05-ms-paint.png" width="200"><br>**5** MS Paint 烂涂鸦 | <img src="examples/06-pen-scribble.png" width="200"><br>**6** 圆珠笔单线涂鸦 | <img src="examples/07-real-crayon.png" width="200"><br>**7** 蜡笔实拍 |
| <img src="examples/08-ink-wash.png" width="200"><br>**8** 水墨写意 | <img src="examples/09-pixel-art.png" width="200"><br>**9** 复古像素 | <img src="examples/10-emo-sketch.png" width="200"><br>**10** 情绪叙事淡彩速写 | <img src="examples/11-retro-concept.png" width="200"><br>**11** 二维水彩风格 |
| <img src="examples/12-sunlit-storybook.png" width="200"><br>**12** 暖光童画 | <img src="examples/13-paper-folk.png" width="200"><br>**13** 北欧纸雕 | <img src="examples/14-nordic-storybook.png" width="200"><br>**14** 北欧绘本水粉 | <img src="examples/15-softnose-vinyl.png" width="200"><br>**15** 大鼻软偶 |
| <img src="examples/16-gouache-spotlight.png" width="200"><br>**16** 聚光水粉立绘 | <img src="examples/17-inked-storybook.png" width="200"><br>**17** 墨线绘本 | <img src="examples/18-warm-flat-storybook.png" width="200"><br>**18** 暖色扁平绘本 | <img src="assets/style-19/anchor-roundhead-redline.png" width="200"><br>**19** 圆头红线极简童画 |
| <img src="assets/style-20/anchor-warm-yellow-ink-story.png" width="200"><br>**20** 暖黄墨线情绪小剧场 | | | |

> 每种画风的输入示例与完整提示词见 [examples/](examples/)。

## 接入各 Agent 工具

核心是工具无关的 [`PROTOCOL.md`](PROTOCOL.md)(执行流程)+ [`STYLES.md`](STYLES.md)(画风配方)。风格 3.1、19 和 20 分别依赖三张正式锚点；风格 13 还使用两张北欧纸雕参考图。轻量包保留这些依赖，正式生产必须安装整个包，不要只复制文本片段。

需要从源码安装时，使用浅克隆和部分克隆，只下载运行目录。服务器需要支持 Git 的部分克隆；不支持时，使用 [Release 轻量包](https://github.com/threerocks/hand-drawn-styles/releases/latest/download/hand-drawn-skill.zip)。

```bash
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/threerocks/hand-drawn-styles.git
git -C hand-drawn-styles sparse-checkout set --no-cone \
  '/SKILL.md' '/AGENTS.md' '/PROTOCOL.md' '/STYLES.md' '/LICENSE' '/INSTALL.md' \
  '/scripts/' '/assets/' \
  '/examples/13-paper-folk.png' '/examples/13-paper-folk-musician.png'
python3 -B hand-drawn-styles/scripts/check_skill.py
```

| 工具 | 接入方式 |
|------|----------|
| **Claude Code** | 把解压后的 `hand-drawn/` 放入 `~/.claude/skills/`，由 `SKILL.md` 提供入口。 |
| **Codex** | 把解压后的 `hand-drawn/` 放入 `~/.codex/skills/`。 |
| **Cursor / Gemini CLI / Jules** | 保留完整安装目录，让项目规则指向其中的 `AGENTS.md` 与 `PROTOCOL.md`。 |
| **Cline / Windsurf / Continue** | 让 rules / custom instructions 指向完整安装目录中的协议和配方。 |
| **直接对话** | 普通纯文本配方可以复制；需要锚点的正式调用仍须保留参考图与完整调用包。 |

接入后,说"用手绘风画……"或"用吉卜力风画……"就能触发。

### 维护者构建与验收

Python 3.10 或更高版本即可运行，不需要 Python 第三方依赖：

```bash
python3 -B -m unittest discover -s scripts -p 'test_*.py'
python3 -B scripts/check_skill.py
python3 -B scripts/build_skill_package.py
```

打包脚本从配方中的资源引用收集必要图片，在仓库外解压 ZIP，再调用全部画风。只有依赖检查和独立安装验证通过，输出才标为 `verified`。包内的 `PACKAGE-MANIFEST.json` 记录文件大小和 SHA-256；图片按原字节保留。安装包大小上限为 15 MiB，超出时构建失败，维护者需要核对新增依赖。

默认产物是 `dist/hand-drawn-skill.zip`。`--skip-verify` 只生成 `candidate-only` 候选包。持续集成执行相同检查并保存 ZIP 工件；公开发布附件需要维护者另行发布。

## 用法要点

### 不指定画风 → 列菜单让你选

```
你：用手绘风画一只在下雨天打伞的猫
Agent：请选择画风(回复编号或名字)：
       1. 极简黑白线条讲解漫画 …
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
- 你**没传**:纯风格(2、3、3.1、5…20)不注入任何比例;版式风格(1、4)只注入"多格网格"或"竖版多格堆叠"这类软结构提示,不写死数字。

### 占位符自动推断

配方里的 `【主体】【标题词】【主色调】【N】【分镜列表】` 由 Agent 从你的描述里自动推断填好,无需手填。

脚本接受编号、中文完整名称或已登记别名。`python3 -B scripts/render_prompt.py --list` 返回所有配方的参数与参考图。`--var '胡茬='` 可以把可选内容删空；用户文案中的 `【短句】` 会按原文保留。

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

风格 19 默认输出正式 JSON 调用包。调用包固定原创三主体锚点、`gpt-image-2-2026-04-21` 模型快照、高保真参考图要求和 7 项验收维度。基础生成只产生 `candidate-only`;总分至少 30/35 且没有硬失败项后才能标为 final。调用端不支持锚点、高保真参考图或快照锁定时，正式生产失败关闭；换模型只允许作为明确标注的非生产预览。本轮样图由 Codex 内置图像生成完成,C2PA 只记录 `gpt-image 2.0`,没有暴露精确快照;因此已验证的是锚点与配方,精确快照要求来自当前官方模型目录,仍需在实际 API 生产通道做一次确认回归。

```bash
python3 scripts/render_prompt.py \
  --style roundhead-redline \
  --subject 'a small elephant calf lifting one coral-red paper lantern with its trunk' \
  --aspect 3:4 \
  --format json
```

风格 20 默认输出正式 JSON 调用包。调用端使用原创锚点直接生成 `final-candidate`，随后运行 `scripts/validate_style_20_asset.py`。验证器自动检查色板和留白，并核对与候选字节绑定的 8 项人工评分卡；评分卡还必须确认主体数量和物种与预期相同、身份未替换、必要物件未丢失。只有总分至少 34/40、没有硬失败项且验证器退出码为 0 时才能标为 final。候选不合格时整张拒收并重新基础生成，禁止用通用风格编辑修补。调用端不支持锚点、高保真参考图、快照锁定或验收器时，正式生产失败关闭。

```bash
python3 scripts/render_prompt.py \
  --style warm-yellow-ink-story \
  --subject 'a grandmother and child repairing one mustard-yellow kite together' \
  --aspect 3:4 \
  --format json
```

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
├── STYLES.md          # 核心配方:20 种整数编号画风 + 3.1 变体(工具无关)
├── SKILL.md           # Claude Code 适配层(薄,指向上面两个文件)
├── AGENTS.md          # Codex / Gemini / Cursor 等适配层(薄)
├── INSTALL.md         # 轻量包的安装与检查说明
├── assets/            # 需要参考锚点的稳定画风资产
├── scripts/           # 渲染器、安装检查、打包与回归测试
├── examples/          # 展示样图，轻量包只收录实际依赖的参考图
└── benchmarks/        # 研发对照图与验收记录，不进入默认安装包
```

## 贡献新画风

欢迎 PR 提交你验证过的画风。一种画风 = 在 `STYLES.md` 增加一段配方 + 在 `PROTOCOL.md` 的菜单、别名表里登记。建议:

- 配方用你实测满意的语言原文(中英不限),不要替换成未验证的措辞;
- 参数名只使用中英文字符、数字或下划线，以字母、汉字或下划线开头；`【最重要·硬性负向约束】` 这类含标点的固定标签按原文保留，不作为参数;
- 在 `scripts/check_skill.py` 增加该画风的完整调用场景，再运行检查和打包；依赖图片以根目录相对路径写入配方说明中的反引号;
- 移除比例硬约束(`1:1` / `3:4` 等),交由比例规则处理;
- 把内容相关的部分抽象成 `【占位符】`;
- 在 `examples/` 附 1–2 张该配方的出图样例,便于评审。
- 新增或升级画风时至少验证“参考图同构场景 + 一个跨主体场景”;维护者可按 `AGENTS.md` 的验证例外调用图像模型,但最终入库样图必须先完成隐私元数据清理与审计。

## License

[MIT](LICENSE) © liulei
