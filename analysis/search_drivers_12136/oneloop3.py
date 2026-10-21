"""12137 driver: full one-loop Lambda for a model with three Wilson-line tori (T115) using wl3.WLPartN."""
import sys
import json
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, r'C:\tmp\toe_round\stype')
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import oneloop as O
import w33_so16_one_loop as E
import wl3

G = {}


def init(path, Tw):
    V0, V, W = O.load(path)
    G['wl'] = wl3.WLPartN(V0, [W[0], W[2], W[4]], Tw, K=2)
    G['sh'] = E.fixed_point_shifts(V0, V, W)
    G['cos'] = E.cosets(6)


def val(tau):
    return complex(wl3.Z_betaN(tau, G['wl'])), complex(E.Z_twisted(tau, G['sh'], G['cos'], 1))


if __name__ == '__main__':
    path = sys.argv[1]
    Tw = [complex(x) for x in sys.argv[2].split(',')]
    if sys.argv[3] == 'check':
        init(path, Tw)
        t = 0.05 + 1.0j
        zb = wl3.Z_betaN(t, G['wl'])
        zt = E.Z_twisted(t, G['sh'], G['cos'], 1)
        b0 = E.seed_block(0.11 + 1.05j, G['sh'][0], 1)
        g16 = max(abs(E.seed_block(E.act(g, 0.11 + 1.05j), G['sh'][0], 1) / b0 - 1) for g in [(1, 0, 6, 1), (7, 1, 6, 1), (13, 2, 6, 1)])
        r = dict(beta_S=abs(wl3.Z_betaN(-1 / t, G['wl']) / zb - 1), beta_T=abs(wl3.Z_betaN(t + 1, G['wl']) / zb - 1),
                 twisted_S=abs(E.Z_twisted(-1 / t, G['sh'], G['cos'], 1) / zt - 1), twisted_T=abs(E.Z_twisted(t + 1, G['sh'], G['cos'], 1) / zt - 1),
                 gamma1_6=g16)
        print(r)
        json.dump({k: float(v) for k, v in r.items()}, open(r'C:\tmp\toe_round\stype\oneloop3_T115_modcheck.json', 'w'), indent=1)
        sys.exit()
    pts = E.grid()
    with Pool(int(sys.argv[4]), initializer=init, initargs=(path, Tw)) as p:
        vals = p.map(val, [q[0] for q in pts], chunksize=2)
    P = [(q[0], q[1], q[1], q[2], q[3]) for q in pts]
    rb = E.fitted(P, [v[0].real for v in vals])
    rt = E.fitted(P, [v[1].real for v in vals])
    I = rb['I'] + rt['I']
    out = dict(T_WL=[str(x) for x in Tw], I_beta=rb, I_twisted=rt, I_total=I, Lambda_over_M4=-0.5 * I)
    json.dump(out, open(r'C:\tmp\toe_round\stype\oneloop3_T115_%s.json' % sys.argv[2].replace(',', '_'), 'w'), indent=1, default=str)
    print('T115', Tw, 'I_beta', rb['I'], 'I_tw', rt['I'], 'Lambda/M4', -0.5 * I)
