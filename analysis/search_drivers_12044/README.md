# Search drivers for Pass 12044 (Claude track)

## What this folder is

These scripts produced the records quoted in `analysis/w33_pass12044_s_type_cp_and_locus_stability.py`. Run each from
this folder with `py -3`. The `*.json` and `*.log` files are the committed run records.

## Driver map

| script | what it does | status |
|---|---|---|
| `g2.py` | checks that S acts on the level-3 theta as F x F / F x 1 | used |
| `upS.py` | exact up fit on the CP o (S x S) arc | used |
| `ctrlS.py`, `ctrlS2.py` | complex-down positive control at the S-arc tau (frozen solutions) | used |
| `scanTm2.py` | the S x T^-2 up home is degenerate (det Im Omega = 0) | used |
| `scan1d.py` | part (b), the S x T^0 up curve (chi^2_up = 94.6) | used |
| `cwhess.py`, `cwct.py`, `cwfull.py` | transverse Hessian of the 12034 toy potential, the counterterm scan, the (s, Q) grid | used |
| `sfit.py` | first penalty fit; it never reached the fixed set | superseded |
| `diag.py` | shows the fixed sets are reachable (residual 1e-16), so the penalty method was at fault | diagnostic |
| `downS.py` | first fixed-tau down fit; its loose doublet-Wilson condition admitted a non-symmetry (J = -3.4e-4) | superseded |
| `jointS.py`, `jointCtrl.py` | joint constrained multistart (27 branches) | not evidence: failed its own control (1230) |
| `scan1d.py`, part (a), and `scanA2.py` | Wilson-free S x S down scans | truncation artefacts (parity residual 0.41); replaced by the exact parity argument |

## Caveat

These are search drivers, not regression tests. The producer pins the statements.
