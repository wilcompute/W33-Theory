"""An all-field obstruction to bounded-degree matching parametrizations.

For a degree-d morphism f:P1->P1, agreeing with an involution on all q+1
rational points forces d=1 if q>d^2. A projective involution pairs conic
points through a common center, so its chord poles are collinear.
This is NOT a classification of arbitrary exterior arcs.
"""
import json,pathlib,itertools,math
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1]

def null_mod(A,p):
    a=[[int(v)%p for v in row]for row in A];n=len(a[0]);r=0;piv=[]
    for c in range(n):
        k=next((k for k in range(r,len(a))if a[k][c]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r];iv=pow(a[r][c],-1,p);a[r]=[v*iv%p for v in a[r]]
        for k in range(len(a)):
            if k!=r:
                v=a[k][c];a[k]=[(x-v*y)%p for x,y in zip(a[k],a[r])]
        piv.append(c);r+=1
    out=[]
    for c in range(n):
        if c not in piv:
            v=[0]*n;v[c]=1
            for j,k in enumerate(piv):v[k]=-a[j][c]%p
            out.append(v)
    return out

def interpolation(q,matching):
    infinity=q;pi={}
    for a,b in matching:
        a=infinity if a=='inf' else a;b=infinity if b=='inf' else b;pi[a]=b;pi[b]=a
    x=s.symbols('x');rows=[]
    for d in range(1,(q+3)//2+1):
        equations=[]
        for a,b in pi.items():
            mon=[0]*d+[1]if a==infinity else[pow(a,j,q)for j in range(d+1)]
            equations.append(mon+[0]*(d+1)if b==infinity else[u for u in mon]+[-b*u%q for u in mon])
            if b==infinity:equations[-1]=[0]*(d+1)+mon
        basis=null_mod(equations,q);rows.append(dict(degree=d,nullity=len(basis)))
        # Complete projective coefficient enumeration; encountered solution
        # spaces are small. No truncated search is used as a minimality proof.
        assert len(basis)<=5,(q,rows)
        for coeff in itertools.product(range(q),repeat=len(basis)):
            if not any(coeff)or next(c for c in coeff if c)!=1:continue
            v=[sum(c*b[j]for c,b in zip(coeff,basis))%q for j in range(2*d+2)]
            F=sum(v[j]*x**j for j in range(d+1));G=sum(v[d+1+j]*x**j for j in range(d+1))
            if not F or not G or (not v[d]and not v[-1]):continue
            if s.degree(s.gcd(s.Poly(F,x,modulus=q),s.Poly(G,x,modulus=q)))!=0:continue
            return dict(q=q,minimum_morphism_degree=d,lower_bound=math.isqrt(q-1)+1,
                numerator_coefficients=v[:d+1],denominator_coefficients=v[d+1:],degree_rank_checks=rows)
    raise AssertionError('No interpolating morphism in the tested exhaustive degrees')

def conference(q,matching):
    import numpy as np
    order=[q if a=='inf'else a for pair in matching for a in pair]
    squares={a*a%q for a in range(1,q)}
    chi=lambda a:0 if not a%q else 1 if a%q in squares else -1
    det=lambda a,b:0 if a==b else 1 if a==q else -1 if b==q else a-b
    C=np.array([[chi(det(a,b))for b in order]for a in order],dtype=int)
    assert np.array_equal(C@C.T,q*np.eye(q+1,dtype=int))
    assert np.array_equal(C.T,-C)
    for i,j in itertools.combinations(range((q+1)//2),2):
        B=C[2*i:2*i+2,2*j:2*j+2];assert np.array_equal(B@B.T,2*np.eye(2,dtype=int))
    return dict(q=q,reordered_Paley_conference=C.tolist(),off_diagonal_blocks='Every 2x2 block is Hadamard. This is equivalent to the pairwise nonsquare predicate, not to absence of three collinear poles.')

def build():
    old=json.loads((ROOT/'data/w33_20261031_exterior_search.json').read_text())
    rows=[r for r in old if r['status']=='found']
    return dict(status='PASS_ALL_FIELD_BOUNDED_DEGREE_OBSTRUCTION',
        theorem='For any odd prime power q>3, any good matching represented by a degree-d rational morphism P1->P1 must satisfy d^2>=q.',
        proof='The homogeneous cross-product of f composed with f and the identity has degree d^2+1. It vanishes at all q+1 rational points. If q>d^2 it vanishes identically, so degree(f)^2=1. A nontrivial degree-one involution is represented in odd characteristic by a trace-zero matrix. Every chord joining t to f(t) passes through one fixed projective center; polar chord poles are collinear. At q>3 a matching has at least three chords, violating the arc condition.',
        excluded_family='Any uniformly bounded-degree rational formula for infinitely increasing field orders. Arbitrary matching functions, including degree growing at least sqrt(q), are not excluded.',
        interpolations=[interpolation(r['q'],r['matching'])for r in rows if r['q']>3],
        conference_controls=[conference(r['q'],r['matching'])for r in rows],
        boundary='The Paley block identity alone does not encode the no-three-collinear condition. An all-q classification remains open; no further finite searches are promoted to a proof.',
        prior='Conic polarity and exterior matching equivalence: w33_20261031_conic_exterior_arc_bridge.py. Paley conference matrices and degree multiplicativity of rational maps are classical.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261031_arc_degree_obstruction.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['interpolations'])
