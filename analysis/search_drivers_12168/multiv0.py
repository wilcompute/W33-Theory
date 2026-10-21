"""12172 (run in WSL): Pass 11100 used ONE Witten shift V0 per W(3,3) base. Here: up to NV loadable V0 per Z6-I base (same admissibility
and candidate order as so16_bases.py), each scanned with nsoscan (random Wilson lines, the non-SUSY orbifolder's tachyon and SM tests).
usage: python3 multiv0.py NV TRIES OUTJSON"""
import os
import re
import sys
import json
import subprocess
sys.path.insert(0, '/mnt/c/tmp/toe_wt/analysis/orbifolder_n0_drivers')
os.environ['LD_LIBRARY_PATH'] = '/tmp/su9/lib:' + os.path.expanduser('~/orb/sysroot/usr/lib/x86_64-linux-gnu')
import so16_bases as SB

NV, TRIES, OUTJ = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
OUT = os.path.expanduser('~/orb/p1109x/multiv0')
os.makedirs(OUT, exist_ok=True)
bases, geom = SB.read_bases('Z6-I')
res = {}
for label, shifts in bases:
    got = []
    for V0 in SB.candidates(shifts, limit=60):
        rows = [list(V0)] + [s for s in shifts] + [[SB.F(0)] * 16] * (2 - len(shifts)) + [[SB.F(0)] * 16] * 6
        path = f'{OUT}/Z6I_{label}_v{len(got)}.txt'
        open(path, 'w').write(SB.model_text(f'Z6I_{label}_v{len(got)}', geom, rows))
        g, t = SB.loads(path)
        if not g:
            continue
        r = subprocess.run(['./nsoscan', path, str(TRIES), str(7 + len(got)), path[:-4]], cwd=os.path.expanduser('~/orb/nsobuild'),
                           capture_output=True, text=True, timeout=7200)
        last = [l for l in r.stdout.splitlines() if l.startswith('tries')]
        m = re.search(r'ok (\d+) tachyon-free (\d+) SM (\d+) \(ineq (\d+)\) SM&tachyon-free (\d+) problems (\d+)', last[-1]) if last else None
        rec = dict(V0=SB.fmt(V0), gauge=g, base_tachyons=t)
        if m:
            rec.update(ok=int(m.group(1)), tachyon_free=int(m.group(2)), SM=int(m.group(3)), SM_tf=int(m.group(5)), problems=int(m.group(6)))
        got.append(rec)
        print(label, len(got), rec, flush=True)
        if len(got) >= NV:
            break
    res[label] = got
    json.dump(res, open(OUTJ, 'w'), indent=1)
print('DONE')
