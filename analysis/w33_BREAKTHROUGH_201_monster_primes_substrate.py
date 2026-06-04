"""
BT201: All 15 Monster Prime Factors in Substrate

Every prime dividing |Monster| is expressible as a small integer
linear combination of the substrate basis {lambda^mu, q!, q^lambda, q^q}.
"""
import math, itertools, json

q, mu, lam = 3, 4, 2
q_fac = math.factorial(q)

monster_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]
bvals = [lam**mu, q_fac, q**lam, q**q]
bnames = ['lam^mu', 'q!', 'q^lam', 'q^q']

def find_expr(target):
    for r in range(1, 6):
        for idxs in itertools.combinations_with_replacement(range(len(bvals)), r):
            for signs in itertools.product([-1,1], repeat=r):
                val = sum(signs[i]*bvals[idxs[i]] for i in range(r))
                if val == target:
                    terms = {}
                    for i in range(r):
                        key = bnames[idxs[i]]
                        terms[key] = terms.get(key, 0) + signs[i]
                    return {k: v for k, v in terms.items() if v != 0}
    return None

results = {}
for p in monster_primes:
    expr = find_expr(p)
    assert expr is not None, f"No substrate expression for prime {p}"
    # verify
    val = sum(v * eval(k.replace('lam',str(lam)).replace('q!',str(q_fac)).replace('q',str(q)).replace('mu',str(mu)).replace('^','**')) for k,v in expr.items())
    assert val == p
    results[p] = expr

output = {
    "breakthrough": "BT201",
    "title": "All 15 Monster prime factors in substrate basis",
    "date": "2026-06-04",
    "status": "ALL_15_FOUND",
    "substrate": {"q": q, "lam": lam, "mu": mu},
    "basis": {"lam^mu": lam**mu, "q!": q_fac, "q^lam": q**lam, "q^q": q**q},
    "expressions": {str(p): results[p] for p in monster_primes},
}
if __name__ == '__main__':
    print(json.dumps(output, indent=2))
    print(f'BT201: all {len(monster_primes)} Monster prime factors found in substrate')
