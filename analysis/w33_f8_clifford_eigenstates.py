"""Pass 12672: the F_8 regulus minimiser is a Clifford eigenstate.  On the 8-dim code space of T (Pass 12671), sigma (the unique
symplectic map cycling the nine effective Lagrangians; multiplication by an order-9 element of F_64, w33_f8_effective_three_qubit.py)
has 64 Clifford lifts V (8x8 unitaries with V E_a V^dagger ~ E_{sigma(a)}).  Each V^9 is scalar; normalised so V^9 = I its spectrum is
all ninth roots of unity but one.  With j measured from the absent root, the eigenvector psi_j of zeta_9^j has
    64 F(psi_j) = (47 - 32 cos(4 pi j/9))/9   (j = +-1, +-2, +-4: the three roots of 243c^3 - 3807c^2 + 17577c - 23941),
    64 F(psi_j) = 37/3                         (j = +-3),
for all 64 lifts (512 eigenvectors); the minimum c8 is j = +-4, and exactly one lift fixes the Pass 12671 exact witness (as a
1-dim eigenspace).  usage: py -3 analysis/w33_f8_clifford_eigenstates.py"""
import os, json, itertools
import numpy as np, mpmath as mp
HERE0 = os.path.dirname(os.path.abspath(__file__)); __file__ = os.path.join(HERE0, "w33_f8_effective_three_qubit.py")
exec(open(__file__).read())
# code-space basis and witness (double precision from the 45-digit minimiser)
Hh=[-1j*pauli(12,53), pauli(53,33), pauli(1,6)]
Pr=np.eye(64,dtype=complex)
for X in Hh: Pr=Pr@(np.eye(64)+X)/2
w_,V_=np.linalg.eigh((Pr+Pr.conj().T)/2); B=V_[:,w_>0.5]
d=json.load(open(os.path.join(HERE0, "..", "data", "w33_f8_rank3_stabiliser_exact.json")))
src2=open(os.path.join(HERE0, "w33_f8_exact_witness.py")).read()
# rebuild psi via the same construction as the witness script (mp -> complex)
g2={"__name__":"x","__file__":os.path.join(HERE0, "w33_f8_exact_witness.py")}
exec(src2[:src2.index("g = 2 * mp.cos")],g2)
psi=np.array([complex(z) for z in g2["A"]]); psi/=np.linalg.norm(psi)
assert np.allclose(B@(B.conj().T@psi),psi)
t=B.conj().T@psi
E=[B.conj().T@pauli(*k)@B for k in basisE]          # effective Paulis (8x8), coords = basis vectors
def effP(a):
    M=np.eye(8,dtype=complex)
    for i in range(6):
        if a>>i&1: M=M@E[i]
    return M
imgs=[effP(apply(s,1<<i)) for i in range(6)]
sols=[]
for ph in itertools.product([1,-1,1j,-1j],repeat=6):
    # V E_i - ph_i imgs_i V = 0 , linear in vec(V)
    rows=[np.kron(np.eye(8),E[i].T)-ph[i]*np.kron(imgs[i],np.eye(8)) for i in range(6)]
    A=np.vstack(rows); u,sv,vh=np.linalg.svd(A)
    if sv[-1]<1e-9:
        V=vh[-1].conj().reshape(8,8); V=V/np.sqrt(abs(np.linalg.det(V)))**(1/4) if False else V*np.sqrt(8)/np.linalg.norm(V)
        if np.allclose(V@V.conj().T,np.eye(8),atol=1e-8): sols.append(V)
print("Clifford lifts found:",len(sols))
res=[]
for V in sols:
    ov=abs(np.vdot(t,V@t))
    if ov>1-1e-8:
        ev=np.linalg.eigvals(V); lam=np.vdot(t,V@t)
        # order of V up to phase
        M=V.copy(); o=1
        while not np.allclose(M, M[0,0]*np.eye(8) if abs(M[0,0])>1e-6 else np.zeros(8)) and o<100:
            M=M@V; o+=1
        mult=sum(abs(e-lam)<1e-6 for e in ev)
        res.append((o,mult))
