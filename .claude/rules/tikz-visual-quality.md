---
paths:
  - "**/*.sty"
  - "**/*_theme_test.tex"
  - "**/*.tex"
---

# TikZ & Beamer Layout Visual Quality Standards

**Every TikZ diagram and every theme layout change must be visually polished —
and robust to realistic content — before it is considered complete.**

This repo's themes are built almost entirely out of TikZ (backgrounds, frame
titles, the section progress bar) plus stacked `beamercolorbox`es, so these
standards apply to the `.sty` files themselves, not just to figures.

## Layout Robustness (this repo's priority)

- **Derive, don't hard-code.** Prefer `\paperwidth`, `\paperheight`, `\textheight`,
  and Beamer length registers over absolute centimeters. Hard-coded coordinates
  tuned for `aspectratio=169` break on multi-line titles and other aspect ratios.
- **Content must reflow, not overflow.** A two-line `\title` or long `\frametitle`
  must not collide with band edges, body text, or the frame number.
- **Bands must share exact edges.** The gold accent line and the blue band should
  meet with no sliver gap and no overlap.
- **Test against hard cases** before declaring done: a 2-line title, a long frame
  title, and (where claimed to support it) a non-16:9 aspect ratio.

## Label Positioning

- Labels must NEVER overlap with curves, lines, dots, braces, or other labels.
- Stagger labels near the same vertical position. Use consistent font size.
- Annotation labels sit adjacent to braces/arrows, outside the data area.

## Visual Semantics

- **Solid dots/lines** = observed / realized; **hollow circles / dashed lines** =
  counterfactual / unrealized.
- Use the theme palette consistently: `ucdavisBlue`, `ucdavisGold` (defined in the
  color themes). Define new colors in the color theme for reuse, not inline.

### Line Weights
- Axes: `thick` · Data lines: `thick` · Annotation arrows: `thick` (NOT `very thick`)
- Grid/reference lines: `dashed, gray!40`

## Spacing and Proportions

- Minimum ~0.2 units between any label and the nearest graphical element.
- Axes extend beyond all data points. Dot radius `4pt` for data points.

## Checklist

```
[ ] Multi-line title / long frame title does not overflow or collide
[ ] Band coordinates derived from paper dimensions where feasible
[ ] Gold accent line and blue band share an exact edge
[ ] No label-label and no label-curve overlaps
[ ] Consistent dot style (solid=observed, hollow=counterfactual)
[ ] Consistent line style (solid=observed, dashed=counterfactual)
[ ] Palette colors used consistently (ucdavisBlue / ucdavisGold)
[ ] Arrow annotations point FROM label TO feature
[ ] Labels legible at presentation size
[ ] Preview PDF regenerated and eyeballed (scripts/build.sh)
```
