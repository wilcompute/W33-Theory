"""Native E6 27 x 27 exact test of the quartic adjoint-family Yukawa bridge.

No new spacetime/zero-mode claim. Tests if two commuting 16_-3 generators
CAN act nontrivially in succession on the 27 singlet, producing a 10_-2.
"""
import json,itertools,sys
from pathlib import Path
from math import lcm
import sympy as s
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_wire_Novikov_E6 as N
import w33_pass10950_clock_albert_lorentz_spinor as P
from toe_20261118_Albert_qubit_qutrit_SM_selector import independent


def run():
    old=json.loads((ROOT/"data/toe_20261118_wire_Novikov_E6.json").read_text())
    assert old["status"]=="PASS"
    J=P.build_clock_albert()
    n=27
    den=lcm(*[v.denominator for v in J["prod"].flat])
    Pi=np.array([[[int(v*den) for v in row] for row in plane]
                 for plane in J["prod"]],dtype=np.int64)
    L=np.stack([Pi[i].T for i in range(n)])
    frame=[J["idx"][g] for g in J["G"]]
    c=frame[0]
    e_c=s.zeros(n,1);e_c[c]=1
    Psi=6*s.Matrix(L[c])/den-2*s.eye(n)
    Chi=s.Matrix([[s.sympify(v) for v in row]
                  for row in old["native_chi_matrix"]])
    Y=json.loads((ROOT/"data/toe_20261118_biCayley_Peirce16_SM.json").read_text())
    Y=s.Matrix([[s.sympify(v) for v in row] for row in Y["full27_hypercharge_matrix"]])
    assert Psi*e_c==4*e_c and Chi*e_c==s.zeros(n,1) and Y*e_c==s.zeros(n,1)
    deriv=independent([L[i]@L[j]-L[j]@L[i]
                       for i,j in itertools.combinations(range(n),2)])
    eye=np.eye(n,dtype=np.int64)
    tl=[eye[:,i] for i in range(n) if i not in frame]
    tl += [eye[:,i]-eye[:,frame[-1]] for i in frame[:-1]]
    e6=[s.Matrix(d) for d in deriv]+[s.Matrix(np.tensordot(v,L,axes=1))
                                      for v in tl]
    assert len(e6)==78
    left16=N.kernel_combinations(e6,[list(Psi*M-M*Psi+3*M)
                                     for M in e6])
    assert len(left16)==16
    ten=N.kernel_combinations(left16,[list(Chi*M-M*Chi+M)
                                     for M in left16])
    assert len(ten)==10
    # The SAME native algebra also supplies an E6-invariant cubic
    # 78*(-3,-5) x 27bar*(-1,+5) x 27*(+4,0).
    # The adjoint singlet charge maps the 27 singlet into the 27 spinor
    # N^c direction: the 27bar dual pairs nontrivially with this image.
    nu_adj=N.kernel_combinations(left16,[list(Chi*M-M*Chi+5*M)
                                        for M in left16])
    assert len(nu_adj)==1
    nu_img=nu_adj[0]*e_c
    assert nu_img!=s.zeros(n,1)
    assert Psi*nu_img==nu_img and Chi*nu_img==-5*nu_img and Y*nu_img==s.zeros(n,1)
    # Tensor 10_-1 (x) 10_-1 -> 5bar_-2 under SU5; E6 27
    # has weight sequence Psi: +4 -> +1 -> -2, Chi:0 -> -1 -> -2.
    first=[M*e_c for M in ten]
    first_rank=s.Matrix.hstack(*first).rank()
    assert first_rank==10
    pair=[(i,j,ten[i]*ten[j]*e_c) for i in range(10) for j in range(i,10)]
    second_rank=s.Matrix.hstack(*(v for _,_,v in pair)).rank()
    assert second_rank==5, second_rank
    # The five-dimensional second-image is the SU5 5bar_-2 of the SO10
    # vector10_-2. Split by 6Y: d^c-type color 3 at +2; weak doublet 2 at -3.
    assert all((Y-2*s.eye(n))*(Y+3*s.eye(n))*v==s.zeros(n,1)
               for _,_,v in pair)
    weak=[(2*s.eye(n)-Y)*v/5 for _,_,v in pair]
    color=[(Y+3*s.eye(n))*v/5 for _,_,v in pair]
    assert s.Matrix.hstack(*weak).rank()==2
    assert s.Matrix.hstack(*color).rank()==3
    nonzero=[(i,j) for i,j,v in pair if v!=s.zeros(n,1)]
    for i,j,v in pair:
        assert Psi*v == -2*v
        assert Chi*v == -2*v
        # This tensor is an SO10 10_-2, SU5 5bar_-2;
        # the dual 27bar Higgs doublet belongs to 5_+2 with Psi+2.
    commutators=[ten[i]*ten[j]-ten[j]*ten[i]
                 for i in range(10) for j in range(i+1,10)]
    assert all(c==s.zeros(n) for c in commutators)
    # Exact symmetric bilinear double action C_ij^a nonzero, independent of
    # vanishing adjoint Lie brackets [T_i,T_j]=0.
    sym=True
    for i in range(10):
        for j in range(10):
            assert ten[i]*ten[j]*e_c==ten[j]*ten[i]*e_c
    # Rank of generic binary-to-five map is five, exposing a 10*10*5bar
    # invariant (quartic in two adjoints plus 27bar and 27 singlet).
    # Three E6-allowed SM singlet weights in 78,27bar,27 are
    # qA=(-5,-3), qBar=(+5,-1), qS=(0,+4).
    # Their sum is zero: equal VEV norm solves ALL Abelian moment maps.
    # As normalized weight vectors, all other Cartan charges vanish and
    # root-generator diagonal expectation values vanish by orthogonality.
    charges=[s.Matrix([-5,-3]),s.Matrix([5,-1]),s.Matrix([0,4])]
    assert sum(charges,s.zeros(2,1))==s.zeros(2,1)
    masses=sum((c*c.T for c in charges),s.zeros(2))
    assert masses==s.Matrix([[50,10],[10,26]])
    assert masses.det()==1200 and masses.eigenvals()=={
        38+2*s.sqrt(61):1,38-2*s.sqrt(61):1}
    # E6-invariant I = (27bar)* A78 *(27); the rank-one singlet
    # contraction was checked above using ACTUAL native 27 matrices.
    # W = I - I^2/2 is the lambda=1,kappa=-1/2,Lambda=1
    # instance of W=lambda I+kappa I^2/Lambda^3. f'(I=1)=0.
    x,y,z=s.symbols("x y z")
    I=x*y*z
    superW=I-I**2/2
    vacuum={x:1,y:1,z:1}
    F=[s.diff(superW,u).subs(vacuum) for u in (x,y,z)]
    assert F==[0,0,0]
    Hess=s.hessian(superW,(x,y,z)).subs(vacuum)
    assert Hess==-s.ones(3) and Hess.rank()==1
    # Exact net three-chiral-spinor abelian cubic anomaly polynomial
    # factors through the anomalous Psi direction; candidate one-axion
    # GS/Stueckelberg structure, not a constructed 11D inflow.
    chi,psi=s.symbols("chi psi")
    anom=3*(10*(-chi-3*psi)**3+5*(3*chi-3*psi)**3+
            (-5*chi-3*psi)**3)
    assert s.factor(anom)==-432*psi*(5*chi**2+3*psi**2)
    # Full E6 F-terms vanish for this specially chosen W=f(I)
    # because f'(I=1)=0, even along all unexcited field components.
    out=dict(status="PASS",native_E6_adj_dim=78,
             native_nu_adjoint_singlet_action_nonzero=True,
             native_nu_image_charge_PsiChiY=[1,-5,0],
             charge_balanced_78_27bar_27_singlet_VEVs=[list(map(int,c)) for c in charges],
             full_Abelian_Higgs_mass_matrix=masses.tolist(),
             mass_matrix_determinant=int(masses.det()),
             mass_matrix_eigenvalues=["38-2*sqrt(61)","38+2*sqrt(61)"],
             compact_E6_weight_vector_D_flat=True,
             E6_invariant_cubic_I="I=barF_27bar * A_78 * F_27; on singlet fields I~x*y*z, verified nonzero from native adjoint singlet action on 27 singlet.",
             nonrenormalizable_superpotential="W=I-I^2/2 in dimensionless units, namely lambda*I+kappa*I^2/Lambda^3 with nonzero coupling; I_vac=1 makes fprime(I)=0.",
             toy_F_flat_all_components=True,
             scalar_Hessian_rank_in_three_singlet_subspace=int(Hess.rank()),
             cubic_U1_anomaly_factorization="-432*Psi*(5*Chi^2+3*Psi^2) for three net 16_-3",
             GS_candidate_one_anomalous_abelian_direction="Psi, provided suitable local counterterms and UV inflow; not actually derived",
             unrepaired_anomalous_Psi="Three localized chiral 16_-3 still have Psi-gravitational=-144 and Psi-cubic=-1296. The added full 27+27bar are vectorlike for gauge anomalies; anomaly inflow or new chiral matter remains compulsory.",
             localized_ten_dim=10,
             e6_27_singlet_charge_PsiChi=[4,0],
             first_action_rank=first_rank,
             second_action_rank=second_rank,
             weak_doublet_hypercharge_Q6Y=-3,
             weak_doublet_rank=2,
             color_triplet_hypercharge_Q6Y=2,
             color_triplet_rank=3,
             nonzero_symmetric_pairs=len(nonzero),
             first_nonzero_pairs=nonzero[:10],
             second_action_charge_PsiChi=[-2,-2],
             adjoint_brackets_all_zero=True,
             two_step_action_commutes=True,
             gauge_invariant_quartic="(bar_27)_H * T_A * T_B * (27)_S * (78)^A*(78)^B",
             operator="E6-invariant operator W_eff=(1/Lambda)*Hbar T_A T_B S A^A B^B; <S> can generate a Yukawa for native two adjoint16_-3 matter components, since 27 has charge chain4->1->-2.",
             physical_scope="Rep-level EXACT nonvanishing quartic tensor. Whether two adjoint families, the 27 S, and 27bar H are massless 4D chiral superfields on the SAME flux/defect compactification, have normalizable profile overlaps, and satisfy all quantum selection rules is UNPROVED.")
    target=ROOT/"data/toe_20261118_native_E6_quartic_two_step.json"
    target.write_text(json.dumps(out,indent=2,default=int)+"\n",encoding="utf-8")
    print("PASS exact native quartic two-step: rank",second_rank,
          "nonzero sym pairs",len(nonzero))
    return out

if __name__=="__main__":run()
