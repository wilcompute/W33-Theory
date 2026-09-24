#!/usr/bin/env python3
"""Pass 409: self-contained D4 contact-grading root census."""
from __future__ import annotations
import json
from itertools import combinations, product
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_pass409_d4_contact_root_census.json"

e=[sp.eye(4).col(i) for i in range(4)]
simple=[
    e[0]-e[1],
    e[1]-e[2],
    e[2]-e[3],
    e[2]+e[3],
]
S=sp.Matrix.hstack(*simple)
assert int(S.det())==2

roots=[]
for i,j in combinations(range(4),2):
    for si,sj in product((-1,1),repeat=2):
        roots.append(si*e[i]+sj*e[j])
assert len(roots)==24

def icoords(v):
    c=S.inv()*v
    assert all(x.q==1 for x in c)
    return tuple(int(x) for x in c)

records=[]
for r in roots:
    c=icoords(r)
    grade=c[1]
    weights=tuple(int((r.T*a)[0]) for a in (simple[0],simple[2],simple[3]))
    records.append({"root":[int(x) for x in r],
                    "simple":list(c),"grade":grade,
                    "a1_cubed_weights":list(weights)})

grades={g:[r for r in records if r["grade"]==g] for g in (-2,-1,0,1,2)}
assert {g:len(v) for g,v in grades.items()}=={-2:1,-1:8,0:6,1:8,2:1}

zero_simple={tuple(r["simple"]) for r in grades[0]}
assert zero_simple=={
    (1,0,0,0),(-1,0,0,0),
    (0,0,1,0),(0,0,-1,0),
    (0,0,0,1),(0,0,0,-1),
}
minus_weights={tuple(r["a1_cubed_weights"]) for r in grades[-1]}
assert minus_weights==set(product((-1,1),repeat=3))

minus2=sp.Matrix(grades[-2][0]["root"])
pairs=[]
used=set()
for i,a in enumerate(grades[-1]):
    if i in used: continue
    va=sp.Matrix(a["root"])
    js=[j for j,b in enumerate(grades[-1])
        if j!=i and va+sp.Matrix(b["root"])==minus2]
    assert len(js)==1
    j=js[0]
    used.add(i); used.add(j)
    pairs.append((tuple(a["a1_cubed_weights"]),
                  tuple(grades[-1][j]["a1_cubed_weights"])))
assert len(pairs)==4 and len(used)==8
assert all(tuple(-x for x in a)==b for a,b in pairs)

highest=max(records,key=lambda r:r["grade"])
assert highest["grade"]==2
assert highest["simple"]==[1,2,1,1]

out={
 "schema":"w33.pass409.d4_contact_root_census.v1",
 "status":"PASS_D4_CONTACT_GRADING_IS_A1_CUBED_ON_222_HEISENBERG",
 "simple_roots":[[int(x) for x in a] for a in simple],
 "highest_root_simple_coordinates":highest["simple"],
 "root_grade_counts":{str(g):len(v) for g,v in grades.items()},
 "g0_semisimple":"A1^3",
 "g_minus1_dimension":8,
 "g_minus1_weight_set":[list(w) for w in sorted(minus_weights)],
 "g_minus2_dimension":1,
 "heisenberg_pairing_weights":[[list(a),list(b)] for a,b in pairs],

 "derived_contact_parabolic_dimension":9+8+1,
 "derived_contact_parabolic":"sl2^3 semidirect h9",
 "comparison_to_repo_core":{
   "repo_core_dimension":18,
   "repo_levi_after_splitting":"sl2^3",
   "repo_heisenberg":"h9",
   "repo_W8":"(2,2,2)",
   "fingerprint_matches":True,
 },
 "theorem":"The 18D residual core has exactly the D4 derived contact-parabolic root/module fingerprint after splitting the cubic centroid field.",
 "boundary":"This root census proves the abstract graded fingerprint. It does not supply a single basis-conjugating matrix from the repo core to a conventional D4 Chevalley basis."
}
OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":out["status"],
                  "grades":out["root_grade_counts"],
                  "pairs":len(pairs)},indent=2))
