# Passes 1060--1064 execution status

## Completed

All five requested workstreams are implemented on `master`.

* Exact Python checks: **37/37 PASS**.
* Focused local regression: **6 pytest tests passed in 29.39 seconds**.
* Signed-cover construction: **PASS**.
* Springer embedding decision: **PASS — code embedding**.
* Inner-48/540 classification: **PASS — `C2 x S4`**.
* Lean source and umbrella import: committed.
* Dual contextuality/C3 preregistration: **PASS**.

## Formal verification boundary

The full-build workflow was committed at
`467a77f9e54cdcd312cd1a63cbc17c598b1c3137` and requests both:

1. the exact Python certificates and focused pytest suite; and
2. a complete `lake build` of the `formal` package through `leanprover/lean-action`.

The available GitHub connector's commit-workflow endpoint returns only
pull-request-associated runs and returned an empty list for this direct push.
The combined-status endpoint also exposes no legacy status contexts. Therefore
this file does **not** claim a remotely observed Lean success or failure.

The actual formal source is nevertheless wired into `formal/W33.lean`, and the
new module imports `W33.Pass575CyclotomicDVRKernel` and references
`W33.Pass575.orderLocalCertificate`, so any successful umbrella build verifies
both the four-row obstruction theorem and the repository's actual Pass575
certificate rather than a detached proposal file.

## Authoritative artifacts

* `PASS1060_1064_FIVE_STREAM_RELEASE.md`
* `data/w33_pass1060_1064_release.json`
* `.github/workflows/pass1060_1064_exact.yml`
* `tests/test_w33_pass1060_1064.py`
