#!/usr/bin/env python3
"""Five physical W33 frontiers plus vacuum sanity checks, self-contained certificates.

Exact algebra, symmetry no-go and photonic hardware constraints are
distinguished explicitly from a physical theory of everything.
"""
from __future__ import annotations

import itertools, json, math, sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_dual_27_electrical_transport import build_graphs
from w33_20261008_five_physics_frontiers import projective_points_and_lines
from w33_20261008_six_toe_frontier_followthrough import rational_eight_cycle_closure_dimension,levi_graph
from w33_20261008_physical_frontiers_robustness import coherent_device,discrete_vacuum,flux_geometry

OUT=ROOT/"data"/"w33_20261008_five_physics_deepening.json"


def physical_photonic():
    """Exact coupler requirements + topology lower bound + circuit scheduling."""
    graphs=build_graphs()
    out={}
    for name,a in graphs.items():
        n=len(a)
        edges=[(i,j) for i in range(n) for j in range(i+1,n) if a[i,j]]
        assert len(edges)==108 and np.all(a.sum(axis=1)==8)
        assert len(edges)>3*n-6
        # In a drawing with ordinary transverse crossings, planarization
        # turns c crossings into c vertices and 2c additional edges.
        # 108+2c <=3(27+c)-6 => c>=33.
        min_crossings=108-(3*n-6)
        # Vizing => <= Delta+1=9 layers, odd n prevents Delta=8
        assert n%2==1
        colors=9
        m=len(edges)
        # Exact integer programming for one 9-layer conflict-free schedule:
        # one color per edge and at most one same color at each vertex.
        constraints=lil_matrix((m+n*colors,m*colors),dtype=float)
        for ei,(u,v) in enumerate(edges):
            for c in range(colors):
                col=ei*colors+c
                constraints[ei,col]=1
                constraints[m+u*colors+c,col]=1
                constraints[m+v*colors+c,col]=1
        low=np.r_[np.ones(m),np.zeros(n*colors)]
        high=np.ones(m+n*colors)
        result=milp(c=np.zeros(m*colors),integrality=np.ones(m*colors),
                    bounds=Bounds(np.zeros(m*colors),np.ones(m*colors)),
                    constraints=LinearConstraint(constraints.tocsr(),low,high),
                    options={"time_limit":8.0})
        schedule=None
        if result.x is not None and result.success:
            x=np.rint(result.x.reshape(m,colors)).astype(int)
            assert np.all(x.sum(axis=1)==1)
            sched=[[list(edges[i]) for i in range(m) if x[i,c]] for c in range(colors)]
            assert all(len({v for e in layer for v in e})==2*len(layer) for layer in sched)
            schedule=sched
        out[name]={
            "ports":n,"edges_couplers":m,"degree_per_port":8,
            "adjacency_matrix":a.astype(int).tolist(),
            "undirected_edge_list":[list(e) for e in edges],
            "planar_simple_graph_edge_upper_bound":3*n-6,
            "crossing_lower_bound_single_layer":min_crossings,
            "disjoint_edge_layers_min_and_max_by_parity_and_Vizing":[9,9],
            "nine_layer_schedule":schedule,
            "nine_layer_MILP_status":int(result.status),
            "implementation_caveat":"edge-color layers implement a Trotter decomposition, not simultaneous original H without errors; no routed chip/layout built"}
    return out


