#!/usr/bin/env python3
"""Exact/declared-model verifier for Passes 3829-3836.

The finite geometry, edge factorization, SRG defect signatures, projector
identities, and routing formulas are exact.  The adaptive-control and
thermodynamic coefficients are explicitly declared benchmark models rather
than measured device parameters.
"""
from __future__ import annotations
import argparse, collections, hashlib, itertools, json, math
from pathlib import Path
import numpy as np

GENERATOR_VECTORS=[(0,0,0,1),(0,1,0,0),(0,0,1,1),(1,0,0,0)]
FACTORS=[[[0,18],[1,12],[2,39],[3,25],[4,34],[5,16],[6,38],[7,29],[8,14],[9,17],[10,24],[11,22],[13,23],[15,35],[19,28],[20,21],[26,31],[27,33],[30,36],[32,37]],[[0,13],[1,9],[2,35],[3,28],[4,7],[5,19],[6,27],[8,11],[10,15],[12,37],[14,25],[16,36],[17,31],[18,38],[20,22],[21,26],[23,30],[24,39],[29,32],[33,34]],[[0,1],[2,32],[3,24],[4,28],[5,8],[6,9],[7,17],[10,18],[11,25],[12,21],[13,33],[14,39],[15,36],[16,26],[19,20],[22,38],[23,35],[27,37],[29,34],[30,31]],[[0,3],[1,8],[2,33],[4,31],[5,36],[6,30],[7,10],[9,22],[11,15],[12,34],[13,14],[16,18],[17,29],[19,39],[20,35],[21,27],[23,25],[24,32],[26,38],[28,37]],[[0,15],[1,7],[2,31],[3,27],[4,22],[5,13],[6,24],[8,30],[9,33],[10,36],[11,21],[12,26],[14,37],[16,35],[17,28],[18,39],[19,29],[20,23],[25,32],[34,38]],[[0,19],[1,6],[2,36],[3,30],[4,37],[5,29],[7,35],[8,17],[9,28],[10,27],[11,38],[12,15],[13,32],[14,26],[16,34],[18,22],[20,24],[21,25],[23,33],[31,39]],[[0,20],[1,11],[2,38],[3,29],[4,25],[5,39],[6,16],[7,23],[8,37],[9,14],[10,30],[12,18],[13,24],[15,34],[17,33],[19,21],[22,27],[26,28],[31,35],[32,36]],[[0,2],[1,4],[3,22],[5,23],[6,32],[7,26],[8,20],[9,36],[10,21],[11,35],[12,29],[13,31],[14,38],[15,30],[16,27],[17,18],[19,37],[24,34],[25,39],[28,33]],[[0,14],[1,5],[2,3],[4,10],[6,13],[7,20],[8,34],[9,39],[11,32],[12,31],[15,28],[16,25],[17,30],[18,23],[19,38],[21,33],[22,29],[24,26],[27,35],[36,37]],[[0,17],[1,10],[2,37],[3,23],[4,16],[5,33],[6,12],[7,38],[8,31],[9,20],[11,28],[13,22],[14,27],[15,29],[18,24],[19,30],[21,32],[25,34],[26,36],[35,39]],[[0,16],[1,2],[3,26],[4,19],[5,11],[6,35],[7,14],[8,27],[9,25],[10,33],[12,23],[13,15],[17,32],[18,37],[20,34],[21,31],[22,36],[24,28],[29,39],[30,38]],[[0,21],[1,3],[2,34],[4,13],[5,26],[6,19],[7,32],[8,24],[9,12],[10,39],[11,18],[14,15],[16,17],[20,36],[22,31],[23,37],[25,30],[27,29],[28,35],[33,38]]]
MESH_LAYOUT=[25,20,31,28,38,19,21,5,18,13,10,16,7,35,37,0,14,9,26,32,2,17,36,3,27,22,30,12,24,4,8,33,23,11,6,1,15,39,29,34]

def stable_sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def canonical_points():
    pts=[]; seen=set()
    for v in itertools.product(range(3),repeat=4):
        if v==(0,0,0,0): continue
        for x in v:
            if x:
                inv=1 if x==1 else 2
                c=tuple((inv*y)%3 for y in v); break
        if c not in seen: seen.add(c); pts.append(c)
    return pts

def symp(x,y):
    return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3

def build_graph():
    pts=canonical_points(); A=np.zeros((40,40),dtype=int)
    for i,x in enumerate(pts):
        for j,y in enumerate(pts):
            if i!=j and symp(x,y)==0: A[i,j]=1
    assert np.all(A.sum(1)==12)
    assert np.array_equal(A@A,8*np.eye(40,dtype=int)-2*A+4*np.ones((40,40),dtype=int))
    return pts,A

