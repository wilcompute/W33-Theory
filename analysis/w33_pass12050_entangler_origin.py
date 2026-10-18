"""Pass 12050: where can the small entangler eps = Omega_12 come from? Two standard string mechanisms checked. The
heterotic Wilson-line reading of Pass 12049 has no home in the computed heterotic orbifold class, and magnetized-flux
stabilisation needs flux integers ~ 1/eps (Claude track).

(i) Heterotic continuous Wilson lines (Kobayashi-Lebedev, hep-th/0303009, eqs. 33-36; read for this pass). In abelian
    Z_N orbifolds with a T^2 + T^2 + T^2 decomposition, a continuous Wilson line a_i in plane i enters the twisted
    Yukawa couplings only through the per-plane combination T_i + kappa (T_i + Tbar_i) a_i abar_i. That is a rescaling of
    the plane's own Kahler modulus -- a DIAGONAL period-matrix entry. This holds for the standard embedding and for the
    block non-standard embeddings they treat (eq. 35). An off-diagonal Omega_12 would need a gauge block shared between
    two planes, outside the computed class; even then it would be proportional to a product a_1 abar_2, whose zero locus
    is not the full gauge-restoration locus. So the identification "Omega_12 = an SU(5)-restoring Wilson line" (12049)
    has no home there. K-L also find heterotic Wilson lines give no CP phases in the Yukawas, unlike open strings. The
    12045 CP-in-a-Wilson-line row therefore belongs to the open-string (magnetized) reading of 11942.
(ii) Magnetized fluxes. In the magnetized reading Omega_12 is a complex-structure modulus. Fluxes stabilise complex
    structure through the (1,1) condition: each extra (1,1) flux class confines the abelian surface to a Humbert surface
        a tau1 + b eps + c tau2 + d (eps^2 - tau1 tau2) + e = 0,   Delta = b^2 - 4ac - 4de > 0.
    The product locus eps = 0 is Delta = 1. On the symmetric CP home tau = 1 + i y, eps = i delta, the relation reduces
    to (a + c - 2d) y + b delta = 0 and (a + c) + e = d(1 - y^2 + delta^2). An exhaustive integer search (|b| <= 4000,
    |d| <= 60) within the data tolerance (y +- 0.007 from the Weber invariant, delta +- 3% from m_c/m_t) gives a minimal
    discriminant of 23716 (1 sigma), 22500 (2 sigma) or 21025 (3 sigma). It is attained by the linear relation
    eps = (tau - 1)/b with b ~ 150, i.e. b ~ y/delta = 158. Flux stabilisation can put the up home on such a surface,
    but only with flux integers ~ 150. The product locus itself is ~33 sigma away in delta.
Reading. Neither standard mechanism explains the near-product hierarchy naturally. Heterotic Wilson lines rescale
planes instead of entangling them, and magnetized fluxes need integers ~ 1/eps. Together with 12048 (canonical
potentials repel the product locus), what keeps eps ~ 1/150 remains the central open question. 12049's
threshold-matching stays conditional, now with no known string home.
Scope: the K-L class (abelian orbifolds, factorisable planes, their embeddings); the symmetric CP-locus up home; one
extra flux class. Not new: K-L's Wilson-line Yukawas; flux (1,1) stabilisation of complex structure (Antoniadis-Kumar-
Maillard and others); Humbert singular relations (classical).
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12050_entangler_origin.json"
Y, DEL = 0.8744698731421595, 0.005520606513514881
SY, SD = 0.007, 0.03 * DEL


def search(nsig, B=4000, Dm=60):
    best = []
    for d in range(-Dm, Dm + 1):
        for b in range(1, B + 1):
            s_real = 2 * d - b * DEL / Y
            s = int(round(s_real))
            if abs(s - s_real) > nsig * np.hypot(b * SD / Y, b * DEL * SY / Y ** 2) + 1e-12:
                continue
            e_real = d * (1 - Y * Y + DEL * DEL) - s
            e = int(round(e_real))
            if abs(e - e_real) > nsig * abs(d) * 2 * Y * SY + 1e-9:
                continue
            for a in (s // 2, s - s // 2):
                c = s - a
                D = b * b - 4 * a * c - 4 * d * e
                if D > 0:
                    best.append((D, a, b, c, d, e))
    best.sort()
    return best[0] if best else None


def main():
    checks, res = {}, {}
    mins = {str(n): search(n) for n in (1.0, 2.0, 3.0)}
    res["min_discriminant"] = mins
    m1 = mins["1.0"]
    a, b, c, d, e = m1[1:]
    tau, eps = 1 + 1j * Y, 1j * Y / b                     # nearest point of the minimal surface (eps = (tau-1)/b)
    rel = a * tau + b * eps + c * tau + d * (eps * eps - tau * tau) + e
    res["minimal_surface_point"] = dict(relation=[a, b, c, d, e], eps=float(eps.imag), delta_pull=float((eps.imag - DEL) / SD), residual=abs(rel))
    res["analytic_b_bound"] = Y / DEL
    res["product_locus_pull_in_delta"] = DEL / SD
    checks["minimal Humbert discriminant through the fitted up home exceeds 2e4 (1-3 sigma)"] = bool(min(v[0] for v in mins.values()) > 2e4)
    checks["the minimiser is the linear relation eps = (tau - 1)/b with b ~ y/delta (~150)"] = bool(
        d == 0 and abs(b - Y / DEL) / (Y / DEL) < 0.1 and abs(rel) < 1e-12 and abs(res["minimal_surface_point"]["delta_pull"]) < 1.0)
    checks["the product locus (Delta = 1) is > 20 sigma from the fitted eps"] = bool(DEL / SD > 20)
    res["kobayashi_lebedev"] = dict(ref="hep-th/0303009 eqs. 33-36",
                                    statement="continuous Wilson lines enter twisted Yukawas as T_i + kappa(T_i+Tbar_i) a_i abar_i per plane (diagonal); no CP phases")
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    print(json.dumps(res["min_discriminant"]), res["minimal_surface_point"])
    return res


if __name__ == "__main__":
    main()
