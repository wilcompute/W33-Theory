"""TOE46: exact Wilson point / cusp line selector crosschecked with 491 model census.

The frozen 491 records contain torus position labels, not an embedding of
each model's holonomy as a particular projective Pauli vector. This packet
deliberately refuses to infer unsupplied model-specific cusp constraints.
"""
import json,itertools,collections
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
old=json.loads((ROOT/"data/w33_pass11903_census491_frozen.json").read_text())
summary=json.loads((ROOT/"data/w33_pass11903_local_ten_locks_charm_up.json").read_text())
assert len(old)==491 and summary["all_checks_pass"]
types=collections.Counter(row["kind"] for row in old.values())
twist=[row for row in old.values() if row["kind"]=="twisted_one_torus"]
assert types=={"untwisted":339,"twisted_one_torus":152}
assert all(row["U_same"] and row["E_same"] for row in twist)
assert all(row["up_wilson_patterns"]==[[0,0]] or row["up_wilson_patterns"]==[] for row in twist)
down=[row["label"] for row in twist if any(any(p) for p in row["down_wilson_patterns"])]
assert len(down)==5
canon=lambda v:min(v,tuple(-a%3 for a in v))
pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
sp=lambda p,q:(p[0]*q[2]+p[1]*q[3]-p[2]*q[0]-p[3]*q[1])%3
i={p:j for j,p in enumerate(pts)}
lines=set()
for u,p in enumerate(pts):
 for q in pts[u+1:]:
  if sp(p,q):continue
  lines.add(tuple(sorted({i[canon(tuple((a*p[k]+b*q[k])%3 for k in range(4)))] for a,b in itertools.product(range(3),repeat=2) if a or b})))
lines=sorted(lines);assert len(lines)==40
# Prove the selection 4 incident +36 with exactly one commuting point
# for EVERY 40 possible Wilson point, not just the example Z2.
patterns=[]
for j,p in enumerate(pts):
 inc=[line for line in lines if j in line]
 noninc=[line for line in lines if j not in line]
 assert len(inc)==4 and len(noninc)==36
 assert all(sum(sp(p,pts[q])==0 for q in line)==4 for line in inc)
 assert all(sum(sp(p,pts[q])==0 for q in line)==1 for line in noninc)
 patterns.append([len(inc),len(noninc)])
# Class torus labels represent VEV/fixed-point localization, not direct
# projective W33 Pauli coordinates; keep them separate!
classes=collections.Counter(str(row["Q_points"]) for row in twist)
npatterns=collections.Counter(str(row["down_wilson_patterns"]) for row in twist)
zero_model_selector_information=(len(set(map(tuple,patterns)))==1)
out={
 "status":"CENSUS491_WILSON_CUSP_GEOMETRIC_SELECTOR_AND_FLAVOR_FIREWALL",
 "census":{"records":len(old),"kinds":dict(types),"twisted_local_10":sum(r["U_same"] and r["E_same"] for r in twist),
 "renormalizable_up_non_single_point_patterns":0,"down_non_single_point_models":len(down),
 "down_non_single_point_labels":down,
 "twisted_Q_point_patterns":dict(classes),
 "down_pattern_distribution":dict(npatterns)},
 "geometry":{"projective_points":len(pts),"cusps":len(lines),
 "all_40_holonomy_choices_incidence_4_36":all(k==[4,36] for k in patterns),
 "every_nonincident_context_has_exactly_one_commuting_pauli":True,
 "incident_flags":40*4},
 "no_discriminative_information":"Each Wilson-point p has EXACTLY the same [4,36] incidence fingerprint under Sp(4,3) transitivity. Therefore a raw 4:36 count alone cannot distinguish or predict which of the 491 models admits up-sector splitting. A model-by-model embedding of each torus Wilson line into an actual projective Pauli p and physical Yukawa selection operators is necessary.",
 "zero_model_discrimination_from_unlabelled_incidence":zero_model_selector_information,
 "source_boundary":"The frozen census includes torus localization Q_points, field family kind and allowed triangles; it does NOT identify projective W33 p for each local model, nor a map from cusp lines to modulus-dependent Yukawa operators. Claiming a 491-model physical 4:36 selection directly from current columns would fabricate data.",
 "proof":"W(3,3) collinearity defines maximal isotropic lines. For fixed projective p, p lies on 4 lines; each nonincident totally isotropic 2-plane L intersects p^perp in exactly one projective point because p^perp has dim3 and L dim2 but L not fully contained in p^perp. All 40 points lie in one Sp4(3) orbit."}
(ROOT/"data/w33_20261010_toe46_census_selector_firewall.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:out[k] for k in ("status","zero_model_discrimination_from_unlabelled_incidence")}|{"census":{k:out["census"][k] for k in ("records","kinds","twisted_local_10","down_non_single_point_models")}}))
