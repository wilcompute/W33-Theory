#!/usr/bin/env python3
"""Freeze the exact GAP qutrit-fibre -> W33 signed-edge transducer witness."""
from __future__ import annotations
import json, re, subprocess, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GAP=ROOT/"analysis/w33_20260923_qutrit_edge_triality_transducer.g"
OUT=ROOT/"data/w33_20260923_qutrit_edge_triality_transducer.json"
if shutil.which("gap"):
    cmd=["gap","-q",str(GAP)]
else:
    wsl_path="/mnt/c/"+str(GAP).replace("\\","/").split("C:/",1)[-1]
    cmd=["wsl","gap","-q",wsl_path]
cp=subprocess.run(cmd,capture_output=True,text=True,check=True)
s=cp.stdout+cp.stderr

def ints(pat):
    m=re.search(pat,s); assert m,(pat,s)
    return [int(x) for x in re.findall(r"-?\d+",m.group(1))]

canonical=int(re.search(r"CANONICAL_H6\s+(\d+)",s).group(1))
ind=ints(r"IND_DEG.*?DEGS \[([^\]]+)\]")
edge=ints(r"EDGE_DEG.*?DEGS \[([^\]]+)\]")
inner=int(re.search(r"INNER\s+(\d+)",s).group(1))
orbit=ints(r"OUTER_ORBIT \[([^\]]+)\]")
assert canonical==11 and ind==[10,60,80,90]
assert edge==[15,24,30,81,90] and inner==1 and orbit==[9,10,11]

out={
 "schema":"w33.20260923.qutrit_edge_triality_transducer.v1",
 "status":"PASS_UNIQUE_QUTRIT_FIBRE_TO_W90_CONSTRAINT_TRANSDUCER",
 "W_order":51840,"H_order":1296,"index":40,
 "canonical_local_Weil6_character_id":canonical,
 "induced_240_degrees":ind,
 "signed_edge_240_degrees":edge,
 "Hom_dimension":inner,
 "unique_common_degree":90,
 "local_six_outer_orbit":orbit,
 "outer_group":"C3",
 "routing":{
   "global_W6_restricts_to_local_frame":9,
   "W90_contains_local_frames":[10,11],
   "canonical_frame":11,
   "image":"unique degree-90 W(E6) constituent"
 },
 "repo_crosscheck":"Prior exact passes identify W90 as the fused constraint block; W81 is the harmonic/logical block.",
 "boundary":"This is an equivariant finite-module routing theorem, not a dynamical coupling strength or particle identification.",
 "gap_stdout":s
}
OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:out[k] for k in ("status","Hom_dimension","unique_common_degree")},indent=2))
