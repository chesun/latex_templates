# LaTeX Beamer Presentation Templates

Custom Beamer themes for UC Davis–affiliated presentations, in two brands packaged as three theme directories:

- [`ucdavis_beamer_theme_xelatex/`](/ucdavis_beamer_theme_xelatex) — UC Davis theme, **XeLaTeX/LuaLaTeX** (font: Helvetica Neue via `fontspec`).
- [`ucdavis_beamer_theme_pdflatex/`](/ucdavis_beamer_theme_pdflatex) — the same UC Davis theme, **pdfLaTeX** (font: Helvetica via the `helvet` package). The only substantive difference from the XeLaTeX variant is the font setup.
- [`ca_ed_lab_beamer_theme/`](/ca_ed_lab_beamer_theme) — California Education Lab theme, a faithful port of the official CEL PowerPoint template. **pdfLaTeX** (font: Carlito, the free Calibri-metric clone). Navy + gold brand, with a table of contents and automatic section dividers.

## Use on Overleaf (recommended)

Each theme is also published as a **single bundled `.sty`** under [`dist/`](/dist), so you don't have to copy four files. In an Overleaf project:

1. **New File → From External URL**, and paste the raw URL for your theme. Pin it to a release tag (e.g. `v1`) so in-progress commits never break a live deck:
    - UC Davis (XeLaTeX): `https://raw.githubusercontent.com/chesun/latex_templates/v1/dist/ucdavis-xelatex/beamerthemeucdavis.sty`
    - UC Davis (pdfLaTeX): `https://raw.githubusercontent.com/chesun/latex_templates/v1/dist/ucdavis-pdflatex/beamerthemeucdavis.sty`
    - California Education Lab: `https://raw.githubusercontent.com/chesun/latex_templates/v1/dist/caedlab/beamerthemecaedlab.sty`
2. For the **CEL theme only**, add its logo the same way (the bundled theme expects `cel_logo.png` next to the `.sty`, i.e. at the project root):
    - `https://raw.githubusercontent.com/chesun/latex_templates/v1/dist/caedlab/cel_logo.png`
3. In your preamble use `\usetheme{ucdavis}` (UC Davis) or `\usetheme{caedlab}` (CEL), and set the compiler in **Menu → Compiler** — XeLaTeX for the UC Davis XeLaTeX theme, pdfLaTeX for the other two.

**To pull updates:** click the imported file in Overleaf and hit **Refresh** — it re-downloads the latest from the URL. Updates are opt-in and per-project; nothing changes until you Refresh.

The bundled file is generated from the four split `.sty` sources by `scripts/bundle.sh` (run automatically by `scripts/build.sh`) — edit the sources, never `dist/`.

## Using a theme manually (local compiles)

If you compile locally instead, you can use the same single bundle from `dist/` (one file; for CEL, also drop `dist/caedlab/cel_logo.png` next to it). Or copy the four split source files:

1. Copy the four `.sty` files of the theme into your presentation's directory:
    - `beamertheme<name>.sty`
    - `beamercolortheme<name>.sty`
    - `beamerinnertheme<name>.sty`
    - `beameroutertheme<name>.sty`

    (`<name>` is `ucdavis` for either UC Davis variant, `caedlab` for the CEL theme. The two UC Davis variants share the name `ucdavis`, so use only one at a time.)
2. For the split CEL theme, also copy the `assets/` folder (it references `../assets/cel_logo.png`). The UC Davis themes need no image assets. (The `dist/` bundles avoid this — the CEL bundle references a bare `cel_logo.png` instead.)
3. Load the theme in your preamble with `\usetheme{<name>}`.
4. Compile with the right engine: `xelatex` for the UC Davis XeLaTeX theme, `pdflatex` for the UC Davis pdfLaTeX theme and the CEL theme. Run it **twice** if your deck has a table of contents.

## California Education Lab theme

The CEL theme works at the template's **native 4:3 and at 16:9 from the same source** — only the `aspectratio` option changes, and the layout adapts automatically:

- 4:3 (CEL native): `\documentclass[aspectratio=43]{beamer}`
- 16:9 (widescreen): `\documentclass[aspectratio=169]{beamer}`

The CEL logo (`assets/cel_logo.png`) is bundled and placed automatically on the title slide — no per-presentation path edits. Set your funding note with `\renewcommand{\acknowledgement}{...}`; it defaults to the official CEL placeholder.

## Building the previews

Each theme ships a compiled `*_theme_test.pdf` as its reference preview. Regenerate them with the build script (compiles each sample with the correct engine, runs the needed passes, and cleans aux files):

```bash
scripts/build.sh            # all three themes (CEL builds both 4:3 and 16:9)
scripts/build.sh ucdavis-xe # UC Davis (XeLaTeX) only
scripts/build.sh ucdavis-pdf # UC Davis (pdfLaTeX) only
scripts/build.sh caedlab    # California Education Lab only
```

## Compiled previews

- [UC Davis — XeLaTeX](ucdavis_beamer_theme_xelatex/ucdavis_theme_test.pdf)
- [UC Davis — pdfLaTeX](ucdavis_beamer_theme_pdflatex/ucdavis_theme_test.pdf)
- [California Education Lab — 4:3](ca_ed_lab_beamer_theme/caedlab_theme_test.pdf)
- [California Education Lab — 16:9](ca_ed_lab_beamer_theme/caedlab_theme_test_169.pdf)

These templates are unofficial and not affiliated with or endorsed by UC Davis; the CEL theme is a LaTeX port of the lab's own PowerPoint template.
