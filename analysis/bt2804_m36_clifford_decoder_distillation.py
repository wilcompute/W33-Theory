#!/usr/bin/env python3
"""Pass 2804: exhaustive two-copy M36 distillation with logical Clifford decoding."""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];SQ3=sp.sqrt(3);p=sp.symbols('p',real=True)
I2=np.eye(2,complex);X=np.array([[0,1],[1,0]],complex);Z=np.array([[1,0],[0,-1]],complex)
H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2);S=np.diag([1,1j])
def kron(ms):
 o=np.array([[1]],complex)
 for m in ms:o=np.kron(o,m)
 return o
def pkey(v,d=9):
 v=np.asarray(v,complex).reshape(-1);v/=np.linalg.norm(v);i=next(i for i,z in enumerate(v) if abs(z)>1e-9);v/=v[i]/abs(v[i]);return tuple((round(float(z.real),d),round(float(z.imag),d)) for z in v)
def mkey(M,d=9):
 a=M.reshape(-1);i=next(i for i,z in enumerate(a) if abs(z)>1e-9);M=M/(a[i]/abs(a[i]));return tuple((round(float(z.real),d),round(float(z.imag),d)) for z in M.reshape(-1))
def cliffords():
 c01=np.zeros((4,4),complex);c10=np.zeros((4,4),complex)
 for a,b in itertools.product(range(2),repeat=2):c01[2*a+(b^a),2*a+b]=1;c10[2*(a^b)+b,2*a+b]=1
 gs=[np.kron(H,I2),np.kron(I2,H),np.kron(S,I2),np.kron(I2,S),c01,c10];I=np.eye(4,complex);seen={mkey(I):I};q=deque([I])
 while q:
  x=q.popleft()
  for g in gs:
   y=g@x;k=mkey(y)
   if k not in seen:seen[k]=y;q.append(y)
 assert len(seen)==11520;return list(seen.values())
def rays():
 w=np.exp(2j*np.pi/3);R=[];meta=[]
 for f in range(4):
  for mu in range(3):
   for nu in range(3):
    raw=[0,1,-w**mu,w**nu] if f==0 else [1,0,-w**mu,-w**nu] if f==1 else [1,-w**mu,0,w**nu] if f==2 else [1,w**mu,w**nu,0]
    R.append(np.array(raw,complex)/np.sqrt(3));meta.append((f,mu,nu))
 return R,meta
def bvec(i):return tuple((i>>k)&1 for k in range(8))
def bxor(a,b):return tuple(x^y for x,y in zip(a,b))
def symp(a,b):return sum(a[i]*b[4+i]+a[4+i]*b[i] for i in range(4))%2
def pauli(v):return kron([(1j**(x*z))*np.linalg.matrix_power(X,x)@np.linalg.matrix_power(Z,z) for x,z in zip(v[:4],v[4:])])
PAULI={bvec(i):pauli(bvec(i)) for i in range(256)}
def spaces():
 V=[bvec(i) for i in range(1,256)];out=set()
 for i,u in enumerate(V):
  for v in V[i+1:]:
   if not symp(u,v):out.add(tuple(sorted((u,v,bxor(u,v)))))
 assert len(out)==5355;return sorted(out)
def span(bs):
 s={(0,)*8}
 for b in bs:s|={bxor(x,b) for x in tuple(s)}
 return s
def extend(s1,s2):
 bs=[s1,s2];s=span(bs)
 for v in [bvec(i) for i in range(1,256)]:
  if v not in s and all(not symp(v,b) for b in bs):
   bs.append(v);s=span(bs)
   if len(bs)==4:return bs[2],bs[3]
 raise AssertionError
def joint(ops,signs):
 P=np.eye(16,complex);I=np.eye(16,complex)
 for s,o in zip(signs,ops):P=P@((I+s*o)/2)
 j=int(np.argmax(np.linalg.norm(P,axis=0)));v=P[:,j];v/=np.linalg.norm(v);i=next(i for i,z in enumerate(v) if abs(z)>1e-10);v/=v[i]/abs(v[i]);return v
def bases(space):
 s1,s2,_=space;l1,l2=extend(s1,s2);ops=[PAULI[x] for x in (s1,s2,l1,l2)];out={}
 for e1,e2 in itertools.product((1,-1),repeat=2):out[(e1,e2)]=np.column_stack([joint(ops,(e1,e2,z1,z2)) for z1,z2 in itertools.product((1,-1),repeat=2)])
 return out
CACHE={}
def exact(x):
 k=round(float(x),10)
 if abs(k)<1e-9:return sp.Integer(0)
 if k not in CACHE:CACHE[k]=sp.nsimplify(k,[SQ3],tolerance=1e-8,full=False)
 return CACHE[k]
def positive(poly,end):
 roots=[]
 for r in sp.nroots(poly,maxsteps=100):
  if abs(complex(r).imag)<1e-9 and 1e-10<float(sp.re(r))<float(end)-1e-10:roots.append(float(sp.re(r)))
 cuts=[0.0]+sorted(set(round(x,10) for x in roots))+[float(end)]
 return all(float(sp.N(poly.subs(p,(cuts[i]+cuts[i+1])/2),30))>1e-10 for i in range(len(cuts)-1))
