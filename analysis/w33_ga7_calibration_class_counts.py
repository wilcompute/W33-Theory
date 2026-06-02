from itertools import combinations, product
from collections import Counter, defaultdict
import math, json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'data' / 'PART_MMCDII_GA7_CALIBRATION_CLASS_COUNTS_results.json'
PTS = tuple(range(1, 8))
TRIS = list(combinations(PTS, 3))
PRS = set(combinations(PTS, 2))


def primaries():
    p2t = defaultdict(list)
    for t in TRIS:
        for p in combinations(t, 2):
            p2t[tuple(sorted(p))].append(t)
    ans = []
    def bt(chosen, rem):
        if not rem:
            ans.append(tuple(sorted(chosen))); return
        p = min(rem)
        for t in p2t[p]:
            e = set(tuple(sorted(x)) for x in combinations(t, 2))
            if e <= rem:
                bt(chosen + [t], rem - e)
    bt([], set(PRS))
    return sorted(set(ans))


def table(sys, sigs):
    m = {}
    for i in PTS: m[(i, i)] = (-1, 0)
    for t, s in zip(sys, sigs):
        a, b, c = t
        for x, y, z in [(a,b,c),(b,c,a),(c,a,b)]:
            m[(x,y)] = (s, z)
            m[(y,x)] = (-s, z)
    return m


def pmul(x, y, m):
    sx, ix = x; sy, iy = y
    if ix == 0: return (sx*sy, iy)
    if iy == 0: return (sx*sy, ix)
    s, k = m[(ix, iy)]
    return (sx*sy*s, k)


def defect_count(sys, sigs):
    m = table(sys, sigs)
    c = 0
    for a, b, d in TRIS:
        left = pmul(pmul((1,a),(1,b),m), (1,d), m)
        right = pmul((1,a), pmul((1,b),(1,d),m), m)
        c += (left != right)
    return c


def main():
    q, k, v, phi6, f5, chi, g1, dim_g2 = 3, 12, 40, 7, 5, 4, 21, 14
    systems = primaries()
    dist = Counter(); oct_per = []
    for s in systems:
        prof = Counter(defect_count(s, signs) for signs in product([1,-1], repeat=7))
        dist.update(prof); oct_per.append(prof[28])
    expect = Counter({4:192, 8:192, 10:512, 12:928, 14:1408, 16:128, 28:480})
    total = sum(dist.values())
    pseudo = Counter({a:b for a,b in dist.items() if a != 28})
    pseudo_total = sum(pseudo.values())
    wt_total = sum(a*b for a,b in dist.items())
    wt_pseudo = sum(a*b for a,b in pseudo.items())
    checks = {
        'triples_35': len(TRIS) == 35,
        'pairs_21': len(PRS) == 21,
        'primary_count_30': len(systems) == 30,
        'each_primary_has_7_terms': all(len(s) == 7 for s in systems),
        'each_primary_covers_pairs_once': all(Counter(tuple(sorted(p)) for t in s for p in combinations(t,2)) == Counter(PRS) for s in systems),
        'landscape_3840': total == 30*128 == 3840,
        'classes_exact': dist == expect,
        'octonion_count_480': dist[28] == 480,
        'sixteen_octonions_per_primary': Counter(oct_per) == Counter({16:30}),
        'pseudo_count_3360': pseudo_total == 3360,
        'pseudo_weight_8_factorial': wt_pseudo == math.factorial(8) == 40320,
        'total_weight_320_times_168': wt_total == 320*168 == 53760,
        'average_all_14': wt_total == dim_g2 * total,
        'average_pseudo_12': wt_pseudo == k * pseudo_total,
        'rank_law_21_minus_7_equals_14': g1 - phi6 == dim_g2,
        'twenty_eight_is_v_minus_k': 28 == v-k,
        'twenty_eight_is_chi_phi6': 28 == chi*phi6,
        'thirty_five_is_phi6_f5': 35 == phi6*f5,
        'allowed_values': set(dist) == {4,8,10,12,14,16,28}
    }
    assert all(checks.values()), checks
    out = {
        'part':'MMCDII',
        'theorem':'GA7 calibration class count theorem',
        'counts': {'primaries':30, 'signings_per_primary':128, 'total':total},
        'class_distribution': dict(sorted(dist.items())),
        'weighted_laws': {'all':wt_total, 'pseudo':wt_pseudo, 'all_average':14, 'pseudo_average':12},
        'dictionary': {'21-7':'14', '28':'v-k=chi*Phi6', '35':'Phi6*F5', '480':'30*16'},
        'checks': checks, 'n_verified': sum(checks.values()), 'n_checks': len(checks)
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    return out

if __name__ == '__main__':
    r = main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['class_distribution'])
