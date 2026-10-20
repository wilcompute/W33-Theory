"""12130: full one-loop vacuum energy (Pass 11106 engine) for a Z2W x Z3 model; control = 11106 model 2 at T_WL = 2i, T* = rho."""
import sys
import json
import time
import numpy as np
from fractions import Fraction as Fr
from multiprocessing import Pool

sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import w33_so16_one_loop as E

RHO = 0.5 + 0.8660254037844386j


def load(which):
    if which == 'model2':
        d = json.load(open(r'C:\tmp\toe_wt\data\w33_pass11106_survivor_shifts.json'))['models']['2']
        return E.parse_model(d['rows'])
    path = which
    rows = open(path).read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    rows = [r.strip() for r in rows]
    block = [','.join(r.split()) for r in [rows[0], rows[1]] + rows[3:9]]
    return E.parse_model(block)


def setup(which, Tw, Ts):
    V0, V, W = load(which)
    nz = [i for i in (0, 2, 4) if np.any(np.abs(W[i]) > 1e-12)]
    assert len(nz) <= 2, nz
    while len(nz) < 2:
        nz.append([i for i in (0, 2, 4) if i not in nz][0])
    wl = E.WLPart(V0, [W[nz[0]], W[nz[1]]], [Tw, Tw], K=2)
    sh = E.fixed_point_shifts(V0, V, W)
    cos = E.cosets(6)
    return wl, sh, cos, Ts


G = {}


def init(which, Tw, Ts):
    G['s'] = setup(which, Tw, Ts)


def val(tau):
    wl, sh, cos, Ts = G['s']
    zb = E.Z_beta(tau, wl, Ts)
    zt = E.Z_twisted(tau, sh, cos, 1)
    return complex(zb), complex(zt)


if __name__ == '__main__':
    which = sys.argv[1]
    Tw = complex(sys.argv[2]) if len(sys.argv) > 2 else 2j
    Ts = RHO
    pts = E.grid()
    if len(sys.argv) > 3 and sys.argv[3] == 'time':
        init(which, Tw, Ts)
        t0 = time.time()
        print(val(pts[0][0]), val(pts[-1][0]), 'sec/pt', (time.time() - t0) / 2)
        sys.exit()
    with Pool(int(sys.argv[4]) if len(sys.argv) > 4 else 8, initializer=init, initargs=(which, Tw, Ts)) as p:
        vals = p.map(val, [q[0] for q in pts], chunksize=4)
    P = [(q[0], q[1], q[1], q[2], q[3]) for q in pts]
    rb = E.fitted(P, [v[0].real for v in vals])
    rt = E.fitted(P, [v[1].real for v in vals])
    I = rb['I'] + rt['I']
    out = dict(model=which, T_WL=str(Tw), T_star=str(Ts), I_beta=rb, I_twisted=rt, I_total=I, Lambda_over_M4=-0.5 * I,
               imag_max=max(abs(v[0].imag) + abs(v[1].imag) for v in vals))
    tag = 'model2' if which == 'model2' else which.split('\\')[-1].split('/')[-1][:-4]
    json.dump(out, open(r'C:\tmp\toe_round\stype\oneloop_%s_%s.json' % (tag, str(Tw).strip('()')), 'w'), indent=1, default=str)
    print(tag, 'I_beta', rb['I'], 'I_tw', rt['I'], 'Lambda/M4', -0.5 * I, 'imag', out['imag_max'])