def scan(psi,fstab,orbit,subs):
 A=np.outer(psi,psi.conj());B=np.eye(4)/4-A;Cs=[np.kron(A,A),np.kron(A,B)+np.kron(B,A),np.kron(B,B)];end=sp.N(4*(1-fstab)/3,30)
 closed=improving=identical=0;profiles=Counter()
 for sub in subs:
  for syn,V in bases(sub).items():
   L=[V.conj().T@C@V for C in Cs];q=[exact(np.trace(x).real) for x in L]
   if q[0]==0:continue
   vals,vecs=np.linalg.eigh(L[0]/float(q[0]));t=vecs[:,int(np.argmax(vals))]
   if max(vals)<1-1e-8 or pkey(t) not in orbit:continue
   closed+=1;n=[exact(np.real(np.vdot(t,x@t))) for x in L];qp=sum(q[i]*p**i for i in range(3));np_=sum(n[i]*p**i for i in range(3));D=sp.factor(np_-(1-sp.Rational(3,4)*p)*qp)
   if D==0:identical+=1;profiles['identical']+=1
   elif positive(D,end):improving+=1;profiles[str((tuple(q),tuple(n),str(D)))]+=1
   else:profiles['nonimproving']+=1
 return {'closed_branches':closed,'improving_branches':improving,'identical_branches':identical,'profiles':dict(profiles)}
def protocol(R,meta):
 s1=(0,1,0,1,0,1,1,1);s2=(1,0,1,1,1,1,0,1);space=tuple(sorted((s1,s2,bxor(s1,s2))));V=bases(space)[(-1,1)]
 A=np.outer(R[5],R[5].conj());B=np.eye(4)/4-A;L=[V.conj().T@C@V for C in (np.kron(A,A),np.kron(A,B)+np.kron(B,A),np.kron(B,B))]
 q=[exact(np.trace(x).real) for x in L];vals,vecs=np.linalg.eigh(L[0]/float(q[0]));t=vecs[:,int(np.argmax(vals))];D=np.kron(I2,H);target=D@t
 assert pkey(target)==pkey(R[7]);n=[exact(np.real(np.vdot(t,x@t))) for x in L]
 assert q==[sp.Rational(1,2),-sp.Rational(1,2),sp.Rational(1,4)] and n==[sp.Rational(1,2),-sp.Rational(3,4),sp.Rational(5,16)]
 qp=sum(q[i]*p**i for i in range(3));np_=sum(n[i]*p**i for i in range(3));return {'input_id':5,'input_metadata':list(meta[5]),'stabilizer_generators':[list(s1),list(s2),list(bxor(s1,s2))],'syndrome':[-1,1],'decoder':'Hadamard on second logical qubit','target_id':7,'target_metadata':list(meta[7]),'success_probability':str(sp.factor(qp)),'output_fidelity':str(sp.factor(np_/qp)),'difference_from_input':str(sp.factor(np_/qp-(1-sp.Rational(3,4)*p))),'strict_improvement_interval':'0 < p < 2/3','deep_magic_interval':'0 < p < (8-2*sqrt(3))/9'}
def main():
 R,meta=rays();C=cliffords();unseen=set(range(36));orbits=[];union={}
 while unseen:
  seed=min(unseen);K={pkey(U@R[seed]) for U in C};ids=[i for i,r in enumerate(R) if pkey(r) in K]
  for i in ids:unseen.discard(i)
  orbits.append({'seed':seed,'size':len(K),'m36_ids':ids});union.update({k:seed for k in K})
 assert sorted(x['size'] for x in orbits)==[640,960,2880,2880] and len(union)==7360
 subs=spaces();reps={'shallow':(0,sp.Rational(3,4)),'mid_a':(1,(5+2*SQ3)/12),'mid_b':(2,(5+2*SQ3)/12),'deep':(5,(2+SQ3)/6)};res={k:scan(R[i],f,union,subs) for k,(i,f) in reps.items()}
 assert [res[k]['improving_branches'] for k in ('shallow','mid_a','mid_b','deep')]==[0,0,0,48]
 checks={'clifford_order_11520':len(C)==11520,'four_orbits':len(orbits)==4,'union_7360':len(union)==7360,'codes_5355':len(subs)==5355,'deep_improving_48':res['deep']['improving_branches']==48}
 out={'schema':'w33.pass2804.m36_clifford_decoder_distillation.v1','status':'EXACT_EXHAUSTIVE','clifford_group_order':len(C),'m36_clifford_orbits':orbits,'search_space':{'codes':5355,'syndromes_per_code':4,'logical_cliffords':11520},'grade_results':res,'distillation_protocol':protocol(R,meta),'result':'The deep eight-ray grade has 48 improving two-copy branches under full logical Clifford decoding; the explicit H-decoded branch improves throughout the full deep magic-witness interval.','boundary':'State-fidelity distillation, not yet a fault-tolerant injection threshold or asymptotic yield theorem.','checks':checks}
 path=ROOT/'data/PART_BT2804_M36_CLIFFORD_DECODER_DISTILLATION_results.json';path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
