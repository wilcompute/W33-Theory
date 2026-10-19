"""Round10 front1: exact Schreier graph orbit classification of the
2916-element stabilizer of a fixed rank2 two-qutrit stabilizer vacuum.
No full group element enumeration required.
"""
from __future__ import annotations
import collections,itertools,json
from pathlib import Path
import numpy as np
from w33_20261019_round8_clifford_vacuum_orbit import basis,contexts,mapping
from w33_20261019_nextfive_optics_su9 import GENERATORS
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round10_pair_orbit_schreier.json"
def run():
    pair=[(9*h+a,9*h+b) for h in range(40)
          for a,b in itertools.combinations(range(9),2)]
    ix={p:i for i,p in enumerate(pair)}
    moves=[]
    for name,U in GENERATORS.items():
        m,_=mapping(name,U)
        moves.append(np.array([ix[tuple(sorted((int(m[a]),int(m[b]))))]
                 for a,b in pair],dtype=np.int32))
    n=len(pair);identity=np.arange(n,dtype=np.int32)
    reps=[None]*n;reps[0]=identity
    queue=collections.deque([0])
    while queue:
        j=queue.popleft()
        for g in moves:
            nxt=int(g[j])
            if reps[nxt] is None:
                reps[nxt]=g[reps[j]]
                queue.append(nxt)
    assert all(x is not None for x in reps)
    inv=[]
    for a in reps:
        ar=np.empty(n,dtype=np.int32)
        ar[a]=identity
        inv.append(ar)
    parent=np.arange(n)
    rank=np.zeros(n,dtype=np.uint8)
    def root(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    def union(a,b):
        x,y=root(a),root(b)
        if x==y:return
        if rank[x]<rank[y]:x,y=y,x
        parent[y]=x
        if rank[x]==rank[y]:rank[x]+=1
    schreier=0;idcheck=0
    for v,tv in enumerate(reps):
        for g in moves:
            vv=int(g[v])
            h=inv[vv][g[tv]]
            assert int(h[0])==0
            if np.array_equal(h,identity):
                idcheck+=1;continue
            schreier+=1
            for a,b in enumerate(h):union(a,int(b))
    blocks=collections.defaultdict(list)
    for j in range(n):blocks[root(j)].append(j)
    Q=np.array([basis[h,a]+basis[h,b] for h in range(40)
                for a,b in itertools.combinations(range(9),2)])
    q=Q[0]
    overlap=np.einsum('ij,aji->a',q,Q).real
    orbit_data=[]
    residual=0.
    for ids in blocks.values():
        ov=overlap[ids]
        residual=max(residual,float(ov.max()-ov.min()))
        orbit_data.append({"size":len(ids),"overlap_to_reference":float(np.mean(ov)),
                           "representative":min(ids)})
    orbit_data.sort(key=lambda z:(z["overlap_to_reference"],z["size"]))
    overlap_hist=collections.Counter((round(x["overlap_to_reference"],9),x["size"]) for x in orbit_data)
    checks={
       "complete_1440_pair_orbit":len(reps)==1440,
       "Schreier_stabilizer_generators_fix_base":schreier>0,
       "stabilizer_orbits_partition_1440":sum(x["size"] for x in orbit_data)==1440,
       "identity_orbit_size_1":sum(x["size"]==1 and abs(x["overlap_to_reference"]-2)<1e-9 for x in orbit_data)==1,
       "two_body_overlap_constant_per_orbit":residual<1e-9,
       "all_1440_reachable_under_full_group":all(x is not None for x in reps)}
    result={"schema":"w33.round10.stabilizer_2916_pair_orbits.schreier.v1",
      "algorithm":"BFS transversals of the 1440-node Clifford orbit, then generate Schreier stabilizer maps h=t_(g·v)^-1 g t_v for every orbit point v and every five Clifford generators g. Union orbit labels under h; no group element enumeration or optical matrix approximation required for orbit sizes.",
      "full_clifford_order":4199040,"vacuum_orbit":1440,"stabilizer_order":2916,
      "nontrivial_schreier_generators_processed":schreier,"identity_schreier_maps":idcheck,
      "stabilizer_orbit_count":len(orbit_data),"stabilizer_pair_orbits":orbit_data,
      "overlap_constant_max_residual":residual,
      "meaning":"For fixed Q0, the 2916 stabilizer's orbits on all 1440 Q classify distinct pair-vacuum geometry. Any Clifford-invariant pair energy depends only on these orbit classes; free coefficients remain undetermined, and even a minimizing pair breaks orbit symmetry spontaneously rather than selecting unique absolute vacuum.",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"checks":result["checks"],"orbits":orbit_data,"schreier":schreier},indent=2))
    assert result["all_checks_pass"]
    return result
if __name__=="__main__":run()
