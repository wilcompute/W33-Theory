"""12498: the fair null for w33_mdl_shortest.py (its own functions, unchanged).
That tool matches the 10 substrate observables at a loose 1.5% tolerance but the random targets of its null at their tight achieved
precisions delta -- unequal tests.  Here (A) both sides use the SAME rule (each target at the same tolerance), and (B) the statistic --
the fraction of the 10 observables reachable at cost <= 2 -- is recomputed for random alphabets (13 distinct integers in [2,40], plus
the leaf 1 as in the tool) to see whether the q = 3 alphabet is special.  usage: py -3 mdl_fair_null.py [n_alphabets]"""
import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from w33_mdl_shortest import build_expressions, min_cost_match

OBS = [("sin^2 th_W", 0.23122, 2.0e-3), ("sin^2 th_12", 0.307, 4.2e-2), ("sin^2 th_13", 0.02238, 2.9e-2), ("sin^2 th_23", 0.550, 2.1e-2),
       ("M_Z", 91.19, 2.1e-3), ("CC exponent", 120.0, 8.0e-4), ("Dm31/Dm21", 32.6, 1.2e-2), ("alpha_s", 0.1180, 3.4e-3),
       ("m_Higgs", 125.1, 8.0e-4), ("Omega_DM/Omega_b", 5.38, 1.6e-2)]
Q3 = [1, 2, 3, 4, 7, 10, 12, 13, 15, 18, 24, 27, 30, 40]


def frac_short(alphabet, rule):
    val = build_expressions(alphabet, max_cost=2)
    hits = 0
    for name, x, d in OBS:
        m = min_cost_match(val, x, tol=(0.015 if rule == "loose" else d))
        hits += bool(m and m[0] <= 2)
    return hits / len(OBS)


def random_targets(alphabet, rule, n=400, seed=7):
    val = build_expressions(alphabet, max_cost=2); rng = random.Random(seed); deltas = [d for _, _, d in OBS]; hit = 0
    for _ in range(n):
        x = 10 ** rng.uniform(-2, 2.5); d = rng.choice(deltas)
        m = min_cost_match(val, x, tol=(0.015 if rule == "loose" else d)); hit += bool(m and m[0] <= 2)
    return hit / n


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    out = {}
    for rule in ("loose", "tight"):
        out[rule] = dict(substrate_frac_cost_le2=frac_short(Q3, rule), random_targets_frac_cost_le2=random_targets(Q3, rule))
    out["tool_as_written"] = dict(substrate=out["loose"]["substrate_frac_cost_le2"], random=out["tight"]["random_targets_frac_cost_le2"])
    print(json.dumps(out, indent=1), flush=True)
    rng = random.Random(11); fr = {"loose": [], "tight": []}
    for t in range(n):
        A = [1] + sorted(rng.sample(range(2, 41), 13))
        for rule in fr: fr[rule].append(frac_short(A, rule))
    for rule in fr:
        q3 = out[rule]["substrate_frac_cost_le2"]
        out[rule]["random_alphabets_mean"] = sum(fr[rule]) / n
        out[rule]["p_random_alphabet_ge_q3"] = sum(1 for f in fr[rule] if f >= q3) / n
    out["n_alphabets"] = n
    print(json.dumps({k: out[k] for k in ("loose", "tight")}, indent=1))
    json.dump(out, open("mdl_fair_null.json", "w"), indent=1)
