"""A conditional classical SU4 vacuum of the actual native signed cubic.

Supersymmetry, canonical Kahler potential and SU4 gauging are supplied.
SU4/USp4 is standard geometry, not a new symmetry-breaking mechanism.
This tests the explicit native embedding, F/D equations and finite stabilizer.
"""
import hashlib
import itertools
import json
import pathlib
import sys

import sympy as s

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_clifford_native_cubic_repair import cubic_terms,DUADS
from w33_20261102_spin6_rotation_group_audit import multiply


def parity(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2


def build():
    z=s.symbols('z:27')
    W=sum(c*z[a]*z[b]*z[d] for (a,b,d),c in cubic_terms().items())
    v=[s.Integer(0)]*27
    for pair in [(0,2),(1,3)]:v[DUADS.index(pair)]=1
    v[19]=v[26]=1  # u4 and v5, both SU4 singlets
    sub=dict(zip(z,v));gradient=[s.diff(W,x) for x in z]
    assert all(g.subs(sub)==0 for g in gradient)
    chi=s.zeros(4)
    for (i,j),x in zip(DUADS,v[:15]):
        if i<4 and j<4:chi[i,j]=x;chi[j,i]=-x
    assert chi*chi.conjugate().T==s.eye(4)
    moment=chi*chi.conjugate().T-s.trace(chi*chi.conjugate().T)*s.eye(4)/4
    assert moment==s.zeros(4)
    pure=v.copy();pure[19]=pure[26]=0
    assert gradient[DUADS.index((4,5))].subs(dict(zip(z,pure)))==-1
    H=s.hessian(W,z).subs(sub)
    assert H.rank()==10 and H.eigenvals()=={s.Integer(0):17,s.Integer(2):5,s.Integer(-2):5}
    generators=[]
    for i,j in itertools.combinations(range(4),2):
        X=s.zeros(4);X[i,j]=X[j,i]=s.Rational(1,2);generators.append(X)
        Y=s.zeros(4);Y[i,j]=-s.I/2;Y[j,i]=s.I/2;generators.append(Y)
    for k in range(1,4):
        generators.append(s.diag(*([1]*k+[-k]+[0]*(3-k)))/s.sqrt(2*k*(k+1)))
    assert all(s.simplify(s.trace(a*b))==(s.Rational(1,2) if i==j else 0)
               for i,a in enumerate(generators) for j,b in enumerate(generators))
    variations=[s.I*(g*chi+chi*g.T) for g in generators]
    pairs=list(itertools.combinations(range(4),2))
    gram=s.Matrix(15,15,lambda i,j:s.simplify(s.re(sum(s.conjugate(variations[i][a,b])*variations[j][a,b] for a,b in pairs))))
    assert gram.eigenvals()=={s.Integer(0):10,s.Integer(1):5}
    for variation in variations:
        dz=s.zeros(27,1)
        for pair in pairs:dz[DUADS.index(pair)]=variation[pair[0],pair[1]]
        assert H*dz==s.zeros(27,1)
    repair=json.loads((ROOT/'data/w33_20261102_clifford_native_cubic_repair.json').read_text())
    native_v=[0]*27
    for row in repair['model_to_native']:
        native_v[row['native_coordinate']]=row['sign']*int(v[row['model_coordinate']])
    old=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    native_W=sum(row['coefficient']*s.prod(z[i] for i in row['triple']) for row in old['coefficient_rows'])
    assert all(s.diff(native_W,x).subs(dict(zip(z,native_v)))==0 for x in z)
    orthogonal=json.loads((ROOT/'data/w33_20261102_spin6_rotation_group_audit.json').read_text())
    actions=[]
    for matrix in orthogonal['generator_orthogonal_matrices']:
        p=[];bits=0
        for j in range(6):
            i=next(i for i in range(6) if matrix[i][j]);p.append(i);bits|=int(matrix[i][j]<0)<<j
        actions.append((tuple(p),bits))
    def closure(gens):
        identity=(tuple(range(6)),0);seen={identity};queue=[identity]
        for a in queue:
            for g in gens:
                b=multiply(g,a)
                if b not in seen:seen.add(b);queue.append(b)
        return seen
    group=closure(actions);old_group=closure(actions[:6])
    stabilizer={a for a in group if a[0][0]==0 and not a[1]&1}
    assert len(group)==23040 and len(stabilizer)==1920 and len(old_group)==960 and old_group<=stabilizer
    orbit={(a[0][0],bool(a[1]&1)) for a in group};assert len(orbit)==12
    # For odd dimension5, Q -> det(Q)Q gives W(D5) isomorphically onto B5+.
    image=set()
    for p in itertools.permutations(range(5)):
        for bits in range(32):
            if bits.bit_count()%2:continue
            image.add((p,bits^(31 if parity(p) else 0)))
    assert len(image)==1920 and all(bits.bit_count()%2==parity(p) for p,bits in image)
    return dict(status='PASS_CONDITIONAL_CLASSICAL_NATIVE_SU4_TO_USP4_VACUUM',
        assumptions=['4D N=1 global supersymmetry','canonical Kahler potential','gauge only chosen SU4 subgroup','superpotential W=Pf6(A)+u^TAv; no added terms'],
        model_VEV=[[i,int(x)] for i,x in enumerate(v) if x],native_VEV=[[i,x] for i,x in enumerate(native_v) if x],
        family='t times this VEV, arbitrary complex t; F scales as t^2 and D as |t|^2, so both remain zero.',
        nonzero_F_terms=0,D_moment_matrix=[[str(x) for x in row] for row in moment.tolist()],
        pure_chi_F_A45=-1,singlet_repair='u4=v5=1 cancels Pf4(Omega)=-1 in F_A45.',
        holomorphic_hessian_rank=10,holomorphic_hessian_eigenvalues={'0':17,'2':5,'-2':5},
        gauge_variation_gram_eigenvalues={'0':10,'1':5},generator_normalization='Tr(Ta Tb)=delta_ab/2; duad kinetic norm sum_(i<j)|Aij|^2.',
        continuous_stabilizer='USp(4), defined by U Omega U^T=Omega inside SU4.',
        old_linear_finite_subgroup_order=1920,full_linear_finite_stabilizer_order=3840,
        exterior_square_stabilizer_order=1920,projective_stabilizer_order=1920,oriented_form_orbit_size=12,
        finite_stabilizer_identification='Six-form stabilizer is rotational signed B5+, isomorphic to W(D5) by Q -> det(Q)Q. Kernel on spinor matrices is +/-I4.',
        q5_boundary='Parallel Pass12525 identifies another W(D5) stabilizer of order1920. Abstract isomorphism here does not supply an intertwiner to that finite-field geometry.',
        matter='SU4 content 6 + 2*4 + 2*bar4 + 5*1; perturbative cubic gauge anomaly cancels, since 6 is real and the fundamentals pair.',
        quadratic_uneaten_zero_directions=12,
        boundary='Classical family in a supplied SU4 gauge model; not full E6 D-flatness, an isolated or quantum-stable vacuum, a selected scale, twelve proven nonlinear moduli, or an SM/gravity derivation.',
        references=['https://arxiv.org/abs/hep-ph/9709356','https://arxiv.org/abs/2202.05516'],
        input_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['data/w33_20261102_clifford_native_cubic_repair.json','data/w33_20261102_spin6_rotation_group_audit.json','data/w33_20261031_signed_cubic_lift.json']})


if __name__=='__main__':
    out=build()
    (ROOT/'data/w33_20261102_conditional_symplectic_vacuum.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],out['native_VEV'],out['full_linear_finite_stabilizer_order'],flush=True)
