# Generation Atlas Design System

## 1. Product and atmosphere

This is a unified visual index of the generative systems under `D:\GitHub Program`: image recipes, video workflows, motion systems, presentation tools, audio generators, and the complete HyperFrames effect registry. It should feel like a quiet studio archive: warm paper, dark ink, real artwork, and compact editorial labels. Samples remain the focus. The interface must make 202 heterogeneous capabilities comparable without flattening them into one visual style.

## 2. Color

Use semantic CSS tokens only.

### Light

| Token | Value | Use |
|---|---|---|
| `--canvas` | `#f2eee6` | Page background |
| `--surface` | `#fbf8f1` | Cards and controls |
| `--surface-strong` | `#e8e1d5` | Image wells and selected filters |
| `--ink` | `#24211d` | Primary text |
| `--ink-muted` | `#6d675f` | Supporting text |
| `--line` | `#d4ccbf` | Borders and dividers |
| `--accent` | `#b8442f` | Active state and focus |
| `--accent-ink` | `#fff8ee` | Text on accent |

### Dark

| Token | Value | Use |
|---|---|---|
| `--canvas` | `#1b1a18` | Page background |
| `--surface` | `#25231f` | Cards and controls |
| `--surface-strong` | `#34302a` | Image wells and selected filters |
| `--ink` | `#f1eadf` | Primary text |
| `--ink-muted` | `#b9b0a4` | Supporting text |
| `--line` | `#49443d` | Borders and dividers |
| `--accent` | `#e07a61` | Active state and focus |
| `--accent-ink` | `#211b18` | Text on accent |

Contrast target: WCAG AA minimum, AAA for body copy when practical.

## 3. Typography

- Display: `"Iowan Old Style", "Songti SC", "STSong", Georgia, serif`
- UI and body: `"PingFang SC", "Microsoft YaHei", system-ui, sans-serif`
- Metadata: `"SFMono-Regular", Consolas, monospace`

| Token | Size | Line height | Use |
|---|---:|---:|---|
| `--text-xs` | 12px | 1.5 | Aliases and counts |
| `--text-sm` | 14px | 1.55 | Card support text |
| `--text-md` | 16px | 1.65 | Controls and dialog body |
| `--text-lg` | 20px | 1.35 | Card titles |
| `--text-xl` | clamp(34px, 6vw, 68px) | 1.08 | Page title |
| `--text-dialog` | clamp(28px, 4vw, 48px) | 1.12 | Dialog title |

## 4. Spacing and grid

Base unit: 4px.

| Token | Value |
|---|---:|
| `--space-1` | 4px |
| `--space-2` | 8px |
| `--space-3` | 12px |
| `--space-4` | 16px |
| `--space-6` | 24px |
| `--space-8` | 32px |
| `--space-12` | 48px |
| `--space-16` | 64px |

- Content width: 1480px maximum.
- Generator and style galleries: responsive auto-fill grid, 288px minimum card width.
- Effect gallery: denser responsive grid, 248px minimum card width.
- Breakpoints: 640px and 960px.
- Mobile: single column, full-width controls, reduced outer spacing.

## 5. Components

### Filter bar

- Search field plus category buttons.
- Selected category uses `--surface-strong` and a clear inset border.
- Every button exposes `aria-pressed`; search has a visible label.

### Style card

- Real sample image in a neutral image well using `object-fit: contain`.
- Number, group, title, one-sentence character, and aliases below.
- The sample button opens the detail dialog. A secondary button copies the invocation phrase.
- Hover uses a small negative translate and border-color change. Focus uses a 3px accent ring.

### Generator card

- Real poster, GIF, or muted looping video above the capability description.
- Every poster maps one-to-one to the named source capability; unrelated, generic, or reused media is not acceptable evidence.
- Presentation and deck generators use a contact sheet of at least three distinct 16:9 slide frames from that tool's real output. Browser pages, documentation, dashboards, editor chrome, single slides, and single webpage screenshots must not stand in for a deck.
- Family and output type are the first metadata line.
- Detail dialog shows the source project path and a copyable invocation note.

### Effect card

- Every effect uses the same fixed generated artwork, `effect-gouache-portrait.png`, as plate A. Transition and before/after effects may additionally use only the fixed generated artwork `effect-ink-family.png` as plate B.
- Plate A is a high-contrast teal-and-orange painted portrait with strong facial detail, textured brushwork, and a circular light field. Plate B is a bright paper-and-ink family scene under an orange umbrella. Their stable subject placement, tonal contrast, texture, and distinct light/dark balance keep blur, grain, distortion, masks, wipes, displacement, and color effects legible at card size without looking like a diagnostic chart.
- Cards play deterministic functional preview loops while they are visible or about to enter the viewport; offscreen previews pause. They keep the fixed A/B artwork and never rotate themes or introduce an image carousel.
- A mode-level state is not sufficient: every registry effect receives a deterministic signature derived from its name. The signature varies only effect-relevant properties such as blur strength, grain density, mask geometry, reveal direction, displacement, grid form, highlight position, and caption treatment. It never changes the A/B artwork. Repeated effects within one family must therefore remain comparable without appearing as duplicated cards.
- Text-effect cards use only the neutral `Aa` specimen inside the preview. The card title below already identifies the effect, so neither implementation placeholders (`FIXED INPUT`) nor effect-name labels are repeated over the artwork.
- Opening a card loads the normalized HyperFrames effect lab, which plays the corresponding effect against the same A or A/B inputs. Registry names remain the catalog identity; registry-specific artwork and composition content do not enter the comparison surface.
- The generated plates retain their original palettes. Effect overlays continue to use the existing semantic effect colors; no per-card tint or substitute artwork may be introduced.

### View navigation

- Sticky segmented navigation switches among overview, generators, styles, and effects.
- Exactly one view is visible at a time and the active button exposes `aria-pressed`.
- View changes scroll the active section below the sticky masthead at every breakpoint; headings must never land underneath it.

### Detail dialog

- Native `<dialog>` for keyboard and focus behavior.
- Large sample area, description, aliases, and all available variants.
- Copy actions produce complete fill-in invocation templates with an action, source, input slots, and execution expectations; labels or paths alone are not valid invocation information.
- Dialog content scrolls independently between the header and a persistent copy action, so close and copy remain visible on mobile, tablet, and desktop.
- Effect dialogs describe the normalized motion in two plain-language lines: `画面怎么动` states the direction, timing, and transformation; `判断是否生效` names the easiest visual anchor to watch. Generic fixed-input copy is not sufficient.
- Close and copy actions remain visible without obscuring the artwork.

### Empty state

- Plain language, no illustration.
- Offers one action: clear filters.

## 6. Motion and interaction

- Motion intensity: 2/10.
- Standard transition: 180ms ease-out.
- Interface motion uses only `transform` and `opacity`; functional effect previews may additionally animate the effect-specific `filter` and `clip-path` properties required to demonstrate the cataloged behavior.
- Respect `prefers-reduced-motion: reduce`; remove card translation and dialog transition.
- Escape closes the dialog. Clicking the backdrop closes it. Search updates results immediately.
- Effect loops reuse the same normalized timeline as the detail lab, run only near the viewport, and pause offscreen. They are functional previews, not decorative motion; `prefers-reduced-motion` collapses them to a settled representative frame.

## 7. Depth and surface

Use a borders-only strategy.

- Cards and controls use 1px `--line` borders.
- No outer glows and no decorative drop shadows.
- Rounded corners: 10px for controls, 16px for cards, 20px for the dialog.
- Artwork wells may use a faint tonal shift but no texture overlay.
