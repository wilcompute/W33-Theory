"""Exact commuting/noncommuting two-tick spectra and fourth-order incidence.
Intrinsic bare two-projector Gibbs discrimination first appears at quartic
order and favors commuting projectors; does NOT induce negative C coupling.
"""
from __future__ import annotations
import json,itertools
import numpy as np
from pathlib import Path
from w33_20261019_tick_operator_frame_majorization import points,symp,build_projectors
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_nextfive_quartic_incidence.json"
pts=points()
P=build_projectors(pts)
A=P[0]
pc=next(j for j in range(1,40) if symp(pts[0],pts[j])==0)
pn=next(j for j in range(1,40) if symp(pts[0],pts[j])!=0)
C=P[3*pc]; N=P[3*pn]
a,b=.5,.5

def spectrum(B):
    return np.linalg.eigvalsh(a*A+b*B)
def partition(spec,T):
    x=spec/T
    mx=max(x)
    return float(np.exp(mx)*np.exp(x-mx).sum())
def analytic_spec(kind):
    if kind=="commuting": return np.array([1.]+[a]*2+[b]*2+[0.]*4)
    delta=np.sqrt((a-b)**2+4*a*b/3)
    return np.array([(a+b+delta)/2]*3+[(a+b-delta)/2]*3+[0.]*3)

s_c=spectrum(C);s_n=spectrum(N)
ac=analytic_spec("commuting");an=analytic_spec("noncommuting")
mom={}
for k in range(1,9):
    mom[str(k)]={"commuting":float(np.sum(s_c**k)),
        "noncommuting":float(np.sum(s_n**k)),
        "difference":float(np.sum(s_c**k)-np.sum(s_n**k))}
# n=4 trace difference from two alternating projector words: 2*(1-1/3)*a^2 b^2 =4/3 a² b².
temps=[.1,.2,.5,1.,2.,5.,10.,20.]
rows=[]
for T in temps:
    Zc=partition(s_c,T);Zn=partition(s_n,T)
    fd=float(T*np.log(Zc/Zn))  # F_non - F_comm
    leading=(a*a*b*b)/(162*T**3)
    rows.append({"T":T,"commuting_preferred_free_energy_gap":fd,
                 "large_T_quartic_asymptotic":leading,
                 "ratio_to_quartic_asymptotic":fd/leading})
# Exact termwise sign proof: every cyclic word in P,Q containing both
# reduces to alternating r blocks (PQ)^r (for r>=1).
# Commuting tr=1; isoclinic noncomm tr=3^(1-r).
# Thus all exp Taylor coefficients of Zcomm-Znon >=0, strict for r>=2.
checked=[]
for r in range(1,6):
    direct=np.trace(np.linalg.matrix_power(A@N,r)).real
    checked.append({"r":r,"direct_trace":float(direct),
                    "analytic_trace":float(3**(1-r))})
checks={
 "commuting_eigenspectrum_exact":np.max(abs(np.sort(s_c)-np.sort(ac)))<1e-12,
 "noncommuting_eigenspectrum_exact":np.max(abs(np.sort(s_n)-np.sort(an)))<1e-12,
 "same_moments_up_through_cubic":all(abs(mom[str(k)]["difference"])<1e-12 for k in (1,2,3)),
 "quartic_coefficient_exact":abs(mom["4"]["difference"]-(4/3)*a*a*b*b)<1e-12,
 "noncommuting_alternating_word_trace":all(abs(x["direct_trace"]-x["analytic_trace"])<1e-12 for x in checked),
 "intrinsic_commuting_preference_all_sampled_T":all(z["commuting_preferred_free_energy_gap"]>0 for z in rows),
 "high_T_asymptotic_converges":abs(rows[-1]["ratio_to_quartic_asymptotic"]-1)<.1
}
checks={k:bool(v) for k,v in checks.items()}
out={"schema":"w33.nextfive.quartic_incidence.v1",
 "claim":"For any two distinct W33 projective Pauli directions with the same positive weights a,b, the bare Gibbs trace is strictly larger for a COMMUTING pair than for NONCOMMUTING pair at all T>0 (if a,b>0). Incidence first appears at fourth trace moment.",
 "noncommuting_projector_isoclinicity":"P Q P = P/3; Tr (PQ)^r=3^(1-r)",
 "commuting_spectrum":"{a+b:1,a:2,b:2,0:4}",
 "noncommuting_spectrum":"{(a+b+sqrt((a-b)^2+4ab/3))/2:3,(a+b-sqrt(...))/2:3,0:3}",
 "moment_difference_n4":"Tr[(aP+bQcomm)^4]-Tr[(aP+bQnoncomm)^4]=(4/3)a^2 b^2",
 "asymptotic_free_gap":"F_noncomm - F_comm = a^2*b^2/(162*T^3) + O(T^-4) for a+b=1",
 "sign_proof":"Every cyclic mixed word has trace 1 for commuting P,Q; for isoclinic noncommuting P,Q it has trace 3^(1-r) where r alternating PQ blocks. For r>=2 this is strictly below 1, with positive exponential Taylor coefficients.",
 "scope":"Two distinct projective Pauli directions, fixed positive a,b, rank-three outcome projectors. Does not prove arbitrary multi-tick incidence contributions have fixed sign; does not produce negative coupling or physical time.",
 "input_weights":[a,b],"moments":mom,"temperature_comparison":rows,
 "alternating_trace_checks":checked,"checks":checks,"all_checks_pass":all(checks.values())}
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"checks":checks,"moments_first_four":{k:mom[k] for k in ("1","2","3","4")},
 "T10_ratio":rows[-2]["ratio_to_quartic_asymptotic"]},indent=2))
assert out["all_checks_pass"]
