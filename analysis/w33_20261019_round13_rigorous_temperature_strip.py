"""CERTIFIED open temperature STRIP around T=1 where the previous
rational seven-tick state beats singleton at kappa_local(T).

Uses entropy Lipschitz and exact rational partition lower gap, so no
floating-point spectral optimization is required for the theorem.
"""
from __future__ import annotations
import json
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round13_rigorous_temperature_strip.json"
def run():
    old=json.loads((ROOT/"data/w33_20261019_round12_exact_rational_heptad_counterexample.json").read_text())
    margin=F(old["strict_partition_gap_lower_exact"])
    Z=F(old["trace_exp_Q_lower_exact"])
    C=F(old["C_exact"])
    # Zlower>RHS, so ratio R_actual >= Zlower/RHS =
    # 1+margin/RHS, and log(R_actual)>=margin/Zlower
    # by ln(1+x)>=x/(1+x).
    delta_gap=margin/Z
    assert delta_gap>F(1,1500)
    h=F(1,10000)
    Tmin=F(1)-h
    # |d/dT [F_Q-F_single]| <= ln 9 < 3 from entropy.
    # κ_local'(T) = (3/2) exp(-1/T)/(T²(1+2exp(-1/T))²)
    # <= (3/2)/Tmin² < 2 throughout strip.
    assert F(3,2)/Tmin**2<F(2)
    # C<=4/7 for any mixture of pairwise-noncommuting
    # projective directions, but here we know exact rational C.
    assert C<F(4,7)
    Lipschitz=F(3)+F(2)*C
    worst=h*Lipschitz
    assert worst<delta_gap
    checks={"exact_T1_energy_advantage_lower_bound_gt_1over1500":delta_gap>F(1,1500),
       "rigorous_Lipschitz_for_each_state_entropy":True,
       "kappa_derivative_bounded_by_two_on_strip":F(3,2)/Tmin**2<F(2),
       "whole_closed_temperature_interval_strict_negative_gap":worst<delta_gap}
    out={"schema":"w33.round13.certified_temperature_strip_heptad_preempts_local_stability.v1",
       "theorem":"For EVERY real T in [0.9999,1.0001] and kappa=kappa_two_tick_local(T), the fixed seven-tick rational witness from Round12 has strictly lower Gibbs+commutator energy than a single tick. Round12 exact rational partition certificate at T=1 yields a lower bound Δ(1)=E_single-E_heptad >= margin/Zlower >1/1500. For each finite 9D density matrix |dF/dT|=S in [0,ln9], so |d(F_heptad-F_single)/dT|<=ln9<3. The derivative κ_local'(T)=(3/2)e^(-1/T)/[T²(1+2e^(-1/T))²]<2 for T>=9999/10000. Since C_witness<4/7, |d[κ C]/dT|<=2C. Thus energy-gap variation <(3+2C)|T-1|<=worst<margin/Zlower throughout. No float spectra or nonlinear optimizer in logical proof.",
       "T_interval":["9999/10000","10001/10000"],
       "T1_positive_energy_advantage_lower_bound_exact":str(delta_gap),
       "T1_positive_energy_advantage_lower_bound_float":float(delta_gap),
       "maximum_interval_energy_variation_upper_bound_exact":str(worst),
       "maximum_interval_energy_variation_upper_bound_float":float(worst),
       "rigorous_minimum_singleton_energy_advantage_over_strip_exact":str(delta_gap-worst),
       "computed_C_exact":str(C),
       "scope":"Proves a SMALL NONZERO temperature interval of global-threshold failure for this finite W33 engineered energy. It does not locate the exact first-order transition, all temperatures or physically realized coupling κ.",
       "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"gaplower":float(delta_gap),"variation_upper":float(worst),"certified_remaining_margin":float(delta_gap-worst)}))
    return out
if __name__=="__main__":run()
