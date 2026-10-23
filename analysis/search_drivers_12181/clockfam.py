"""12181 (WSL): clock Witten shifts V0 = (alpha/2; beta/2) on the other W(3,3) families (Z6-I, Z3xZ3, Z12-I bases of Pass 11100).
Theorem tested: the zero-winding Witten-sector state p = V0 (p^2 = 1) is kept by every admissible shift and Wilson line, so every
clock-V0 model is tachyonic.  Per family: up to NB bases, the first loadable clock V0, its orbifold-point tachyons, and nsoscan
with TRIES random Wilson lines.  usage: python3 clockfam.py FAMILY NB TRIES OUTJSON"""
import json, os, re, subprocess, sys
from fractions import Fraction as F
sys.path.insert(0, '/mnt/c/tmp/toe_wt/analysis/orbifolder_n0_drivers')
os.environ['LD_LIBRARY_PATH'] = '/tmp/su9/lib:' + os.path.expanduser('~/orb/sysroot/usr/lib/x86_64-linux-gnu')
import so16_bases as SB

FAM, NB, TRIES, OUTJ = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
ROOTS = SB.e8_norm(2)
HALFR = [tuple(x / 2 for x in r) for r in ROOTS]
OUT = os.path.expanduser('~/orb/p1109x/clockfam'); os.makedirs(OUT, exist_ok=True)
bases, geom = SB.read_bases(FAM)
res = {}
for label, shifts in bases[:NB]:
    rec = None
    for a in HALFR:
        for b in HALFR:
            V0 = a + b
            if any(SB.dot(V0, s).denominator != 1 for s in shifts):
                continue
            rows = [list(V0)] + [s for s in shifts] + [[F(0)] * 16] * (2 - len(shifts)) + [[F(0)] * 16] * 6
            path = f'{OUT}/{FAM}_{label}.txt'
            open(path, 'w').write(SB.model_text(f'{FAM}_{label}', geom, rows))
            g, t = SB.loads(path)
            if not g:
                continue
            rec = dict(V0=SB.fmt(V0), gauge=g, tachyons=t)
            r = subprocess.run(['./nsoscan', path, str(TRIES), '5', path[:-4]], cwd=os.path.expanduser('~/orb/nsobuild'),
                               capture_output=True, text=True, timeout=7200)
            last = [l for l in r.stdout.splitlines() if l.startswith('tries')]
            m = re.search(r'ok (\d+) tachyon-free (\d+) SM (\d+) \(ineq (\d+)\) SM&tachyon-free (\d+) problems (\d+)', last[-1]) if last else None
            if m:
                rec.update(ok=int(m.group(1)), tachyon_free=int(m.group(2)), SM=int(m.group(3)))
            break
        if rec:
            break
    res[label] = rec
    print(FAM, label, rec, flush=True)
    json.dump(res, open(OUTJ, 'w'), indent=1)
print('DONE')
