"""12137: the Pass 11107 winding-tachyon enumerator generalised to three Wilson-line tori (no free torus).
Control: S002 with its free torus as a third torus with W = 0 reproduces the two-torus enumerator."""
import sys
import json
import itertools
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import w33_pass11107_winding_tachyons as T
import w33_so16_one_loop as E
import oneloop as O

RHO = 0.5 + 0.8660254037844386j


def tachyons3(V0, Wt, Tw, Nrange=3):
    found = []
    nt = len(Wt)
    rng = [range(-Nrange, Nrange + 1) if np.any(Wt[i] != 0) else range(0, 1) for i in range(nt)]
    for N in itertools.product(*rng):
        w = V0 + sum(N[i] * Wt[i] for i in range(nt))
        A = [T.e8_near(w[:8], 2.0), T.e8_near(w[8:], 2.0)]
        for x1 in A[0]:
            for x2 in A[1]:
                pi = np.concatenate([x1, x2])
                l = pi + w
                l2 = l @ l
                if l2 >= 2 - 1e-9:
                    continue
                if abs(np.exp(2j * np.pi * (pi @ V0 + V0 @ V0)) + 1) > 1e-6:
                    continue
                pp = pi + V0
                tabs = []
                for i in range(nt):
                    o = (pp @ Wt[i] + 0.5 * Wt[i] @ sum(N[m] * Wt[m] for m in range(nt))) % 1.0
                    tabs.append(T.torus_table(Tw[i], np.array([o, o]), N[i] if np.any(Wt[i] != 0) else None))
                target = round(1 - l2, 6)
                best = None
                for k1, (r1, _) in tabs[0].items():
                    for k2, (r2, _) in tabs[1].items():
                        k3 = round(target - k1 - k2, 6)
                        if k3 in tabs[2]:
                            tot = r1 + r2 + tabs[2][k3][0]
                            if tot < 1 - 1e-9 and (best is None or tot < best):
                                best = tot
                if best is not None:
                    found.append(-0.5 + best / 2)
    return sorted(found)


if __name__ == '__main__':
    out = {}
    V0, V, W = O.load(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt')
    # control: S002, free torus as W = 0 (any winding, N range collapses to one value)
    c = tachyons3(V0, [W[0], W[2], W[4]], [RHO, RHO, RHO], Nrange=3)
    out['control_S002_rho'] = dict(n=len(c), Delta=c[0] if c else None)
    c2 = tachyons3(V0, [W[0], W[2], W[4]], [2j, 2j, RHO], Nrange=3)
    out['control_S002_2i'] = len(c2)
    print(out, flush=True)
    V0, V, W = O.load(r'C:\tmp\toe_wt\analysis\search_drivers_12121\smwl3\N008_F1_04_S037_T115.txt')
    for name, tw in [('3i', 3j), ('2i', 2j), ('1.5i', 1.5j), ('1.25i', 1.25j), ('i', 1j), ('0.8i', 0.8j), ('rho', RHO)]:
        f = tachyons3(V0, [W[0], W[2], W[4]], [tw, tw, tw], Nrange=3)
        out['T115_' + name] = dict(n=len(f), Delta=f[0] if f else None)
        print(name, out['T115_' + name], flush=True)
        json.dump(out, open(r'C:\tmp\toe_round\stype\tach3.json', 'w'), indent=1)
    print('DONE')