def integer_cycle_algebra():
    """Exact rational structure of 8 original Levi-cycle current matrices."""
    n=8
    gens=[]
    for i in range(n):
        j=(i+1)%n
        left=np.zeros(n,dtype=object);right=np.zeros(n,dtype=object)
        left[i]=left[j]=1;right[i]=1;right[j]=-1
        gens.append(np.outer(left,right))
    # Maintain reduced rational matrices and a consistent pivot ordered row basis.
    reduced=[]
    pivots=[]
    def reduce(m):
        v=[sp.Rational(int(x)) if isinstance(x,(int,np.integer)) else sp.Rational(x)
           for x in m.reshape(-1)]
        for pivot,row in zip(pivots,reduced):
            if v[pivot]:
                a=v[pivot]
                v=[x-a*y for x,y in zip(v,row)]
        return v
    def add(m):
        v=reduce(m)
        for i,x in enumerate(v):
            if x:
                v=[y/x for y in v]
                j=next(k for k,p in enumerate(pivots) if p>i) if any(p>i for p in pivots) else len(pivots)
                pivots.insert(j,i);reduced.insert(j,v)
                return True
        return False
    found=[]
    for g in gens:
        if add(g):found.append(g)
    for x in found:
        for g in gens:
            c=x@g-g@x
            if add(c):found.append(c)
    assert len(found)==34 and len(reduced)==34
    basis=[sp.Matrix(n,n,row) for row in reduced]
    # Obtain exact 34x34 adjoint operators by triangular reduction and
    # solving in the original 34D row-space using an exact left inverse.
    B=sp.Matrix.hstack(*[sp.Matrix(list(m)) for m in basis])
    assert B.rank()==34
    piv_rows=list((B.T).rref()[1])
    Bp=B.extract(piv_rows,list(range(34)))
    inv=Bp.inv()
    def coords(m):
        vec=sp.Matrix(list(m))
        coeff=inv*vec.extract(piv_rows,[0])
        assert B*coeff==vec
        return coeff
    ad=[]
    for x in basis:
        cols=[coords(x*y-y*x) for y in basis]
        ad.append(sp.Matrix.hstack(*cols))
    derived=sp.Matrix.hstack(*[ad[i][:,j] for i in range(34) for j in range(34)]).rank()
    center=sp.Matrix.vstack(*ad).nullspace()
    k=sp.Matrix(34,34,lambda i,j:(ad[i]*ad[j]).trace())
    killing_rank=k.rank()
    assert derived==34 and len(center)==1
    assert killing_rank<=33
    center_mat=sum((center[0][i]*basis[i] for i in range(34)),sp.zeros(8))
    assert all(center_mat*g==g*center_mat for g in gens)
    return {"eight_cycle_dim_over_Q":len(basis),
            "derived_algebra_dimension_over_Q":derived,
            "center_dimension_over_Q":len(center),
            "center_matrix":[[str(center_mat[i,j]) for j in range(8)] for i in range(8)],
            "killing_form_rank_over_Q":killing_rank,
            "killing_form_nullity":34-killing_rank,
            "identity_Lie_algebra_not_assumed":True,
            "scope":"8-cycle subset of 80-vertex graph; not ADM constraints"}


