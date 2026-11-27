"""Exact square gluing defect census and critical-window numerical controls."""
from collections import Counter
from itertools import permutations
import json
from math import comb, exp, factorial, log, log1p

import numpy as np
from scipy.special import logsumexp


def block_orders(k):
    """Oriented cyclic orders on k runs with no original successor retained."""
    return sum((-1)**j*comb(k,j)*factorial(k-j-1) for j in range(k)) + (-1)**k


def defect_census(n):
    counts = Counter(sum(b[(i+1)%n] != (b[i]+1)%n for i in range(n))
                     for b in permutations(range(n)))
    assert counts[0] == n
    for k in range(1,n+1):
        assert counts[k] == n*comb(n,k)*block_orders(k)
    assert sum(counts.values()) == factorial(n)
    return {str(k): counts[k] for k in sorted(counts)}


def flat_stats(n, offset):
    """Beta = log(n)+offset, evaluated stably from the positive count terms."""
    log_falling_ratio = 0.
    terms = [0.]
    defects = [0]
    for k in range(1,n+1):
        log_falling_ratio += log1p(-(k-1)/n)
        if k < 3:
            continue
        correction = sum((-1)**j/(factorial(j)*(k-j)) for j in range(min(k,32)))
        if k < 32:
            correction += (-1)**k/factorial(k)
        terms.append(log_falling_ratio + log(correction)-k*offset)
        defects.append(k)
    log_norm = float(logsumexp(terms))
    mean_fraction = float(np.exp(np.asarray(terms)-log_norm) @ np.asarray(defects)/n)
    return {"probability":exp(-log_norm),"mean_defect_fraction":mean_fraction,
            "negative_log_flat_probability_per_site":log_norm/n}


def flat_slope_geometry(n):
    slopes = np.arange(n, dtype=np.int64)
    shortest = np.full(n,n,dtype=np.int64)
    # A kernel relation is x+ky=0 mod n. Minimize |x|+|y|.
    for y in range(1,ceil_search(n)):
        residue = (slopes*y)%n
        shortest = np.minimum(shortest,y+np.minimum(residue,n-residue))
    assert np.max(shortest) < ceil_search(n)
    r = int(n**.3)
    short = int(np.count_nonzero(shortest <= r))
    assert short/n <= min(1.,6*r*r/n)
    selected = int(np.argmax(shortest))
    momentum = 2*np.pi*slopes/n
    spectrum = 4-2*np.cos(momentum)-2*np.cos(selected*momentum)
    return {"n":n,"test_relation_radius":r,"fraction_short_relations":short/n,
            "max_shortest_relation":int(shortest[selected]),"example_slope":selected,
            "example_gap":float(np.min(spectrum[1:]))}


def ceil_search(n):
    # Pigeonhole applied to a square of residues gives a relation <= 2 ceil(sqrt(n)).
    return 2*int(np.ceil(np.sqrt(n)))+2


def build():
    censuses = {str(n):defect_census(n) for n in range(3,9)}
    rows = []
    for c in (-.5,0.,.1,.5,1.):
        x = exp(-c)
        limit = exp(x)/(1-log1p(-x)) if c>0 else 0.
        ps = [{"n":n,**flat_stats(n,c)} for n in (8,64,512,4096,32768)]
        if c>0:
            assert abs(ps[-1]["probability"]-limit)<.002
        density_limit = 1-exp(c) if c<0 else 0.
        rate_limit = exp(c)-1-c if c<0 else 0.
        assert abs(ps[-1]["mean_defect_fraction"]-density_limit)<.002
        assert abs(ps[-1]["negative_log_flat_probability_per_site"]-rate_limit)<.002
        rows.append({"offset":c,"limit":limit,"defect_density_limit":density_limit,
                     "flat_probability_decay_rate_per_site":rate_limit,"finite_size":ps})
    for c in (-.5,0.,.5):
        counts = censuses["8"]
        direct = 8/sum(v*exp(-int(k)*(log(8)+c)) for k,v in counts.items())
        assert abs(direct-flat_stats(8,c)["probability"]) < 1e-13
    return {"status":"PASS","small_exact_defect_censuses":censuses,
            "critical_window":rows,"flat_geometry":[flat_slope_geometry(n) for n in (257,4093,65537)]}


if __name__ == "__main__":
    print(json.dumps(build(),indent=2))
