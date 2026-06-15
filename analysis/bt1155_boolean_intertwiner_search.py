#!/usr/bin/env python3
import itertools, json
import numpy as np

choice={1:'l1',2:'l0',3:'s',4:'l1',5:'l2',6:'l1',7:'s',8:'l0',9:'s',10:'l0',11:'s',12:'l0',13:'l0',14:'l0',15:'l1'}

def pts():
    out=[]; seen=set()
    for v in itertools.product(range(3), repeat=4):
        if not any(v): continue
        i=next(k for k,x in enumerate(v) if x)
        inv=1 if v[i]==1 else 2
        w=tuple((inv*x)%3 for x in v)
        if w not in seen: seen.add(w); out.append(w)
    return out

def sp(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3

def lg(a):
    a%=3
    return 0 if a==0 else (1 if a==1 else -1)

def feat(v,m,k):
    if k[0]=='l': return lg(sum(((m>>i)&1)*v[i] for i in range(4))+int(k[1]))
    z=1
    for i in range(4):
        if (m>>i)&1: z*=1 if v[i] else -1
    return z

P=pts(); n=len(P); A=np.zeros((n,n),int)
for i,u in enumerate(P):
    for j,v in enumerate(P):
        if i!=j and sp(u,v)==0: A[i,j]=1
I=np.eye(n); Pm=(A-12*I)@(A-2*I)/96
F=np.array([[feat(v,m,choice[m]) for m in range(1,16)] for v in P],float)
PF=Pm@F
out={'bt':1155,'points':n,'edges':int(A.sum()//2),'negative_rank':int(np.linalg.matrix_rank(Pm,tol=1e-8)),'raw_rank':int(np.linalg.matrix_rank(F,tol=1e-8)),'projected_rank':int(np.linalg.matrix_rank(PF,tol=1e-8)),'choice':choice,'status':'projected features span negative sector; equivariance still open'}
out['all_checks_pass']=(out['points'],out['edges'],out['negative_rank'],out['projected_rank'])==(40,240,15,15)
print(json.dumps(out,indent=2,sort_keys=True))
