# BT947 — Route the E8 selector appendix to w33_paper.tex

Wil corrected the paper split:

```text
photonic_holonet.tex = current main narrative / architecture paper
w33_paper.tex       = heavy-math manuscript target
```

## What BT947 adds

```text
tools/bt947_w33_selector_appendix_verify.py
```

This helper applies

```text
tools/integrate_bt942_selector_appendix_w33.py
```

and then attempts a two-pass `pdflatex` build of

```text
w33_paper.tex
```

in a full local checkout.

## Boundary

The connector pass committed the w33-target helper and routing result. It did not directly overwrite `w33_paper.tex` or perform a full-root compile in the connector environment.
