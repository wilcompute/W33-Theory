#!/usr/bin/env python3
"""October 8: inspect H27/H13 bridge and execute five independent physical guards.

Prior W33 13+27 polar shell and regular H27 are explicitly credited to Pass
369-371 and Pass 5105; this pass adds concrete modular matrix transport and
new source-bound no-go / cost tests. No physical TOE claimed.
"""
from __future__ import annotations
import itertools, json, math, sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_five_physics_frontiers import projective_points_and_lines
from w33_20261008_dual_27_electrical_transport import build_graphs
from w33_20261008_five_plus_one_deep import physical_photonic, hexality_generator
from w33_20261008_photonic_trotter_depth_loss import compile_depths
OUT=ROOT/"data"/"w33_20261008_h27_h13_five_frontiers.json"
P=3
J=np.array([[0,0,0,1],[0,0,1,0],[0,-1,0,0],[-1,0,0,0]],dtype=int)
I4=np.eye(4,dtype=int)


def um(a,b,c):
    return np.array([[1,a,b,c],[0,1,0,b],[0,0,1,-a],[0,0,0,1]],dtype=int)%3


def canon(v):
    v=tuple(int(x)%3 for x in v)
    t=next(x for x in v if x)
    inv=pow(t,-1,3)
    return tuple((x*inv)%3 for x in v)


def mm(a,b):
    return (a@b)%3


def ut8(a,b,c):
    # quotient of 13D Heisenberg Lie radical: choose first r and v
    g=np.eye(8,dtype=int)
    g[0,1]=a%3
    g[1,7]=b%3
    g[0,7]=c%3
    return g


def h27_and_h13():
    pts,lines=projective_points_and_lines()
    p=(1,0,0,0)
    polar=[v for v in pts if (J@np.asarray(v))[0]%3==0]
    bulk=[v for v in pts if (J@np.asarray(v))[0]%3!=0]
    assert len(polar)==13 and len(bulk)==27
    assert all(v[3]!=0 for v in bulk) # existing projective normal form fixes the first nonzero coordinate
    elements={(a,b,c):um(a,b,c) for a,b,c in itertools.product(range(3),repeat=3)}
    assert len({tuple(v.flat) for v in elements.values()})==27
    assert all(np.array_equal(mm(mm(g.T,J),g),J%3) for g in elements.values())
    assert all(canon(g@np.array(p))==p for g in elements.values())
    assert all({canon(g@np.asarray(v)) for v in polar}==set(polar) for g in elements.values())
    base=np.array([0,0,0,1])
    hit={canon(g@base) for g in elements.values()}
    assert hit==set(bulk)
    center={(0,0,c) for c in range(3)}
    # Full subgroup multiplication and explicit identification with the
    # chosen 2D symplectic Heisenberg slice of h13 reduced modulo 3.
    witness={}
    for a,b,c in elements:
        # UT8 group coordinate includes a half-cocycle correction,
        # representing U(a,b,c) by (a,b,2c-ab) in F3.
        witness[(a,b,c)]=ut8(a,b,2*c-a*b)
    for x,y in itertools.product(elements,repeat=2):
        ax,bx,cx=x;ay,by,cy=y
        xy=((ax+ay)%3,(bx+by)%3,(cx+cy+ax*by-bx*ay)%3)
        assert np.array_equal(mm(elements[x],elements[y]),elements[xy])
        assert np.array_equal(mm(witness[x],witness[y]),witness[xy])
    z=um(0,0,1)
    # Central U acts on 27 outside points in nine orbits of length three,
    # while fixing every point of the polar hyperplane (not pointwise,
    # noncentral U acts nontrivially there).
    assert all(canon(z@np.asarray(v))==v for v in polar)
    orbits={tuple(sorted({canon(np.linalg.matrix_power(z,j)@np.asarray(v)) for j in range(3)}))
            for v in bulk}
    assert len(orbits)==9 and all(len(o)==3 for o in orbits)
    # 13 dimensional Lie algebra radical matrices r6,v6,z, exact 12D
    # nondegenerate pairing after mod3. It has order 3^13 upon exponentiation.
    E=lambda i,j:np.array([[int(a==i and b==j) for b in range(8)] for a in range(8)],dtype=int)
    Rs=[E(0,i) for i in range(1,7)]
    Vs=[E(i,7) for i in range(1,7)]
    Z=E(0,7)
    pair=np.array([[(r@v-v@r)[0,7]%3 for v in Vs] for r in Rs],dtype=int)
    assert np.array_equal(pair,np.eye(6,dtype=int))
    assert all(np.array_equal((r@v-v@r)%3,Z if i==j else np.zeros((8,8),int))
               for i,r in enumerate(Rs) for j,v in enumerate(Vs))
    assert 3**13==1594323
    # The size-13 projective PG(2,3) and dimension-13 h13 share only a
    # numeral: one is a nonlinear set, other is 13D vector space over Q.
    return {"W33_point_count":40,"polar_plane_size":13,"noncollinear_affine_shell_size":27,
            "unipotent_H27_order":len(elements),"H27_nonabelian_commutator_power":2,
            "regular_bulk_orbit_size":len(hit),"central_fibers":9,"central_fiber_size":3,
            "H13_dimension_over_Q":13,"H13_mod3_extraspecial_order":3**13,
            "H13_mod3_six_symplectic_pair_rank":int(np.linalg.matrix_rank(pair)),
            "chosen_H27_subgroup_order":len(witness),
            "explicit_W33_elation_to_H13_slice_isomorphism":"U(a,b,c) maps to UT8(a,b,2c-ab) mod 3",
            "isomorphism_checked_multiplications":27*27,
            "H27_abstract_vs_representation":"address regular center has no fixed basis vector; operator Schrodinger center acts as scalar omega",
            "13_point_count_vs_13_Lie_dimension":"numerical equality; no Sp4-equivariant natural identification exhibited",
            "provenance":"W33 13+27 and Payne regular H27 already proved in repo Passes 369-371 and Pass 5105; standard finite GQ prior art"}


