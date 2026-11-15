"""Pass 12672: the torus symmetry of the F_8 code-space problem is inherited from a GLOBAL symmetry of the regulus MUB set.
The regulus set is preserved by m -> g m h^T (g, h in SL(2,8)) and Frobenius (m = 2x2 matrix over F_8, Q = det; label map to this
repo's Pauli labels via the other track's trace-pairing convention).  Enumerates the 504^2 * 3 maps, keeps those normalising
T = <-iP(12,53), P(53,33), P(1,6)> (Pass 12671), and records the induced permutations of the nine effective Lagrangians
(w33_f8_effective_three_qubit.py): a dihedral group D_9 of order 18, the 9-cycles coming from pairs (g, h) with g and h both of order
9 (non-split tori).  Then builds the six-qubit Clifford W of one such pair, selects the Pauli correction fixing the exact witness,
and minimises F on every eigenspace of W.   usage: py -3 analysis/w33_f8_torus_global_origin.py"""
import os, itertools, collections
import numpy as np
HERE0 = os.path.dirname(os.path.abspath(__file__)); __file__ = os.path.join(HERE0, "w33_f8_effective_three_qubit.py")
exec(open(__file__).read().split("order=[0,4,3,7,2,8,1,5,6]")[0])
# conventions: my label (u,v) <-> other track's (x,z) with v = vmap(z); matrix m = [[x_lo, x_hi],[z_hi, z_lo]], det m = Q
def multiply(a,b):
    r=0
    while b:
        if b&1: r^=a
        b>>=1; a<<=1
        if a&8: a^=0b1011
    return r
def tr8(a): s=multiply(a,a); return a^s^multiply(s,s)
det=lambda x,z: multiply(x&7,z&7)^multiply(x>>3,z>>3)
vmap=lambda z: sum(tr8(det(1<<i,z))<<i for i in range(6))
zinv={vmap(z):z for z in range(64)}; assert len(zinv)==64
tomat=lambda u,v: ((u&7, u>>3),(zinv[v]>>3, zinv[v]&7))
def tolabel(m):
    (a,b),(c,d)=m; x=a|(b<<3); z=d|(c<<3); return (x, vmap(z))
# sanity: covered (my classification) <=> det m == 0
mdet=lambda m: multiply(m[0][0],m[1][1])^multiply(m[0][1],m[1][0])
assert all((covered((u,v)) if (u,v)!=(0,0) else False)==((u,v)!=(0,0) and mdet(tomat(u,v))==0) for u in range(64) for v in range(64))
mm=lambda A,B: tuple(tuple(multiply(A[i][0],B[0][j])^multiply(A[i][1],B[1][j]) for j in range(2)) for i in range(2))
tp=lambda A: ((A[0][0],A[1][0]),(A[0][1],A[1][1]))
SL=[((a,b),(c,d)) for a in range(8) for b in range(8) for c in range(8) for d in range(8) if multiply(a,d)^multiply(b,c)==1]
assert len(SL)==504
frob=lambda m: tuple(tuple(multiply(e,e) for e in r) for r in m)
Tset=set(T[1:]); Tm=[tomat(*t) for t in T[1:]]
# symplectic check on one random element (form = Tr polarisation of det = Pauli commutation)
norm=[]
for g in SL:
    gT=[mm(g,m) for m in Tm]
    for h in SL:
        hT=tp(h)
        for f in range(3):
            ok=True; imgs=[]
            for m in gT:
                y=mm(m,hT)
                for _ in range(f): y=frob(y)
                lab=tolabel(y)
                if lab not in Tset: ok=False; break
            if ok: norm.append((g,h,f))
print("elements of (SL2 x SL2):Frob normalising T:",len(norm))
# induced permutation on the nine effective Lagrangians
def act(el,lab):
    g,h,f=el; y=mm(mm(g,tomat(*lab)),tp(h))
    for _ in range(f): y=frob(y)
    return tolabel(y)
def cosrep(lab): return min((lab[0]^t[0],lab[1]^t[1]) for t in T)
lagsets=[frozenset(lag[i]) for i in range(9)]
perms=collections.Counter()
for el in norm:
    pi=[]
    for i in range(9):
        img=frozenset(cosrep(act(el,k)) for k in lag[i])
        pi.append(lagsets.index(img) if img in lagsets else None)
    perms[tuple(pi)]+=1
cyc=lambda p: sorted(len(c) for c in __import__("itertools").chain()) 
def cycle_type(p):
    seen=set(); out=[]
    for i in range(9):
        if i in seen: continue
        L=0; j=i
        while j not in seen: seen.add(j); j=p[j]; L+=1
        out.append(L)
    return tuple(sorted(out))
print("induced permutations:",len(perms),"cycle types:",collections.Counter(cycle_type(p) for p in perms))
def order2(A):
    I=((1,0),(0,1)); M=A; k=1
    while M!=I: M=mm(M,A); k+=1
    return k
