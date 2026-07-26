from __future__ import annotations
import itertools, math
from dataclasses import dataclass
import numpy as np
from sympy import Matrix
from sympy.combinatorics import Permutation, PermutationGroup

Q=3
J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%Q

def normalize(v):
    a=np.array(tuple(v),dtype=int)%Q
    for x in a:
        if int(x): return tuple(int(y) for y in (a*pow(int(x),-1,Q))%Q)
    raise ValueError

def symp(x,y): return int((np.array(x,dtype=int)@J@np.array(y,dtype=int))%Q)
def pimages(g,n): return [int(g(i)) for i in range(n)]
def compose(a,b): return tuple(a[b[i]] for i in range(len(a)))
def invperm(a):
    out=[0]*len(a)
    for i,x in enumerate(a): out[x]=i
    return tuple(out)
def perm_order_tuple(p):
    n=len(p); seen=[False]*n; o=1
    for i in range(n):
        if not seen[i]:
            j=i;l=0
            while not seen[j]: seen[j]=True;j=p[j];l+=1
            o=math.lcm(o,l)
    return o

@dataclass
class W33:
    points:list; pidx:dict; lines:list; point_lines:list; gens:list; G:PermutationGroup; adj:np.ndarray

def build_w33():
    pts=sorted({normalize(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={p:i for i,p in enumerate(pts)}
    lset=set()
    for i,x in enumerate(pts):
        for y in pts[i+1:]:
            if symp(x,y): continue
            sp={idx[normalize((a*np.array(x)+b*np.array(y))%3)] for a,b in itertools.product(range(3),repeat=2) if (a,b)!=(0,0)}
            if len(sp)==4:lset.add(tuple(sorted(sp)))
    lines=sorted(lset); pl=[[] for _ in pts]; adj=np.zeros((40,40),dtype=np.int8)
    for li,L in enumerate(lines):
        for p in L: pl[p].append(li)
        for a,b in itertools.combinations(L,2): adj[a,b]=adj[b,a]=1
    def trans(v):
        vv=np.array(v,dtype=int); im=[]
        for x in pts:
            xx=np.array(x,dtype=int); im.append(idx[normalize((xx+symp(x,v)*vv)%3)])
        return Permutation(im)
    gens=[trans(v) for v in pts]; G=PermutationGroup(gens)
    return W33(pts,idx,lines,[tuple(sorted(x)) for x in pl],gens,G,adj)

def row_basis(rows):
    B=[]
    for r in rows:
        x=int(r)
        for b in B:x=min(x,x^b)
        if x:B.append(x);B.sort(reverse=True)
    return B

def toword(row):
    x=0
    for i,b in enumerate(row):
        if int(b)&1:x|=1<<i
    return x

def null_basis(A):
    rows=[[int(x)&1 for x in A[i]] for i in range(A.shape[0])]
    n=A.shape[1]; piv={};r=0
    for c in range(n):
        p=next((i for i in range(r,len(rows)) if rows[i][c]),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for i in range(len(rows)):
            if i!=r and rows[i][c]:rows[i]=[a^b for a,b in zip(rows[i],rows[r])]
        piv[c]=r;r+=1
    out=[]
    for f in [c for c in range(n) if c not in piv]:
        v=[0]*n;v[f]=1
        for c,rr in piv.items():v[c]=rows[rr][f]
        out.append(toword(v))
    return out

def reduce_basis(x,B):
    for b in B:x=min(x,x^b)
    return x

def perm_word(word,g,n=40):
    out=0
    for i in range(n):
        if word>>i&1:out|=1<<g(i)
    return out

@dataclass
class Quot:
    C:list;Cp:list;glue:list;rep:dict;canon_to_coord:dict;gens:list;G:PermutationGroup;ani:list;iso:list

def build_quot(w):
    C=row_basis(toword(r) for r in w.adj); Cp=null_basis(w.adj); allb=list(C);gl=[]
    for v in Cp:
        if reduce_basis(v,allb):allb.append(v);allb.sort(reverse=True);gl.append(v)
    rep={};ctc={}
    for c in range(256):
        x=0
        for i,v in enumerate(gl):
            if c>>i&1:x^=v
        can=reduce_basis(x,C);rep[c]=x;ctc[can]=c
    gens=[]
    for g in w.gens:
        im=[ctc[reduce_basis(perm_word(rep[c],g),C)] for c in range(256)]
        gens.append(Permutation(im))
    G=PermutationGroup(gens); q=lambda c:(rep[c].bit_count()//2)%2
    return Quot(C,Cp,gl,rep,ctc,gens,G,[c for c in range(1,256) if q(c)],[c for c in range(1,256) if not q(c)])

def match4(items):
    a,b,c,d=items
    return [tuple(sorted(((a,b),(c,d)))),tuple(sorted(((a,c),(b,d)))),tuple(sorted(((a,d),(b,c))))]

@dataclass
class Axes:
    axes:list;coords:list;endpoints:list;ep_axis_sign:dict;axis_gens:list;ep_gens:list

def build_axes(w,q):
    axes=[];coords=[];eps=[];eas={}
    for p in range(40):
        for m in match4(w.point_lines[p]):
            objs=[];words=[]
            for pair in m:
                supp=(set(w.lines[pair[0]])|set(w.lines[pair[1]]))-{p}
                objs.append((p,tuple(sorted(pair))));words.append(sum(1<<x for x in supp))
            c0=reduce_basis(words[0],q.C);c1=reduce_basis(words[1],q.C);assert c0==c1
            ai=len(axes);axes.append((p,m));coords.append(q.canon_to_coord[c0])
            for s,e in zip((1,-1),objs):eas[e]=(ai,s);eps.append(e)
    li={L:i for i,L in enumerate(w.lines)}; ai={a:i for i,a in enumerate(axes)}; ei={e:i for i,e in enumerate(eps)}
    def ml(l,g):return li[tuple(sorted(g(p) for p in w.lines[l]))]
    def ma(a,g):
        p,m=a;mm=tuple(sorted(tuple(sorted((ml(x,g),ml(y,g)))) for x,y in m));return (g(p),mm)
    def me(e,g):
        p,pair=e;return (g(p),tuple(sorted(ml(x,g) for x in pair)))
    ag=[Permutation([ai[ma(a,g)] for a in axes]) for g in w.gens]
    eg=[Permutation([ei[me(e,g)] for e in eps]) for g in w.gens]
    return Axes(axes,coords,eps,eas,ag,eg)

E8_SIMPLE=[(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0),(0,0,0,0,-2,2,0,0),(0,0,0,0,0,-2,2,0)]
CH=(1,3,9,27,2,6,18,54)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def e8roots():
    R=[]
    for i in range(8):
      for j in range(i+1,8):
       for si in (1,-1):
        for sj in (1,-1):
         v=[0]*8;v[i]=2*si;v[j]=2*sj;R.append(tuple(v))
    for s in itertools.product((1,-1),repeat=8):
      if sum(x==-1 for x in s)%2==0:R.append(tuple(s))
    return sorted(set(R))
@dataclass
class E8: roots:list; pairs:dict; positive:dict

def build_e8():
    R=e8roots();M=Matrix(8,8,lambda r,c:E8_SIMPLE[c][r]);Mi=M.inv();d={}
    for root in R:
        co=Mi*Matrix(root);res=sum((int(x)%2)<<i for i,x in enumerate(co));d.setdefault(res,[]).append(root)
    pairs={k:tuple(sorted(v)) for k,v in d.items()};pos={k:max(v,key=lambda r:dot(CH,r)) for k,v in pairs.items()}
    return E8(R,pairs,pos)

def gf2rank(vs):return len(row_basis(vs))
def hypbasis(q,b):
    def rec(ch):
        if len(ch)==8:return ch
        for x in range(1,256):
            if gf2rank(ch+[x])!=len(ch)+1 or q(x) or any(b(x,y) for y in ch):continue
            for y in range(1,256):
                if gf2rank(ch+[x,y])!=len(ch)+2 or q(y) or b(x,y)!=1 or any(b(y,z) for z in ch):continue
                z=rec(ch+[x,y])
                if z:return z
    z=rec([])
    if not z:raise RuntimeError
    return z

def basis_lookup(B):
    out={}
    for m in range(256):
        x=0
        for i,b in enumerate(B):
            if m>>i&1:x^=b
        out[x]=m
    return out

def isometry(q,e):
    sq=lambda c:(q.rep[c].bit_count()//2)%2
    sb=lambda a,b:(q.rep[a]&q.rep[b]).bit_count()%2
    def lv(r):return tuple(sum(E8_SIMPLE[i][j] for i in range(8) if r>>i&1) for j in range(8))
    tq=lambda r:(dot(lv(r),lv(r))//8)%2; tb=lambda a,b:(dot(lv(a),lv(b))//4)%2
    S=hypbasis(sq,sb);T=hypbasis(tq,tb);look=basis_lookup(S);im={}
    for c in range(256):
        m=look[c];x=0
        for i,b in enumerate(T):
            if m>>i&1:x^=b
        im[c]=x
    assert {im[c] for c in q.ani}==set(e.pairs)
    return im

def matrix_perm(w,M):
    return Permutation([w.pidx[normalize(np.array(M,dtype=int)@np.array(x,dtype=int)%3)] for x in w.points])
