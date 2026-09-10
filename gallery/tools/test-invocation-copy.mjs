import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const galleryRoot = path.resolve(here, "..");
const invocationPath = path.join(galleryRoot, "invocations.js");

assert.ok(
  existsSync(invocationPath),
  "复制调用信息必须由可测试的调用模板生成；当前页面仍只复制名称或描述。",
);

const sandbox = { window: {} };
vm.runInNewContext(readFileSync(invocationPath, "utf8"), sandbox, { filename: invocationPath });
vm.runInNewContext(
  readFileSync(path.join(galleryRoot, "data", "catalog-data.js"), "utf8"),
  sandbox,
  { filename: "catalog-data.js" },
);

const invocations = sandbox.window.AtlasInvocations;
const catalog = sandbox.window.GENERATION_CATALOG;
assert.ok(invocations, "invocations.js 必须导出 window.AtlasInvocations");

const formulaLab = catalog.generators.find((item) => item.id === "phil-aesthetic-formulas");
assert.ok(formulaLab, "画栏必须包含 Phil 审美公式");
assert.equal(formulaLab.source, "D:\\GitHub Program\\Phil-aesthetic-formulas");
assert.ok(existsSync(path.join(galleryRoot, formulaLab.poster)), "Phil 审美公式必须使用本地真实样片");

for (const item of catalog.generators) {
  assert.ok(existsSync(item.source), `${item.id} 引用了不存在的本地来源：${item.source}`);
  const copied = invocations.generator(item);
  assert.match(copied, /^请使用以下本地生成能力完成任务：/u, `${item.id} 缺少明确调用动作`);
  assert.ok(copied.includes(`能力：${item.name}`), `${item.id} 缺少能力名称`);
  assert.ok(copied.includes(`来源：${item.source}`), `${item.id} 缺少能力来源`);
  assert.ok(copied.includes("任务：【请填写具体需求】"), `${item.id} 缺少任务输入位`);
  assert.ok(copied.includes("不要只复述说明"), `${item.id} 缺少执行约束`);
}

for (const item of catalog.styles) {
  const copied = invocations.style(item);
  assert.match(copied, /^请使用 hand-drawn-styles/u, `${item.id} 缺少画风调用动作`);
  assert.ok(copied.includes(`画风：${item.name}`), `${item.id} 缺少画风名称`);
  assert.ok(copied.includes("绘制内容：【请填写要画的内容】"), `${item.id} 缺少绘制内容输入位`);
  assert.ok(copied.includes("PROTOCOL.md"), `${item.id} 缺少协议入口`);
  assert.ok(copied.includes("STYLES.md"), `${item.id} 缺少配方入口`);
}

for (const item of catalog.effects) {
  assert.ok(existsSync(item.source), `${item.id} 引用了不存在的 Registry 来源：${item.source}`);
  const copied = invocations.effect(item);
  assert.match(copied, /^请在 HyperFrames 中使用以下 Registry 特效：/u, `${item.id} 缺少特效调用动作`);
  assert.ok(copied.includes(`特效：${item.name}`), `${item.id} 缺少 Registry 名称`);
  assert.ok(copied.includes(`来源：${item.source}`), `${item.id} 缺少 Registry 来源`);
  assert.ok(copied.includes("目标：【请填写要实现的画面或交互】"), `${item.id} 缺少目标输入位`);
  assert.ok(copied.includes("不要只描述效果"), `${item.id} 缺少执行约束`);
}

const indexHtml = readFileSync(path.join(galleryRoot, "index.html"), "utf8");
const galleryJs = readFileSync(path.join(galleryRoot, "gallery.js"), "utf8");
assert.ok(indexHtml.indexOf("invocations.js") < indexHtml.indexOf("gallery.js"), "调用模板必须先于 gallery.js 加载");
assert.match(galleryJs, /invocations\.generator\(item\)/u);
assert.match(galleryJs, /invocations\.style\(item\)/u);
assert.match(galleryJs, /invocations\.effect\(item\)/u);
assert.match(galleryJs, /window\.clearTimeout\(copyFeedbackTimeout\)/u, "切换条目时必须取消旧的复制反馈计时器");
assert.match(galleryJs, /function configureDialog[\s\S]*?resetCopyFeedback\(\)/u, "打开条目时必须重置复制按钮文案");
assert.match(galleryJs, /detailCopy\.dataset\.copy !== copyValue/u, "异步复制完成后必须确认仍是同一条目");

console.log(`PASS: ${catalog.generators.length + catalog.styles.length + catalog.effects.length} 条调用信息均为可填写、可执行模板。`);