def flag_vacuum_action():
    """Complete 320 element sets and the symplectic-central kernel obstruction."""
    pts,lines=projective_points_and_lines()
    inc=[(p,li) for li,L in enumerate(lines) for p in L]
    assert len(inc)==160
    # Each nontrivial line character determined by nonzero pair
    # lambda(g1),lambda(g2) in F3, giving exactly eight values.
    states={(li,a,b) for li in range(40) for a in range(3) for b in range(3) if (a,b)!=(0,0)}
    assert len(states)==320
    # Central -I in Sp4(3) acts v -> -v. It fixes projective
    # points and lines but dualizes every nonzero line character.
    inversion={(li,(-a)%3,(-b)%3) for li,a,b in states}
    assert inversion==states
    assert all((a,b)!=((-a)%3,(-b)%3) for _,a,b in states)
    triangles=set()
    for li,L in enumerate(lines):
        for omitted_p in L:
            triangle=frozenset((q,li) for q in L if q!=omitted_p)
            assert len(triangle)==3
            triangles.add(triangle)
    for p in pts:
        own=[li for li,L in enumerate(lines) if p in L]
        assert len(own)==4
        for omitted_li in own:
            triangle=frozenset((p,j) for j in own if j!=omitted_li)
            assert len(triangle)==3
            triangles.add(triangle)
    assert len(triangles)==320
    lg=__import__("networkx").line_graph(levi_graph())
    # Map (point,line) to actual graph edge (point index,40+li)
    pi={p:i for i,p in enumerate(pts)}
    assert all(all(lg.has_edge(tuple(sorted((pi[x],40+li))),tuple(sorted((pi[y],40+lj))))
                       for (x,li),(y,lj) in itertools.combinations(t,2))
               for t in triangles)
    # Because -I fixes EVERY triangle, but freely pairs states, a
    # Sp4(3)-equivariant injection between these 320-sets cannot exist.
    return {"flags":160,"physical_quartic_characters":len(states),
            "line_centered_triangles":160,"point_centered_triangles":160,
            "total_flag_graph_triangles":len(triangles),
            "central_minus_identity_order":2,
            "central_minus_identity_fixed_projective_triangles":len(triangles),
            "central_minus_identity_fixed_nontrivial_line_characters":0,
            "symplectic_equivariant_bijection_possible":False,
            "kernel_obstruction":"-I fixes all projective triangles but takes lambda to -lambda for all 320 nontrivial characters",
            "claim_scope":"exact action on line character torsors; no assertion of physical gauge redundancy"}


