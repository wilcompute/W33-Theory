"""12180c: where the parent generations sit.  For every Z6-II W(3,3) SUSY Standard Model (.sp spectra, Pass 10960 archive):
net quark doublets (q minus bq) in even sectors (k = 0, 2, 4) and odd sectors (k = 1, 3, 5).  A Scherk-Schwarz translation on
the order-2 plane halves the odd-sector generations, so three generations at large radius require odd net = 0."""
import json, re, subprocess
from collections import defaultdict
sh = "cd ~/orb/scan/cp2/sp && for f in *.sp; do echo \"FILE $f\"; grep -hE '^S (b?q)_' $f | cut -d' ' -f2-5; done"
o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
res = {}
cur = None
for l in o.splitlines():
    if l.startswith('FILE '):
        cur = l[5:-3]; res[cur] = defaultdict(int); continue
    m = re.match(r'(b?)q_\d+ k=(\d+) susy=\d+ dim=(\S+)', l)
    if m:
        tot = 1
        for x in m.group(3).split(','):
            tot *= abs(int(re.match(r'-?\d+', x).group(0)))
        assert tot % 6 == 0, l
        res[cur]['odd' if int(m.group(2)) % 2 else 'even'] += (-1 if m.group(1) else 1) * tot // 6
res = {k: dict(v) for k, v in res.items()}
print('parents', len(res))
from collections import Counter
print('(even, odd) net quark doublets:', Counter((v.get('even', 0), v.get('odd', 0)) for v in res.values()).most_common())
json.dump(res, open('oddgen.json', 'w'), indent=1)
