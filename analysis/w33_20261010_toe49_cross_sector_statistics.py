"""TOE49: observational limits and shared-family-torus analytic obstruction.

Positive mass invariants from frozen Pass11910 and sample bounds from 11911,
not a proof of no string vacua.
"""
import json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
m=json.loads((R/"data/w33_pass11910_cross_sector_invariant_and_ckm.json").read_text())
f=json.loads((R/"data/w33_pass11911_susy_z3_scan.json").read_text())
assert m["all_checks_pass"]
rates=m["data_invariants"];T=m["implied_im_tau"]
area_up_down=T["up"]/T["down"]
area_down_lept=T["down"]/T["lept"]
assert 1.5<area_up_down<1.7
ratio=rates["down"]/rates["up"]
assert 600<ratio<800
# If 0 successes in N IID draws from a FIXED population,
# the one-sided Clopper-Pearson upper endpoint is 1-alpha^(1/N).
# Distinct model spectra are NOT independent draws from the space of
# physical vacua, and stochastic scan distribution may overweight some.
c95=1-.05**(1/80000)
per=1-.05**(1/20000)
assert c95>3.6e-5 and c95<3.9e-5
out={"status":"TOE49_CROSS_SECTOR_AREA_AND_RANDOM_SCAN_BOUNDARY",
"cross_sector":{"reference":"Pass11910 fixed MZ running masses",
"invariant_up":rates["up"],"invariant_down":rates["down"],"invariant_lepton":rates["lept"],
"inferred_Im_tau_up":T["up"],"down":T["down"],"lepton":T["lept"],
"required_effective_area_up_over_down":area_up_down,
"invariant_down_over_up":ratio,
"shared_tau_one_higgs_obstruction":"Pass11910 says same gaussian e^(-4pi Im tau/3) for up, down and lepton. Their frozen masses imply up/down invariants differ by ~716 and effective Im tau ratio~1.605, violating the shared-tau ansatz. Sector-dependent torus/flux, nonlocal Higgs, modified wavefunction kinetics or threshold effects are needed; the formula is asymptotic near a hierarchy branch, not exact over arbitrary Wilson directions."},
"supersymmetric_Z3_scan":{"draws_total":80000,"successes_reported":0,
"model_groups_reported":4,
"conditional_95pct_one_sided_binomial_upper_hit_probability_if_IID":c95,
"conditional_95pct_per_20000_draw_class":per,
"claim_scope":"Only the four specified shift classes, orbifolder's SM-like criteria (including vector-like exotics), and their reported random draw protocol. No mathematical exclusion of all supersymmetric E8xE8 Z3 compactifications, no proof of independence of inequivalent spectra. The 80k trials across four distributions cannot be treated as one uniform sampler of the complete model landscape."},
"math_proof":"For iid Bernoulli success probability p, P(0 successes in N)=(1-p)^N. Solve (1-p)^N=.05 for the one-sided 95% upper confidence endpoint p=1-.05^(1/N)."
}
(R/"data/w33_20261010_toe49_cross_sector_statistics.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"area":area_up_down,"ratio":ratio,"95_up":c95}))
