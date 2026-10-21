"""12151: one-loop Lambda (11106 engine) and the lowest Witten-sector level (11107 enumerator) along the imaginary Wilson-line axis
for the two vetted candidates."""
import sys, json, math
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, r'C:\tmp\toe_round\stype'); sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import oneloop as O
import w33_so16_one_loop as E
import marginal as Mg
RHO = 0.5 + 0.8660254037844386j
G = {}


def init(path, tw, K):
    (V0, V, W), b = O.load_any(path)
    nz = [i for i in (0, 2, 4) if np.any(np.abs(W[i]) > 1e-12)]
    G['wl'] = E.WLPart(V0, [W[nz[0]], W[nz[1]]], [tw, tw], K=K)
    G['sh'] = E.fixed_point_shifts(V0, V, W)
    G['cos'] = E.cosets(6)


def val(tau):
    return complex(E.Z_beta(tau, G['wl'], RHO)), complex(E.Z_twisted(tau, G['sh'], G['cos'], 1))


if __name__ == '__main__':
    out = {}
    for lab in ['A8SM_20260928_16222_TF']:
        path = r'C:\tmp\toe_round\stype\a8\%s.txt' % lab
        (V0, V, W), block = O.load_any(path)
        out[lab] = {}
        for im in (1.5, 1.0, 0.8):
            K = 2 if im >= 0.8 else 4
            pts = E.grid()
            with Pool(7, initializer=init, initargs=(path, im * 1j, K)) as p:
                vals = p.map(val, [q[0] for q in pts], chunksize=4)
            P = [(q[0], q[1], q[1], q[2], q[3]) for q in pts]
            rb = E.fitted(P, [v[0].real for v in vals]); rt = E.fitted(P, [v[1].real for v in vals])
            f = Mg.levels(block, [im * 1j, im * 1j], RHO, cut=0.2)
            ds = sorted(s['Delta'] for s in f)
            out[lab]['%.6f' % im] = dict(Lambda=-0.5 * (rb['I'] + rt['I']), c_top=rb['c_top'], lowest=float(ds[0]) if ds else None,
                                         mult=sum(1 for d in ds if ds and abs(d - ds[0]) < 1e-9))
            print(lab, '%.4f' % im, out[lab]['%.6f' % im], flush=True)
            json.dump(out, open('candaxis_16222.json', 'w'), indent=1)
    print('DONE')
