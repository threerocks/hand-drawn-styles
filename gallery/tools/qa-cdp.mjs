import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const endpoint = `${process.env.CHROME_ENDPOINT ?? "http://127.0.0.1:9333"}/json/list`;
const galleryUrl = process.env.GALLERY_URL ?? "/hand-drawn-styles/gallery/";
const here = path.dirname(fileURLToPath(import.meta.url));
const evidenceDir = path.resolve(here, "..", "qa-evidence");
const plateA = "./assets/effect-plates/effect-gouache-portrait.png";
const plateB = "./assets/effect-plates/effect-ink-family.png";
await mkdir(evidenceDir, { recursive: true });

const pages = await (await fetch(endpoint)).json();
const target = pages.find((page) => page.type === "page" && page.url.includes(galleryUrl));
if (!target) throw new Error("No Chrome page target found");

const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  socket.addEventListener("open", resolve, { once: true });
  socket.addEventListener("error", reject, { once: true });
});

let messageId = 0;
const pending = new Map();
const consoleErrors = [];
socket.addEventListener("message", (event) => {
  const message = JSON.parse(event.data);
  if (message.id && pending.has(message.id)) {
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(message.error.message));
    else resolve(message.result);
  }
  if (message.method === "Runtime.exceptionThrown") {
    consoleErrors.push(message.params.exceptionDetails.text);
  }
  if (message.method === "Runtime.consoleAPICalled" && message.params.type === "error") {
    consoleErrors.push(message.params.args.map((arg) => arg.value ?? arg.description).join(" "));
  }
});

const send = (method, params = {}) => new Promise((resolve, reject) => {
  const id = ++messageId;
  pending.set(id, { resolve, reject });
  socket.send(JSON.stringify({ id, method, params }));
});
const wait = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));
const evaluate = async (expression) => {
  const result = await send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
  return result.result.value;
};
const screenshot = async (name) => {
  const result = await send("Page.captureScreenshot", {
    format: "png",
    captureBeyondViewport: false,
    fromSurface: true,
  });
  const output = path.join(evidenceDir, name);
  await writeFile(output, Buffer.from(result.data, "base64"));
  return output;
};
const viewport = async (width, height) => {
  await send("Emulation.setDeviceMetricsOverride", {
    width,
    height,
    deviceScaleFactor: 1,
    mobile: width <= 480,
  });
  await wait(350);
};

await send("Page.enable");
await send("Runtime.enable");
await send("Network.enable");
await send("Page.reload", { ignoreCache: true });
await wait(1600);

