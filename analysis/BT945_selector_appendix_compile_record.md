# BT945 — Selector appendix compile record

BT945 verifies the BT942 selector appendix at the TeX/PDF layer and commits a helper for a full W36 build in a local checkout.

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

## Repo helper

```text
tools/bt945_selector_appendix_verify.py
```

This helper applies `tools/integrate_bt942_selector_appendix.py` and then builds `W36_PAPER.tex` twice with pdflatex when run in a full local checkout.

## Boundary

The full root `W36_PAPER.tex` build was not performed inside the connector because a complete local checkout was unavailable. The appendix source itself was compiled and rendered successfully, and the full-build helper is now committed.

## Local artifact

```text
/mnt/data/w36_bt945/BT945_e8_selector_appendix_check.pdf
```
