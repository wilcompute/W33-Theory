#!/usr/bin/env python3
"""Can three reoriented W33 216-outcome POVMs be informationally complete?
Independent ordinary 24D Haar unitaries, calibrated Hermitian operator-span
rank, diagonal-only phase-masks control and exact 3-setting rank lower bound.
"""
from pathlib import Path
import json,sys,math
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_five_deeper_fronts import route_frame

def embed_effects(V,U):
 # For each s, a_s = V_s U; E_s=outer(conj(a_s),a_s).
 # diag, sqrt(2) real & imag off-diagonal gives orthonormal real Hermitian basis.
 X=V@U
 n=X.shape[1];ii,jj=np.triu_indices(n,k=1)
 diag=(X.conj()*X).real
 off=X[:,ii].conj()*X[:,jj]
 return np.concatenate([diag,math.sqrt(2)*off.real,math.sqrt(2)*off.imag],axis=1)
def rank(M,tol=1e-9):
 sv=np.linalg.svd(M,compute_uv=False)
 return int(np.sum(sv>tol)),sv
def main():
 Z,N=route_frame();E=Z.T@Z
 eig,U=np.linalg.eigh(E.astype(float));V=Z@U[:,16:]/math.sqrt(360)
 for k in range(24):
  j=np.argmax(abs(V[:,k]))
  if V[j,k]<0:V[:,k]*=-1
 assert np.max(abs(V.T@V-np.eye(24)))<1e-9
 r=np.random.default_rng(20261103)
 frames=[]; results=[]
 for s in range(4):
  if s==0:rot=np.eye(24,dtype=complex)
  else:
   X=r.normal(size=(24,24))+1j*r.normal(size=(24,24))
   rot,R=np.linalg.qr(X)
   rot=rot@np.diag(np.conj(np.diag(R))/np.abs(np.diag(R)))
  frames.append(embed_effects(V,rot))
  MM=np.vstack(frames);rk,sv=rank(MM)
  results.append({'settings':s+1,'effects':216*(s+1),'operator_rank':rk,
   'hermitian_dimension':576,'null_dimension':576-rk,'nonzero_condition_ratio':
      float(sv[0]/sv[rk-1]),'max_operator_isometry':float(np.max(abs(np.sum(
       (V@rot).conj()[:,:,None]*(V@rot)[:,None,:],axis=0)-np.eye(24))))})
  print('FULL_UNITARY_SETTINGS',results[-1],flush=True)
 # Phase-only masks, diagonal unchanged: cannot access nontrivial invisible diagonals.
 ph=[];phase_results=[]
 for s in range(4):
  rot=np.eye(24,dtype=complex) if s==0 else np.diag(np.exp(1j*r.uniform(0,2*np.pi,24)))
  ph.append(embed_effects(V,rot));rk,sv=rank(np.vstack(ph))
  phase_results.append({'settings':s+1,'rank':rk,'blind_dim':576-rk})
 print('PHASE_ONLY',phase_results,flush=True)
 # All effects share I, so 2 settings at most 2*(201-1)+1=401.
 assert results[0]['operator_rank']==201
 assert results[1]['operator_rank']<=401
 assert results[2]['operator_rank']<=576
 data={'status':'COMPLETE_IF_RANK_576_ELSE_PARTIAL',
   'rank_one_effects_per_setting':216,
   'individual_operator_span':201,'complex_hermitian_dimension':576,
   'algebraic_lower_bound_on_settings':3,
   'full_unitary_results':results,'phase_only_control':phase_results,
   'three_settings_informationally_complete':results[2]['operator_rank']==576,
   'physical_requirements':'Three independently calibrated 24-mode complex unitary pre-rotations before the existing 216-output Naimark receiver; no claim of cheap implementation or robust inversion',
   'scope':'Numerical rank/conditioning with seeded Haar unitaries. Reuse same 216-outcome POVM; new full complex measurement only after orientations. Not a SIC or hardware experiment.'}
 (ROOT/'data/w33_20261103_three_setting_ic_povm.json').write_text(json.dumps(data,indent=2)+'\n')
 print('RESULT',json.dumps(data)[:4500],flush=True)
 return data
if __name__=='__main__':main()
