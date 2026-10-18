# Search drivers for Pass 12045 (Claude track)

These scripts produced the records quoted in `analysis/w33_pass12045_geometric_barr_row.py`. Run each from this folder
with `py -3`. The `*.json`, `*.log` and `*.npy` files are the run records.

The producer imports `barrfit.py`, `jointlep.py` and `mcC.py` from here.

| script | what it does |
|---|---|
| `barrfit.py` | Fits the row in three modes: `shared` (b = theta vector on the 5bar torus, 6 parameters), `free` (tau_B free, 8 parameters) and `row` (the free row of 12005, used as a positive control). |
| `jointlep.py` | The 12007 shared matching for the charged leptons. Also a joint 8-ratio fit with narrow starts; those runs were stopped and are not used. |
| `catalog.py` | Broad-start catalogue of isolated branches, keyed by their invariants and lepton predictions. Two runs crashed on an unguarded SVD; they were guarded and rerun. The runs were stopped after at least 7 distinct branches had been found. |
| `mcC.py` | Monte Carlo through branch C with homotopy tracking. It showed that the first reading ("m_mu/m_tau within 2.4%") is not significant. |
| `sens.py` | Linear sensitivities and pulls for branches A, B and C. |
| `mapC.py` | Exact nonlinear posterior on branch C, with comparator or precise priors. Gives chi^2 = 2.8 with comparator priors and 10.8 with precise priors, at a 5% lepton theory error. |

These are search drivers, not regression tests. The producer pins the statements.
