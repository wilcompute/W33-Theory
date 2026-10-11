"""Pass 11924: why stabiliser Higgs vacua lock m_c = m_u (a residual S3), and how a misaligned flavon unlocks it.

Setting: Y_u(h)_{ab} = h_{a+b} g_{a-b} with g even (Passes 11918, 11921, 11923); Delta(54) = <X, Z, R> acting on the family
qutrit Q (and u^c) by shift, clock and reflection.

1. Covariance. All 18 projective elements U of Delta(54) act covariantly: U Y(h) U^T = Y(V_U h) for a linear map V_U on
   the Higgs triplet.
2. Theorem (residual S3). Each of the 12 qutrit stabiliser states h has residual group {U : V_U h ~ h} of projective
   order 6 (an S3 = Z3 x| Z2), whose action on Q has commutant dimension 2, i.e. Q = 1 + 2. Since Y Y^dagger commutes
   with the image, it has a degenerate pair -- the lock of Pass 11923 is symmetry-protected, to all orders, in any
   vacuum that preserves that S3. A generic h has trivial residual group; a misaligned pair (Z-eigenstate Higgs,
   X-eigenstate flavon) keeps only the reflection Z2 (commutant dimension 5: no forced degeneracy).
3. Two triplets (frozen, data/w33_pass11924_two_triplet_frozen.json). Higgs h and flavon phi, each with the general
   Delta(54) self-potential, coupled by the general Delta(54)-invariant mixed quartic
   lam sum_{d,e} Re(C_de sum_i hbar_i h_{i+d} phibar_{i+e} phi_{i+e-d}), C_de = C_{-d,-e}.
   Over 120 random Delta(54) coupling draws (global minimum at lam = 0.1, continued to 0.01 and 0.001): 32 vacua keep
   the Higgs exactly at a stabiliser state (Pauli expectation 1 - 3e-14) and stay locked; 88 unlock, 79 of them linearly
   in lam (median gap ratio 9.8 per decade; the rest switch branch). A Delta(27)-only control agrees (28/40 unlock).
   So a flavon triplet coupled to the Higgs lifts m_c = m_u in about three quarters of Delta(54) vacua, at first order in
   the mixing.
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11924_residual_s3_and_misaligned_flavon.json"
FROZEN = ROOT / "data" / "w33_pass11924_two_triplet_frozen.json"
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11924_two_triplet_scan as TT  # noqa: E402
W = np.exp(2j * np.pi / 3)
XQ = np.roll(np.eye(3), 1, axis=0)
ZQ = np.diag([1, W, W * W])
RQ = np.eye(3)[[0, 2, 1]]
STAB = [np.eye(3)[k] for k in range(3)] + [np.array([W ** (s * j * j + t * j) for j in range(3)]) / np.sqrt(3)
                                           for s in range(3) for t in range(3)]


def elements(g):
    def Y(h):
        return np.array([[h[(a + b) % 3] * g[(a - b) % 3] for b in range(3)] for a in range(3)])

    basisY = [Y(e) for e in np.eye(3)]
    B = np.array([m.ravel() for m in basisY]).T
    els, resid = [], 0.0
    for x, z, r in itertools.product(range(3), range(3), range(2)):
        U = np.linalg.matrix_power(XQ, x) @ np.linalg.matrix_power(ZQ, z) @ np.linalg.matrix_power(RQ, r)
        V = np.zeros((3, 3), complex)
        for k in range(3):
            target = (U @ basisY[k] @ U.T).ravel()
            sol = np.linalg.lstsq(B, target, rcond=None)[0]
            resid = max(resid, float(np.linalg.norm(B @ sol - target)))
            V[:, k] = sol
        els.append((U, V))
    return els, resid


def commutant_dim(Us):
    A = np.vstack([np.kron(U, np.eye(3)) - np.kron(np.eye(3), U.T) for U in Us])
    s = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(s < 1e-9)) + max(0, 9 - len(s))


def stabgroup(els, h):
    return [k for k, (U, V) in enumerate(els) if abs(abs(np.vdot(h, V @ h)) / np.linalg.norm(V @ h) - 1) < 1e-10]


def main():
    rng = np.random.default_rng(11924)
    out = []
    for _ in range(5):
        e = rng.normal() + 1j * rng.normal()
        g = np.array([rng.normal() + 1j * rng.normal(), e, e])
        els, resid = elements(g)
        stab = [(len(stabgroup(els, h)), commutant_dim([els[k][0] for k in stabgroup(els, h)])) for h in STAB]
        hg = rng.normal(size=3) + 1j * rng.normal(size=3)
        gen = len(stabgroup(els, hg / np.linalg.norm(hg)))
        common = set(stabgroup(els, STAB[0])) & set(stabgroup(els, STAB[3]))
        out.append(dict(covariance_residual=resid, stabiliser=stab, generic_group=gen, misaligned_common=len(common),
                        misaligned_commutant=commutant_dim([els[k][0] for k in common])))
    fz = json.loads(FROZEN.read_text())
    cr = fz["check_row"]
    repro = float(np.max(abs(TT.scan(cr["sym"], cr["seed"], cr["trial"] + 1, only=[cr["trial"]])[0] - np.array(cr["row"]))))
    res = dict(pass_id=11924, residual_symmetry=out, two_triplet=fz, scan_repro_max_diff=repro)
    res["checks"] = {k: bool(v) for k, v in dict(
        delta54_covariant=all(o["covariance_residual"] < 1e-12 for o in out),
        stabiliser_states_keep_s3_with_doublet=all(all(s == (6, 2) for s in o["stabiliser"]) for o in out),
        generic_h_no_symmetry=all(o["generic_group"] == 1 for o in out),
        misaligned_pair_only_z2=all(o["misaligned_common"] == 2 and o["misaligned_commutant"] == 5 for o in out),
        **fz["checks"],
        scan_reproduces=repro < 1e-10,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
