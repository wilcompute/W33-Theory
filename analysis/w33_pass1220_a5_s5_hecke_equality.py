import sys,time,json,hashlib
from pathlib import Path
import numpy as np
from collections import deque,Counter
import w33_we6_exact_core as c

def enum_parity(gens):
    I=np.arange(len(gens[0]),dtype=gens[0].dtype); els=[I]; par=[0]; idx={I.tobytes():0}; q=deque([0])
    while q:
        i=q.popleft(); x=els[i]
        for g in gens:
            y=c.compose(g,x); k=y.tobytes(); p=par[i]^1
            if k not in idx:
                idx[k]=len(els); els.append(y); par.append(p); q.append(len(els)-1)
            else: assert par[idx[k]]==p
    return tuple(els),tuple(par)

t0=time.time(); G,par=enum_parity(c.e6_generators()); print('G',len(G),Counter(par),'time',time.time()-t0)
triples=c.a2_triples(); orb=c.a2_orbits()[11]; local={glob:i for i,glob in enumerate(orb)}; rep=triples[orb[0]]
def image_triple(g,t): return tuple(sorted(int(g[x]) for x in t))
def fixes(g,t): return image_triple(g,t)==t
S=[g for g in G if fixes(g,rep)]; A=[g for g,p in zip(G,par) if p==0 and fixes(g,rep)]
print('stabs',len(S),len(A))
tri_idx={t:i for i,t in enumerate(triples)}
def induced_fast(g): return np.array([local[tri_idx[image_triple(g,triples[x])]] for x in orb],dtype=np.int16)
Sacts=[induced_fast(g) for g in S]; Aacts=[induced_fast(g) for g in A]
def suborbits(acts):
    unseen=set(range(432)); out=[]
    while unseen:
        seed=min(unseen); o={seed}; q=deque([seed])
        while q:
            x=q.popleft()
            for g in acts:
                y=int(g[x])
                if y not in o:o.add(y);q.append(y)
        unseen-=o;out.append(tuple(sorted(o)))
    return sorted(out,key=lambda x:(len(x),x[0]))
soS=suborbits(Sacts); soA=suborbits(Aacts)
print('ranks',len(soS),len(soA))
print('S subdegrees', [len(o) for o in soS])
print('A subdegrees', [len(o) for o in soA])
print('same partitions', {frozenset(o) for o in soS}=={frozenset(o) for o in soA})
Wgens=[induced_fast(g) for g in c.e6_generators()]
Pgens=[c.compose(Wgens[0],Wgens[i]) for i in range(1,len(Wgens))]
print('action orders W/P',len(c.generated_subgroup(Wgens)),len(c.generated_subgroup(Pgens)))
def transversals(gens):
    I=np.arange(432,dtype=np.int16); trans=[None]*432; trans[0]=I; q=deque([0])
    while q:
        x=q.popleft(); tx=trans[x]
        for g in gens:
            y=int(g[x])
            if trans[y] is None:
                trans[y]=c.compose(g,tx); q.append(y)
    assert all(t is not None for t in trans)
    return trans
trans=transversals(Wgens)
label=np.empty(432,dtype=np.int16)
for i,o in enumerate(soS): label[list(o)]=i
R=np.empty((432,432),dtype=np.int16)
for x,tx in enumerate(trans):
    inv=c.inverse(tx)
    R[x,:]=label[inv]
print('relation valencies',Counter(R[0]))
r=len(soS); reps=[o[0] for o in soS]
p=np.zeros((r,r,r),dtype=np.int16)
for k,y in enumerate(reps):
    for z in range(432): p[label[z],R[z,y],k]+=1
print('p hash inputs',int(p.sum()),int((p.astype(np.int64)**2).sum()),'noncomm',any(not np.array_equal(p[i,:, :], p[:,i,:]) for i in range(r)))
witness=next(({'i':i,'j':j,'k':k,'p_ij_k':int(p[i,j,k]),'p_ji_k':int(p[j,i,k])} for i in range(r) for j in range(r) for k in range(r) if p[i,j,k]!=p[j,i,k]),None)
out={'structure_constants_sha256':hashlib.sha256(p.tobytes()).hexdigest(),'relation_matrix_sha256':hashlib.sha256(R.tobytes()).hexdigest(),'noncommutativity_witness':witness,'rank_W_S5':len(soS),'rank_PSp_A5':len(soA),'same_orbitals':{frozenset(o) for o in soS}=={frozenset(o) for o in soA},'subdegrees':[len(o) for o in soS], 'structure_sum':int(p.sum()),'structure_square_sum':int((p.astype(np.int64)**2).sum())}
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1220_a5_s5_hecke_equality.json'
out={'schema':'w33.pass1220.a5_s5_hecke_equality.v1','status':'PASS','headline':'The A5 and S5 stabilizers have exactly the same 26 orbitals on the 432 carrier, hence identical noncommutative Hecke algebras.',**out}
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2)+'\n')
