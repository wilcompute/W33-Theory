import json, pathlib
ROOT=pathlib.Path('c:/Repos/Theory of Everything')
out=json.loads((ROOT/'artifacts'/'outer_twist_rootword_cocycle_defect.json').read_text(encoding="utf-8"))
for entry in out['cycles']:
    print('A2',entry['a2_index'],'rows count',len(entry['rows']))
    if entry['rows']:
        print('first row',entry['rows'][0])
