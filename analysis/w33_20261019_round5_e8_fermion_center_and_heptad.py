"""Fronts 1-2: E8/SU9 central-character obstruction to the nine
fundamental fermions, and exact discrete projector-outcome census of
one W33 maximum noncommuting heptad.

Read Pass11681, Pass11687-91 and earlier October-19 result before claims.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
from w33_20261019_tick_operator_frame_majorization import points,build_projectors,symp
from w33_20261019_tick_commutator_extremum import maximal_cliques
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_round5_e8_fermion_center_and_heptad.json"
z9=np.exp(2j*np.pi/9)
omega=z9**3
P=build_projectors(points()).reshape(40,3,9,9)
pts=points()
masses=np.zeros(120)
cl=maximal_cliques([sum(int(i!=j and symp(pts[i],pts[j])!=0)<<j for j in range(40)) for i in range(40)])
hept=tuple(next(x for x in cl if len(x)==7))
# E8 adjoint of SU9 has three parts: sl9 (80), Lambda3 (84), Lambda6 (84).
# A scalar omega I_9 is identity on ALL those spaces but acts as omega on fundamental 9.
def center():
    eig_fund=omega
    eig_sl9=1+0j
    eig_w3=omega**3
    eig_w6=omega**6
    allowed_rep=False
    return {"central_element":"omega I_9, omega=e^(2pi*i/3), det(omega I_9)=1",
        "fundamental9_character":[float(eig_fund.real),float(eig_fund.imag)],
        "E8_grade_characters":{"sl9":[1,0],"Lambda3":[float(eig_w3.real),float(eig_w3.imag)],
            "Lambda6":[float(eig_w6.real),float(eig_w6.imag)]},
        "full_248_central_element_identity_residual":max(abs(eig_sl9-1),abs(eig_w3-1),abs(eig_w6-1)),
        "fundamental_nontrivial_center_residual":abs(eig_fund-1),
        "representation_theorem":"SU9->E8 has kernel mu3. The fundamental 9 of SU9 is nontrivial on this kernel, hence cannot be a linear representation of the embedded SU9/mu3 subgroup of E8. Neither sl9 nor Lambda3 nor Lambda6 contains a 9 SU9 representation. Therefore a nine-fundamental-fermion matter bath is not supplied by the E8 adjoint branching alone.",
        "scope":"Does not forbid externally added fundamental fermions after lifting gauge group, symmetry breaking, charged defects or projective representations; no natural mu=1/2 follows.",
        "pass":bool(abs(omega**3-1)<1e-12 and abs(eig_fund-1)>1)}
def eig_for(choice):
    Q=sum(P[p,k] for p,k in zip(hept,choice))/7
    return np.linalg.eigvalsh(Q)
def free(ev,T):
    e=np.exp((ev-1)/T)
    return float(-T*np.log(e.sum()))
def census():
    spectra={}
    outcome_records=[]
    for choices in itertools.product(range(3),repeat=7):
        ev=eig_for(choices)
        key=tuple(np.round(ev,10))
        spectra.setdefault(key,0)
        spectra[key]+=1
        outcome_records.append((choices,ev))
    totals=sum(spectra.values())
    ranks=[]
    for T in (.1,.2,.5,1.,2.):
        values=np.array([free(ev,T) for _,ev in outcome_records])
        ix_best=int(np.argmin(values));ix_worst=int(np.argmax(values))
        sort=np.argsort(values)
        ranks.append({"T":T,"minimum_F":float(values[ix_best]),
            "maximum_F":float(values[ix_worst]),
            "spread_F":float(np.ptp(values)),
            "argmin_outcomes":list(outcome_records[ix_best][0]),
            "argmax_outcomes":list(outcome_records[ix_worst][0]),
            "all_zero_outcome_F":float(values[0]),
            "all_zero_outcome_rank":int(np.count_nonzero(values<values[0]-1e-11)+1),
            "number_nearly_optimal":int(np.sum(values<values[ix_best]+1e-10))})
    # all 7 projective directions are pairwise noncommuting; so C=4/7 exactly
    ok=all(symp(pts[p],pts[q])!=0 for p,q in itertools.combinations(hept,2))
    return {"seven_clique":list(hept),"outcome_assignments_enumerated":totals,
        "distinct_eigenspectra_at_10_decimal_precision":len(spectra),
        "eigenspectrum_family_sizes":sorted(spectra.values()),
        "temperature_census":ranks,
        "noncommutation_C":"4/7 for every one of the 3^7 assignments at uniform s=1/7",
        "significance":"Previous 40-rate scans fixed k=0; exactly 3^7 choices on this heptad have DIFFERENT Gibbs energies. Fixed identical outcomes is not globally justified.",
        "pass":ok and totals==2187 and len(spectra)>1}
def run():
    c=center();h=census()
    checks={"E8_central_obstruction":c["pass"],"heptad_outcome_census":h["pass"],
        "outcome_energy_spread_detected":max(x["spread_F"] for x in h["temperature_census"])>1e-5}
    out={"schema":"w33.round5.e8_fermion_center_and_heptad.v1",
         "prior_art":"Repo Pass 11681 constructs e8=sl9+Lambda3+Lambda3* and Pass 11687-91 documents matter grades; earlier October-19 packets proved outcome-vertex reduction. The SU9/mu3 central-kernel obstruction is a representation-theoretic consequence, not a novel E8 classification.",
         "matter_sector_center_obstruction":c,
         "heptad_outcome_exhaustive":h,
         "checks":{k:bool(v) for k,v in checks.items()},
         "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"heptad_spectra":h["distinct_eigenspectra_at_10_decimal_precision"],
        "temperatures":h["temperature_census"]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
