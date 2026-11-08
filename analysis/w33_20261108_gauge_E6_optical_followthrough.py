#!/usr/bin/env python3
"""Follow-through: affine Hodge frame, native E6 rank repairs, optical routing.

All fields/repairs and optical losses are conditional mathematical/engineering
fixtures, not derived Standard Model dynamics or experimental observations.
"""
from __future__ import annotations
import argparse,itertools,json,math,sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
def gauge(root=ROOT):
    sys.path.insert(0,str(root/"analysis"))
    import w33_20261108_s4_harmonic_qdual as S
    E,F,ei,B1,B2=S.complex27()
    PH=np.eye(108)-B1.T@np.linalg.pinv(B1@B1.T,rcond=1e-12)@B1-B2@B2.T/3
    avg=sum(S.edge_action(pv,E,ei) for _,pv in S.group24().values())/24
    seed=PH@avg
    assert np.max(abs(seed@seed-seed))<1e-10
    frame=np.zeros((108,108));crosscheck=None
    for shift in S.V:
        pv=[S.IX[tuple((v[i]+shift[i])%3 for i in range(3))] for v in S.V]
        R=S.edge_action(pv,E,ei)
        frame+=R@seed@R.T/27
        if shift==(0,0,1):crosscheck=float(np.linalg.norm(seed@R-R@seed))
    eig=np.linalg.eigvalsh((frame+frame.T)/2)
    spectrum={"0":int(np.count_nonzero(abs(eig)<1e-8)),
              "1/12":int(np.count_nonzero(abs(eig-1/12)<1e-8)),
              "1/6":int(np.count_nonzero(abs(eig-1/6)<1e-8))}
    assert spectrum=={"0":90,"1/12":12,"1/6":6}
    assert abs(np.trace(seed)-2)<1e-10 and abs(np.trace(frame)-2)<1e-10
    assert crosscheck>0.1
    assert np.max(abs(frame@frame - frame))>1e-3  # frame is not a projector
    source=np.zeros(27);source[0]=1;source[1]=-1
    assert np.linalg.norm(PH@B1.T@source)<1e-10
    return {"status":"EXACT_S4_ORBIT_FRAME_SPECTRUM_NUMERIC",
      "S4_seed_rank":2,"T27_averaged_frame_eigenvalues":spectrum,
      "affine_generated_sector_rank":18,"unreached_H1_dim":28,
      "S4_seed_translation_commutator_norm":crosscheck,
      "frame_trace":float(np.trace(frame)),
      "constraint":"No translation-covariant self-adjoint operator can have the exact two S4-fixed seed modes as an isolated spectral eigenspace: a spectral subspace of a translation-covariant operator must be translation stable.",
      "charge_source":"vertex-edge gradients are orthogonal to H1, so matter charges require nontrivial circulation/gauge coupling to excite the harmonic sector.",
      "scope":"No normalized physical photon/gauge coupling or matter action was derived."}

