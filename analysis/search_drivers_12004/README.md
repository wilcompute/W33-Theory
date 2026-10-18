# Search drivers for Pass 12004 (Claude track)

## What this folder is

These scripts produced the frozen search record quoted in `analysis/w33_pass12004_cp_real_bare_theta_no_fit.py`. Run each
from this folder with `py -3`. Outputs (`*.json`, `*.log`) are the committed records of the runs.

## Driver map

| script | what it does |
|---|---|
| `cpfit.py`, `cpls.py`, `cplsS.py` | shared-tau multistart fits on the CP locus; `cplsS` seeds from the exact up solution; `cpls free` is the CP-free positive control |
| `downonly.py` | down sector at the up-required tau: `frozen` (CP-real), `0`/`1` (own CP-real tau'), `free` (complex positive control) |
| `deep.py` | centred-window theta evaluator (`validate` mode) and deep-cusp least squares |
| `grid.py`, `gridX.py` | earlier N=40 grids; `gridX` found the deep-cusp truncation artefact (257 -> 357) |
| `gridC.py` | the accurate full-range grid, 746,496 points; global minimum chi^2 = 329 |
| `verify.py`, `epsM.py` | intake checks: signed J and det Y_d winding; the 11940 eps_M dependence |

## Caveat

These are search drivers, not regression tests. Results can depend on library versions; the producer pins the statements.
