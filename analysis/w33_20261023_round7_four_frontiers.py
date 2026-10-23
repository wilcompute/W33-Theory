#!/usr/bin/env python3
"""Round 7 independent W33 physics/theory controls.

1. GF9 explicit connecting-map witnesses, not just Jordan dimensions.
2. Source-free K-symmetric many-two-qutrit mean-field chiral sectors.
3. Permutation routing: exact 3-layer CP-SAT attempt (bounded).
4. Offline qutrit magic |M+> -> Choi state with noise certificate.
5. Strict normalized W(3,q) kinetic gap obstruction.
"""
from __future__ import annotations
import json, math
from pathlib import Path
from itertools import product
import numpy as np
try:
    from analysis.w33_20261022_five_frontiers_round6 import (
        make_geometry,modular_basis,kernel_from_pivots,microscopic_chiral_projector,
        bell_resource_injection)
    from analysis.w33_20261022_five_followups_round5 import A,transvection
except ImportError:
    from w33_20261022_five_frontiers_round6 import (
        make_geometry,modular_basis,kernel_from_pivots,microscopic_chiral_projector,
        bell_resource_injection)
    from w33_20261022_five_followups_round5 import A,transvection


def delta_rows(mat,perm,p):
    return (np.asarray(mat,dtype=np.int64)[:,perm]-mat)%p


def reduce_and_insert(vec,pivots,p):
    z=np.array(vec,dtype=np.int64,copy=True)%p
    while True:
        nz=np.flatnonzero(z)
        if not len(nz):return False
        i=int(nz[0])
        if i in pivots:z=(z-int(z[i])*pivots[i])%p
        else:
            pivots[i]=z*pow(int(z[i]),-1,p)%p
            return True


def reduce_zero(vec,pivots,p):
    z=np.array(vec,dtype=np.int64,copy=True)%p
    while True:
        nz=np.flatnonzero(z)
        if not len(nz):return True
        i=int(nz[0])
        if i not in pivots:return False
        z=(z-int(z[i])*pivots[i])%p


def sparse(vec):
    return [[int(i),int(z)] for i,z in enumerate(vec) if z]


def frobenius_obstruction_witnesses():
    g=make_geometry(9);p=3;n=g["n"];perm=g["perm"]
    pivC=modular_basis(g["B"],p)
    basisC=np.array(list(pivC.values()),dtype=np.int64)
    K=kernel_from_pivots(pivC,n,p).astype(np.int64)
    dC=delta_rows(basisC,perm,p)
    pivDC=modular_basis(dC,p)
    # Row elimination of D(K) modulo C, tracking actual K preimages.
    zeros=np.zeros(n,dtype=np.int64)
    piv={j:(row.astype(np.int64),zeros) for j,row in pivC.items()}
    newDC=dict(pivDC)
    witnesses=[]
    c_intersection=0
    for pre in K:
        y=delta_rows(pre.reshape(1,-1),perm,p)[0]
        u=pre.copy()
        while True:
            nz=np.flatnonzero(y)
            if not len(nz):
                dy=delta_rows(u.reshape(1,-1),perm,p)[0]
                if np.any(dy):
                    c_intersection+=1
                    assert reduce_zero(dy,pivC,p)
                    if reduce_and_insert(dy,newDC,p):
                        witnesses.append({"preimage_ternary":"".join(map(str,u)),
                                          "image_ternary":"".join(map(str,dy))})
                break
            j=int(nz[0])
            if j in piv:
                z,src=piv[j]
                factor=int(y[j])
                y=(y-factor*z)%p
                u=(u-factor*src)%p
            else:
                factor=pow(int(y[j]),-1,p)
                piv[j]=(y*factor%p,u*factor%p)
                break
    assert len(witnesses)==4,(len(witnesses),c_intersection)
    assert len(piv)==470,(len(piv),n)
    assert len(pivDC)==54 and len(newDC)==58
    # Counted dependency rows can be redundant: their dimension is 58,
    # whereas the number of nonzero candidate rows depends on the basis.
    assert c_intersection>=58
    return {"status":"EXPLICIT_GF9_FIRST_ORDER_EXTENSION_WITNESS_RANK4",
      "q":9,"p":3,"n":820,"dimC":100,"dimK":720,"dimQ":620,
      "rank_DC":54,"rank_DK_intersection_C":58,
      "rank_delta1":4,
      "four_independent_witness_pairs":witnesses,
      "verification":"Each preimage is in K; its D-image lies in C, and four images are linearly independent modulo D(C).",
      "boundary":"Finite GF9 exact witness, no general q=p^t Frobenius decomposition theorem proved."}


