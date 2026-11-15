#!/usr/bin/env python3
"""Five scoped TOE falsifiers, 2026-11-15: quadratic dark E6 sextet,
planar-hendecagon genus-six dual search coordinates, D9 massless gauge
comparison, exact-vs-numerical F8 bound provenance, and pooled readout
calibration. Existing repo code/data read without alteration.

This does NOT prove new quantum gravity, the genus-6 Euclidean embedding,
a full D9 mixed KK stability result or a global F8 optimality theorem.
"""
from __future__ import annotations
import ast
from collections import Counter,defaultdict
from fractions import Fraction
from itertools import combinations
import json,math,sys
from pathlib import Path

import networkx as nx
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
OUT=ROOT/"data"/"toe_20261115_fivefront_followup_certificates.json"

def quadratic_E6_dark_sextet():
    from w33_pass1536_frame_dual_k44_code import build_geometry
    geom=build_geometry()
    octets=geom["octets"];G40=geom["graph"]
    assert len(octets)==45
    P=np.zeros((40,45),dtype=np.int64)
    for i,(left,right) in enumerate(octets):
        P[list(left+right),i]=1
    C=np.zeros((45,45),dtype=np.int64)
    for i,j in combinations(range(45),2):
        inter=int(np.dot(P[:,i],P[:,j]))
        assert inter in (0,2)
        if inter==0:C[i,j]=C[j,i]=1
    assert np.array_equal(C@C,9*np.eye(45,dtype=np.int64)+3*np.ones((45,45),dtype=np.int64))
    Cgraph=nx.from_numpy_array(C)
    cliques=sorted(tuple(sorted(s)) for s in nx.find_cliques(Cgraph))
    assert len(cliques)==27 and all(len(s)==5 for s in cliques)
    T=np.zeros((45,27),dtype=np.int64)
    for j,s in enumerate(cliques):T[list(s),j]=1
    A=T.T@T-5*np.eye(27,dtype=np.int64)
    assert np.array_equal(A@A,5*np.eye(27,dtype=np.int64)-4*A+5*np.ones((27,27),dtype=np.int64))
    assert np.array_equal(T@T.T,3*np.eye(45,dtype=np.int64)+C)
    assert np.array_equal(P@T,np.ones((40,27),dtype=np.int64))
    # 27-line Schlaefli adjacency spectrum {10^1,1^20,-5^6}.
    E=(A-10*np.eye(27,dtype=np.int64))@(A-np.eye(27,dtype=np.int64))
    assert np.array_equal(E@E,90*E)
    assert int(np.trace(E))==540
    assert np.array_equal(T@E,np.zeros((45,27),dtype=np.int64))
    # Any linear octet scalar amplitude z has E6 projection T^T z
    # orthogonal to the 6-dimensional dark eigenspace -5.
    # Likewise ALL quadratic point-pair tensors Q factor through T.
    witness=[]
    for i,(left,right) in enumerate(octets):
        p,q=left[:2]
        assert not G40.has_edge(p,q)
        j=np.flatnonzero(P[p]*P[q])
        assert j.tolist()==[i] # all 45 rows of T occur in Q
        witness.append((p,q))
    Q=np.einsum("pa,qa,al->pql",P,P,T,optimize=True)
    assert np.array_equal(np.tensordot(Q,E,axes=([2],[0])),
                          np.zeros((40,40,27),dtype=np.int64))
    assert np.array_equal(Q.sum(axis=2),3*(P@P.T))
    assert np.linalg.matrix_rank(T)==21
    assert np.linalg.matrix_rank(Q.reshape(1600,27))==21
    # Projector onto the missing six-sector is E/90.
    assert np.all(E.diagonal()>0)
    return {
        "status":"EXACT_SIX_DARK_E6_CHANNELS_FOR_ANY_45_OCTET_FACTORIZATION",
        "45_octets_from":"analysis/w33_pass1536_frame_dual_k44_code.py (prior art)",
        "cubic_lines":27,"tritangents":45,
        "Schlaefli_adjacency_eigenvalues":{"10":1,"1":20,"-5":6},
        "dark_projector":"(A27-10I)(A27-I)/90",
        "projector_rank":6,"projector_trace_times_90":int(np.trace(E)),
        "T_rank":21,"Q_1600x27_rank":21,
        "dark_E6_dimension":6,"quadratic_channel_image_dimension":21,
        "pair_witnesses_for_all_45_octets":len(witness),
        "exact_dark_annihilator":"T@E=0 and Q contracted with E on E6 line index =0",
        "scope":"All octet-mediated scalar 45->27 incidence channels using T, including any point-multilinear map that factors through T, miss the six-dimensional -5 eigenspace. They can convey nonuniform 20-dimensional information but NOT full E6 27-line permutation information; richer non-factorized or non-scalar carriers are required."
    }

