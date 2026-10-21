"""12174 driver: E8 x E8 fermion-parity orbifolds g = (-1)^F exp(2 pi i p.V), V = (V1, V2) with V_i in {0, clock, split}
(clock: V = alpha/2, alpha a root, V^2 = 1/2, fixed e7+a1; split: V = v/2, v of norm 4, V^2 = 1, fixed d8).
Blocks Z[a,b] = conj(R[a,b]) L1[a,b] L2[a,b] / eta^16 with R00 = V8-S8, R01 = V8+S8, R10 = O8-C8, R11 = e^{-i pi/3}(O8+C8),
L[a,b] = sum_{p in E8+aV} exp(i pi b (2 p.V - a V^2)) q^{p^2/2}.  Checks Z(tau+1) = Z(tau), Z(-1/tau) = Z(tau) numerically,
then counts the massless and tachyonic states from the projected sectors."""
import itertools, json, sys
import numpy as np
import mpmath as mp

mp.mp.dps = 30


def e8_vectors(maxnorm):
    out = []
    for half in (0, 1):
        vals = [x + 0.5 * half for x in range(-5, 6)]
        part = [((), 0.0)]
        for d in range(8):
            nxt = []
            for v, n in part:
                for x in vals:
                    nn = n + x * x
                    if nn <= maxnorm + 1e-9:
                        nxt.append((v + (x,), nn))
            part = nxt
        for v, n in part:
            if round(sum(v) * (1 if not half else 1)) % 2 == 0 if not half else (round(sum(v)) % 2 == 0):
                out.append(v)
    return np.array(out)


E8 = e8_vectors(20)
SHIFT = {"0": np.zeros(8), "clock": np.array([.5, .5, 0, 0, 0, 0, 0, 0]), "split": np.array([1., 0, 0, 0, 0, 0, 0, 0])}


def coset(V, maxn=12.0):
    P = E8 + V
    n = (P * P).sum(1)
    k = n <= maxn + 1e-9
    return P[k], n[k]


def L(V, a, b, tau):
    P, n = coset(V if a else np.zeros(8))
    ph = np.exp(1j * np.pi * b * (2 * (P @ V) - a * (V @ V)))
    return complex(np.sum(ph * np.exp(1j * np.pi * complex(tau) * n)))


def eta(tau):
    q = mp.exp(2j * mp.pi * tau)
    return mp.exp(1j * mp.pi * tau / 12) * mp.qp(q)


def chars(tau):
    nome = mp.exp(1j * mp.pi * tau)
    t2, t3, t4 = (mp.jtheta(k, 0, nome) for k in (2, 3, 4))
    e4 = eta(tau) ** 4
    return dict(O=(t3 ** 4 + t4 ** 4) / (2 * e4), V=(t3 ** 4 - t4 ** 4) / (2 * e4), S=t2 ** 4 / (2 * e4), C=t2 ** 4 / (2 * e4))


def block(V1, V2, a, b, tau):
    c = chars(tau)
    R = {(0, 0): c["V"] - c["S"], (0, 1): c["V"] + c["S"], (1, 0): c["O"] - c["C"]}[(a, b)]
    return complex(mp.conj(R)) * L(V1, a, b, tau) * L(V2, a, b, tau) / complex(eta(tau) ** 16)


def Z(V1, V2, tau):
    """Z = F/2 [B00 + B01 + B10 + B11], B11(tau) := B10(tau + 1) (the T-image, so no phase convention enters)."""
    F = float(mp.im(tau)) ** -4 * abs(complex(eta(tau))) ** -16
    return F * (block(V1, V2, 0, 0, tau) + block(V1, V2, 0, 1, tau) + block(V1, V2, 1, 0, tau) + block(V1, V2, 1, 0, tau + 1)) / 2


def closure(V1, V2, tau):
    """T^2 closure of the twisted block (level matching): |B10(tau+2) - B10(tau)| / |B10|."""
    b0, b2 = block(V1, V2, 1, 0, tau), block(V1, V2, 1, 0, tau + 2)
    return abs(b2 - b0) / abs(b0)


def spectrum(V1, V2):
    """massless n_B, n_F and tachyon count from the projected sectors (light-cone dof)."""
    V = np.concatenate([V1, V2])
    r1, r2 = [p for p in E8 if abs(p @ p - 2) < 1e-9], None
    R = np.array(r1)
    roots = np.vstack([np.hstack([R, np.zeros_like(R)]), np.hstack([np.zeros_like(R), R])])
    ph = roots @ V
    even = int(np.sum(np.abs(ph - np.round(ph)) < 1e-9))
    odd = len(roots) - even
    nB = 8 * (8 + 16 + even)
    nF_un = 8 * odd
    P1, n1 = coset(V1, 6)
    P2, n2 = coset(V2, 6)
    tot = (n1[:, None] + n2[None, :]).ravel()
    tach = int(np.sum(np.abs(tot - 1) < 1e-9))
    tw2 = int(np.sum(np.abs(tot - 2) < 1e-9)) + 24 * int(np.sum(np.abs(tot) < 1e-9))
    nonint = bool(np.any(np.abs(tot - np.round(tot)) > 1e-9))
    return dict(gauge_dim=even + 16, even_roots=even, odd_roots=odd, nB=nB, nF=nF_un + 8 * tw2, tachyons=tach, twisted_norm_nonintegral=nonint)


if __name__ == "__main__":
    print("E8 vectors", len(E8), "norm2", int(np.sum(np.abs((E8 * E8).sum(1) - 2) < 1e-9)))
    res = {}
    for c1, c2 in [("0", "0"), ("split", "0"), ("split", "split"), ("clock", "clock"), ("clock", "0"), ("clock", "split")]:
        V1, V2 = SHIFT[c1], SHIFT[c2]
        out = dict(V2=float(V1 @ V1 + V2 @ V2))
        for t in (mp.mpc(0.2, 1.05), mp.mpc(-0.31, 0.93)):
            z, zT, zS = Z(V1, V2, t), Z(V1, V2, t + 1), Z(V1, V2, -1 / t)
            out.setdefault("Z", []).append([abs(z), abs(zT - z) / max(abs(z), 1e-30), abs(zS - z) / max(abs(z), 1e-30), closure(V1, V2, t)])
        out.update(spectrum(V1, V2))
        res[f"{c1}x{c2}"] = out
        print(c1, c2, out, flush=True)
    json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else "tenD.json", "w"), indent=1)
