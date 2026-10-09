"""Finite W33 Levi shells and dimension-selection obstruction.

The native 80-vertex incidence geometry has finite diameter four.
This does not select a 3+1 dimensional continuum.
"""
from collections import deque,Counter
from math import log
from pathlib import Path
import numpy as np,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261008_5state_ritz as geo
def certificate():
    edges,inc,*_=geo.geometry()
    adj=[set() for _ in range(80)]
    for p,l in edges:
        adj[p].add(l);adj[l].add(p)
    assert all(len(a)==4 for a in adj)
    shells=[]
    for origin in range(80):
        dist=[-1]*80;dist[origin]=0;q=deque([origin])
        while q:
            v=q.popleft()
            for w in adj[v]:
                if dist[w]<0:dist[w]=dist[v]+1;q.append(w)
        counts=[dist.count(i) for i in range(max(dist)+1)]
        assert counts==[1,4,12,36,27]
        shells.append(counts)
    balls=np.cumsum(shells[0]).tolist()
    dim=[log(balls[r]/balls[r-1])/log(r/(r-1)) for r in range(2,5)]
    L=np.zeros((80,80),int)
    for p,l in edges:L[p,l]=L[l,p]=1
    e=np.linalg.eigvalsh(L)
    target=np.array([-4]+[-np.sqrt(6)]*24+[0]*30+[np.sqrt(6)]*24+[4])
    assert np.max(np.abs(e-target))<1e-10
    return dict(status='PASS',vertices=80,edges=160,diameter=4,
       distance_shells=shells[0],ball_sizes=balls,
       ball_growth_dimension_estimates=dim,
       exact_full_Levi_spectrum='-4(1),-sqrt(6)(24),0(30),sqrt(6)(24),4(1)',
       boundary='A finite diameter-four graph supplies no intrinsic large-scale polynomial volume growth or canonical spatial dimension. Infinite replication/limit and metric are extra inputs.')
if __name__=='__main__':
    x=certificate()
    (ROOT/'data/w33_20261008_levi_shell_dimension.json').write_text(json.dumps(x,indent=2)+'\n')
    print(x)
