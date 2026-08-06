# GitHub Pages deployment root-cause certificate — 2026-08-06

## Incident

The public project site continued to show a tiny landing page after `master/docs/index.html` had been restored in the repository.

## Artifact-level evidence

Managed GitHub Pages workflow run `31029182878` produced artifact `8939954954` (`github-pages`) from branch `master` at head SHA `358da7c8b379d4460ee7c70da34416a742a7f054`.

The artifact was downloaded and inspected directly. Its published root document was:

- path: `/index.html`
- byte count: `4064`
- Git blob SHA-1: `1e17bddc8cb6db8e3562a1a8522fc70f89c23f22`
- title: `W33 Theory`
- identifying text: `One substrate. Many exact interfaces.`

Its build, deploy, and report jobs concluded `cancelled`. The tiny page was therefore a real historical Pages artifact, not an invented browser rendering.

## Authoritative source

The sole authoritative public source is:

`master:/docs/index.html`

Its canonical long-form blob is:

`41a8d733f42da18282fa276f5d2fa82bac7516f6`

The file is 28,865 lines. The compact page is retained only as an archive and must never replace `master/docs/index.html`.

## Current diagnosis

Independent retrieval of the public origin now returns the long-form W(3,3) site, while the historical 4,064-byte page contains no JavaScript, service worker, redirect, or storage code. If a browser still displays that exact compact page, the remaining mechanism is stale client or intermediary cache state, or navigation to a different URL—not persistent code in the compact page.

## Cache-clean witnesses

The canonical large blob is also published at:

`master:/docs/full-site-2026-08-06.html`

A one-time cache-reset entry is published at:

`master:/docs/refresh-authoritative-site-2026-08-06.html`

The reset entry unregisters service workers, clears Cache Storage, and opens the canonical project root with a unique query key.

## Verification rule

No future assistant may claim success merely because the repository blob is correct. Verify all of the following:

1. Pages is configured for `master:/docs`.
2. `master/docs/index.html` has the canonical long-form blob or an intentionally updated long-form successor.
3. A fresh/cache-busted fetch of the public root returns the long-form page.
4. A user seeing the historical compact page tests the cache-clean mirror or reset entry before any branch/source migration is attempted.

Current status: `MASTER_DOCS_AND_ORIGIN_LONG_FORM_CONFIRMED; STALE_CLIENT_PATH_REMEDIATION_PUBLISHED`.
