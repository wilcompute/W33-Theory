"""TOE49: RG/matching-scale counterterm for Pass11909 SUSY Coleman-Weinberg.

Fixed-coupling one-loop V(Q) depends on arbitrary Q. Exact Q change
can be absorbed by a local gauge-allowed |H|² trace mass counterterm.
A selected Q/msoft is NOT a dynamical prediction until matching/RG
conditions fix the finite term.
"""
import sys,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_pass11909_up_sector_coleman_weinberg import V_SUSY,masses
O=R/"data/w33_20261010_toe49_cw_scale_counterterm.json"
rng=np.random.default_rng(49009)
ms=1000.;Q0=.6307*ms;Q1=1.1*ms
# define M_c^2=masses(x,nu)^2, S_c=M_c²+ms²
# V(Q1)-V(Q0) = (3/16pi²)*[-ln(Q1²/Q0²)] *sum (2 ms² M_c²+ms^4)
# = -(3 ms²/4pi²)ln(Q1/Q0) sum M_c² - (9 ms^4/8pi²) ln(Q1/Q0)
alpha= -3*ms**2/(4*np.pi**2)*np.log(Q1/Q0)
constant= -9*ms**4/(8*np.pi**2)*np.log(Q1/Q0)
res=[]
for _ in range(52):
 z=[float(rng.uniform(0,1/3)),float(rng.uniform(0,1/3))]
 m2=masses(*z)**2
 delta=V_SUSY(z,ms,Q1)-V_SUSY(z,ms,Q0)
 res.append(float((delta-alpha*m2.sum()-constant)))
residual=float(max(abs(np.array(res))))
assert residual<.002,(residual,constant)
# numerical absolute size is order 1e9, residual relative ~1e-13.
relative=residual/max(1,abs(constant))
assert relative<1e-11
# Identify scale-dependent coefficient. Matching finite counterterm
# alpha1 = alpha0-alpha to make V(Q1)+counter(Q1) equal V(Q0)+counter(Q0).
# This counterterm has the Wilson line dependence of sum m².
c0=0;c1=-alpha
res2=[]
for _ in range(42):
 z=[float(rng.uniform(0,1/3)),float(rng.uniform(0,1/3))]
 m2=masses(*z)**2
 res2.append(float((V_SUSY(z,ms,Q1)+c1*m2.sum())-(V_SUSY(z,ms,Q0)+c0*m2.sum())-constant))
assert max(abs(np.array(res2)))<.002
out={
"status":"TOE49_CW_MATCHING_SCALE_IS_NOT_A_PHYSICAL_WILSON_VACUUM_PARAMETER",
"msoft_GeV":ms,"Q0_GeV":Q0,"Q1_GeV":Q1,
"field_dependent_scale_shift_coefficient_GeV2":alpha,
"field_independent_shift_GeV4":constant,
"counterterm_shift_needed_GeV2":c1,
"max_52_points_absolute_Vshift_formula_error_GeV4":residual,
"max_52_points_relative_Vshift_error":relative,
"derivation":"For S=m²+msoft², V(Q)=(3/16pi²)sum[S²(log(S/Q²)-3/2)-m⁴(log(m²/Q²)-3/2)]. V(Q1)-V(Q0)=-(3/(8pi²))log(Q1/Q0) sum[2 msoft² m²+msoft⁴]. This equals alpha sum m² + constant with alpha= -3 msoft² log(Q1/Q0)/(4pi²).",
"conclusion":"The vacuum location found by scanning the renormalization/matching scale Q with fixed tree-level Wilson-flat potential changes if one includes allowed finite Wilson/Higgs mass counterterms. Changing Q by itself is not a tunable physical mechanism or prediction; one must specify full renormalized matching conditions, RG running, gauge/down/lepton sectors and all Wilson-dependent local terms. The Pass11909 restricted fixed-coupling potential is mathematically calculated correctly, but its Q-dependent vacuum should not be construed as scheme-independent.",
"boundary":"This is a formal one-loop scale identity and counterterm dependence, not proof that a particular UV supersymmetric completion admits or excludes the hierarchical vacuum."
}
O.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"residual":residual,"relative":relative,"alpha":alpha}))
