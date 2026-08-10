import json
from pathlib import Path

internal_to_edge=json.loads(Path('internal_to_edge_labeling.json').read_text(encoding="utf-8"))
# invert to edge->internal
edge_to_internal={int(v):int(k) for k,v in internal_to_edge.items()}
adj=[int(x) for x in open('W33_adjacency_matrix.txt').read().split()] # not good
# fix: read matrix differently
data=[l.strip() for l in open('W33_adjacency_matrix.txt') if l.strip()]
adjmat=[[int(x) for x in line.split()] for line in data]
neighbors0=[i for i,v in enumerate(adjmat[0]) if v==1]
print('neighbors0',neighbors0)
print('mapped via edge->internal', [edge_to_internal[n] for n in neighbors0])
# edge_to_root neighbors now
edge_to_root=json.loads(Path('artifacts/edge_to_e8_root.json').read_text(encoding="utf-8"))
near=[int(k.strip()[1:-1].split(',')[1]) for k in edge_to_root if k.startswith('(0,')]
print('edge_to_root neighbors0',sorted(near))
