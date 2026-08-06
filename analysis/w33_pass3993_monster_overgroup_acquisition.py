#!/usr/bin/env python3
"""Pass 3993: fail-closed Monster U4(2) acquisition through explicit maximal overgroups."""
from __future__ import annotations
import argparse, ast, contextlib, hashlib, importlib.util, io, itertools, json, os, re, subprocess, sys
from collections import deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGET_ORDER=25920
PAIR_TARGET=[3,6,6,6,6,6]
TRIPLE_TARGET=[648,648,648,648]

def norm(x):
    x=x.lower().replace("psl","l").replace("psu","u")
    return re.sub(r"[^a-z0-9]","",x)

def parse_gap(path):
    direct=None; maximal=None; rows=[]
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith("DIRECT_FUSION_COUNT="): direct=int(line.split("=",1)[1])
        elif line.startswith("MAXIMAL_TABLE_COUNT="): maximal=int(line.split("=",1)[1])
        elif line.startswith("OVERGROUP="):
            fields=dict(item.split("=",1) for item in line.split(";"))
            rows.append({"table":fields["OVERGROUP"],
              "u_to_h":int(fields["U_TO_H"]),"h_to_m":int(fields["H_TO_M"]),
              "composed":int(fields["COMPOSED"]),"direct_match":int(fields["DIRECT_MATCH"])})
    if direct is None or maximal is None: raise RuntimeError("incomplete GAP output")
    return direct,maximal,rows

def load_database(repo):
    source=repo/"GetGeneratorsOfSubgroupInM.py"
    if not source.exists(): raise FileNotFoundError(source)
    text=source.read_text(encoding="utf-8")
    sys.path.insert(0,str(repo))
    spec=importlib.util.spec_from_file_location("monster_subgroups_db",source)
    if spec is None or spec.loader is None: raise RuntimeError("cannot import generator database")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    capture=io.StringIO(); returned=None
    if hasattr(mod,"ListKeys"):
        with contextlib.redirect_stdout(capture): returned=mod.ListKeys()
    if isinstance(returned,(list,tuple,set)): keys=[str(x) for x in returned]
    else:
        keys=[]
        for line in capture.getvalue().splitlines():
            keys.extend(re.findall(r"['\"]([^'\"]+)['\"]",line))
    if not keys:
        tree=ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node,ast.Dict):
                for k in node.keys:
                    if isinstance(k,ast.Constant) and isinstance(k.value,str): keys.append(k.value)
    keys=sorted(set(keys))
    commit=subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()
    return mod,source,keys,commit

def generator_words(mod,key):
    for args in [(key,False),(key,)]:
        try:
            value=mod.Maximal(*args)
            if isinstance(value,(list,tuple)) and len(value)>=2:
                return [str(x) for x in value]
        except Exception:
            continue
    return []

def bfs_pool(gens,cap=3000,depth=4):
    one=gens[0]**0; moves=gens+[g**-1 for g in gens]
    seen={one.as_int():one}; q=deque([(one,0)])
    while q and len(seen)<cap:
        h,d=q.popleft()
        if d>=depth: continue
        for g in moves:
            x=g*h; k=x.as_int()
            if k not in seen:
                seen[k]=x; q.append((x,d+1))
                if len(seen)>=cap: break
    return list(seen.values())

def subgroup_order(gens,MM_from_int,cap):
    one=gens[0]**0; moves=gens+[g**-1 for g in gens]
    seen={one.as_int():one}; q=deque([one])
    while q:
        h=q.popleft()
        for g in moves:
            x=g*h; k=x.as_int()
            if k not in seen:
                if len(seen)>=cap: return cap+1
                y=MM_from_int(k)
                if y.as_int()!=k: raise RuntimeError("MM integer roundtrip failed")
                seen[k]=y; q.append(y)
    return len(seen)

