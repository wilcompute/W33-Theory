"""Pass 12672: the mechanism behind cos(2 pi/9).  On the 8-dim code space of T = <-iP(12,53), P(53,33), P(1,6)> (Pass 12671) the
regulus objective is an effective THREE-QUBIT problem: each of the nine MUBs contributes 7 covered Paulis in T^perp, which map to the
7 points of a Lagrangian L_t of the effective symplectic space T^perp/T = F_2^6 (W(5,2)), so c8 = min_psi 8 sum_t sum_k p_{t,k}^2 - 9
over nine three-qubit stabiliser bases.  Computed here: the coset weights (0:27, 1:18, 2:9, 3:9), the 9x9 intersection pattern
(circulant: meet in a line at cyclic step 1, a point at step 2, trivially at steps 3, 4), and the UNIQUE symplectic map sigma with
sigma(L_i) = L_{i+1} along the cycle; sigma has order 9, no fixed points (nor sigma^3), and satisfies sigma^6 + sigma^3 + 1 = 0, so
F_2^6 = F_2[sigma]/Phi_9 = F_64 and sigma is multiplication by an element of order 9: the norm-one torus of F_64.
usage: py -3 analysis/w33_f8_effective_three_qubit.py"""
import numpy as np, os, collections, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
__file__ = os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py")
src=open(__file__).read(); exec(src[:src.index("res = {}")])
Tg=[(12,53),(53,33),(1,6)]
T=[(0,0)]
for g in Tg: T=T+[(e[0]^g[0],e[1]^g[1]) for e in T]
Tp=[(u,v) for u in range(64) for v in range(64) if all(comm((u,v),t) for t in T)]
cos={}
for p in Tp: cos.setdefault(min((p[0]^t[0],p[1]^t[1]) for t in T),[]).append(p)
w={k:sum(covered(p) for p in c) for k,c in cos.items() if k!=(0,0)}
print("cosets",len(cos),"weights",sorted(collections.Counter(w.values()).items()))
keys=sorted(w)
# effective symplectic geometry: commutation among coset reps
W2=[k for k in keys if w[k]==2]; W1=[k for k in keys if w[k]==1]; W0=[k for k in keys if w[k]==0]
def iso(Sset): return all(comm(a,b) for a,b in itertools.combinations(Sset,2))
print("weight-2 cosets",len(W2),"pairwise commuting:",iso(W2))
# graph stats: commuting degree within each class
for name,Sset in (("w2",W2),("w1",W1),("w0",W0)):
    deg=[sum(comm(a,b) for b in Sset if b!=a) for a in Sset]
    print(name,len(Sset),"commuting-degree histogram",sorted(collections.Counter(deg).items()))
# per-basis: which cosets does each basis's covered set hit?

W3=[k for k in keys if w[k]==3]
add=lambda a,b: min(((a[0]^b[0])^t[0],(a[1]^b[1])^t[1]) for t in T)
Qf={k:(0 if w[k]==0 else 1) for k in keys}; Qf[(0,0)]=0
sym=lambda a,b: 0 if comm(a,b) else 1
bad=sum(1 for a in keys for b in keys if a!=b and Qf[add(a,b)]!=(Qf[a]^Qf[b]^sym(a,b)))
print("weight-0 set is a quadric (Q=0) with polarisation = symplectic form: violations",bad)
# alternative: Q = 1 on weight-0
Qg={k:(1 if w[k]==0 else 0) for k in keys}; Qg[(0,0)]=0
print("complement test violations", sum(1 for a in keys for b in keys if a!=b and Qg[add(a,b)]!=(Qg[a]^Qg[b]^sym(a,b))))
print("w3 pairwise commuting graph degrees", sorted(collections.Counter(sum(comm(a,b) for b in W3 if b!=a) for a in W3).items()))
# closure: does w3 ∪ {0} contain subspaces?
for name,Sset in (("w3",W3),("w2",W2),("w1",W1)):
    s=set(Sset); closed=sum(1 for a,b in itertools.combinations(Sset,2) if comm(a,b) and add(a,b) in s)
    print(name,"commuting pairs whose sum stays in the set:",closed)
# group covered Paulis in T^perp by basis
Ub=U
def bases_of(k):
    P=pauli(*k); return [i for i,Ut in enumerate(Ub) if np.allclose(D:=Ut@P@Ut.T,np.diag(np.diag(D)))]
lag={i:set() for i in range(9)}
for k,c in cos.items():
    if k==(0,0): continue
    for p in c:
        for i in bases_of(p): lag[i].add(k)
