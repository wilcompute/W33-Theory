import json
import re
import subprocess
from collections import Counter

res = json.load(open(r'C:\tmp\toe_round\stype\nsscan_5.json'))
out = []
for r in res:
    if r['gauge'] == 'LOADFAIL':
        continue
    lab = r['label']
    sh = ('cd ~/orb/buildns && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          'timeout 900 ./nsdump_v2 /mnt/c/tmp/toe_round/stype/nsmodels/%s.txt 2>/dev/null' % lab)
    txt = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    mults = Counter()
    n16 = Counter()
    for m in re.finditer(r'F m=(\d+) dim=([^ ]+) x(\d+)', txt):
        mult, dims, k = int(m.group(1)), m.group(2).split(','), int(m.group(3))
        mults[mult] += k
        if mult == 2:
            for pos, d in enumerate(dims):
                if d in ('16', '-16'):
                    n16[(pos, d)] += k
    net = {pos: n16[(pos, '16')] - n16[(pos, '-16')] for pos in {p for p, _ in n16}}
    out.append(dict(label=lab, gauge=r['gauge'], perfect=r['perfect'], net16_by_position=net, multiplet_codes=dict(mults)))
    print(out[-1], flush=True)
json.dump(out, open(r'C:\tmp\toe_round\stype\nsrecount_5.json', 'w'), indent=1)
