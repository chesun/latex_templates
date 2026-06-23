# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Custom, unofficial LaTeX Beamer themes for UC Davis-affiliated presentations. There are two brands, packaged as three theme directories:

- `ucdavis_beamer_theme_xelatex/` — UC Davis theme, **XeLaTeX/LuaLaTeX only** (uses `fontspec`, main font Verdana).
- `ucdavis_beamer_theme_pdflatex/` — the same UC Davis theme, **pdfLaTeX-compatible** (no `fontspec`, default serif font). The *only* substantive difference from the xelatex variant is the font setup.
- `ca_ed_lab_beamer_theme/` — California Education Lab theme, **XeLaTeX only** (`fontspec`, main font Helvetica). Simpler than the UC Davis theme: no table of contents styling, no section progress bar.

`assets/` holds logos/wordmarks (official UC Davis brand files under `assets/ucdavis_wordmarks/`, plus `ca_ed_lab.png` and `expanded_logo_gold-blue.png`). `resources/` holds a Beamer cheat sheet PDF.

## Theme architecture

Each theme follows Beamer's standard four-file split. `\usetheme{<name>}` loads `beamertheme<name>.sty`, which loads the other three:

- `beamertheme<name>.sty` — **master file.** `\useinnertheme` / `\useoutertheme` / `\usecolortheme`, font setup, itemize markers, blocks style. For the UC Davis theme it *also* defines the TOC styling (gold-numbered circles + rules), the TikZ section **progress bar** (`\sectionprogressbar`), and an `\AtBeginSection` hook that auto-generates a section-title slide.
- `beamercolortheme<name>.sty` — color definitions and structural colors.
- `beamerinnertheme<name>.sty` — the slide **background** (the blue/gold bands) and the **title page** template.
- `beameroutertheme<name>.sty` — the **frametitle** template (title text + frame number, positioned with TikZ).

Internal theme name: both UC Davis variants use the name `ucdavis` (so `beamerthemeucdavis.sty` exists in both the xelatex and pdflatex dirs — you cannot have both on the TeX path at once; you copy the variant you want into your presentation). The CA Ed Lab theme is named `caedlab`.

### Cross-cutting facts worth knowing before editing

- **Colors are shared and the names are UC-Davis-flavored everywhere.** Both themes define `ucdavisBlue` (`cmyk 1,0.56,0,0.34`) and `ucdavisGold` (`RGB 255,191,0`). The CA Ed Lab color theme reuses these same `ucdavis*` color names despite being a different brand — renaming them requires touching all four caedlab files.
- **`\emph` and `\textbf` are redefined as color commands** in the UC Davis color theme: `\emph` → blue, `\textbf` → gold. This is surprising; bold text is not black. The CA Ed Lab theme does not do this.
- The CA Ed Lab title page expects a user-defined `\acknowledgement` macro and `\includegraphics` of `../assets/ca_ed_lab.png` (relative path). When copying the theme into a real presentation, the logo path must be updated (README points at "line 75" of the inner theme).

### The hard-coded-spacing problem (primary improvement target)

The layout is positioned with **absolute, hand-tuned coordinates**, which is why multi-line titles and non-16:9 aspect ratios break it. Concretely:

- **Backgrounds** (inner themes) draw the blue/gold bands at fixed TikZ y-coordinates — e.g. UC Davis xelatex uses `2.5` (footer band) and `7.55`/`7.65` (header band); CA Ed Lab uses `2`/`1.85` and `7.35`/`7.5`. These numbers assume `aspectratio=169` at Beamer's default paper height; changing the aspect ratio misaligns every slide.
- **Frametitles** (outer themes) place the title text and frame number at absolute coordinates (e.g. `(0.4,1.1)`, frame number at `(15.3,1.75)`). A long/multi-line frame title overflows the band rather than reflowing.
- **Title pages** (inner themes) stack `beamercolorbox`es separated by hard `\vskip1.5cm` / `\vskip0.7cm` etc., with the title forced to `\LARGE` regardless of length — a two-line title pushes content out of place.

When making layout "automatic," prefer deriving from `\paperheight`/`\paperwidth`/`\textheight` and Beamer length registers over absolute centimeters, and let boxes size to content instead of fixed `ht=`/`\vskip`.

## Building / previewing

Use the build script — it compiles each sample `*_theme_test.tex` with the right engine, runs the multi-pass `latexmk` needs, and cleans aux files:

```bash
scripts/build.sh            # all three themes
scripts/build.sh ucdavis-xe # UC Davis (XeLaTeX) only
scripts/build.sh ucdavis-pdf # UC Davis (pdfLaTeX) only
scripts/build.sh caedlab    # California Education Lab only
```

To compile by hand instead, do it **from within the theme directory** (the `.sty` files and relative asset paths like `../assets/ca_ed_lab.png` resolve relative to it): `xelatex ucdavis_theme_test.tex` (xelatex + caedlab themes) or `pdflatex ucdavis_theme_test.tex` (pdflatex theme). Run the engine **twice** when the document has a TOC or the section progress bar — the bar reads `\insertframenumber/\inserttotalframenumber` and section counts (`totcount`), correct only on the second pass.

Each test file is the canonical smoke test and reference for what the theme should look like; the compiled `*_theme_test.pdf` is **committed and is the deliverable preview**. After a layout change, recompile the affected sample, eyeball the PDF, and commit the regenerated PDF alongside the `.sty` change (matches the "recompile samples" / "update template pdf" history). The `build-reminder` hook nudges this after a `.sty` edit.

## Repo automation & conventions (`.claude/`, `MEMORY.md`)

This repo carries a small, project-local Claude infrastructure (ported/adapted from the author's research workflow):

- **`MEMORY.md`** — durable, cross-session facts in `[LEARN:category]` format. Read it at the start of layout work; append a `[LEARN]` line when a non-obvious fact or correction is established.
- **`.claude/agents/beamer-tikz-reviewer.md`** — a harsh, read-only visual critic for theme layout geometry and TikZ. Invoke it after non-trivial `.sty` layout changes and iterate until it returns APPROVED; it writes reports to `quality_reports/reviews/`.
- **`.claude/hooks/`** — `build-reminder.py` (PostToolUse advisory: recompile the affected theme after a `.sty` edit) and `log-reminder.py` (Stop hook: nudge a session-log update after 10 responses). Wired in `.claude/settings.json`.
- **`.claude/rules/`** — `logging.md` (session logs in `quality_reports/session_logs/`, reviews in `quality_reports/reviews/`) and `tikz-visual-quality.md` (the visual bar for `.sty`/TikZ work — prefer paper-dimension-derived coordinates over hard-coded cm).
- **`templates/session-log.md`** — session-log template.

LaTeX build artifacts are git-ignored via `.gitignore` globs; the committed `*_theme_test.pdf` previews are kept on purpose. (Note: some build artifacts in the UC Davis dirs were committed before the `.gitignore` was fixed and remain tracked until untracked deliberately.)
