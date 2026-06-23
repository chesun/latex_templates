# Project Memory

Corrections and learned facts that persist across sessions for the UC Davis /
California Education Lab Beamer themes. When a mistake is corrected or a durable
fact is established, append a `[LEARN:category]` entry below (most recent at bottom).

See `CLAUDE.md` for architecture and `.claude/rules/` for working rules.

---

<!-- Append new entries below. Most recent at bottom. -->

## Architecture

[LEARN:architecture] Three theme dirs, two brands: `ucdavis_beamer_theme_xelatex` (XeLaTeX, Verdana) and `ucdavis_beamer_theme_pdflatex` (pdfLaTeX, default serif) are the SAME theme named `ucdavis` — only the font setup differs. `ca_ed_lab_beamer_theme` is theme `caedlab` (XeLaTeX, Helvetica) and is simpler (no TOC styling, no progress bar).

[LEARN:architecture] Both UC Davis variants name their master file `beamerthemeucdavis.sty`, so only one can be on the TeX path at a time — you copy the variant you want into your presentation dir.

[LEARN:architecture] Standard Beamer 4-file split per theme: master (`beamertheme*`) loads inner/outer/color and defines fonts + (UC Davis only) TOC styling, the `\sectionprogressbar`, and an `\AtBeginSection` auto section-title slide. Inner = background bands + title page. Outer = frametitle. Color = palette + structural colors.

## Gotchas

[LEARN:gotcha] The UC Davis color theme redefines `\emph` -> ucdavisBlue and `\textbf` -> ucdavisGold. Bold text is NOT black. The CA Ed Lab theme does not do this.

[LEARN:gotcha] Colors `ucdavisBlue` (cmyk 1,0.56,0,0.34) and `ucdavisGold` (RGB 255,191,0) are defined in BOTH themes, and the CA Ed Lab color theme reuses these `ucdavis*` names despite being a different brand — renaming requires touching all four caedlab files.

[LEARN:gotcha] Layout is positioned with absolute, hand-tuned coordinates assuming `aspectratio=169`: background bands at fixed TikZ y-coords (UC Davis xe: 2.5 footer, 7.55/7.65 header; caedlab: 2/1.85 and 7.35/7.5), frametitle text/number at absolute coords, and title pages stacked with hard `\vskip`s + a forced `\LARGE` title. This is why multi-line titles and non-16:9 break — the primary improvement target. Derive from `\paperwidth`/`\paperheight` instead.

## Build

[LEARN:build] Compile each sample from INSIDE its theme dir (`.sty` and relative assets like `../assets/ca_ed_lab.png` resolve relative to it). Use `scripts/build.sh [all|ucdavis-xe|ucdavis-pdf|caedlab]` (latexmk, handles multi-pass). Documents with a TOC / progress bar need two passes (the bar reads `\insertframenumber/\inserttotalframenumber` + `totcount`).

[LEARN:build] The committed `*_theme_test.pdf` files ARE the deliverable previews; regenerate and eyeball them after any `.sty` change (the `build-reminder.py` hook nudges this; matches the "recompile samples" commit history).

## Project Direction

[LEARN:decision] Agreed plan (2026-06): the spacing/visual work is a FRESH MODERN REDESIGN (not incremental patching) that ALSO makes spacing automatic — band positions, frame titles, and title pages derived from `\paperwidth`/`\paperheight`/content rather than hard-coded cm, so multi-line titles and non-16:9 stop breaking. Propose 2–3 design directions before implementing. Infrastructure (build script, beamer-tikz-reviewer agent, MEMORY, logging + build hooks) was set up first and is done.

[LEARN:gotcha] `.gitignore` originally had non-glob patterns (`.aux` not `*.aux`) that ignored nothing, so build artifacts (.aux/.log/.nav/.toc/...) got committed in the two ucdavis dirs. `.gitignore` is now fixed with globs; the already-tracked artifacts were untracked with `git rm --cached` (staged, not yet committed).