const assertions = [];
const assert = (name, value, expected) => {
  const passed = typeof expected === "function" ? expected(value) : value === expected;
  assertions.push({ name, passed, value });
  if (!passed) throw new Error(`${name} failed: ${JSON.stringify(value)}`);
};
const openEffectSample = async (query, expectedMode, expectedTransition, screenshotName) => {
  await evaluate(`document.querySelector('#effect-search').value=${JSON.stringify(query)};
    document.querySelector('#effect-search').dispatchEvent(new Event('input',{bubbles:true}));
    document.querySelector('#effect-grid [data-effect]').click()`);
  await wait(1800);
  await evaluate("(() => { document.querySelector('.effect-stage iframe')?.contentWindow?.seekEffect?.(1.2); return true; })()");
  await wait(120);
  const sample = await evaluate(`({
    open: document.querySelector('#detail-dialog').open,
    description: document.querySelector('#detail-description').textContent,
    frameReady: document.querySelector('.effect-stage iframe')?.contentDocument?.readyState,
    labReady: document.querySelector('.effect-stage iframe')?.contentWindow?.__effectLabReady,
    mode: document.querySelector('.effect-stage iframe')?.contentDocument?.querySelector('.test-effect')?.dataset.mode,
    transition: document.querySelector('.effect-stage iframe')?.contentDocument?.querySelector('.test-effect')?.dataset.transition,
    plateA: document.querySelector('.effect-stage iframe')?.contentDocument?.querySelector('.test-effect__plate--a')?.getAttribute('src'),
    plateB: document.querySelector('.effect-stage iframe')?.contentDocument?.querySelector('.test-effect__plate--b')?.getAttribute('src'),
    plateBClip: getComputedStyle(document.querySelector('.effect-stage iframe')?.contentDocument?.querySelector('.test-effect__plate--b')).clipPath,
    timelineTime: document.querySelector('.effect-stage iframe')?.contentWindow?.__timelines?.['fixed-effect-lab']?.time(),
    timelineDuration: document.querySelector('.effect-stage iframe')?.contentWindow?.__timelines?.['fixed-effect-lab']?.duration(),
    visibleRatio: (() => {
      const frame = document.querySelector('.effect-stage iframe')?.contentDocument;
      const stage = frame?.querySelector('.test-effect')?.getBoundingClientRect();
      if (!stage) return 0;
      const visible = [...frame.querySelectorAll('.test-effect__plate')].reduce((total, plate) => {
        const rect = plate.getBoundingClientRect();
        const width = Math.max(0, Math.min(stage.right, rect.right) - Math.max(stage.left, rect.left));
        const height = Math.max(0, Math.min(stage.bottom, rect.bottom) - Math.max(stage.top, rect.top));
        return total + ((width * height) / (stage.width * stage.height));
      }, 0);
      return visible;
    })()
  })`);
  assert(`${expectedMode} dialog open`, sample.open, true);
  assert(`${expectedMode} motion description`, sample.description, (value) => value.includes("画面怎么动："));
  assert(`${expectedMode} recognition cue`, sample.description, (value) => value.includes("判断是否生效："));
  assert(`${expectedMode} no generic fixed-input copy`, sample.description, (value) => !value.includes("固定输入测试"));
  if (expectedMode === "camera") {
    assert("camera description names the push-in", sample.description, (value) => value.includes("缓慢推近"));
  }
  assert(`${expectedMode} iframe ready`, sample.frameReady, "complete");
  assert(`${expectedMode} lab ready`, sample.labReady, true);
  assert(`${expectedMode} mode`, sample.mode, expectedMode);
  assert(`${expectedMode} transition`, sample.transition, String(expectedTransition));
  assert(`${expectedMode} fixed A`, sample.plateA, plateA);
  assert(`${expectedMode} fixed B or A`, sample.plateB, (value) => value === plateA || value === plateB);
  assert(`${expectedMode} timeline`, sample.timelineDuration, (value) => value >= 3);
  assert(`${expectedMode} representative time`, sample.timelineTime, 1.2);
  if (expectedMode === "wipe") {
    assert("wipe representative frame", sample.plateBClip, (value) => value !== "inset(0px)");
  }
  assert(`${expectedMode} visible plate area`, sample.visibleRatio, (value) => value >= 0.75);
  const output = await screenshot(screenshotName);
  await evaluate("document.querySelector('#detail-close').click()");
  await evaluate("document.querySelector('[data-clear=\"effects\"]').click()");
  return output;
};

await viewport(1280, 900);
await evaluate("window.scrollTo(0, 0)");
const overview = await evaluate(`({
  visible: [...document.querySelectorAll('[data-section]')].filter((el) => !el.hidden).map((el) => el.dataset.section),
  stats: [...document.querySelectorAll('.hero__stats dt')].map((el) => el.textContent),
  overflow: document.documentElement.scrollWidth - innerWidth
})`);
assert("overview sections", overview.visible, (value) => value.every((item) => item === "overview"));
assert("overview totals", overview.stats.join(","), "202,40,142,20");
assert("desktop overflow", overview.overflow, (value) => value <= 1);
const desktopOverview = await screenshot("desktop-overview.png");

await evaluate("document.querySelector('[data-view=\"generators\"]').click()");
await wait(300);
assert("generator count", await evaluate("document.querySelectorAll('#generator-grid .catalog-card').length"), 40);
await evaluate("window.scrollTo(0, 0)");
const desktopGenerators = await screenshot("desktop-generators.png");
await evaluate(`document.querySelector('#generator-search').value='语音';
  document.querySelector('#generator-search').dispatchEvent(new Event('input',{bubbles:true}))`);
assert("generator search", await evaluate("document.querySelectorAll('#generator-grid .catalog-card').length"), (value) => value >= 3);
await evaluate(`document.querySelector('#generator-search').value='';
  document.querySelector('#generator-search').dispatchEvent(new Event('input',{bubbles:true}))`);
await evaluate(`document.querySelector('#generator-search').value='__no_generator__';
  document.querySelector('#generator-search').dispatchEvent(new Event('input',{bubbles:true}))`);
assert("generator empty state", await evaluate("!document.querySelector('#generator-empty').hidden"), true);
await evaluate("document.querySelector('[data-clear=\"generators\"]').click()");
assert("generator clear restores", await evaluate("document.querySelectorAll('#generator-grid .catalog-card').length"), 40);

await evaluate("document.querySelector('[data-view=\"styles\"]').click()");
await wait(250);
assert("style count", await evaluate("document.querySelectorAll('#style-grid .catalog-card').length"), 20);
await evaluate("window.scrollTo(0, 0)");
const desktopStyles = await screenshot("desktop-styles.png");
await evaluate(`document.querySelector('#style-search').value='潮玩';
  document.querySelector('#style-search').dispatchEvent(new Event('input',{bubbles:true}))`);
