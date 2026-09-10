import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const galleryRoot = path.resolve(here, "..");
const programRoot = path.resolve(galleryRoot, "..", "..");
const registryRoot = path.join(programRoot, "hyperframes", "registry");

const readJson = async (filename) => JSON.parse(await readFile(filename, "utf8"));
const styles = await readJson(path.join(galleryRoot, "data", "styles-source.json"));
const generators = await readJson(path.join(galleryRoot, "data", "generators-source.json"));
const registry = await readJson(path.join(registryRoot, "registry.json"));

const labelFor = (name) => name
  .split("-")
  .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
  .join(" ");

const previewKindFor = (name) => {
  const rules = [
    ["code", /code|terminal/],
    ["caption", /caption|lower-third|^lt-|ticker|post|notification/],
    ["liquid", /liquid|glass|ripple|wave/],
    ["burn", /burn|thermal|ember/],
    ["glitch", /glitch|chromatic|matrix|pixel/],
    ["dissolve", /dissolve|shatter|destruction|particle|assemble/],
    ["lens", /lens|iris|vortex|warp|portal|magnetic/],
    ["light", /light|flash|shimmer|glow|vignette|grain|texture/],
    ["camera", /zoom|blur|pan|parallax|3d|push|scale/],
    ["data", /map|chart|flow|decision|money|flight/],
  ];
  return rules.find(([, pattern]) => pattern.test(name))?.[0] ?? "reveal";
};

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

const effects = registry.items.map((item, index) => {
  const folder = folders[item.type];
  const demo = item.type.endsWith("component")
    ? (componentDemos.has(item.name) ? "demo.html" : `${item.name}.html`)
    : item.type.endsWith("example") ? "index.html" : `${item.name}.html`;
  return {
    id: `fx-${String(index + 1).padStart(3, "0")}`,
    name: item.name,
    label: labelFor(item.name),
    family: item.type.split(":")[1],
    previewKind: previewKindFor(item.name),
    preview: `./assets/effect-previews/${item.type.split(":")[1]}-${item.name}`,
    demo: `./assets/hyperframes-registry/${folder}/${item.name}/${demo}`,
    source: `D:\\GitHub Program\\hyperframes\\registry\\${folder}\\${item.name}`,
  };
});

const families = [...new Set(generators.map((item) => item.family))];
const data = { styles, effects, generators, families };
const output = `window.GENERATION_CATALOG = Object.freeze(${JSON.stringify(data, null, 2)});\n`;
await writeFile(path.join(galleryRoot, "data", "catalog-data.js"), output, "utf8");

console.log(JSON.stringify({
  styles: styles.length,
  effects: effects.length,
  generators: generators.length,
  families: families.length,
}, null, 2));
