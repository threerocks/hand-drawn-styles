"use strict";

window.AtlasInvocations = Object.freeze({
  generator(item) {
    return [
      "请使用以下本地生成能力完成任务：",
      `能力：${item.name}`,
      `类别：${item.family}`,
      `预期输出：${item.output}`,
      `能力说明：${item.description}`,
      `来源：${item.source}`,
      "",
      "任务：【请填写具体需求】",
      "",
      "执行要求：",
      "1. 先读取来源中的 SKILL.md、README.md 或同等入口说明。",
      "2. 按该能力的原始流程实际执行，不要只复述说明。",
      "3. 若来源不存在或当前环境未安装，明确报告缺失项，不要假装调用成功。",
    ].join("\n");
  },

  style(item) {
    const root = "D:\\GitHub Program\\hand-drawn-styles";
    return [
      "请使用 hand-drawn-styles 生成最终图像提示词：",
      `画风：${item.name}`,
      `画风编号：${item.id}`,
      `英文别名：${item.aliases.join("、")}`,
      "绘制内容：【请填写要画的内容】",
      "可选比例：【不指定可留空】",
      `协议入口：${root}\\PROTOCOL.md`,
      `配方入口：${root}\\STYLES.md`,
      "执行要求：读取协议和配方，填充占位符，只输出可直接交给图像模型的最终 prompt；不要直接生图。",
    ].join("\n");
  },

  effect(item) {
    return [
      "请在 HyperFrames 中使用以下 Registry 特效：",
      `特效：${item.name}`,
      `显示名：${item.label}`,
      `类型：${item.family}`,
      `来源：${item.source}`,
      "目标：【请填写要实现的画面或交互】",
      "素材或文案：【请填写；没有可留空】",
      "执行要求：先读取 registry-item.json 和对应实现文件，将特效接入实际 composition 并预览验证；不要只描述效果。",
    ].join("\n");
  },
});