assert("style search", await evaluate("document.querySelectorAll('#style-grid .catalog-card').length"), 1);
await evaluate(`document.querySelector('#style-search').value='__no_style__';
  document.querySelector('#style-search').dispatchEvent(new Event('input',{bubbles:true}))`);
assert("style empty state", await evaluate("!document.querySelector('#style-empty').hidden"), true);
await evaluate("document.querySelector('[data-clear=\"styles\"]').click()");
assert("style clear restores", await evaluate("document.querySelectorAll('#style-grid .catalog-card').length"), 20);

await evaluate("document.querySelector('[data-view=\"effects\"]').click()");
await wait(450);
assert("effect count", await evaluate("document.querySelectorAll('#effect-grid .effect-card').length"), 142);
await evaluate("window.scrollTo(0, 0)");
const desktopEffects = await screenshot("desktop-effects.png");
await evaluate(`document.querySelector('#effect-search').value='caption';
  document.querySelector('#effect-search').dispatchEvent(new Event('input',{bubbles:true}))`);
await wait(180);
const desktopCaptionPreviews = await screenshot("desktop-caption-previews.png");
assert(
  "caption cards use only the neutral text specimen",
  await evaluate("[...document.querySelectorAll('#effect-grid .test-effect__caption')].every((caption) => caption.querySelector('strong')?.textContent === 'Aa' && !caption.querySelector('small'))"),
  true,
);
await evaluate(`document.querySelector('#effect-search').value='transitions';
  document.querySelector('#effect-search').dispatchEvent(new Event('input',{bubbles:true}))`);
await wait(180);
const desktopTransitionPreviews = await screenshot("desktop-transition-previews.png");
await evaluate(`document.querySelector('#effect-search').value='';
  document.querySelector('#effect-search').dispatchEvent(new Event('input',{bubbles:true}))`);
await evaluate("document.querySelector('[data-effect-family=\"component\"]').click()");
assert("effect component filter", await evaluate("document.querySelectorAll('#effect-grid .effect-card').length"), 25);
await evaluate("document.querySelector('[data-effect-family=\"全部\"]').click()");
const fixedInputs = await evaluate(`(() => {
  const cards = [...document.querySelectorAll('#effect-grid .effect-card')];
  const sources = [...document.querySelectorAll('#effect-grid .test-effect__plate')].map((image) => image.getAttribute('src'));
  const visualFingerprint = (preview) => [
    getComputedStyle(preview.querySelector('.test-effect__plate--a')).objectPosition,
    getComputedStyle(preview.querySelector('.test-effect__plate--a')).filter,
    getComputedStyle(preview.querySelector('.test-effect__plate--a')).transform,
    getComputedStyle(preview.querySelector('.test-effect__plate--b')).clipPath,
    getComputedStyle(preview.querySelector('.test-effect__plate--b')).transform,
    getComputedStyle(preview.querySelector('.test-effect__grain')).backgroundSize,
    getComputedStyle(preview.querySelector('.test-effect__grid')).backgroundImage,
    getComputedStyle(preview.querySelector('.test-effect__caption')).transform,
    getComputedStyle(preview.querySelector('.test-effect__caption')).backgroundColor,
  ].join('|');
  const previews = cards.map((card) => card.querySelector('.test-effect'));
  return {
    sourceSet: [...new Set(sources)],
    allA: cards.every((card) => card.querySelector('.test-effect__plate--a')?.getAttribute('src') === ${JSON.stringify(plateA)}),
    validB: cards.every((card) => {
      const preview = card.querySelector('.test-effect');
      const expected = preview.dataset.transition === 'true'
        ? ${JSON.stringify(plateB)}
        : ${JSON.stringify(plateA)};
      return card.querySelector('.test-effect__plate--b')?.getAttribute('src') === expected;
    }),
    namedPreviews: cards.every((card) => Boolean(card.querySelector('.test-effect')?.dataset.effect)),
    signatureCount: new Set(cards.map((card) => card.querySelector('.test-effect')?.dataset.signature)).size,
    captionVariantCount: new Set(
      previews
        .filter((preview) => preview?.dataset.mode === 'caption')
        .map((preview) => preview.dataset.signature)
    ).size,
    visualFingerprintCount: new Set(previews.map(visualFingerprint)).size,
    captionVisualFingerprintCount: new Set(
      previews
        .filter((preview) => preview?.dataset.mode === 'caption')
        .map(visualFingerprint)
    ).size,
    motionCards: cards.every((card) => Boolean(card.querySelector('.test-effect')?.dataset.motionState))
  };
})()`);
assert("effect source set", fixedInputs.sourceSet.join(","), [plateA, plateB].join(","));
assert("all cards use fixed A", fixedInputs.allA, true);
assert("cards use only allowed B or A", fixedInputs.validB, true);
assert("all cards expose their concrete effect", fixedInputs.namedPreviews, true);
assert("all cards have distinct representative signatures", fixedInputs.signatureCount, 142);
assert("caption cards do not collapse to one representative", fixedInputs.captionVariantCount, (value) => value >= 12);
assert("most cards have visibly distinct representative styles", fixedInputs.visualFingerprintCount, (value) => value >= 100);
assert("caption cards have visibly distinct representative styles", fixedInputs.captionVisualFingerprintCount, (value) => value >= 12);
assert("card previews are registered for functional motion", fixedInputs.motionCards, true);
await send("Network.setBlockedURLs", { urls: ["https://*"] });
const desktopBlur = await openEffectSample("motion blur", "blur", false, "desktop-effect-blur.png");
const desktopWarp = await openEffectSample("swirl vortex", "warp", true, "desktop-effect-warp.png");
const desktopGrain = await openEffectSample("warm grain", "grain", false, "desktop-effect-grain.png");
const desktopWipe = await openEffectSample("play mode", "wipe", true, "desktop-effect-wipe.png");
const desktopPush = await openEffectSample("transitions push", "push", true, "desktop-effect-push.png");
const desktopCamera = await openEffectSample("product promo", "camera", false, "desktop-effect-camera.png");
await send("Network.setBlockedURLs", { urls: [] });
await evaluate(`document.querySelector('#effect-search').value='__no_effect__';
  document.querySelector('#effect-search').dispatchEvent(new Event('input',{bubbles:true}))`);
