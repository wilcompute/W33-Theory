"""12498 (physics idea 1): the information content of the corpus's headline constant matches.

For each claimed prediction (value from the corpus, PDG/CODATA measurement with its uncertainty):
  tension     = |pred - meas| / sigma                         (is it a match at all?)
  bits_claim  = log2(1 / (2 delta)),  delta = |pred/meas - 1|  (what a "match at delta" would be worth if it were a free guess)
  baseline    = probability that a number drawn log-uniformly from [meas/1.2, meas*1.2] lies at least as close (in relative terms) to
                SOME integer (masses) or SOME fraction a/b with b <= the claim's denominator (couplings) -- the price of "it is near a
                simple number", independent of any theory
  bits_net    = log2(1 / baseline): the evidence the coincidence carries beyond "constants are near simple numbers"
Plus the random-alphabet control of alphabet_null.py (the corpus grammar).  usage: py -3 constants_information_audit.py"""
import json, math, random
from fractions import Fraction

CLAIMS = [  # name, prediction (corpus), measured, sigma, kind, max denominator
    ("m_p/m_e", 1836, 1836.15267343, 1.1e-7, "integer", 1),
    ("1/alpha", 137, 137.035999084, 2.1e-8, "integer", 1),
    ("M_Z [GeV]", 91, 91.1876, 0.0021, "integer", 1),
    ("m_H [GeV]", 125, 125.20, 0.11, "integer", 1),
    ("sin^2 theta_W (MSbar, M_Z)", Fraction(3, 13), 0.23122, 0.00004, "fraction", 13),
    ("alpha_s(M_Z)", Fraction(9, 76), 0.1180, 0.0009, "fraction", 76),
]


def nearest_rel(x, maxden):
    if maxden == 1:
        return abs(round(x) - x) / x
    f = Fraction(x).limit_denominator(maxden)
    best = abs(float(f) - x)
    # limit_denominator returns the closest fraction with denominator <= maxden
    return best / x


def baseline(meas, delta, maxden, n=200000, seed=1):
    rng = random.Random(seed); hit = 0
    lo, hi = math.log(meas / 1.2), math.log(meas * 1.2)
    for _ in range(n):
        x = math.exp(rng.uniform(lo, hi))
        if nearest_rel(x, maxden) <= delta: hit += 1
    return hit / n


def main():
    rows = []
    for name, pred, meas, sig, kind, D in CLAIMS:
        p = float(pred); delta = abs(p / meas - 1)
        b = baseline(meas, delta, D)
        rows.append(dict(name=name, prediction=str(pred), measured=meas, sigma=sig, tension_sigma=round(abs(p - meas) / sig, 2),
                         delta=delta, bits_claim=round(math.log2(1 / (2 * delta)), 2), baseline=b,
                         bits_net=round(math.log2(1 / b), 2) if b > 0 else None))
    for r in rows:
        print(f"{r['name']:28s} pred {r['prediction']:>6s}  tension {r['tension_sigma']:>14,.1f} sigma  delta {r['delta']:.2e}  "
              f"claim {r['bits_claim']:5.2f} bits  baseline {r['baseline']:.3f}  net {r['bits_net']} bits")
    tot = sum(r["bits_net"] for r in rows if r["bits_net"] is not None)
    within = [r["name"] for r in rows if r["tension_sigma"] <= 3]
    out = dict(rows=rows, total_net_bits=round(tot, 2), consistent_within_3sigma=within)
    try:
        out["random_alphabet_control"] = json.load(open("alphabet_null.json"))
    except OSError:
        pass
    print("total net bits beyond 'near a simple number':", round(tot, 2), "| consistent within 3 sigma:", within)
    json.dump(out, open("constants_information_audit.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
