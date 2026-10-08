# AGENTS.md

供读取 `AGENTS.md` 的 Agent 工具使用(OpenAI Codex CLI、Gemini CLI、Cursor、Jules 等)。

## 手绘风格生图提示词能力

当用户希望生成"手绘 / 插画风格"的图像、或要一段对应的生图提示词时:

1. 按 [PROTOCOL.md](PROTOCOL.md) 的 5 步流程执行(确定画风 → 取配方 → 自动填占位符 → 处理比例 → 输出 prompt)。
2. 画风模板从 [STYLES.md](STYLES.md) 取。
3. 能执行脚本时优先用 `scripts/render_prompt.py`,禁止手工缩写、同义改写或混入业务项目自定义画风规则。
4. 风格 3.1 的正式生产、多页或连续故事必须完整消费渲染器 JSON 中的三阶段 `workflow`:基础生成后依次执行 `scribble-correction` 与 `scribble-chaos-correction`;前两阶段不可作为 final,任一阶段缺失时停止生产。
5. 风格 19 正式生产必须完整消费 `roundhead-redline-v1` JSON 调用包:每张携带原创锚点,锁定模型快照和高保真参考图输入,基础图只标为 `candidate-only`,通过 `acceptance_contract` 后才能标为 final;任一条件不可用时停止生产。
6. 风格 20 正式生产必须完整消费 `warm-yellow-ink-story-v3` JSON 调用包:使用固定原创锚点生成 `final-candidate`,然后运行机读验收器;失败候选整张拒收并重新生成,禁止用通用画风迁移编辑修补。
7. 风格 21 手写独白彩铅自带文案且只定义风格:`--text` 必填(文案原文,渲染器自动分行,空行分段),`--subject` 可省略(默认由模型按文案决定内容与构图),画幅默认 3:4 可用 `--aspect` 覆盖,不需要锚点,默认输出纯文本 prompt。
8. 其他画风默认只输出最终 prompt 纯文本;风格 3.1/19/20 正式生产输出带参考锚点的 JSON 调用包。**不要生图**;唯一例外是用户明确要求在本机用 `scripts/generate_monologue_card_with_codex.sh` 直接出图。

### 维护者验证例外

当用户明确要求新增、升级或验收仓库中的画风时,可在维护流程中调用图像模型做多轮样图验证。此例外只用于研发和验收,不改变本项目面向普通使用者“只输出 prompt”的能力边界。

维护者验证必须:

1. 先固定参考图、测试场景和判定维度,再开始出图。
2. 每轮只针对已观察到的稳定偏差修改配方,保留可复核的候选样图。
3. 至少验证参考图同构场景与一个跨主体场景,不能凭单张满意图入库。
4. 最终入库图片必须使用 `sweety-image-privacy` 清理 EXIF、GPS、来源字段和 macOS 来源扩展属性,并保留审计结果。

> 想用在你自己的项目里:安装整个 skill 并按画风编号调用。不要只复制某几句配方,也不要在业务项目维护第二份画风真源。