assert("effect empty state", await evaluate("!document.querySelector('#effect-empty').hidden"), true);
await evaluate("document.querySelector('[data-clear=\"effects\"]').click()");
assert("effect clear restores", await evaluate("document.querySelectorAll('#effect-grid .effect-card').length"), 142);

await send("Emulation.setEmulatedMedia", {
  features: [{ name: "prefers-reduced-motion", value: "reduce" }],
});
assert("reduced motion", await evaluate("[...document.querySelectorAll('.test-effect--card')].every((preview) => preview.dataset.motionState === 'settled')"), true);
await send("Emulation.setEmulatedMedia", { features: [] });

await viewport(768, 900);
await evaluate("document.querySelector('[data-view=\"effects\"]').click(); window.scrollTo(0,0)");
await wait(300);
assert("tablet overflow", await evaluate("document.documentElement.scrollWidth - innerWidth"), (value) => value <= 1);
const tabletEffects = await screenshot("tablet-effects.png");
const tabletPixel = await openEffectSample("grid pixelate wipe", "pixel", true, "tablet-effect-pixel.png");

await viewport(375, 812);
await evaluate("document.querySelector('[data-view=\"effects\"]').click(); window.scrollTo(0,0)");
await wait(350);
const mobile = await evaluate(`({
  overflow: document.documentElement.scrollWidth - innerWidth,
  cards: document.querySelectorAll('#effect-grid .effect-card').length,
  sourceSet: [...new Set([...document.querySelectorAll('#effect-grid .test-effect__plate')].map((image) => image.getAttribute('src')))]
})`);
assert("mobile overflow", mobile.overflow, (value) => value <= 1);
assert("mobile effect count", mobile.cards, 142);
assert("mobile fixed source set", mobile.sourceSet.join(","), [plateA, plateB].join(","));
const mobileEffects = await screenshot("mobile-effects.png");
const mobileCaption = await openEffectSample("caption pill karaoke", "caption", false, "mobile-effect-caption.png");

await writeFile(path.join(evidenceDir, "qa-report.json"), JSON.stringify({
  assertions,
  consoleErrors,
  screenshots: {
    desktopOverview,
    desktopGenerators,
    desktopStyles,
    desktopEffects,
    desktopCaptionPreviews,
    desktopTransitionPreviews,
    desktopBlur,
    desktopWarp,
    desktopGrain,
    desktopWipe,
    desktopPush,
    desktopCamera,
    tabletEffects,
    tabletPixel,
    mobileEffects,
    mobileCaption,
  },
}, null, 2));
socket.close();

if (consoleErrors.length > 0) {
  throw new Error(`Console errors: ${consoleErrors.join(" | ")}`);
}
console.log(JSON.stringify({ assertions: assertions.length, screenshots: 16, consoleErrors }, null, 2));