def native_e6(root=ROOT):
    sys.path.insert(0,str(root/"analysis"))
    import w33_pass11261_g26_cartan_coordinate_map as P
    old=P._load(root/"analysis/w33_pass11218_e8_cubic_cartan_kernel.py","e6_rank_lift")
    records=old.load_parent().build_records()
    assert len(records)==1620
    phi=np.array([math.sin(i*.712)+.3*math.cos(i*.13)+1j*math.cos(i*.83)
                  for i in range(81)],complex)
    M=np.zeros((81,81),complex)
    for u,x,o,c in records:M[o,x]+=c*phi[u]
    err=float(np.max(abs(M+M.T)))
    U,sv,Vh=np.linalg.svd(M,full_matrices=True)
    rank=int(np.count_nonzero(sv>1e-8))
    assert err<1e-10 and rank==78 and sv[77]>1e-7 and sv[78]<1e-8
    witnesses={}
    for k in (0,1,2,3):
        delta=U[:,78:78+k]@Vh[78:78+k,:] if k else np.zeros((81,81),complex)
        r=int(np.linalg.matrix_rank(M+delta,tol=1e-8))
        witnesses[str(k)]=r
        assert r==78+k
    delta=U[:,78:]@Vh[78:,:]
    skew=delta-delta.T
    assert np.max(abs((M+skew)+(M+skew).T))<1e-10
    assert np.linalg.matrix_rank(M+skew,tol=1e-8)<=80
    return {"status":"NATIVE_SIGNED_E6_RANK_THREE_LIFT_CONDITIONAL",
      "records":len(records),"dimension":81,"native_rank":rank,
      "max_antisymmetry_residual":err,"min_nonzero_singular_value":float(sv[77]),
      "max_zero_singular_value":float(sv[78]),
      "rank_after_rank_k_artificial_corrections":witnesses,
      "alternating_odd_size_never_full_rank":True,
      "proof":"rank(M+delta)<=rank(M)+rank(delta), so a rank78 native operator needs >=3 correction rank for full 81 rank. SVD left/right kernel partial isometries provide algebraic rank3 witness, but not an invariant Yukawa operator.",
      "physical_limit":"The rank3 correction is built after inspecting the mass matrix and is not E6-invariant, not a vacuum construction, not a chiral Standard Model assignment, and not a Nelson-Barr loop calculation."}

def tritter_regroup_nearest(order,axis):
    """Exact min adjacent swaps to ANY ordering with axis triples contiguous.
    Internal order in each triple is preserved; only the next stage is optimized.
    """
    pos={v:i for i,v in enumerate(order)}
    groups={}
    for v in order:
        k=tuple(v[j] for j in range(3) if j!=axis)
        groups.setdefault(k,[]).append(v)
    keys=sorted(groups);n=len(keys)
    assert n==9 and all(len(groups[k])==3 for k in keys)
    cost=[[sum(pos[a]>pos[b] for a in groups[keys[i]] for b in groups[keys[j]])
           for j in range(n)] for i in range(n)]
    dp=[10**9]*(1<<n);path=[None]*(1<<n)
    dp[0]=0;path[0]=()
    for mask in range(1,1<<n):
        for j in range(n):
            if not mask>>j&1:continue
            prev=mask^(1<<j)
            value=dp[prev]+sum(cost[k][j] for k in range(n) if prev>>k&1)
            if value<dp[mask]:dp[mask]=value;path[mask]=path[prev]+(j,)
    final=[v for j in path[-1] for v in groups[keys[j]]]
    ix={v:i for i,v in enumerate(final)}
    mapped=[ix[v] for v in order]
    actual=sum(mapped[i]>mapped[j] for i in range(27) for j in range(i+1,27))
    assert actual==dp[-1]
    return final,actual

