# BT1222 -- BT1218 TeX Integration Helper

## Purpose

BT1218 created the paper-ready experimental-readiness section. BT1222 adds an idempotent integration helper so the section can be inserted into `photonic_holonet.tex` without a risky direct large-file replacement.

## Helper

```text
tools/integrate_bt1218_holonet_experimental_readiness.py
```

Run from repo root:

```bash
python tools/integrate_bt1218_holonet_experimental_readiness.py --dry-run
python tools/integrate_bt1218_holonet_experimental_readiness.py
```

The inserted line is:

```tex
\input{paper/sections/sec_bt1218_holonet_experimental_readiness}
```

## Markers

The helper tries to insert before the first available marker:

1. `\subsection{The fault-tolerant layer is the substrate's lattice tower}`
2. `\subsection{Why the primitive is one \emph{massless} photon}`
3. `\section{Experimental roadmap}`

## Boundary

The helper has been pushed but not applied directly by connector-side large-file replacement. This is deliberate: it avoids accidental truncation or collision in the main paper source.
