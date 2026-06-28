# AGENTS.md

供读取 `AGENTS.md` 的 Agent 工具使用(OpenAI Codex CLI、Gemini CLI、Cursor、Jules 等)。

## 手绘风格生图提示词能力

当用户希望生成"手绘 / 插画风格"的图像、或要一段对应的生图提示词时:

1. 按 [PROTOCOL.md](PROTOCOL.md) 的 5 步流程执行(确定画风 → 取配方 → 自动填占位符 → 处理比例 → 输出 prompt)。
2. 画风模板从 [STYLES.md](STYLES.md) 取。
3. 只输出最终 prompt 纯文本,**不要生图**。

> 想用在你自己的项目里:把 `PROTOCOL.md` 与 `STYLES.md` 拷进你项目,或把这三句指令并入你项目的 `AGENTS.md` / 规则文件即可。
