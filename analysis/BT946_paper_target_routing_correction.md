# BT946 — Paper target routing correction

Routing correction from Wil:

```text
photonic_holonet.tex = current main narrative / architecture paper
w33_paper.tex       = heavy-math manuscript target
```

## What was wrong

The BT942 helper originally targeted `W36_PAPER.tex`. That was the wrong target for this context.

## Corrected target

The E8/SNF/symplectic-selector appendix belongs in `w33_paper.tex`.

## New integrator

```text
tools/integrate_bt942_selector_appendix_w33.py
```

It idempotently inserts:

```text
paper/BT942_e8_selector_appendix.tex
```

before `\end{document}` in `w33_paper.tex`.

## Boundary

The connector pass added the correct integrator and routing record. It did not directly overwrite `w33_paper.tex`; run the integrator in a full checkout to patch the source.
