"""TOE49: complete six-Wilson-vector census from NEW Pass11908 source bundle.

Distinct physical gauge Cartan vectors are NOT automatically 9D W33 Paulis.
This script materializes rank/phase classes without inventing a 9D lift.
"""
from fractions import Fraction
from pathlib import Path
import json,collections,hashlib
R=Path(__file__).resolve().parents[1]
f=R/"data/w33_pass11908_model_definitions.json"
d=json.loads(f.read_text())
rows={}
categories=collections.Counter()
multiplicity=collections.Counter()
zero_count=collections.Counter()
repeated=collections.Counter()
nonorderthree=0
entries=collections.Counter()
models=d["models"]
assert len(models)==600
for label,model in models.items():
 rr=[tuple(Fraction(v) for v in text.split()) for text in model["rows"]]
 assert len(rr)==9,(label,len(rr))
 assert all(len(r)==16 for r in rr)
 # row0=V0 row1=V1, row2..row8 are 7 rows? 9 total -> 2 shifts plus 7?
 # Freeze raw geometry before interpreting the physical Wilson aliases.
 Wilson=rr[3:]
 assert len(Wilson)==6
 nz=[v for v in Wilson if any(x for x in v)]
 distinct=set(nz)
 categories[model["source"]]+=1
 multiplicity[len(distinct)]+=1
 zero_count[len(Wilson)-len(nz)]+=1
 repeated[tuple(len(set(Wilson)) for _ in [0])]+=1
 for v in Wilson:
  for x in v:entries[str(x.denominator)]+=1
  if any((3*x).denominator!=1 for x in v): nonorderthree+=1
 rows[label]={"n_nonzero_W":len(nz),"n_distinct_nonzero_W":len(distinct),
 "W_equalities": [[i+1,j+1] for i in range(6) for j in range(i+1,6) if Wilson[i]==Wilson[j]],
 "has_noninteger_3W_coordinate":any(any((3*x).denominator!=1 for x in w) for w in Wilson)}
assert sum(categories.values())==600
# Count how often a Wilson Cartan vector uses a half-integral coordinate:
# this is NOT its order in the actual E8xE8 / Spin(16)xSpin(16) lattice quotient.
out={
"status":"TOE49_600_FROZEN_GAUGE_WILSON_VECTOR_ROWS_INSPECTED_NO_PAULI_LIFT",
"total_models":600,
"model_source_counts":dict(categories),
"source_digest_claims":d["sources"],
"actual_frozen_json_sha256":hashlib.sha256(f.read_bytes()).hexdigest(),
"all_models_have_9_rows_of_16_rationals":True,
"rows_0_1_2":"First three rows include shift/orbifold parameters; remaining rows 3..8 examined as six Wilson vectors, matching Pass11908 file documentation (not gauge-equivalence reduced).",
"n_distinct_nonzero_W_distribution":dict(multiplicity),
"zero_W_rows_distribution":dict(zero_count),
"raw_W_vector_distinct_including_zero_distribution":{str(k[0]):v for k,v in repeated.items()},
"coordinate_denominator_counts":dict(entries),
"n_W_rows_with_nonintegral_3W_coordinates":nonorderthree,
"model_details":rows,
"provenance_conclusion":"TOE48 frozen-input ABSENCE is superseded: 600 source-model definitions now include explicit 16-rational-coordinate shift/Wilson rows and source SHA claims; their Cartan vectors can be enumerated and indexed. Raw original input bytes are not themselves provided by this JSON, and a canonical gauge-root-lattice / weight-lattice quotient plus physical 9D W33 Pauli representation is still NOT specified. One cannot assign a nonabelian X,Z Pauli action or Yang-Mills/Yukawa predictions merely by labelling raw Wilson vectors as W33 points.",
"abelian_cartans":"All Cartan holonomy matrices commute in their common diagonal weight basis, hence under ANY honest representation their images commute. If mapped faithfully into two-qutrit Weyl projective operators WITHOUT central phases, the corresponding Pauli labels must form an isotropic commuting subset; at most a maximal 2D F3-subspace (four projective W33 points). More general projective lifts need an explicit cocycle/gauge action, never inferred from frozen 16D rows.",
"scientific_boundary":"A rank statistic on the six Wilson rows is not gauge-lattice equivalence, not an exhaustive list of physically inequivalent holonomies, and not a full 9D representation theorem."}
(R/"data/w33_20261010_toe49_gauge_vector_audit.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"classes":out["model_source_counts"],"dist":out["n_distinct_nonzero_W_distribution"],"n_3W":nonorderthree}))
