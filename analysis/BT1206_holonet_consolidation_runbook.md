# BT1206 -- Holonet consolidation runbook

This records the execution path for BT1201--BT1204.

## New manuscript inserts

- `paper/sections/sec_bt1201_holonet_lambda_lock.tex`
- `paper/sections/sec_bt1202_holonet_r3_continuum_checklist.tex`

## Dashboard artifacts

- `data/bt1203_holonet_demonstrator_fault_tolerance_dashboards.json`
- `analysis/BT1204_holonet_milestone_dashboard.md`

## Integration helper

- `tools/integrate_bt1201_bt1202_holonet_inserts.py`

Run path:

```bash
python tools/integrate_bt1201_bt1202_holonet_inserts.py --dry-run
python tools/integrate_bt1201_bt1202_holonet_inserts.py
```

Expected insertion lines:

```tex
\input{paper/sections/sec_bt1202_holonet_r3_continuum_checklist}
\input{paper/sections/sec_bt1201_holonet_lambda_lock}
```

The R3 checklist is inserted before `The fault-tolerant layer is the substrate's lattice tower`.
The lambda-lock theorem is inserted before `Why the primitive is one massless photon`.

## Reviewer-facing boundary

BT1201 adds the caveat that photon helicity is not being generalized to arbitrary qudit dimension. The pump law has a dimension-q family, but a physical photon has exactly two transverse helicities. The significance is that the substrate fixes q=3, so q-1=2 matches the physical carrier.

BT1202 reframes R3 as a convergence residual rather than an architecture gap. The finite holonet architecture remains the symplectic/CV computer even if a metric spacetime continuum hypothesis fails.

BT1203/BT1204 separate near-term demonstrator falsifiers from fault-tolerant CV milestones, preventing the single-photon build from being misread as a threshold GKP machine.
