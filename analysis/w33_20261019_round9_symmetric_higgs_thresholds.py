"""Front5: rigorous scalar permutation-symmetric threshold potential
classification, and conditional one-loop dimensionless Lambda ratios.
Demonstrates why W33/E8 symmetry alone cannot fix threshold ratios.
"""
from __future__ import annotations
import json,math
import numpy as np
from pathlib import Path
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round9_symmetric_higgs_thresholds.json"
def V(x,m2,b,c):
    S=sum(x)
    return -m2*S+b*np.dot(x,x)+c*(S*S-np.dot(x,x))/2
def phases(m2,b,c):
    if c<2*b:
        x=np.full(3,m2/(2*(b+c)))
    elif c>2*b:
        x=np.array([m2/(2*b),0.,0.])
    else:
        x=np.full(3,m2/(6*b))
    return x
def run():
    b=1.;m2=1.
    rows=[]
    rng=np.random.default_rng(20261019)
    for c in (0.,1.,1.9,2.,2.1,3.,5.):
        x=phases(m2,b,c)
        equal=np.full(3,m2/(2*(b+c)))
        single=np.array([m2/(2*b),0,0])
        Emin=min(V(equal,m2,b,c),V(single,m2,b,c))
        energies=[]
        for _ in range(22):
            s=rng.dirichlet(np.ones(3))*(rng.uniform(.05,2))
            opt=minimize(V,s,args=(m2,b,c),method="SLSQP",
                         bounds=[(0,None)]*3,options={"ftol":1e-12})
            energies.append(float(opt.fun))
        rows.append({"quartic_cross_coefficient_c":c,
                     "phase": "equal" if c<2*b else ("single_condensate" if c>2*b else "flat_two_simplex"),
                     "representative_vev_squared":x.tolist(),
                     "minimum_potential_exact_formula_evaluated":V(x,m2,b,c),
                     "energy_equal":V(equal,m2,b,c),
                     "energy_single":V(single,m2,b,c),
                     "optimizer_min_gap_above_formula":min(energies)-Emin})
    # The threshold M_i = y_i sqrt(x_i) only has equality if both
    # radial VEVs and Yukawa couplings are permuted identically.
    cx=1.;x=phases(m2,b,cx)
    examples=[]
    for y in ([1,1,1],[1,2,4]):
        M=np.sqrt(x)*y
        lo=(M[2]/M[0])**(2/11)
        examples.append({"Yukawas":y,"radial_vev_sq":x.tolist(),
            "thresholds_GeV_relative":M.tolist(),
            "IR_scale_ratio_sector3_to1":float(lo)})
    # exact identity:
    # V = -m2 S +(b-c/2) sum xi^2 +(c/2) S^2.
    # at fixed S, min squares=S²/3 for c<2b, and max=S² for c>2b.
    # c=2b -> all xi with S=m2/(2b) minimize equally.
    checks={
       "global_exchange_symmetric_potential_phases":all(abs(r["minimum_potential_exact_formula_evaluated"]-min(r["energy_equal"],r["energy_single"]))<1e-12 for r in rows),
       "numerical_optimizers_recover_analytic_min":min(r["optimizer_min_gap_above_formula"] for r in rows)>-1e-7 and max(r["optimizer_min_gap_above_formula"] for r in rows)<1e-5,
       "critical_c_equal_2b_flat_many_VEVs":abs(V(np.array([.25,.15,.1]),m2,b,2)-V(np.array([.5,0,0]),m2,b,2))<1e-12,
       "equal_thresholds_need_equal_Yukawas":abs(examples[0]["IR_scale_ratio_sector3_to1"]-1)<1e-12 and examples[1]["IR_scale_ratio_sector3_to1"]>1.25}
    out={"schema":"w33.round9.S3_higgs_scalar_threshold_free_parameters.v1",
      "theorem":"For x_i=Tr(Phi_i^dag Phi_i)>=0, i=1,2,3, and S3-permutation-invariant radial potential V=-m² sum x_i+b sum x_i²+c sum_{i<j} x_i x_j with m²,b>0,c>=0: if c<2b the GLOBAL minima are x_1=x_2=x_3=m²/[2(b+c)]; if c>2b the GLOBAL minima are three permutations of (m²/(2b),0,0); if c=2b the entire simplex sum x_i=m²/(2b) is flat. Proof rewrite V=-m²S+(b-c/2)sum x_i²+(c/2)S², and at fixed S, S²/3<=sum x_i²<=S².",
      "rows":rows,
      "conditional_mass_thresholds":"Only in equal-VEV regime and with IDENTICAL Yukawa y_i do M_i=y_i sqrt(x_i) coincide. Otherwise ratios remain continuous parameters. If one-loop bUV=9,bIR=11, Lambda_IR,i/Lambda_IR,j=(M_i/M_j)^(2/11); this does NOT arise from W33 alone.",
      "Yukawa_examples":examples,
      "physical_boundary":"A deliberately minimal radial S3 potential, not derived from W33 or the noncompact E8(-24) action. It omits gauge-index contractions/orientations, cubic invariants, flat directions, gauge breaking, physical vevs, EW scale and ghosts; phenomenological observables are not determined.",
      "checks":{k:bool(v) for k,v in checks.items()},
      "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"examples":examples},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
