"""12137: the Pass 11106 one-loop engine generalised to t Wilson-line tori (t = 3 for T115: no Wilson-line-free torus).
WLPartN.lam is the t-torus version of w33_so16_one_loop.WLPart.lam; Zbeta_blockN multiplies by nothing else (all three tori are
in lam). Control: S002 with its free torus treated as a third torus with W = 0 must reproduce the two-torus engine."""
import sys
import itertools
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import w33_so16_one_loop as E


class WLPartN:
    def __init__(self, V0, Wt, Tw, K=2):
        self.V0, self.Wt, self.Tw, self.K = V0, [np.asarray(w, float) for w in Wt], list(Tw), K
        self.t = len(Wt)
        self.WW = np.array([[a @ b for b in self.Wt] for a in self.Wt])
        self.V0W = np.array([V0 @ a for a in self.Wt])
        self.J = list(itertools.product(range(3), repeat=self.t))
        jj = np.array(self.J)
        self.DFT = np.exp(-2j * np.pi * (jj @ jj.T) / 3.0)          # [k, j]

    def lam(self, tau, s, t, phase_vac=1.0):
        K, V0, Wt, nt = self.K, self.V0, self.Wt, self.t
        Z = [t * V0 + sum(j[i] * Wt[i] for i in range(nt)) for j in self.J]
        Gc = {}
        for Nm in self.J:
            w = s * V0 + sum(Nm[i] * Wt[i] for i in range(nt))
            Gc[Nm] = np.array([E.gauge16(w, z, tau) for z in Z])
        cache = {}

        def S(ti, Nt, o):
            key = (ti, Nt, round(o % 1.0, 10))
            if key not in cache:
                oo = o % 1.0
                acc = 0
                for n1 in range(-K, K + 1):
                    n2 = Nt - n1
                    if abs(n2) > K:
                        continue
                    acc += E.torus_sum(tau, self.Tw[ti], np.array([oo, oo]), np.array([n1, n2], float))
                cache[key] = acc
            return cache[key]
        Zm = np.array(Z)
        tot = 0
        ph0 = np.exp(2j * np.pi * t * s * (V0 @ V0)) / 3.0 ** nt
        for N in itertools.product(range(-2 * K, 2 * K + 1), repeat=nt):
            lamv = sum((N[i] - N[i] % 3) * Wt[i] for i in range(nt))
            vec = np.exp(-2j * np.pi * (Zm @ lamv)) * Gc[tuple(n % 3 for n in N)]
            g = (self.DFT @ vec) * ph0
            for ki, k in enumerate(self.J):
                if abs(g[ki]) < 1e-300:
                    continue
                prod = g[ki]
                for i in range(nt):
                    o = k[i] / 3 + s * self.V0W[i] + 0.5 * sum(N[m] * self.WW[i, m] for m in range(nt))
                    prod = prod * S(i, N[i], o)
                    if prod == 0:
                        break
                tot += prod
        return tot * phase_vac


def Zbeta_blockN(tau, wl, s, t):
    et = E.eta(tau)
    F = np.conj(E.fermions(s * E.V0V, -t * E.V0V, tau)) / np.conj(et) ** 4
    L = wl.lam(tau, s, t)
    return F * L / (et ** 22 * np.conj(et) ** 6) / (tau.imag * abs(et) ** 4)


def Z_betaN(tau, wl):
    return (Zbeta_blockN(tau, wl, 0, 1) + Zbeta_blockN(tau, wl, 1, 0) - Zbeta_blockN(tau, wl, 1, 1)) / 6
