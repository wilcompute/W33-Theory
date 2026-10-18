"""Pass 12047 driver: heavy-row Clebsch scan. Lepton row b_e = kappa * b (b = the 12045 theta-vector row), lepton
matching K_e = 1 - b_e^dag b_e/(1+|b_e|^2), M_e = A_e^T e_bare^T (12007 convention). For every 12045 branch and every
recorded matching scale (12046 scale records, SM running) compute the parameter-free charged-lepton ratios.
"""
import glob
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ANA = os.path.dirname(HERE)
for p in (ANA, os.path.join(ANA, 'search_drivers_12045')):
    sys.path.insert(0, p)
import barrfit as B  # noqa: E402
from w33_pass11942_hypercharge_wilson_leptons import LEPTONS, normalised  # noqa: E402

KAPPAS = {'singlet 1': 1.0, 'adjoint mass 2/3': 2 / 3, 'adjoint row 3/2': 1.5, 'B-L row 3': 3.0, 'B-L mass 1/3': 1 / 3,
          'control 2': 2.0, 'control 1/2': 0.5}


def leptons_kappa(x, kappa):
    Od = np.array([[B.TAU, 1j * x[1]], [1j * x[1], 1j * np.exp(x[0])]])
    d = B.PH.conj()[:, None] * normalised(Od, (0, 1j * x[2]))
    e = (B.PH.conj()[:, None] * normalised(Od, (0, 6j * x[2]))).real / np.linalg.norm(d)
    b = kappa * B.brow(x, 'shared')
    K = np.eye(3) - np.outer(b.conj(), b) / (1 + np.vdot(b, b).real)
    ev, O = np.linalg.eigh(K)
    A = (O * np.sqrt(np.clip(ev, 0, None))) @ O.conj().T
    s = np.linalg.svd(A.T @ e.T, compute_uv=False)
    return s[1] / s[0], s[2] / s[1]


if __name__ == '__main__':
    L = np.array([LEPTONS['mmu_mtau'], LEPTONS['me_mmu']])
    out = []
    for f in sorted(glob.glob(os.path.join(ANA, 'search_drivers_12046', 'scale_*.json'))):
        d = json.load(open(f))
        for row in d['rows']:
            x = np.array(row['x'])
            for name, k in KAPPAS.items():
                a, b = leptons_kappa(x, k)
                dev = np.log(np.array([a, b]) / L)
                out.append(dict(branch=d['branch'], mu=row['mu'], kappa=name, mmu_mtau=float(a), me_mmu=float(b),
                                dev=dev.tolist(), comb_dev=float(dev[1] + 2 * dev[0])))
    json.dump(out, open(os.path.join(HERE, 'kappa_scan.json'), 'w'), indent=1)
    good = [o for o in out if max(abs(v) for v in o['dev']) < 0.15]
    print('entries', len(out), ' within 15% on BOTH ratios:', len(good))
    for o in sorted(out, key=lambda o: max(abs(v) for v in o['dev']))[:15]:
        print('%s  mu=%.3g  %-18s  m_mu/m_tau %.5f  m_e/m_mu %.6f  dev(ln) %+.3f %+.3f  comb %+.3f' % (
            o['branch'], o['mu'], o['kappa'], o['mmu_mtau'], o['me_mmu'], o['dev'][0], o['dev'][1], o['comb_dev']))
