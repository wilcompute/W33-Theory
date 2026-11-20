"""Independent W33 CSS syndrome table and SIC H27/SU3 center check."""
from itertools import product
import json
import numpy as np
from scipy import sparse
omega=np.exp(2j*np.pi/3)
def incidence():
    def norm(v):
        q=tuple(x%3 for x in v);z=next(t for t in q if t)
        return tuple((x*(1 if z==1 else 2))%3 for x in q)
    def sym(u,v):return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3
    pts=sorted({norm(v) for v in product(range(3),repeat=4) if any(v)})
    ids={p:i for i,p in enumerate(pts)}
    lines=set()
    for i,u in enumerate(pts):
        for v in pts[i+1:]:
            if sym(u,v):continue
            lines.add(frozenset(ids[norm(tuple((a*u[k]+b*v[k])%3 for k in range(4)))] for a,b in product(range(3),repeat=2) if a or b))
    L=sorted(lines,key=lambda s:tuple(sorted(s)))
    edges=sorted((p,40+j) for j,line in enumerate(L) for p in line)
    assert (len(pts),len(L),len(edges))==(40,40,160)
    D=np.zeros((80,160),np.int16)
    for j,(u,v) in enumerate(edges):D[u,j]=1;D[v,j]=-1
    return sparse.csr_matrix(D[:-1])
def check():
    A=incidence();B=sparse.csr_matrix([[1,-1,0],[0,1,-1]],dtype=np.int16)
    eye=lambda n:sparse.eye(n,dtype=np.int16,format='csr')
    HX=sparse.hstack([sparse.kron(A,eye(3)),sparse.kron(eye(79),B.T)],format='csr')
    HZ=sparse.hstack([sparse.kron(eye(160),B),-sparse.kron(A.T,eye(2))],format='csr')
    assert HX.shape==(237,638) and HZ.shape==(320,638)
    assert not np.any((HX@HZ.T).data%3)
    def dictionary(H):
        C=H.tocsc();seen={};collisions=0
        for j in range(638):
            a,b=C.indptr[j:j+2];ids=tuple(map(int,C.indices[a:b]));vals=tuple(map(int,C.data[a:b]%3))
            assert ids
            for s in (1,2):
                key=(ids,tuple(int(s*x%3) for x in vals))
                if key in seen:collisions+=1
                else:seen[key]=(j,s)
        return len(seen),collisions
    x=dictionary(HZ);z=dictionary(HX)
    a=np.zeros(638,np.int16);b=a.copy();a[0]=a[1]=1;b[2]=2
    assert np.array_equal((HZ@a)%3,(HZ@b)%3)
    assert x==z==(1276,0)
    U=np.zeros((9,9),complex);V=U.copy()
    for b0 in range(3):
        for a0 in range(3):
            i=3*b0+a0;U[3*b0+(a0+1)%3,i]=omega**b0;V[3*((b0+1)%3)+a0,i]=1
    comm=U@V@U.conj().T@V.conj().T
    assert np.linalg.norm(comm-omega*np.eye(9))<1e-12
    X=np.roll(np.eye(3,dtype=complex),1,axis=0);Z=np.diag([1,omega,omega**2])
    v=np.array([1,-1,0],complex)
    Q=np.column_stack([np.linalg.matrix_power(X,b0)@np.linalg.matrix_power(Z,a0)@v for b0 in range(3) for a0 in range(3)])
    assert np.linalg.norm(Q@U-Z@Q)<1e-12 and np.linalg.norm(Q@V-X@Q)<1e-12
    return {'status':'PASS','CSS':{'physical':638,'logical':81,'dX':3,'dZ':8,'single_X_syndromes':x[0],'single_Z_syndromes':z[0],'collisions':x[1]+z[1],'two_vs_one_X_ambiguity':True},'H27':{'center_residual':float(np.linalg.norm(comm-omega*np.eye(9))),'center_identified_with_SU3_color_gauge':True,'global_flavor_quotient':'Z3^2'},'limits':'Ideal/noiseless CSS syndrome extraction; SIC gauge-center toy. Not an E8 UV or physical TOE.'}
if __name__=='__main__':print(json.dumps(check(),indent=2))
