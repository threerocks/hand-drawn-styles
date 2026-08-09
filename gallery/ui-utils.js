"use strict";

window.AtlasUI = Object.freeze({
  escape(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  },

  imageForStyle(filename) {
    return `./assets/style-previews/${filename}`;
  },

  mediaMarkup(source, alt, className = "") {
    const safeSource = this.escape(source);
    const safeAlt = this.escape(alt);
    const classAttribute = className ? ` class="${this.escape(className)}"` : "";
    if (/\.(mp4|webm)$/i.test(source)) {
      return `<video${classAttribute} src="${safeSource}" autoplay muted loop playsinline aria-label="${safeAlt}"></video>`;
    }
    return `<img${classAttribute} src="${safeSource}" alt="${safeAlt}" loading="lazy" decoding="async">`;
  },

  effectPreview(effect) {
    return window.AtlasEffects.markup(effect.name, "card");
  },

  buttonGroup(items, active, attribute) {
    return items.map((item) => `
      <button
        class="filter${item === active ? " is-active" : ""}"
        type="button"
        ${attribute}="${this.escape(item)}"
        aria-pressed="${item === active}"
      >${this.escape(item)}</button>
    `).join("");
  },

  searchable(item) {
    return Object.values(item)
      .flat()
      .filter((value) => typeof value === "string")
      .join(" ")
      .toLocaleLowerCase("zh-CN");
  },
});
