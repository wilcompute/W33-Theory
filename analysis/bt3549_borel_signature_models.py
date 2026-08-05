#!/usr/bin/env python3
"""Emit the 24 exact B-invariant Moore-graph model contracts.

Each model has one binary variable per B-orbit on unordered vertex pairs.
The SRG(3250,57,0,1) equations are imposed lazily on ordered-pair orbit
representatives:
    sum_w e(u,w)e(v,w) = 0 when e(u,v)=1,
    sum_w e(u,w)e(v,w) = 1 when e(u,v)=0.
Products are linearized only when a separator is activated.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=ROOT/"analysis/bt3549_3555_borel_pentad_quantum_walk.py"

def load_main():
    spec=importlib.util.spec_from_file_location("bt3549_3555",MAIN)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def model_contract(signature):
    return {
        "schema":"w33.m57.borel_orbit_model.v1",
        "signature":signature,
        "variables":{
            "edge_orbit_binary":signature["binary_edge_orbit_variables"],
            "meaning":"select an undirected B-orbit of vertex pairs",
        },
        "linear_constraints":{
            "edge_count":1,
            "degree_orbit_equations":signature["vertex_orbits"],
            "internal_signature_counts":3,
        },
        "lazy_relation_equations":{
            "count":signature["ordered_pair_relation_equations"],
            "adjacent_rhs":0,
            "nonadjacent_rhs":1,
            "linearization":"introduce z_w=e(u,w)*e(v,w) only for activated representatives",
        },
        "fixed_data":{
            "vertices":3250,
            "degree":57,
            "edges":92625,
            "group":"C19 semidirect C9",
            "group_order":171,
        },
        "boundary":"Exact finite model contract only; no SAT/UNSAT verdict.",
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path)
    ap.add_argument("--signature")
    args=ap.parse_args()
    models=load_main().borel_signature_models()
    selected=[x for x in models["signatures"] if args.signature in (None,x["name"])]
    if args.signature and not selected:
        raise SystemExit(f"unknown signature: {args.signature}")
    packet={"status":"PASS_24_BOREL_MODEL_CONTRACTS","models":[model_contract(x) for x in selected]}
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(packet,indent=2,sort_keys=True)+"\n")
    print(packet["status"],len(packet["models"]))

if __name__=="__main__":
    main()
