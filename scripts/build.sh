#!/usr/bin/env bash
#
# Recompile the sample/preview PDFs for the Beamer themes.
#
# The committed *_theme_test.pdf files are the deliverable previews; regenerate
# them with this after editing any .sty so the previews stay in sync. latexmk
# handles the multi-pass runs the TOC / section progress bar need.
#
# Usage:
#   scripts/build.sh                 # build all themes
#   scripts/build.sh ucdavis-xe      # UC Davis (XeLaTeX) only
#   scripts/build.sh ucdavis-pdf     # UC Davis (pdfLaTeX) only
#   scripts/build.sh caedlab         # California Education Lab only
#
# Each theme is compiled from inside its own directory because the .sty files
# and relative asset paths (e.g. ../assets/cel_logo.png) resolve relative to it.
#
# After building, the single-file deploy bundles under dist/ are regenerated
# (scripts/bundle.sh) so they stay in sync with the split .sty sources.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILED=()

# build_theme <dir> <texfile> <latexmk-engine-flag>
build_theme() {
  local dir="$1" tex="$2" engine="$3"
  echo "==> Building ${dir}/${tex}"
  if ( cd "${ROOT}/${dir}" \
        && latexmk "${engine}" -interaction=nonstopmode -halt-on-error "${tex}" >/dev/null 2>&1 \
        && latexmk -c "${tex}" >/dev/null 2>&1 ); then
    echo "    OK  -> ${dir}/${tex%.tex}.pdf"
  else
    echo "    FAILED (rerun without >/dev/null to see the log)"
    FAILED+=("${dir}/${tex}")
  fi
}

build_ucdavis_xe()  { build_theme "ucdavis_beamer_theme_xelatex"  "ucdavis_theme_test.tex" "-xelatex"; }
build_ucdavis_pdf() { build_theme "ucdavis_beamer_theme_pdflatex" "ucdavis_theme_test.tex" "-pdf"; }
build_caedlab() {  # CEL ships two decks (4:3 native + 16:9) from one shared body
  build_theme "ca_ed_lab_beamer_theme" "caedlab_theme_test.tex"     "-pdf"
  build_theme "ca_ed_lab_beamer_theme" "caedlab_theme_test_169.tex" "-pdf"
}

target="${1:-all}"
case "${target}" in
  ucdavis-xe)  build_ucdavis_xe ;;
  ucdavis-pdf) build_ucdavis_pdf ;;
  caedlab)     build_caedlab ;;
  all)         build_ucdavis_xe; build_ucdavis_pdf; build_caedlab ;;
  *)
    echo "Unknown target: ${target}" >&2
    echo "Valid targets: all | ucdavis-xe | ucdavis-pdf | caedlab" >&2
    exit 2
    ;;
esac

# Regenerate the single-file deploy bundles (dist/) from the split .sty sources.
"${ROOT}/scripts/bundle.sh"

if [ "${#FAILED[@]}" -gt 0 ]; then
  echo
  echo "Build failures: ${FAILED[*]}" >&2
  exit 1
fi
echo
echo "All requested builds succeeded."
