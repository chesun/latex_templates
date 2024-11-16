# LaTeX Beamer Presentation Templates
## Instructions
- To start, put the following files in the same directory as your presentation
    - ```beamerthemecaedlab.sty```
    - ```beamercolorthemecaedlab.sty```
    - ```beamerinnerthemecaedlab.sty```
    - ```beamerouterthemecaedlab.sty```
- Then put the ```assets``` folder in the directory
- Modify ```beamerinnerthemecaedlab.sty``` line 75 to reflect the correct directory to the logo.
- The theme [```ucdavis_beamer_theme_xelatex```](/ucdavis_beamer_theme_xelatex) can only be compiled using XeLaTeX (recommended) or LualaLaTeX (not tested). The [```ucdavis_beamer_theme_pdflatex```](/ucdavis_beamer_theme_pdflatex) theme can be compiled using pdfLaTeX, since it does not utilize the ```fontspec``` package and uses a default serif font. 