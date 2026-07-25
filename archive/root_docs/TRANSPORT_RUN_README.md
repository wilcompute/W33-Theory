Transport solver farm — run instructions
=====================================

Overview
--------

This repository contains symmetry-reduced CSP tooling for the transport/holonomy
frontier. The heavy search must be executed locally (or on a cluster) inside
the project's virtualenv. The workflow is:

1. Export CNF(s) or run OR-Tools CP-SAT locally for chosen seeds.
2. If a candidate assignment is found, verify it with the repo bridges.
3. If no solution, escalate to stronger solvers or controlled symmetry breaking.

Quick local steps (Windows / PowerShell)
---------------------------------------

Activate venv (example):

```powershell
& 'C:\Repos\Theory of Everything\.venv\Scripts\Activate.ps1'
```

Run OR-Tools runner for seed 0 (recommended if `ortools` is installed):

```powershell
python scripts/transport_csp_or_tools_larger.py --seed 0 --time_limit 300 --workers 8
```

Export CNF for multiple seeds and generate a PowerShell runner script:

```powershell
python scripts/transport_job_generator.py --seeds 0-7 --time_limit 300 --workers 8
# will write data/transport_seed{S}.cnf and data/run_transport_jobs.ps1
```

If you prefer to use an external SAT solver, export CNF only and run your
solver on `data/*.cnf` files. The CNF exporter writes a `.meta.json` with
variable mapping to recover assignments:

```powershell
python scripts/transport_csp_cnf_export.py --out data/transport_seed0.cnf --seeds 0
```

After any solver run that produces a JSON assignment (or after mapping a SAT
model back to an assignment), verify using the repo verifier:

```powershell
python scripts/transport_result_verify.py data/<solver_result.json>
```

Outputs
-------

- `data/transport_csp_or_tools_seed{S}.json` — OR-Tools output (if used)
- `data/transport_csp_pysat_seed{S}.json` — pysat flow result (if used)
- `data/transport_seed{S}.cnf` and `data/transport_seed{S}_seed{S}.cnf.meta.json` — CNF + varmap
- `data/transport_verification_*.json` — verification certificates produced by the verifier

Escalation tips
---------------

- If CP-SAT times out, increase `--time_limit` and try multiple `--seed` values
  (these break the first-orbit symmetry). Use `transport_job_generator.py` to
  create many seed jobs quickly.
- For SAT farms, export CNF and run Kissat/Maple/etc., then convert models using
  the `.meta.json` varmap.
- If external solvers fail, try minimal symmetry-breaking seeds: allow a small
  number of representative orbits free (edit `transport_csp_cnf_export.py`), or
  generate lex-leader constraints to prune symmetric solutions.

Notes
-----

- All solver runs should be performed in the repository venv to ensure imports
  and helper bridges resolve. If you produce candidate assignments, include the
  verification certificate (JSON) when reporting results so the verification
  bridges can reproduce the check deterministically.
