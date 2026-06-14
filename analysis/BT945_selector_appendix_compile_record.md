# BT945 — Selector appendix compile record

BT945 verified the BT942 selector appendix at the standalone TeX/PDF layer. Its original helper targeted `W36_PAPER.tex`; that routing is superseded by BT946/BT947.

## Runtime check

A standalone wrapper around the BT942 appendix was compiled with pdflatex in the ChatGPT runtime.

```text
pdflatex_returncode = 0
pdf_pages = 1
pdf_page_size_pt = 612 x 792
pdf_sha256 = 0f50d638832125adad50ebbb849ab91b91bec980ad869d550983afcfae7e13b9
tex_sha256 = 92c19d9bf016c8af0946f423ee0c327b065b9b5ed533859677ecc91720486e3c
```

The PDF was inspected and rendered successfully.

## Correct routing after BT946/BT947

```text
photonic_holonet.tex = current main narrative / architecture paper
w33_paper.tex       = heavy-math manuscript target
```

Use the corrected helper:

```text
tools/bt947_w33_selector_appendix_verify.py
```

It applies `tools/integrate_bt942_selector_appendix_w33.py` and then builds `w33_paper.tex` twice with pdflatex in a full local checkout.

## Boundary

The BT945 standalone appendix compile remains valid. The W36 helper path is deprecated for this context; heavy E8/SNF selector math belongs in `w33_paper.tex`.
