"""
Symplectic / Clifford extension facts for the Witting 40-ray PG(3,3) model.

This file is self-contained and uses only finite-field arithmetic mod 3.

Key objects:
- V = F3^4 with symplectic form J0 (alternating bilinear).
- PG(3,3) points are 1D subspaces of V; we use normalized representatives.
- The 40 Witting rays are identified with the 40 PG points (nonzero vectors mod ±1).
- Ω(i,j,k) (ordered triple) is 0 iff collinear; otherwise Ω = ω(i,j) ω(j,k) ω(k,i).

Group layer:
- PSp(4,3) (order 25920) acts on the 40 points and preserves Ω.
- The Heisenberg group H(V) = V × F3 with multiplication (v,t)*(w,s)=(v+w, t+s+2ω(v,w))
  is the central extension underlying qutrit Pauli phases.
- The full 2-qutrit Clifford group has shape H(V) ⋊ Sp(4,3), order 3^5 * 51840 = 12,597,120.
"""

import itertools
import numpy as np

MOD=3

J0 = np.array([[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]], dtype=int) % MOD

# 40 normalized projective points (representatives) in F3^4
COORD = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (1, 0, 0, 0), (1, 0, 0, 2), (0, 1, 0, 1), (1, 2, 2, 1), (1, 0, 2, 2), (1, 1, 2, 0), (1, 1, 0, 0), (1, 1, 1, 0), (0, 0, 1, 0), (1, 2, 1, 0), (1, 2, 0, 1), (0, 1, 1, 1), (1, 0, 1, 2), (0, 1, 2, 0), (1, 1, 0, 1), (0, 1, 1, 2), (1, 0, 1, 0), (0, 1, 2, 2), (1, 2, 0, 0), (1, 2, 2, 0), (1, 0, 2, 1), (1, 1, 2, 2), (0, 1, 0, 2), (1, 1, 1, 1), (0, 0, 1, 1), (1, 2, 1, 1), (1, 2, 0, 2), (1, 1, 1, 2), (0, 0, 1, 2), (1, 2, 1, 2), (0, 1, 0, 0), (0, 1, 1, 0), (1, 0, 1, 1), (0, 1, 2, 1), (1, 1, 0, 2), (1, 2, 2, 2), (1, 0, 2, 0), (1, 1, 2, 1)], dtype=int) % MOD

def norm_vec(v):
    v=[int(x)%MOD for x in v]
    for x in v:
        if x!=0:
            if x==2:
                v=[(2*y)%MOD for y in v]
            return tuple(v)
    raise ValueError("zero vector")

coord_to_pt={tuple(COORD[i].tolist()): i for i in range(40)}

def omega(u,v):
    """Symplectic pairing ω(u,v) = u^T J0 v in F3."""
    u=np.array(u,dtype=int).reshape((4,1))%MOD
    v=np.array(v,dtype=int).reshape((4,1))%MOD
    return int((u.T @ J0 @ v)[0,0]) % MOD

# Orthogonality on PG points (ω=0)
ORTH=set()
for i in range(40):
    for j in range(i+1,40):
        if omega(COORD[i],COORD[j])==0:
            ORTH.add((i,j))

def is_collinear(i,j,k):
    """Collinearity in PG(3,3): v_k ∈ span(v_i,v_j)."""
    u=COORD[i]; v=COORD[j]; w=COORD[k]
    for a in (0,1,2):
        for b in (0,1,2):
            if a==0 and b==0:
                continue
            if np.all((a*u + b*v)%MOD == w%MOD):
                return True
    return False

def Omega(i,j,k):
    """Ordered Ω_mod3 for a triple (i,j,k) of distinct points.
    Returns None if any edge is orthogonal."""
    a,b=sorted((i,j))
    if (a,b) in ORTH: return None
    a,b=sorted((j,k))
    if (a,b) in ORTH: return None
    a,b=sorted((k,i))
    if (a,b) in ORTH: return None
    if is_collinear(i,j,k):
        return 0
    return (omega(COORD[i],COORD[j]) * omega(COORD[j],COORD[k]) * omega(COORD[k],COORD[i])) % MOD

# -------- Symplectic transvections generate Sp(4,3) --------

I=np.eye(4,dtype=int)%MOD

def symp_transvection_matrix(v):
    v=np.array(v,dtype=int).reshape((4,1))%MOD
    w=(J0@v)%MOD
    return (I + (v@w.T))%MOD

def act_on_point(M, coord):
    v=np.array(coord,dtype=int).reshape((4,1))%MOD
    w=(M@v)%MOD
    return norm_vec(w.reshape(-1).tolist())

def induced_perm(M):
    return tuple(coord_to_pt[act_on_point(M, COORD[p])] for p in range(40))

def preserves_Omega(perm):
    for i in range(40):
        for j in range(40):
            if j==i: continue
            for k in range(40):
                if k==i or k==j: continue
                om=Omega(i,j,k)
                if om is None: 
                    continue
                om2=Omega(perm[i],perm[j],perm[k])
                if om2!=om:
                    return False
    return True

# -------- Heisenberg group H(V) = V × F3 --------
# group law uses factor 2 (=1/2 mod 3) so commutator is exactly ω(v,w)

def H_mul(x,y):
    """Multiply in Heisenberg group: (v,t)*(w,s) = (v+w, t+s + 2ω(v,w))."""
    v,t=x
    w,s=y
    v=np.array(v,dtype=int)%MOD
    w=np.array(w,dtype=int)%MOD
    tw=(t + s + 2*omega(v,w))%MOD
    return ((v+w)%MOD, tw)

def H_inv(x):
    v,t=x
    v=np.array(v,dtype=int)%MOD
    # inverse: (-v, -t) because ω(v,v)=0 (alternating)
    return ((-v)%MOD, (-t)%MOD)

def H_comm(x,y):
    """Commutator [x,y] in H(V)."""
    return H_mul(H_mul(x,y), H_mul(H_inv(x), H_inv(y)))

def demo_commutator():
    # returns True if commutator matches ω(v,w) in central coord for random samples
    for _ in range(200):
        v=np.array([np.random.randint(0,3) for _ in range(4)],dtype=int)%MOD
        w=np.array([np.random.randint(0,3) for _ in range(4)],dtype=int)%MOD
        x=(v,0); y=(w,0)
        com=H_comm(x,y)  # should be (0, ω(v,w))
        if np.any(com[0]%MOD):
            return False
        if com[1]%MOD != omega(v,w)%MOD:
            return False
    return True

if __name__=="__main__":
    # quick generator/invariance smoke test
    gens=[
        symp_transvection_matrix((1,0,0,0)),
        symp_transvection_matrix((0,1,0,0)),
        symp_transvection_matrix((0,0,1,0)),
        symp_transvection_matrix((0,0,0,1)),
    ]
    perms=[induced_perm(M) for M in gens]
    print("Ω invariant under generators:", all(preserves_Omega(p) for p in perms))
    print("Heisenberg commutator test:", demo_commutator())