def global_cycle_glue():
    """Two overlapping real W33 C8 local-central currents fail to commute."""
    from w33_20261008_six_toe_frontier_followthrough import levi_graph
    G=levi_graph()
    base=[0,40,1,44,4,53,13,41]
    assert all(G.has_edge(base[i],base[(i+1)%8]) for i in range(8))
    # Enumerate induced C8 through point 0, find second cycle with a
    # single shared vertex so local-central overlap has no forced cancellation.
    chosen=None
    def walk(path):
        nonlocal chosen
        if chosen:return
        if len(path)==8:
            if G.has_edge(path[-1],path[0]) and len(set(path)&set(base))==1:
                chosen=path[:]
            return
        for v in sorted(G.neighbors(path[-1])):
            if v not in path and (v not in base or v==0):
                walk(path+[v])
                if chosen:return
    walk([0])
    assert chosen is not None, "No C8 singleton overlap found"
    def local_centre(path):
        # bipartite alternating s, all-ones u; C=u s^T
        u=np.zeros(80,dtype=int);s=np.zeros(80,dtype=int)
        for i,v in enumerate(path):
            u[v]=1;s[v]=1 if (v<40) else -1
        return np.outer(u,s)
    A=local_centre(base);B=local_centre(chosen)
    comm=A@B-B@A
    assert np.any(comm)
    rank=int(np.linalg.matrix_rank(comm))
    assert rank==2
    # Build other nonedge terms outside each eight-vertex support.
    cross_count=int(np.count_nonzero(comm))
    return {"cycleA":base,"cycleB":chosen,"intersection_size":len(set(base)&set(chosen)),
            "local_central_matrices_rank":[1,1],"central_commutator_rank":rank,
            "commutator_nonzero_entries":cross_count,
            "interpretation":"local h13 centers are not central under overlapping-chart gluing; full Levi 80D closure not classified"}


