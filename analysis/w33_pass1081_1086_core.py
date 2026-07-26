from __future__ import annotations
import itertools
from collections import deque
import numpy as np
Q=3
J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=np.int8)%Q

def normalize(v):
    a=np.array(v,dtype=np.int16)%Q
    for x in a:
        if int(x):
            return tuple(int(y) for y in (a*pow(int(x),-1,Q))%Q)
    raise ValueError

def symp(x,y): return int((np.array(x,dtype=np.int16)@J@np.array(y,dtype=np.int16))%Q)

def build_w33():
    pts=sorted({normalize(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    pidx={p:i for i,p in enumerate(pts)}
    lset=set()
    for i,x in enumerate(pts):
        for y in pts[i+1:]:
            if symp(x,y): continue
            sp={pidx[normalize((a*np.array(x)+b*np.array(y))%3)] for a,b in itertools.product(range(3),repeat=2) if (a,b)!=(0,0)}
            if len(sp)==4:lset.add(tuple(sorted(sp)))
    lines=sorted(lset); lidx={L:i for i,L in enumerate(lines)}
    point_lines=[[] for _ in pts]
    for li,L in enumerate(lines):
        for p in L: point_lines[p].append(li)
    frames=[(a,b) for a in range(40) for b in range(a+1,40) if not(set(lines[a])&set(lines[b]))]
    fidx={f:i for i,f in enumerate(frames)}
    flags=[(p,l) for p in range(40) for l in point_lines[p]]
    flagidx={x:i for i,x in enumerate(flags)}
    return pts,pidx,lines,lidx,point_lines,frames,fidx,flags,flagidx

def transvection_perm(v,pts,pidx):
    vv=np.array(v,dtype=np.int16)
    return tuple(pidx[normalize((np.array(x,dtype=np.int16)+symp(x,v)*vv)%3)] for x in pts)

def compose(a,b): return tuple(a[b[i]] for i in range(len(a)))

def inverse(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)

def enumerate_group(gens):
    I=tuple(range(len(gens[0]))); seen={I:0}; elems=[I]; q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose(g,x)
            if y not in seen:
                seen[y]=len(elems); elems.append(y); q.append(y)
    return elems,seen

def line_perm(p,lines,lidx): return tuple(lidx[tuple(sorted(p[x] for x in L))] for L in lines)
def frame_perm(lp,frames,fidx): return tuple(fidx[tuple(sorted((lp[a],lp[b])))] for a,b in frames)
def flag_perm(p,lp,flags,flagidx): return tuple(flagidx[(p[x],lp[l])] for x,l in flags)

def all_spreads(lines,npts=40):
    onpt=[[li for li,L in enumerate(lines) if p in L] for p in range(npts)]; sols=[]
    def rec(chosen,used):
        if len(used)==npts:
            sols.append(tuple(sorted(chosen))); return
        p=min(x for x in range(npts) if x not in used)
        for li in onpt[p]:
            if set(lines[li])&used: continue
            rec(chosen+[li],used|set(lines[li]))
    rec([],set()); return sorted(set(sols))

def outer_similitude_perm(pts,pidx):
    M=np.diag([1,2,1,2]).astype(np.int16)
    return tuple(pidx[normalize(M@np.array(x,dtype=np.int16)%3)] for x in pts)

def rank_mod(A,p=1000003):
    A=np.array(A,dtype=np.int64)%p; r=0
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None: continue
        A[[r,q]]=A[[q,r]]; A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]: A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==A.shape[0]: break
    return r
