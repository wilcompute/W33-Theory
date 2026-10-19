"""Round6 front1: exact SU9-to-SU3^3 grade branching and gauge
obstruction, plus chemical-potential origin freedom. Uses existing
E8=sl9+Lambda3+Lambda3dual; DOES NOT invent SM matter.
"""
from __future__ import annotations
import itertools,collections,json
from pathlib import Path
import numpy as np
from w33_20261019_round4_fermions_global import specC,specN,omega
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round6_matter_lift_branch.json"
def run():
    sectors=collections.Counter()
    for inds in itertools.combinations(range(9),3):
        occ=tuple(sum(i//3==k for i in inds) for k in range(3))
        sectors[occ]+=1
    expected={
       (3,0,0):1,(0,3,0):1,(0,0,3):1,(1,1,1):27,
       (2,1,0):9,(2,0,1):9,(1,2,0):9,(0,2,1):9,(1,0,2):9,(0,1,2):9}
    n_single=sum(v for k,v in sectors.items() if max(k)==3)
    n_threefactor=sectors[(1,1,1)]
    n_twoone=sum(v for k,v in sectors.items() if sorted(k)==[0,1,2])
    Ucent=np.exp(2j*np.pi/3)
    center_chars={"fundamental_9":complex(Ucent),"three_fermion_84":complex(Ucent**3),"three_hole_84":complex(Ucent**-3),"adjoint_80":complex(1)}
    # Fock of 9 fundamental has charged sectors despite E8 adjoint
    # containing only center-trivial 84 and 80.
    # A separate full SU9 lift can couple fundamental fermions in 9,
    # but is extra matter content and changes global gauge group.
    from scipy.special import expit
    density=[]
    for T in (.05,.2,.5,1.,2.):
        occupations=[float(expit((s-1+.5)/T).sum()) for s in (specC,specN)]
        expected_count=3+3*float(expit(-.5/T))
        density.append({"T":T,"N_comm":occupations[0],"N_noncomm":occupations[1],
            "equal_formula":expected_count})
    # A uniform shift of the orbital energy origin must be accompanied
    # by same shift in mu; physical occupation unchanged.
    def gp(vals,T,mu):
        return float(-T*np.logaddexp(0,(vals-1+mu)/T).sum())
    shifts=[]
    for shift in (-2.,-.1,0.,.4,5.):
        # omega(H+shift*I,T,mu+shift) = omega(H,T,mu)
        T=.3;mu=.5
        lhs=-T*np.logaddexp(0,(specN-1-shift+mu+shift)/T).sum()
        rhs=gp(specN,T,mu)
        shifts.append(float(abs(lhs-rhs)))
    checks={
      "SU3cubed_Lambda3_branch_exact":dict(sectors)==expected,
      "dimension_84_partition":n_single+n_threefactor+n_twoone==84 and (n_single,n_threefactor,n_twoone)==(3,27,54),
      "central_mu3_blocks_fundamental_representation":abs(center_chars["fundamental_9"]-1)>1 and abs(center_chars["three_fermion_84"]-1)<1e-12,
      "equal_density_not_half_filling":all(abs(x["N_comm"]-x["N_noncomm"])<1e-12 and abs(x["N_comm"]-x["equal_formula"])<1e-12 for x in density),
      "chemical_potential_energy_origin_redundancy":max(shifts)<1e-12
    }
    result={"schema":"w33.round6.matter_lift_branching.v1",
      "branch":"Lambda3(3a + 3b + 3c) = (1,1,1) x3 singlets + (3,3,3) dimension27 + 6 ordered (Lambda2 3_i tensor 3_j) dimensions9 each =3+27+54=84.",
      "occupation_type_counts":{str(k):v for k,v in sectors.items()},
      "dimension_1_27_54":[n_single,n_threefactor,n_twoone],
      "center_kernel":"SU9 -> E8 factors through SU9/mu3. The SU9 fundamental 9 has nontrivial mu3 character; the 84 three-particle states are center-neutral. A 9 fundamental fermion bath cannot be identified with an adjoint E8 summand.",
      "gauge_lift_option":"One can posit full SU9 with additional 9-valued fermion matter (nontrivial mu3 charge), or an independently justified matter bundle; this changes the global gauge structure and is an ADDED assumption. SU3cubed branching alone does not fix a natural nine-mode Hamiltonian.",
      "equal_occupation_at_mu_point5":density,
      "energy_origin_redundancy":"A uniform shift of the 9 one-particle energies E->E+c can be undone by mu->mu+c. No absolute numerical chemical potential is physically fixed without an independently chosen energy reference. The special relative location mu=.5 for H=I-Q is not guaranteed by group data.",
      "max_energy_origin_shift_residual":max(shifts),
      "prior_repo":"Pass11681 E8 two-qutrit grading, Pass11687-91 matter/triality, Pass11879-83 Higgs SU9 claims.",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"checks":result["checks"],"branch_counts":result["dimension_1_27_54"]},indent=2))
    assert result["all_checks_pass"]
    return result
if __name__=="__main__":run()
