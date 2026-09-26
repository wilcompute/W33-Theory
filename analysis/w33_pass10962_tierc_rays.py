#!/usr/bin/env python3
"""Pass 10962 Tier C reproducer: exact extreme-ray closure of Z6II_23..2913 over invariant generators.

Runs cdd (GMP) on the D-flat cone of the ever-even hidden-invariant generator types and tests
every FI-cancelling ray for parity realizability over the full B-L freedom (Smith normal
form).  ~15 minutes.  Writes data/w33_pass10962_tierc_rays.json.
"""
import gzip
import importlib.util
import json
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p10962", ROOT / "analysis" / "w33_pass10962_hidden_sector_dflat_tiers.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
P = M.P
NAME = "Z6-II|Z6II_23__SM_20260917_2913"


def main():
    ledger, _ = P.load_ledger()
    gauge = json.loads(gzip.decompress(M.GAUGE.read_bytes()))
    c60 = json.loads(M.CERT10960.read_text())["models"]
    groups = gauge[NAME]
    fl, hidden, x0, N = M.model_data(NAME, ledger[NAME], groups)
    s = 1 if Fraction(c60[NAME]["trace_anomalous"]) > 0 else -1
    _, (T, types, C, Mm, alpha, beta, U) = M.tier_b(fl, groups, x0, N, s)
    t0 = time.time()
    rays = P.cone_rays([Mm[i] for i in U])
    neg = [r for r in rays if sum((C[U[i]] * r[i] for i in range(len(U))), Fraction(0)) < 0]
    hits, kinds = 0, set()
    for r in neg:
        S_ = [U[i] for i in range(len(U)) if r[i] != 0]
        ok, why = P.realizable([alpha[i] for i in S_], [beta[i] for i in S_])
        hits += ok
        if not ok:
            kinds.add(why["kind"])
    rec = {NAME: dict(exact=True, generator_types=len(T), ever_even_generator_types=len(U), extreme_rays=len(rays),
                      fi_cancelling_rays=len(neg), realizable=hits, obstruction_kinds=sorted(kinds),
                      seconds=round(time.time() - t0, 1),
                      method="cdd (GMP) extreme rays + Smith normal form realizability")}
    print(json.dumps(rec, indent=1))
    (ROOT / "data" / "w33_pass10962_tierc_rays.json").write_text(json.dumps(rec, indent=1) + "\n")


if __name__ == "__main__":
    main()
