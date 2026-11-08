# NS-FLUID — Florida News (static site)

Plain static HTML/CSS, no build step. Repo root is the site root.

- `index.html` — front page
- `dossiers.html` — the files index
- `dossier-liu.html`, `dossier-elsayed.html` — generated from the markdown
  dossiers in ~/workspace/your_files/ by `build_dossiers.py`; rerun it after
  editing a dossier .md, never hand-edit the generated pages
- `about.html`, `404.html`
- `styles.css` — the design system (palette sampled from the badge)
- `assets/` — badge.png (Jeff's supplied mark), dossier photographs
- `CNAME` — ns-fluid.com (GitHub Pages custom domain)

Brand: ~/workspace/your_files/ns-fluid-brand/brand-sheet.md
Status: v1 built 2026-11-08 for Jeff's verdict. NOT yet pushed anywhere.
Deploy, on Jeff's go: confirm which GitHub repo serves ns-fluid.com today,
then publish these files to that repo's Pages branch. Do not delete any
existing repo content — Jeff's source-access hard line.