def optical():
    """Exhaustively minimize adjacent permutation swaps for 3 b-blocks of 9 rails."""
    w=list(itertools.product(range(3),repeat=2))
    wx={a:i for i,a in enumerate(w)}
    F1=[wx[(a,(c+2*a)%3)] for a,c in w]
    F2=[wx[((a+2*c)%3,c)] for a,c in w]
    def inversions(p):
        return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
    best=(10**9,None)
    evaluated=0
    for order in itertools.permutations(range(9)):
        pos=[0]*9
        for i,k in enumerate(order):pos[k]=i
        cost=0
        for fun in (F1,F2):
            action=[pos[fun[k]] for k in order]
            cost+=inversions(action)
        if cost<best[0]:best=(cost,order)
        evaluated+=1
    assert evaluated==math.factorial(9) and best[0]==14
    base=[w[i] for i in best[1]]
    positions=[(a,b,c) for b in range(3) for a,c in base]
    lex=list(itertools.product(range(3),repeat=3))
    blex=sorted(lex,key=lambda x:(x[1],x[0],x[2]))
    maps=[
        lambda v:(v[0],v[1],(v[2]+2*v[0])%3),
        lambda v:((v[0]+2*v[2])%3,v[1],v[2]),
        lambda v:((v[0]+v[2])%3,v[1],v[2]),
        lambda v:(v[0],v[1],(v[2]+v[0])%3)]
    def audit(order):
        ix={v:i for i,v in enumerate(order)}
        return [inversions([ix[f(v)] for v in order]) for f in maps]
    original=audit(lex)
    b_lex=audit(blex)
    optimized=audit(positions)
    assert original==[12,162,162,12]
    assert b_lex==[12,54,54,12]
    assert optimized==[12,30,30,12]
    # Concrete stage-by-stage 1D regrouping for every three-qutrit axis order.
    # Each DP transition is exact for its fixed incoming order; the full path
    # is a feasible greedy schedule, NOT a global chip/routing optimum.
    routes=[]
    for axes in itertools.permutations((0,1,2)):
        active=positions
        legs=[]
        for axis in axes:
            active,cost=tritter_regroup_nearest(active,axis)
            legs.append(cost)
        back={v:i for i,v in enumerate(positions)}
        perm=[back[v] for v in active]
        legs.append(inversions(perm))
        routes.append({"tritter_axis_sequence":list(axes),
                       "routing_swaps_by_transition":legs,
                       "total_regroup_swaps":sum(legs)})
    best_route=min(routes,key=lambda x:(x["total_regroup_swaps"],x["tritter_axis_sequence"]))
    assert best_route["total_regroup_swaps"]==288
    return {"status":"EXHAUSTIVE_WITHIN_THREE_B_BLOCKS_ROUTING_OPTIMUM",
      "tested_orders":evaluated,"optimized_b_block_pair_order":base,
      "initial_lexicographic_crossing_counts":original,
      "b_first_lexicographic_crossing_counts":b_lex,
      "optimized_crossing_counts":optimized,
      "full_permutation_swaps_before":sum(original),
      "full_permutation_swaps_after":sum(optimized),
      "reduction_fraction":1-sum(optimized)/sum(original),
      "tritter_route_candidates_1d":routes,
      "best_feasible_tritter_regroup_route":best_route,
      "total_1d_adjacent_swaps_in_explicit_schedule":sum(optimized)+best_route["total_regroup_swaps"],
      "upper_bound_internal_plus_active_swap_interactions":81+sum(optimized)+best_route["total_regroup_swaps"],
      "not_global_tritter_routing_optimum":True,
      "tritter_count":27,"upper_bound_internal_two_mode_couplers":81,
      "generic_27_port_unitary_couplers":351,
      "critical_limit":"Counts only adjacent swaps needed by the four SUM permutations in a one-dimensional rail order; additional routing to bring all 27 tritter groups together, phase shifters, losses, crossings and physical layer switching are NOT included. A full chip could erase the apparent resource advantage.",
      "phase_witness":"The previously frozen three four-amplitude gauge-invariant plaquettes must be measured interferometrically; uniform port intensities cannot certify phases."}

def produce(root=ROOT):
    return {"schema":"w33.20261108.gauge_E6_optics.followthrough.v1",
     "gauge":gauge(root),"E6":native_e6(root),"optics":optical(),
     "status":"THREE_CHECKED_CONDITIONAL_FRONTS_PLUS_THE_FULL_AFFINE_NO_GO",
     "limit":"Symmetry constraints and synthetic compiler accounting, not a complete theory of fundamental interactions."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--out",type=Path,default=Path("data/w33_20261108_gauge_E6_optical_followthrough.json"))
    args=p.parse_args();d=produce(args.root)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"gauge_spectrum":d["gauge"]["T27_averaged_frame_eigenvalues"],
     "E6_rank_repair":d["E6"]["rank_after_rank_k_artificial_corrections"],
     "optical_swaps":d["optics"]["full_permutation_swaps_after"]}))
if __name__=="__main__":main()
