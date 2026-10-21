"""12175b (WSL): CLOCK-type Witten shifts on the W(3,3) A8 Kac base of T6/Z3.  The corpus used only split V0 (P12084).
V0 = (alpha/2; beta/2), alpha, beta roots (V0^2 = 1, the (E7xSU2)^2 parent of Pass 12174), with V0.V1 in Z.  Classes by
4D gauge roots; per class load representatives in the non-SUSY orbifolder (nsodump: gauge, tachyons at the orbifold point)
and scan random Wilson lines with nsoscan (tachyon-free / SM-like).  usage: python3 clockv0.py TRIES OUTJSON"""
import itertools, json, os, re, subprocess, sys
from collections import defaultdict
from fractions import Fraction as F
sys.path.insert(0, '/mnt/c/tmp/toe_wt/analysis/orbifolder_n0_drivers')
os.environ['LD_LIBRARY_PATH'] = '/tmp/su9/lib:' + os.path.expanduser('~/orb/sysroot/usr/lib/x86_64-linux-gnu')
from a8_so16 import ROOTS8, V1a, V1b, dot

TRIES, OUTJ = int(sys.argv[1]), sys.argv[2]
OUT = os.path.expanduser('~/orb/p1109x/clockv0'); os.makedirs(OUT, exist_ok=True)
V1 = V1a + V1b
cls = defaultdict(list)
for a in ROOTS8:
    for b in ROOTS8:
        V0 = tuple(x / 2 for x in a) + tuple(x / 2 for x in b)
        if dot(V0, V1).denominator != 1:
            continue
        kept = [i for i, r in enumerate([r + (0,) * 8 for r in ROOTS8] + [(0,) * 8 + r for r in ROOTS8])
                if dot(r, V0).denominator == 1 and dot(r, V1).denominator == 1]
        cls[len(kept)].append(V0)
print('admissible', sum(len(v) for v in cls.values()), 'classes by #roots', {k: len(v) for k, v in sorted(cls.items())}, flush=True)
fmt = lambda v: ' '.join(str(x) for x in v)
res = {}
for k, lst in sorted(cls.items()):
    got = []
    for j, V0 in enumerate(lst[:: max(1, len(lst) // 4)][:4]):
        rows = [V0, V1] + [(F(0),) * 16] * 7
        path = f'{OUT}/clock_{k}_{j}.txt'
        open(path, 'w').write(f"begin model\nLabel:clock_{k}_{j}\nSpaceGroup:Geometry/Geometry_Z3_1_1.txt\nLattice:E8xE8\nShifts and Wilsonlines:\n"
                              + '\n'.join(fmt(r) for r in rows) + "\nend model\n")
        d = subprocess.run(['./nsodump', path], cwd=os.path.expanduser('~/orb/nsobuild'), capture_output=True, text=True, timeout=900).stdout
        g = [l for l in d.splitlines() if l.startswith('GAUGE')]
        t = [l for l in d.splitlines() if l.startswith('T_NFIELDS')]
        rec = dict(V0=fmt(V0), roots=k, gauge=g[0] if g else None, loadfail='LOADFAIL' in d, tachyons=t[0] if t else None)
        if g and 'LOADFAIL' not in d and TRIES > 0:
            r = subprocess.run(['./nsoscan', path, str(TRIES), str(11 + j), path[:-4]], cwd=os.path.expanduser('~/orb/nsobuild'),
                               capture_output=True, text=True, timeout=7200)
            last = [l for l in r.stdout.splitlines() if l.startswith('tries')]
            m = re.search(r'ok (\d+) tachyon-free (\d+) SM (\d+) \(ineq (\d+)\) SM&tachyon-free (\d+) problems (\d+)', last[-1]) if last else None
            if m:
                rec.update(ok=int(m.group(1)), tachyon_free=int(m.group(2)), SM=int(m.group(3)), SM_tf=int(m.group(5)), problems=int(m.group(6)))
        got.append(rec)
        print(rec, flush=True)
    res[str(k)] = got
    json.dump(res, open(OUTJ, 'w'), indent=1)
print('DONE')
