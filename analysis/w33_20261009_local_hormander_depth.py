"""Constructive Hormander bracket-depth witness at the Pass11769
common classical symbol zero for 160 real first-order W33 vector fields
X_e=(Ve.q+a) Ue.grad. Nonzero Xi(q0) begin with active currents.
For inactive X_j(q0)=0, [X_j,Z](q0)=-DX_j(q0)Z(q0), proportional
to U_j when V_j.U_i != 0. This gives literal nested brackets.
Only a *local rank/step* certificate, NOT a quantitative full spectrum
subelliptic constant or quantum lower eigenvalue/gap.
"""
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as V
def rank_mod(mat,p=32003):
  M=np.asarray(mat,dtype=np.int64).copy()%p
  r=0
  for j in range(M.shape[1]):
    nz=np.flatnonzero(M[r:,j])
    if not len(nz):continue
    k=r+int(nz[0]);M[[r,k]]=M[[k,r]]
    M[r]=(M[r]*pow(int(M[r,j]),-1,p))%p
    if r+1<len(M):M[r+1:]=(M[r+1:]-M[r+1:,j,None]*M[r])%p
    r+=1
    if r>=M.shape[0]:break
  return r
def certificate():
  g=V.geometry()
  U=np.rint(40*g['u']).astype(np.int64)
  W=np.rint(40*g['v']).astype(np.int64)
  qi=np.array([39]+[-1]*39+[0]*40,dtype=np.int64)
  X=W@qi+40
  active=set(np.flatnonzero(X).tolist())
  assert len(active)==4
  dot=U@W.T
  reached=set(active);front=set(active);layers=[]
  for depth in range(1,10):
    mat=U[sorted(reached)]
    rank=rank_mod(mat)
    layers.append(dict(bracket_depth=depth,current_indices_reached=len(reached),
                       vector_field_evaluation_rank_lower=rank,
                       frontier_size=len(front)))
    if rank==78:break
    nextset=set()
    for i in front:
      for j in np.flatnonzero(dot[i]):
        j=int(j)
        if j not in reached and X[j]==0: nextset.add(j)
    assert nextset,('failed',depth)
    reached|=nextset;front=nextset
  assert layers[-1]['vector_field_evaluation_rank_lower']==78,layers
  assert rank_mod(U)==78
  return dict(status='PASS',active_current_indices=sorted(active),
    actual_hormander_bracket_step_upper=layers[-1]['bracket_depth'],
    stage_rank_lower_certificates=layers,
    prime=32003,ambient_configuration_dim=78,
    construction='At q0 with Xi(q0)=0 for inactive j, nested [Xj,Z] evaluated at q0 equals -Uj*(Vj.Z(q0)), producing nonzero Uj along each directed nonzero-dot path. Values of constructed iterated brackets span 78 by explicit independent modular minor.',
    scope='Genuine local bracket-generating witness at this single q0 for first-order transport fields only. Not a global uniform step or explicit subelliptic inequality; the full quantum H includes scalar multiplications and complex phases. Does not imply full-H numerical gap.')
if __name__=='__main__':
  d=certificate()
  (ROOT/'data/w33_20261009_local_hormander_depth.json').write_text(json.dumps(d,indent=2)+'\n')
  print('Hormander depth<=',d['actual_hormander_bracket_step_upper'],'ranks',[(t['bracket_depth'],t['vector_field_evaluation_rank_lower']) for t in d['stage_rank_lower_certificates']])
