"""TOE91 symmetry audit: finite-field symplectic transvections against Witting Bargmann phases."""
from __future__ import annotations
import re,json
import numpy as np
from pathlib import Path
from tools.witting_graph_isomorphism import construct_f3_points, omega_symp
from tools.bt1408_witting_contextual_communication_bridge import construct_witting_40_rays
ROOT=Path(__file__).resolve().parents[1]
R=np.asarray(construct_witting_40_rays())
P=construct_f3_points()
doc=(ROOT/'docs/witting_graph_isomorphism.md').read_text()
mp={int(a):int(b) for a,b in re.findall(r'(?m)^(\d+) -> (\d+)$',doc)}
assert len(mp)==40
inv={p:i for i,p in mp.items()}
idx={p:i for i,p in enumerate(P)}
def norm(v):
 for x in v:
  if x%3:return tuple(int((2 if x%3==2 else 1)*a%3) for a in v)
 raise ValueError
def transvection(v,sign=1):
 out=[]
 for i in range(40):
  x=P[mp[i]];w=omega_symp(x,v)
  z=norm([(a+sign*w*b)%3 for a,b in zip(x,v)])
  out.append(inv[idx[z]])
 assert len(set(out))==40
 return out
def triple_test(p):
 Gram=R.conj()@R.T
 d1=d2=0.;nonzero=0
 for i in range(40):
  for j in range(i+1,40):
   if abs(Gram[i,j])<1e-10:continue
   for k in range(j+1,40):
    z=Gram[i,j]*Gram[j,k]*Gram[k,i]
    if abs(z)<1e-10:continue
    u=Gram[p[i],p[j]]*Gram[p[j],p[k]]*Gram[p[k],p[i]]
    d1=max(d1,abs(u-z));d2=max(d2,abs(u-z.conjugate()))
    nonzero+=1
 return float(round(d1,12)),float(round(d2,12)),int(nonzero)
def certificate():
 vals=[]
 for j in range(4):
  v=[int(t==j) for t in range(4)]
  for sign in (1,):
   perm=transvection(v,sign)
   a,b,n=triple_test(perm)
   vals.append({'F3_transvection_v':v,'unitary_Bargmann_max_error':a,'antiunitary_Bargmann_max_error':b,'nonorthogonal_triples':n,'unitary_possible':a<1e-9,'antiunitary_possible':b<1e-9})
   print('SYMP',j,a,b,n,flush=True)
 return {'reference_mapping':'docs/witting_graph_isomorphism.md','tests':vals,'interpretation':'Preserving the W33 orthogonality graph is weaker than a physical ququart unitary lift. Bargmann triple phases give a necessary projective-unitary invariant. This test does not classify the full 25920 action.'}
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261015_toe91_symplectic_phase_audit.json').write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
