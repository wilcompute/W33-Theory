# BT958 — Final selector stack build and Holonet pointer

BT958 wires the final BT957 selector theorem into the corrected paper stack.

## w33 heavy-math stack

```text
tools/integrate_bt942_selector_appendix_w33.py
tools/integrate_bt952_exact_selector_w33.py
tools/integrate_bt957_final_selector_w33.py
```

## Holonet narrative stack

```text
tools/integrate_bt949_holonet_w33_crossref.py
tools/integrate_bt958_holonet_final_selector_pointer.py
```

## Build helper

```text
tools/bt958_final_selector_stack_build.py
```

It applies the w33 and Holonet integrators and then attempts two-pass pdflatex builds of both `w33_paper.tex` and `photonic_holonet.tex` in a full checkout.

## Final selector

```text
[(3,68),(4,42),(38,65),(90,144)]
```

Support minimum is 60, and vertex E8 plus tetracode E8 metrics both select this minimizer.

## Boundary

The connector pass committed helper and pointer files. It did not directly overwrite root paper sources or compile the final PDFs.
