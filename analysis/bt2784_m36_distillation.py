#!/usr/bin/env python3
"""Pass 2784: exhaustive two-copy stabilizer search for an M36 distiller.

The native M36 resource is treated as a two-qubit/ququart pure state. We exhaust all binary [[4,2]] stabilizer subspaces, four syndromes, and one representative of each four two-qubit Clifford orbits inside M36.
"""
from __future__ import annotations
import itertools, json, math
from collections import deque
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
I2=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]).astype(complex)
H=np.array([[1,1],[1,-1]],complex)/math.sqrt(2); S=np.diag([1,1j]).astype(complex)
def canon_unitary(u,tol=1e-9):
 z=next(x for x in u.ravel() if abs(x)>tol); v=u*np.exp(-1j*np.angle(z)); return tuple(np.round(v.real,10).ravel())+tuple(np.round(v.imag,10).ravel())
def canon_state(v,tol=1e-9):
 z=next(x for x in v if abs(x)>tol); w=v*np.exp(-1j*np.angle(z)); return tuple(np.round(w.real,10))+tuple(np.round(w.imag,10))
def two_qubit_clifford():
 cnot=np.zeros((4,4),complex)
 for a,b in itertools.product(range(2),repeat=2): cnot[2*a+(b^a),2*a+b]=1
 gens=[('H0',np.kron(H,I2)),('H1',np.kron(I2,H)),('S0',np.kron(S,I2)),('S1',np.kron(I2,S)),('CX01',cnot)]
 ident=np.eye(4,complex); seen={canon_unitary(ident):(ident,[])}; q=deque([ident])
 while q:
  u=q.popleft(); word=seen[canon_unitary(u)][1]
  for name,g in gens:
   v=u@g; k=canon_unitary(v)
   if k not in seen: seen[k]=(v,word+[name]); q.append(v)
 assert len(seen)==11520
 return [x[0] for x in seen.values()],{k:x[1] for k,x in seen.items()}
def m36_rays():
 w=np.exp(2j*np.pi/3); rays=[]; meta=[]
 for f,mu,nu in itertools.product(range(4),range(3),range(3)):
  raw=[0,1,-w**mu,w**nu] if f==0 else [1,0,-w**mu,-w**nu] if f==1 else [1,-w**mu,0,w**nu] if f==2 else [1,w**mu,w**nu,0]
  rays.append(np.array(raw,complex)/math.sqrt(3)); meta.append((f,mu,nu))
 return rays,meta
def symp(a,b):
 ax,az=a&15,(a>>4)&15; bx,bz=b&15,(b>>4)&15; return ((ax&bz).bit_count()+(az&bx).bit_count())&1
def span_set(basis):
 out={0}
 for b in basis: out|={x^b for x in list(out)}
 return out
def isotropic_rank2_subspaces():
 out=sorted({tuple(sorted((u,v,u^v))) for u in range(1,256) for v in range(u+1,256) if symp(u,v)==0}); assert len(out)==5355; return out
def pauli_matrix(v):
 x,z=v&15,(v>>4)&15; out=np.array([[1]],complex); phase=0
 for q in range(4):
  xb,zb=(x>>q)&1,(z>>q)&1; phase+=xb*zb; out=np.kron(out,np.linalg.matrix_power(X,xb)@np.linalg.matrix_power(Z,zb))
 return (1j**phase)*out
PAULI={v:pauli_matrix(v) for v in range(256)}; I16=np.eye(16,complex)
def logical_completion(space):
 s1,s2,_=space; stab=span_set([s1,s2]); central=[v for v in range(1,256) if symp(v,s1)==0 and symp(v,s2)==0]
 z1=next(v for v in central if v not in stab); z2=next(v for v in central if v not in span_set([s1,s2,z1]) and symp(v,z1)==0)
 x1=next(v for v in central if symp(v,z1)==1 and symp(v,z2)==0); x2=next(v for v in central if symp(v,z1)==0 and symp(v,z2)==1 and symp(v,x1)==0)
 assert len(span_set([s1,s2,z1,z2,x1,x2]))==64; return s1,s2,z1,z2,x1,x2
