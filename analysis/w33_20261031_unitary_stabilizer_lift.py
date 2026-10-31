"""Exact complex two-qubit lift of the frozen q=5 stabilizer.

Extends the kernel dictionary in w33_20261031_petersen_stabilizer.py.
All group closure uses integer numerators over denominator two.
"""
import itertools,json,pathlib,hashlib
import numpy as np
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1]

def inverse5(A):return np.array(s.Matrix(A.tolist()).inv_mod(5)).astype(np.int64)%5

def build():
    old=json.loads((ROOT/'data/w33_20261031_petersen_stabilizer.json').read_text())
    S=np.array(old['two_qubit_kernel_intertwiner']['intertwiner_mod5']);Si=inverse5(S)
    X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);I=s.eye(2)
    paulis=[s.I*s.kronecker_product(X,I),s.I*s.kronecker_product(Z,I),s.kronecker_product(I,X),s.kronecker_product(I,Z)]
    def mod5(M):
        def scalar(x):
            a,b=s.fraction(x);return int(a)*pow(int(b),-1,5)%5
        return np.array([scalar(s.re(x))+2*scalar(s.im(x))for x in M]).reshape(4,4)%5
    kernel={tuple(s.eye(4)):s.eye(4)};todo=[s.eye(4)]
    for A in todo:
        for P in paulis:
            B=P*A
            if tuple(B)not in kernel:kernel[tuple(B)]=B;todo.append(B)
    reduced_kernel={tuple(mod5(A).flat):A for A in todo};assert len(reduced_kernel)==32
    lifts=[];conjugation=[]
    for generator in old['symplectic_matrix_generators']:
        G=Si@np.array(generator)@S%5;Gi=inverse5(G)
        images=[reduced_kernel[tuple((G@mod5(P)@Gi%5).flat)]for P in paulis]
        equations=[]
        for A,B in zip(paulis,images):
            for r,c in itertools.product(range(4),repeat=2):
                row=[0]*16
                for k in range(4):row[r*4+k]+=A[k,c];row[k*4+c]-=B[r,k]
                equations.append(row)
        null=s.Matrix(equations).nullspace();assert len(null)==1
        U=s.Matrix(4,4,null[0]);U=s.simplify(U/s.sqrt((U.conjugate().T*U)[0,0]))
        U=next(phase*U for phase in [1,-1,s.I,-s.I]if np.array_equal(mod5(phase*U),G))
        assert U.conjugate().T*U==s.eye(4) and s.simplify(U.det())==1
        assert all(U*A==B*U for A,B in zip(paulis,images))
        lifts.append(U);conjugation.append([[[str(x)for x in row]for row in B.tolist()]for B in images])
    # Exact dyadic Gaussian matrix multiplication. Every numerator stays even
    # before division, and all 1920 matrices stay in (Z[i]/2)^(4x4).
    def encode(M):return tuple(int(2*s.re(x))for x in M)+tuple(int(2*s.im(x))for x in M)
    def arrays(key):return np.array(key[:16]).reshape(4,4),np.array(key[16:]).reshape(4,4)
    def mul(a,b):
        A,B=arrays(a);C,D=arrays(b);real=A@C-B@D;imag=A@D+B@C
        assert not np.any(real%2) and not np.any(imag%2)
        return tuple(map(int,(real//2).flat))+tuple(map(int,(imag//2).flat))
    identity=encode(s.eye(4));gens=[encode(U)for U in lifts];seen={identity};queue=[identity]
    for A in queue:
        for U in gens:
            B=mul(U,A)
            if B not in seen:seen.add(B);queue.append(B)
        assert len(seen)<=1920
    assert len(seen)==1920
    reductions=set();projective=set()
    for key in seen:
        A,B=arrays(key)
        assert np.array_equal(A.T@A+B.T@B,4*np.eye(4,dtype=int))
        assert not np.any(A.T@B-B.T@A)
        M=3*(A+2*B)%5;k=tuple(map(int,M.flat));reductions.add(k)
        lead=next(int(x)for x in M.flat if x);projective.add(tuple(map(int,(M*pow(lead,-1,5)%5).flat)))
    assert len(reductions)==1920 and len(projective)==960
    omega=s.kronecker_product(s.Matrix([[0,1],[-1,0]]),s.eye(2))
    assert all(U.T*omega*U==omega for U in lifts)
    # Recover the actual SO5 action from the five involution axes of the
    # extraspecial-minus kernel, rather than identifying dimensions by count.
    axes=[]
    for A in todo:
        if A*A==s.eye(4) and A!=s.eye(4) and A!=-s.eye(4) and all(A!=B and A!=-B for B in axes):axes.append(A)
    assert len(axes)==5 and all(A*B==-B*A for A,B in itertools.combinations(axes,2))
    signed=[]
    for U in lifts:
        M=s.zeros(5)
        for j,A in enumerate(axes):
            image=U*A*U.conjugate().T
            i,sign=next((i,z)for i,B in enumerate(axes)for z in (1,-1)if image==z*B)
            M[i,j]=sign
        signed.append(M)
    equations=[]
    for A,B in zip(signed,old['signed_five_dimensional_generators']):
        # A L = L B.
        B=s.Matrix(B)
        for r,c in itertools.product(range(5),repeat=2):
            row=[0]*25
            for k in range(5):row[k*5+c]+=A[r,k];row[r*5+k]-=B[k,c]
            equations.append(row)
    null=s.Matrix(equations).nullspace();assert len(null)==1
    L=s.Matrix(5,5,null[0]);assert L.det()!=0 and L.T*L==s.eye(5)
    return dict(status='PASS_EXACT_SU4_CLIFFORD_LIFT',unitary_group_order=1920,projective_group_order=960,
        reduction_i_to_2_is_injective=True,complex_symplectic_form=[[str(x)for x in row]for row in omega.tolist()],
        unitary_generators=[[[str(x)for x in row]for row in U.tolist()]for U in lifts],
        generator_doubled_integer_keys=[list(k)for k in gens],kernel_conjugation_images=conjugation,
        gamma_axes=[[[str(x)for x in row]for row in A.tolist()]for A in axes],
        five_dimensional_basis_intertwiner=[list(map(int,row))for row in L.tolist()],
        exact_group_sha256=hashlib.sha256(json.dumps(sorted(seen),separators=(',',':')).encode()).hexdigest(),
        meaning='Explicit two-qubit Clifford subgroup of USp(4)=Spin(5). Its central +/-I quotient is the actual 960-element Petersen stabilizer. Reduction i->2 and the frozen S identify its full lift with the actual Sp(4,5) stabilizer preimage.',
        prior='Kernel dictionary and signed SO5 action: w33_20261031_petersen_stabilizer.py. No novelty claimed for Clifford groups or Spin(5)=USp(4).',
        boundary='A mathematical four-level unitary representation, not a physical qubit/qutrit coupling, hardware implementation or spacetime derivation.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['unitary_group_order'])
