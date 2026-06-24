# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Custom, unofficial LaTeX Beamer themes for UC Davis-affiliated presentations. There are two brands, packaged as three theme directories:

- `ucdavis_beamer_theme_xelatex/` — UC Davis theme, **XeLaTeX/LuaLaTeX only** (uses `fontspec`, main font Helvetica Neue).
- `ucdavis_beamer_theme_pdflatex/` — the same UC Davis theme, **pdfLaTeX-compatible** (no `fontspec`; uses `helvet`, the Helvetica clone, as the pdfLaTeX stand-in for Helvetica Neue). The *only* substantive difference from the xelatex variant is the font setup — the other three `.sty` files are byte-identical.
- `ca_ed_lab_beamer_theme/` — California Education Lab theme, a faithful port of the **official CEL PowerPoint template**. **pdfLaTeX** (uses `carlito`, the free Calibri-metric clone — no `fontspec`/XeLaTeX needed). Brand colors navy `#014B84` + gold `#DFB305`. Has TOC styling and auto section dividers (but no section progress bar). Spacing is fully paper-size-derived, so the **same source renders at the native 4:3 and at 16:9** via the beamer `aspectratio` option; the dir ships both preview decks.

`assets/` holds logos/wordmarks (official UC Davis brand files under `assets/ucdavis_wordmarks/`, plus `expanded_logo_gold-blue.png`, the CEL logo `cel_logo.png` used by the caedlab theme, and the legacy/unused `ca_ed_lab.png` from the old CEL theme). `resources/` holds a Beamer cheat sheet PDF.

## Theme architecture

Each theme follows Beamer's standard four-file split. `\usetheme{<name>}` loads `beamertheme<name>.sty`, which loads the other three:

- `beamertheme<name>.sty` — **master file.** `\useinnertheme` / `\useoutertheme` / `\usecolortheme`, font setup, itemize markers, blocks style. The UC Davis theme *also* defines its TOC styling (gold-numbered circles + rules), the TikZ section **progress bar** (`\sectionprogressbar`), and an `\AtBeginSection` hook that auto-generates a section-title slide. The caedlab master likewise defines TOC styling (gold numbered circles) and an `\AtBeginSection` section divider (navy slide, gold crossing rules, centered title) — but **no** progress bar; it also intercepts `\section` (via `\RenewDocumentCommand`) to capture the raw title so the divider can title-case it with `titlecaps`' `\titlecap` (`\insertsection` itself expands to a `\hyperlink` wrapper that can't be processed).
- `beamercolortheme<name>.sty` — color definitions and structural colors.
- `beamerinnertheme<name>.sty` — the slide **background** (the blue/gold bands) and the **title page** template.
- `beameroutertheme<name>.sty` — the **frametitle** template (title text + frame number, positioned with TikZ).

Internal theme name: both UC Davis variants use the name `ucdavis` (so `beamerthemeucdavis.sty` exists in both the xelatex and pdflatex dirs — you cannot have both on the TeX path at once; you copy the variant you want into your presentation). The CA Ed Lab theme is named `caedlab`.

### Cross-cutting facts worth knowing before editing

- **Each brand now owns its colors.** The UC Davis themes define `ucdavisBlue` (`cmyk 1,0.56,0,0.34`) and `ucdavisGold` (`RGB 255,191,0`). The caedlab theme defines its own `celNavy` (`#014B84`) and `celGold` (`#DFB305`) in its master file (not the color theme) — it no longer reuses the `ucdavis*` names. (Historical note: the *old* CA Ed Lab theme reused the `ucdavis*` color names.)
- **`\emph` and `\textbf` are redefined as color commands** in the UC Davis color theme: `\emph` → blue, `\textbf` → gold. This is surprising; bold text is not black. The CA Ed Lab theme does not do this.
- The CA Ed Lab title page expects a user-defined `\acknowledgement` macro (it defaults to the official CEL placeholder note). The CEL logo is bundled (`../assets/cel_logo.png`) and drawn automatically by the inner theme's title-slide background — no per-presentation path edit is needed, unlike the old theme.

### The hard-coded-spacing problem (resolved)

The original layouts were positioned with **absolute, hand-tuned coordinates**, which is why multi-line titles and non-16:9 aspect ratios broke them. All three themes are now dimension-derived and robust at 16:9 and 4:3:

- **`ucdavis_beamer_theme_xelatex`** — redesigned with dimension-derived spacing (bands/title via beamer templates + `\paperheight`-derived lengths `\udmargin`/`\udaccent`/`\udtitlepad`/`\udgoldblock`; reflowing frame titles).
- **`ucdavis_beamer_theme_pdflatex`** — the xelatex redesign ported down verbatim; only the font setup differs (`helvet` instead of `fontspec`/Helvetica Neue), so its color/inner/outer `.sty` files are byte-identical to the xelatex ones.
- **`ca_ed_lab_beamer_theme`** — separately ported from the CEL pptx, fully paper-size-derived (named lengths like `\celstrip`, `\celmargin`, `\celborderinset` as fractions of paper size).