def canon_vec(v):
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError

def transvection_perm(pts,v):
    idx={p:i for i,p in enumerate(pts)}; out=[]
    for x in pts:
        c=symp(x,v); y=tuple((x[i]+c*v[i])%3 for i in range(4))
        out.append(idx[canon_vec(y)])
    return tuple(out)

def invperm(p):
    q=[0]*len(p)
    for i,j in enumerate(p): q[j]=i
    return tuple(q)

def adaptive_hypervisor():
    states=["clean","diagonal_drift","burst_loss","crosstalk"]
    acts=["w33","local_ring","floquet","spectrometer","direct_29_port"]
    cost=np.array([[4,3,8,12,10],[12,15,2,4,5],[3,10,8,12,6],[9,7,10,3,4]],dtype=float)
    P0=np.array([[15,2,1,2],[4,12,1,3],[6,1,10,3],[5,2,1,12]],dtype=float)/20
    Ps=[]
    for a in acts:
        P=P0.copy()
        if a=="floquet": P[1]=np.array([15,3,0,2])/20
        if a=="spectrometer": P[3]=np.array([14,2,0,4])/20
        if a=="w33": P[2]=np.array([10,1,7,2])/20
        if a=="local_ring": P[0]=np.array([17,1,1,1])/20
        if a=="direct_29_port":
            P[1]=np.array([12,5,1,2])/20; P[3]=np.array([10,2,1,7])/20
        Ps.append(P)
    gamma=.9; N=20; V=np.zeros(N); policy=np.zeros(N,dtype=int)
    for _ in range(10000):
        NV=np.zeros(N); npol=np.zeros(N,dtype=int)
        for s in range(4):
            for last in range(5):
                vals=[]
                for a in range(5):
                    imm=cost[s,a]+(0 if a==last else 2)
                    ev=sum(Ps[a][s,sp]*V[sp*5+a] for sp in range(4))
                    vals.append(imm+gamma*ev)
                NV[s*5+last]=min(vals); npol[s*5+last]=int(np.argmin(vals))
        if np.max(np.abs(NV-V))<1e-12:
            V=NV; policy=npol; break
        V=NV; policy=npol
    adaptive=float(np.mean([V[s*5+4] for s in range(4)]))
    static={}
    for fixed in range(5):
        T=np.zeros((N,N)); cv=np.zeros(N)
        for s in range(4):
            for last in range(5):
                i=s*5+last; cv[i]=cost[s,fixed]+(0 if fixed==last else 2)
                for sp in range(4): T[i,sp*5+fixed]=Ps[fixed][s,sp]
        vv=np.linalg.solve(np.eye(N)-gamma*T,cv)
        static[acts[fixed]]=float(np.mean([vv[s*5+4] for s in range(4)]))
    pol=[[acts[x] for x in row] for row in policy.reshape(4,5)]
    assert pol[0]==["local_ring"]*5 and pol[1]==["floquet"]*5 and pol[2]==["w33"]*5
    return {"states":states,"actions":acts,"discount":"9/10","switch_penalty":2,
            "declared_cost_matrix":cost.astype(int).tolist(),
            "optimal_policy_by_state_and_previous_action":pol,
            "uniform_initial_noise_previous_direct_score":adaptive,
            "best_static_scores":static,
            "improvement_vs_best_static":min(static.values())-adaptive,
            "boundary":"Finite fully observed benchmark MDP; not a learned device process tensor or measured logical-error law."}

def virtual_topology(A):
    seen=set()
    for f in FACTORS:
        verts=[]
        assert len(f)==20
        for u,v in f:
            assert A[u,v] and u<v and (u,v) not in seen
            seen.add((u,v)); verts += [u,v]
        assert sorted(verts)==list(range(40))
    edges={(i,j) for i in range(40) for j in range(i+1,40) if A[i,j]}
    assert seen==edges
    return {"w33_edges":240,"perfect_matching_rounds":12,"minimum_rounds":12,
            "minimum_reason":"Each node has degree 12 and can consume at most one edge token per round; the frozen 1-factorization attains 12.",
            "edge_tokens_per_round":20,"total_heralded_edge_tokens":240,
            "factorization_digest":stable_sha(FACTORS),
            "static_w33_couplers_required":0,
            "boundary":"Edge-token/teleportation abstraction. Source, fusion, memory, classical-feedforward, and code overheads are not included."}

