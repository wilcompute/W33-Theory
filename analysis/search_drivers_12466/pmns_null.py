"""12504: the PMNS triple, tested fairly.  The site claims sin^2 th12 = (q+1)/Phi3 = 4/13, sin^2 th13 = lambda/(Phi3 Phi6) = 2/91,
sin^2 th23 = Phi6/Phi3 = 7/13, "all within 0.5 sigma".  For the q = 3 alphabet and for random alphabets (13 distinct integers from
[2,40] plus the leaf 1, as in w33_mdl_shortest.py), count how many of the three angles are hit within 1 sigma by an expression of
cost <= 3 (w33_mdl_shortest.build_expressions), and the probability that a random alphabet hits all three.
Data: NuFIT 6.0 (2024), normal ordering, with SK atmospheric data: s12^2 = 0.307 +- 0.012, s13^2 = 0.02195 +- 0.00056,
s23^2 = 0.561 +- 0.014 (and the site's own value 0.546 +- 0.021 as a second reading).  usage: py -3 pmns_null.py [n]"""
import sys, os, json, random, bisect
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from w33_mdl_shortest import build_expressions

Q3 = [1, 2, 3, 4, 7, 10, 12, 13, 15, 18, 24, 27, 30, 40]
READINGS = {"nufit6_SK": [("s12", 0.307, 0.012), ("s13", 0.02195, 0.00056), ("s23", 0.561, 0.014)],
            "site_values": [("s12", 0.307, 0.013), ("s13", 0.02203, 0.00056), ("s23", 0.546, 0.021)]}


def hits(alphabet, targets, cost=3):
    vals = sorted(build_expressions(alphabet, max_cost=cost).keys())
    h = []
    for name, x, s in targets:
        i = bisect.bisect_left(vals, x - s)
        h.append(i < len(vals) and vals[i] <= x + s)
    return h


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    out = {}
    rng = random.Random(3)
    alphs = [[1] + sorted(rng.sample(range(2, 41), 13)) for _ in range(n)]
    for cost in (2, 3):
        for rd, T in READINGS.items():
            h3 = hits(Q3, T, cost)
            rand = [hits(A, T, cost) for A in alphs]
            q3n = sum(h3)
            p_ge = sum(1 for h in rand if sum(h) >= q3n) / n
            per = [sum(1 for h in rand if h[i]) / n for i in range(3)]
            key = f"cost{cost}_{rd}"
            out[key] = dict(q3_hits=h3, p_random_at_least_as_many=p_ge, random_per_angle=per, n=n)
            print(key, json.dumps(out[key]), flush=True)
    json.dump(out, open("pmns_null.json", "w"), indent=1)
