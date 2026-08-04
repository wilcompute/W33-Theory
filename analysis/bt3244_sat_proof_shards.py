#!/usr/bin/env python3
"""Proof-producing 100-shard driver; SAT and UNSAT are accepted only with checked evidence."""
from __future__ import annotations
import argparse, collections, hashlib, importlib.util, json, re
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("base",ROOT/"analysis/bt3187_3192_chromatic_defect_block_filter.py")
BASE=importlib.util.module_from_spec(SPEC); assert SPEC.loader; SPEC.loader.exec_module(BASE)
BASE_SHA="6c0c3daac0ac1592fd3d84c45cad157c8e6e1b95ffe87b47868db4589c6b7cd5"
BASE_VARS=7800; BASE_CLAUSES=146289; X_VARS=5400


def emit_base(path:Path):
    _,_,_,_,_,m,h=BASE.build_geometry(); k=10
    x=lambda v,c:1+v*k+c; miss=lambda e,c:1+X_VARS+e*k+c
    inc=[list(map(int,np.where(m[:,e])[0])) for e in range(240)]
    with path.open("w",encoding="ascii") as out:
        out.write(f"p cnf {BASE_VARS} {BASE_CLAUSES}\n")
        def clause(z): out.write(" ".join(map(str,z))+" 0\n")
        for v in range(540):
            clause([x(v,c) for c in range(k)])
            for a in range(k):
                for b in range(a+1,k): clause([-x(v,a),-x(v,b)])
        for u,v in zip(*np.where(np.triu(h,1))):
            for c in range(k): clause([-x(int(u),c),-x(int(v),c)])
        for e,fs in enumerate(inc):
            clause([miss(e,c) for c in range(k)])
            for a in range(k):
                for b in range(a+1,k): clause([-miss(e,a),-miss(e,b)])
            for c in range(k):
                for v in fs: clause([-miss(e,c),-x(v,c)])
                clause([x(v,c) for v in fs]+[miss(e,c)])
        for c,v in enumerate(inc[0]): clause([x(v,c)])
    got=hashlib.sha256(path.read_bytes()).hexdigest()
    if got!=BASE_SHA: raise RuntimeError(f"base CNF drift: {got}")


def assumptions(shard:int):
    if not 0<=shard<100: raise ValueError(shard)
    a,b=divmod(shard,10)
    return a,b,[1+X_VARS+1*10+a,1+X_VARS+2*10+b]


def emit_shard(path:Path, shard:int):
    tmp=path.with_suffix(".base.tmp")
    emit_base(tmp)
    a,b,lits=assumptions(shard)
    with tmp.open("r",encoding="ascii") as src, path.open("w",encoding="ascii") as out:
        header=src.readline().strip()
        if header!=f"p cnf {BASE_VARS} {BASE_CLAUSES}": raise RuntimeError(header)
        out.write(f"p cnf {BASE_VARS} {BASE_CLAUSES+2}\n")
        for line in src: out.write(line)
        for lit in lits: out.write(f"{lit} 0\n")
    tmp.unlink()
    return {"shard":f"{shard:02d}","missing_colors":[a,b],"assumptions":lits,
            "cnf_sha256":hashlib.sha256(path.read_bytes()).hexdigest()}


def parse_model(log:Path):
    vals={}
    for line in log.read_text(encoding="utf-8",errors="replace").splitlines():
        if not line.startswith("v "): continue
        for tok in line.split()[1:]:
            lit=int(tok)
            if lit==0: continue
            vals[abs(lit)]=lit>0
    colors=[]
    for v in range(540):
        selected=[c for c in range(10) if vals.get(1+10*v+c,False)]
        if len(selected)!=1: raise ValueError(f"vertex {v}: {selected}")
        colors.append(selected[0])
    return colors


