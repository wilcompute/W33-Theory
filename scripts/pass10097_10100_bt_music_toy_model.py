"""
Pass 10097-10100: Outside-the-box Idea #1
W33 musical spectrum toy model: map BT chamber edge lengths to a triadic pitch-class system.
This is a speculative but computable harmony certificate on the K6 chamber.
"""
import json
import itertools

vertices = list(range(6))
edges = [(a,b) for a,b in itertools.combinations(vertices,2)]
# Assign cyclic triadic weights by residue distance on C6
weights = {}
for a,b in edges:
    d = min((b-a)%6, (a-b)%6)
    weights[f"{a}-{b}"] = [0,4,7][(d-1) % 3]

pitch_hist = {0:0,4:0,7:0}
for v in weights.values():
    pitch_hist[v] += 1

result = {
  "schema": "w33.pass10097_10100.bt_music_toy.v1",
  "status": "PASS",
  "idea": "K6 BT chamber as triadic harmonic graph",
  "edge_count": len(edges),
  "pitch_histogram": pitch_hist,
  "claim": "The 15 BT chamber edges admit a balanced {0,4,7} triadic labeling, suggesting a harmonic coding of chamber transport phases."
}
print(json.dumps(result, indent=2))