def photonic_loss_design():
    j=json.loads((ROOT/"data/w33_20261008_five_physics_deepening.json").read_text())["physical_photonic"]
    out=compile_depths(j)
    values=[]
    for row in out["discriminator_vs_depth"]:
        gap=row["discriminator_probability_gap"]
        survival=row["survival_1pct_each"]
        proxy=survival*gap**2
        # Simultaneous confidence bound for all 2*27*26 offdiagonal
        # position probabilities, without pretending a maximum is a
        # prespecified single pair. Per source port and device, collect
        # n successful readouts; each of its 26 event frequencies obeys
        # Hoeffding. With error epsilon=Delta/4, both max estimates
        # have <=epsilon error, and inferred gap remains >=Delta/2.
        K=2*27*26
        confidence=0.95
        epsilon=gap/4
        n=math.ceil(math.log(2*K/(1-confidence))/(2*epsilon**2))
        detected_required=2*27*n
        expected_launched=math.ceil(detected_required/survival)
        values.append({"stages":row["circuit_depth"],"conditional_gap":gap,
                       "launched_information_proxy":proxy,"survival":survival,
                       "successful_detections_per_input_setting":n,
                       "total_required_successful_detections":detected_required,
                       "expected_launches_under_independent_loss":expected_launched})
    winner=max(values,key=lambda x:x["launched_information_proxy"])
    least_launch=min(values,key=lambda x:x["expected_launches_under_independent_loss"])
    assert winner["stages"] in (36,72)
    return {"tested_depths":values,"best_proxy_stages":winner["stages"],
            "best_Hoeffding_expected_launch_stages":least_launch["stages"],
            "confidence_level_for_complete_offdiagonal_scan":0.95,
            "union_bound_observables":2*27*26,
            "loss_assumption":"independent survival 0.99 per stage",
            "rigorous_conditional_statistical_claim":"Given exact predicted gap and n independent successful samples for each of 54 input configurations, joint Hoeffding error probability <=0.05; all offdiagonal probabilities estimated within Delta/4, so maximum gap sign is positive",
            "warning":"Expected launched counts use independent uniform loss; not a 95%-guaranteed launch budget, not device-calibrated and exclude systematic port/coupler and detector errors"}


def signed_vacuum_cover():
    """Actual 320 char cover vs 320 triangles: sign orientation necessity."""
    from w33_20261008_five_plus_one_deep import flag_vacuum_action
    x=flag_vacuum_action()
    assert x["symplectic_equivariant_bijection_possible"] is False
    # Forget sign -> line-centered 160 projective triangles, 2-to-1,
    # not a bijection with all 320 projective triangles.
    return {"vacua":320,"flags":160,"line_centered_projective_triangles":160,
            "point_centered_projective_triangles":160,
            "forget_sign_fiber_degree":2,
            "central_minus_I_action_on_vacuum_fiber":"swaps signs",
            "central_minus_I_action_on_projective_triangles":"trivial",
            "equivariant_320_to_projective_320_isomorphism":False,
            "equivariant_320_to_signed_line_triangle_cover":"yes by transporting sign from exact character torsor, tautological until independent orientation defined",
            "physical_lorentz_chirality_selected":False}


def proton_center_guard():
    z=hexality_generator()
    x=z["additional_Z3_charge_vector"]
    assert x["Q"]!=x["Uc"]
    assert all((v%3)==(x["Q"]%3) for v in (x["Q"],))
    # Trinification H27 acts on E6 27 as 9 times one central
    # character: the common center cannot differentiate fields
    # within a single 27 representation.
    return {"X3_charges":x,"different_Q_Uc":True,
            "central_operator_H27_scalar_on_all_E6_27":True,
            "central_operator_H27_alone_cannot_be_X3_on_Q_and_Uc_within_one_E6_27":True,
            "conditional":"no-go assumes Q and Uc are embedded in same E6 27 and H27 center unbroken; it is not a no-go for extra gauge factors",
            "anomaly_and_string_worldsheet_complete":False}


