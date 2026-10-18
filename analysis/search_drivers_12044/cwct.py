import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
import sys,numpy as np; sys.path.insert(0,'.')
import cwhess as C
def make_ct(x0):
    norms=[np.linalg.norm(Y,2) for Y in C.mats(x0)]
    return lambda x: sum(n*np.trace((Y/nr)@(Y/nr).conj().T).real for n,Y,nr in zip(C.NC,C.mats(x),norms))
for name,x0 in C.POINTS.items():
    H=C.hess(C.make_V(x0,1.0,1.0),x0,C.T); Hc=C.hess(make_ct(x0),x0,C.T)
    best=(-1e9,None)
    for c in np.concatenate([-np.logspace(-4,4,400)[::-1],[0],np.logspace(-4,4,400)]):
        m=np.linalg.eigvalsh(H+c*Hc).min()
        if m>best[0]: best=(m,c)
    print(f'{name:24s} counterterm Hessian eig',np.array2string(np.linalg.eigvalsh(Hc),precision=3),' best min-eigenvalue over c: %.3e at c=%.3g'%best)
