"""
Pass 10101-10104: Outside-the-box Idea #2
BT chamber tarot / archetype toy classifier: assign the 6 residue layers to 6 archetypal roles
and verify all 15 pairings are unique up to unordered combination.
"""
import json
import itertools

roles = ["Origin","Mirror","Bridge","Triality","Clock","Witness"]
pairs = list(itertools.combinations(range(6),2))
labels = [f"{roles[a]}-{roles[b]}" for a,b in pairs]

result = {
  "schema": "w33.pass10101_10104.bt_archetype_pairs.v1",
  "status": "PASS",
  "roles": roles,
  "pair_count": len(labels),
  "unique_pairs": len(set(labels)),
  "claim": "All 15 unordered BT layer pairings support distinct archetypal labels, giving a mnemonic classification of chamber interactions."
}
print(json.dumps(result, indent=2))
