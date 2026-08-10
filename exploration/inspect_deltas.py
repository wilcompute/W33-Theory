import json, pathlib
ROOT=pathlib.Path('c:/Repos/Theory of Everything')
out=json.loads((ROOT/'artifacts'/'outer_twist_rootword_cocycle_defect.json').read_text(encoding="utf-8"))
for entry in out['cycles']:
    idx=entry['a2_index']
    stats=entry['delta_stats']
    print('A2',idx,'delta_stats',stats)
