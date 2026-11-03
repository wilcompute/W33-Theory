"""One-field Lambda + s M exp(-n b chi) + sparse tower, fast: dm_drag.solve shoots with a general two-field integrator and is too slow for fits.  Here chi only, starting at N = -12 as elsewhere (N = -9 is only z = 8000, which loses part of the kick: the control caught that), and Lambda by iteration on E(0) = 1, raising if the budget does not close.  Parametrised by the amplitude Z at chi = 0, so Lambda is the only shooting variable; eps = Z exp(-n b chi_0) follows.
Control: agreement with dm_drag.solve at the same parameters, in casimir_fits.py.  Imported by casimir_fits.py."""
import math
import numpy as np
from scipy.integrate import solve_ivp
import dark_like as L

NI = -12.0
NG = np.log(1 / (1 + L.ZGRID))[::-1]
NREC = -math.log(1090.0)
MASK = NG >= NI


def solve(b, prod, n, Z, wb, wbc, h, want=False):
    """Z is the amplitude at chi = 0, in units of the critical density today, with its sign: < 0 is net bosons.  eps today is returned with want."""
    f = prod / b
    h2 = h * h
    orr, ob, onu = L.OMEGA_R_H2 / h2, wb / h2, L.OMEGA_NU_H2 / h2
    oc_rec = (wbc - wb) / h2
    lam = n * b
    obn = ob + onu

    def run(ol, Z, oci):
        fo = f * oci
        uo = (1 - f) * oci + obn

        def rhs(N, y):
            chi, x = y
            ea = math.exp(-3 * N)
            rcc = fo * ea * math.exp(-b * chi)
            rr = orr * ea * math.exp(-N)
            Vc = Z * math.exp(-lam * chi)
            E2 = (rcc + uo * ea + rr + ol + Vc) / (1 - x * x / 6)
            if not (x * x < 5.9 and E2 > 0):  # the integrator crawls at the kination wall or where V drives E^2 negative: such a point is rejected, not an exclusion of the model
                raise RuntimeError("left the domain")
            dl = -0.5 * (x * x + 3 * (rcc + uo * ea + 4 / 3 * rr) / E2)
            return [x, -(3 + dl) * x + 3 * (b * rcc + lam * Vc) / E2]

        return solve_ivp(rhs, (NI, 0.0), [0.0, 0.0], rtol=1e-8, atol=1e-11, method="LSODA")

    oci = oc_rec
    ol = 1 - (wbc + L.OMEGA_NU_H2) / h2 - Z * math.exp(-lam * 2 * prod * 2.0)
    closed = False
    for _ in range(40):
        s = run(ol, Z, oci)
        if not s.success:
            raise RuntimeError
        chi_end, x_end = s.y[:, -1]
        rc0 = oci * ((1 - f) + f * math.exp(-b * chi_end))
        E0 = (rc0 + obn + orr + ol + Z * math.exp(-lam * chi_end)) / (1 - x_end * x_end / 6)
        chi_rec = float(np.interp(NREC, s.t, s.y[0]))
        oci2 = oc_rec / ((1 - f) + f * math.exp(-b * chi_rec))
        if abs(E0 - 1) < 2e-6 and abs(oci2 / oci - 1) < 1e-6:
            closed = True
            break
        ol += 1 - E0
        oci = oci2
    if not closed:
        raise RuntimeError("budget did not close")
    fo, uo = f * oci, (1 - f) * oci + obn

    def rhs2(N, y):
        chi, x = y
        ea = math.exp(-3 * N)
        rcc = fo * ea * math.exp(-b * chi)
        rr = orr * ea * math.exp(-N)
        Vc = Z * math.exp(-lam * chi)
        E2 = (rcc + uo * ea + rr + ol + Vc) / (1 - x * x / 6)
        if not (x * x < 5.9 and E2 > 0):
            raise RuntimeError("left the domain")
        dl = -0.5 * (x * x + 3 * (rcc + uo * ea + 4 / 3 * rr) / E2)
        return [x, -(3 + dl) * x + 3 * (b * rcc + lam * Vc) / E2]

    s = solve_ivp(rhs2, (NI, 0.0), [0.0, 0.0], rtol=1e-7, atol=1e-10, method="LSODA", t_eval=NG[MASK])
    if not s.success:
        raise RuntimeError
    chi = np.zeros_like(NG)
    x_ = np.zeros_like(NG)
    chi[MASK], x_[MASK] = s.y
    a3 = np.exp(-3 * NG)
    rc = fo * a3 * np.exp(-b * chi) + (uo * a3)
    Vc = Z * np.exp(-lam * chi)
    E2 = (rc + orr * a3 * np.exp(-NG) + ol + Vc) / (1 - x_ ** 2 / 6)
    if abs(E2[-1] - 1) > 2e-5:
        raise RuntimeError("E(0) != 1")
    E = np.sqrt(E2)[::-1]
    if want:
        ir = int(np.argmin(abs(NG - NREC)))
        kin = E2 * x_ ** 2 / 6
        V = ol + Vc
        rho_phi = kin + V
        w_phi = (kin - V) / rho_phi
        zs = (0.0, 0.3, 0.5, 1.0, 2.0)
        idx = {str(z): int(np.argmin(abs(NG + math.log(1 + z)))) for z in zs}
        return E, dict(ol=ol, Z=Z, eps=float(Z * math.exp(-lam * chi[-1])), chi0=float(chi[-1]), chi_rec=float(chi[ir]), chiN0=float(x_[-1]), f=f, dln_mKK_rec_to_0=float(-b * (chi[-1] - chi[ir])), w_phi={k: float(w_phi[i]) for k, i in idx.items()}, chi_at={k: float(chi[i]) for k, i in idx.items()}, V_over_V0={k: float(V[i] / V[-1]) for k, i in idx.items()}, c_eff=float(lam * Vc[-1] / V[-1]), E0=float(E2[-1]))
    return E