def code_basis(space,signs):
 s1,s2,z1,z2,x1,x2=logical_completion(space); p=I16.copy()
 for check,sign in zip((s1,s2),signs): p=p@((I16+sign*PAULI[check])/2)
 for lz in (z1,z2): p=p@((I16+PAULI[lz])/2)
 norms=np.linalg.norm(p,axis=0); col=int(np.argmax(norms)); v00=p[:,col]/norms[col]
 b=np.column_stack([v00,PAULI[x2]@v00,PAULI[x1]@v00,PAULI[x1]@PAULI[x2]@v00]); assert np.max(np.abs(b.conj().T@b-np.eye(4)))<1e-8; return b
def label(v):
 x,z=v&15,(v>>4)&15; return ''.join('I' if not xb and not zb else 'X' if xb and not zb else 'Z' if zb and not xb else 'Y' for xb,zb in [((x>>q)&1,(z>>q)&1) for q in range(4)])
def build():
 cliff,words=two_qubit_clifford(); rays,meta=m36_rays(); orbit={canon_state(u@r) for u in cliff for r in rays}; reps=[(0,0,0),(0,0,1),(0,0,2),(0,1,2)]; inputs=[]
 for m in reps:
  psi=rays[meta.index(m)]; single=np.outer(psi,psi.conj()); delta=np.eye(4)/4-single; inputs.append((m,np.kron(psi,psi),np.kron(delta,single)+np.kron(single,delta)))
 retained=[]
 for space in isotropic_rank2_subspaces():
  for signs in ((1,1),(1,-1),(-1,1),(-1,-1)):
   b=code_basis(space,signs); bd=b.conj().T
   for m,psi2,first in inputs:
    d=bd@psi2; s0=float(np.vdot(d,d).real)
    if s0<1e-10: continue
    ideal=d/math.sqrt(s0)
    if canon_state(ideal) not in orbit: continue
    e1=bd@first@b; slope=(float(np.trace(e1).real)-float(np.vdot(ideal,e1@ideal).real))/s0; retained.append((slope,s0,space,signs,m,ideal))
 assert len(retained)==9264; improving=[x for x in retained if x[0]<.75-1e-9]; optimal=[x for x in retained if abs(x[0]-.5)<1e-9]; assert len(improving)==48 and len(optimal)==12
 chosen=next(x for x in optimal if label(x[2][0])=='IYYX' and label(x[2][1])=='YXIY'); slope,s0,space,signs,input_meta,ideal=chosen; comp=logical_completion(space); correction=None
 for k,word in sorted(words.items(),key=lambda kv:(len(kv[1]),kv[1])):
  u=next(u for u in cliff if canon_unitary(u)==k); out=u@ideal
  for target_meta,target in zip(meta,rays):
   if abs(np.vdot(target,out))**2>1-1e-9: correction={'matrix_word_product':word,'target_ray':list(target_meta)}; break
  if correction: break
 assert correction
 return {'schema':'w33.pass2784.m36_two_copy_distillation.v1','status':'EXACT_EXHAUSTIVE_TWO_COPY_SEARCH','search':{'rank2_isotropic_stabilizer_subspaces':5355,'syndromes_per_subspace':4,'m36_clifford_orbit_representatives':4,'protocol_instances':85680,'m36_closed_instances':9264,'strictly_distilling_instances':48,'optimal_instances':12,'best_output_infidelity_slope_in_p':slope,'input_infidelity_slope_in_p':.75},'selected_protocol':{'input_ray':list(input_meta),'input_vector':'(0,1,-omega,omega^2)/sqrt(3)','checks':[label(space[0]),label(space[1])],'accepted_eigenvalues':list(signs),'logical_Z':[label(comp[2]),label(comp[3])],'logical_X':[label(comp[4]),label(comp[5])],'ideal_success_probability':s0,'logical_clifford_correction':correction,'success_probability':'(p^2-2p+2)/4','output_fidelity':'(5p^2-12p+8)/(4*(p^2-2p+2))','output_infidelity':'p*(4-p)/(4*(p^2-2p+2))','distillation_region':'0<p<2/3','equivalent_input_fidelity_threshold':'F_in>1/2','fixed_points_in_p':[0,2/3,1]},'scope_boundary':'Exhaustive for two-copy binary [[4,2]] stabilizer projections, all syndromes, and the four M36 Clifford orbits; not arbitrary multi-copy ququart protocols.'}
def main():
 out=build(); p=ROOT/'data/PART_BT2784_M36_TWO_COPY_DISTILLATION.json'; p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
