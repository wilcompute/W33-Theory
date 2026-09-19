#!/usr/bin/env python3
"""CZ_3 + parity restores the physical C6 on the oriented 80-state Pauli/A8 lift.

Cross-track input (Holotrade commit 1d03cbb4):
the flagship Z6-I model has two commuting SU(9) holonomies whose joint
root census equals the joint spectrum of (CZ_3, parity).

This certificate proves the finite W33/Pauli side exactly.

Let Pauli labels be v=(x1,x2,z1,z2) in F3^4\{0}.  In the standard convention

  CZ: (x1,x2,z1,z2) -> (x1,x2,z1+x2,z2+x1)
  P : v -> -v.

Then CZ has order 3, P has order 2, they commute, and G=CZ*P has order 6.
Thus <CZ,P> ~= C3 x C2 ~= C6.

Projectivization kills P because [v]=[-v].  Consequently on W33 points:
  P   : 1^40
  CZ  : 1^4 3^12
  G   : 1^4 3^12.

On the 80 nonzero oriented Pauli vectors:
  P   : 2^40
  CZ  : 1^8 3^24
  G   : 2^4 6^12.

The eight CZ-fixed vectors are the nonzero vectors of one 2D isotropic
subspace; projectively they are the four points of one W33 line.

Representation-level check.
Use the naive Pauli monomials
  X1^a X2^b Z1^c Z2^d.
Parity contributes no phase.  Conjugation by CZ sends
  X1^a X2^b Z1^c Z2^d
to
  omega^(ab) X1^a X2^b Z1^(c+b) Z2^(d+a).
Therefore G=CZ*P maps a Pauli monomial along the F3^4 label action with
phase omega^(ab).  For every one of the 4 two-cycles and 12 six-cycles of G,
the accumulated phase exponent is 0 mod 3.  Hence the Pauli basis can be
rephased cycle-by-cycle so that Ad(G) is literally the permutation
2^4 6^12.

Its six C6 eigenvalue multiplicities on sl9 are therefore
  [16,12,12,16,12,12].
The imported heterotic joint root census is
  (a,b)=(0,0):8, (0,1):16,
        (1,0):12,(1,1):12,(2,0):12,(2,1):12.
Adding the eight Cartan directions to (0,0) and mapping the joint character
omega^a(-1)^b to zeta_6^(2a+3b) gives exactly the same multiplicities.

This explains a key visibility issue:
the physical even-order ingredient is invisible on bare projective W33, but
is exact on its oriented 80-state Pauli/sl9 lift.

Scope:
- exact finite Clifford/Pauli and imported heterotic-adjoint census statement;
- no claim that the heterotic lattice has yet been canonically identified with
  the repository's preferred Pauli basis;
- no claim that the separate E8 C6 fiber is this same C6 action.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_cz_parity_oriented_c6.json'
MOD=3

I=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1))
CZ=((1,0,0,0),(0,1,0,0),(0,1,1,0),(1,0,0,1))
P=((2,0,0,0),(0,2,0,0),(0,0,2,0),(0,0,0,2))

def mm(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(4))%MOD
                       for j in range(4)) for i in range(4))

def mv(A,v):
    return tuple(sum(A[i][j]*v[j] for j in range(4))%MOD for i in range(4))

def mpow(A,n):
    R=I
    for _ in range(n): R=mm(R,A)
    return R

def order(A):
    R=I
    for n in range(1,25):
        R=mm(R,A)
        if R==I:return n
    raise AssertionError("order too large")

def canon(v):
    nz=next(x for x in v if x)
    return tuple((2*x)%3 for x in v) if nz==2 else tuple(v)

def cycles(items,act):
    idx={x:i for i,x in enumerate(items)}
    perm=[idx[act(x)] for x in items]
    seen=set(); out=[]
    for i in range(len(items)):
        if i in seen: continue
        u=i; orb=[]
        while u not in seen:
            seen.add(u);orb.append(items[u]);u=perm[u]
        out.append(orb)
    return out

def symp(v,w):
    return (v[0]*w[2]+v[1]*w[3]-v[2]*w[0]-v[3]*w[1])%3

def main(write=True):
    G=mm(CZ,P)
    assert mm(CZ,P)==mm(P,CZ)
    assert order(CZ)==3 and order(P)==2 and order(G)==6

    # generated matrix group
    group={mpow(G,n) for n in range(6)}
    assert len(group)==6
    assert CZ in group and P in group

    V=sorted(v for v in itertools.product(range(3),repeat=4) if any(v))
    PP=sorted({canon(v) for v in V})
    assert len(V)==80 and len(PP)==40

    cP=cycles(PP,lambda v:canon(mv(P,v)))
    cCZ=cycles(PP,lambda v:canon(mv(CZ,v)))
    cG=cycles(PP,lambda v:canon(mv(G,v)))
    pvP=Counter(map(len,cP)); pvCZ=Counter(map(len,cCZ)); pvG=Counter(map(len,cG))
    assert pvP==Counter({1:40})
    assert pvCZ==Counter({3:12,1:4})
    assert pvG==pvCZ

    vP=Counter(map(len,cycles(V,lambda v:mv(P,v))))
    vCZ=Counter(map(len,cycles(V,lambda v:mv(CZ,v))))
    gcycles=cycles(V,lambda v:mv(G,v))
    vG=Counter(map(len,gcycles))
    assert vP==Counter({2:40})
    assert vCZ==Counter({3:24,1:8})
    assert vG==Counter({6:12,2:4})

    fixed=[v for v in PP if canon(mv(CZ,v))==v]
    assert len(fixed)==4
    assert all(symp(a,b)==0 for a,b in itertools.combinations(fixed,2))

    # Exact phase accumulation for naive Pauli monomials under G=CZ*P.
    # If v=(a,b,c,d), parity sends v->-v and CZ contributes omega^(ab).
    phase_sums=[]
    for orb in gcycles:
        s=sum((v[0]*v[1])%3 for v in orb)%3
        phase_sums.append((len(orb),s))
        assert s==0
    assert Counter(phase_sums)==Counter({(6,0):12,(2,0):4})

    # Pure permutation C6 spectrum from 2^4 6^12.
    pauli_mult=[12]*6
    pauli_mult[0]+=4
    pauli_mult[3]+=4
    assert pauli_mult==[16,12,12,16,12,12]

    # Imported heterotic root joint census from Holotrade 1d03cbb4.
    root_joint={(0,0):8,(0,1):16,(1,0):12,(1,1):12,(2,0):12,(2,1):12}
    adj_joint=dict(root_joint)
    adj_joint[(0,0)]+=8  # Cartan of sl9
    het=[0]*6
    for (a,b),m in adj_joint.items():
        het[(2*a+3*b)%6]+=m
    assert het==pauli_mult

    out={
      'schema':'w33.cz_parity_oriented_c6.v1',
      'status':'PASS',
      'headline':'The flagship-compatible pair (CZ_3, parity) generates C6 on the oriented two-qutrit Pauli/sl9 lift. Parity is the central symplectic -I, hence disappears on projective W33 but acts nontrivially on the 80 oriented Pauli vectors. The order-six product has vector cycle type 2^4 6^12 and, after exact phase-cycle cancellation, adjoint C6 multiplicities 16,12,12,16,12,12, exactly matching the imported heterotic joint-adjoint spectrum.',
      'group':{
        'CZ_order':3,'parity_order':2,'commute':True,
        'generated_group':'C3 x C2 ~= C6','product_order':6},
      'projective_W33':{
        'parity_cycles':{'1':40},
        'CZ_cycles':{'1':4,'3':12},
        'CZ_times_parity_cycles':{'1':4,'3':12},
        'fixed_four':'one isotropic W33 line',
        'reading':'projectivization quotients out the central parity C2'},
      'oriented_80':{
        'parity_cycles':{'2':40},
        'CZ_cycles':{'1':8,'3':24},
        'CZ_times_parity_cycles':{'2':4,'6':12},
        'naive_Pauli_conjugation_phase':'omega^(x1*x2)',
        'phase_product_on_every_cycle':'1',
        'rephasable_to_pure_permutation':True,
        'C6_eigenvalue_multiplicities':pauli_mult},
      'heterotic_import':{
        'source_repo':'wilcompute/Holotrade',
        'source_commit':'1d03cbb4fb0cfeac7a0e6b455231f715db8f8ce1',
        'root_joint_census':{f'{a},{b}':m for (a,b),m in root_joint.items()},
        'Cartan_added_to_0_0':8,
        'C6_character_map':'(a,b) -> 2a+3b mod 6',
        'adjoint_C6_multiplicities':het,
        'exact_match_to_oriented_Pauli_adjoint':True},
      'literature_boundary':{
        'classical':'generalized Pauli/Clifford modular arithmetic for qudits',
        'reference':'Hostens-Dehaene-De Moor, Phys. Rev. A 71, 042315 (2005), quant-ph/0408190',
        'new_repo_weld':'the exact heterotic joint-adjoint / oriented-Pauli C6 match and the projective-visibility explanation'},
      'scope':'Exact finite representation fingerprint. It does not supply the still-open canonical lattice-to-Pauli basis identification and does not identify this C6 with the separate E8 Coxeter-fiber C6.'
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__':main(True)
