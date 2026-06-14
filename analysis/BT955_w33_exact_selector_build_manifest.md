# BT955 — w33 exact selector build manifest

BT955 adds the full heavy-math build helper for the corrected W33 target.

## Target

```text
w33_paper.tex
```

## Included integrators

```text
tools/integrate_bt942_selector_appendix_w33.py
tools/integrate_bt952_exact_selector_w33.py
```

## Build helper

```text
tools/bt955_w33_exact_selector_build.py
```

The helper applies both integrators and then attempts a two-pass `pdflatex` build of `w33_paper.tex` in a full local checkout.

## Mathematical payload

- BT942 E8 selector status appendix.
- BT952 exact support-60 selector theorem.
- BT954 metric-preferred support-60 minimizer:

```text
[[3,68], [4,42], [38,65], [90,144]]
```

## Boundary

The connector pass committed the build helper and manifest. It did not directly overwrite `w33_paper.tex` or compile the full PDF.
