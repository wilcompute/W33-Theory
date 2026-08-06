# GitHub Pages deployment root-cause certificate — 2026-08-06

## Incident

The public project site continued to show a tiny landing page even after `docs/index.html` was restored in the repository.

## Artifact-level evidence

The managed GitHub Pages workflow run `31029182878` produced artifact `8939954954` (`github-pages`) from branch `master` at head SHA `358da7c8b379d4460ee7c70da34416a742a7f054`.

The artifact was downloaded and inspected directly. Its deployed root document was:

- path: `/index.html`
- byte count: `4064`
- Git blob SHA-1: `1e17bddc8cb6db8e3562a1a8522fc70f89c23f22`
- title: `W33 Theory`
- identifying text: `One substrate. Many exact interfaces.`

All three jobs in that managed Pages run (`build`, `deploy`, and `report-build-status`) concluded `cancelled`.

Therefore the incident was not merely browser caching and was not solved by checking the current repository blob. The actual Pages artifact contained the tiny page, and the deployment was cancelled.

## Root cause

GitHub Pages was configured in legacy branch-publishing mode, using the high-churn `master` branch and `/docs` folder. Continuous research commits repeatedly invalidated or cancelled the managed Pages run. Earlier custom `actions/deploy-pages` workflows were not authoritative while the repository remained configured for legacy branch publication.

## Source hardening

The authoritative large site has Git blob SHA-1:

`41a8d733f42da18282fa276f5d2fa82bac7516f6`

It is mirrored at all plausible publication paths:

- `master:/index.html`
- `master:/docs/index.html`
- `main:/index.html`
- `main:/docs/index.html`
- root and `/docs` immutable/fallback documents.

The tiny redirect shell is retained only as:

`docs/index-redirect-archive-2026-08-06.html`

## Deployment repair

The durable repair is to change the legacy Pages source from high-churn `master:/docs` to stable `main:/docs`, then explicitly request a Pages build. The source-switch controller and emergency issue-event controller are committed. Native merge commits were used to avoid the GitHub rule that `GITHUB_TOKEN`-generated commits do not trigger follow-on Pages builds.

## Verification rule

No future assistant may claim this incident fixed merely because a repository file has the correct blob. Success requires both:

1. the Pages settings report `main:/docs` (or an intentionally configured custom-workflow source); and
2. a cache-busted HTTP fetch of `https://wilcompute.github.io/W33-Theory/` whose complete response hashes to the authoritative large-site blob.

Until both receipts exist, status is `SOURCE_REPAIRED_DEPLOYMENT_CONTROL_PENDING`, not `FIXED`.
