#!/usr/bin/env python3
"""Passes 3238-3249 exact switch/gauge/spiral certificate coordinator."""
from __future__ import annotations
import collections, hashlib, importlib.util, json, sys
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from bt3238_3249_common import semantic_hash, switch_family
from bt3238_3239_cover_symmetry import cover_symmetry
from bt3240_3241_port_gauge import block_complex
from bt3242_3243_real_spiral import spiral_controller
OUT=ROOT/"data/PART_BT3238_BT3249_SWITCH_GAUGE_SPIRAL_results.json"
DIAG=ROOT/"data/bt3244_sat_shard_diagnostic.json"
SPEC=importlib.util.spec_from_file_location("base",ROOT/"analysis/bt3187_3192_chromatic_defect_block_filter.py")
BASE=importlib.util.module_from_spec(SPEC); assert SPEC.loader; SPEC.loader.exec_module(BASE)

def json_default(o):
    if isinstance(o,np.bool_): return bool(o)
    if isinstance(o,np.integer): return int(o)
    if isinstance(o,np.floating): return float(o)
    if o is sp.true: return True
    if o is sp.false: return False
    if isinstance(o,sp.Integer): return int(o)
    if isinstance(o,sp.Rational): return str(o)
    if isinstance(o,sp.Basic): return str(o)
    raise TypeError(type(o).__name__)

def sat_diagnostic():
    d=json.loads(DIAG.read_text())
    assert d["shards_executed"]==d["unique_shards"]==100
    assert d["status_histogram"]=={"TIME_LIMIT_NO_PRIMAL":100}
    assert d["SAT_models"]==d["UNSAT_proofs"]==0
    return {
      "shards_executed":100,
      "bounded_HiGHS_status_histogram":d["status_histogram"],
      "SAT_models":0,"UNSAT_proofs":0,
      "time_limit_seconds_each":d["time_limit_seconds_each"],
      "elapsed_seconds_range":[d["elapsed_seconds_min"],d["elapsed_seconds_max"]],
      "elapsed_seconds_mean":d["elapsed_seconds_mean"],
      "record_manifest_sha256":d["record_manifest_sha256"],
      "diagnostic_sha256":hashlib.sha256(DIAG.read_bytes()).hexdigest(),
      "boundary":"All 100 shards were executed under a bounded MILP diagnostic. Timeouts without primals are neither SAT nor UNSAT evidence. The proof workflow requires a checked model or DRAT/LRAT proof."
    }

def certificate():
    points,a,lines,edges,frames,m,h=BASE.build_geometry()
    octets,blocks,pairorbits=BASE.canonical_blocks(points,a,lines,frames)
    pidx={p:i for i,p in enumerate(points)}
    point_generators=[BASE.transvection(points,pidx,v) for v in ((1,0,0,0),(0,1,0,0),(0,0,0,1),(1,0,1,0))]
    colors=BASE.load_coloring(); counts=collections.Counter(map(int,colors))
    cover=tuple(sorted(map(int,np.where(colors==next(c for c,n in counts.items() if n==60))[0])))
    loci,coords,family=switch_family(m,h,cover)
    symmetry=cover_symmetry(m,h,points,lines,frames,point_generators,cover,loci,coords,family)
    complex_data=block_complex(m,h,blocks)
    spiral=spiral_controller()
    diag=sat_diagnostic()
    checks={
      "w33_counts":(len(points),len(lines),len(edges),len(frames))==(40,40,240,540),
      "pair_orbits":pairorbits==[540,3240,3240,4320,12960],
      "family_243":len(family)==243,
      "C4_switch_stabilizer":symmetry["setwise_stabilizer_structure"]=="C4",
      "fixed_27":symmetry["fixed_covers"]==27,
      "free_pi1_rank_436":complex_data["free_nonabelian_generators"]==436,
      "spiral_S3_shadow":spiral["mod2_even_subgroup_is_S3"],
      "all_100_diagnostic_shards":diag["shards_executed"]==100
    }
    assert all(checks.values())
    data={
      "schema":"w33.pass3238_3249.switch_gauge_spiral.v1",
      "status":"PASS_EXACT_SWITCH_GAUGE_SPIRAL_WITH_CHROMATIC_AND_PUBLICATION_GATES_OPEN",
      "live_chromatic_boundary":"10 <= chi(H) <= 11",
      "pass3238_3239_PSp_switch_family":symmetry,
      "pass3240_3241_nonabelian_port_gauge":complex_data,
      "pass3242_3243_real_spiral_and_S3_shadow":spiral,
      "pass3244_sat_shards":diag,
      "pass3245_publication_gate":{
        "source_packet":"ready",
        "previous_pass3226_3237_job":"externally queued at source time",
        "claim_boundary":"No RTL, synthesis, placement or three-PDF success is promoted until the dedicated workflow is terminal green and its artifacts are inspected."
      },
      "pass3246_bonkers_fixed27":{
        "result":"The C4-fixed covers are a weighted ternary cube, not the Schlaefli graph.",
        "exact_formula":symmetry["fixed27_affine_code"]["cover_intersection_formula"]
      },
      "pass3247_bonkers_nonabelian_logical_ports":{
        "result":"The [[720,436,2]] binary CSS layer is the sign-character shadow of flat S3 gain assignments on the free fundamental group F_436.",
        "spiral_compiler":"The six S3 gains are realized by the mod-2 shadow of the integral O(2,2) unit-spiral controller."
      },
      "checks":checks,
      "evidence_boundary":{
        "proved":"finite geometry, PSp action, affine involution, weighted ternary metric, free fundamental group, Burnside count, integer invariant forms, finite-field group actions",
        "diagnostic_only":"100 bounded HiGHS shard runs",
        "pending":"checked SAT/UNSAT terminal certificates, observed RTL/synthesis/placement, materialized canonical front doors and three PDFs, physical calibration"
      }
    }
    data["sha256_without_hash_field"]=semantic_hash(data)
    return data

def main():
    data=certificate()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,sort_keys=True,separators=(",",":"),default=json_default)+"\n")
    print(json.dumps({
      "status":data["status"],
      "semantic_sha256":data["sha256_without_hash_field"],
      "switch_stabilizer":data["pass3238_3239_PSp_switch_family"]["setwise_stabilizer_structure"],
      "fixed_covers":data["pass3238_3239_PSp_switch_family"]["fixed_covers"],
      "free_pi1_rank":data["pass3240_3241_nonabelian_port_gauge"]["free_nonabelian_generators"],
      "mod2_S3":data["pass3242_3243_real_spiral_and_S3_shadow"]["mod2_even_subgroup_is_S3"],
      "sat_boundary":data["pass3244_sat_shards"]["boundary"]
    },indent=2))
if __name__=="__main__":main()
