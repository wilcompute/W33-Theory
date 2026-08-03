#!/usr/bin/env python3
"""Pass 2947: compile the explicit deep-M36 branch and exhaust its Pauli faults."""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT2947_M36_COMPILED_BRANCH_results.json';N=4
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex);H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2);P={'I':I,'X':X,'Y':Y,'Z':Z}
def kron(xs):
 out=np.array([[1]],complex)
 for x in xs:out=np.kron(out,x)
 return out
def one(U,q):return kron([U if i==q else I for i in range(N)])
def cx(c,t):
 U=np.zeros((16,16),complex)
 for bits in itertools.product((0,1),repeat=N):
  out=list(bits);out[t]^=out[c];ii=sum(bits[i]<<(N-1-i) for i in range(N));jj=sum(out[i]<<(N-1-i) for i in range(N));U[jj,ii]=1
 return U
def pv(s):return tuple([int(c in 'XY') for c in s]+[int(c in 'ZY') for c in s])
def gate_v(v,g):
 v=list(v)
 if g[0]=='H':q=g[1];v[q],v[N+q]=v[N+q],v[q]
 elif g[0]=='CX':c,t=g[1:];v[t]^=v[c];v[N+c]^=v[N+t]
 elif g[0]=='SW':a,b=g[1:];v[a],v[b]=v[b],v[a];v[N+a],v[N+b]=v[N+b],v[N+a]
 return tuple(v)
abstract=[('CX',0,1),('CX',0,2),('H',0),('CX',1,3),('H',1),('CX',1,3),('CX',3,2),('CX',0,3),('SW',0,2),('SW',1,3),('H',3)]
primitive=[]
for g in abstract:primitive += [('CX',g[1],g[2]),('CX',g[2],g[1]),('CX',g[1],g[2])] if g[0]=='SW' else [g]
Us=[one(H,g[1]) if g[0]=='H' else cx(g[1],g[2]) for g in primitive]
s1,s2,l1,l2=pv('IYZY'),pv('YZXY'),(1,1,1,0,0,0,0,0),(0,1,0,1,0,0,0,0);rows=[s1,s2,l1,l2]
for g in abstract[:-1]:rows=[gate_v(v,g) for v in rows]
standard=[tuple([0]*4+[int(i==q) for i in range(4)]) for q in range(4)];assert rows==standard
w=np.exp(2j*np.pi/3);rays=[]
for family in range(4):
 for mu in range(3):
  for nu in range(3):
   raw=([0,1,-w**mu,w**nu] if family==0 else [1,0,-w**mu,-w**nu] if family==1 else [1,-w**mu,0,w**nu] if family==2 else [1,w**mu,w**nu,0]);rays.append(np.asarray(raw,complex)/np.sqrt(3))
psi=np.kron(rays[5],rays[5]);state=psi
for U in Us:state=U@state
def evaluate(st,flip0=0,flip1=0):
 T=st.reshape(2,2,2,2);out=T[0^flip0,1^flip1,:,:].reshape(4);pa=float(np.vdot(out,out).real)
 if pa<1e-12:return pa,None
 out/=np.sqrt(pa);return pa,float(abs(np.vdot(rays[7],out))**2)
ideal=evaluate(state);assert abs(ideal[0]-.5)<1e-10 and abs(ideal[1]-1)<1e-10
faults=[];prefix=psi
for li,(g,U) in enumerate(zip(primitive,Us)):
 prefix=U@prefix;support=[g[1]] if g[0]=='H' else [g[1],g[2]]
 for label in (''.join(s) for s in itertools.product('IXYZ',repeat=len(support)) if any(c!='I' for c in s)):
  ops=[I]*4
  for q,c in zip(support,label):ops[q]=P[c]
  st=kron(ops)@prefix
  for V in Us[li+1:]:st=V@st
  pa,f=evaluate(st);cl='rejected' if pa<1e-10 else 'benign' if f and f>1-1e-9 else 'accepted_bad';faults.append({'location':li,'gate':list(g),'fault':label,'accept_probability':pa,'conditional_fidelity':f,'class':cl})
for bit in (0,1):
 pa,f=evaluate(state,int(bit==0),int(bit==1));faults.append({'location':len(primitive)+bit,'gate':['MZ',bit],'fault':'classical_flip','accept_probability':pa,'conditional_fidelity':f,'class':'rejected' if pa<1e-10 else 'benign' if f and f>1-1e-9 else 'accepted_bad'})
loc=defaultdict(list)
for r in faults:loc[r['location']].append(r)
coeff={k:sum(r['accept_probability']*(1-(r['conditional_fidelity'] or 0)) for r in rr)/len(rr) for k,rr in loc.items()};oneq=[2,4,14];twoq=[i for i in range(15) if i not in oneq];meas=[15,16]
def conditional(keys):return Fraction(2*sum(coeff[k] for k in keys)).limit_denominator()
c1,c2,cm=conditional(oneq),conditional(twoq),conditional(meas);assert (c1,c2,cm)==(Fraction(140,81),Fraction(2084,405),Fraction(4,9))
checks={'decoder_maps_ordered_generators_to_Z':rows==standard,'ideal_acceptance_one_half':abs(ideal[0]-.5)<1e-10,'ideal_output_ray7':abs(ideal[1]-1)<1e-10,'primitive_gate_count_15':len(primitive)==15,'fault_event_count_191':len(faults)==191,'exact_first_order_coefficients':(c1,c2,cm)==(Fraction(140,81),Fraction(2084,405),Fraction(4,9))}
out={'schema':'w33.pass2947.m36_compiled_branch.v1','status':'COMPLETE_EXACT_CIRCUIT_AND_PAULI_MODEL','checks':checks,'check_count':len(checks),'input_ray':5,'output_ray':7,'stabilizers':['IYZY','YZXY'],'syndrome':[-1,1],'decoded_accept_bits':[0,1],'logical_operation':'H on decoded qubit 3','abstract_decoder_and_logical_gates':[list(g) for g in abstract],'primitive_gates':[list(g) for g in primitive],'primitive_gate_count':len(primitive),'measurement_count':2,'ideal_success_probability':ideal[0],'fault_model':'after each one-qubit gate: uniform X/Y/Z; after each CNOT: uniform 15 nonidentity two-qubit Paulis; each Z measurement has one classical bit-flip event','fault_event_count':len(faults),'fault_class_histogram':dict(Counter(r['class'] for r in faults)),'accepted_bad_fidelity_histogram':{str(k):v for k,v in Counter(round(r['conditional_fidelity'],12) for r in faults if r['class']=='accepted_bad').items()},'first_order_output_infidelity':'(2/3)p + (140/81)q1 + (2084/405)q2 + (4/9)qm + higher order','coefficients':{'input':'2/3','one_qubit':'140/81','two_qubit':'2084/405','measurement':'4/9'},'fault_rows':faults,'claim_boundary':'Exact for the stated decoder, direct-Z measurement, and stochastic Pauli/bit-flip model. It is not a coherent-error threshold, leakage model, or hardware calibration.'};assert all(checks.values());OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(f"PASS {len(checks)}/{len(checks)}",out['first_order_output_infidelity'])
