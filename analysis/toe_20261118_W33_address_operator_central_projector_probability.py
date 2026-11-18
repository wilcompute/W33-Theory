"""Native W33 H27 central-charge projection to E6 operator sector.

The no-invertible-intertwiner theorem and rank<=9 are ALREADY repo prior art
(2026-09-22), as are nontrivial nine-dimensional commutant dressings.
This implementation adds an exact numerical canonical central-Fourier
projection on the ACTUAL W33 27-point regular torsor and its
per-address acceptance probability, not an E6 physical quantum channel.
"""
import sys,json,numpy as np
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_W33_triperiodic_Levi_homogenization as W
from toe_20261118_W33_dual_parabolic_radicals_27 import unipotent_radical

def run():
    _,points,lines=W.levi()
    ix={p:i for i,p in enumerate(points)}
    perms=[]
    for v in points:
        perms.append(Permutation([ix[W.projective(tuple((x[k]+W.symplectic(x,v)*v[k])%3
                            for k in range(4)))] for x in points]))
    G=PermutationGroup(perms)
    _,H=unipotent_radical(G.stabilizer(0))
    far=sorted(i for i in range(40) if i!=0 and
               W.symplectic(points[0],points[i])!=0)
    assert len(far)==27
    index={p:i for i,p in enumerate(far)}
    center=[z for z in H if all(z*h==h*z for h in H)]
    assert len(center)==3
    z=next(q for q in center if q.order()==3)
    R=np.zeros((27,27),complex)
    for j,p in enumerate(far):R[index[z(p)],j]=1
    I=np.eye(27, dtype=complex)
    assert np.max(abs(R.conj().T@R-I))<1e-13
    assert np.max(abs(np.linalg.matrix_power(R,3)-I))<1e-13
    assert abs(np.trace(R))<1e-13
    omega=np.exp(2j*np.pi/3)
    sectors={}
    Ps=[]
    for k in (0,1,2):
        lam=omega**k
        P=(I+np.conj(lam)*R+np.conj(lam)**2*(R@R))/3
        assert np.max(abs(P-P.conj().T))<1e-13
        assert np.max(abs(P@P-P))<1e-13
        assert np.max(abs(R@P-lam*P))<1e-12
        assert abs(np.trace(P)-9)<1e-11
        assert np.allclose(np.diag(P),1/3)
        assert np.linalg.matrix_rank(P,tol=1e-10)==9
        for h in H:
            Rh=np.zeros((27,27),complex)
            for j,p in enumerate(far):Rh[index[h(p)],j]=1
            assert np.max(abs(P@Rh-Rh@P))<1e-12
        Ps.append(P)
        sectors[str(k)]=dict(center_eigenvalue= "1" if k==0 else "omega" if k==1 else "omega^2",
                  exact_projector_rank=9,
                  computational_address_state_success_probability=1/3,
                  maximally_mixed_success_probability=1/3)
    assert np.max(abs(Ps[0]+Ps[1]+Ps[2]-I))<1e-12
    assert all(np.max(abs(Ps[i]@Ps[j]))<1e-12 for i in range(3) for j in range(i+1,3))
    # For any 27-address computational label, projecting onto target
    # E6 center-character omega succeeds with probability 1/3.
    # But arbitrary superpositions may live entirely outside the rank9
    # source sector => probability0. So no universal lossless transducer.
    target=Ps[1]
    succ=[float(np.real(target[i,i])) for i in range(27)]
    assert max(abs(v-1/3) for v in succ)<1e-12
    # E6 operator 27 has center scalar omega and nine copies of Vomega,
    # so any equivariant linear T obeys T=T Pomega by center relation.
    # Compute explicit no-kernel-bound violation:
    assert np.linalg.matrix_rank(target,tol=1e-10)==9
    out=dict(status="PASS",W33_far_shell_order=27,
             native_center_orbits=9,source_regular_character_sector_ranks=sectors,
             fourier_projectors_pairwise_orthogonal=True,
             target_trinification_center_character="omega",
             E6_operator_representation_dimension=27,
             equivariant_linear_map_rank_upper_bound=9,
             canonical_postselect_center_sector="P_omega=(I+omega^-1 Rz+omega^-2 Rz^2)/3",
             probability_for_each_of_27_address_basis_states=1/3,
             probability_for_maximally_mixed_address=1/3,
             worst_case_input_success_probability=0,
             best_case_input_success_probability=1,
             quantum_information_loss="Heralded central-sector projection removes18 of27 complex amplitudes. Cannot be a universal reversible encoder; record cannot make it an E6 linear equivariance isomorphism.",
             Clifford_implementation="In a chosen group-coordinate basis H27~(a,b,c), the center acts by cyclic shifting c. Fourier transform the c qutrit and measure eigenvalue omega, obtaining 1/3 on each computational address basis input. This fixes a coordinate gauge and is not a native photonic experiment.",
             prior_art="Intertwiner rank<=9 and center-character mismatch were established by repo 2026-09-22; nine-dimensional commutant dressing already in Pass11043. New computation is the exact source-W33 projector and operational success bound for this natural projection.")
    file=ROOT/"data/toe_20261118_W33_address_operator_central_projector_probability.json"
    file.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS native W33 center projectors ranks9+9+9; basis address postselect1/3; no reversible27->27 intertwiners")
    return out

if __name__=="__main__":run()
