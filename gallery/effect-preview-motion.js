"use strict";

const effectPreviewGrid = document.querySelector("#effect-grid");
const effectMotionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
const effectPreviewTimelines = new Map();
const registeredEffectPreviews = new Set();
const visibleEffectPreviews = new Set();

function timelineForPreview(scene) {
  const existing = effectPreviewTimelines.get(scene);
  if (existing) return existing;
  const spec = window.AtlasEffects.specFor(scene.dataset.effect);
  const timeline = window.AtlasEffectMotion.timelineFor(scene, spec, {
    repeat: -1,
    repeatDelay: 0.6,
  });
  const phase = (Number(scene.dataset.variant) / 8) * window.AtlasEffectMotion.duration;
  timeline.pause(phase);
  effectPreviewTimelines.set(scene, timeline);
  return timeline;
}

function updatePreviewPlayback(scene) {
  const timeline = effectPreviewTimelines.get(scene);
  if (effectMotionPreference.matches) {
    timeline?.pause(window.AtlasEffectMotion.duration);
    scene.dataset.motionState = "settled";
    return;
  }
  if (!visibleEffectPreviews.has(scene) || document.hidden) {
    timeline?.pause();
    scene.dataset.motionState = timeline ? "paused" : "waiting";
    return;
  }
  timelineForPreview(scene).play();
  scene.dataset.motionState = "playing";
}

const effectPreviewObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    const scene = entry.target;
    if (entry.isIntersecting) visibleEffectPreviews.add(scene);
    else visibleEffectPreviews.delete(scene);
    updatePreviewPlayback(scene);
  });
}, { rootMargin: "120px 0px" });

function syncEffectPreviews() {
  const currentPreviews = new Set(
    effectPreviewGrid.querySelectorAll(".test-effect--card"),
  );
  registeredEffectPreviews.forEach((scene) => {
    if (currentPreviews.has(scene)) return;
    effectPreviewObserver.unobserve(scene);
    effectPreviewTimelines.get(scene)?.kill();
    effectPreviewTimelines.delete(scene);
    registeredEffectPreviews.delete(scene);
    visibleEffectPreviews.delete(scene);
  });
  currentPreviews.forEach((scene) => {
    if (registeredEffectPreviews.has(scene)) return;
    scene.dataset.motionState = effectMotionPreference.matches ? "settled" : "waiting";
    registeredEffectPreviews.add(scene);
    effectPreviewObserver.observe(scene);
  });
}

new MutationObserver(syncEffectPreviews).observe(effectPreviewGrid, { childList: true });
effectMotionPreference.addEventListener("change", () => {
  registeredEffectPreviews.forEach(updatePreviewPlayback);
});
document.addEventListener("visibilitychange", () => {
  registeredEffectPreviews.forEach(updatePreviewPlayback);
});

window.AtlasEffectPreviews = Object.freeze({ refresh: syncEffectPreviews });
syncEffectPreviews();
