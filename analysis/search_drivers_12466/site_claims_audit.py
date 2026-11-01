"""12512: run the fair null of scripts/check_constant_claim.py over every "<prediction> (obs: X +- s ..." row of docs/index.html.
For each row: tension = |pred - X| / s and p_random = fraction of random 13-integer alphabets (+ leaf 1) reaching X within
max(|pred/X - 1|, s/X) at expression cost <= 2 and <= 3.  usage: py -3 site_claims_audit.py"""
import re, html, json, sys, os, random, bisect
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from w33_mdl_shortest import build_expressions
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
t = html.unescape(re.sub(r"<[^>]+>", " ", open(os.path.join(ROOT, "docs", "index.html"), encoding="utf-8", errors="ignore").read()))
t = re.sub(r"\s+", " ", t)
rows = []
for m in re.finditer(r"([0-9]+\.?[0-9]*)\s*\(obs:?\s*([0-9]+\.?[0-9]*)\s*±\s*([0-9]+\.?[0-9]*)", t):
    name = t[max(0, m.start() - 70):m.start()].strip()
    pred, obs, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
    if s <= 0 or obs <= 0: continue
    rows.append(dict(name=name[-50:], predicted=pred, measured=obs, sigma=s))
seen, uniq = set(), []
for r in rows:
    k = (r["name"], r["predicted"], r["measured"])
    if k not in seen: seen.add(k); uniq.append(r)
rng = random.Random(1); alph = [[1] + sorted(rng.sample(range(2, 41), 13)) for _ in range(200)]
cache = {c: [sorted(build_expressions(A, max_cost=c).keys()) for A in alph] for c in (2, 3)}
def reach(vals, x, w):
    i = bisect.bisect_left(vals, x * (1 - w)); return i < len(vals) and vals[i] <= x * (1 + w)
for r in uniq:
    x, w = r["measured"], max(abs(r["predicted"] / r["measured"] - 1), r["sigma"] / r["measured"])
    r["tension_sigma"] = round(abs(r["predicted"] - x) / r["sigma"], 2)
    for c in (2, 3):
        r[f"p_random_cost{c}"] = round(sum(reach(v, x, w) for v in cache[c]) / len(alph), 3)
    # judged at cost <= 3: the site's formulas use 2-3 integer leaves (e.g. lambda/(Phi3 Phi6) is cost 3)
    r["verdict"] = ("EXCLUDED" if r["tension_sigma"] > 3 else "not evidence" if r["p_random_cost3"] > 0.05 else "rare at cost 3")
    print(f"{r['name'][:40]:40s} pred {r['predicted']:<10g} obs {x:<10g}+-{r['sigma']:<8g} {r['tension_sigma']:>7}s "
          f"p2={r['p_random_cost2']:<5} p3={r['p_random_cost3']:<5} {r['verdict']}")
summ = {v: sum(1 for r in uniq if r["verdict"] == v) for v in ("EXCLUDED", "not evidence", "rare at cost 3")}
print("rows:", len(uniq), summ)
json.dump(dict(rows=uniq, summary=summ), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "site_claims_audit.json"), "w"), indent=1)
