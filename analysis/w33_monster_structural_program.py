"""Passes 3614-3627: Monster/U4(2) structural and falsifier verifier.

This file deliberately separates exact W33 computations, documented class-fusion
constraints, GAP-delegated restriction computations, and two falsified direct
constructions. No arithmetic coincidence is promoted to an embedding or mechanism.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import asdict, dataclass
import itertools, json
from pathlib import Path

P=3; MONSTER_ORDER=808017424794512875886459904961710757005754368000000000
U42_ORDER=25920; MONSTER_MIN_IRREP=196883; MONSTER_LARGE_PRIMES=(47,59,71)
MOONSHINE_1A=(196884,21493760,864299970,20245856256,333202640600,4252023300096)

def rank_mod(a, prime=1000003):
    m=[[x%prime for x in r] for r in a]; rows=len(m); cols=len(m[0]); rank=0
    for c in range(cols):
        p=next((i for i in range(rank,rows) if m[i][c]),None)
        if p is None: continue
        m[rank],m[p]=m[p],m[rank]; inv=pow(m[rank][c],prime-2,prime)
        m[rank]=[(x*inv)%prime for x in m[rank]]
        for i in range(rows):
            if i!=rank and m[i][c]:
                f=m[i][c]; m[i]=[(x-f*y)%prime for x,y in zip(m[i],m[rank])]
        rank+=1
    return rank

def canonical(v):
    for x in v:
        if x%P:
            inv=pow(x%P,-1,P); return tuple((inv*y)%P for y in v)
    raise ValueError

points=sorted({canonical(v) for v in itertools.product(range(P),repeat=4) if any(v)})
J4=((0,0,1,0),(0,0,0,1),(-1,0,0,0),(0,-1,0,0))
def symp(x,y): return sum(x[i]*J4[i][j]*y[j] for i in range(4) for j in range(4))%P
n=len(points); A=[[0]*n for _ in range(n)]
for i,x in enumerate(points):
    for j,y in enumerate(points):
        A[i][j]=int(i!=j and symp(x,y)==0)

def mm(X,Y): return [[sum(a*b for a,b in zip(r,c)) for c in zip(*Y)] for r in X]
I=[[int(i==j) for j in range(n)] for i in range(n)]; ONE=[[1]*n for _ in range(n)]
A2=mm(A,A); target=[[8*I[i][j]-2*A[i][j]+4*ONE[i][j] for j in range(n)] for i in range(n)]
B=[[12*I[i][j]-A[i][j] for j in range(n)] for i in range(n)]
C=[[A[i][j]+4*I[i][j] for j in range(n)] for i in range(n)]
N=mm(B,C); N2=mm(N,N)
adj={N[i][j] for i in range(n) for j in range(n) if A[i][j]}
non={N[i][j] for i in range(n) for j in range(n) if i!=j and not A[i][j]}
# Any sequence in span{12^n,2^n,(-4)^n} satisfies this recurrence.
res=[]
for i in range(len(MOONSHINE_1A)-3):
    res.append(MOONSHINE_1A[i+3]-10*MOONSHINE_1A[i+2]-32*MOONSHINE_1A[i+1]+96*MOONSHINE_1A[i])
checks={
 "points":n==40,
 "degree":set(map(sum,A))=={12},
 "srg_identity":A2==target,
 "projector_rank":rank_mod(N)==24,
 "projector_scale":N2==[[60*x for x in r] for r in N],
 "projector_diagonal":{N[i][i] for i in range(n)}=={36},
 "adjacent_value":adj=={6},
 "nonadjacent_value":non=={-4},
 "leech_uniform_no_go":(6*4)%36!=0 and (-4*4)%36!=0,
 "moonshine_raw_moment_no_go":all(x!=0 for x in res),
 "prime_separation":all(U42_ORDER%p for p in MONSTER_LARGE_PRIMES),
 "minimal_degree_factorization":MONSTER_MIN_IRREP==47*59*71,
 "steinberg_sylow_scale":81==3**4 and U42_ORDER%(3**4)==0,
}
assert all(checks.values())
result={
 "verified":True,"passes":"3614-3627","checks":checks,
 "w33":{"vertices":40,"degree":12,"srg":[40,12,2,4],"eigenvalue_2_projector":{"rank":24,"numerator_scale":60,"diagonal":36,"adjacent_off_diagonal":6,"nonadjacent_off_diagonal":-4}},
 "bonkers_falsifiers":{
   "leech_seed":{"status":"NO_GO_FOR_DIRECT_UNIFORM_EMBEDDING","norm4_adjacent_inner_product":"2/3","norm4_nonadjacent_inner_product":"-4/9","surviving_direction":"nonuniform integral extension, glue code, quotient, or multi-copy cancellation"},
   "raw_moonshine_moments":{"status":"NO_GO_FOR_RAW_THREE_EIGENMODE_MODEL","recurrence":"s[n+3]=10*s[n+2]+32*s[n+1]-96*s[n]","residuals":res,"surviving_direction":"graded induction, Hecke/replicability, VOA, or ambient Monster module"}},
 "monster_u42":{"u42_order":U42_ORDER,"u42_primes":[2,3,5],"monster_large_primes_external_to_u42":list(MONSTER_LARGE_PRIMES),"documented_5B_type_fusion_constraints":{"involutions":"2B","order_3":"3B","order_5":"5B"},"majorana_consequence":"DIRECT_2A_AXIS_MODEL_BLOCKED_FOR_5B_TYPE_EMBEDDING","steinberg_3_local_register":{"degree":81,"sylow_3_order":81,"status":"delegated to GAP companion certificate"}},
 "evidence_boundary":{"not_claimed":["canonical concrete mmgroup U4(2) embedding","unique class fusion","observed degree-81 multiplicity","Griess or VOA multiplication from W33 incidence","Leech embedding of the W33 rank-24 frame"]}}
if __name__=="__main__":
    out=Path("data/PART_3614_3627_MONSTER_STRUCTURAL_PROGRAM_results.json"); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8"); print(json.dumps(result,indent=2))
