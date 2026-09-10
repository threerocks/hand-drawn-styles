"use strict";

const catalog = window.GENERATION_CATALOG;
const ui = window.AtlasUI;
const render = window.AtlasRender;
const invocations = window.AtlasInvocations;
const state = {
  view: "overview",
  generatorFamily: "全部",
  styleGroup: "全部",
  effectFamily: "全部",
};

const sections = [...document.querySelectorAll("[data-section]")];
const viewButtons = [...document.querySelectorAll("[data-view]")];
const generatorGrid = document.querySelector("#generator-grid");
const styleGrid = document.querySelector("#style-grid");
const effectGrid = document.querySelector("#effect-grid");
const generatorSearch = document.querySelector("#generator-search");
const styleSearch = document.querySelector("#style-search");
const effectSearch = document.querySelector("#effect-search");
const dialog = document.querySelector("#detail-dialog");
const detailMedia = document.querySelector("#detail-media");
const detailMeta = document.querySelector("#detail-meta");
const detailTitle = document.querySelector("#detail-title");
const detailDescription = document.querySelector("#detail-description");
const detailTags = document.querySelector("#detail-tags");
const detailSource = document.querySelector("#detail-source");
const detailCopy = document.querySelector("#detail-copy");
let iframeObserver;
let copyFeedbackTimeout;