When changing any layout, keep it "automatic": prefer deriving from `\paperheight`/`\paperwidth`/`\textheight` and Beamer length registers over absolute centimeters, and let boxes size to content instead of fixed `ht=`/`\vskip`. **Any change to the UC Davis layout must be made in both variants** (xelatex + pdflatex) to keep them in sync — only the master's font block should differ.

## Building / previewing

Use the build script — it compiles each sample `*_theme_test.tex` with the right engine, runs the multi-pass `latexmk` needs, and cleans aux files:

```bash
scripts/build.sh            # all three themes (caedlab builds both 4:3 and 16:9)
scripts/build.sh ucdavis-xe # UC Davis (XeLaTeX) only
scripts/build.sh ucdavis-pdf # UC Davis (pdfLaTeX) only
scripts/build.sh caedlab    # California Education Lab only (both aspect-ratio decks)
```

To compile by hand instead, do it **from within the theme directory** (the `.sty` files and relative asset paths like `../assets/cel_logo.png` resolve relative to it): `xelatex ucdavis_theme_test.tex` (UC Davis xelatex theme), `pdflatex ucdavis_theme_test.tex` (UC Davis pdflatex theme), or `pdflatex caedlab_theme_test.tex` / `pdflatex caedlab_theme_test_169.tex` (CEL theme — two decks from one shared body `caedlab_theme_content.tex`). Run the engine **twice** when the document has a TOC or the section progress bar — the progress bar reads `\insertframenumber/\inserttotalframenumber` and section counts (`totcount`), correct only on the second pass.

Each test file is the canonical smoke test and reference for what the theme should look like; the compiled `*_theme_test.pdf` is **committed and is the deliverable preview**. After a layout change, recompile the affected sample, eyeball the PDF, and commit the regenerated PDF alongside the `.sty` change (matches the "recompile samples" / "update template pdf" history). The `build-reminder` hook nudges this after a `.sty` edit.

### Deployment bundles (`dist/`)

For low-friction use on Overleaf (where there's no shared package store), each theme is also shipped as a **single-file** `beamertheme<name>.sty` under `dist/`, generated by `scripts/bundle.sh`:

- It inlines the color/inner/outer bodies into the master at the `\useinnertheme`/`\useoutertheme`/`\usecolortheme` call sites and strips the per-file `\mode<presentation>`/`\mode<all>` wrappers, leaving one wrapper around the whole file.
- For CEL it rewrites the logo path `../assets/cel_logo.png` → bare `cel_logo.png` and copies the PNG into `dist/caedlab/` (on Overleaf both files sit at the project root).
- Output dirs: `dist/ucdavis-xelatex/`, `dist/ucdavis-pdflatex/`, `dist/caedlab/`. (The two UC Davis bundles share the internal filename `beamerthemeucdavis.sty` but live at distinct paths/URLs.)

`scripts/build.sh` runs `bundle.sh` automatically, so `dist/` regenerates with every build. **`dist/` is generated — never hand-edit it; edit the four split sources and rebuild.** Users import the `dist/` file into Overleaf via *New File → From External URL* (raw GitHub URL, pinned to a release tag) and **Refresh** to pull updates; see README "Use on Overleaf".

## Repo automation & conventions (`.claude/`, `MEMORY.md`)

This repo carries a small, project-local Claude infrastructure (ported/adapted from the author's research workflow):

- **`MEMORY.md`** — durable, cross-session facts in `[LEARN:category]` format. Read it at the start of layout work; append a `[LEARN]` line when a non-obvious fact or correction is established.
- **`.claude/agents/beamer-tikz-reviewer.md`** — a harsh, read-only visual critic for theme layout geometry and TikZ. Invoke it after non-trivial `.sty` layout changes and iterate until it returns APPROVED; it writes reports to `quality_reports/reviews/`.
- **`.claude/hooks/`** — `build-reminder.py` (PostToolUse advisory: recompile the affected theme after a `.sty` edit) and `log-reminder.py` (Stop hook: nudge a session-log update after 10 responses). Wired in `.claude/settings.json`.
- **`.claude/rules/`** — `logging.md` (session logs in `quality_reports/session_logs/`, reviews in `quality_reports/reviews/`) and `tikz-visual-quality.md` (the visual bar for `.sty`/TikZ work — prefer paper-dimension-derived coordinates over hard-coded cm).
- **`templates/session-log.md`** — session-log template.

LaTeX build artifacts are git-ignored via `.gitignore` globs; the committed `*_theme_test.pdf` previews are kept on purpose. (Note: some build artifacts in the UC Davis dirs were committed before the `.gitignore` was fixed and remain tracked until untracked deliberately.)
