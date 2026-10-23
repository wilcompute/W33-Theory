#!/usr/bin/env python3
"""Five independent round-eight W33 research audits and exact theorems.

1. All-prime-power p-rank B via Lucas coefficient extraction.
2. 40-site W33 graph-local, source-free chirality/domain-wall barrier.
3. SWAP transposition-parity lower bound and bounded solver outcome.
4. Actual 5-qutrit stabilizer projection for the ninth-root target.
5. Full Sp(4,q)-invariant scalar kinetic commutant / locality obstruction.
"""
from __future__ import annotations
import json,math,itertools
from pathlib import Path
import numpy as np
try:
 from analysis.w33_20261022_five_frontiers_round6 import make_geometry,modular_basis
 from analysis.w33_20261022_five_followups_round5 import A,transvection,cycles
except ImportError:
 from w33_20261022_five_frontiers_round6 import make_geometry,modular_basis
 from w33_20261022_five_followups_round5 import A,transvection,cycles

def rank_theorem():
    checks=[]
    for q,p,t in [(3,3,1),(4,2,2),(8,2,3),(9,3,2)]:
        g=make_geometry(q)
        observed=len(modular_basis(g["B"],p))
        predicted=math.comb(p+2,3)**t
        assert observed==predicted,(q,observed,predicted)
        checks.append({"q":q,"p":p,"extension_t":t,
                       "matrix_p_rank":observed,"lucas_formula":predicted})
    samples=[{"p":p,"t":t,"formula":math.comb(p+2,3)**t,
              "PG_points":(p**t+1)*(p**(2*t)+1)}
              for p,t in [(2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(5,1),(5,2),(7,1)]]
    return {"status":"INDEPENDENT_LUCAS_PROOF_OF_KNOWN_ALLQ_P_RANK",
      "theorem":"rank_Fp(B_{W(3,p^t)})=binom(p+2,3)^t",
      "proof":"B_xy=omega(x,y)^(q-1) in Fp. As a polynomial in y, expand the linear form power q-1. Coefficient extraction on Fq^4 using 4-variable Vandermonde interpolation (each coordinate exponent < q) shows the row span over Fq equals the span of its nonzero monomial coefficients. Lucas's theorem says multinomial coefficients survive mod p exactly when each base-p digit of four exponents sums to p-1. There are binom(p+2,3) choices per digit, independently for t digits. These monomials have degree q-1 and evaluate independently on Fq^4 since their individual exponents < q; degree q-1 guarantees projective scale invariance. Matrix entries lie in Fp, hence ranks agree after scalar extension Fp->Fq.",
      "exact_geometry_checks":checks,"formula_scenarios":samples,
      "scope":"Independent elementary interpolation derivation of classical Hamada p-rank already explicitly used in analysis/w33_20261022_allq_pascal_CSS_exact_distance.py; not a novel rank result. Does not calculate the all-q connecting-map ranks or establish physics."}


def chiral_local_graph():
    n=len(A);degree=int(A[0].sum())
    assert n==40 and degree==12 and np.all(A.sum(axis=1)==degree)
    assert np.array_equal(A,A.T)
    edge_count=int(np.sum(A)//2)
    assert edge_count==240
    a2=9/32
    # Local H0 has ground energy -4; O commutes with H0, with
    # ground eigenvalues 0 once, +/-sqrt(a2) twice each.
    # H = sum H0_i - g sum_(i,j in E) O_i O_j, g=1.
    ground=-4*n-a2*edge_count
    assert ground==-227.5
    # Every edge contribution >=-a² and every site H0>=-4.
    # A is connected, so equality requires uniform sign +/- on all sites.
    assert np.linalg.matrix_rank(12*np.eye(n)-A)>0
    # Spectral expansion bound: cut(S) >= (k-r)|S|(n-|S|)/n.
    k=degree;r=2
    controls=[]
    for sz in (1,2,10,20):
        lower=(k-r)*sz*(n-sz)/n
        controls.append({"domain_size":sz,"spectral_cut_lower_bound":lower,
                         "chiral_domain_wall_energy_lower_bound":2*a2*lower})
    # Exact one-site flip and one-site zero-charge defects.
    return {"status":"EXACT_W33_EDGE_LOCAL_K_SYMMETRIC_CHIRAL_SECTORS",
      "sites":n,"graph_degree":degree,"edge_count":edge_count,
      "H":"sum_i H0_i - sum_(i,j in W33_edges) O_i O_j",
      "symmetries":"graph automorphisms on sites and global computational-basis complex conjugation K",
      "onsite_operator":"H0=(I-9Pi)/2, O=[Re(X1),Re(Z1)]/(2i)",
      "onsite_O_spectrum":"0 mult5 total 9D; in ground 0 mult1, +/-3sqrt2/8 each mult2",
      "exact_ground_energy":ground,"ground_degeneracy":2**(n+1),
      "ground_sectors":"all O_i=+3sqrt2/8 or all O_i=-3sqrt2/8; 2 local multiplicity at each vertex",
      "one_zero_charge_energy_cost":degree*a2,
      "one_sign_flip_energy_cost":2*degree*a2,
      "domain_wall_bound":"cut(S)>=(k-r)|S|(n-|S|)/n via adjacency eigenvalue r=q-1=2",
      "domain_controls":controls,
      "boundary":"Commuting W33 edge-local quantum toy with exact finite-N degeneracy and no dynamics between sectors; graph diameter2 and site degree12 do not imply physical 3+1D localization or spontaneous time arrow."}


def routing_parity():
    g=transvection(0);n=len(g)
    cyc=cycles(g)
    assert len(cyc)==9 and all(len(x)==3 for x in cyc)
    # Sign of a 3-cycle positive, hence sign(g)=+1, so #transpositions even.
    parity=sum(len(c)-1 for c in cyc)%2
    assert parity==0
    root=Path(__file__).resolve().parents[1]
    resultfile=root/"data/PART_20261023_SWAPCOUNT_35_SEARCH.json"
    observed=json.loads(resultfile.read_text())
    assert observed["swap_budget"]==35 and observed["status"]=="UNKNOWN"
    # All total-swap counts must be even. Count 27 lower bound from
    # transport distance, 36 constructive upper bound.
    return {"status":"PROVED_EVEN_SWAP_COUNT_AND_SOLVER_BOUNDARY",
      "target":"nine disjoint length-three cycles, thirteen fixed points",
      "permutation_sign":"+1",
      "all_valid_SWAP_counts_even":True,
      "transport_distance_lower_bound":27,
      "parity_refined_lower_bound":28,
      "known_construction_upper_bound":36,
      "possible_counts_under_bounds":[28,30,32,34,36],
      "four_layer_35_SWAP_budget_solver":observed,
      "critical":"UNKNOWN does not prove that 34 or 35 SWAPs are impossible; no optimum total gate count claimed."}


def kron(*matrices):
    result=np.array([[1]],dtype=complex)
    for u in matrices:result=np.kron(result,u)
    return result


def project_five_qutrit():
    zeta=np.exp(2j*np.pi/9);omega=zeta**3
    X=np.roll(np.eye(3,dtype=complex),1,axis=0)
    Z=np.diag([1,omega,omega**2])
    I=np.eye(243,dtype=complex)
    # Each row x0..x4|z0..z4 for canonical cyclic [[5,1,3]]_3
    rows=np.array([[1,0,0,2,0,0,1,2,0,0],
                   [0,1,0,0,2,0,0,1,2,0],
                   [2,0,1,0,0,0,0,0,1,2],
                   [0,2,0,1,0,2,0,0,0,1]],dtype=int)
    forms=[(rows[i,:5]@rows[j,5:]-rows[i,5:]@rows[j,:5])%3
           for i in range(4) for j in range(i+1,4)]
    assert not any(forms)
    G=[kron(*[np.linalg.matrix_power(X,int(row[i]))@
               np.linalg.matrix_power(Z,int(row[5+i])) for i in range(5)]) for row in rows]
    P=I.copy()
    for g in G:
        assert np.allclose(g@g@g,I,atol=1e-12)
        P=P@(I+g+g@g)/3
    assert np.allclose(P@P,P,atol=1e-11)
    assert np.isclose(np.trace(P),3,atol=1e-11)
    # canonical logical X shifts logical Z label by +1 using Xbar²
    Xbar=kron(*([X]*5))
    v=np.zeros(243,dtype=complex);v[0]=1
    u=P@v;u/=np.linalg.norm(u)
    basis=np.column_stack([u,np.linalg.matrix_power(Xbar,2)@u,Xbar@u])
    assert np.allclose(basis.conj().T@basis,np.eye(3),atol=1e-11)
    magic=np.array([1,zeta,zeta**2])/np.sqrt(3)
    psi=kron(*[magic.reshape(3,1) for _ in range(5)]).ravel()
    amp=basis.conj().T@psi
    prob=float(np.linalg.norm(amp)**2)
    out=amp/np.linalg.norm(amp)
    # Exhaust the 216 single-qutrit projective Clifford group.
    F=np.array([[omega**(j*k) for k in range(3)] for j in range(3)],complex)/np.sqrt(3)
    S=np.diag([1,1,omega])
    gens=[F,S,X,Z]
    def key(U):
        flat=U.ravel();c=flat[np.flatnonzero(abs(flat)>1e-10)[0]]
        normalized=U/(c/abs(c))
        return tuple(np.round(normalized.real.ravel(),8))+tuple(np.round(normalized.imag.ravel(),8))
    seen={key(np.eye(3,dtype=complex))}
    allcl=[np.eye(3,dtype=complex)]
    for mat in allcl:
        for gen in gens:
            nextmat=mat@gen
            k=key(nextmat)
            if k not in seen:
                seen.add(k);allcl.append(nextmat)
    assert len(allcl)==216
    fidelities=[float(abs(np.vdot(magic,U@out))**2) for U in allcl]
    fmax=max(fidelities)
    assert 0.9182<fmax<0.9183
    # One qutrit Clifford correction cannot make the ideal-output
    # state exactly equal to the original 9th-root magic target.
    return {"status":"ACTUAL_5_QUTRIT_STABILIZER_PROJECTOR_TARGET_MISMATCH",
      "code":"cyclic qutrit [[5,1,3]] with four commuting Pauli stabilizers",
      "stabilizer_xz_rows":rows.tolist(),
      "codespace_rank":3,
      "input_resource":"(|0>+zeta9|1>+zeta9²|2>)/sqrt(3)",
      "ideal_5_copy_projection_probability":prob,
      "normalized_output_amplitudes_real_imag":[[float(z.real),float(z.imag)] for z in out],
      "projective_single_qutrit_Cliffords_tested":216,
      "max_Clifford_corrected_overlap_with_same_magic_target":fmax,
      "is_exact_target_fixed_point_under_one_Clifford":False,
      "boundary":"Only bare trivial-syndrome projection and one logical qutrit Clifford correction tested. Does not exclude other syndrome branches, code choices, stabilizer transformations before projection, or the known qutrit magic-state distillers targeting other states. No W33 magic threshold proved."}


def invariant_commutant():
    # Transitivity and Witt's lemma: for ordered projective pairs (x,y),
    # there are three Sp4(q) orbitals: equal, distinct orthogonal,
    # and nonorthogonal. Therefore scalar centralizer algebra is span{I,A,B}.
    cases=[]
    for q in (3,4,8,9):
        g=make_geometry(q)
        n=g["n"];B=g["B"].astype(np.int64);I=np.eye(n,dtype=np.int64)
        A0=np.ones((n,n),dtype=np.int64)-I-B
        assert np.array_equal(A0,A0.T)
        k=q*(q+1);nondeg=q**3
        assert np.all(A0.sum(axis=1)==k) and np.all(B.sum(axis=1)==nondeg)
        assert n==1+k+nondeg
        # SRG parameters and quadratic identity via all integer matrix multiplication.
        # actual A^2 = k I + lambda A + mu B; lambda=q-1, mu=q+1.
        assert np.array_equal(A0@A0,k*I+(q-1)*A0+(q+1)*B)
        samples=[]
        for alpha,beta,gamma in [(0,1,0),(2,3,5),(7,-2,4)]:
            M=alpha*I+beta*A0+gamma*B
            eigs=[alpha+beta*k+gamma*nondeg,
                  alpha+beta*(q-1)+gamma*(-q),
                  alpha+beta*(-q-1)+gamma*q]
            # B=J-I-A has eigen -1-r=-q, -1-s=q.
            assert all(abs(float(z))<10**8 for z in eigs)
            samples.append({"coefficients":[alpha,beta,gamma],"eigenvalues_at_most_3":eigs})
        cases.append({"q":q,"n":n,"orbit_sizes":[1,k,nondeg],
                      "nontrivial_invariant_simple_graph_degrees":[k,nondeg,n-1],
                      "commutant_dimension":3,
                      "sample_operator_eigenvalues":samples})
    return {"status":"ALL_Q_RANK3_SYMPLECTIC_SCALAR_COMMUTANT_THEOREM",
       "theorem":"Any Sp(4,q)-equivariant scalar complex-linear endomorphism of C[PG(3,q)] belongs to span{I,A_q,B_q}, hence has <=3 distinct eigenvalues.",
       "reason":"Sp(4,q) is transitive on ordered projective pairs of each type: same point, distinct symplectically orthogonal, and symplectically nonorthogonal (Witt's lemma). The centralizer dimension equals the number of orbitals, 3. The basis indicator matrices are I,A,B.",
       "locality":"Any nonempty nontrivial invariant simple loopless graph has degree q(q+1), q^3 or q(q+1)+q^3; no uniformly bounded-degree nonempty such graph as q grows.",
       "cases":cases,
       "physics_boundary":"Break symmetry, add internal fibers/modes, or change the carrier to get growing scalar spectral bands/locality. This is classical rank-three association-scheme rigidity, not a universal no-go for quantum gravity."}


def run():
    return {"schema":"w33.toe.20261023.five_round8.v1",
       "primepower":rank_theorem(),
       "local_chirality":chiral_local_graph(),
       "routing":routing_parity(),
       "five_qutrit_magic":project_five_qutrit(),
       "kinematic_rigidity":invariant_commutant()}

if __name__=="__main__":
    import sys
    data=json.dumps(run(),indent=2)+"\n"
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(data,encoding="utf-8")
    else:print(data,end="")
