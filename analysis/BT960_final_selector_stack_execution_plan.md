# BT960 — Final selector stack execution plan

BT960 adds the production wrapper that applies every corrected final-selector paper patch and builds both papers in a full checkout.

## Execution wrapper

```text
tools/bt960_execute_final_selector_stack.py
```

## Integrators

```text
tools/integrate_bt942_selector_appendix_w33.py
tools/integrate_bt952_exact_selector_w33.py
tools/integrate_bt957_final_selector_w33.py
tools/integrate_bt949_holonet_w33_crossref.py
tools/integrate_bt958_holonet_final_selector_pointer.py
```

## Papers

```text
w33_paper.tex
photonic_holonet.tex
```

## Expected outputs in a full checkout

```text
w33_paper.pdf
photonic_holonet.pdf
data/bt960_final_selector_stack_execution_manifest.json
```

## Boundary

The connector pass commits the production execution wrapper and execution plan. It does not mutate the root paper sources or compile final PDFs in this connector environment.