def bounded_search(words,max_quads=50000):
    from mmgroup import MM,MM_from_int
    gens=[MM(w) for w in words[:2]]
    for g in gens:
        assert MM_from_int(g.as_int())==g
    pool=bfs_pool(gens)
    order3=[]
    for x in pool:
        try:
            if int(x.order())==3: order3.append(x)
        except Exception: pass
        if len(order3)>=80: break
    tested=0
    for quad in itertools.combinations(order3,4):
        tested+=1
        if tested>max_quads: break
        pairs=sorted(int((quad[i]*quad[j]).order()) for i,j in itertools.combinations(range(4),2))
        if pairs!=PAIR_TARGET: continue
        triples=[]; good=True
        for omit in range(4):
            o=subgroup_order([quad[j] for j in range(4) if j!=omit],MM_from_int,648)
            triples.append(o)
            if o!=648: good=False; break
        if not good: continue
        full=subgroup_order(list(quad),MM_from_int,TARGET_ORDER)
        if full==TARGET_ORDER:
            return {"found":True,"words":[str(x) for x in quad],"pair_orders":pairs,
                    "triple_orders":triples,"closure_order":full,"pool_size":len(pool),
                    "order3_candidates":len(order3),"quadruples_tested":tested}
    return {"found":False,"pool_size":len(pool),"order3_candidates":len(order3),
            "quadruples_tested":tested}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--gap-output",type=Path,required=True)
    ap.add_argument("--database",type=Path,required=True); args=ap.parse_args()
    direct,maximal,rows=parse_gap(args.gap_output)
    compatible=[r for r in rows if r["direct_match"]>0]
    mod,source,keys,commit=load_database(args.database)
    matches={}
    for row in compatible:
        nt=norm(row["table"])
        choices=sorted(keys,key=lambda k:(0 if norm(k)==nt else 1,abs(len(norm(k))-len(nt)),k))
        close=[k for k in choices if nt in norm(k) or norm(k) in nt][:5]
        matches[row["table"]]=close
    inventories=[]; candidate=None
    searched=set()
    for table,close in matches.items():
        for key in close:
            if key in searched: continue
            searched.add(key); words=generator_words(mod,key)
            rec={"key":key,"overgroup_table":table,"generator_count":len(words),
                 "generator_sha256":hashlib.sha256("\n".join(words).encode()).hexdigest() if words else None}
            if words:
                try:
                    search=bounded_search(words); rec["bounded_search"]=search
                    if search.get("found") and candidate is None: candidate=search
                except Exception as exc: rec["bounded_search_error"]=repr(exc)
            inventories.append(rec)
    result={"schema":"w33.pass3993.monster_overgroup_acquisition.v1",
      "status":"PASS_CONCRETE_MONSTER_U42_WORDS" if candidate else "PENDING_EXPLICIT_MONSTER_U42_WORDS",
      "direct_class_fusions":direct,"monster_maximal_tables":maximal,
      "compatible_overgroups":compatible,"database_commit":commit,
      "database_source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
      "database_key_count":len(keys),"matched_explicit_overgroups":inventories,
      "candidate":candidate,"promoted":bool(candidate),
      "boundary":"Maximal-overgroup fusions and published maximal-generator inventory are executable narrowing evidence. An embedding is promoted only if four explicit MM words pass pair, triple, full closure, and subsequent object-action/class-fusion gates."}
    result["semantic_sha256"]=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    out=ROOT/"data/PART_3993_MONSTER_OVERGROUP_ACQUISITION.json"; out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    if candidate:
        target=ROOT/"data/PART_3751_MONSTER_U42_CLASS_FUSION_EXECUTION.json"
        target.write_text(json.dumps({"generators":candidate["words"],"source":"pass3993 bounded maximal-overgroup search"},indent=2)+"\n")
    print("PASS_MONSTER_OVERGROUP_ACQUISITION",len(compatible),len(inventories),result["status"],result["semantic_sha256"])
if __name__=="__main__": main()
