"""Exact projective qutrit holonomies saturate all eight Y7 torsion periods.

Analytic topology identifying the torsion-cycle pairings is in the companion
report. Integer monomial arithmetic verifies every group and cocycle relation.
Also constructs a compensated abstract flat E8 holonomy. No G2 metric or
computation of all twisted K groups is supplied.
"""
import json
from itertools import product, combinations_with_replacement
from pathlib import Path
from toe_20261119_h27_integral_torsion_gerbes import GROUP, multiply

I = ((0, 1, 2), (0, 0, 0))
X = ((1, 2, 0), (0, 0, 0))
D = ((0, 1, 2), (0, 0, 1))


def mul(a, b):
    return (tuple(a[0][b[0][j]] for j in range(3)),
            tuple((b[1][j]+a[1][b[0][j]]) % 3 for j in range(3)))


def inv(a):
    p = tuple(a[0].index(j) for j in range(3))
    return p, tuple(-a[1][p[j]] % 3 for j in range(3))


def power(a, n):
    if n < 0:
        return power(inv(a), -n)
    out = I
    for _ in range(n):
        out = mul(out, a)
    return out


def comm(a, b):
    return mul(mul(mul(a, b), inv(a)), inv(b))


def scalar(a):
    assert a[0] == I[0] and len(set(a[1])) == 1, a
    return a[1][0]


def canonical(a):
    return a[0], tuple((p-a[1][0]) % 3 for p in a[1])


def closure(generators, projective=False):
    normalize = canonical if projective else lambda a:a
    found, queue = {I}, [I]
    while queue:
        a = queue.pop()
        for g in generators:
            b = normalize(mul(a, g))
            if b not in found:
                found.add(b)
                queue.append(b)
    return found


def e8_matter_descent(matrices):
    """Explicit 81-block of the standard (E6 x SU3)/Z3 embedding.

Trinification gives r(g)=(1,conj(g),g), with 27=7*3+6bar.
The pair (r(conj(g)),g) descends from SU3 to PSU3 because its
central phases cancel. We check the faithful (27,3) block, in an
abstract branching basis, not the repo's native Albert coordinates.
"""
    def mul9(a,b):
        n=len(a[0])
        return (tuple(a[0][b[0][j]] for j in range(n)),
                tuple((b[1][j]+a[1][b[0][j]])%9 for j in range(n)))
    def normalized_SU3(a):
        assert a[0] in ((0,1,2),(1,2,0),(2,0,1))
        phase=[3*t for t in a[1]]
        correction=(sum(phase)%9)//3
        result=(a[0],tuple((t-correction)%9 for t in phase))
        assert sum(result[1])%9==0
        return result
    def block81(a):
        # 27 under r(conj(g)): seven 3bar blocks and Sym^2(3).
        perm=[];phase=[]
        for k in range(7):
            perm.extend(3*k+j for j in a[0])
            phase.extend(-t%9 for t in a[1])
        pairs=list(combinations_with_replacement(range(3),2))
        for i,j in pairs:
            perm.append(21+pairs.index(tuple(sorted((a[0][i],a[0][j])))))
            phase.append((a[1][i]+a[1][j])%9)
        return (tuple(3*perm[i]+a[0][j] for i,j in product(range(27),range(3))),
                tuple((phase[i]+a[1][j])%9 for i,j in product(range(27),range(3))))
    # Central generator maps to the identity on all 81 components.
    assert block81(((0,1,2),(3,3,3))) == (tuple(range(81)),(0,)*81)
    normalized={g:normalized_SU3(a) for g,a in matrices.items()}
    blocks={g:block81(a) for g,a in normalized.items()}
    for g,h in product(GROUP,repeat=2):
        assert mul9(blocks[g],blocks[h])==blocks[multiply(g,h)]
    assert len(set(blocks.values()))==27
    # E6 adjoint restricts to 14 trivial plus eight adjoint SU3 copies.
    # Together with flavor8, E8 character is 14+9*chi8+chi81+conj(chi81).
    # Accumulate exactly in Z[zeta9]/(zeta9^6+zeta9^3+1).
    charsum=[0]*9
    for g,a in normalized.items():
        charsum[0]+=14-9
        trace=[a[1][j] for j in range(3) if a[0][j]==j]
        for p,q in product(trace,repeat=2):charsum[(p-q)%9]+=9
        for j in range(81):
            if blocks[g][0][j]==j:
                p=blocks[g][1][j]
                charsum[p]+=1;charsum[-p%9]+=1
    for j in range(8,5,-1):
        c=charsum[j];charsum[j]=0
        charsum[j-3]-=c;charsum[j-6]-=c
    assert charsum==[810,0,0,0,0,0,0,0,0]
    return {'faithful_27_times3_block_dimension':81,
            'exact_unprojectivized_product_checks':729,
            'finite_E8_holonomy_image_order':27,
            'exact_E8_adjoint_character_sum':810,
            'E8_parallel_adjoint_invariant_dimension':30,
            'embedding':'PSU3 -> (E6 x SU3)/Z3 -> E8; [g] -> [(r(conj(g)),g)], r(g)=(1,conj(g),g) in E6 trinification',
            'E6_27_restriction_on_compensating_factor':'7*3bar + Sym^2(3)',
            'scope':'Global flat E8 holonomy on this Y, in a standard abstract branching basis. Not a native Albert intertwiner, SM centralizer, nonproportional PW-compatible background or G2 metric.'}