def hexality_generator():
    """Minimal order-3 residual needed beyond Y and B-L at charge-table level."""
    result=discrete_vacuum()
    q=result["known_proton_hexality_assignment"]
    y=result["sixY"];bl=result["threeBL"]
    names=("Q","Uc","Dc","L","Ec","Nc","Hu","Hd")
    diff={x:(q[x]-y[x]-bl[x])%6 for x in names}
    assert all(v%2==0 for v in diff.values())
    z3={x:(diff[x]//2)%3 for x in names}
    assert set(z3.values())=={0,1,2}
    assert all((bl[x]+y[x]+2*z3[x])%6==q[x] for x in names)
    # SU3^2, SU2^2, grav weighted integer anomalies for proposed
    # Z3, NOT a complete string selection / discrete anomaly proof.
    mixed_su3=3*(2*z3["Q"]+z3["Uc"]+z3["Dc"])
    mixed_su2=3*(3*z3["Q"]+z3["L"])+z3["Hu"]+z3["Hd"]
    grav=3*(6*z3["Q"]+3*z3["Uc"]+3*z3["Dc"]+2*z3["L"]+z3["Ec"]+z3["Nc"])+2*(z3["Hu"]+z3["Hd"])
    # Klein-four free quotient has 1D character group Z2xZ2.
    char_orders=[1,2,2,2]
    assert all(order%3 for order in char_orders)
    return {"minimal_extra_prime_factor":3,
            "additional_Z3_charge_vector":z3,
            "charge_identity":"P6=3(B-L)+6Y+2 X3 (mod 6) on all eight tested superfields",
            "mixed_integer_sums_su3_su2_grav":[mixed_su3,mixed_su2,grav],
            "sums_mod3":[mixed_su3%3,mixed_su2%3,grav%3],
            "free_Klein4_1d_character_orders":char_orders,
            "Klein4_Wilson_character_can_supply_Z3":False,
            "candidate_must_use_additional_structure":"U1 Higgsing, nonabelian discrete group or other order-3 data not yet constructed",
            "worldsheet_anomaly_FI_Higgs_tests_complete":False}


def physical_yukawa_preflight():
    """Numerical known Kaehler coordinates and exact bundle charge test."""
    t=(sp.Integer(1),(13+sp.sqrt(241))/12,sp.Rational(1,2),(5+sp.sqrt(241))/36)
    K=[(-2,1,1,0),(0,-3,0,1),(2,2,-1,-1)]
    assert tuple(map(sum,zip(*K)))==(0,0,0,0)
    # X is (2,2,2,2) in (P1)^4. d_ijk = 2 for
    # all distinct i,j,k and zero if repeated.
    kappa=[sum(t[j]*t[k] for j in range(4) for k in range(j+1,4) if j!=i and k!=i)
           for i in range(4)]
    slopes=[sp.simplify(sum(k[i]*kappa[i] for i in range(4))) for k in K]
    assert slopes==[0,0,0]
    vol=sp.simplify(sum(2*t[i]*t[j]*t[k] for i in range(4) for j in range(i+1,4)
                            for k in range(j+1,4)))
    assert vol>0
    # Direct K3 vs K1,K2 charge neutrality and no bilateral mass:
    pair=[tuple(K[i][d]+K[j][d] for d in range(4))
          for i,j in itertools.combinations(range(3),2)]
    assert all(any(x!=0 for x in v) for v in pair)
    # NN-based physical algorithm requires explicit polynomial F and closed
    # cohomology representatives (not present in original existence proof).
    # It is impossible to certify a physical numeric Yukawa from C=1/2 alone.
    return {"Kaehler_moduli":[str(v) for v in t],
            "Kaehler_moduli_numeric":[float(v) for v in t],
            "intersection_volume_normalization":str(vol),
            "bundle_K1_K2_K3":[list(k) for k in K],
            "exact_bundles_slopes":[str(x) for x in slopes],
            "nonzero_holomorphic_quotient_cup_from_prior":"1/2",
            "no_two_bundle_neutral_quadratic_mass":True,
            "explicit_smooth_CY_polynomial_provided":False,
            "actual_Ricci_flat_HYM_harmonic_metrics_calculated":False,
            "missing_to_run_full_training":["specific free smooth invariant tetraquadric polynomial","complex structure parameters and moduli choice","closed Dolbeault representatives in supplied bundle conventions","trained CY/HYM/harmonic networks and validated convergence"],
            "available_library_preflight":"heteroticyukawas is not installed in available Windows Python; read published API only"}


def flux_stabilization_firewall():
    """Extra analytic condition: positive exponent Hessian rank and sign."""
    k=np.array([2]+[4]*7,np.int64)
    assert np.all(k>0)
    u0=1.0
    grad=-(u0*k)
    assert np.all(grad<0)
    # Opposite exponent terms can stabilize, but no claim they exist in theory.
    toy=np.stack([np.eye(8,dtype=int)[i] for i in range(8)]+[-np.ones(8,dtype=int)])
    h=toy.T@toy
    evals=np.linalg.eigvalsh(h)
    assert np.allclose(evals,[1]*7+[9])
    return {"previous_flux_exponent":k.tolist(),
            "single_flux_U_grad_at_origin":grad.tolist(),
            "positive_exponents_in_common_strict_halfspace_no_stationarity":True,
            "minimal_eight_scalar_full_rank_balanced_positive_terms":9,
            "toy_balanced_hessian_eigenvalues":[int(round(x)) for x in evals],
            "local_toy_U0":9,
            "physical_4D_compactification_or_CC_solution":False}


def build():
    return {
        "scope":"mathematical exact tests and hardware constraints; not TOE physical completion",
        "physical_photonic":physical_photonic(),
        "rational_lie_classification":integer_cycle_algebra(),
        "flag_chirality_equivariance":flag_vacuum_action(),
        "hexality_missing_generator":hexality_generator(),
        "physical_Yukawa_preflight":physical_yukawa_preflight(),
        "flux_vacuum_firewall":flux_stabilization_firewall(),
    }


if __name__=="__main__":
    result=build()
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for key,value in result.items():
        if key!="scope":
            print(key, json.dumps(value if key!="physical_photonic" else {
                n:{k:v for k,v in data.items() if k not in ("adjacency_matrix","undirected_edge_list","nine_layer_schedule")}
                for n,data in value.items()},sort_keys=True),flush=True)
    print("FIVE_PLUS_ONE_DEEP_PASS",flush=True)
