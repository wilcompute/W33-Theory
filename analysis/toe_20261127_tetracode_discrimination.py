"""Check USD and minimum-error measurement dual witnesses on the exact Gram support."""
from itertools import product, combinations
import numpy as np
from fractions import Fraction
import json

def run():
    V=list(product(range(3),repeat=4)); N=[v for v in V if sum(x*x for x in v)%3==0]
    C=sorted({tuple(sorted({tuple((i*x+j*y)%3 for x,y in zip(a,b)) for i,j in product(range(3),repeat=2)})) for a,b in combinations(N[1:],2) if sum(x*y for x,y in zip(a,b))%3==0 and b!=tuple(2*x%3 for x in a)})
    assert len(C)==8
    L=list(map(set,C)); f=[i for i,c in enumerate(L) if i==0 or len(c&L[0])==1]; L=[L[i] for i in f+[i for i in range(8) if i not in f]]
    B=np.array([[int(v in c)/3 for c in L] for v in V]); G0=B.T@B
    B2=np.column_stack([np.kron(B[:,i],B[:,i]) for i in range(8)]); assert np.allclose(B2.T@B2,G0**2)
    out=[]
    for g in range(1,5):
        G=G0**g; w,U=np.linalg.eigh(G); w=np.maximum(w,0); w[w<1e-12]=0
        R=(U*np.sqrt(w))@U.T
        d=np.trace(R)/8; assert np.max(np.abs(np.diag(R)-d))<1e-12
        Y=d*R/8; residuals=[np.linalg.eigvalsh(Y-np.outer(R[:,i],R[:,i])/8).min() for i in range(8)]
        assert min(residuals)>-1e-12
        assert abs(np.trace(Y)-d*d)<1e-12
        usd=(1-Fraction(1,3**g))*(1-Fraction(1,3**(g-1)))
        assert abs(w.min()-float(usd))<1e-12
        if g>=2:
            reciprocal=np.linalg.inv(R); conclusive=float(usd)*reciprocal@reciprocal.T
            assert np.linalg.eigvalsh(np.eye(8)-conclusive).min()>-1e-12
            assert np.allclose(reciprocal.T@R,np.eye(8))
        out.append({'copies':g,'optimal_USD':str(usd),'optimal_minimum_error_success':float(d*d),'dual_slack_min_eigenvalue':float(min(residuals))})
    return out
if __name__=='__main__': print(json.dumps(run(),indent=2))
