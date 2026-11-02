"""Exact scalar-spinor-spinor invariant tensors of the prescribed61440 cover.

Integer Reynolds witnesses give lower bounds; modular constraint ranks give
upper bounds over Q(i). Matching them certifies the dimensions in characteristic0.
"""
import pathlib,json,itertools,math,functools,sys
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261101_common_cubic_spinor_extension import signed_mul

def rank_mod(A,p=1009,columns=False):
    A=np.array(A,dtype=np.int64)%p;r=0;piv=[]
    for c in range(A.shape[1]):
        nz=np.flatnonzero(A[r:,c])
        if not len(nz):continue
        k=r+int(nz[0]);A[[r,k]]=A[[k,r]]
        A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
        nz=np.flatnonzero(A[r+1:,c])+r+1
        if len(nz):A[nz]=(A[nz]-A[nz,c,None]*A[r])%p
        piv.append(c);r+=1
        if r==min(A.shape):break
    return piv if columns else r

def gaussian_product(g,h):
    A=np.array(g[:16],dtype=np.int64).reshape(4,4);B=np.array(g[16:],dtype=np.int64).reshape(4,4)
    C=np.array(h[:16],dtype=np.int64).reshape(4,4);D=np.array(h[16:],dtype=np.int64).reshape(4,4)
    E=A@C-B@D;F=A@D+B@C
    assert not np.any(E%2) and not np.any(F%2)
    return tuple(map(int,(E//2).flat))+tuple(map(int,(F//2).flat))

def action_numerator(p,b,U):
    A=np.array(U[:16],dtype=np.int64).reshape(4,4);B=np.array(U[16:],dtype=np.int64).reshape(4,4)
    K=np.kron(A.T,A.T)-np.kron(B.T,B.T);L=np.kron(A.T,B.T)+np.kron(B.T,A.T)
    n=len(p);R=np.zeros((16*n,16*n),dtype=np.int64);S=R.copy()
    for j,k in enumerate(p):
        R[16*j:16*j+16,16*k:16*k+16]=(-1)**b[j]*K
        S[16*j:16*j+16,16*k:16*k+16]=(-1)**b[j]*L
    return R,S

def build():
    d=json.loads((ROOT/'data/w33_20261101_common_cubic_spinor_extension.json').read_text())
    gens=[(tuple(x['permutation']),tuple(x['sign_bits']))for x in d['paired_signed_generators']]
    I27=(tuple(range(27)),(0,)*27);seen={I27};queue=[I27];words={I27:[]}
    for x in queue:
        for j,g in enumerate(gens):
            y=signed_mul(g,x)
            if y not in seen:seen.add(y);queue.append(y);words[y]=words[x]+[j]
    assert len(queue)==30720
    kernel=[b for p,b in queue if p==I27[0]]
    fixed=[j for j in range(27)if all(b[j]==0 for b in kernel)]
    assert len(kernel)==32
    print('KERNEL_FIXED_COORDINATES',fixed,flush=True)
    pos={j:k for k,j in enumerate(fixed)}
    small=[(tuple(pos[p[j]]for j in fixed),tuple(b[j]for j in fixed))for p,b in gens]
    ugens=[tuple(x)for x in d['paired_unitary_dyadic_generators']]
    mats=[np.array(x,dtype=np.int16)for x in d['paired_GF5_generators']]
    eye=np.eye(4,dtype=np.int16);uid=tuple(map(int,(2*eye).flat))+(0,)*16
    n=len(fixed);N=16*n
    unit={tuple(map(int,eye.flat)):(uid,(tuple(range(n)),(0,)*n))};uq=[eye]
    for x in uq:
        u,s=unit[tuple(map(int,x.flat))]
        for M,U,g in zip(mats,ugens,small):
            y=M@x%5;k=tuple(map(int,y.flat));v=gaussian_product(U,u)
            p,a=g;q,b=s;t=(tuple(p[q[j]]for j in range(n)),tuple(b[j]^a[q[j]]for j in range(n)))
            if k not in unit:unit[k]=(v,t);uq.append(y)
            else:assert unit[k]==(v,t)
    assert len(unit)==1920
    # Numerator of1920*4 times the Reynolds projector in coefficient space.
    R=np.zeros((N,N),dtype=np.int64);S=R.copy()
    for u,(p,b) in unit.values():
        A,B=action_numerator(p,b,u);R+=A;S+=B
    constraints=[];root=next(a for a in range(1009)if a*a%1009==1008)
    for (p,b),u in zip(small,ugens):
        A,B=action_numerator(p,b,u)
        assert np.array_equal(A@R-B@S,4*R) and np.array_equal(A@S+B@R,4*S)
        constraints.append(A+root*B-4*np.eye(N,dtype=np.int64))
    upper=N-rank_mod(np.vstack(constraints));piv=rank_mod(R+root*S,columns=True)
    assert len(piv)==upper
    def sector(antisymmetric):
        cols=[]
        for j in range(n):
            for a in range(4):
                for b in range(a if not antisymmetric else a+1,4):
                    k=16*j+4*a+b;l=16*j+4*b+a
                    v=R[:,k].copy();w=S[:,k].copy()
                    if a!=b:
                        v+=(-1 if antisymmetric else 1)*R[:,l];w+=(-1 if antisymmetric else 1)*S[:,l]
                    cols.append(v+root*w)
        return rank_mod(np.array(cols).T)
    symmetric=sector(False);alternating=sector(True);assert symmetric+alternating==upper
    witnesses=[]
    for k in piv:
        a=R[:,k].copy();b=S[:,k].copy();g=functools.reduce(math.gcd,map(abs,map(int,np.r_[a,b])))
        a//=g;b//=g
        blocks=[]
        for j,coord in enumerate(fixed):
            A=a[16*j:16*j+16].reshape(4,4);B=b[16*j:16*j+16].reshape(4,4)
            if np.any(A)or np.any(B):blocks.append(dict(coordinate=coord,real=A.tolist(),imag=B.tolist()))
        witnesses.append(dict(seed_column=k,blocks=blocks))
    return dict(status='PASS_EXACT_COMMON_COVER_CUBIC_SPINOR_INTERACTIONS',
        signed_kernel_order=32,scalar_coordinates_fixed_by_kernel=fixed,forbidden_linear_scalar_coordinates=sorted(set(range(27))-set(fixed)),
        signed_kernel_word_witnesses=[dict(sign_bits=b,word=words[(I27[0],b)])for b in kernel],
        invariant_dimension=upper,symmetric_spinor_bilinear_dimension=symmetric,alternating_spinor_bilinear_dimension=alternating,
        reduced_coefficient_space_dimension=N,modulus=1009,imaginary_unit_modulus=root,modular_constraint_rank=N-upper,integer_Reynolds_independent_columns=piv,
        exact_witnesses=witnesses,
        covariance_convention='P(phi,psi,eta)=sum_i phi_i psi^T B_i eta for two independent spinor vectors. If scalar generator sends e_j to(-1)^b_j e_p(j), invariance is(-1)^b_j U^T B_p(j) U=B_j. The sole alternating tensor vanishes on identical commuting spinors; the symmetric-polynomial space is zero. Grassmann/Lorentz conventions require separate physical input.',
        proof='The32-element signed kernel acts trivially on spinors; averaging kills all scalar coordinates with a nontrivial kernel character. On the recorded surviving coordinates the scalar action descends to the same960 quotient as the spinor1920 lift. Enumerate1920 exact dyadic unitaries, average their coefficient action, and verify every integer witness against all six generators. Reduction at i modulo1009 bounds characteristic-zero nullity above; the equally many independent exact Reynolds columns attain that bound.',
        boundary='Only the prescribed27 and4 representations, degree one in the scalar and two in the spinor, complex bilinear rather than Hermitian. No masses, vacuum, coupling strengths, Lorentz spinors or physical Yukawa dynamics are derived.')

if __name__=='__main__':
    out=build();(ROOT/'data/w33_20261102_common_cover_interactions.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],out['invariant_dimension'],out['symmetric_spinor_bilinear_dimension'],out['alternating_spinor_bilinear_dimension'],flush=True)
