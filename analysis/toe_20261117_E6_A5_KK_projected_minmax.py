"""Independent A5/W33 weak-context orbit and KK variational obstruction.

Audits the existing 10 W(3,3) special measurement contexts <-> 10 weak
two-subsets of the five E6 skew-frame transversals, and derives an EXACT
graph/orbit obstruction to unique symmetry-invariant selection.

The equal-flux physical KK negative subspace has a stronger
Courant-Fischer certificate: only its diagonal Rayleigh block must be
negative. Off-block physical mixing with other modes can be arbitrarily
large without removing all negative modes, PROVIDED the transported
negative subspace is in the correct positive-norm, gauge-constrained
domain and the whole quadratic mass operator is self-adjoint.
"""
import itertools,json,math
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_E6_A5_context_KK_Rayleigh_certificate.json"

def even(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2==0

def context_orbit():
    labels=tuple(range(5))
    contexts=list(itertools.combinations(labels,2))
    G=[p for p in itertools.permutations(labels) if even(p)]
    assert len(G)==60 and len(contexts)==10
    parallel=json.loads((ROOT/'data'/'w33_pass12683_doublet_triplet_contexts.json').read_text(encoding='utf8'))
    assert parallel['special_contexts']==parallel['distinct_weak_pairs']==10
    assert parallel['weak_factorisations_product_basis']
    assert parallel['colour_factorisations_maximally_entangled']
    labels_index={pair:i for i,pair in enumerate(contexts)}
    action=[]
    for p in G:
        a=[labels_index[tuple(sorted([p[i],p[j]]))] for i,j in contexts]
        action.append(tuple(a))
    assert len(set(action))==60  # faithful A5 action on the 10 choices
    for j in range(10):
        assert len({a[j] for a in action})==10
        assert sum(a[j]==j for a in action)==6
    J=sp.Matrix(10,10,lambda i,j: int(i!=j and len(set(contexts[i])&set(contexts[j]))==1))
    K=sp.ones(10)-sp.eye(10)-J
    assert all(sum(J.row(i))==6 for i in range(10))
    assert all(sum(K.row(i))==3 for i in range(10))
    assert J.eigenvals()=={sp.Integer(6):1,sp.Integer(1):4,sp.Integer(-2):5}
    assert K.eigenvals()=={sp.Integer(3):1,sp.Integer(1):5,sp.Integer(-2):4}
    for a in action:
        P=sp.zeros(10,10)
        for j,i in enumerate(a): P[i,j]=1
        assert P.T*J*P==J and P.T*K*P==K
    return {
      "status":"PASS_A5_WEAK_PAIR_CONTEXT_PETERSEN_ORBIT",
      "source_parallel_context_certificate":"data/w33_pass12683_doublet_triplet_contexts.json: ten special contexts biject ten weak two-subsets of five common transversals",
      "A5_order":60,"number_of_weak_pairs":10,"stabilizer_order_each":6,
      "entire_context_orbit_transitive":True,
      "intersection_graph_J_5_2":{"degree":6,"eigenvalue_multiplicities":{"6":1,"1":4,"-2":5},
                                    "permutation_module_irreps_dimensions":[1,4,5]},
      "disjointness_graph_Petersen":{"degree":3,"eigenvalue_multiplicities":{"3":1,"1":5,"-2":4}},
      "invariant_selection_no_go":"Every A5-invariant one-context energy function is constant on the 10 weak pairs. A unique chosen 2+3 split cannot follow from A5 alone; it requires explicit symmetry breaking, additional fields/data or spontaneous selection (with 10 equivalent choices before further effects).",
      "not_a_physical_proton_decay_calculation":True}

def minmax():
    # Negative Rayleigh block = 2 or 4 equal-flux KK harmonics in
    # a transported physically admissible subspace P.
    # For any offdiagonal mixing B, the restriction of H+4I to P
    # is negative definite. The full operator has at least dim(P)
    # negative eigenvalues below the AdS5 BF level.
    rows=[]
    rng=np.random.default_rng(20261117)
    for k in (2,4):
        for coupling in (0.0,0.1,5.0,100.0):
            n=k+5
            delta=1.0 if k==4 else 1.6628431434177413
            AA=(-4-delta)*np.eye(k)
            BB=coupling*rng.standard_normal((k,5))
            CC=(2+0.5*rng.standard_normal(5))*np.eye(5)
            H=np.block([[AA,BB],[BB.T,CC]])
            eig=np.linalg.eigvalsh(H)
            count=int(np.sum(eig<(-4-1e-9)))
            assert count>=k
            rows.append({"subspace_dim":k,"unbounded_offdiagonal_scale":coupling,
                         "negative_eigenvalues_below_BF":count,
                         "max_of_k_smallest_eigenvalues":float(eig[k-1])})
    # Exact Sylvester inertia proof with arbitrary rational B
    A=sp.diag(sp.Rational(-11,2),sp.Rational(-25,4)) # H_PP<-4
    B=sp.Matrix([[7,-3,11],[-9,2,10]])
    C=sp.diag(10,12,15)
    shift=A+4*sp.eye(2)
    # congruence to diag(shift,C-B.T*shift.inv()*B)
    assert all(v<0 for v in shift.diagonal())
    Schur=C+4*sp.eye(3)-B.T*shift.inv()*B
    assert all(Schur[:k,:k].det()>0 for k in range(1,4))
    # Stronger condition than ||H-H_equal|| control:
    # require only projected error sup on the negative subspace.
    return {"status":"PASS_BF_PROJECTED_RAYLEIGH_MINMAX_NO_OFFDIAGONAL_BOUND",
      "exact_inertia_example":{"negative_restricted_eigenvalues":[str(v) for v in shift.diagonal()],
                             "schur_complement_positive":True},
      "theorem":"For a canonically normalized self-adjoint physical KK operator H on a positive-definite Hilbert space and a k-dimensional gauge-admissible subspace P satisfying lambda_max(P H P)<-4, Courant-Fischer ensures at least k eigenvalues below -4, regardless of H mixing P with the complement.",
      "sufficient_flux_perturbation":"If H_equal|P<=(-4-Delta)I and lambda_max(P(H_unequal-H_equal)P)<Delta, at least k modes persist; no bound on off-diagonal P H Q is necessary.",
      "square_torus_k":4,"two_mode_modular_chamber_k":2,
      "equal_flux_square_gap":1.0169440813078374,
      "open_two_mode_chamber_uniform_gap_infimum":1.6628431434177413,
      "matrix_controls":rows,
      "physical_obstruction":"An actual constraint-compatible transport of P from the equal-flux background and the projected unequal-flux 11D metric-C3 quadratic form are not yet calculated. A scalar Laplacian proxy does not provide these.",
      "not_a_full_11d_spectrum":True}

def verify():
    a=context_orbit();b=minmax()
    return {"status":"PASS_E6_A5_KK_PROJECTED_RAYLEIGH_TWOFRONT", "A5_E6_context":a,"KK_projected_minmax":b}

if __name__=="__main__":
    x=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(x["status"])