function setView(view, scroll = true) {
  state.view = view;
  sections.forEach((section) => {
    section.hidden = section.dataset.section !== view;
  });
  viewButtons.forEach((button) => {
    const isActive = button.dataset.view === view;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
  if (scroll) document.querySelector("#catalog-main").scrollIntoView({ behavior: "smooth" });
}

function filterBy(items, query, group, key) {
  const normalized = query.trim().toLocaleLowerCase("zh-CN");
  return items.filter((item) => {
    const matchesGroup = group === "全部" || item[key] === group;
    return matchesGroup && ui.searchable(item).includes(normalized);
  });
}

function renderGenerators() {
  const items = filterBy(catalog.generators, generatorSearch.value, state.generatorFamily, "family");
  generatorGrid.innerHTML = items.map(render.generatorCard).join("");
  document.querySelector("#generator-count").textContent = `显示 ${items.length} / ${catalog.generators.length} 项能力`;
  document.querySelector("#generator-empty").hidden = items.length > 0;
}

function renderStyles() {
  const items = filterBy(catalog.styles, styleSearch.value, state.styleGroup, "group");
  styleGrid.innerHTML = items.map(render.styleCard).join("");
  document.querySelector("#style-count").textContent = `显示 ${items.length} / ${catalog.styles.length} 套画风`;
  document.querySelector("#style-empty").hidden = items.length > 0;
}

function renderEffects() {
  const items = filterBy(catalog.effects, effectSearch.value, state.effectFamily, "family");
  effectGrid.innerHTML = items.map(render.effectCard).join("");
  document.querySelector("#effect-count").textContent = `显示 ${items.length} / ${catalog.effects.length} 个特效`;
  document.querySelector("#effect-empty").hidden = items.length > 0;
}

function setFilters(container, values, active, attribute) {
  container.innerHTML = ui.buttonGroup(["全部", ...values], active, attribute);
}

async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.className = "clipboard-fallback";
  document.body.append(textarea);
  textarea.select();
  document.execCommand("copy");
  textarea.remove();
}

function resetCopyFeedback() {
  window.clearTimeout(copyFeedbackTimeout);
  copyFeedbackTimeout = undefined;
  detailCopy.textContent = "复制调用信息";
}

function configureDialog(meta, title, description, tags, source, copyValue) {
  resetCopyFeedback();
  detailMeta.textContent = meta;
  detailTitle.textContent = title;
  detailDescription.textContent = description;
  detailTags.innerHTML = tags.map((tag) => `<span>${ui.escape(tag)}</span>`).join("");
  detailSource.textContent = source;
  detailCopy.dataset.copy = copyValue;
  dialog.showModal();
}

function openGenerator(id) {
  const item = catalog.generators.find((candidate) => candidate.id === id);
  if (!item) return;
  detailMedia.innerHTML = ui.mediaMarkup(item.poster, item.name, "dialog__asset");
  configureDialog(
    `${item.family} / ${item.output}`,
    item.name,
    item.description,
    [item.family, item.output],
    item.source,
    invocations.generator(item),
  );
}

function openStyle(id) {
  const item = catalog.styles.find((candidate) => candidate.id === id);
  if (!item) return;
  detailMedia.innerHTML = `
    <div class="dialog__style-gallery">
      ${item.images.map((image) => `<img src="${ui.imageForStyle(image)}" alt="${ui.escape(item.name)}样片" loading="lazy">`).join("")}
    </div>
  `;
  configureDialog(
    `${item.id} / ${item.group}`,
    item.name,
    item.tone,
    item.aliases,
    "D:\\GitHub Program\\hand-drawn-styles",
    invocations.style(item),
  );
}

function fitEffectFrame() {
  const stage = detailMedia.querySelector(".effect-stage");
  const frame = detailMedia.querySelector("iframe");
  if (!stage || !frame) return;
  const scale = Math.min(stage.clientWidth / 1920, stage.clientHeight / 1080);
  frame.style.left = `${(stage.clientWidth - (1920 * scale)) / 2}px`;
  frame.style.top = `${(stage.clientHeight - (1080 * scale)) / 2}px`;
  frame.style.transform = `scale(${scale})`;
}

function openEffect(id) {
  const item = catalog.effects.find((candidate) => candidate.id === id);
  if (!item) return;
  const runner = `./effect-lab.html?v=20260809-1400&name=${encodeURIComponent(item.name)}`;
  detailMedia.innerHTML = `
    <div class="effect-stage">
      <iframe src="${ui.escape(runner)}" title="${ui.escape(item.label)}真实特效演示" loading="eager"></iframe>
    </div>
  `;
  configureDialog(
    `HYPERFRAMES / ${item.family.toUpperCase()}`,
    item.label,
    window.AtlasEffects.descriptionFor(item.name),
    [item.family, window.AtlasEffects.specFor(item.name).mode, item.name],
    item.source,
    invocations.effect(item),
  );
  iframeObserver?.disconnect();
  iframeObserver = new ResizeObserver(fitEffectFrame);
  iframeObserver.observe(detailMedia);
  requestAnimationFrame(fitEffectFrame);
}

function handleCatalogClick(event) {
  const generator = event.target.closest("[data-generator]");
  const style = event.target.closest("[data-style]");
  const effect = event.target.closest("button[data-effect]");
  if (generator) openGenerator(generator.dataset.generator);
  if (style) openStyle(style.dataset.style);
  if (effect) openEffect(effect.dataset.effect);
}

function clearCatalog(kind) {
  const settings = {
    generators: {
      input: generatorSearch, stateKey: "generatorFamily", filters: "#generator-filters",
      values: catalog.families, attribute: "data-generator-family",
      render: renderGenerators,
    },
    styles: {
      input: styleSearch, stateKey: "styleGroup", filters: "#style-filters",
      values: [...new Set(catalog.styles.map((item) => item.group))], attribute: "data-style-group",
      render: renderStyles,
    },
    effects: {
      input: effectSearch, stateKey: "effectFamily", filters: "#effect-filters",
      values: ["block", "component", "example"], attribute: "data-effect-family",
      render: renderEffects,
    },
  };
  const setting = settings[kind];
  if (!setting) return;
  setting.input.value = "";
  state[setting.stateKey] = "全部";
  setFilters(document.querySelector(setting.filters), setting.values, "全部", setting.attribute);
  setting.render();
  setting.input.focus();
}

viewButtons.forEach((button) => {
  button.addEventListener("click", () => setView(button.dataset.view));
});

document.querySelectorAll("[data-jump]").forEach((button) => {
  button.addEventListener("click", () => setView(button.dataset.jump));
});

document.querySelector("#family-board").addEventListener("click", (event) => {
  const button = event.target.closest("[data-family-jump]");
  if (!button) return;
  state.generatorFamily = button.dataset.familyJump;
  setFilters(document.querySelector("#generator-filters"), catalog.families, state.generatorFamily, "data-generator-family");
  renderGenerators();
  setView("generators");
});

document.querySelectorAll(".catalog-grid, .effect-grid").forEach((grid) => {
  grid.addEventListener("click", handleCatalogClick);
});

document.querySelectorAll("[data-clear]").forEach((button) => {
  button.addEventListener("click", () => clearCatalog(button.dataset.clear));
});

document.querySelector("#generator-filters").addEventListener("click", (event) => {
  const button = event.target.closest("[data-generator-family]");
  if (!button) return;
  state.generatorFamily = button.dataset.generatorFamily;
  setFilters(event.currentTarget, catalog.families, state.generatorFamily, "data-generator-family");
  renderGenerators();
});

document.querySelector("#style-filters").addEventListener("click", (event) => {
  const button = event.target.closest("[data-style-group]");
  if (!button) return;
  state.styleGroup = button.dataset.styleGroup;
  const groups = [...new Set(catalog.styles.map((item) => item.group))];
  setFilters(event.currentTarget, groups, state.styleGroup, "data-style-group");
  renderStyles();
});

document.querySelector("#effect-filters").addEventListener("click", (event) => {
  const button = event.target.closest("[data-effect-family]");
  if (!button) return;
  state.effectFamily = button.dataset.effectFamily;
  setFilters(event.currentTarget, ["block", "component", "example"], state.effectFamily, "data-effect-family");
  renderEffects();
});

generatorSearch.addEventListener("input", renderGenerators);
styleSearch.addEventListener("input", renderStyles);
effectSearch.addEventListener("input", renderEffects);
document.querySelector("#detail-close").addEventListener("click", () => dialog.close());
detailCopy.addEventListener("click", async () => {
  const copyValue = detailCopy.dataset.copy;
  resetCopyFeedback();
  await copyText(copyValue);
  if (!dialog.open || detailCopy.dataset.copy !== copyValue) return;
  detailCopy.textContent = "已复制";
  copyFeedbackTimeout = window.setTimeout(resetCopyFeedback, 1400);
});
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});
dialog.addEventListener("close", () => {
  iframeObserver?.disconnect();
  resetCopyFeedback();
});

document.querySelector("#family-board").innerHTML = render.familyBoard(catalog.generators);
setFilters(document.querySelector("#generator-filters"), catalog.families, state.generatorFamily, "data-generator-family");
setFilters(document.querySelector("#style-filters"), [...new Set(catalog.styles.map((item) => item.group))], state.styleGroup, "data-style-group");
setFilters(document.querySelector("#effect-filters"), ["block", "component", "example"], state.effectFamily, "data-effect-family");
renderGenerators();
renderStyles();
renderEffects();
setView("overview", false);