def source_free_chiral_clock():
    # Established single-site exact identities: H=(I-9Pi)/2 and
    # O=[Re(X_1),Re(Z_1)]/(2i), [H,O]=0, O spectrum 0,+/-3sqrt2/8.
    om=np.exp(2j*np.pi/3)
    x=np.roll(np.eye(3),1,axis=0).astype(complex)
    z=np.diag([1,om,om**2])
    Rx=(x+x.conj().T)/2; Rz=(z+z.conj().T)/2
    O=np.kron((Rx@Rz-Rz@Rx)/(2j),np.eye(3))
    parity=np.zeros((9,9),dtype=complex)
    for a,b in product(range(3),repeat=2):
        parity[3*(-a%3)+(-b%3),3*a+b]=1
    H=(np.eye(9)-9*parity)/2
    assert np.allclose(H@O,O@H,atol=1e-11)
    assert np.allclose(parity@O@parity,O,atol=1e-11)
    assert np.allclose(O.conj(),-O,atol=1e-11)
    assert np.allclose(O@O@O-9/32*O,0,atol=1e-11)
    P=(np.eye(9)+parity)/2
    Oground=P@O@P
    a2=9/32
    eig=np.linalg.eigvalsh(Oground)
    assert np.allclose(eig,[-math.sqrt(a2)]*2+[0]*5+[math.sqrt(a2)]*2,atol=1e-9)
    # N-copy, all-to-all H_N=sum_i H_i - J/N*(sum_i O_i)^2
    # has a rigorous operator bound E>=-4N - J*a²*N,
    # saturated by products of the local ground joint eigenstates O=±a.
    # Ground degeneracy exactly 2*(2^N) (two local polarizations per sign).
    checks=[]
    for N in range(1,9):
        Emin=-4*N-a2*N
        degeneracy=2*(2**N)
        # Spectral energy if one ground-state local O=0 and remaining O=a.
        Eone=-4*N-a2*(N-1)**2/N
        assert Eone>Emin
        checks.append({"replicas":N,"exact_ground_energy":Emin,
                       "ground_degeneracy":degeneracy,
                       "single_zero_charge_excitation_gap":Eone-Emin})
    return {"status":"EXACT_SOURCE_FREE_K_SYMMETRIC_DEGENERATE_CHIRAL_SECTORS",
      "H_N":"sum_i H_i - (J/N)(sum_i O_i)^2, J=1",
      "K_symmetry":"antiunitary computational conjugation on every qutrit, K H_N K^-1=H_N",
      "O":"[Re(X_1),Re(Z_1)]/(2i)",
      "O_minimal_polynomial":"O(O^2-9/32 I)=0",
      "single_site_ground_projected_eigenvalues":"0 (one), +/-3sqrt2/8 (two each)",
      "exact_general_N_E_ground":"E0(N)=-4N-(9/32)N",
      "exact_general_N_ground_degeneracy":"2^(N+1), K exchanges all-plus and all-minus macroscopic sectors",
      "finite_N_checks":checks,
      "scope":"Exact K-symmetric ferromagnetic mean-field toy Hamiltonian with infinitely ranged O_i O_j interactions and pre-existing finite-N exact degeneracy. It is NOT local or a demonstrated spontaneous time arrow; physical K is not established."}


