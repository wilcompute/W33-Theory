#!/usr/bin/env python3
"""Sharded, independently checked proof archive for the 3,720 clique instances."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROVER=ROOT/"analysis/bt3544_clique_proof_dag.py"
ENGINE=ROOT/"analysis/bt3535_star_clique_recertify.py"
MAIN=ROOT/"analysis/bt3549_3555_borel_pentad_quantum_walk.py"

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def ranges():
    q,r=divmod(3720,64);out=[];start=0
    for shard in range(64):
        size=q+(shard<r)
        out.append((start,start+size))
        start+=size
    assert start==3720
    return out

def run_shard(shard):
    if not 0<=shard<64: raise ValueError(shard)
    prover=load(PROVER,"proof_dag")
    engine=load(ENGINE,"clique_engine")
    census=engine.load_census()
    states,counts=census.enumerate_candidates(3)
    assert counts==census.EXPECTED_STAGE_COUNTS
    survivors,candidate_digest=census.spectral_survivors(states)
    start,stop=ranges()[shard]
    rows=[]
    for index in range(start,stop):
        state_rows,state_edges=survivors[index]
        A=census.build_graph(state_rows,state_edges)
        columns,num,den=engine.admissible_columns(A)
        adj=engine.compatibility_graph(A,columns,num,den)
        witness,nodes=engine.maximum_clique(adj)
        cert=prover.certify(adj,witness)
        assert prover.verify_upper(adj,(1<<len(adj))-1,len(witness),cert["upper_proof"])
        rows.append({
            "candidate":index,
            "compatibility_vertices":len(adj),
            "maximum_clique":len(witness),
            "witness":witness,
            "search_nodes":nodes,
            "proof_DAG":cert["upper_proof"],
            "proof_DAG_digest":cert["proof_sha256"],
        })
    return {
        "schema":"w33.star_clique_proof_shard.v1",
        "shard":shard,"start":start,"stop":stop,
        "candidate_digest":candidate_digest,
        "rows":rows,
        "shard_digest":digest([(r["candidate"],r["proof_DAG_digest"]) for r in rows]),
    }

def aggregate(paths):
    main=load(MAIN,"packet")
    packets=[json.loads(Path(p).read_text()) for p in paths]
    assert len(packets)==64
    packets.sort(key=lambda x:x["shard"])
    rows=[];candidate_digest=None
    for shard,p in enumerate(packets):
        assert p["shard"]==shard
        start,stop=ranges()[shard]
        assert (p["start"],p["stop"])==(start,stop)
        candidate_digest=candidate_digest or p["candidate_digest"]
        assert p["candidate_digest"]==candidate_digest
        assert p["shard_digest"]==digest([(r["candidate"],r["proof_DAG_digest"]) for r in p["rows"]])
        rows.extend(p["rows"])
    assert [r["candidate"] for r in rows]==list(range(3720))
    histogram={};leaves=[]
    for r in rows:
        histogram[str(r["maximum_clique"])]=histogram.get(str(r["maximum_clique"]),0)+1
        leaves.append(digest([r["candidate"],r["proof_DAG_digest"],r["maximum_clique"],r["witness"]]))
    root=main.merkle_root(leaves)
    return {
        "status":"PASS_COMPLETE_3720_PROOF_ARCHIVE",
        "instances":3720,
        "candidate_digest":candidate_digest,
        "maximum_clique_histogram":dict(sorted(histogram.items(),key=lambda kv:int(kv[0]))),
        "archive_merkle_root":root,
        "shard_digests":[p["shard_digest"] for p in packets],
    }

def self_test():
    main=load(MAIN,"packet")
    contract=main.proof_archive_contract()
    assert len(ranges())==64
    assert contract["shard_size_census"]=={"58":56,"59":8}
    return {"status":"PASS_PROOF_ARCHIVE_SELF_TEST","synthetic_merkle":contract["synthetic_merkle_selftest"]}

def main_cli():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--shard",type=int)
    ap.add_argument("--aggregate",nargs="*")
    ap.add_argument("--json",type=Path)
    args=ap.parse_args()
    if args.self_test: result=self_test()
    elif args.shard is not None: result=run_shard(args.shard)
    elif args.aggregate is not None: result=aggregate(args.aggregate)
    else: raise SystemExit("choose --self-test, --shard, or --aggregate")
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(result["status"])

if __name__=="__main__":
    main_cli()
