"use strict";

window.AtlasRender = Object.freeze({
  generatorCard(item) {
    const ui = window.AtlasUI;
    return `
      <article class="catalog-card">
        <button class="catalog-card__media" type="button" data-generator="${ui.escape(item.id)}" aria-label="查看${ui.escape(item.name)}">
          ${ui.mediaMarkup(item.poster, item.name)}
        </button>
        <div class="catalog-card__body">
          <p class="catalog-card__meta">${ui.escape(item.family)} / ${ui.escape(item.output)}</p>
          <h3>${ui.escape(item.name)}</h3>
          <p>${ui.escape(item.description)}</p>
          <button class="card-action" type="button" data-generator="${ui.escape(item.id)}">查看能力</button>
        </div>
      </article>
    `;
  },

  styleCard(style) {
    const ui = window.AtlasUI;
    return `
      <article class="catalog-card catalog-card--style">
        <button class="catalog-card__media" type="button" data-style="${ui.escape(style.id)}" aria-label="查看${ui.escape(style.name)}">
          <img src="${ui.imageForStyle(style.images[0])}" alt="${ui.escape(style.name)}样片" loading="lazy" decoding="async">
        </button>
        <div class="catalog-card__body">
          <p class="catalog-card__meta">${ui.escape(style.id)} / ${ui.escape(style.group)}</p>
          <h3>${ui.escape(style.name)}</h3>
          <p>${ui.escape(style.tone)}</p>
          <button class="card-action" type="button" data-style="${ui.escape(style.id)}">查看画风</button>
        </div>
      </article>
    `;
  },

  effectCard(effect, index) {
    const ui = window.AtlasUI;
    return `
      <article class="effect-card">
        <button class="effect-card__preview" type="button" data-effect="${ui.escape(effect.id)}" aria-label="播放${ui.escape(effect.label)}真实演示">
          ${ui.effectPreview(effect, index)}
        </button>
        <div class="effect-card__body">
          <p><span>${ui.escape(effect.id.replace("fx-", ""))}</span>${ui.escape(effect.family)}</p>
          <h3>${ui.escape(effect.label)}</h3>
          <button class="card-action" type="button" data-effect="${ui.escape(effect.id)}">真实演示</button>
        </div>
      </article>
    `;
  },

  familyBoard(generators) {
    const ui = window.AtlasUI;
    const grouped = generators.reduce((result, item) => {
      const items = result.get(item.family) ?? [];
      items.push(item);
      result.set(item.family, items);
      return result;
    }, new Map());
    return [...grouped.entries()].map(([family, items], index) => `
      <button class="family-tile" type="button" data-family-jump="${ui.escape(family)}">
        <span class="family-tile__index">${String(index + 1).padStart(2, "0")}</span>
        <strong>${ui.escape(family)}</strong>
        <span>${items.length} 项能力</span>
      </button>
    `).join("");
  },
});