rows=[]
for el in norm:
    g,h,f=el
    pi=[]
    for i in range(9):
        img=frozenset(cosrep(act(el,k)) for k in lag[i]); pi.append(lagsets.index(img))
    rows.append(dict(order_g=order2(g),order_h=order2(h),frob=f,cycle_type=list(cycle_type(pi))))
print(collections.Counter((r["order_g"],r["order_h"],r["frob"],tuple(r["cycle_type"])) for r in rows))
import json
json.dump(dict(n_normaliser=len(norm), elements=rows, cycle_type_hist={str(k):v for k,v in collections.Counter(tuple(r["cycle_type"]) for r in rows).items()}),
          open(os.path.join(HERE0, "..", "data", "w33_f8_torus_global_origin.json"),"w"), indent=1)
from scipy.optimize import minimize
el9=[el for el,r in zip(norm,rows) if r["cycle_type"]==[9]][0]
S=lambda lab: act(el9,lab)
pcount=lambda n: bin(n).count("1")
Hm=lambda u,v: (1j**(pcount(u&v)%4))*pauli(u,v)
v0=np.ones(64,complex)
Pr=np.eye(64,dtype=complex)
for i in range(6): Pr=Pr@(np.eye(64)+Hm(*S((0,1<<i))))/2
w_,Vv=np.linalg.eigh((Pr+Pr.conj().T)/2); v0=Vv[:,np.argmax(w_)]
Xi_=[Hm(*S((1<<i,0))) for i in range(6)]
V=np.zeros((64,64),complex)
for x in range(64):
    c=v0.copy()
    for i in range(6):
        if x>>i&1: c=Xi_[i]@c
    V[:,x]=c
assert np.allclose(V.conj().T@V,np.eye(64),atol=1e-9)
for (u,v) in [(1<<i,0) for i in range(6)]+[(0,1<<i) for i in range(6)]:
    M=V@Hm(u,v)@V.conj().T; T_=Hm(*S((u,v)))
    assert np.allclose(M,T_) or np.allclose(M,-T_)
# witness
g2={"__name__":"x","__file__":os.path.join(HERE0, "w33_f8_exact_witness.py")}
src2=open(os.path.join(HERE0, "w33_f8_exact_witness.py")).read(); exec(src2[:src2.index("g = 2 * mp.cos")],g2)
psi=np.array([complex(z) for z in g2["A"]]); psi/=np.linalg.norm(psi)
Ws=[]
for c in range(4096):
    W=V@Hm(c>>6,c&63)
    if abs(abs(np.vdot(psi,W@psi))-1)<1e-8: Ws.append(W)
print("global Clifford lifts (x Pauli) with the witness as eigenvector:",len(Ws))
W=Ws[0]
o=1; M=W.copy()
while not np.allclose(M, M[0,0]*np.eye(64), atol=1e-8): M=M@W; o+=1
print("projective order of W:",o)
Wn=W/M[0,0]**(1/o); ev,U_=np.linalg.eig(Wn)
_, fgf = gl["model"](3)
groups=[]
for i,e in enumerate(ev):
    for gp in groups:
        if abs(ev[gp[0]]-e)<1e-6: gp.append(i); break
    else: groups.append([i])
lam=np.vdot(psi,Wn@psi)
rng_=np.random.default_rng(5); out={}
for gi,idx in enumerate(groups):
    Q_,_=np.linalg.qr(U_[:,idx]); m=Q_.shape[1]
    def f(wv):
        A=Q_@(wv[:m]+1j*wv[m:]); val,gr=fgf(np.concatenate([A.real,A.imag])); G=Q_.conj().T@(gr[:64]+1j*gr[64:]); return val,np.concatenate([G.real,G.imag])
    best=min(minimize(f,rng_.standard_normal(2*m),jac=True,method="L-BFGS-B",options=dict(maxiter=20000,gtol=1e-12,ftol=1e-16)).fun*64 for _ in range(30))
    k=int(round(np.angle(ev[idx[0]])/(2*np.pi/o)))%o
    wit=bool(abs(ev[idx[0]]-lam)<1e-6)
    out[k]=(m,round(best,10),wit); print("eigenvalue exp(2 pi i %d/%d) dim %d min 64F %.10f %s"%(k,o,m,best,"(witness)" if wit else ""),flush=True)
jw=[k for k,v in out.items() if v[2]][0]
json.dump(dict(n_lifts_fixing=len(Ws),projective_order=o,eigenspaces={str(j):dict(dim=m,min_c=v,witness=w) for j,(m,v,w) in out.items()},witness_k=jw,c8=C8),
          open(os.path.join(HERE0, "..", "data", "w33_f8_global_torus_eigenspaces.json"),"w"),indent=1)