print("lifts fixing the witness (order up to phase, eigenspace dim of witness):",res)
_, fgf = gl["model"](3)
def F64(v):
    A=B@v; A/=np.linalg.norm(A); return fgf(np.concatenate([A.real,A.imag]))[0]*64
from scipy.optimize import minimize
vals=[]
for li,V in enumerate(sols):
    ev,U_=np.linalg.eig(V)
    # group eigenvalues
    groups=[]
    for i,e in enumerate(ev):
        for gp in groups:
            if abs(ev[gp[0]]-e)<1e-6: gp.append(i); break
        else: groups.append([i])
    for gp in groups:
        Q_,_=np.linalg.qr(U_[:,gp])
        if len(gp)==1: vals.append((F64(Q_[:,0]),li,1))
        else:
            m=len(gp)
            def f(w):
                return F64(Q_@(w[:m]+1j*w[m:]))
            best=min(minimize(f,np.random.default_rng(i).standard_normal(2*m),method="BFGS").fun for i in range(6))
            vals.append((best,li,m))
vals.sort()
import collections
print("eigenspace dims histogram:",collections.Counter(v[2] for v in vals))
print("lowest candidate values:",[ (round(v[0],10),v[2]) for v in vals[:6]])
print("c8 =",C8,"; candidates attaining c8:",sum(abs(v[0]-C8)<1e-8 for v in vals))
print("distinct values:",sorted(collections.Counter(round(v[0],6) for v in vals).items())[:12])
tab=collections.defaultdict(collections.Counter)
for V in sols:
    # normalise V projectively so that V^9 = I
    M=np.linalg.matrix_power(V,9); ph=M[0,0]; V9=V/ph**(1/9)
    assert np.allclose(np.linalg.matrix_power(V9,9),np.eye(8),atol=1e-8)
    ev,U_=np.linalg.eig(V9)
    for i,e in enumerate(ev):
        # e = zeta9^j * zeta9^m ambiguity from choice of 9th root: record j relative to the missing eigenvalue
        tab[None][round(F64(U_[:,i]),6)]+=0
    js=sorted(int(round((np.angle(e)/(2*np.pi/9))))%9 for e in ev)
    missing=[j for j in range(9) if j not in js]
    assert len(missing)==1
    for i,e in enumerate(ev):
        j=(int(round(np.angle(e)/(2*np.pi/9)))-missing[0])%9
        tab[j][round(F64(U_[:,i]),6)]+=1
print("eigenvalue zeta9^j (j relative to the absent eigenvalue) -> F values:")
for j in range(1,9): print(j, dict(tab[j]))
import math
closed = {j: (47 - 32 * math.cos(4 * math.pi * j / 9)) / 9 for j in (1, 2, 4, 5, 7, 8)}; closed[3] = closed[6] = 37 / 3
maxdev = 0.0; per_j = {}
for V in sols:
    M = np.linalg.matrix_power(V, 9); V9 = V / M[0, 0] ** (1 / 9)
    ev, U_ = np.linalg.eig(V9)
    js = [int(round(np.angle(e) / (2 * np.pi / 9))) % 9 for e in ev]; missing = [j for j in range(9) if j not in js][0]
    for i, e in enumerate(ev):
        j = (js[i] - missing) % 9; v = F64(U_[:, i]); maxdev = max(maxdev, abs(v - closed[j])); per_j.setdefault(j, []).append(v)
fix = [V for V in sols if abs(np.vdot(t, V @ t)) > 1 - 1e-8]
out = dict(n_lifts=len(sols), n_eigenvectors=sum(len(v) for v in per_j.values()), max_deviation_from_closed_forms=maxdev,
           counts_per_j={str(j): len(v) for j, v in sorted(per_j.items())}, lifts_fixing_witness=len(fix), witness_lift=res)
print(out)
json.dump(out, open(os.path.join(HERE0, "..", "data", "w33_f8_clifford_eigenstates.json"), "w"), indent=1, default=str)