def verify_colors(colors):
    _,_,_,_,_,m,h=BASE.build_geometry(); colors=np.asarray(colors,dtype=np.int64)
    if colors.shape!=(540,) or not set(map(int,colors))<=set(range(10)): return False
    if any(colors[u]==colors[v] for u,v in zip(*np.where(np.triu(h,1)))): return False
    for e in range(240):
        used=set(map(int,colors[np.where(m[:,e])[0]]))
        if len(used)!=9: return False
    return True


def classify(shard:int, solver_log:Path, exit_code:int, out:Path, drat_verified:bool=False):
    text=solver_log.read_text(encoding="utf-8",errors="replace")
    record={"schema":"w33.pass3244.sat_shard_status.v1","shard":f"{shard:02d}",
            "solver_exit_code":exit_code,"SAT_model_valid":False,"UNSAT_proof_verified":False}
    if re.search(r"^s SATISFIABLE\s*$",text,re.M):
        colors=parse_model(solver_log)
        if not verify_colors(colors): raise SystemExit("SAT model failed independent checker")
        record.update(status="SAT_VALID_MODEL",SAT_model_valid=True,class_sizes=dict(sorted(collections.Counter(colors).items())),
                      model_sha256=hashlib.sha256(bytes(colors)).hexdigest())
    elif re.search(r"^s UNSATISFIABLE\s*$",text,re.M):
        if not drat_verified: raise SystemExit("UNSAT without verified DRAT/LRAT proof")
        record.update(status="UNSAT_VERIFIED_PROOF",UNSAT_proof_verified=True)
    elif exit_code in (124,137):
        record.update(status="TIMEOUT_NO_RESULT")
    else:
        record.update(status="UNKNOWN_NO_RESULT")
    record["solver_log_sha256"]=hashlib.sha256(solver_log.read_bytes()).hexdigest()
    out.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
    return record


def aggregate(directory:Path,out:Path):
    files=sorted(directory.rglob("status.json"))
    records=[json.loads(p.read_text()) for p in files]
    ids=[r["shard"] for r in records]
    if len(records)!=100 or len(set(ids))!=100 or set(ids)!={f"{i:02d}" for i in range(100)}:
        raise SystemExit(f"incomplete shard set: {len(records)} records, {len(set(ids))} unique")
    hist=collections.Counter(r["status"] for r in records)
    result={"schema":"w33.pass3244.sat_shard_aggregate.v1","shards":100,
            "status_histogram":dict(sorted(hist.items())),
            "SAT_valid_models":hist["SAT_VALID_MODEL"],"UNSAT_verified_proofs":hist["UNSAT_VERIFIED_PROOF"],
            "terminally_decided":hist["SAT_VALID_MODEL"]+hist["UNSAT_VERIFIED_PROOF"],
            "boundary":"Only SAT_VALID_MODEL or UNSAT_VERIFIED_PROOF is theorem evidence; timeout and UNKNOWN are non-results.",
            "records":sorted(records,key=lambda r:r["shard"])}
    result["sha256_without_hash_field"]=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")


def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("emit");p.add_argument("--shard",type=int,required=True);p.add_argument("--out",type=Path,required=True);p.add_argument("--meta",type=Path)
    p=sub.add_parser("classify");p.add_argument("--shard",type=int,required=True);p.add_argument("--solver-log",type=Path,required=True);p.add_argument("--exit-code",type=int,required=True);p.add_argument("--drat-verified",action="store_true");p.add_argument("--out",type=Path,required=True)
    p=sub.add_parser("aggregate");p.add_argument("--dir",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    if a.cmd=="emit":
        a.out.parent.mkdir(parents=True,exist_ok=True); rec=emit_shard(a.out,a.shard)
        if a.meta:a.meta.write_text(json.dumps(rec,indent=2,sort_keys=True)+"\n")
        print(json.dumps(rec,sort_keys=True))
    elif a.cmd=="classify": classify(a.shard,a.solver_log,a.exit_code,a.out,a.drat_verified)
    else: aggregate(a.dir,a.out)
if __name__=="__main__":main()