def certificate(U, V):
    C = comm(U, V)
    assert power(C, 3) == I
    pair = (scalar(comm(U, C)), scalar(comm(V, C)))
    assert pair != (0, 0)
    # Normal form B^b A^a C^c matches the source's cocycle a*b'.
    def rho(g):
        a, b, c = g
        return mul(mul(power(V, b), power(U, a)), power(C, c))
    matrices = {g:rho(g) for g in GROUP}
    sigma = {}
    for g, h in product(GROUP, repeat=2):
        sigma[g,h] = scalar(mul(mul(matrices[g], matrices[h]), inv(matrices[multiply(g,h)])))
    checks = 0
    for g, h, k in product(GROUP, repeat=3):
        assert (sigma[g,h]+sigma[multiply(g,h),k]
                -sigma[h,k]-sigma[g,multiply(h,k)]) % 3 == 0
        checks += 1
    assert len(closure([U,V], projective=True)) == 27
    assert len(closure([U,V])) == 81
    # The two commuting source pairs detect torsion two-cycle holonomy.
    for g, expected in (((1,0,0),pair[0]), ((0,1,0),pair[1])):
        c = (0,0,1)
        assert (sigma[g,c]-sigma[c,g]) % 3 == expected
    return {'U':U, 'V':V, 'C':C,
            'torsion_cycle_pairing_exponents_mod3':pair,
            'projective_image_order':27, 'unitary_lift_group_order':81,
            'projective_product_checks':27**2, 'scalar_cocycle_checks':checks,
            'E8_compensated_descent':e8_matter_descent(matrices)}


def run():
    records = []
    assert scalar(comm(X,comm(X,D))) == 1
    assert scalar(comm(D,comm(X,D))) == 0
    for a,b in product(range(3), repeat=2):
        if (a,b) == (0,0):continue
        # Genuine integral determinant-one changes of generators of Gamma.
        p,q,r,s = next((p,q,r,s) for p,q,r,s in product(range(-2,3), repeat=4)
                       if p*s-q*r == 1 and p % 3 == a and q % 3 == b)
        U, V = mul(power(X,p),power(D,r)), mul(power(X,q),power(D,s))
        cert = certificate(U,V)
        assert cert['torsion_cycle_pairing_exponents_mod3'] == (a,b)
        cert['integral_SL2_generator_matrix'] = [[p,q],[r,s]]
        cert['period'] = cert['topological_index'] = cert['minimal_twisted_bundle_rank'] = 3
        records.append(cert)
    out = {'status':'PASS', 'space':'Y7=(S5 x T2)/H27',
           'fundamental_group':'<x,y,c | c^3=1, [x,y]=c, [x,c]=[y,c]=1>',
           'torsion_H3':'(Z/3)^2',
           'nonzero_twists':records, 'zero_twist_index':1,
           'topological_argument':'The commuting tori (x,c),(y,c) generate Tor H2(Y;Z)=(Z3)^2. Scalar lift commutators give their flat-gerbe holonomies. Exponential-sequence Bockstein identifies these torsion pairings with all eight nonzero H3 twists. Each representation constructs a flat PU3 bundle and associated degree3 Azumaya algebra. Period3 divides index, and degree3 existence gives index divides3, hence index3 and a rank3 twisted bundle.',
           'scope':'Exact finite matrix/cocycle verification, analytic topology proof and compensated abstract flat E8 holonomy; no full twisted K groups, native Albert intertwiner, physical compactification, or fermion-family inference.'}
    target = Path(__file__).resolve().parents[1]/'data/toe_20261119_h27_projective_period_index.json'
    target.write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print('PASS eight twists, degree3 flat projective realizations, period=index=3')
    return out


if __name__ == '__main__':
    run()