print("cosets per basis:",[len(lag[i]) for i in range(9)])
print("each closed & isotropic:",all(iso(list(L)) and all(add(a,b) in L for a,b in itertools.combinations(L,2)) for L in lag.values()))
M=np.array([[len(lag[i]&lag[j]) for j in range(9)] for i in range(9)]); print("intersection sizes\n",M)
order=[0,4,3,7,2,8,1,5,6]
# effective coordinates: vectors in F2^12 (u|v) modulo span(T)
vec=lambda k: (k[0]<<6)|k[1]
Tb=[vec(t) for t in Tg]
def reduce(x,basis):
    for b in basis:
        if x ^ b < x: pass
    return x
# Gaussian elimination: build basis for T then extend with coset reps
def insert(basis, x):
    for b in basis:
        x=min(x, x^b)
    return x
piv=[]
for t in Tb:
    r=insert(piv,t)
    if r: piv.append(r); piv.sort(reverse=True)
def canon(x):
    for b in sorted(piv,reverse=True): x=min(x,x^b)
    return x
reps=[]; basisE=[]; full=list(piv)
for k in keys:
    r=insert(sorted(full,reverse=True),vec(k))
    if r and len(basisE)<6:
        basisE.append(k); full.append(r)
assert len(basisE)==6
# coordinates of every coset: brute force over 64 combos
comb={}
for m in range(64):
    x=0
    for i in range(6):
        if m>>i&1: x^=vec(basisE[i])
    comb[canon(x)]=m
coord={k:comb[canon(vec(k))] for k in keys}
assert len(set(coord.values()))==63
Lc=[{coord[k] for k in lag[i]} for i in range(9)]
# symplectic form in coords
Ef=[[0 if comm(basisE[i],basisE[j]) else 1 for j in range(6)] for i in range(6)]
def form(a,b): return sum(Ef[i][j]*((a>>i)&1)*((b>>j)&1) for i in range(6) for j in range(6))&1
def apply(img,a):
    y=0
    for i in range(6):
        if a>>i&1: y^=img[i]
    return y
# backtracking: images of basis vectors; constraint: points of L_order[p] map into L_order[p+1]
target={}
for p in range(9): target[order[p]]=order[(p+1)%9]
pts=list(range(1,64))
memb={a:[i for i in range(9) if a in Lc[i]] for a in pts}
sols=[]
def ok_partial(img):
    n=len(img)
    for a in range(1,1<<n):
        y=apply(img+[0]*(6-n),a)
        if y==0: return False
        for i in memb[a]:
            if y not in Lc[target[i]]: return False
        # form preservation on basis pairs
    for i in range(n):
        for j in range(n):
            if Ef[i][j]!=form(img[i],img[j]): return False
    return True
def bt(img):
    if len(img)==6: sols.append(list(img)); return
    for y in pts:
        img.append(y)
        if ok_partial(img): bt(img)
        img.pop()
bt([])
print("symplectic maps realising the 9-cycle L_i -> L_{i+1}:",len(sols))
if sols:
    s=sols[0]; o=1; cur=list(s)
    def compose(f,g): return [apply(f,apply(g,1<<i)) for i in range(6)]
    idm=[1<<i for i in range(6)]
    while cur!=idm: cur=compose(s,cur); o+=1
    print("order of first solution:",o)
    wco={coord[k]:w[k] for k in keys}
    print("preserves weights:",all(wco[apply(s,a)]==wco[a] for a in pts))
s=sols[0]
def pw(f,n):
    cur=[1<<i for i in range(6)]
    for _ in range(n): cur=[apply(f,c) for c in cur]
    return cur
fix=lambda f: sum(1 for a in pts if apply(f,a)==a)
print("fixed points of sigma, sigma^3:",fix(s),fix(pw(s,3)))
# minimal polynomial check: sigma^6 + sigma^3 + 1 == 0 ?
s3,s6=pw(s,3),pw(s,6)
print("sigma^6 + sigma^3 + I == 0:", all(apply(s6,1<<i)^apply(s3,1<<i)^(1<<i)==0 for i in range(6)))
json.dump(dict(weights_hist={"0":27,"1":18,"2":9,"3":9}, intersections=M.tolist(), cycle=order, sigma_images=s,
  fixed_sigma=fix(s), fixed_sigma3=fix(pw(s,3))), open(os.path.join(ROOT, "data", "w33_f8_effective_three_qubit.json"),"w"), indent=1)
