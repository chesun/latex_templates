# Project Memory

Corrections and learned facts that persist across sessions for the UC Davis /
California Education Lab Beamer themes. When a mistake is corrected or a durable
fact is established, append a `[LEARN:category]` entry below (most recent at bottom).

See `CLAUDE.md` for architecture and `.claude/rules/` for working rules.

---

<!-- Append new entries below. Most recent at bottom. -->

## CA Education Lab theme (official port)

[LEARN:project] The unofficial CA Ed Lab theme was SCRAPPED and replaced with a port of the OFFICIAL CEL PowerPoint template (Box: California Education Lab - Full Team Access/Presentations & Publications/Templates/CEL Presentation PPT Template.pptx; native 4:3). New `ca_ed_lab_beamer_theme` (theme name `caedlab`): pdfLaTeX + Carlito (free Calibri metric-clone via `\usepackage{carlito}` — no system fonts/XeLaTeX needed; Calibri/Carlito are NOT findable by fontspec name on this Mac, but the carlito LaTeX package works). Brand colors `celNavy` #014B84 + `celGold` #DFB305 (defined in the master). All spacing paper-size-derived (named lengths `\celmargin`, `\celstrip`, `\celaccent`, `\celtitlerule`, `\celborderinset`) -> modular across 4:3 (native) and 16:9 (verified both). Title slide = navy field with a white bottom strip (`\celstrip` 0.22\paperheight) holding the official logo (`assets/cel_logo.png`, extracted from pptx media), a thick gold boundary rule (`\celtitlerule` 4pt), centered white title + bold presenter + italic affiliation, and a centered small-italic `\acknowledgement` note (minipage width derived from `\textwidth`, NOT `\paperwidth` — paperwidth overflows the body column and pushes it right, worst in 4:3). Content slides = navy header band + white title + slide number top-right; full-width gold rule under the band (`celaccentbar` beamercolorbox, the CEL cxnSp connector); white body. TOC = GOLD numbered circles with WHITE numerals + navy titles, no rules. Section divider (`\AtBeginSection`): solid navy slide with FOUR gold rules that each span the full width/height inset by `\celborderinset`, so they cross at the corners and reach the slide edges (matches pptx slide 4); centered white title, title-cased via `titlecaps` `\titlecap` — requires intercepting `\section` with `\RenewDocumentCommand{s o m}` into `\celcursection` because `\insertsection` expands to a `\hyperlink` wrapper that titlecaps can't process. Final "Thank you!" slide (pptx slide5): `[t]`-top-aligned, partners grouped by organization (org name `\large\color{celNavy}` heading, member names normal black beneath, blank line between groups), funding note at bottom. Test decks: shared body `caedlab_theme_content.tex` + wrappers `caedlab_theme_test.tex` (4:3) / `caedlab_theme_test_169.tex` (16:9); `build.sh caedlab` builds both; deck includes an instructions slide on the aspectratio toggle. Old `assets/ca_ed_lab.png` now unused (legacy). README + CLAUDE.md updated for the new caedlab.

## Architecture

[LEARN:architecture] Three theme dirs, two brands: `ucdavis_beamer_theme_xelatex` (XeLaTeX, Helvetica Neue via fontspec) and `ucdavis_beamer_theme_pdflatex` (pdfLaTeX, Helvetica via `helvet`) are the SAME theme named `ucdavis` — only the master's font block differs; the other three `.sty` (color/inner/outer) are byte-identical between the two. `ca_ed_lab_beamer_theme` is theme `caedlab` (pdfLaTeX, Carlito) — a port of the official CEL pptx; it HAS TOC styling + an `\AtBeginSection` section divider but NO progress bar. [updated: caedlab was formerly XeLaTeX/Helvetica and simpler; both ucdavis variants were formerly Verdana/serif]

[LEARN:architecture] Both UC Davis variants name their master file `beamerthemeucdavis.sty`, so only one can be on the TeX path at a time — you copy the variant you want into your presentation dir.

[LEARN:architecture] Standard Beamer 4-file split per theme: master (`beamertheme*`) loads inner/outer/color and defines fonts. UC Davis master adds TOC styling, the `\sectionprogressbar`, and an `\AtBeginSection` auto section-title slide; caedlab master adds TOC styling + an `\AtBeginSection` section divider (no progress bar) + the `\section` interception for title-casing. Inner = background bands + title page. Outer = frametitle. Color = palette + structural colors.

## Gotchas

