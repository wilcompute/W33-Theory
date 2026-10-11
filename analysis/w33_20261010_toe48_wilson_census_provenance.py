"""TOE48: exhaustive 491-model gauge-holonomy provenance and Pauli lift impossibility.
The current frozen census has no model-specific W33 Pauli matrices.
"""
from pathlib import Path
import json,itertools,collections,math
import numpy as np
R=Path(__file__).resolve().parents[1]
a=json.loads((R/"data/w33_pass11903_census491_frozen.json").read_text())
b=json.loads((R/"data/w33_pass11903_local_ten_locks_charm_up.json").read_text())
assert len(a)==491 and b["all_checks_pass"]
types=collections.Counter(x["kind"] for x in a.values())
assert types=={"untwisted":339,"twisted_one_torus":152}
allkeys=set().union(*(set(x.keys()) for x in a.values()))
provenance_fields=("pauli_vector","weyl_operator","gauge_holonomy_matrix","wilson_matrix",
"wilson_embedding","wilson_vectors","gauge_shift_16","shift_vector","modular_invariant_shift")
assert all(k not in allkeys for k in provenance_fields)
labels=sorted(a.keys()); assert len(labels)==len(set(labels))
twisted=[x for x in a.values() if x["kind"]=="twisted_one_torus"]
assert len(twisted)==152
assert all(x["U_same"] and x["E_same"] for x in twisted)
assert all(x["up_wilson_patterns"] in ([],[[0,0]]) for x in twisted)
down=sorted(x["label"] for x in twisted if any(any(z) for z in x["down_wilson_patterns"]))
assert down==sorted(b["down_escape_capable"])
# Equal incidence fingerprint for ALL 40 Wilson point labels, so geometry
# alone yields identical graph summary no matter how assigned to models.
canon=lambda v:min(v,tuple(-int(u)%3 for u in v))
pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
sp=lambda p,q:(p[0]*q[2]+p[1]*q[3]-p[2]*q[0]-p[3]*q[1])%3
index={v:i for i,v in enumerate(pts)}
lines=set()
for i,p in enumerate(pts):
 for q in pts[i+1:]:
  if sp(p,q):continue
  lines.add(tuple(sorted({index[canon(tuple((r*p[k]+s*q[k])%3 for k in range(4)))] for r,s in itertools.product(range(3),repeat=2) if r or s})))
lines=sorted(lines)
patterns={str(j):[sum(j in L for L in lines),sum(j not in L for L in lines)] for j in range(40)}
assert set(map(tuple,patterns.values()))=={(4,36)}
# All lifts p across all 491 records are indistinguishable from count alone.
candidate_assignments=len(a)*len(pts)
sourcepath=R/"data/w33_pass11714_orbifolder_frozen_states.json"
modelsource=json.loads(sourcepath.read_text())
assert "models" in modelsource
out={"status":"491_MODEL_PHYSICAL_WILSON_EMBEDDING_NOT_RECOVERABLE_FROM_FROZEN_INPUTS",
"census_records":len(a),"categories":dict(types),"observed_record_fields":sorted(allkeys),
"absent_required_gauge_holonomy_fields":list(provenance_fields),
"twisted_local_ten":152,"up_escape_capable_recorded":len(b["up_escape_capable"]),
"five_down_escape_labels":down,
"geometric_candidate_w33_point_labels":len(pts),
"indistinguishable_combinatorial_model_point_assignments":candidate_assignments,
"unlabelled_selector_incidence_for_each_candidate":[4,36],
"maximum_unlabelled_geometry_discrimination_bits":0,
"minimum_pauli_point_address_bits_if_missing":math.log2(40),
"orbifolder_other_archive_source":modelsource["source"],
"orbifolder_other_archive_different_model_family":True,
"proof":"For all 40 symplectic Pauli points the number of incident W33 lines is four. The per-model frozen data list Z3 torus positions and Yukawa localization types, NOT a gauge-space Wilson matrix or a map of its actual representation to a 9D Pauli unitary. The 491x40 candidate assignments produce identical unlabelled 4:36 counts. The separate older Z6-I orbifolder archive is not an identifier-preserving matrix dump for this 491-model class.",
"boundary":"This is a PROVENANCE/identifiability obstruction for currently accessible frozen certificates, NOT proof the original orbifolder source data can never be retrieved. No physical model-specific Wilson charges or SM Yukawa predictions have been fabricated."}
(R/"data/w33_20261010_toe48_wilson_census_provenance.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:out[k] for k in ["status","census_records","indistinguishable_combinatorial_model_point_assignments","maximum_unlabelled_geometry_discrimination_bits"]}))
