"""Connected torus-cover census and prime-size component crossover."""
from collections import Counter
from itertools import permutations
import json
from math import factorial

import numpy as np
from scipy.special import zeta


def orbit_count(a,b):
    unseen = set(range(len(a)))
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            v = stack.pop()
            for w in (a[v],b[v]):
                if w in unseen:
                    unseen.remove(w)
                    stack.append(w)
    return count


def divisor_sums(n):
    sigma = np.zeros(n+1,dtype=np.int64)
    for d in range(1,n+1):
        sigma[d::d] += d
    return sigma


def flat_weight(n, weight, sigma):
    values = np.zeros(n+1)
    values[0] = 1.
    for m in range(1,n+1):
        values[m] = (weight/m)*(sigma[1:m+1] @ values[m-1::-1])
    return values[n]


def exact_small(n,sigma):
    perms = list(permutations(range(n)))
    counts = Counter(orbit_count(a,b) for a in perms for b in perms
                     if all(a[b[i]] == b[a[i]] for i in range(n)))
    assert counts[1] == factorial(n-1)*sigma[n]
    for q in (.125,1.,2.):
        exact = sum(number*q**k for k,number in counts.items())/factorial(n)
        assert abs(exact-flat_weight(n,q,sigma)) < 1e-10
    return {str(k):counts[k] for k in sorted(counts)}


def prime_window(c):
    odds = 1+sum(c**(k-1)*zeta(2)**k/(factorial(k)*factorial(k-1)*zeta(2*k))
                 for k in range(2,45))
    return float(1/odds)


def build():
    sigma = divisor_sums(4095)
    small = {str(n):exact_small(n,sigma) for n in range(2,6)}
    rows = []
    for c in (.25,1.,4.):
        limit = prime_window(c)
        finite = []
        for n in (31,127,509,4093):
            q = c/n
            a = sigma[n]/n
            value = q*a/flat_weight(n,q,sigma)
            finite.append({"n":n,"probability":float(value)})
        assert abs(finite[-1]["probability"]-limit)<.002
        rows.append({"c":c,"prime_limit":limit,"finite":finite})
    arithmetic = []
    for n in (4093,4094,4095,4092):
        coefficient = sigma[n]/n
        q = 1/n
        arithmetic.append({"n":n,"divisor_factor":float(coefficient),
                           "connected_probability":float(q*coefficient/flat_weight(n,q,sigma))})
    geometry = []
    for n in (31,127,509,4093):
        radius = int(n**.3)
        bad_kernels = set()
        for x in range(-radius,radius+1):
            for y in range(-(radius-abs(x)),radius-abs(x)+1):
                if y:
                    bad_kernels.add((-x*pow(y,-1,n))%n)
                elif x:
                    bad_kernels.add(n)
        bound = 2*radius*(radius+1)/(n+1)
        assert len(bad_kernels)/(n+1) <= bound
        geometry.append({"prime_size":n,"relation_radius":radius,
                         "fraction_short_relation":len(bad_kernels)/(n+1),"union_bound":bound})
    return {"status":"PASS","exact_commuting_orbit_censuses":small,"prime_window":rows,
            "nearby_composite_controls":arithmetic,"prime_geometry_controls":geometry,
            "scope":"Both permutations free. Prime window conditions on exact zero commutator; weight is per joint orbit."}


if __name__ == "__main__":
    print(json.dumps(build(),indent=2))
