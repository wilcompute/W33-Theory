import json
from pathlib import Path

data = json.loads(Path('analysis/outer_twist_cocycle/edge_defect.json').read_text(encoding="utf-8"))
print(len(data['rows']))
print(data['rows'][:10])
