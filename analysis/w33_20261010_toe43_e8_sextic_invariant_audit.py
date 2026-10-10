"""TOE43 E8 84 independent audit: non-holomorphic degree-six invariants.
Tests SU(9) invariant 3-T/3-Tbar contraction diagrams along normalized
Vinberg Cartan and checks under seeded random unitary.
"""
from pathlib import Path
import sys, itertools, json, time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass11681_e8_from_two_qutrits as E
rng=np.random.default_rng(4321)
H=np.array(E.cartan_trivectors())
def tri(c):
 T=E.full(c@H).astype(complex)
 return T/np.linalg.norm(T)
rays=[np.eye(4,dtype=complex)[0],np.eye(4,dtype=complex)[1]]
for i in range(4):
 c=rng.normal(size=4)+1j*rng.normal(size=4)
 rays.append(c/np.linalg.norm(c))
Ts=[tri(c) for c in rays]
s="abcdefghi"
def contract(T,perm):
 tt=T.conj()
 pat="abc,def,ghi,"+",".join("".join(s[p] for p in perm[3*j:3*j+3]) for j in range(3))+"->"
 return complex(np.einsum(pat,T,T,T,tt,tt,tt,optimize="greedy")),pat
perms=[list(range(9))]
for i in range(55):
 perms.append(rng.permutation(9).tolist())
rows=[]
for perm in perms:
 try:
  vals=[contract(t,perm)[0] for t in Ts[:3]]
 except ValueError as e:
  print("SKIP",str(e),flush=True);continue
 score=float(max(abs(vals[0]-v) for v in vals[1:]))
 if score>1e-7:
  rows.append((score,perm,vals,contract(Ts[0],perm)[1]))
print("SAMPLES",len(perms),"VARIABLE_INVARIANTS",len(rows),flush=True)
for score,p,v,pat in sorted(rows,key=lambda z:-z[0])[:7]:
 print("CANDIDATE",score,pat,"values",v,flush=True)
if rows:
 _,perm,vals,pat=sorted(rows,key=lambda z:-z[0])[0]
 z=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
 Q,_=np.linalg.qr(z)
 transformed=np.einsum("ai,bj,ck,ijk->abc",Q,Q,Q,Ts[2],optimize=True)
 before=contract(Ts[2],perm)[0]
 after=contract(transformed,perm)[0]
 print("UNITARY_INVARIANT",abs(before-after),before,after,flush=True)
 assert abs(before-after)<1e-8
else:
 print("NO_VARIABLE_IN_SAMPLE; DOES NOT PROVE DEGREE6 FLATNESS",flush=True)
