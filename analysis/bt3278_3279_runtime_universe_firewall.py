#!/usr/bin/env python3
"""Passes 3278-3279: typed runtime universes and fail-closed projections.

The four-opcode operational baselines, the 194-member five/six-opcode census,
and future >=7-opcode families are distinct universes.  Records may be compared
on shared metrics, but may never increment another universe's completeness.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "PART_BT3278_BT3279_RUNTIME_UNIVERSE_FIREWALL_results.json"
AGG = DATA / "PART_BT3163_ISA_FULL_BFS_AGGREGATE.json"

BASELINES = [
    {"record_id":"baseline4/current4","universe":"baseline4","generators":["F_p","CX_pf","CX_fp","Z1"],"opcode_count":4,"group_order_reached":4_199_040,"mean_distance":14.175585133744857,"diameter":19},
    {"record_id":"baseline4/low4","universe":"baseline4","generators":["CX_fp","CX_pf","F_f","Z0"],"opcode_count":4,"group_order_reached":4_199_040,"mean_distance":15.216323969288219,"diameter":20},
]
FAST6 = {"record_id":"census56/fast6","universe":"census56","generators":["F_f","CX_pf","CX_fp","Z0","Z1","Z3"],"opcode_count":6,"group_order_reached":4_199_040,"mean_distance":13.72936957018747,"diameter":19}


def canonical_key(record):
    return tuple(sorted(record["generators"]))


def validate(record):
    assert record["universe"] in {"baseline4","census56","future_ge7"}
    n = record["opcode_count"]
    assert n == len(record["generators"])
    if record["universe"] == "baseline4": assert n == 4
    elif record["universe"] == "census56": assert n in (5,6)
    else: assert n >= 7
    assert record["group_order_reached"] == 4_199_040
    return True


def project(record, target):
    validate(record)
    if target == "shared_runtime_metrics":
        return {k:record[k] for k in ("record_id","universe","opcode_count","mean_distance","diameter")}
    if target == "census194_completeness":
        if record["universe"] != "census56":
            raise ValueError("cross-universe completeness promotion refused")
        return canonical_key(record)
    if target == "baseline_comparison":
        if record["universe"] not in {"baseline4","census56"}:
            raise ValueError("future family lacks frozen comparison contract")
        return project(record,"shared_runtime_metrics")
    raise ValueError("unknown projection")


def load_census():
    if not AGG.exists():
        return [FAST6], "CENSUS_1_OF_194_PLUS_2_BASELINES"
    data = json.loads(AGG.read_text(encoding="utf-8"))
    records = []
    for i,row in enumerate(data.get("records",[])):
        full = row["full_group"]
        record = {"record_id":f"census56/{i}","universe":"census56","generators":row["generators"],"opcode_count":len(row["generators"]),"group_order_reached":full["group_order_reached"],"mean_distance":full["mean_distance"],"diameter":full["diameter"]}
        validate(record); records.append(record)
    assert len(records) == 194 and len({canonical_key(r) for r in records}) == 194
    return records, "CENSUS_COMPLETE_194_PLUS_2_BASELINES"


def main():
    for record in BASELINES + [FAST6]: validate(record)
    census,status = load_census()
    census_keys = {project(r,"census194_completeness") for r in census}
    assert len(census_keys) == len(census)

    refused = []
    for record in BASELINES:
        try: project(record,"census194_completeness")
        except ValueError as exc: refused.append({"record_id":record["record_id"],"reason":str(exc)})
    assert len(refused) == 2

    malformed = dict(FAST6, record_id="negative/mislabelled_fast6", universe="baseline4")
    malformed_refused = False
    try: validate(malformed)
    except AssertionError: malformed_refused = True
    assert malformed_refused

    payload = {
        "schema":"w33.pass3278_3279.runtime_universe_firewall.v1",
        "status":status,
        "universes":{
            "baseline4":{"expected_size":2,"observed_size":2,"coverage_semantics":"operational comparison baselines only"},
            "census56":{"expected_size":194,"observed_size":len(census),"coverage_semantics":"five/six-opcode exhaustive census"},
            "future_ge7":{"expected_size":None,"observed_size":0,"coverage_semantics":"separately planned future families"},
        },
        "baseline_records":BASELINES,
        "census_observed_records":len(census),
        "census_pending_records":194-len(census),
        "shared_comparison_rows":[project(r,"shared_runtime_metrics") for r in BASELINES + census],
        "cross_universe_refusals":refused,
        "malformed_universe_control_refused":malformed_refused,
        "promotion_rule":"Only census56 records may increment the 194-design coverage counter. Baseline4 and future_ge7 records may enter explicitly typed shared-metric views but never census completeness.",
        "boundary":"Full affine reachability and software metrics do not establish decoder area, placement, calibration, energy, or a global optimum outside the completed universe.",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":status,"census":len(census),"baselines":2,"refused":len(refused)},sort_keys=True))


if __name__ == "__main__": main()
