import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const endpoint = process.env.CHROME_ENDPOINT ?? "http://127.0.0.1:9444";
const site = process.env.GALLERY_URL ?? "http://127.0.0.1:8876";
const here = path.dirname(fileURLToPath(import.meta.url));
const galleryRoot = path.resolve(here, "..");
const outputRoot = path.join(galleryRoot, "assets", "effect-previews");
const registry = JSON.parse(await readFile(
  path.join(galleryRoot, "assets", "hyperframes-registry", "registry.json"),
  "utf8",
));
await mkdir(outputRoot, { recursive: true });

const folders = {
  "hyperframes:block": "blocks",
  "hyperframes:component": "components",
  "hyperframes:example": "examples",
};
const componentDemos = new Set([
  "grain-overlay",
  "shimmer-sweep",
  "grid-pixelate-wipe",
  "motion-blur",
  "texture-mask-text",
  "vignette",
]);
const demoFor = (item) => {
  if (item.type.endsWith("component")) {
    return componentDemos.has(item.name) ? "demo.html" : `${item.name}.html`;
  }
  return item.type.endsWith("example") ? "index.html" : `${item.name}.html`;
};

const created = await fetch(`${endpoint}/json/new?about:blank`, { method: "PUT" });
if (!created.ok) throw new Error(`Cannot create Chrome target: ${created.status}`);
const target = await created.json();
const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  socket.addEventListener("open", resolve, { once: true });
  socket.addEventListener("error", reject, { once: true });
});

let messageId = 0;
const pending = new Map();
socket.addEventListener("message", (event) => {
  const message = JSON.parse(event.data);
  if (!message.id || !pending.has(message.id)) return;
  const { resolve, reject } = pending.get(message.id);
  pending.delete(message.id);
  if (message.error) reject(new Error(message.error.message));
  else resolve(message.result);
});
const send = (method, params = {}) => new Promise((resolve, reject) => {
  const id = ++messageId;
  pending.set(id, { resolve, reject });
  socket.send(JSON.stringify({ id, method, params }));
});
const wait = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));
const capture = async (filename) => {
  const result = await send("Page.captureScreenshot", {
    format: "jpeg",
    quality: 76,
    captureBeyondViewport: false,
    fromSurface: true,
  });
  await writeFile(path.join(outputRoot, filename), Buffer.from(result.data, "base64"));
};
const evaluate = async (expression) => {
  const result = await send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  return result.result.value;
};
const waitUntilReady = async () => {
  for (let attempt = 0; attempt < 30; attempt += 1) {
    if (await evaluate("window.__effectRunnerReady === true")) return;
    await wait(100);
  }
};

await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", {
  width: 640,
  height: 400,
  deviceScaleFactor: 1,
  mobile: false,
});

for (const [index, item] of registry.items.entries()) {
  const family = item.type.split(":")[1];
  const folder = folders[item.type];
  const relative = `assets/hyperframes-registry/${folder}/${item.name}/${demoFor(item)}`;
  const source = encodeURIComponent(`./${relative}`);
  await send("Page.navigate", { url: `${site}/effect-runner.html?src=${source}` });
  await waitUntilReady();
  await evaluate("window.seekEffect?.(0.8)");
  await capture(`${family}-${item.name}-a.jpg`);
  await evaluate("window.seekEffect?.(2.4)");
  await capture(`${family}-${item.name}-b.jpg`);
  if ((index + 1) % 20 === 0) process.stdout.write(`${index + 1}/${registry.items.length}\n`);
}

socket.close();
await fetch(`${endpoint}/json/close/${target.id}`);
process.stdout.write(`${registry.items.length}/${registry.items.length}\n`);
