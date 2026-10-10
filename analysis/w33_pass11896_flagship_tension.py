"""Pass 11896: the flagship tension -- with the CZ3 Wilson line, the Z6 flat directions are Standard-Model charged.

Flagship holonomies (w33_paper 79.81-79.86): the order-two theta3 = sigma' (5 + 4, fixed su5+su4+u1) and the order-three
CZ3 Wilson line W3 = diag(w^{xy}) (5 + 2 + 2), commuting, with joint fundamental multiplicities (3,2,1,1,1,1). Here
sigma' = +1 on three zero-phase levels and on one level of each nontrivial CZ3 block.

  * Local gauge algebra: the joint centraliser su(3) + su(2) + u(1)^5 (dimension 16).
  * Untwisted matter: family planes = sigma'-odd and W3-invariant 3-forms, 16 states:
    (3bar,2) [AAB] + 2 (3,1) [A c d] + 2 (1,2) [B c c', B d d'] -- a family without e^c, consistent with families split
    between untwisted and twisted sectors (Holotrade 3caf15e, Pass 11714); qutrit plane = sigma'-even and W3-invariant, 14.
  * Every Kempf-Ness flat point of the family-plane matter (and of the qutrit-plane matter) leaves only a 2-dimensional
    unbroken group: SU(3) x SU(2) is broken. So in the flagship the Siegel-type flat direction is Standard-Model charged:
    a Standard-Model vacuum sits at its origin, and the vacuum-selection mechanism of Passes 11884-11895 (which acts on
    nonzero flat vevs) cannot operate in the visible untwisted sector without breaking the Standard Model.
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.linalg import null_space

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402

OUT = ROOT / "data" / "w33_pass11896_flagship_tension.json"
W = np.exp(2j * np.pi / 3)
PTS = [(a, b) for a in range(3) for b in range(3)]


def holonomies():
    cross = [i for i, (a, b) in enumerate(PTS) if a * b % 3 == 0]
    om = [i for i, (a, b) in enumerate(PTS) if a * b % 3 == 1]
    om2 = [i for i, (a, b) in enumerate(PTS) if a * b % 3 == 2]
    sig = -np.ones(9)
    for i in cross[:3] + om[:1] + om2[:1]:
        sig[i] = 1
    W3 = np.array([W ** (a * b) for a, b in PTS])
    return sig, W3


def on_l3(d):
    return np.array([E.sorted_c(np.einsum("ai,bj,ck,ijk->abc", np.diag(d), np.diag(d), np.diag(d), E.full(np.eye(84)[i])))
                     for i in range(84)]).T


def gauge_basis(key):
    G = []
    for i in range(9):
        for j in range(i + 1, 9):
            if key[i] == key[j]:
                A = np.zeros((9, 9), complex)
                A[i, j], A[j, i] = 1, -1
                G.append(A / np.sqrt(2))
                A = np.zeros((9, 9), complex)
                A[i, j], A[j, i] = 1j, 1j
                G.append(A / np.sqrt(2))
    blocks = sorted(set(key))
    D = np.array([[1.0 if key[i] == bk else 0.0 for i in range(9)] for bk in blocks])
    sizes = D.sum(1)
    for col in null_space(sizes[None, :]).T:
        G.append(1j * np.diag(sum(col[b] * D[b] for b in range(len(blocks)))))
    for bk in blocks:
        idx = [i for i in range(9) if key[i] == bk]
        for m in range(len(idx) - 1):
            d = np.zeros(9)
            d[idx[m]], d[idx[m + 1]] = 1, -1
            G.append(1j * np.diag(d))
    return G


def main():
    rng = np.random.default_rng(11896)
    sig, W3 = holonomies()
    joint = Counter((int(sig[i]), int(round(np.angle(W3[i]) * 3 / (2 * np.pi))) % 3) for i in range(9))
    key = [(sig[i], round(float(np.angle(W3[i])), 6)) for i in range(9)]
    S, Wm = np.diag(on_l3(sig)).real, np.diag(on_l3(W3))
    fam = [i for i in range(84) if S[i] < 0 and abs(Wm[i] - 1) < 1e-9]
    qut = [i for i in range(84) if S[i] > 0 and abs(Wm[i] - 1) < 1e-9]
    G = gauge_basis(key)
    # block-type content of the family plane
    from w33_pass11681_e8_from_two_qutrits import TR
    names = {}
    labels = {}
    for i in range(9):
        k = key[i]
        if k not in labels:
            labels[k] = "ABcdef"[len(labels)]
    btype = Counter("".join(sorted(labels[key[t]] for t in TR[i])) for i in fam)
    HERM = [1j * A for A in G]

    def act(A, x):
        return E.sorted_c(E._act(A, E.full(x)))

    def mu(x):
        return np.array([np.vdot(x, act(Hm, x)).real for Hm in HERM])
    flat = {}
    for name, idx in (("family_plane", fam), ("qutrit_plane", qut)):
        Vs = np.eye(84)[:, idx]
        dims = []
        for _ in range(3):
            y = Vs @ (rng.normal(size=len(idx)) + 1j * rng.normal(size=len(idx)))
            y /= np.linalg.norm(y)
            for _ in range(20000):
                m = mu(y)
                if np.linalg.norm(m) < 1e-11:
                    break
                y = y - 0.1 * sum(m[a] * act(HERM[a], y) for a in range(len(HERM)))
                y /= np.linalg.norm(y)
            T = E.full(y)
            Mm = np.array([E._act(A, T).ravel() for A in G]).T
            _, sr, _ = np.linalg.svd(np.vstack([Mm.real, Mm.imag]))
            dims.append(dict(mu=float(np.linalg.norm(mu(y))), unbroken=int(np.sum(sr < 1e-7 * sr[0]))))
        flat[name] = dims
    res = dict(pass_id=11896, joint_multiplicities={str(k): v for k, v in joint.items()}, gauge_dim=len(G),
               family_plane_states=len(fam), qutrit_plane_states=len(qut), family_block_types=dict(btype),
               block_labels={str(k): v for k, v in labels.items()}, flat_points=flat)
    res["checks"] = {k: bool(v) for k, v in dict(
        flagship_multiplicities=sorted(joint.values()) == [1, 1, 1, 1, 2, 3],
        gauge_su3_su2_u1_5=len(G) == 16,
        family_16_qutrit_14=len(fam) == 16 and len(qut) == 14,
        flat_points_found=all(d["mu"] < 1e-9 for v in flat.values() for d in v),
        sm_broken_on_flat_directions=all(d["unbroken"] < 11 for v in flat.values() for d in v),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
