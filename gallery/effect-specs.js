"use strict";

window.AtlasEffects = Object.freeze({
  plateA: "./assets/effect-plates/effect-gouache-portrait.png",
  plateB: "./assets/effect-plates/effect-ink-family.png",

  signatureFor(name) {
    let hash = 2166136261;
    for (const character of name) {
      hash ^= character.charCodeAt(0);
      hash = Math.imul(hash, 16777619);
    }
    hash >>>= 0;
    return Object.freeze({
      variant: hash % 8,
      x: ((hash >>> 3) % 19) - 9,
      y: ((hash >>> 8) % 13) - 6,
      tilt: ((hash >>> 12) % 13) - 6,
      scale: (104 + ((hash >>> 16) % 14)) / 100,
      saturation: (96 + ((hash >>> 14) % 27)) / 100,
      blur: (14 + ((hash >>> 20) % 24)) / 100,
      grid: 10 + ((hash >>> 24) % 13),
      hue: hash % 280,
      cut: 30 + ((hash >>> 5) % 31),
      cutAlt: 35 + ((hash >>> 11) % 31),
      grain: 3 + ((hash >>> 17) % 5),
    });
  },

  specFor(name) {
    const rules = [
      ["data", /swiss-grid|decision-tree|nyt-graph/],
      ["vignette", /vignelli/],
      ["caption", /kinetic-type/],
      ["camera", /product-promo|app-showcase/],
      ["blur", /blur|defocus|bokeh/],
      ["grain", /grain|noise|texture/],
      ["vignette", /vignette|dark-card/],
      ["pixel", /pixel|matrix/],
      ["glitch", /glitch|chromatic|rgb|scanline/],
      ["shatter", /shatter|destruction|assemble|fragment/],
      ["dissolve", /dissolve|particle/],
      ["wipe", /wipe|cover|mask|reveal/],
      ["push", /push|slide|carousel/],
      ["scale", /scale|zoom|unzoom/],
      ["rotate", /rotate|flip|3d|cube/],
      ["warp", /warp|vortex|portal|magnetic|distortion/],
      ["liquid", /liquid|glass|ripple|wave|fluid/],
      ["lens", /lens|iris|spotlight/],
      ["burn", /burn|thermal|ember|fire/],
      ["light", /light|flash|shimmer|glow|flare/],
      ["caption", /caption|lower-third|^lt-|ticker|post|notification/],
      ["code", /code|terminal|editor|vscode/],
      ["data", /map|chart|graph|flow|decision|money|flight/],
      ["camera", /camera|pan|parallax|motion/],
    ];
    const mode = rules.find(([, pattern]) => pattern.test(name))?.[0] ?? "wipe";
    const transitionModes = new Set([
      "dissolve", "shatter", "wipe", "push", "scale", "rotate", "warp", "liquid", "lens", "burn",
    ]);
    const transition = transitionModes.has(mode) || /^transitions-|transition|wipe/.test(name);
    return Object.freeze({ mode, transition });
  },

  descriptionFor(name) {
    const spec = this.specFor(name);
    const descriptions = {
      blur: spec.transition
        ? {
            motion: "底片 A 先逐渐失焦并轻微放大，随后底片 B 从左向右覆盖进来。",
            cue: "盯住人物眼睛和轮廓；前半段会明显变糊，后半段左侧会出现第二张图。",
          }
        : {
            motion: "整张画面从清晰逐渐变成强模糊，同时缓慢放大约 8%。",
            cue: "盯住人物眼睛、胡须和衣领；这些细节会持续失去锐度。",
          },
      grain: {
        motion: "细密颗粒从很淡逐渐加重，并在画面上轻微横向漂移。",
        cue: "观察脸部暗部和纯色背景；会出现不断增强的细小噪点。",
      },
      vignette: {
        motion: "画面四周逐渐压暗，中心人物保持相对明亮。",
        cue: "对比四个角和人物面部；角落会越来越暗，视线被收拢到中央。",
      },
      pixel: spec.transition
        ? {
            motion: "像素网格逐渐显现，底片 B 以分级跳动的方式从左向右展开。",
            cue: "观察竖向揭示边界；它不是连续滑动，而是按格子一段段前进。",
          }
        : {
            motion: "网格从稀薄放大状态收紧并加深，同时画面对比度上升、颜色减少。",
            cue: "观察脸部和橙色圆环；边缘会呈现明显的块状网格感。",
          },
      glitch: {
        motion: "一条偏色的横向画面切片从左向右错位，并逐渐增强。",
        cue: "盯住人物眼睛附近；会出现青红偏色和横向断裂的局部切片。",
      },
      dissolve: {
        motion: "底片 B 从透明和轻微模糊状态逐渐溶解显现，最后恢复清晰。",
        cue: "观察人物轮廓；第二张图会像雾散开一样由虚到实。",
      },
      shatter: {
        motion: "底片 B 由中心碎片区域向外扩张，碎裂遮罩逐步拼成完整画面。",
        cue: "观察画面中央的不规则折线边界；可见区域会沿碎片形状扩大。",
      },
      push: {
        motion: "底片 A 向左退出，底片 B 同时从右侧推入，完成整幅画面的替换。",
        cue: "盯住画面中线；两张图会并排经过，移动方向相反。",
      },
      scale: {
        motion: "底片 B 从很小、近乎透明的状态向中心放大，并逐渐变为不透明。",
        cue: "观察画面中心；第二张图会像卡片一样从小到大落到全幅。",
      },
      rotate: {
        motion: "底片 A 像门板一样向后翻走，底片 B 从另一侧进行三维翻转接入。",
        cue: "观察画面中央的透视折叠；图像宽度会先被压窄再展开。",
      },
      warp: {
        motion: "底片 B 从中央圆形区域出现，带着倾斜和拉伸向外扩张。",
        cue: "盯住人物面部中心；圆形揭示区会扩大，边缘同时发生扭曲。",
      },
      liquid: {
        motion: "底片 B 从中央液滴状椭圆向四周扩散，边缘由圆润逐渐铺满画面。",
        cue: "观察中央遮罩边缘；它会像水洼扩散一样持续变大。",
      },
      lens: {
        motion: "一个圆形镜头窗口从人物右上方展开，窗口内画面由放大逐渐回到正常比例。",
        cue: "盯住眼睛附近的圆形区域；圆圈会扩大，圈内缩放与圈外不同。",
      },
      burn: {
        motion: "底片 B 沿圆形区域向外烧开，同时出现一圈短暂增强的橙红亮边。",
        cue: "观察人物面部周围；扩张边缘会出现明显的暖色光圈。",
      },
      light: spec.transition
        ? {
            motion: "一道高亮光带横向扫过画面，同时底片 B 从左向右显现。",
            cue: "观察移动的白色亮带；亮带经过的位置会逐步换成第二张图。",
          }
        : {
            motion: "一道高亮光带从左侧穿过主体并移向右侧。",
            cue: "盯住人物脸部和衣服；会有一条明亮反光带快速扫过。",
          },
      caption: {
        motion: "文字样式从画面下方上移进入，并在约 1.4 秒后停在最终位置。",
        cue: "观察预览中的 Aa 字样；它会由下向上出现，而不是一直静止。",
      },
      code: {
        motion: "代码线条由淡到浓显现，并从上方向下轻微漂移。",
        cue: "观察人物前方的青色横线；线条数量和亮度会逐渐增强。",
      },
      data: {
        motion: "数据网格从底部向上揭示，透明度同步增加。",
        cue: "观察图表边框和折线；它们会自下而上逐步完整出现。",
      },
      camera: {
        motion: "镜头从正常景别缓慢推近，人物放大约 22%，并轻微向右上方移动。",
        cue: "盯住人物脸部和背后的橙色圆环；二者会持续变大，构图位置也会缓慢偏移。",
      },
      wipe: {
        motion: "底片 B 沿竖向边界从左向右擦入，逐步覆盖底片 A。",
        cue: "观察画面中的竖向分界线；它会从左侧持续移向右侧。",
      },
    };
    const description = descriptions[spec.mode] ?? descriptions.wipe;
    return `画面怎么动：${description.motion}\n判断是否生效：${description.cue}`;
  },

  markup(name, context = "card") {
    const spec = this.specFor(name);
    const signature = this.signatureFor(name);
    const sourceB = spec.transition ? this.plateB : this.plateA;
    return `
      <div
        class="test-effect test-effect--${spec.mode} test-effect--${context}"
        data-mode="${spec.mode}"
        data-transition="${spec.transition}"
        data-effect="${name}"
        data-variant="${signature.variant}"
        data-signature="${name}-${signature.variant}"
        style="--preview-x:${signature.x}%;--preview-y:${signature.y}%;--preview-tilt:${signature.tilt}deg;--preview-scale:${signature.scale};--preview-saturation:${signature.saturation};--preview-blur:${signature.blur}rem;--preview-grid:${signature.grid}px;--preview-hue:${signature.hue}deg;--preview-cut:${signature.cut}%;--preview-cut-negative:-${signature.cut}%;--preview-cut-alt:${signature.cutAlt}%;--preview-inset:${signature.cut / 3}%;--preview-rotate-y:${(signature.tilt - 18) * 1.5}deg;--preview-grain:${signature.grain}px;--preview-grain-alt:${signature.grain + 2}px;--preview-grain-mask:${signature.grain + 1}px;--preview-grain-gap:${signature.grain + 7}px"
      >
        <img class="test-effect__plate test-effect__plate--a" src="${this.plateA}" alt="">
        <img class="test-effect__plate test-effect__plate--b" src="${sourceB}" alt="">
        <span class="test-effect__grain"></span>
        <span class="test-effect__shade"></span>
        <span class="test-effect__sweep"></span>
        <span class="test-effect__grid"></span>
        <span class="test-effect__caption" aria-hidden="true"><strong>Aa</strong></span>
      </div>
    `;
  },
});
