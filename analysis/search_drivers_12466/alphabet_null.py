"""12498 (physics idea 1): is the q = 3 alphabet special at matching physical constants, or does a RANDOM alphabet do as well?

w33_alphabet_pool.py computes the look-elsewhere density of the q = 3 alphabet {2,3,4,7,10,12,13,15,18,24,27,30,40} under a fixed
grammar (depth 1: a/b, ab, a+b, |a-b|, 1/a, a^2, sqrt a, e^-a; depth 2: one more composition with an alphabet letter) and concludes
that its high-precision matches are a ~1e-5 - 1e-6 coincidence.  It never runs the control that decides the question: the SAME grammar
and windows applied to random alphabets of 13 distinct integers from [2, 40].  This does.

Targets (PDG 2024 central values; relative windows as in the corpus): m_p/m_e (1e-4), 1/alpha (3e-4), m_H/GeV (8e-4),
sin^2 theta_W(M_Z, MSbar) (2e-3), M_Z/GeV (2e-3).  Scores per alphabet: matches = number of targets hit within their window;
bits = sum_i log2(window_i / max(err_i, window_i * 2^-10)) over hit targets (precision beyond the window, capped at 10 bits each).
usage: py -3 alphabet_null.py [n_random] [seed]"""
import sys, json, math, random, bisect
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), "..", ".."))
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), ".."))
from w33_alphabet_pool import enumerate_depth1, compose_depth2

TARGETS = {"m_p/m_e": (1836.15267343, 1e-4), "1/alpha": (137.035999084, 3e-4), "m_H": (125.20, 8e-4),
           "sin2_thetaW": (0.23122, 2e-3), "M_Z": (91.1876, 2e-3)}
Q3 = [2, 3, 4, 7, 10, 12, 13, 15, 18, 24, 27, 30, 40]


def score(alphabet):
    vals = sorted(compose_depth2(enumerate_depth1(alphabet), alphabet))
    out = {}
    for name, (x, w) in TARGETS.items():
        i = bisect.bisect_left(vals, x)
        best = min((abs(v / x - 1) for v in vals[max(0, i - 2):i + 2]), default=1.0)
        out[name] = best
    matches = sum(1 for n, (x, w) in TARGETS.items() if out[n] <= w)
    bits = sum(math.log2(w / max(out[n], w * 2 ** -10)) for n, (x, w) in TARGETS.items() if out[n] <= w)
    return matches, bits, out


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    m3, b3, e3 = score(Q3)
    print("q=3 alphabet:", m3, "matches", round(b3, 2), "bits", {k: f"{v:.2e}" for k, v in e3.items()}, flush=True)
    rng = random.Random(seed); ms, bs = [], []
    for t in range(n):
        A = sorted(rng.sample(range(2, 41), 13))
        m, b, _ = score(A); ms.append(m); bs.append(b)
        if (t + 1) % 250 == 0: print(t + 1, flush=True)
    p_m = sum(1 for m in ms if m >= m3) / n; p_b = sum(1 for b in bs if b >= b3) / n
    hist = {k: ms.count(k) for k in range(6)}
    out = dict(q3=dict(matches=m3, bits=b3, errors=e3), n_random=n, seed=seed, p_matches=p_m, p_bits=p_b, match_histogram=hist,
               mean_bits=sum(bs) / n)
    print(json.dumps(out, indent=1))
    json.dump(out, open("alphabet_null.json", "w"), indent=1)
