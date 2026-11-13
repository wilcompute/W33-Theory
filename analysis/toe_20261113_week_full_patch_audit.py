#!/usr/bin/env python3
"""Stream every text patch reachable in the past-week master log.
Read only; report content digests and correction indicators, not physics proofs.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import datetime, hashlib, json, re, subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261113_week_full_patch_audit.json"
BEGIN="===W33_COMMIT_START==="
cmd=["git","log","master","-m","--since=2026-11-06T00:00:00-05:00",
     "--format="+BEGIN+"%H|%aI|%s","--patch","--no-ext-diff","--no-renames"]
p=subprocess.Popen(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
current=None
all_records=[]
total_lines=0
total_bytes=0
keyword_hits=Counter()
needle=re.compile(rb"(withdrawn?|no.go|correction|counterexample|unsupported|refut|invalid|fails?|experimental|saturation|proven|conjecture)",re.I)
def finish():
    if current is not None:
        h=current.pop("_hash")
        current["text_patch_sha256"]=h.hexdigest()
        all_records.append(current)
for raw in p.stdout:
    total_lines+=1
    total_bytes+=len(raw)
    line=raw.decode("utf-8","replace")
    if line.startswith(BEGIN):
        finish()
        fields=line[len(BEGIN):].strip().split("|",2)
        current={"sha":fields[0],"date":fields[1],"subject":fields[2],
                 "patch_bytes":0,"added_lines":0,"removed_lines":0,"file_hunks":0,
                 "match_terms":[],"_hash":hashlib.sha256()}
        if len(all_records)%80==0: print("patch_records",len(all_records),flush=True)
        continue
    if current is None:continue
    current["patch_bytes"]+=len(raw)
    current["_hash"].update(raw)
    if line.startswith("diff --git "):
        current["file_hunks"]+=1
    elif line.startswith("+") and not line.startswith("+++"):
        current["added_lines"]+=1
    elif line.startswith("-") and not line.startswith("---"):
        current["removed_lines"]+=1
    if len(current["match_terms"])<4:
        m=needle.search(raw)
        if m:
            word=m.group().decode("ascii","replace").lower()
            keyword_hits[word]+=1
            current["match_terms"].append(word)
finish()
rc=p.wait()
stderr=p.stderr.read().decode("utf-8","replace")[-500:]
assert rc==0,stderr
unique=len(set(r["sha"] for r in all_records))
res={"scope":"master all parents, week ending 2026-11-13",
     "head":subprocess.check_output(["git","rev-parse","master"],cwd=ROOT).decode().strip(),
     "distinct_commit_sha":unique,"patch_stream_records":len(all_records),
     "total_text_lines":total_lines,"total_text_bytes":total_bytes,
     "keyword_counter":keyword_hits.most_common(),
     "records":all_records,
     "notes":"Binary contents are summarized by git diff, not decoded. Merge commits repeat per parent under -m. Hashing/keyword scanning all text patches is not a line-by-line human proof review."}
OUT.write_text(json.dumps(res,indent=2)+"\n",encoding="utf-8")
print("COMMITS",unique,"RECORDS",len(all_records),"PATCH_BYTES",total_bytes,"PATCH_LINES",total_lines)
print("OUTPUT",OUT)