def orbit_projection(A,X):
    D=np.eye(40,dtype=bool); E=A.astype(bool); N=~(D|E)
    Y=np.zeros((40,40),dtype=float)
    for mask in [D,E,N]: Y[mask]=float(np.mean(X[mask]))
    return Y

def autonomous_attractor(A):
    rng=np.random.default_rng(3829); X=rng.normal(size=(40,40)); X=(X+X.T)/2
    P=orbit_projection(A,X); Y=.5*X+.5*P
    before=float(np.linalg.norm(X-P)); after=float(np.linalg.norm(Y-P))
    assert abs(after/before-.5)<1e-12
    return {"fixed_space_basis":["I","A","J-I-A"],"fixed_space_dimension":3,
            "half_step_map":"X -> (X + Pi_orbit(X))/2",
            "exact_deviation_contraction_factor":"1/2",
            "steps_for_2^-20_suppression":20,
            "projector_idempotence_error":float(np.linalg.norm(orbit_projection(A,P)-P)),
            "boundary":"Ideal association-scheme reservoir target. A physical dissipator implementing the orbit projector remains to be engineered."}

def thermodynamic_tournament():
    wW,wL=1064,938
    pstar=math.sqrt(1-math.sqrt((wW-wL)/wL))
    def q(p,r): return 1-(1-p*p)**r
    table=[]; k=1.380649e-23; T=300.; land=k*T*math.log(2)
    for p in [.5,.7,.8,.9,.99]:
        qw,ql=q(p,4),q(p,2)
        table.append({"edge_success":p,"w33_route_success":qw,"two_route_success":ql,
                      "normalized_wire_energy_per_success_w33":wW/qw,
                      "normalized_wire_energy_per_success_control":wL/ql,
                      "landauer_J_per_heralded_success_w33":land/qw,
                      "landauer_J_per_heralded_success_control":land/ql})
    return {"wirelength_proxy_w33":wW,"wirelength_proxy_two_route_control":wL,
            "route_models":{"w33":"1-(1-p^2)^4","control":"1-(1-p^2)^2"},
            "exact_break_even_formula":"sqrt(1-sqrt(63/469))",
            "break_even_edge_success":pstar,
            "w33_lower_normalized_energy_below_break_even":True,
            "table":table,
            "boundary":"Retry-plus-wirelength and Landauer-floor benchmark only; wall-plug source, cooling, detector, and decoder energy are not measured."}