[LEARN:gotcha] The UC Davis color theme redefines `\emph` -> ucdavisBlue and `\textbf` -> ucdavisGold. Bold text is NOT black. The CA Ed Lab theme does not do this.

[LEARN:gotcha] The UC Davis themes define `ucdavisBlue` (cmyk 1,0.56,0,0.34) and `ucdavisGold` (RGB 255,191,0). The caedlab theme now owns its own `celNavy` (#014B84) + `celGold` (#DFB305), defined in its MASTER file (not the color theme) — it no longer reuses the `ucdavis*` names. [updated: the OLD caedlab reused `ucdavis*`]

[LEARN:gotcha] The old hard-coded absolute-coordinate layout (bands at fixed TikZ y-coords assuming `aspectratio=169`, absolute frametitle/number coords, hard `\vskip`s + forced `\LARGE` title) is now FIXED in ALL THREE themes — `ucdavis_beamer_theme_xelatex` (redesigned), `ucdavis_beamer_theme_pdflatex` (xelatex redesign ported down verbatim; only the master font block differs), and `ca_ed_lab_beamer_theme` (ported from the CEL pptx). All are fully paper-size-derived and verified at 16:9 + 4:3. To keep the two UC Davis variants in sync, make any layout change in BOTH (the color/inner/outer `.sty` are byte-identical; only the master's font setup may differ).

## Build

[LEARN:build] Compile each sample from INSIDE its theme dir (`.sty` and relative assets like `../assets/cel_logo.png` resolve relative to it). Use `scripts/build.sh [all|ucdavis-xe|ucdavis-pdf|caedlab]` (latexmk, handles multi-pass); `caedlab` builds BOTH decks (`caedlab_theme_test.tex` 4:3 + `caedlab_theme_test_169.tex` 16:9). Documents with a TOC / progress bar need two passes (the bar reads `\insertframenumber/\inserttotalframenumber` + `totcount`).

[LEARN:build] The committed `*_theme_test.pdf` files ARE the deliverable previews; regenerate and eyeball them after any `.sty` change (the `build-reminder.py` hook nudges this; matches the "recompile samples" commit history).

[LEARN:build] DEPLOYMENT: each theme is also bundled to a single-file `dist/<theme>/beamertheme<name>.sty` by `scripts/bundle.sh` (auto-run by `build.sh`) for Overleaf import via *New File -> From External URL* + Refresh. `dist/` is GENERATED — never hand-edit; edit the four split sources and rebuild. CEL bundle references a bare `cel_logo.png` (path rewritten from `../assets/`) and ships the PNG alongside. Publish model: `main` = working branch; **`release` branch** = what Overleaf URLs point at (always known-good). Publish an update with `git push origin main:release`. Tags (`v1`, `v2`…) are immutable snapshots for *freezing* a specific deck (that deck's URL uses the tag instead of `release`). KEY: a commit to `main` is NOT live to imported decks until pushed to `release`.

## Project Direction

[LEARN:decision] Agreed plan (2026-06): the spacing/visual work is a FRESH MODERN REDESIGN (not incremental patching) that ALSO makes spacing automatic — band positions, frame titles, and title pages derived from `\paperwidth`/`\paperheight`/content rather than hard-coded cm, so multi-line titles and non-16:9 stop breaking. Propose 2–3 design directions before implementing. Infrastructure (build script, beamer-tikz-reviewer agent, MEMORY, logging + build hooks) was set up first and is done.

[LEARN:gotcha] `.gitignore` originally had non-glob patterns (`.aux` not `*.aux`) that ignored nothing, so build artifacts (.aux/.log/.nav/.toc/...) got committed in the two ucdavis dirs. `.gitignore` is now fixed with globs; the already-tracked artifacts were untracked with `git rm --cached` (staged, not yet committed).

[LEARN:gotcha] In band templates, draw a gold rule inside an `\hbox` (`\hbox{\color{ucdavisGold}\rule{\paperwidth}{\udaccent}}`), NOT as a bare `\rule` in vertical mode — a bare `\rule` enters horizontal mode, so a following `\nointerlineskip` throws `! You can't use \prevdepth in horizontal mode.`

[LEARN:gotcha] (General beamer lesson, even though we ended up removing the footer.) Do NOT guard a beamer footline/headline template with `\ifnum\thepage=...` / `\insertframenumber`: it's measured during head/foot height calculation when that counter can make it evaluate empty, so beamer reserves ZERO height and the footer overflows off the bottom (looks "squished"). Keep footlines unconditional (infolines pattern: `\hbox` rows + trailing `\vskip0pt`).

[LEARN:gotcha] Content that must land in the title-slide gold strip (date, conference, a logo) must be drawn by the BACKGROUND template as a tikz `\node` pinned at `(0.5\paperwidth,0.5\udgoldblock)` — the title-page frame body does NOT reliably reach into the strip, so body-flowed content ends up in the blue field (blue-on-blue = invisible).

[LEARN:design] Subtitles were REMOVED entirely (user never uses them) — `\framesubtitle` is ignored; the framesubtitle font/color defs and the strut subtitle line were deleted. Frame-title font bumped to `\LARGE` bold (was `\Large`). The header band sizes to the title (one line normally; grows for multi-line). Dropping the subtitle line made the band net thinner, so `\udtitlepad` was raised 0.45em -> 1.35em to restore the prior band thickness. [supersedes the old uniform-height-via-strut approach] **UPDATE 2026-06-23:** per user request, all three themes got a thinner band + bigger title — `\udtitlepad` 1.35em -> 0.9em and frametitle `\LARGE` -> `\huge` (both ucdavis variants, kept in sync); caedlab `\celtitlepad` 1.5em -> 1.0em and frametitle `\LARGE` -> `\huge`. Band is content-sized so it still grows for multi-line titles (verified a 3-line title: band grows, gold rule stays attached, no collision with the frame number).

[LEARN:design] Frame content uses beamer's DEFAULT vertical centering (do NOT set `\beamer@centeredfalse` — that was tried and reverted). The user wants: sparse content centered with whitespace top+bottom; heavy content expands to reach the top (just under the header band) and bottom edges. Verified both cases render correctly with default centering — no fixed gap blocks heavy content from reaching the edges.

[LEARN:design] Date/conference on the gold strip stay BLUE — white-on-gold is washed out (rendered both, confirmed). Carry into the pdfLaTeX + CA Ed Lab ports.

[LEARN:design] TOC + section dividers redesigned for sleekness (user disliked the originals). TOC (`section in toc`): gold numbered circle + blue title, generous `\vskip1.2ex` spacing, NO full-width rules (the rules read as dated); subsections muted `ucdavisBlue!55`, indented. Section dividers (`\AtBeginSection`): FULL-BLEED Aggie-blue slide — gold "SECTION N" eyebrow above a large white `\huge` bold title, left-aligned and vertically centered. NO gold rule and NO progress bar (user found the bar confusing — it read like a stray rule and clashed with the frame-title gold accent). The `\sectionprogressbar` macro + `totalsections` counter are now unused dead code (left in place, harmless). Carry into the ports.

## Redesign progress

[LEARN:decision] UC Davis XeLaTeX redesign DONE + refined per user feedback, visually verified at 16:9 + 4:3 with 1-/2-/3-line titles. Final design: title slide = blue field (centered title + short gold rule + author + institute) with date + conference drawn in the bottom gold strip (blue on gold, via background node — NO logo); content slides = content-sized blue frametitle band with a 2.5pt gold accent band below, the frame number in the band's top-right (NO footer), no subtitles, frame title `\LARGE` bold white sizing the band. Block body softened to `ucdavisBlue!8` on white. Title frames are normal (NOT `[plain]`; the earlier footer that needed plain was removed). Layout params at top of `beamerthemeucdavis.sty`: `\udmargin`, `\udaccent`(2.5pt), `\udtitlepad`, `\udgoldblock`(0.22). NEXT: port to pdfLaTeX (font via `helvet`) and CA Ed Lab.

[LEARN:decision] CA Ed Lab redesign DONE (see the CA Education Lab theme entry near the top of this file) — it was reworked as a from-scratch port of the official CEL pptx rather than a UC Davis re-skin.

[LEARN:decision] ALL THREE themes are now redesigned/ported and dimension-derived (no remaining hard-coded targets). `ucdavis_beamer_theme_pdflatex` received the xelatex redesign verbatim: color/inner/outer `.sty` copied byte-for-byte, master copied with the font block swapped (`fontspec` + `\setmainfont{Helvetica Neue}` -> `\RequirePackage[T1]{fontenc}` + `\RequirePackage[scaled=0.92]{helvet}`, keeping `\usefonttheme{professionalfonts}` + `\renewcommand{\familydefault}{\sfdefault}`), and the test deck mirrored from xelatex. Verified at 16:9 + 4:3 (the longer 4:3 title reflows to two lines and re-centers cleanly). helvet ≈ Helvetica Neue — visually near-indistinguishable.