def magic_factory_interface():
    pi=np.pi;zeta=np.exp(2j*pi/9)
    magic=np.array([1,zeta,zeta**2],dtype=complex)/math.sqrt(3)
    vac=np.array([1,0,0],dtype=complex)
    SUM=np.zeros((9,9),dtype=complex)
    for x,a in product(range(3),repeat=2):
        SUM[3*x+(a+x)%3,3*x+a]=1
    assert np.allclose(SUM.conj().T@SUM,np.eye(9))
    target=sum((zeta**i)*np.eye(9)[:,4*i] for i in range(3))/math.sqrt(3)
    assert np.allclose(SUM@np.kron(magic,vac),target)
    choices=[]
    for epsilon in (0,0.001,0.01,0.05,0.1):
        pure=np.outer(magic,magic.conj())
        mixed=(1-epsilon)*pure+epsilon*np.eye(3)/3
        bipartite=SUM@np.kron(mixed,np.outer(vac,vac))@SUM.conj().T
        F=np.real(np.vdot(target,bipartite@target))
        assert np.isclose(F,1-2*epsilon/3,atol=1e-12)
        assert np.isclose(np.trace(bipartite),1)
        choices.append({"raw_depolarizing_parameter":epsilon,
                        "Choi_resource_fidelity":float(F),
                        "upper_bound_output_trace_distance":float(math.sqrt(2*epsilon/3))})
    cert=bell_resource_injection()
    assert len(cert["outcomes"])==9
    return {"status":"EXACT_SINGLE_MAGIC_TO_CHOI_CLIFFORD_PREPARATION_AND_NOISE_BUDGET",
       "input_resource":"|M+>=(|0>+zeta9|1>+zeta9^2|2>)/sqrt3",
       "Clifford_conversion":"SUM on |M+>|0> gives (I tensor M)|Phi_3>",
       "Bell_injection":"one Bell measurement, nine equiprobable branches, Clifford feedback",
       "raw_depolarizing_model":"rho=(1-eps)|M+><M+|+eps I/3",
       "Choi_F":"1-2eps/3",
       "output_trace_DISTANCE_upper_bound":"sqrt(2eps/3) assuming perfect Clifford preparation/measurement/corrections; Fuchs-van-de-Graaf",
       "noise_samples":choices,
       "magic_distillation":False,"logical_error_threshold":False,
       "boundary":"Exact resource conversion and a conservative error budget; raw magic is assumed available, not distilled or prepared physically."}


def kinetic_gap_obstruction():
    examples=[]
    for q in (3,4,8,9):
        g=make_geometry(q)
        n=g["n"];k=q*(q+1)
        A=(1-np.eye(n,dtype=np.int8)-g["B"]).astype(np.float64)
        assert np.all(A.sum(axis=1)==k)
        gap=1-(q-1)/k
        # W(3,q) SRG(q,q) has eigenvalues k, q-1, -(q+1).
        # L=I-A/k is PSD and has gap exactly 1-(q-1)/k.
        rng=np.random.default_rng(20261023+q)
        for _ in range(5):
            v=rng.standard_normal(n)
            v-=np.mean(v)
            rayleigh=(v@v-(v@A@v)/k)/(v@v)
            assert rayleigh >= gap - 1e-9
        # For D_u,D_v PSD and constant-vector annihilators,
        # L+epsilon(D_u+D_v) retains the same lower bound on 1^perp.
        for strength in (0,0.1,1):
            w=np.array([1,0,0,0],dtype=np.int16)
            v=np.array([0,1,0,0],dtype=np.int16)
            P=g["trans"](w,1);Q=g["trans"](v,1)
            y=rng.standard_normal(n);y-=y.mean()
            D_y=(4*y-y[P]-y[np.argsort(P)]-y[Q]-y[np.argsort(Q)])
            assert np.dot(y,D_y)>=-1e-8
            total=(y@y-y@A@y/k+strength*(y@D_y))/(y@y)
            assert total>=gap-1e-9
        examples.append({"q":q,"n":n,"degree":k,
                         "normalized_L_gap_lower_bound":gap,
                         "fraction_of_eigenvalues_in_(0,gap)":0,
                         "exact_nonzero_L_eigenvalues":[gap,1+1/q]})
    return {"status":"ALL_Q_THEOREM_POSITIVE_ANCHOR_DEFECTS_CANNOT_CLOSE_NORMALIZED_W33_GAP",
       "operator":"L_q=I-A_q/[q(q+1)] + eps(D_u+D_v), eps>=0",
       "gap_bound":"lambda_2(L_q)>=1-(q-1)/[q(q+1)], tending to 1 as q grows",
       "proof":"Strongly regular W(3,q) adjacency has k=q(q+1), r=q-1, s=-q-1; 1perp Poincare bound. D_u,D_v=2I-T-T^-1 are PSD and annihilate constants. Positive addition preserves Poincare gap.",
       "examples":examples,
       "boundary":"Restricted natural normalized positive-graph kinetic/defect model cannot yield gapless low-energy Weyl limit without altered scaling/dynamics; does not disprove all continuum theories or signed H_sparse."}


def run():
    return {"schema":"w33.20261023.round7.v1",
      "frobenius":frobenius_obstruction_witnesses(),
      "chirality":source_free_chiral_clock(),
      "magic":magic_factory_interface(),
      "continuum":kinetic_gap_obstruction()}


if __name__=="__main__":
    import sys
    raw=json.dumps(run(),indent=2)+"\n"
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(raw,encoding="utf-8")
    else:print(raw,end="")
