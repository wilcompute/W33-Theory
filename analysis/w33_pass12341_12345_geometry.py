"""Exact soft-mode locus and reflection-slice tests on the native cover.

Prior owners: Pass12340's order-three witness, the Oct28 three-mixed endpoint,
and the Oct27 native-cover reflection. No physical 3+1 orbifold is assumed.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'analysis'))
import w33_20261027_five_front_followthrough as prior
import w33_pass12340_mixed_loop_exception as previous

R = sp.Matrix([[1,0,5,-5,1,0],[0,1,-1,0,1,0],[0,0,5,-5,0,1]])
PAIRS = list(combinations(range(4),2))
OMEGA = (-sp.Integer(1)+sp.I*sp.sqrt(3))/2
POWERS = ((1,0),(0,1),(-1,-1))


def clean(counter):
    return {k:v for k,v in counter.items() if v}


def path_laurent(path, voltages):
    position = np.zeros(4,dtype=int)
    coefficients = Counter()
    for e,sign in path:
        e,sign=int(e),int(sign)
        if sign<0:
            position-=voltages[e]
        coefficients[(e,tuple(map(int,position)))]+=sign
        if sign>0:
            position+=voltages[e]
    return clean(coefficients),tuple(map(int,position))


def shift_poly(poly,period):
    return {(e,tuple(x+y for x,y in zip(position,period))):v
            for (e,position),v in poly.items()}


def sum_poly(*terms):
    c=Counter()
    for scale,poly in terms:
        for key,value in poly.items():
            c[key]+=scale*value
    return clean(c)


def unit_minor(paths,voltages):
    """Deterministic fraction-free row elimination over Z[z_i,z_i^-1].

    Every pivot is a unit +/-z^v. The selected square minor's determinant
    is the recorded unit. Operations use only integer Laurent polynomials;
    no generic-point or floating-rank argument enters the proof.
    """
    rows=[];original=[]
    for path in paths:
        terms,_=path_laurent(path,voltages);row={}
        for (edge,power),value in terms.items():
            row.setdefault(edge,{})[power]=value
        rows.append(row);original.append({j:p.copy() for j,p in row.items()})
    columns=[];powers=[];sign=1;pivots=[]
    def unit(p):return len(p)==1 and abs(next(iter(p.values())))==1
    def subtract(old,left,right,shift):
        out=old.copy()
        for p,a in left.items():
            for q,b in right.items():
                key=tuple(p[i]+q[i]-shift[i] for i in range(4))
                out[key]=out.get(key,0)-a*b
                if out[key]==0:del out[key]
        return out
    while rows:
        colfreq=Counter(j for row in rows for j in row)
        candidates=[((colfreq[j]-1)*(len(row)-1),len(row),i,j)
                    for i,row in enumerate(rows) for j,poly in row.items() if unit(poly)]
        assert candidates,('Nonunit pivot required',len(rows))
        _,_,i,j=min(candidates);pivot=rows.pop(i)
        exponent,value=next(iter(pivot[j].items()))
        columns.append(j);powers.append(exponent);sign*=(-1)**i*value
        pivots.append(dict(row_position=i,column=j,power=list(exponent),sign=value))
        for k in pivot:
            pivot[k]={p:value*c for p,c in pivot[k].items()}
        for row in rows:
            if j not in row:continue
            left=row.pop(j)
            for k,poly in pivot.items():
                if k==j:continue
                value2=subtract(row.get(k,{}),left,poly,exponent)
                if value2:row[k]=value2
                elif k in row:del row[k]
    total=[sum(v[i] for v in powers) for i in range(4)]
    # Direct modular determinants independently check row permutations,
    # pivot-sign bookkeeping and all four negative Laurent powers.
    controls=[]
    for modulus,z in ((101,(2,3,5,7)),(103,(2,3,5,7)),(107,(3,4,7,11))):
        A=np.zeros((len(original),len(columns)),dtype=np.int64)
        for i,row in enumerate(original):
            for j,col in enumerate(columns):
                for exp,c in row.get(col,{}).items():
                    term=int(c)%modulus
                    for base,power in zip(z,exp):term=term*pow(base,power,modulus)%modulus
                    A[i,j]=(A[i,j]+term)%modulus
        determinant=1
        for j in range(len(columns)):
            options=np.flatnonzero(A[j:,j]);assert len(options)
            k=j+int(options[0])
            if k!=j:A[[j,k]]=A[[k,j]];determinant=-determinant
            pivot=int(A[j,j]);determinant=determinant*pivot%modulus
            factor=A[j+1:,j]*pow(pivot,-1,modulus)%modulus
            A[j+1:]=(A[j+1:]-factor[:,None]*A[j])%modulus
        expected=sign%modulus
        for base,power in zip(z,total):expected=expected*pow(base,power,modulus)%modulus
        assert determinant%modulus==expected
        controls.append(dict(modulus=modulus,values=list(z),determinant=int(expected)))
    return dict(size=len(columns),columns=columns,sign=sign,power=total,
                pivot_witness=pivots,modular_determinant_controls=controls)


@lru_cache(None)
def symbol_certificate():
    B,V,edges,loops,W,comm,_,M=prior.inputs()
    W=sp.Matrix(W);M=sp.Matrix(M)
    assert W.det()==1
    paths=[path_laurent(path,V) for path in loops]
    assert [list(x[1]) for x in paths] == W.tolist()
    for k,(i,j) in enumerate(PAIRS):
        actual,period=path_laurent(comm[k],V)
        expected=sum_poly((1,paths[i][0]),(-1,shift_poly(paths[i][0],list(W[j,:]))),
                          (1,shift_poly(paths[j][0],list(W[i,:]))),(-1,paths[j][0]))
        assert period==(0,0,0,0) and actual==expected
    faces=json.loads((ROOT/'data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json').read_text())['independent_face_basis']
    short_minor=unit_minor([f['boundary'] for f in faces],V)
    augmented_minor=unit_minor([f['boundary'] for f in faces]+list(loops),V)
    assert (short_minor['size'],short_minor['sign'],short_minor['power'])==(105,-1,[-12,2,18,-15])
    assert (augmented_minor['size'],augmented_minor['sign'],augmented_minor['power'])==(109,1,[-14,2,20,-18])
    # This identity holds as Laurent polynomials, not only at sampled momenta.
    N=W.inv().T*M*W.inv()
    # A quantitative zero-free neighborhood for real loop angles.
    assert [N[:j,:j].det() for j in range(1,5)]==[10,75,540,2916]
    assert max(sum(abs(x) for x in row) for row in N.tolist())==30
    assert max(sum(abs(x) for x in row) for row in N.inv().tolist())==sp.Rational(23,54)
    delta0=sp.Rational(1,20)
    zero_free_lower=sp.Rational(27,23)-30*(delta0/2+delta0**2/8)
    assert zero_free_lower==sp.Rational(3051,7360)>0
    d=sp.Matrix(sp.symbols('d0:4'))
    C=sp.Matrix([[d[a]*int(b==j)-d[b]*int(a==j) for j in range(4)]
                 for a,b in PAIRS])
    Q=sp.expand((d.T*N*d)[0]/2)
    mixed=R*C
    minors=[sp.factor(mixed[:,[k for k in range(4) if k!=j]].det()) for j in range(4)]
    for j,value in enumerate(minors):
        assert sp.expand(value-(-1)**j*d[j]*Q)==0
    # A rank-one mixed symbol would make every 2x2 minor vanish.
    two=[sp.expand(mixed.extract(ii,jj).det()) for ii in combinations(range(3),2)
         for jj in combinations(range(4),2)]
    groebner=[]
    for i in range(4):
        basis=sp.groebner([p.subs(d[i],1) for p in two],*[d[j] for j in range(4) if j!=i])
        assert [x.as_expr() for x in basis.polys]==[1]
        groebner.append('1')
    complement=sp.Matrix([[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0]])
    assert R.col_join(complement).det()==-1
    # Known first witness: h=(omega,omega^2,1,1).
    h=sp.Matrix([OMEGA,sp.conjugate(OMEGA),1,1])
    delta=h-sp.ones(4,1)
    assert sp.simplify((delta.T*N*delta)[0])==0
    deriv=[sp.simplify(sp.I*h[i]*(N*delta)[i]) for i in range(4)]
    jac=sp.Matrix([[sp.simplify(sp.re(x)) for x in deriv],
                   [sp.simplify(sp.im(x)) for x in deriv]])
    assert sp.simplify(jac[:,:2].det()+225*sp.sqrt(3)/2)==0
    # Point on the actual reflection-fixed momentum torus z0=1.
    z=[sp.Integer(1),sp.Integer(1),OMEGA,sp.conjugate(OMEGA)]
    h2=sp.Matrix([sp.simplify(sp.prod(z[j]**int(W[i,j]) for j in range(4))) for i in range(4)])
    delta2=h2-sp.ones(4,1)
    assert sp.simplify((delta2.T*N*delta2)[0])==0
    deriv2=sp.Matrix([sp.simplify(sp.I*h2[i]*(N*delta2)[i]) for i in range(4)])
    dz=W.T*deriv2
    fixedjac=sp.Matrix([[sp.simplify(sp.re(dz[i])) for i in (1,2,3)],
                        [sp.simplify(sp.im(dz[i])) for i in (1,2,3)]])
    assert sp.simplify(fixedjac[:,[0,1]].det()-54*sp.sqrt(3))==0
    # Exact third-root census via integer coefficients a+b*omega.
    Wint=np.array(W.tolist(),dtype=int);Nint=np.array(N.tolist(),dtype=int)
    deltas=((0,0),(-1,1),(-2,-1));third_roots=[]
    for labels in product(range(3),repeat=4):
        if not any(labels):continue
        exponents=Wint@np.array(labels)%3
        a=np.array([deltas[v][0] for v in exponents],dtype=int)
        b=np.array([deltas[v][1] for v in exponents],dtype=int)
        if a@Nint@a-b@Nint@b==0 and 2*a@Nint@b-b@Nint@b==0:
            third_roots.append(list(labels))
    assert len(third_roots)==10
    return dict(period_matrix=[[int(x) for x in row] for row in W.tolist()],
        N=[[int(x) for x in row] for row in N.tolist()],Q=str(Q),
        three_by_three_minors=list(map(str,minors)),
        six_exact_laurent_loop_identities=True,
        short_global_unit_minor=short_minor,augmented_global_unit_minor=augmented_minor,
        two_by_two_minors_projective_groebner=groebner,
        third_root_nonidentity_zeros=third_roots,
        period_three_real_zero_modes=dict(three_mixed=14,six_loop_or_either_repair=4,
            explanation='Four identity-character global holonomies plus ten real dimensions from five conjugate pairs of nonidentity Q=0 characters.'),
        original_character=['omega','omega','1','1'],
        original_loop_character=['omega','omega^2','1','1'],
        first_two_angle_jacobian_determinant=str(jac[:,:2].det()),
        reflection_fixed_character=['1','1','omega','omega^2'],
        fixed_slice_jacobian_minor=str(fixedjac[:,[0,1]].det()),
        global_classification='At every nonidentity z in (C*)^4, short rank=105 and six-loop rank=108. Mixed rank is107 iff Q(h(z)-1)=0 and108 otherwise; on the unitary torus the respective nongauge nullities are1 and0. At identity the short/mixed/six ranks are105 and gradient rank26, leaving4 holonomies.',
        repaired_kernel='Both the Pass12340 24-term repair and the parallel449bcd3c 12-term unimodular-complement repair have exactly the six-loop kernel for every unitary character. Therefore each has no nonidentity nongauge magnetic zero anywhere on the torus.',
        zero_free_angle_bound=dict(max_abs_loop_angle='1/20',
          coefficient='3051/7360',
          inequality='|Q(exp(i*t)-1)| >= (3051/7360) ||t||_2^2 when max_i |t_i| <= 1/20.',
          proof='Write exp(it)-1=it+r with ||r||_2 <= max|t_i|*||t||_2/2. The exact positive N has lambda_min>=54/23 and norm<=30, giving 27/23 - 30*(delta/2+delta^2/8).'),
        local_dimension='The real unitary torus has a smooth 2D Q=0 sheet near the original witness; the fixed z0=1 slice has a smooth 1D intersection near its specified witness.')


def pairmul(a,b,c,d):
    return a@c-b@d, a@d+b@c-b@d


def rank(a,b):
    lifted=np.block([[a,-b],[b,a-b]])
    value=DomainMatrix.from_Matrix(sp.Matrix(lifted)).to_field().rank()
    assert value%2==0
    return value//2


@lru_cache(None)
def fixed_momentum_operators():
    B,V,edges,_,_,loops,_,_=prior.inputs()
    faces=json.loads((ROOT/'data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json').read_text())['independent_face_basis']
    exponent=np.array([0,0,1,2])
    def row(path):
        a=np.zeros(135,dtype=object);b=a.copy();position=np.zeros(4,dtype=int)
        for e,sgn in path:
            if sgn<0:position-=V[e]
            u,v=POWERS[int(position@exponent)%3]
            a[e]+=int(sgn)*u;b[e]+=int(sgn)*v
            if sgn>0:position+=V[e]
        assert not position.any()
        return a,b
    face=[row(x['boundary']) for x in faces]
    loop=[row(x) for x in loops]
    a,b=(np.array([v[i] for v in face],dtype=object) for i in (0,1))
    c,d=(np.array([v[i] for v in loop],dtype=object) for i in (0,1))
    rr=np.array(R.tolist(),dtype=object)
    f0,f1=np.vstack([a,rr@c]),np.vstack([b,rr@d])
    f60,f61=np.vstack([a,c]),np.vstack([b,d])
    d0=np.zeros((135,27),dtype=object);d1=d0.copy()
    for e,(u,v) in enumerate(edges):
        a0,b0=POWERS[int(V[e]@exponent)%3]
        d0[e,u]=-1;d0[e,v]=a0;d1[e,v]=b0
    # Exact infinite-cover lift from the already-owned reflection certificate.
    perm=[18,20,19,23,22,21,25,24,26,9,11,10,14,13,12,16,15,17,0,2,1,5,4,3,7,6,8]
    offsets=np.array([[0,0,0,0]]*3+[[-1,0,1,-1]]*3+[[-1,0,1,0]]*3+
                     [[0,0,0,0]]*3+[[-1,0,0,0]]*3+[[0,0,0,0]]*6+
                     [[0,0,-1,1]]*3+[[0,0,-1,0]]*3)
    lookup={edge:i for i,edge in enumerate(edges)}
    p0=np.zeros((135,135),dtype=object);p1=p0.copy()
    for i,(u,v) in enumerate(edges):
        j=lookup[tuple(sorted((perm[u],perm[v])))]
        sg=1 if perm[u]<perm[v] else -1
        position=offsets[u]-(V[j] if sg<0 else 0)
        x,y=POWERS[int(position@exponent)%3]
        p0[i,j]=sg*x;p1[i,j]=sg*y
    v0=np.zeros((27,27),dtype=object);v1=v0.copy()
    for i in range(27):
        x,y=POWERS[int(offsets[i]@exponent)%3]
        v0[i,perm[i]]=x;v1[i,perm[i]]=y
    return (f0,f1,f60,f61,d0,d1,p0,p1,v0,v1)


def reflection_certificate():
    f0,f1,f60,f61,d0,d1,p0,p1,v0,v1=fixed_momentum_operators()
    for a,b,size in ((p0,p1,135),(v0,v1,27)):
        x,y=pairmul(a,b,a,b)
        assert np.array_equal(x,np.eye(size,dtype=object)) and not np.any(y)
    lhs=pairmul(p0,p1,d0,d1);rhs=pairmul(d0,d1,v0,v1)
    assert all(np.array_equal(x,y) for x,y in zip(lhs,rhs))
    fd=pairmul(f0,f1,d0,d1)
    assert not np.any(fd[0]) and not np.any(fd[1])
    ranks=dict(mixed=rank(f0,f1),six=rank(f60,f61),gradient=rank(d0,d1))
    assert ranks==dict(mixed=107,six=108,gradient=27)
    parities={}
    for sign in (1,-1):
        joint=rank(np.vstack([f0,p0-sign*np.eye(135,dtype=object)]),np.vstack([f1,p1]))
        vertex=rank(v0-sign*np.eye(27,dtype=object),v1)
        nongauge=135-joint-(27-vertex)
        assert nongauge==0
        parities[str(sign)]=dict(joint_rank=joint,vertex_parity_constraint_rank=vertex,
                                 surviving_nongauge_nullity=nongauge)
    return dict(character=['1','1','omega','omega^2'],exact_ranks=ranks,
        full_unprojected_nongauge_nullity=1,parity_constraints=parities,
        exact_reflection_square_and_gauge_intertwining=True,
        scope='At this one fixed Bloch character, either imposed edge parity removes the individual nongauge null line. The selected-face action is not itself invariant under the reflection; this is a constrained linear calculation, not a constructed anomaly-free orbifold or a global zero-locus classification.')


def run():
    return dict(schema='w33.pass12341_12345.geometry.v1',symbol=symbol_certificate(),
        reflection=reflection_certificate(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        prior_owners=['analysis/w33_pass12340_mixed_loop_exception.py',
                      'analysis/w33_20261028_three_mixed_loop_minimal_maxwell.py',
                      'analysis/w33_20261027_microscopic_response_and_lifts.py',
                      'analysis/w33_20261028_sixfront_ratio_and_12repair.py'])


if __name__=='__main__':
    data=run();target=ROOT/'data/w33_pass12341_12345_geometry.json'
    target.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',fixed_parities=data['reflection']['parity_constraints'])))
