import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const galleryUrl = process.env.GALLERY_URL
  ?? "http://127.0.0.1:8876/hand-drawn-styles/gallery/";

const browser = await chromium.launch({ channel: "chrome", headless: false });

try {
  // Given: a fresh browser that allows motion and bypasses service-worker state.
  const context = await browser.newContext({
    reducedMotion: "no-preference",
    serviceWorkers: "block",
    viewport: { width: 1280, height: 800 },
  });
  const page = await context.newPage();
  const pageErrors = [];
  page.on("pageerror", (error) => pageErrors.push(error.message));
  await page.goto(galleryUrl, { waitUntil: "load" });
  await page.locator('[data-view="effects"]').click();

  // When: a representative effect card is visible long enough to enter preview playback.
  const scene = page.locator('.test-effect--card[data-effect="warm-grain"]').first();
  await scene.scrollIntoViewIfNeeded();
  const initialStyle = await scene.evaluate((node) => {
    const grain = node.querySelector(".test-effect__grain");
    const style = getComputedStyle(grain);
    return `${style.transform}|${style.opacity}`;
  });

  try {
    await page.waitForFunction(
      ({ effectName, previousStyle }) => {
        const node = document.querySelector(
          `.test-effect--card[data-effect="${effectName}"] .test-effect__grain`,
        );
        if (!node) return false;
        const style = getComputedStyle(node);
        return `${style.transform}|${style.opacity}` !== previousStyle;
      },
      { effectName: "warm-grain", previousStyle: initialStyle },
      { timeout: 5000 },
    );
  } catch (error) {
    throw new Error(
      `Effect card cover remained static; warm-grain stayed at ${initialStyle}`,
      { cause: error },
    );
  }

  // Then: the cover visibly advances and the page raises no runtime errors.
  assert.deepEqual(pageErrors, []);
  const playbackStates = await page.locator(".test-effect--card").evaluateAll((nodes) => (
    nodes.reduce((counts, node) => {
      counts[node.dataset.motionState] = (counts[node.dataset.motionState] ?? 0) + 1;
      return counts;
    }, {})
  ));
  assert.ok(playbackStates.playing > 0, "At least one visible preview must be playing");
  assert.ok(
    (playbackStates.waiting ?? 0) + (playbackStates.paused ?? 0) > 0,
    "Offscreen previews must remain idle",
  );

  // When: the moving artwork inside a cover receives the user's click.
  await scene.click();

  // Then: event delegation resolves the containing activation button and opens the lab.
  assert.equal(
    await page.locator("#detail-dialog").evaluate((dialog) => dialog.open),
    true,
    "Clicking moving cover artwork must open the effect lab",
  );
  const protectedDialogPhrases = await page.locator("#detail-description").evaluate((node) => {
    const rectCountFor = (phrase) => {
      const start = node.textContent.indexOf(phrase);
      if (start < 0 || !node.firstChild) return 0;
      const range = document.createRange();
      range.setStart(node.firstChild, start);
      range.setEnd(node.firstChild, start + phrase.length);
      return range.getClientRects().length;
    };
    return {
      slight: rectCountFor("轻微"),
      grainGrowth: rectCountFor("不断增强"),
    };
  });
  assert.deepEqual(
    protectedDialogPhrases,
    { slight: 1, grainGrowth: 1 },
    "Meaningful Chinese phrases in the effect description must not split across lines",
  );
  await page.locator("#detail-close").click();
  await context.close();

  // Given: the narrowest supported phone viewport.
  const mobileContext = await browser.newContext({
    reducedMotion: "no-preference",
    serviceWorkers: "block",
    viewport: { width: 375, height: 812 },
  });
  const mobilePage = await mobileContext.newPage();
  await mobilePage.goto(galleryUrl, { waitUntil: "load" });
  await mobilePage.locator('[data-view="effects"]').click();

  // Then: the action phrase stays intact while the surrounding note may wrap naturally.
  const notePhrase = mobilePage.locator(".effects-note__keep");
  assert.equal(await notePhrase.count(), 1, "The protected note phrase must exist once");
  assert.equal(
    await notePhrase.evaluate((node) => node.getClientRects().length),
    1,
    "播放对应特效 must not split across lines",
  );
  assert.equal(
    await mobilePage.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth),
    true,
    "The protected phrase must not introduce page overflow",
  );
  await mobileContext.close();

  // Given: a fresh browser whose user preference requests reduced motion.
  const reducedContext = await browser.newContext({
    reducedMotion: "reduce",
    serviceWorkers: "block",
    viewport: { width: 1280, height: 800 },
  });
  const reducedPage = await reducedContext.newPage();
  const reducedPageErrors = [];
  reducedPage.on("pageerror", (error) => reducedPageErrors.push(error.message));

  // When: the effect gallery is opened.
  await reducedPage.goto(galleryUrl, { waitUntil: "load" });
  await reducedPage.locator('[data-view="effects"]').click();

  // Then: every cover stays settled and no infinite preview timeline is created.
  const reducedState = await reducedPage.evaluate(() => ({
    allSettled: [...document.querySelectorAll(".test-effect--card")]
      .every((node) => node.dataset.motionState === "settled"),
    loopingTimelines: window.gsap.globalTimeline
      .getChildren(true, true, true)
      .filter((timeline) => timeline.vars.repeat === -1).length,
  }));
  assert.equal(reducedState.allSettled, true);
  assert.equal(reducedState.loopingTimelines, 0);
  assert.deepEqual(reducedPageErrors, []);
  console.log("PASS: visible covers animate, offscreen covers pause, and reduced motion settles all covers");
} finally {
  await browser.close();
}