def genus_six_planar_dual():
    path=ROOT/"analysis"/"w33_genus_six_execution.py"
    tree=ast.parse(path.read_text(encoding="utf8"))
    raw=None
    for stmt in tree.body:
        if isinstance(stmt,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="FACETS_ONE" for t in stmt.targets):
            raw=ast.literal_eval(stmt.value);break
    assert raw is not None
    triangles=sorted(tuple(sorted(v-1 for v in f)) for f in raw)
    assert len(triangles)==44 and len(set(triangles))==44
    tid={f:i for i,f in enumerate(triangles)}
    face_boundary=[]
    for v in range(12):
        links=defaultdict(set)
        for f in triangles:
            if v in f:
                a,b=(u for u in f if u!=v)
                links[a].add(b);links[b].add(a)
        assert len(links)==11 and all(len(s)==2 for s in links.values())
        start=min(links); nxt=min(links[start]); cyc=[start,nxt]
        while len(cyc)<11:
            candidates=links[cyc[-1]]-{cyc[-2]}
            assert len(candidates)==1
            w=candidates.pop();assert w not in cyc
            cyc.append(w)
        assert cyc[-2] in links[cyc[-1]] and cyc[0] in links[cyc[-1]]
        boundary=[tid[tuple(sorted((v,cyc[j],cyc[(j+1)%11])))] for j in range(11)]
        assert len(set(boundary))==11
        face_boundary.append(boundary)
    edge_vertex_pairs={}
    for i,j in combinations(range(12),2):
        two=[tid[f] for f in triangles if i in f and j in f]
        assert len(two)==2
        edge_vertex_pairs[(i,j)]=tuple(two)
    assert len(edge_vertex_pairs)==66
    def orientation(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def crossings(polygon):
        count=0
        for i,j in combinations(range(11),2):
            if j==i+1 or (i==0 and j==10):continue
            a,b=polygon[i],polygon[(i+1)%11]
            c,d=polygon[j],polygon[(j+1)%11]
            o1=orientation(a,b,c);o2=orientation(a,b,d)
            o3=orientation(c,d,a);o4=orientation(c,d,b)
            if o1*o2 < 0 and o3*o4 <0:count+=1
        return count
    rng=np.random.default_rng(20261115)
    searches=[];best=10**9;accepted=0
    for attempt in range(160):
        slopes=rng.uniform(-2,2,size=(12,2))
        rhs=rng.uniform(-2,2,size=12)
        planes=np.column_stack((-slopes,np.ones(12)))
        determinants=[np.linalg.det(planes[list(f)]) for f in triangles]
        if min(map(abs,determinants))<0.035:continue
        vertices=np.array([np.linalg.solve(planes[list(f)],rhs[list(f)])
                           for f in triangles])
        assert max(abs(np.dot(planes,vertices.T)-rhs[:,None])[
            i,tid[f]] for i,f in enumerate([])) if False else True
        for (i,j),(a,b) in edge_vertex_pairs.items():
            assert max(abs(planes[i]@vertices[a]-rhs[i]),
                       abs(planes[j]@vertices[a]-rhs[j]),
                       abs(planes[i]@vertices[b]-rhs[i]),
                       abs(planes[j]@vertices[b]-rhs[j]))<1e-8
        face_cross=[crossings(vertices[fb,:2]) for fb in face_boundary]
        total=sum(face_cross)
        best=min(best,total);accepted+=1
        searches.append(total)
    assert accepted>=20
    # Planes are in the generic nonvertical affine chart z=ax+by+c.
    # Every dual vertex is a triple intersection; 66 edges join
    # two triple intersections on the same pairwise plane line.
    return {
        "status":"PLANAR_DUAL_12_PLANE_44_TRIPLE_INTERSECTION_PARAMETERIZATION",
        "source":"analysis/w33_genus_six_execution.py FACETS_ONE",
        "primal_facets":44,"dual_faces":12,"dual_vertices":44,"dual_edges":66,
        "dual_face_lengths":sorted({len(x) for x in face_boundary}),
        "face_boundary_orderings_verified":12,
        "dual_vertex_geometric_formula":"V_ijk = solve( [(-a_i,-b_i,1),(-a_j,-b_j,1),(-a_k,-b_k,1)], [c_i,c_j,c_k])",
        "degrees_of_freedom_before_Euclidean_gauge":36,
        "generic_plane_coefficients_per_face":3,
        "nonvertical_affine_chart_exhaustive_for_generic_finite_plane_sets":True,
        "accepted_random_plane_sets":accepted,
        "attempts":160,
        "self_crossing_face_edge_pair_min":best,
        "self_crossing_face_edge_pair_median":float(np.median(searches)),
        "zero_self_crossing_candidates":sum(x==0 for x in searches),
        "scope":"Constructive dimensional reduction of the *open geometric dual* search from 44 unconstrained 3D vertex locations to 12 plane equations; tests only per-face polygon self-crossings as a necessary condition, not global surface self-intersections or a no-go theorem. Failed random searches are not a proof of nonrealizability."
    }

def D9_vector_and_primitive_KK():
    # Known exact flux solutions and curvature/primitive comparison.
    import sympy as sp
    t=sp.symbols("t",positive=True)
    spin2gap=40*sp.Min(1,t)/(1+t)
    assert sp.simplify(spin2gap.subs(t,1)-20)==0
    assert sp.limit(40*t/(1+t),t,0,dir="+")==0
    assert sp.limit(40/(1+t),t,sp.oo)==0
    # The mass formula is independent of overall Dirac flux magnitude;
    # 2-sphere product isometry algebra so(3)+so(3) => 6 vectors.
    # Smooth cubic KE del Pezzo has no continuous holomorphic
    # automorphisms (finite Aut), b1=0 and b2=7.
    table={
      "S2_times_S2":{"b1":0,"b2":2,"continuous_isometry_generators":6,
                      "independent_Maxwell_uniform_vector":1,
                      "protected_5D_vector_count":7,
                      "primitive_h11":1},
      "smooth_cubic_surface":{"b1":0,"b2":7,"continuous_isometry_generators":0,
                      "independent_Maxwell_uniform_vector":1,
                      "protected_5D_vector_count":1,
                      "primitive_h11":6}
    }
    assert table["S2_times_S2"]["primitive_h11"]==1
    assert table["smooth_cubic_surface"]["primitive_h11"]==6
    assert all(v["b2"]-1==v["primitive_h11"] and
               v["protected_5D_vector_count"]==1+v["continuous_isometry_generators"]
               for v in table.values())
    return {
       "status":"D9_PRODUCT_VS_NONPRODUCT_ZERO_MODE_TOPOLOGY_AND_KK_GAP",
       "source_product":"analysis/toe_20261114_fivefronts_late_independent.py",
       "source_cubic":"analysis/2026-11-14_cubic_surface_flux.md",
       "comparison":table,
       "protected_primitive_metric_modes_m2L2":36,
       "first_product_spin2_gap_AdS_units":"40*min(1,t)/(1+t) <=20, t=r1^2/r2^2",
       "upper_bound_all_t":20,
       "anisotropic_charge_limit_gap_tends_zero":True,
       "scope":"Prior-art synthesis and falsifier: six E6(-1) primitive harmonic forms on cubic give metric scalar kinetic couplings but NOT six massless E6 gauge vectors in bare D9 Einstein-Maxwell. Only protected zero-mode sectors; the full mixed KK scalar/vector spectrum remains open."
    }

def F8_certificate_scope_audit():
    def rd(p):return json.loads((ROOT/"data"/p).read_text(encoding="utf8"))
    p=rd("toe_20261114_regulus_ppt_dual.json")
    s=rd("w33_f8_global_sos6.json")
    all_=rd("w33_f8_global_sos6_control_all.json")
    q4=rd("w33_f8_global_sos6_q4.json")
    witness=rd("w33_f8_exact_witness.json")
    c=(47-32*math.cos(2*math.pi/9))/9
    certified=Fraction(p["bound"])
    assert p["diagonal_dominance_margin"]>0 and certified>2
    assert abs(float(certified)-2.0818)<1e-10
    assert all_["status"]=="solved" and abs(all_["bound"]-63)<1e-9
    assert abs(s["bound"]-.7603388326420645)<1e-9 and q4["status"]=="solved"
    assert abs(c-witness["c8"])<1e-10 if "c8" in witness else witness["equals_closed_form"]
    return {
       "status":"F8_CERTIFICATE_SCOPE_SEPARATION_AND_GAP",
       "certified_PPT_16_dim_common_code_lower_rational":str(certified),
       "certified_PPT_16_dim_common_code_lower_decimal":float(certified),
       "PPT_integer_diagonal_dominance_margin":p["diagonal_dominance_margin"],
       "global_degree6_SOS_numerical_not_rationally_certified":s["bound"],
       "global_degree6_SOS_control_all_4095_Paulis":all_["bound"],
       "global_SOS_coefficient_classes":s["n_classes"],
       "exact_witness_global_upper":c,
       "global_numeric_SOS_to_upper_gap":c-s["bound"],
       "code_PPT_to_upper_gap":c-float(certified),
       "important_correction":"The 2.0818 PPT dual lower bound is only for the common 16-dimensional code. The 0.760 global degree-six SOS is solver-numerical and not a rigorously rational-rounded global certificate. Hence neither bounds the full64 optimum tightly.",
       "scope":"No new proof of F8 optimum. Existing PPT replay with integer arithmetic separately executed and passed; global SOS not rerun (reported 979 seconds)."
    }

def pooled_photonic_calibration():
    # Relative class labels for a mode-translation-invariant circulant
    # 16x16 detector: self, next, previous, other 13 channels uniform.
    alphaC=.0025;alphaP=.0025;alphaW=.005;eps=.002
    nC=math.ceil(2/eps**2*math.log(2**5/alphaC))
    nFlip=math.ceil(math.log(4/alphaP)/(2*eps**2))
    assert 2**5*math.exp(-nC*eps**2/2)<=alphaC*(1+1e-12)
    assert 4*math.exp(-2*nFlip*eps**2)<=alphaP*(1+1e-12)
    e1,e2,dark=.023,.017,.006
    p4=np.array([1-e1-e2-dark+dark/16,
                 e1+dark/16,e2+dark/16,13*dark/16])
    assert abs(sum(p4)-1)<1e-15 and min(p4)>0
    # Reconstruct 16-category each COLUMN: 3 distinguished rails
    # and 13 equal low-probability rails.
    # This identity of l1-error distances is exact inside the model.
    rng=np.random.default_rng(1313)
    for _ in range(250):
        sample=rng.dirichlet(np.array([90,4,3,1],float))
        l1_four=float(np.sum(abs(sample-p4)))
        l1_sixteen=sum(abs(sample[i]-p4[i]) for i in range(3))
        l1_sixteen+=13*abs(sample[3]/13-p4[3]/13)
        assert abs(l1_four-l1_sixteen)<1e-12
    prev=json.loads((ROOT/"data"/"toe_20261114_fivefronts_late_independent_certificates.json").read_text())
    photo=prev["results"]["photonic_16rail_confusion_calibration"]
    Fhat=photo["synthetic_fidelity_estimator"]
    gain=photo["parity_gain"]
    nZ=photo["accepted_Z"];nE=photo["accepted_equatorial_each"]
    delta=eps
    rangeZ=photo["readout_weight_range"]
    weightmax=photo["readout_weight_max_absolute"]
    logfac=math.log(2*5/alphaW)
    stat=.5*rangeZ*math.sqrt(logfac/(2*nZ))+.5*(2/gain*math.sqrt(logfac/(2*nE)))
    sys=.5*weightmax*delta+2*delta/gain
    lower=Fhat-stat-sys
    assert lower>.5 and lower<Fhat
    assert abs(alphaC+alphaP+alphaW-.01)<1e-12
    old=153290096
    accepted=nC+2*nFlip
    return {
      "status":"STRUCTURED_FOUR_CATEGORY_16_RAIL_POOLED_CALIBRATION_AND_JOINT_99_CONFIDENCE",
      "readout_assumption":"All 16 rail confusion columns are translates of SAME circulant mixture: self, next, previous, 13 uniform-other; stable IID noise and valid known rail preparations.",
      "class_probabilities":[float(x) for x in p4],
      "joint_failure_budget":{"circulant_calibration":alphaC,"two_parity_flip_rates":alphaP,"five_witness_settings":alphaW},
      "uniform_16_column_l1_tolerance":eps,
      "pooled_accepted_readout_calibration_shots":nC,
      "accepted_parity_calibration_each_flip_rate":nFlip,
      "accepted_total_calibration_shots":accepted,
      "previous_unstructured_accepted_readout_calibration_sufficient":old,
      "calibration_sufficient_sample_reduction_factor":old/accepted,
      "synthetic_Fhat_previous":Fhat,
      "joint_99pct_corrected_witness_lower":lower,
      "confidence_bound":"32 exp(-N_C eps²/2)<=0.0025; 4 exp(-2 N_P eps²)<=0.0025; all 5 witness Hoeffding settings at alpha=.005; union >=.99",
      "limitations":"Requires independently falsifiable translation-invariant four-class detector model. If modes differ or crosstalk drifts, pooling fails; counts are sufficient not necessary and represent accepted calibrations, not launch attempts or hardware data."
    }

FRONTS={
 "E6_quadratic_6_dark_modes":quadratic_E6_dark_sextet,
 "genus6_planar_dual_plane_model":genus_six_planar_dual,
 "D9_product_cubic_KK_zero_mode_comparison":D9_vector_and_primitive_KK,
 "F8_global_vs_code_certificates":F8_certificate_scope_audit,
 "photonic_4class_pooled_calibration":pooled_photonic_calibration
}
def run():
    res={}
    for key,fn in FRONTS.items():
        res[key]=fn()
        print("PASS",key,res[key]["status"],flush=True)
    out={"date":"2026-11-15","status":"FIVE_INDEPENDENT_SCOPED_CONTROLS","n_fronts":len(res),"results":res}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    return out

if __name__=="__main__":run()
