"""12146: exotic masses to quartic order in the 16 crossed models (same method as 12133: trilinear with all rules, quartic with
gauge + space group; generic-rank upper bounds, so remaining light pairs are robust)."""
import os
import sys
import json
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, r'C:\tmp\toe_round\stype')
os.environ['EXACT'] = '1'
import exomass4 as X


def task(item):
    lab, yv = item
    rep = X.run(lab, yv, a8=True)
    return lab, dict(classes=rep, light_trilinear=sum(v['need'] - v['rank_trilinear'] for v in rep.values()),
                     light_up_to_quartic=sum(v['need'] - v['rank_up_to_quartic'] for v in rep.values()))


if __name__ == '__main__':
    d = json.load(open(r'C:\tmp\toe_round\stype\a8cross.json'))
    lat = json.load(open(r'C:\tmp\toe_round\stype\latff_a8.json'))
    items = []
    for lab in sorted(json.load(open(r'C:\tmp\toe_round\stype\crossflavor.json'))):
        ys = [y for y in lat[lab]['ys'] if 2 * sum(Fr(x) ** 2 for x in y) == Fr(17, 3)][:4]
        for x, yv in zip(d[lab], ys):
            if x['up']['rank'] == 1:
                items.append((lab, yv))
                break
    out = {}
    with Pool(6) as p:
        for lab, r in p.imap_unordered(task, items):
            out[lab] = r
            print(lab, r['light_trilinear'], '->', r['light_up_to_quartic'], flush=True)
    json.dump(out, open(r'C:\tmp\toe_round\stype\crossexo_hm.json', 'w'), indent=1)
    print('DONE')
