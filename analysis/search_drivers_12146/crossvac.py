"""12146: one-loop Lambda (11106 engine, T_WL = 2i, T* = rho) and winding tachyons (11107 enumerator, Im T_WL = 2, 1.75, 1.5)
for the 16 fraction-free single-heavy-top A8 models."""
import sys, json
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, r'C:\tmp\toe_round\stype'); sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import oneloop as O
import w33_so16_one_loop as E
import w33_pass11107_winding_tachyons as T
RHO = 0.5 + 0.8660254037844386j
G = {}


def init(path):
    (V0, V, W), b = O.load_any(path)
    nz = [i for i in (0, 2, 4) if np.any(np.abs(W[i]) > 1e-12)]
    G['wl'] = E.WLPart(V0, [W[nz[0]], W[nz[1]]], [2j, 2j], K=2)
    G['sh'] = E.fixed_point_shifts(V0, V, W)
    G['cos'] = E.cosets(6)


def val(tau):
    return complex(E.Z_beta(tau, G['wl'], RHO)), complex(E.Z_twisted(tau, G['sh'], G['cos'], 1))


if __name__ == '__main__':
    d = json.load(open('a8cross.json'))
    labs = sorted({lab for lab, r in d.items() for x in r if x['up']['rank'] == 1})
    out = {}
    for lab in labs:
        path = r'C:\tmp\toe_round\stype\a8\%s.txt' % lab
        pts = E.grid()
        with Pool(8, initializer=init, initargs=(path,)) as p:
            vals = p.map(val, [q[0] for q in pts], chunksize=4)
        P = [(q[0], q[1], q[1], q[2], q[3]) for q in pts]
        rb = E.fitted(P, [v[0].real for v in vals]); rt = E.fitted(P, [v[1].real for v in vals])
        (V0, V, W), block = O.load_any(path)
        tach = {}
        for im in (2.0, 1.75, 1.5):
            f = T.tachyons(None, [im * 1j, im * 1j], RHO, rows=block)
            tach[str(im)] = dict(n=len(f), Delta=float(f[0]['Delta']) if f else None)
        out[lab] = dict(Lambda_over_M4=-0.5 * (rb['I'] + rt['I']), I_beta=rb['I'], I_tw=rt['I'], c_top=rb['c_top'], tachyons=tach)
        print(lab, round(out[lab]['Lambda_over_M4'], 2), tach, flush=True)
        json.dump(out, open('crossvac.json', 'w'), indent=1)
    print('DONE')
