"""Prime-size orbit crossover and local geometry for flat commuting tuples."""
from collections import Counter
from itertools import product, permutations
import json
from math import factorial, prod

import numpy as np
from scipy.special import ive, zeta
from sympy import primerange


def subgroup_counts(n, rank):
    counts = np.ones(n+1,dtype=np.int64)
    for r in range(2,rank+1):
        new = np.zeros_like(counts)
        for d in range(1,n+1):
            new[d::d] += d**(r-1)*counts[1:n//d+1]
        counts = new
    return counts


def partition_coefficient(n, q, counts):
    weights = np.zeros(n+1)
    weights[0] = 1.
    for m in range(1,n+1):
        weights[m] = q/m * (counts[1:m+1] @ weights[m-1::-1])
    return weights[n]


def exact_orbit_count(n,rank,subgroups):
    ps = list(permutations(range(n)))
    compatible = [{b for b in ps if all(a[b[i]]==b[a[i]] for i in range(n))}
                  for a in ps]
    i_of = {a:i for i,a in enumerate(ps)}
    histogram = Counter()

    def walk(generators,candidates):
        if len(generators)==rank:
            unseen = set(range(n))
            orbits = 0
            while unseen:
                orbits += 1
                todo = [unseen.pop()]
                while todo:
                    v = todo.pop()
                    for a in generators:
                        if a[v] in unseen:
                            unseen.remove(a[v])
                            todo.append(a[v])
            histogram[orbits] += 1
            return
        for a in candidates:
            walk(generators+[a],candidates&compatible[i_of[a]])

    walk([],set(ps))
    assert histogram[1] == factorial(n-1)*subgroups[n]
    for q in (.25,1.):
        exact = sum(count*q**k for k,count in histogram.items())/factorial(n)
        assert abs(exact-partition_coefficient(n,q,subgroups))<1e-10
    return {str(k):count for k,count in sorted(histogram.items())}


def prime_limit(c,rank):
    bulk = prod(zeta(j) for j in range(2,rank+1))
    factors = [1-prod(1-p**(-j) for j in range(2,rank+1))
               for p in map(float,primerange(2,3000))]
    terms = [1.]
    for k in range(2,24):
        primitive = bulk**k * prod(1-f**k for f in factors)
        simplex = factorial(rank-2)**k/factorial(k*(rank-1)-1)
        terms.append(c**(k-1)*primitive*simplex/factorial(k))
    return 1/sum(terms)


def local_geometry(n,rank,radius):
    vectors = np.array([v for v in product(range(-radius,radius+1),repeat=rank)
                        if 0 < sum(map(abs,v)) <= radius],dtype=np.int64)
    rng = np.random.default_rng(1918+rank)
    normals = rng.integers(n,size=(rank,128))
    assert np.all(np.any(normals,axis=0))
    without_relation = np.all((vectors@normals)%n != 0,axis=0)
    return {"prime_size":n,"relation_radius":radius,"checked":len(without_relation),
            "without_relation":int(without_relation.sum()),
            "fraction_short_relation_union_bound":len(vectors)/n}


def heat_controls(rank):
    prime = 5
    characters = np.arange(prime)
    normal_vectors = [np.array((0,)*j+(1,)+tail) for j in range(rank)
                      for tail in product(range(prime),repeat=rank-j-1)]
    hann = (prime**(rank-1)-1)/(prime**rank-1)
    rows = []
    for t in (.3,1.7,8.):
        spectrum = lambda v: (2-2*np.cos(2*np.pi*np.outer(characters,v)/prime)).sum(axis=1)
        ensemble = np.mean([np.mean(np.exp(-t*spectrum(v))) for v in normal_vectors])
        mod_grid = np.mean(np.exp(-t*spectrum([1])))**rank
        prediction = mod_grid + hann*(1-mod_grid)
        assert abs(ensemble-prediction)<1e-13
        rows.append({"time":t,"enumerated_return":float(ensemble),"predicted_return":float(prediction)})
    # Finite-size crossover time on bigger prime quotients. No sampling needed.
    for p in (509,4093,65537):
        alpha = .5
        t = alpha*p**(2/rank)
        one_axis_mod = np.mean(np.exp(-t*(2-2*np.cos(2*np.pi*np.arange(p)/p))))
        mod_grid = one_axis_mod**rank
        fraction = (p**(rank-1)-1)/(p**rank-1)
        prediction = mod_grid+fraction*(1-mod_grid)
        rows.append({"prime":p,"alpha":alpha,"scaled_mean_return":float(p*prediction),
                     "scaled_infinite_grid_return":float(p*ive(0,2*t)**rank),
                     "continuum_scaled_limit":1+(4*np.pi*alpha)**(-rank/2)})
    return rows


def build():
    rows = []
    for rank in (2,3,4):
        subgroups = subgroup_counts(4093,rank)
        exact = exact_orbit_count(4,rank,subgroups)
        for p in (31,127,509,4093):
            assert subgroups[p] == sum(p**i for i in range(rank))
        probs = []
        for c in (.25,1.,4.):
            limit = prime_limit(c,rank)
            finite = []
            for n in (31,127,509,4093):
                q = c/n**(rank-1)
                probability = q*subgroups[n]/(n*partition_coefficient(n,q,subgroups))
                finite.append({"n":n,"probability":float(probability)})
            assert abs(finite[-1]["probability"]-limit)<.002
            probs.append({"c":c,"prime_limit":limit,"finite":finite})
        rows.append({"rank":rank,"exact_four_site_commuting_orbit_census":exact,
                     "component_crossover":probs,"prime_geometry":local_geometry(65537,rank,8),
                     "heat_controls":heat_controls(rank)})
    return {"status":"PASS","rows":rows,"component_weight_scale":"c/n^(rank-1)",
            "scope":"Pairwise commuting permutations already imposed. Geometry conditional on one orbit."}


if __name__ == "__main__":
    print(json.dumps(build(),indent=2))
