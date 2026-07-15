#!/usr/bin/env python3
"""Pass 257: Koide's 45 degrees is a LIGHT-CONE condition -- and it is an
on-shell (IR) statement, not an RG fixed point.

Pass 251 proved Koide's Q = 2/3 is exactly the S3 singlet/doublet equipartition
of the sqrt-mass vector z.  This witness sharpens the geometry and then tests
the obvious dynamical hypothesis -- that 45 degrees is an RG fixed point --
honestly.

1. THE LIGHT CONE (rigorous, new).  Equipartition
        z^T P_1 z = z^T P_2 z    (P_1 = singlet projector, P_2 = I - P_1)
   is equivalent to
        z^T (2 P_1 - I) z = 0.
   The S3-invariant form  eta = 2 P_1 - I  has eigenvalues (+1, -1, -1):
   MINKOWSKI signature (1,2) on generation space, with the timelike direction
   the democratic singlet.  So

        KOIDE  <=>  the sqrt-mass vector z is NULL (lightlike) for the
                    S3-invariant Lorentzian metric eta on generation space.

   The charged leptons lie on the light cone of the family clock.

2. SCALE INVARIANCE (rigorous).  Q = |z|^2/(z.u)^2 is invariant under z -> lam z,
   so Koide constrains only the DIRECTION of z -- a point on the celestial
   sphere of eta -- never the overall mass scale.  This is why the statement is
   an angle.

3. IS 45 AN RG FIXED POINT? (honest test).  Because Q is invariant under uniform
   rescaling, only NON-universal running can move it.  We evaluate Q and theta
   for (a) the pole masses and (b) the MS-bar masses run to M_Z, and report the
   shift.  If theta moves off 45, the equipartition is an on-shell/IR property
   that selects the pole scale rather than an RG-invariant fixed point.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass257_koide_lightcone.json"

# pole (on-shell) charged-lepton masses, MeV (PDG)
POLE = {"e": 0.51099895000, "mu": 105.6583755, "tau": 1776.86}
# MS-bar charged-lepton masses run to M_Z, MeV (standard values)
MSBAR_MZ = {"e": 0.486570, "mu": 102.718, "tau": 1746.24}


def Q_of(masses):
    z = np.array([math.sqrt(m) for m in masses], dtype=float)
    return float(np.sum(z ** 2) / (np.sum(z) ** 2)), z


def theta_of(z):
    u = np.ones(3) / math.sqrt(3.0)
    return math.degrees(math.acos(float(np.dot(z, u) / np.linalg.norm(z))))


def main():
    checks = {}

    # ---- 1. the Lorentzian form eta = 2 P_1 - I
    u = (np.ones(3) / math.sqrt(3.0)).reshape(3, 1)
    P1 = u @ u.T
    eta = 2 * P1 - np.eye(3)
    ev = sorted(np.linalg.eigvalsh(eta).tolist(), reverse=True)
    checks["eta_signature_1_2"] = (abs(ev[0] - 1) < 1e-12
                                   and abs(ev[1] + 1) < 1e-12
                                   and abs(ev[2] + 1) < 1e-12)
    checks["eta_symmetric"] = bool(np.allclose(eta, eta.T))
    # timelike direction is the democratic singlet
    checks["timelike_dir_is_singlet"] = abs((u.T @ eta @ u).item() - 1.0) < 1e-12

    # ---- Koide <=> z null for eta  (verified on a constructed null vector)
    w = np.array([1.0, -1.0, 0.0])
    w /= np.linalg.norm(w)
    z_null = u.flatten() + w          # equal singlet/doublet norm
    checks["constructed_is_null"] = abs(float(z_null @ eta @ z_null)) < 1e-12
    Qn = float(np.sum(z_null ** 2) / (np.sum(z_null) ** 2))
    checks["null_vector_gives_Q_two_thirds"] = abs(Qn - 2 / 3) < 1e-12

    # ---- 2. scale invariance of Q
    Qa, za = Q_of(list(POLE.values()))
    scaled = [4.0 * m for m in POLE.values()]   # z -> 2z
    Qs, _ = Q_of(scaled)
    checks["Q_scale_invariant"] = abs(Qa - Qs) < 1e-12

    # ---- 3. pole vs MS-bar(M_Z): is 45 an RG fixed point?
    th_pole = theta_of(za)
    null_pole = float(za @ eta @ za) / float(za @ za)   # normalised null defect
    Qz, zz = Q_of(list(MSBAR_MZ.values()))
    th_mz = theta_of(zz)
    null_mz = float(zz @ eta @ zz) / float(zz @ zz)

    checks["pole_theta_is_45"] = abs(th_pole - 45.0) < 0.01
    checks["pole_nearly_null"] = abs(null_pole) < 1e-3
    # the honest question: does it survive running?
    moved = abs(th_mz - 45.0) > abs(th_pole - 45.0)
    checks["running_moves_theta_off_45"] = moved
    checks["msbar_less_null_than_pole"] = abs(null_mz) > abs(null_pole)

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass257.koide_lightcone.v1",
        "status": "PASS" if all_pass else "FAIL",
        "theorem": (
            "Koide's Q = 2/3 is exactly the statement that the sqrt-mass vector "
            "is NULL for the S3-invariant Lorentzian metric eta = 2P_singlet - I "
            "of signature (1,2) on generation space, whose timelike direction is "
            "the democratic singlet. The charged leptons lie on the light cone "
            "of the family clock. Q is invariant under z -> lambda z, so the "
            "condition constrains only the direction of z."
        ),
        "lorentzian_form": {
            "eta": "2 P_singlet - I",
            "eigenvalues": ev,
            "signature": "(1,2) Minkowski; timelike = democratic singlet",
            "koide_condition": "z^T eta z = 0  (z lightlike)",
        },
        "pole_masses": {
            "masses_MeV": POLE, "Q": Qa, "theta_deg": th_pole,
            "null_defect_zT_eta_z_over_z2": null_pole,
        },
        "msbar_at_MZ": {
            "masses_MeV": MSBAR_MZ, "Q": Qz, "theta_deg": th_mz,
            "null_defect_zT_eta_z_over_z2": null_mz,
        },
        "rg_verdict": (
            "NOT an RG fixed point: the pole masses sit on the light cone "
            f"(theta = {th_pole:.5f} deg, defect {null_pole:.2e}) while the "
            f"MS-bar masses at M_Z do not (theta = {th_mz:.4f} deg, defect "
            f"{null_mz:.2e}). Since Q is invariant under uniform rescaling, "
            "only the non-universal part of the running moves it -- and it does. "
            "The equipartition is an ON-SHELL (IR) property that selects the "
            "pole scale, not a scale-invariant fixed point."
        ),
        "reading": (
            "Koide becomes geometry: the charged-lepton sqrt-mass vector is a "
            "null ray of the family clock's Minkowski metric, and Q measures "
            "only its direction. The natural dynamical hypothesis -- that 45 "
            "degrees is an RG fixed point -- is FALSE: running to M_Z moves the "
            "vector off the cone. So whatever fixes the leptons on the light "
            "cone acts at the on-shell/IR scale. That is a sharper and more "
            "falsifiable statement than the original numerical coincidence, and "
            "it tells the next investigation where to look."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
