"""12199 (WSL) [adapted from 12180 ss_z6ii.py to Z2xZ6-I: rows V0, V_Z2, V_Z6, W3, W4, W1, W2, W5, W6 (planes 1<->2 of the
non-SUSY geometry Z2xZ6-I_1_1); paired sectors = odd Z2 power (nsodump n)].  Original header:
12180 (WSL): Scherk-Schwarz interpolation of the 128 Z6-II W(3,3) Standard Models (~/orb/scan/sm) to SO(16)^2.
Large-radius massless spectrum of the interpolating model = the Witten-UNTWISTED fields (k=0) of the non-free Z2W x Z6-II
model with the same split V0, in the sectors that leave plane 3 unrotated (Z6 power m in {0,2,4}); the sectors m odd rotate
plane 3, the translation t = e6/2 pairs their fixed points freely and they contribute n_B = n_F.  V0 = (a; b), a, b in
(1/2){norm-4 E8 vectors}, V0.V and V0.W_i integral, W6 = 0 (t = e6/2 carries no Wilson line).
usage: python3 ss_z6ii.py NMODELS NV0 OUTJSON"""
import json, os, re, subprocess, sys
from fractions import Fraction as F
sys.path.insert(0, '/mnt/c/tmp/toe_wt/analysis/orbifolder_n0_drivers')
os.environ['LD_LIBRARY_PATH'] = '/tmp/su9/lib:' + os.path.expanduser('~/orb/sysroot/usr/lib/x86_64-linux-gnu')
import so16_bases as SB

NM, NV, OUTJ = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
START, STEP = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 1)
OUT = os.path.expanduser('~/orb/p1109x/ssz2z6'); os.makedirs(OUT, exist_ok=True)
models = []
for f in sorted(os.listdir(os.path.expanduser('~/orb/scan/z2z6/sm'))):
    t = open(os.path.expanduser('~/orb/scan/z2z6/sm/' + f)).read()
    for blk in t.split('begin model')[1:]:
        lab = re.search(r'Label:(\S+)', blk).group(1)
        rows = blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().splitlines()
        rows = [[F(x.strip(',')) for x in r.replace(',', ' ').split()] for r in rows]
        models.append((f[:-4] + '_' + lab, rows))
print('models', len(models), flush=True)
dot = lambda u, v: sum(a * b for a, b in zip(u, v))
res = {}
def in_e8(v):
    return (all(x.denominator == 1 for x in v) or all(x.denominator == 2 for x in v)) and sum(v) % 2 == 0
def triv(w):
    return in_e8(w[:8]) and in_e8(w[8:])
def ok(rows):
    W1, W2 = rows[2], rows[3]
    return triv(W1) or triv(W2) or triv([a + b for a, b in zip(W1, W2)])
for lab, rows in [m for m in models if ok(m[1])][:NM][START::STEP]:
    V, W = rows[0], rows[2:8]
    VZ6 = rows[1]
    rec = dict(v0=[])
    shifts = [V, VZ6] + W
    got = 0
    for V0 in SB.candidates(shifts, limit=400):
        if any(dot(V0, s).denominator != 1 for s in shifts):
            continue
        nrows = [list(V0), V, VZ6, W[2], W[3], W[0], W[1], W[4], W[5]]
        path = f'{OUT}/{lab}_v{got}.txt'
        open(path, 'w').write(SB.model_text(f'{lab}_v{got}', 'Geometry_Z2xZ6-I_1_1.txt', nrows))
        d = subprocess.run(['./nsodump', path], cwd=os.path.expanduser('~/orb/nsobuild'), capture_output=True, text=True, timeout=1800).stdout
        if 'LOADFAIL' in d or 'GAUGE' not in d:
            continue
        cnt = {}
        for l in d.splitlines():
            m = re.match(r'F m=(\d+) k=(\d+) m=(\d+) n=(\d+) dim=(\S+) x(\d+)', l)
            if m:
                mult, k, zm, zn = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
                dim = 1
                for x in m.group(5).split(','):
                    dim *= abs(int(re.match(r'-?\d+', x).group(0)))
                key = f'mult{mult}_w{zm}_n{zn}'
                cnt[key] = cnt.get(key, 0) + dim * int(m.group(6))
        g = re.search(r'GAUGE (.*)', d).group(1).strip()
        t = re.search(r'T_NFIELDS (\d+)', d)
        nu1 = int(re.search(r'NU1 (\d+)', g).group(1))
        BOS, FER = {8, 9, 13, 14, 15, 16, 17, 18}, {19, 20}
        def tally(pred):
            b = sum(c for kk, c in cnt.items() if int(kk.split('_')[0][4:]) in BOS and pred(int(kk.split('_')[1][1:]), int(kk.split('_')[2][1:])))
            f = sum(c for kk, c in cnt.items() if int(kk.split('_')[0][4:]) in FER and pred(int(kk.split('_')[1][1:]), int(kk.split('_')[2][1:])))
            return b, f
        bs, fs = tally(lambda w, n: w == 0 and n % 2 == 0)
        bo, fo = tally(lambda w, n: w == 0 and n % 2 == 1)
        rec['v0'].append(dict(SS_nB=bs + 2 * nu1, SS_nF=fs, SS_diff=bs + 2 * nu1 - fs, oddsector_nB=bo, oddsector_nF=fo, NU1=nu1, V0=SB.fmt(V0), gauge=g, tachyons=int(t.group(1)) if t else None, counts=cnt))
        print(lab, got, g, t.group(0) if t else None, flush=True)
        got += 1
        if got >= NV:
            break
    res[lab] = rec
    json.dump(res, open(OUTJ, 'w'), indent=1)
print('DONE')