def substrate_inversion(A):
    coords={i:(i//8,i%8) for i in range(40)}
    edges=[(i,j) for i in range(40) for j in range(i+1,40) if A[i,j]]
    ds=[abs(coords[MESH_LAYOUT[i]][0]-coords[MESH_LAYOUT[j]][0])+abs(coords[MESH_LAYOUT[i]][1]-coords[MESH_LAYOUT[j]][1]) for i,j in edges]
    assert sum(ds)==870 and max(ds)==10
    classes={
      "native_w33_fabric":{"static_links":240,"consumable_edge_tokens":0,"interaction_rounds":12,"hop_tokens":240},
      "teleported_virtual_graph":{"static_links":0,"consumable_edge_tokens":240,"interaction_rounds":12,"hop_tokens":240},
      "nearest_neighbor_5x8_mesh":{"static_links":67,"consumable_edge_tokens":0,"interaction_rounds_lower_bound":12,"interaction_rounds_serial_witness":870,"hop_tokens":870,"maximum_route_hops":10},
      "single_shared_bus":{"static_links":1,"consumable_edge_tokens":0,"interaction_rounds":240,"hop_tokens":240}}
    return {"abstract_substrate_classes":classes,"mesh_layout":MESH_LAYOUT,"mesh_layout_digest":stable_sha(MESH_LAYOUT),
            "weighted_cost_symbols":["alpha_static_link","beta_consumable_token","gamma_round","delta_hop"],
            "cost_expressions":{"native":"240a+12g+240d","virtual":"240b+12g+240d","mesh_interval":"67a+[12,870]g+870d","bus":"a+240g+240d"},
            "conclusion":"No substrate is coefficient-independently optimal; the preferred implementation changes with fabrication, consumable-entanglement, latency, and routing-energy prices.",
            "boundary":"Exact primitive-count inversion, not a vendor benchmark. Mapping a physical platform to coefficients requires measured data."}

def srg_checksum(A):
    I=np.eye(40,dtype=int); J=np.ones((40,40),dtype=int)
    def R(B): return B@B+2*B-8*I-4*J
    assert not np.any(R(A))
    edge_sigs=collections.Counter(); add_sigs=collections.Counter()
    for i in range(40):
        for j in range(i+1,40):
            B=A.copy(); B[i,j]=B[j,i]=1-A[i,j]; Q=R(B)
            sig=(int(np.count_nonzero(Q)),int(np.sum(Q*Q)),int(np.max(np.abs(Q))),int(np.linalg.matrix_rank(Q)),tuple(sorted((int(k),int(v)) for k,v in collections.Counter(np.count_nonzero(Q,axis=1)).items())))
            (edge_sigs if A[i,j] else add_sigs)[sig]+=1
    assert len(edge_sigs)==len(add_sigs)==1
    de,ae=next(iter(edge_sigs)),next(iter(add_sigs))
    return {"identity":"A^2+2A-8I-4J=0",
            "single_edge_deletion":{"count":240,"residual_support":de[0],"frobenius_norm_squared":de[1],"rank":de[3],"row_support_histogram":dict(de[4])},
            "single_edge_insertion":{"count":540,"residual_support":ae[0],"frobenius_norm_squared":ae[1],"rank":ae[3],"row_support_histogram":dict(ae[4])},
            "endpoint_localization":"The two endpoint rows are uniquely the rows with support 13 (deletion) or 14 (insertion).",
            "boundary":"Exact single-edge digital-twin checksum and localizer; simultaneous defects require a separate decoding theorem."}

def heralded_distillation():
    out={}
    for target in [.99,.999,.9999]:
        pn=math.sqrt(1-(1-target)**.25); lo,hi=0.,1.
        for _ in range(100):
            p=(lo+hi)/2; val=1-(1-p)*(1-p*p)**2
            if val<target: lo=p
            else: hi=p
        out[str(target)]={"nonedge_four_two_hop_threshold":pn,"adjacent_direct_plus_two_detours_threshold":(lo+hi)/2}
    return {"nonedge_success":"1-(1-p^2)^4","adjacent_success":"1-(1-p)(1-p^2)^2","thresholds":out,
            "path_structure":"Four internally disjoint two-hop paths for every nonedge; one direct edge plus two edge-disjoint triangle detours for every edge.",
            "boundary":"Independent heralded-edge model; correlated source, memory, and fusion failures are outside the formula."}

def symmetry_bath(pts):
    gens=[transvection_perm(pts,v) for v in GENERATOR_VECTORS]; sgens=gens+[invperm(g) for g in gens]
    P=np.zeros((40,40),dtype=float)
    for i in range(40):
        for g in sgens: P[i,g[i]]+=1/8
    ev=np.linalg.eigvalsh(P); ev=np.sort(ev)[::-1]; gap=1-ev[1]
    t=math.ceil(math.log(.02/math.sqrt(40))/math.log(ev[1]))
    return {"generator_jumps":8,"stationary_distribution":"uniform on 40 points","second_eigenvalue":float(ev[1]),"spectral_gap":float(gap),"one_percent_total_variation_bound_steps":t,
            "interpretation":"Random transvection jumps spread a localized single-site defect over the full point orbit before orbit averaging.",
            "boundary":"Spectral statement for the ideal discrete symmetry bath; physical jump rates and dissipation costs are not specified."}

def certificate():
    pts,A=build_graph()
    result={"schema":"w33.pass3829_3836.v1","passes":{
      "3829_noise_adaptive_geometry_hypervisor":adaptive_hypervisor(),
      "3830_measurement_only_virtual_w33_topology":virtual_topology(A),
      "3831_autonomous_association_scheme_attractor":autonomous_attractor(A),
      "3832_thermodynamic_geometry_tournament":thermodynamic_tournament(),
      "3833_substrate_inversion_tournament":substrate_inversion(A),
      "3834_bonkers_srg_digital_twin_checksum":srg_checksum(A),
      "3835_bonkers_heralded_topology_distillation":heralded_distillation(),
      "3836_bonkers_transvection_symmetry_bath":symmetry_bath(pts)},
      "boundaries":["Adaptive-control coefficients are a declared benchmark MDP, not measured process-tensor data.","Virtual edges are abstract heralded qutrit edge tokens; complete cluster/fusion overhead remains open.","The attractor is an ideal orbit-projector reservoir target.","Thermodynamic and substrate results separate exact event counts from unmeasured platform coefficients.","Checksum and heralded-route theorems assume single defects or independent heralded edge events.","The symmetry bath is an ideal permutation Markov process, not a laboratory dissipator."]}
    result["semantic_sha256"]=stable_sha(result); return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--json",type=Path); ns=ap.parse_args(); c=certificate()
    if ns.json: ns.json.write_text(json.dumps(c,indent=2,sort_keys=True)+"\n")
    print("PASS_8_FRONTS",c["semantic_sha256"])
if __name__=="__main__": main()
