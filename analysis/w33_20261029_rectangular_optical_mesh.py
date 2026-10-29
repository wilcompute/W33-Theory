#!/usr/bin/env python3
"""Exact Clements-style 40-mode W33 walk compiler and loss comparison.
Independent two-sided Givens elimination; standard NumPy only.
This is one photon over 40 modes, NOT the physical [[40,8,6]] CSS block.
"""
from pathlib import Path
import json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261029_rectangular_optical_mesh.json"
def graph():
 p=set()
 for a in range(3):
  for b in range(3):
   for c in range(3):
    for d in range(3):
     x=(a,b,c,d)
     if x==(0,0,0,0):continue
     h=next(t for t in x if t);inv=pow(h,-1,3)
     p.add(tuple(t*inv%3 for t in x))
 p=sorted(p)
 form=lambda x,y:(x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3
 A=np.array([[int(i!=j and form(x,y)==0) for j,y in enumerate(p)] for i,x in enumerate(p)],float)
 assert len(p)==40 and np.all(A.sum(1)==12)
 return A
def target(A):
 I=np.eye(40);J=np.ones((40,40))
 P12=J/40
 P2=(2/3)*I+(1/6)*A-(1/15)*J
 return P12-P2+(I-P12-P2)
def right(a,b):
 h=np.hypot(abs(a),abs(b))
 return None if h<1e-14 else np.array([[b,np.conj(a)],[-a,np.conj(b)]],complex)/h
def left(a,b):
 h=np.hypot(abs(a),abs(b))
 return None if h<1e-14 else np.array([[np.conj(a),np.conj(b)],[-b,a]],complex)/h
def rectangular(U):
 n=len(U);W=U.astype(np.complex128).copy();ops=[];lefts=[]
 for width in range(n-1):
  for offset in range(width+1):
   if width%2==0:
    row=n-1-offset;col=width-offset
    R=right(W[row,col],W[row,col+1])
    if R is not None:
     W[:,col:col+2]=W[:,col:col+2]@R;ops.append((col,R))
     assert abs(W[row,col])<1e-12
   else:
    col=offset;lower=n-1-width+offset;upper=lower-1
    L=left(W[upper,col],W[lower,col])
    if L is not None:
     W[upper:lower+1,:]=L@W[upper:lower+1,:];lefts.append((upper,L))
     assert abs(W[lower,col])<1e-12
 assert np.max(abs(W-np.diag(np.diag(W))))<2e-12
 for upper,L in reversed(lefts):
  W[upper:upper+2,:]=L.conj().T@W[upper:upper+2,:]
  R=right(W[upper+1,upper],W[upper+1,upper+1])
  if R is not None:
   W[:,upper:upper+2]=W[:,upper:upper+2]@R;ops.append((upper,R))
  assert abs(W[upper+1,upper])<5e-12
 assert np.max(abs(W-np.diag(np.diag(W))))<3e-12
 phases=np.diag(W).copy()
 gates=[(i,R.conj().T) for i,R in ops]
 product=np.diag(phases.astype(np.complex128))
 for i,B in reversed(gates):product[:,i:i+2]=product[:,i:i+2]@B
 error=float(np.max(abs(product-U)))
 assert error<3e-12
 return gates,phases,error
def triangular(U):
 n=len(U);W=U.astype(np.complex128).copy();gates=[]
 for col in range(n-1):
  for row in range(n-1,col,-1):
   L=left(W[row-1,col],W[row,col])
   if L is not None:
    W[row-1:row+1,:]=L@W[row-1:row+1,:]
    gates.append((row-1,L.conj().T))
 assert np.max(abs(W-np.diag(np.diag(W))))<2e-12
 gates=gates[::-1];phases=np.diag(W).copy()
 P=np.diag(phases.astype(np.complex128))
 for i,B in gates:P[i:i+2,:]=B@P[i:i+2,:]
 error=float(np.max(abs(P-U)))
 assert error<3e-12
 return gates,phases,error
def depth(gates):
 last=[-1]*40
 for i,_ in gates:
  k=max(last[i],last[i+1])+1
  last[i]=last[i+1]=k
 return max(last)+1
def attenuate(gates,phases,output_phases=False,eta=.999):
 K=np.eye(40,dtype=complex) if output_phases else np.diag(phases.astype(np.complex128))
 for i,B in gates:K[i:i+2,:]=eta**.5*B@K[i:i+2,:]
 if output_phases:K=np.diag(phases)@K
 return K
def main():
 U=target(graph());assert np.max(abs(U@U.conj().T-np.eye(40)))<1e-12
 C,phc,ec=rectangular(U);T,pht,et=triangular(U)
 dc,dt=depth(C),depth(T)
 assert len(C)==656 and dc==40 and len(T)==653 and dt==77
 def metrics(g,p,out):
  K=attenuate(g,p,out)
  survival=(abs(K)**2).sum(0)
  ev=np.linalg.eigvalsh(K.conj().T@K)
  return {"active_gates":len(g),"layers":depth(g),
    "reconstruction_max_abs_error":ec if out else et,
    "input_0_survival":float(survival[0]),"input_min_survival":float(min(survival)),
    "input_mean_survival":float(np.mean(survival)),
    "input_max_survival":float(max(survival)),
    "K_dagger_K_eigenvalue_bounds":[float(min(ev)),float(max(ev))]}
 result={"status":"PASS","target":"exp(-i*pi*A/2), 40-mode W(3,3) one-photon walk",
         "rectangular":metrics(C,phc,True),"triangular":metrics(T,pht,False),
         "per_active_element_transmission":.999,
         "method":"alternating right/left Givens elimination and exact rephasing; reconstructed matrices checked",
         "boundary":"Depth is disjoint-layer DAG depth. No interconnect propagation loss, hardware imperfection, CSS fault tolerance, or fundamental physics prediction."}
 OUT.write_text(json.dumps(result,indent=2)+"\n")
 print("PASS rectangular",len(C),dc,"triangular",len(T),dt)
 return result
if __name__=="__main__":main()