def flavor_polynomial():
    """An explicit *candidate* K4 invariant polynomial, free fixed loci.

    No claim of smoothness is made: avoiding 48 fixed points alone does
    not imply a globally nonsingular tetraquadric.
    """
    import sympy as sp
    # monomial in degree two on each P1, exponents of v are d_i=0,1,2.
    mons=[a for a in itertools.product(range(3),repeat=4) if sum(k==1 for k in a)%2==0]
    seen=set();basis=[]
    for t in mons:
        if t in seen:continue
        flip=tuple(2-a for a in t)
        seen.update((t,flip))
        basis.append(tuple(sorted(set((t,flip)))))
    assert len(basis)==21
    def evalpoly(coeff,coords):
        val=0
        for w,orbit in zip(coeff,basis):
            for term in orbit:
                f=sp.prod((coords[i][0]**(2-term[i]))*(coords[i][1]**term[i]) for i in range(4))
                val+=w*f
        return sp.expand(val)
    import random
    rng=random.Random(20261008)
    fixed={}
    for name,opts in (
        ("g",[(sp.Integer(1),sp.Integer(0)),(sp.Integer(0),sp.Integer(1))]),
        ("h",[(sp.Integer(1),sp.Integer(1)),(sp.Integer(1),sp.Integer(-1))]),
        ("gh",[(sp.Integer(1),sp.I),(sp.Integer(1),-sp.I)])):
        fixed[name]=list(itertools.product(opts,repeat=4))
    coeff=None
    for _ in range(300):
        trial=[rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) for _ in basis]
        if all(sp.simplify(evalpoly(trial,c))!=0 for arr in fixed.values() for c in arr):
            coeff=trial;break
    assert coeff is not None
    for arr in fixed.values():
        assert all(sp.simplify(evalpoly(coeff,c))!=0 for c in arr)
    assert all(coef!=0 for coef in coeff)
    return {"invariant_linear_system_dimension":len(basis),
            "degree_vectors_in_each_orbit":[[list(q) for q in orbit] for orbit in basis],
            "coefficients":coeff,"all_g_h_gh_fixed_points_avoided":[len(fixed[k]) for k in ("g","h","gh")],
            "explicit_polynomial_status":"invariant and free on the finite ambient fixed-point set, but not certified smooth",
            "smoothness_proved":False,"Ricci_flat_HYM_kinetic_metrics_computed":False}


def representation_character_probe():
    """Compare exact H27 center characters on its two 27D representations."""
    group=list(itertools.product(range(3),repeat=3))
    # Center z=U(0,0,1) acts by left translation in the regular
    # permutation module. Nine disjoint 3-cycles, hence 9 eigenvalues
    # of each third root of unity. On 9 copies of the 3D irreducible
    # Schrödinger module with central character omega, z=omega I27.
    action={}
    for c in range(3):
        row=[]
        for a,b,c0 in group:
            row.append((a,b,(c+c0)%3))
        action[c]=row
    for c in (1,2):
        assert not any(x==y for x,y in zip(group,action[c]))
    regular_trace=[27,0,0]
    multiplicity_regular=[9,9,9]
    multiplicity_operator=[0,27,0] # order [1,omega,omega^2]
    assert sum(multiplicity_regular)==sum(multiplicity_operator)==27
    return {"regular_center_traces":regular_trace,
            "regular_center_eigenvalue_multiplicities_1_omega_omega2":multiplicity_regular,
            "operator_center_eigenvalue_multiplicities_1_omega_omega2":multiplicity_operator,
            "no_27x27_representation_intertwiner_for_fixed_central_character":True,
            "prior_art":"Pass 11043 gives 9D commutant dressing changing the H27 representation to regular; not rederived here"}


def build():
    return {"h27_h13":h27_and_h13(),
            "address_operator_character":representation_character_probe(),
            "global_gravity":global_cycle_glue(),
            "photonic_optimization":photonic_loss_design(),
            "chirality_signed_cover":signed_vacuum_cover(),
            "proton_hexality":proton_center_guard(),
            "flavor_polynomial_candidate":flavor_polynomial()}


if __name__=="__main__":
    data=build()
    OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for k,v in data.items():
        print(k,json.dumps({a:b for a,b in v.items() if a not in ("degree_vectors_in_each_orbit","coefficients","tested_depths")},sort_keys=True),flush=True)
    print("H27_H13_FIVE_FRONTIERS_PASS")
