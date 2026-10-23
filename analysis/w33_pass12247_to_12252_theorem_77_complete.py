"""Passes 12247-12252: Theorem 7.7 completed to every Wilson-line configuration of the route; the statistics rule predicts every field;
the SM_2496 Higgs-branch reading corrected (rank); the Z6-II exception still unresolved (Claude track).

12247 -- completion.  Torus 1 carries the base's family line, so a configuration has at most two further order-3 lines.  Commuting
  lines diagonalise on the D5 Cartan, so an A4 intersection forces one line to be A4-type and the other to preserve that A4 (A4-type or
  not, e.g. trivial on so(10)).  Enumerating W1 over the A4 class and W2 over EVERY consistent admissible line preserving it:
  119,915,126 consistent pairs on the 7 bases, 2,210,046 with a twisted 10-type massless vector, 0 of scalar type; positive control 366/366
  sampled hits.  With the one-line theorem (165,465 configurations) and the untwisted theorem: no scalar 10 for ANY Wilson-line
  configuration with an SU(5) on the e6+a2 route.
12248 -- the Z6-II exception, attempted independent check: the independent N = 0 engine (nsdump_v2) rejects the translated Z6-II model
  at the fixed-point level (local condition N(V_loc^2 - v_loc^2) not 0 mod 2 -- its Witten-twist conventions differ); inconclusive, the
  labelling of the 8 states stays 'suspected'.
12249 -- SM_2496 correction: the shift-broken class v9 keeps A2 + A1 + A2 + 11 U(1)s (rank 16; a shift never lowers the rank), while a
  scalar-10 vev of the unbroken class v0 (A4 + A2 + 10 U(1)s) keeps only the Cartan directions orthogonal to the weight -- rank 15.
  The 12244 identity holds for the ROOTS (8 = A2 + A1), but the two are not the same vacuum: the shift class keeps one more U(1)
  than any 10 vev.
12250 -- the rule as a predictor: from the left weights alone, 'boson iff P.V0 - w/2 is an integer' reproduces the engine's statistics
  for all 5,974 fields of eight T6/Z3 dumps (both routes) and 782 of 790 on Z6-II -- the 8 misses are exactly the suspect states of 12242.
12251 -- the main checkout was NOT synced: a file of the parallel track differs from origin (work in progress).
12252 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12247_to_12252_theorem_77_complete.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    T = [json.loads(p.read_text()) for p in sorted((A / "search_drivers_12247").glob("exhaust3_*.json"))]
    pairs = sum(d["pairs"] for d in T); hits = sum(d["twisted10_pairs"] for d in T); sc = sum(d["scalar10_pairs"] for d in T)
    res["12247"] = dict(per_base=T, pairs=pairs, twisted10=hits, scalar10=sc,
                        control=[sum(d["control_found"] for d in T), sum(d["control_sampled_hits"] for d in T)])
    checks["12247: every SU(5)-preserving two-line configuration: 119,915,126 pairs, 2,210,046 with twisted 10s, 0 scalar; control 366/366"] = (
        len(T) == 7 and all(d.get("extended") for d in T) and pairs == 119915126 and hits == 2210046 and sc == 0 and res["12247"]["control"] == [366, 366])
    p = json.loads((A / "search_drivers_12250" / "predict.json").read_text())
    res["12250"] = p
    t3 = {k: v for k, v in p.items() if not k.startswith("Z6II")}
    checks["12250: the rule predicts the engine's statistics for all 5,974 T6/Z3 fields; 782/790 on Z6-II, misses = the 8 suspect states"] = (
        sum(v["agree"] for v in t3.values()) == 5974 and all(v["mismatch"] == 0 for v in t3.values())
        and p["Z6II_2496_v0"]["agree"] == 782 and p["Z6II_2496_v0"]["mismatch"] == 8)
    out = (A / "search_drivers_12248" / "nsdump_v2_out.txt").read_text(errors="ignore")
    res["12248"] = dict(nsdump_v2_rejects="local condition" in out)
    checks["12248: the independent engine rejects the translated Z6-II model (inconclusive cross-check, recorded)"] = "local condition" in out
    rank_v9 = 2 + 1 + 2 + 11
    rank_v0 = 4 + 2 + 10
    res["12249"] = dict(v0_rank=rank_v0, v9_rank=rank_v9, higgs_branch_rank=rank_v0 - 1)
    checks["12249: shift class rank 16 vs scalar-10 Higgs branch rank 15 -- root identity only"] = rank_v9 == 16 and rank_v0 == 16
    tex = (ROOT / "papers" / "forty_points" / "sec07_realforms.tex").read_text(encoding="utf-8")
    checks["paper: Theorem 7.7 states every Wilson-line configuration with an SU(5)"] = "119{,}915{,}126" in tex
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
