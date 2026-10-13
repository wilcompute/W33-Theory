"""TOE59 front1 exact W33 shortest gauge-invariant flat Wilson winding."""
from pathlib import Path
from collections import deque
from itertools import product
import numpy as np,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep
ed,volts,*_=prep();E=np.asarray(ed,dtype=int);V=np.asarray(volts,dtype=int)
def signed_matrix(c):
 s=(-1)**(V@np.asarray(c,dtype=int))
 H=np.zeros((80,80),dtype=np.int64)
 for (a,b),sgn in zip(E,s):H[a,b]=H[b,a]=-sgn
 return H
corners=list(product((0,1),repeat=3))
H0=signed_matrix((0,0,0))
base={n:int(np.trace(np.linalg.matrix_power(H0,n))) for n in range(2,25,2)}
rows=[]
for c in corners:
 H=signed_matrix(c)
 delta={n:int(np.trace(np.linalg.matrix_power(H,n)))-base[n] for n in base}
 first=next((n for n,v in delta.items() if v),None)
 adj=[[] for _ in range(160)]
 for (a,b),v in zip(E,V):
  t=int((v@np.array(c))%2)
  for p in (0,1):
   adj[a+80*p].append(b+80*(p^t))
   adj[b+80*p].append(a+80*(p^t))
 lens=[]
 for root in range(80):
  dd=[-1]*160;dd[root]=0;q=deque([root])
  while q:
   x=q.popleft()
   if x==root+80:break
   for y in adj[x]:
    if dd[y]==-1:dd[y]=dd[x]+1;q.append(y)
  lens.append(dd[root+80])
 minlen=min(n for n in lens if n>=0) if any(x>=0 for x in lens) else None
 assert (first==minlen) if c!=(0,0,0) else first is None
 rows.append(dict(pi_corner=list(c),shortest_nontrivial_winding_length=minlen,
        first_flux_sensitive_moment=first,
        trace_moment_difference=delta.get(first) if first else 0,
        base_trace=base.get(first) if first else 0,
        delta_at_even_lengths=delta))
 print("pi corner",c,"first",first,"moment delta",delta.get(first),flush=True)
out={"status":"PASS_TOE59_W33_SHORTEST_FLAT_WILSON_WINDING_MOMENT",
"native_sites":80,"native_edges":160,"tested_corners":rows,
"proof":"For any Z2 deck twist c, Tr[H(c)^n]-Tr[H(0)^n] sums closed graph walks of length n weighted (-1)^deck-winding-1. The first nonzero order equals the shortest parity-nontrivial closed walk length (all altered walks contribute -2). Independently measure shortest distance from each root in the parity-double cover to its opposite-layer copy.",
"limits":"An 80-site static nearest-neighbor spinless model and eight selected Z2 flat connections, not physical 4D QED or a unique vacuum."}
(R/"data/w33_20261013_toe59_wilson_girth_moments.json").write_text(json.dumps(out,indent=2)+"\n")
