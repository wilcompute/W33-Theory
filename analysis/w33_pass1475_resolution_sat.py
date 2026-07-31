import json, time, sys
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
d=json.load(open("data/w33_pass1392_frame_edge_incidence.json",encoding="utf-8"))
rows,nE=d["rows"],d["edges"]; nF=len(rows)
byedge=[[] for _ in range(nE+1)]
for i,r in enumerate(rows):
    for c in r: byedge[c].append(i)
NC=9; pool=IDPool(); X=lambda f,c: pool.id(("x",f,c))
t0=time.time(); cls=[]
for f in range(nF):
    cls.extend(CardEnc.equals(lits=[X(f,c) for c in range(NC)],bound=1,vpool=pool,
                              encoding=EncType.pairwise).clauses)
for e in range(1,nE+1):
    for c in range(NC):
        cls.extend(CardEnc.equals(lits=[X(f,c) for f in byedge[e]],bound=1,vpool=pool,
                                  encoding=EncType.pairwise).clauses)
for k,f in enumerate(byedge[1]): cls.append([X(f,k)])
print(f"encoding: {pool.top} vars, {len(cls)} clauses, built in {time.time()-t0:.1f}s",flush=True)
t1=time.time()
with Cadical153(bootstrap_with=cls) as S:
    sat=S.solve()
    print(f"solve {time.time()-t1:.0f}s -> {'SAT' if sat else 'UNSAT'}",flush=True)
    if sat:
        m=set(l for l in S.get_model() if l>0)
        col=[next(c for c in range(NC) if X(f,c) in m) for f in range(nF)]
        from collections import Counter
        print("class sizes:",sorted(Counter(col).values()),flush=True)
        print("every edge sees 9 distinct classes:",
              all(len(set(col[f] for f in byedge[e]))==9 for e in range(1,nE+1)),flush=True)
        json.dump({"colouring":col},open("data/w33_pass1475_resolution.json","w"))
        print("*** RESOLUTION EXISTS ***",flush=True)
    else:
        print("*** NO RESOLUTION EXISTS (UNSAT) ***",flush=True)
