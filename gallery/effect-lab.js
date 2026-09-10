"use strict";

const params = new URLSearchParams(window.location.search);
const effectName = params.get("name") ?? "wipe";
const effects = window.AtlasEffects;
const spec = effects.specFor(effectName);
const root = document.querySelector("#effect-lab-root");
root.innerHTML = effects.markup(effectName, "stage");

const scene = root.querySelector(".test-effect");
const timeline = window.AtlasEffectMotion.timelineFor(scene, spec);
window.__timelines = { "fixed-effect-lab": timeline };
window.seekEffect = (time) => {
  timeline.pause(time);
};
window.__effectLabReady = true;
timeline.play(0);
