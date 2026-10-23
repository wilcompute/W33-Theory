"""12213: family-triplet quark multiplets across the 128 Z6-II W(3,3) Standard Models (one q line carrying three generations,
dimension 18) vs the generation placement (12200) and the existence of a translation-symmetric direction (12205)."""
import json, re, subprocess
from collections import Counter
sh = "cd ~/orb/scan/cp2/sp && for f in *.sp; do echo \"FILE $f\"; grep -hE '^S b?q_' $f | cut -d' ' -f2-5; done"
o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
trip, cur = {}, None
for l in o.splitlines():
    if l.startswith('FILE '):
        cur = l[5:-3]; trip[cur] = []; continue
    m = re.match(r'(b?)q_\d+ k=(\d+) susy=\d+ dim=(\S+)', l)
    if m:
        tot = 1
        for x in m.group(3).split(','):
            tot *= abs(int(re.match(r'-?\d+', x).group(0)))
        if tot // 6 > 1:
            trip[cur].append(dict(k=int(m.group(2)), mult=tot // 6, anti=bool(m.group(1))))
au = json.load(open('../search_drivers_12205/audit.json'))
rows = []
for k, t in trip.items():
    a = au[k]
    rows.append(dict(parent=k, family_multiplets=t, even=a['even'], odd=a['odd'], symmetric_direction=bool(a['refined_dirs'])))
withT = [r for r in rows if r['family_multiplets']]
print('parents with a multi-generation q multiplet:', len(withT))
for r in withT:
    print(r)
print('N_even = 3 parents:', [r['parent'] for r in rows if r['even'] == 3])
json.dump(rows, open('triplets.json', 'w'), indent=1)
