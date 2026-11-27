"""Local square-grid controls with a fixed number of failed plaquettes."""
import json
from math import isqrt

import numpy as np


STEPS = ((1,0),(-1,0),(0,1),(0,-1))


def generators(b):
    n = len(b)
    a = (np.arange(n)+1)%n
    return a, np.argsort(a), b, np.argsort(b)


def signed_defects(moves):
    return set(np.flatnonzero(np.logical_or.reduce(
        [moves[i][moves[j]] != moves[j][moves[i]] for i in (0,1) for j in (2,3)])))


def good_ball(root, radius, moves):
    """Check the induced, edge-colored ball against the square grid."""
    chart = {(0,0):root}
    inverse = {root:(0,0)}
    layer = [(0,0)]
    for _ in range(radius):
        next_layer = []
        for x,y in layer:
            v = chart[x,y]
            for move,(dx,dy) in zip(moves,STEPS):
                target = (x+dx,y+dy)
                w = int(move[v])
                if target in chart:
                    if chart[target] != w:
                        return False
                else:
                    if w in inverse:
                        return False
                    chart[target] = w
                    inverse[w] = target
                    next_layer.append(target)
        layer = next_layer
    for (x,y),v in chart.items():
        for move,(dx,dy) in zip(moves,STEPS):
            if inverse.get(int(move[v])) != ((x+dx,y+dy) if (x+dx,y+dy) in chart else None):
                return False
    return len(chart) == 1+2*radius*(radius+1)


def unsafe_region(defects, radius, moves):
    ball, frontier = set(defects), set(defects)
    for _ in range(radius):
        frontier = {int(move[v]) for v in frontier for move in moves} - ball
        ball.update(frontier)
    return ball


def base_permutation(n, k):
    # Reverse the cyclic order of k unequal runs, preserving internal order.
    ends = [i*i*n//(k*k) for i in range(k+1)]
    return np.concatenate([np.arange(ends[j],ends[j+1]) for j in reversed(range(k))])


def build():
    rows = []
    rng = np.random.default_rng(1647)
    for n in (257,4093,65537):
        for k in (3,5):
            base = base_permutation(n,k)
            radius = 3 if n == 257 else 6
            successes = 0
            max_unsafe = 0
            cases = 96
            for shift,root in rng.integers(n,size=(cases,2)):
                b = (base+shift)%n
                moves = generators(b)
                assert np.count_nonzero(moves[0][b] != b[moves[0]]) == k
                defects = signed_defects(moves)
                assert len(defects)<=4*k
                capped_radius = 2*radius+1
                unsafe = unsafe_region(defects,capped_radius,moves)
                assert len(unsafe)<=len(defects)*(1+2*capped_radius*(capped_radius+1))
                max_unsafe = max(max_unsafe,len(unsafe))
                successes += good_ball(int(root),radius,moves)
            rows.append({"n":n,"defects":k,"tested_radius":radius,"shift_root_cases":cases,
                         "grid_balls":successes,"max_defect_neighborhood_size":max_unsafe})
    # For the zero-defect rotation by floor(sqrt(n)), a short ball is visibly
    # a square-grid ball. Rotation by one collapses the two directions.
    n = 4093
    assert good_ball(0,8,generators((np.arange(n)+isqrt(n))%n))
    assert not good_ball(0,1,generators((np.arange(n)+1)%n))
    return {"status":"PASS","seeded_controls":rows,
            "uniform_shift_bad_ball_bound":"O_k((r+1)^(max(2,k+1))/n), for 2r+1<n"}


if __name__ == "__main__":
    print(json.dumps(build(),indent=2))
