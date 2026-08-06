# Website restoration and deployment contract — 2026-08-06

`docs/index.html` is the sole automatic GitHub Pages entry point. The repository Pages source is `master:/docs`; no custom Actions workflow may automatically publish a competing artifact.

## Canonical long-form payload

The following files must remain byte-identical to Git blob
`41a8d733f42da18282fa276f5d2fa82bac7516f6`:

- `docs/index.html`
- `docs/404.html`
- `docs/full-site-2026-08-06.html`
- `docs/exceptional-geometry-41a8d733.html`

`docs/index.html` was restored byte-for-byte from commit
`df5c52314bf4c8c4b0d7a1b1f0afb66d872bdfb6`, the parent immediately before
commit `413ed869b1ae82446df3583e43c3f9bcb365a18c` replaced the long-form site.

## Archived compact page

The compact source-derived landing page is preserved only at
`docs/source-derived-architecture-landing-2026-08-05.html`, with Git blob
`94e90827ec73fc20e632fba5519fed2d109846d6`. It is historical material and is
never an authorized replacement for `docs/index.html`.

## Publisher rule

- Automatic publisher: GitHub Pages branch source `master:/docs`.
- `.github/workflows/deploy-pages.yml`: manual fallback only.
- `docs/.nojekyll`: retained so the directory is published verbatim.
- A persistent `data/website_migration_authorization.json` must not exist.

This single-publisher rule prevents an old queued artifact or redirect migration
from overwriting the canonical long-form site.