[LEARN:gotcha] In band templates, draw a gold rule inside an `\hbox` (`\hbox{\color{ucdavisGold}\rule{\paperwidth}{\udaccent}}`), NOT as a bare `\rule` in vertical mode — a bare `\rule` enters horizontal mode, so a following `\nointerlineskip` throws `! You can't use \prevdepth in horizontal mode.`

[LEARN:gotcha] (General beamer lesson, even though we ended up removing the footer.) Do NOT guard a beamer footline/headline template with `\ifnum\thepage=...` / `\insertframenumber`: it's measured during head/foot height calculation when that counter can make it evaluate empty, so beamer reserves ZERO height and the footer overflows off the bottom (looks "squished"). Keep footlines unconditional (infolines pattern: `\hbox` rows + trailing `\vskip0pt`).

[LEARN:gotcha] Content that must land in the title-slide gold strip (date, conference, a logo) must be drawn by the BACKGROUND template as a tikz `\node` pinned at `(0.5\paperwidth,0.5\udgoldblock)` — the title-page frame body does NOT reliably reach into the strip, so body-flowed content ends up in the blue field (blue-on-blue = invisible).

[LEARN:design] Subtitles were REMOVED entirely (user never uses them) — `\framesubtitle` is ignored; the framesubtitle font/color defs and the strut subtitle line were deleted. Frame-title font bumped to `\LARGE` bold (was `\Large`). The header band sizes to the title (one line normally; grows for multi-line). Dropping the subtitle line made the band net thinner, so `\udtitlepad` was raised 0.45em -> 1.35em to restore the prior band thickness (~20.8% of slide height at 16:9; verified by measuring the gold-accent row). [supersedes the old uniform-height-via-strut approach]

[LEARN:design] Frame content uses beamer's DEFAULT vertical centering (do NOT set `\beamer@centeredfalse` — that was tried and reverted). The user wants: sparse content centered with whitespace top+bottom; heavy content expands to reach the top (just under the header band) and bottom edges. Verified both cases render correctly with default centering — no fixed gap blocks heavy content from reaching the edges.

[LEARN:design] Date/conference on the gold strip stay BLUE — white-on-gold is washed out (rendered both, confirmed). Carry into the pdfLaTeX + CA Ed Lab ports.

[LEARN:design] TOC + section dividers redesigned for sleekness (user disliked the originals). TOC (`section in toc`): gold numbered circle + blue title, generous `\vskip1.2ex` spacing, NO full-width rules (the rules read as dated); subsections muted `ucdavisBlue!55`, indented. Section dividers (`\AtBeginSection`): FULL-BLEED Aggie-blue slide — gold "SECTION N" eyebrow above a large white `\huge` bold title, left-aligned and vertically centered. NO gold rule and NO progress bar (user found the bar confusing — it read like a stray rule and clashed with the frame-title gold accent). The `\sectionprogressbar` macro + `totalsections` counter are now unused dead code (left in place, harmless). Carry into the ports.

## Redesign progress

[LEARN:decision] UC Davis XeLaTeX redesign DONE + refined per user feedback, visually verified at 16:9 + 4:3 with 1-/2-/3-line titles. Final design: title slide = blue field (centered title + short gold rule + author + institute) with date + conference drawn in the bottom gold strip (blue on gold, via background node — NO logo); content slides = content-sized blue frametitle band with a 2.5pt gold accent band below, the frame number in the band's top-right (NO footer), no subtitles, frame title `\LARGE` bold white sizing the band. Block body softened to `ucdavisBlue!8` on white. Title frames are normal (NOT `[plain]`; the earlier footer that needed plain was removed). Layout params at top of `beamerthemeucdavis.sty`: `\udmargin`, `\udaccent`(2.5pt), `\udtitlepad`, `\udgoldblock`(0.22). NEXT: port to pdfLaTeX (font via `helvet`) and CA Ed Lab.
