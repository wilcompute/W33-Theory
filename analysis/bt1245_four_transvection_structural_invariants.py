#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from pathlib import Path

ROWS = [
  {"count":90,"order":24,"diameter":3,"pair_orders":{"24":6},"triple_orders":{"24":4},"isotropic_pairs":0,"span_rank":2,"sample":[0,10,11,12]},
  {"count":40,"order":27,"diameter":2,"pair_orders":{"9":6},"triple_orders":{"27":4},"isotropic_pairs":6,"span_rank":2,"sample":[0,19,20,21]},
  {"count":1440,"order":72,"diameter":4,"pair_orders":{"9":3,"24":3},"triple_orders":{"24":1,"72":3},"isotropic_pairs":3,"span_rank":3,"sample":[0,1,13,19]},
  {"count":1620,"order":576,"diameter":8,"pair_orders":{"9":4,"24":2},"triple_orders":{"72":4},"isotropic_pairs":4,"span_rank":4,"sample":[0,3,21,26]},
  {"count":4320,"order":648,"diameter":6,"pair_orders":{"9":1,"24":5},"triple_orders":{"648":4},"isotropic_pairs":1,"span_rank":3,"sample":[0,9,26,39]},
  {"count":1440,"order":648,"diameter":6,"pair_orders":{"9":3,"24":3},"triple_orders":{"27":1,"648":3},"isotropic_pairs":3,"span_rank":3,"sample":[0,20,21,39]},
  {"count":2880,"order":648,"diameter":6,"pair_orders":{"9":3,"24":3},"triple_orders":{"72":3,"648":1},"isotropic_pairs":3,"span_rank":3,"sample":[0,19,29,38]},
  {"count":2880,"order":648,"diameter":6,"pair_orders":{"24":6},"triple_orders":{"24":1,"648":3},"isotropic_pairs":0,"span_rank":3,"sample":[0,9,23,34]},
  {"count":8640,"order":648,"diameter":7,"pair_orders":{"9":1,"24":5},"triple_orders":{"24":1,"648":3},"isotropic_pairs":1,"span_rank":3,"sample":[0,13,34,36]},
  {"count":2160,"order":648,"diameter":7,"pair_orders":{"9":2,"24":4},"triple_orders":{"648":4},"isotropic_pairs":2,"span_rank":3,"sample":[0,9,19,36]},
  {"count":4320,"order":648,"diameter":7,"pair_orders":{"9":4,"24":2},"triple_orders":{"27":1,"72":2,"648":1},"isotropic_pairs":4,"span_rank":3,"sample":[0,2,3,22]},
  {"count":12960,"order":51840,"diameter":10,"pair_orders":{"9":1,"24":5},"triple_orders":{"648":4},"isotropic_pairs":1,"span_rank":4,"sample":[0,16,29,37]},
  {"count":3240,"order":51840,"diameter":10,"pair_orders":{"9":2,"24":4},"triple_orders":{"648":4},"isotropic_pairs":2,"span_rank":4,"sample":[0,14,28,33]},
  {"count":6480,"order":51840,"diameter":10,"pair_orders":{"24":6},"triple_orders":{"648":4},"isotropic_pairs":0,"span_rank":4,"sample":[0,22,30,35]},
  {"count":25920,"order":51840,"diameter":12,"pair_orders":{"9":2,"24":4},"triple_orders":{"72":1,"648":3},"isotropic_pairs":2,"span_rank":4,"sample":[0,8,11,30]},
  {"count":12960,"order":51840,"diameter":14,"pair_orders":{"9":3,"24":3},"triple_orders":{"72":2,"648":2},"isotropic_pairs":3,"span_rank":4,"sample":[0,1,7,13]},
]


def build():
    full = [r for r in ROWS if r["order"] == 51840]
    by_diam = {}
    for r in full:
        by_diam.setdefault(str(r["diameter"]), []).append(r)
    return {
        "bt": 1245,
        "title": "Four-transvection structural invariant classifier",
        "rows": ROWS,
        "full_order_regime_summary": {
            "diam10": {"count": sum(r["count"] for r in by_diam["10"]), "patterns": len(by_diam["10"])},
            "diam12": {"count": sum(r["count"] for r in by_diam["12"]), "patterns": len(by_diam["12"])},
            "diam14": {"count": sum(r["count"] for r in by_diam["14"]), "patterns": len(by_diam["14"])},
        },
        "diagnostic_rules": [
            "All full-order sets have span rank 4.",
            "Diameter 10 is exactly the full-order regime with all four triples closing to 648.",
            "Diameter 12 has pair orders 9^2 24^4 and triple orders 72^1 648^3.",
            "Diameter 14 has pair orders 9^3 24^3 and triple orders 72^2 648^2; this is the BT1228/BT1233 word-metric regime."
        ],
        "interpretation": "The full-order diameter split is explained by local pair/triple closure structure: the diameter-14 regime is not just full rank and full order, but the balanced 3/3 pair split together with two weak 72 triples and two strong 648 triples."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1245_four_transvection_structural_invariants_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt":1245, "full_order_regime_summary":result["full_order_regime_summary"], "out":str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
