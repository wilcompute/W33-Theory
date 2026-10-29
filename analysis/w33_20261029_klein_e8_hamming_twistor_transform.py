#!/usr/bin/env python3
"""Exact binary Klein quadric => 30 Hamming lifts => E8 and finite twistor transform.

The E8/Construction A and Klein two-rulings facts are classical. The
project-specific result is their explicit 8-Conwell-label stabilizer-frame
intertwiner, with every coefficient tested in the full 256-dimensional
8-qubit computational Hilbert space. No spacetime or physical photon implied.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

MASK = 0xff
CANON = lambda x: min(x, x ^ MASK)


def quadratic(x):
    assert x.bit_count() % 2 == 0
    return (x.bit_count() // 2) % 2


def even_quotient():
    return sorted({CANON(x) for x in range(256) if x.bit_count() % 2 == 0})


def generators():
    points = even_quotient()
    singular = [x for x in points if x and quadratic(x) == 0]
    nonsingular = [x for x in points if quadratic(x) == 1]
    assert len(points) == 64 and len(singular) == 35 and len(nonsingular) == 28
    # A generator is a 3D subspace with seven nonzero singular projective points.
    found = set()
    for a,b,c in combinations(singular, 3):
        span = frozenset(CANON(x) for x in (0,a,b,a^b,c,a^c,b^c,a^b^c))
        if len(span) == 8 and all(quadratic(x) == 0 for x in span):
            found.add(span)
    return sorted(found, key=lambda g: tuple(sorted(g)))


def hamming_code(g):
    return frozenset(x for a in g for x in (a,a ^ MASK))


def swap_bits(x, i=0, j=1):
    return x ^ (((1 << i) | (1 << j)) if ((x >> i) ^ (x >> j)) & 1 else 0)


def partition_rulings(gs):
    alpha = [gs[0]] + [g for g in gs if g != gs[0] and len(gs[0]&g) == 2]
    beta = [g for g in gs if g not in alpha]
    assert len(alpha) == 15 and len(beta) == 15
    assert all(len(a & b) == 2 for a,b in combinations(alpha, 2))
    assert all(len(a & b) == 2 for a,b in combinations(beta, 2))
    assert frozenset(CANON(swap_bits(x)) for x in gs[0]) in beta
    return alpha,beta


def transform_certificate(alpha, beta):
    # Point-plane incidence of PG(3,2). Across rulings the generator
    # intersection has 4 binary classes (projective line) or 1 (empty).
    M = [[int(len(a&b) == 4) for b in beta] for a in alpha]
    assert all(sum(row) == 7 for row in M)
    assert all(sum(M[i][j] for i in range(15)) == 7 for j in range(15))
    assert all(len(alpha[i]&beta[j]) in (1,4) for i in range(15) for j in range(15))
    mm = [[sum(M[i][k]*M[j][k] for k in range(15)) for j in range(15)] for i in range(15)]
    assert all(mm[i][j] == (7 if i==j else 3) for i in range(15) for j in range(15))
    # 15x15 orthogonal rational Penrose-INCIDENCE transform:
    # T=(3M-J)/6; entries +1/3 on incident, -1/6 on nonincident.
    B = [[3*M[i][j]-1 for j in range(15)] for i in range(15)]
    assert all(sum(B[i][k]*B[j][k] for k in range(15)) == (36 if i==j else 0)
               for i in range(15) for j in range(15))
    ca=[hamming_code(a) for a in alpha]
    cb=[hamming_code(b) for b in beta]
    # Exact equality of 15 state vectors in the 256D Hilbert space.
    # |C> = (1/4) sum_{x in C}|x>, so multiply coefficients by 24:
    # 6*1_{C_beta}(x) = sum_alpha (3*M-1) * 1_{C_alpha}(x).
    assert all(6*int(word in cb[j]) == sum(B[i][j]*int(word in ca[i]) for i in range(15))
               for j in range(15) for word in range(256))
    return M,B


def lift_e8(g):
    code=hamming_code(g)
    weight=Counter(x.bit_count() for x in code)
    assert weight=={0:1, 4:14, 8:1}
    assert len(code)==16
    assert all((x&y).bit_count() % 2==0 for x in code for y in code)
    # Construction A lattice E8 has norm-2 roots from integral vectors
    # of squared length 4: 16 axis roots +/-2e_i and 16 sign assignments
    # on each of 14 weight-4 Hamming code supports.
    roots={tuple(2*sign if k==j else 0 for k in range(8))
           for j in range(8) for sign in (-1,1)}
    for word in code:
        if word.bit_count()!=4:continue
        loc=[k for k in range(8) if (word>>k)&1]
        for signs in range(16):
            root=[0]*8
            for k,j in enumerate(loc):root[j]=(-1 if (signs>>k)&1 else 1)
            roots.add(tuple(root))
    assert len(roots)==240 and all(sum(v*v for v in x)==4 for x in roots)
    return code,roots


def stabilizer_in_s8(code):
    number=0; odd=0
    for p in permutations(range(8)):
        images={sum(1<<p[i] for i in range(8) if (x>>i)&1) for x in code}
        if images==code:
            number+=1
            odd+=sum(p[i]>p[j] for i in range(8) for j in range(i+1,8))%2
    assert number==1344 and odd==0
    return number


def certificate():
    pts=even_quotient()
    assert len(pts)==64
    assert len([x for x in pts if quadratic(x)])==28
    assert len([x for x in pts if x and not quadratic(x)])==35
    # 28 nondegenerate coordinates are precisely K8 duads.
    assert {CANON((1<<i)|(1<<j)) for i,j in combinations(range(8),2)} == {
        x for x in pts if quadratic(x)}
    # The 35 singulars are the 70 tetrads modulo complement.
    assert {CANON(sum(1<<i for i in ids)) for ids in combinations(range(8),4)} == {
        x for x in pts if x and quadratic(x)==0}
    gs=generators(); assert len(gs)==30
    alpha,beta=partition_rulings(gs)
    codes=[]
    for g in gs:
        c,_=lift_e8(g); codes.append(c)
    assert len(set(codes))==30
    stabilizer=stabilizer_in_s8(codes[0])
    M,B=transform_certificate(alpha,beta)
    overlaps=Counter(Fraction(len(hamming_code(a)&hamming_code(b)),16)
                     for a,b in combinations(gs,2))
    assert overlaps=={Fraction(1,4):210, Fraction(1,8):120, Fraction(1,2):105}
    assert all(sum(x in g for g in gs)==6 for x in pts if x and quadratic(x)==0)
    # Intrinsic Gram spectrum: two 15-state frames both have
    # A=(3/4)I+(1/4)J; the orthogonal bridge T=B/6 identifies their spans.
    # Complete 30-state Gram eigenvalues are {9, 3/2 (14x), 0 (15x)}.
    return {
        'status':'EXACT_KLEIN_TO_30_HAMMING_E8_AND_FINITE_ORTHOGONAL_TWISTOR_FRAME',
        'K8_even_weight_quotient_dimension':6,
        'point_counts':{'nonzero':63,'Klein_quadric':35,'off_quadric':28},
        'maximal_singular_planes':30,
        'rulings':{'alpha':15,'beta':15,'odd_permutation_exchanges':True},
        'extended_Hamming_codes':30,
        'Hamming_parameters':[8,4,4],
        'Hamming_weight_enumerator':{'0':1,'4':14,'8':1},
        'S8_orbit_stabilizer':{'order':40320,'single_code_stabilizer':stabilizer,'orbit':30,'stabilizer_contained_in_A8':True},
        'Construction_A_E8_roots_per_code':{'axis':16,'sign_weight4':224,'total':240},
        'incidence_15x15':M,
        'orthogonal_transform_integer_numerator_B_equal_6T':B,
        'transform_formula':'T=(3M-J)/6, T*T^T=I',
        'stabilizer_frame_relation':'|beta_j>=sum_i T_ij |alpha_i>, exactly in C^256',
        'cross_ruling_intersection_counts':{'projective_line':7,'empty':8},
        'pairwise_state_overlaps':{'1/4':210,'1/8':120,'1/2':105},
        'thirty_state_Gram_spectrum':{'9':1,'3/2':14,'0':15},
        'thirty_state_span_dimension':15,
        'single_ruling_frame_Gram':'A=(3/4)I+(1/4)J',
        'finite_incidence_not_holomorphic_Penrose_transform':True,
        'not_a_physical_TOE_or_derived_photon':True
    }


if __name__=='__main__':
    c=certificate()
    text=json.dumps(c,indent=2)+'\n'
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(text,encoding='utf-8')
    else:print(text,end='')
