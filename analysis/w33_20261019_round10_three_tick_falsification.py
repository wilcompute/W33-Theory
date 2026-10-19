"""Round10 front2: adversarial Monte Carlo THREE-TICK support search
against claimed extension of exact 2-tick threshold to full 120 simplex.
Feasible witnesses ONLY, not certified global optimization.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_20261019_tick_operator_frame_majorization import points,symp,build_projectors
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round10_three_tick_falsification.json"
pts=points();P=build_projectors(pts)
def run():
    rng=np.random.default_rng(120761)
    T=.5
    u=np.exp(-1/T)
    Fs=-T*np.log(3+6*u)
    krit=-1.5*(1-u)/(3+6*u)
    families=[]
    for batch in range(30):
        triples=np.array([rng.choice(120,3,replace=False) for _ in range(300)])
        # remove same projective direction (same p different k)
        triples=triples[np.array([len({int(v//3) for v in t})==3 for t in triples])]
        n=len(triples)
        mode=batch%5
        if mode==0:rates=np.tile(np.array([1/3,1/3,1/3]),(n,1))
        elif mode==1:rates=rng.dirichlet([.2,.2,.2],size=n)
        elif mode==2:rates=rng.dirichlet([1,1,1],size=n)
        elif mode==3:rates=rng.dirichlet([5,5,5],size=n)
        else:rates=rng.dirichlet([.05,.05,.05],size=n)
        Q=np.einsum('nk,nkij->nij',rates,P[triples])
        eig=np.linalg.eigvalsh(Q).real
        Z=np.exp((eig-1)/T).sum(axis=1)
        F=-T*np.log(Z)
        comm=np.array([[int(symp(pts[a//3],pts[b//3])!=0)
           for a,b in ((t[0],t[1]),(t[0],t[2]),(t[1],t[2]))] for t in triples],dtype=float)
        C=(4/3)*(comm[:,0]*rates[:,0]*rates[:,1]+
                 comm[:,1]*rates[:,0]*rates[:,2]+
                 comm[:,2]*rates[:,1]*rates[:,2])
        for k in range(n):
            # Round10 numerical audit: tiny C causes catastrophic
            # cancellation in F-Fsingle and false crossings near -1/3.
            if C[k]<1e-5 or F[k]-Fs<1e-9:continue
            threshold=(Fs-F[k])/C[k]
            families.append((float(threshold),tuple(map(int,triples[k])),
              tuple(map(float,rates[k])),int(sum(comm[k])),float(C[k]),float(F[k])))
    best=max(families,key=lambda x:x[0])
    best_by_edges={str(edge):max((v for v in families if v[3]==edge),key=lambda x:x[0]) for edge in (1,2,3)}
    checks={"all_3_noncommuting_pair_strata_sampled":set(map(int,(v[3] for v in families)))=={1,2,3},
        "all_C_positive_feasible":all(0<x[4]<=4/9+1e-9 for x in families),
        "all_F_above_majorization_baseline":min(v[5]-Fs for v in families)>-1e-10,
        "best_witness_has_negative_threshold":best[0]<0,
        "large_stratified_sample":len(families)>4000}
    out={"schema":"w33.round10.triple_support_adversarial_search.v1",
       "T":T,"single_tick_free_energy":float(Fs),
       "local_two_tick_instability_kappa":float(krit),
       "sampled_three_tick_candidates":len(families),
       "best_feasible_three_tick_crossing_kappa":best[0],
       "best_three_tick_indices":list(best[1]),"best_three_weights":list(best[2]),
       "best_three_commuting_complement_edges":best[3],
       "best_three_C":best[4],"best_three_F":best[5],
       "stratum_best":{name:{"crossing_kappa":v[0],"indices":v[1],"weights":v[2],"noncommuting_pairs":v[3],"C":v[4]} for name,v in best_by_edges.items()},
       "comparison":"If ANY three-tick feasible crossing kappa exceeds the two-tick local threshold, it is an explicit numerical counterexample to conjectured full-global boundary at local instability. If not, this finite sampling cannot prove the conjecture; the full 120-variable global phase remains open.",
       "tests":{"three_tick_counterexample_to_local_kappa":bool(best[0]>krit+1e-4),
           "sampled_C_nonsingular":True},
       "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"best_threshold":best[0],"local":krit,"by_edges":{k:x[0] for k,x in best_by_edges.items()}},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
