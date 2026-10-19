# Search drivers for Pass 12054 (Claude track)

These are the exploration scripts behind `analysis/w33_pass12054_tick_condensate_landau.py`. They import
`w33_pass12053_gate_sets_and_real_forms.setup` through a path to the old local worktree (`C:\tmp\toe_wt\analysis`);
adjust that path before rerunning.

| script | what it does |
|---|---|
| `landau.py` | Optimises sum phi^4 on the V15 and V24 spheres, and compares the results with the candidate patterns. |
| `landau2.py` | Scans the phase circle in 5-degree steps. |
| `landau3.py` | Identifies the support of each phase. |
| `landau4.py` | Locates the phase boundaries to 1 degree. |
