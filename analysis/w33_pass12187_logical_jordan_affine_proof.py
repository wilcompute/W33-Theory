"""All-prime affine proof certificates for Pascal-CSS logical transvections.

The theorem is proved in PASS12187_LOGICAL_JORDAN_AFFINE_PROOF.md. Symbolic
identities and finite controls support the proof; samples are not its substitute.
Prior exact projective census: w33_20261022_pascal_css_logical_transvection_jordan.
"""
from pathlib import Path
from math import comb
import hashlib
import itertools
import json
import numpy as np
import sympy as s
import w33_20261022_pascal_css_logical_transvection_jordan as prior

ROOT = Path(__file__).resolve().parents[1]


def rank_formula(p, k):
    """Exact rank on C^perp/C; the exceptional k=0 adds one."""
    assert s.isprime(p) and 0 <= k <= p
    return (2*p**3 + p + 3)//3 if k == 0 else (p-k)*((p-k)*(2*p+k)+1)//3


def affine_exponents(p, degree):
    return [a for a in itertools.product(range(p), repeat=3) if sum(a) <= degree]


def binomial_value(t, i, p):
    return comb(t, i) % p if t >= i else 0


def evaluate(p, exponents, binomial=False):
    points = list(itertools.product(range(p), repeat=3))
    return np.array([[(binomial_value(t, a, p) if binomial else pow(t,a,p))
                     *pow(u,b,p)*pow(v,c,p) % p for t,u,v in points]
                     for a,b,c in exponents], dtype=np.int64)


def affine_count(p, k):
    """Count common binomial-basis supports, not fitted matrix ranks."""
    assert 1 <= k <= p
    image = [(a,b,c) for a in range(p-k) for b,c in
             itertools.product(range(p), repeat=2)
             if a+b+c <= 2*p-2-k]
    intersection = [z for z in image if sum(z) <= p-2]
    return len(image), len(intersection)


def symbolic_identities():
    p,k,l,j = s.symbols('p k l j', integer=True, positive=True)
    R = lambda z: (p-z)*((p-z)*(2*p+z)+1)/3
    summand = p*p-((k+l)*(k+l+1)+(p-1-l)*(p-l))/2
    identities = {
        'affine_rank_sum': s.factor(s.summation(summand,(l,0,p-1-k))-R(k)),
        'middle_Jordan_multiplicity': s.factor(R(j-1)-2*R(j)+R(j+1)-2*j),
        'J1_multiplicity': s.factor(R(0)+1-2*R(1)+R(2)-3),
        'Jp_multiplicity': s.factor(R(p-1)-p),
        'fixed_dimension': s.factor(R(0)+1-R(1)-(p*p+1)),
        'block_dimension': s.factor(3+s.summation(2*j*j,(j,2,p-1))+p*p-(R(0)+1)),
    }
    assert all(x == 0 for x in identities.values())
    return {key:str(value) for key,value in identities.items()}


def affine_matrix_control(p):
    """Independent evaluations, finite differences, GRM dual and intersections."""
    assert p in (2,3,5)
    points = list(itertools.product(range(p), repeat=3))
    idx = {v:i for i,v in enumerate(points)}
    perm = [idx[((t+1)%p,u,v)] for t,u,v in points]
    low_exp=affine_exponents(p,p-2); up_exp=affine_exponents(p,2*p-2)
    low=evaluate(p,low_exp); up=evaluate(p,up_exp,True)
    assert prior.rank(low,p)==len(low_exp)
    assert prior.rank(up,p)==len(up_exp)
    assert not np.any(low@up.T % p)
    assert len(low)+len(up)==p**3
    ranks=[]; transformed=up.copy()
    for k in range(1,p+1):
        transformed=(transformed[:,perm]-transformed)%p
        image_rank=prior.rank(transformed,p)
        intersection=len(low)+image_rank-prior.rank(np.vstack((low,transformed)),p)
        assert (image_rank,intersection)==affine_count(p,k)
        assert image_rank-intersection==rank_formula(p,k)
        ranks.append({'k':k,'image_rank':image_rank,'intersection_rank':intersection})
    return {'p':p,'shortened_dimension':len(low),'projected_dual_dimension':len(up),
            'powers':ranks}


def projective_projection_control(p):
    """Verify the shortening/projection lemma against the full native code."""
    assert p in (2,3,5)
    points=prior.projective_points(p)
    coords=np.array(points,dtype=np.int64)
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]])
    B=((coords@J@coords.T)%p!=0).astype(np.int64)
    C,_=prior.rref(B,p); N=prior.right_kernel(B,p)
    # Take w=e1, omega(x,w)=x0. Affine reps have x0=1 and t=x1.
    A=[i for i,x in enumerate(points) if x[0]!=0]
    H=[i for i,x in enumerate(points) if x[0]==0]
    coeff=prior.right_kernel(C[:,H].T,p)
    short=coeff@C[:,A]%p
    exp=affine_exponents(p,p-2)
    low=evaluate(p,exp); upper=evaluate(p,affine_exponents(p,2*p-2))
    assert prior.rank(short,p)==len(exp)
    assert prior.rank(np.vstack((short,low)),p)==len(exp)
    assert prior.rank(N[:,A],p)==len(upper)
    assert prior.rank(np.vstack((N[:,A],upper)),p)==len(upper)
    return {'p':p,'shortened_rank':len(exp),'projected_rank':len(upper)}


def build():
    data={'status':'ALL_PRIME_THEOREM_WITH_SELF_CONTAINED_PROOF_AND_FINITE_CONTROLS',
          'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'prior_census':'analysis/w33_20261022_pascal_css_logical_transvection_jordan.py',
          'theorem':{'domain':'prime p; point-coordinate symplectic noncollinearity CSS code',
            'Jordan_blocks':'J1^3 + sum(j=2..p-1) Jj^(2j) + Jp^p',
            'rank_k_ge_1':'(p-k)*((p-k)*(2*p+k)+1)/3 for 1<=k<=p',
            'shortened_code':'RM_p(p-2,3)',
            'projected_dual':'RM_p(2*p-2,3)',
            'fixed_dimension':'p^2+1'},
          'symbolic_zero_residuals':symbolic_identities(),
          'affine_controls':[affine_matrix_control(p) for p in (2,3,5)],
          'projection_controls':[projective_projection_control(p) for p in (2,3,5)],
          'prime_rows':[],'scope':{'prime_power_extension':False,'physical_local_gate':False,
            'three_particle_families':False,'derived_spacetime_or_TOE':False}}
    for p in (2,3,5,7,11,13,17,19,23,29,31):
        ranks=[rank_formula(p,k) for k in range(p+1)]
        assert all(affine_count(p,k)[0]-affine_count(p,k)[1]==ranks[k]
                   for k in range(1,p+1))
        blocks={j:ranks[j-1]-2*ranks[j]+ranks[j+1] for j in range(1,p)}
        blocks[p]=ranks[p-1]
        assert blocks==prior.predicted_blocks(p)
        data['prime_rows'].append({'p':p,'ranks':ranks,'blocks':blocks})
    return data


if __name__=='__main__':
    path=ROOT/'data/w33_pass12187_logical_jordan_affine_proof.json'
    result=build();path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'certificate':str(path),'symbolic_residuals':result['symbolic_zero_residuals'],
                      'tested_primes':[r['p'] for r in result['prime_rows']]}))
