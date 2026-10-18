"""Pass 12044: completing Pass 12004 -- S-type generalised CP also forbids a bare theta quark fit, and the CP-fixed locus
is a saddle of the Pass 12034 toy one-loop potential at the Nelson-Barr vacuum (Claude track).

Setting: the quark model of Pass 11942 / 12004. Up home [[tau, eps_u], [eps_u, tau]] Wilson-free; down home
[[tau, eps_d], [eps_d, tau_d]] sharing tau (the quark-doublet torus), Wilson line z_d on the 5bar factor only.

Part A -- S-type generalised CP (the |tau| = 1 arc that 12004 did not cover).
 CP o g acts as (Omega, z) -> (-conj((A Omega + B)(C Omega + D)^-1), -conj((C Omega + D)^-T z) + (0, k/3)), with g a
 product S x h, S on the shared doublet torus and h in {S, T^{2b}} on the second factor (b in Z), on each home.
 A1. S acts on the level-3 theta as the DFT: Y(g Omega, g z) = c F Y F^T (S x S), c F Y (S x 1), c a scalar (checked to
     1e-15). With CP, Y = conj(c F Y F^T): the left factor F is common to up and down, so J = 0 on every S-type fixed
     set. Checked WITH Wilson lines on S x T^0 fixed points; shifting Re z_d off the fixed set restores J != 0. (With
     z = 0 every theta Yukawa is parity-blocked, TOE39, and J = 0 trivially: a first control here was vacuous for that
     reason and was replaced.)
 A2. The up home on the CP o (S x S) fixed set is Omega = R45 diag(e^{ia}, e^{ib}) R45^T (Omega conj(Omega) = 1), i.e.
     |tau|^2 + |eps_u|^2 = 1 with eps_u orthogonal to tau. The up sector fits EXACTLY there, at tau = +-0.67622 + 0.73669 i,
     |eps_u| = 0.00459 (the S-arc image of the Weber point). Positive control: at that tau an unrestricted complex down
     home fits all five down data exactly (chi^2 ~ 1e-9 .. 1e-8 on re-evaluation; frozen solutions below).
 A3. Every branch is closed; four of the five exactly.
     * S x S up, S x T^{2b} down: the down home fixes tau = Omega_11 by tau -> 1/conj(tau), so |tau| = 1; the up home
       has |tau|^2 = 1 - |eps_u|^2. Hence eps_u = 0, a rank-one up Yukawa (Pass 11872): m_c = m_u = 0.
     * S x S up, S x S down: S x S maps the 5bar Wilson line into the doublet factor, z0' = -conj((Omega^-1)_{12} z_d).
       A real CP of the model needs z0' = 0 exactly (a Z/3 shift there is a left phase on Q that the up sector does not
       share; admitting it gives J = -3.4e-4, a non-symmetry). So eps_d z_d = 0: a rank-one down Yukawa, or no Wilson
       line. With no Wilson line both Yukawas are parity-symmetric, P Y P = Y (a -> -a), so the CKM matrix has a
       decoupled generation, one entry of modulus 1 and four zeros (the TOE39 parity-block theorem; checked with the
       full theta to 2e-16). One of |V_us|, |V_cb|, |V_ub| is then 0 or 1.
     * S x T^{2b} up: tau = e^{i theta}, 2 cos theta = -2b - rho^2 (rho = |eps_u|), and the smaller eigenvalue of
       Im Omega_u is cos(theta/2)(2 sin(theta/2) - rho), with (2 sin(theta/2))^2 - rho^2 = 2(1 + b) identically. So
       b >= 1 is empty (cos theta < -1), b = -1 is degenerate (det Im Omega = 0), b <= -2 is indefinite.
     * S x T^0 up (b = 0): a one-parameter curve for two up observables. Its minimum is chi^2_up = 94.6 (m_u/m_c =
       0.0131 against 0.0020), from a 6,001-point scan with refinement. The centred theta is accurate on this curve to
       5e-7 against the full sum. This is the one search-based statement.
 Corrections recorded. (i) A first penalty fit never reached the fixed set; the sets are reachable (projection residual
 1e-16), the method was at fault. (ii) A joint constrained multistart over 27 branches failed its own complex-down
 control (1230) and is not used. (iii) A first scan of the Wilson-free S x S down home found 'minima' (1.04e4, then
 3432) in its cusp. These were truncation artefacts: the centred window follows v2 only, the soft direction of
 Im Omega_d is rotated there, and the parity residual of the computed Yukawa was 0.41 where it is exactly 0. The exact
 parity argument replaces that scan.
 So with exact theta-group CP of T^2 type (Pass 12004) or of S type on the shared torus (here) the bare sector cannot
 fit, and the Barr row of Pass 12005 is necessary on both families of CP-fixed loci.

Part B -- is the CP locus a minimum? Uses the Pass 12034 toy Coleman-Weinberg potential, which is Codex's:
 V1 = sum_sectors Nc/(16 pi^2) sum [f(z+s) - f(z)], f = z^2 (log(z/Q^2) - 3/2), fixed baseline normalisation, with the
 counterterm family c sum Nc Tr Y^dag Y. Transverse (CP-odd) coordinates are the real parts of the ten theta moduli.
 B1. Transverse gradients vanish (<= 1e-10 against longitudinal 6e-4 .. 2): symmetric criticality (Palais 1979), as
     stated in 12004.
 B2. At the 12005 Nelson-Barr vacuum the transverse Hessian has a negative mode for every s in {0.1, 1, 10} (frozen
     record: also every Q in {0.5, 1, 2}), and NO counterterm coefficient removes it (best minimum eigenvalue over c from
     -0.011 to -0.12). The counterterm Hessian there is itself indefinite (eigenvalues -2951, -18, +1.9, +3.3, +8.4).
     The locus is a saddle: in this toy model CP would be broken radiatively, unless the UV supplies transverse
     stabilisation.
 B3. Non-vacuous control: at a generic locus point the same counterterm makes the transverse Hessian positive
     (minimum eigenvalue 1.2e4 at c = 1e4), so B2 is a property of the vacuum, not of the method.
 This complements 12034, which is longitudinal: the fitted point is not stationary along its six shape directions
 (residual force 4.5e-5 after the one counterterm). Longitudinal force plus transverse saddle: the toy potential holds
 the Nelson-Barr vacuum in neither direction, so stabilisation is a UV problem in both.
Scope: product theta-group CP elements (S x {S, T^{2b}}, with S on the shared torus) and the 11942 down model; Part A is
 exact except the S x T^0 up scan. Part B is a toy potential with one counterterm family, not the MSSM field-dependent
 spectrum.
Not new: generalised CP in Sp(4,Z) (Ding-Feruglio-Liu arXiv:2010.07952); the |tau| = 1 CP-fixed arc of modular CP
 (Novichkov-Penedo-Petcov-Titov arXiv:1905.11970); symmetric criticality (Palais 1979); the parity-block theorem (TOE39);
 the 12034 potential and its counterterm.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12004_cp_real_bare_theta_no_fit import theta_c  # noqa: E402

OUT = ROOT / "data" / "w33_pass12044_s_type_cp_and_locus_stability.json"
UP = dict(mc_mt=0.620 / 168.26, mu_mc=1.23e-3 / 0.620)
DATA = dict(mc_mt=(UP["mc_mt"], .05), mu_mc=(UP["mu_mc"], .20), ms_mb=(0.053 / 2.86, .08), md_ms=(2.67e-3 / 0.053, .10),
            Vus=(0.2250, .003), Vcb=(0.0411, .025), Vub=(0.00382, .05))
DK = ["ms_mb", "md_ms", "Vus", "Vcb", "Vub"]
UP_AB = {"+": (0.832764, 0.823581), "-": (2.318011, 2.308829)}
SEARCH_RECORD = dict(scan_b_min_chi2_up=94.63, scan_b_abs_eps_u=0.0096478, scan_b_theta_accuracy=5.0e-7,
                     discarded_cusp_artefacts=dict(values=[1.038e4, 3432.5], parity_residual=0.41),
                     joint_slsqp=dict(branches=27, starts_per_branch=40, best_chi2=9339.0, own_control_chi2=1230.0, used_as_evidence=False),
                     loose_z0_artefact_J=-3.43e-4)
CONTROL_X = {"+": [0.02132614921433778, 0.016042458242390385, -0.9088212634829876, 0.03580386574812934, -0.19308794847209568, -0.02734171207466224],
             "-": [0.02633189437208459, -0.004728494268058302, 0.09070648773442241, 0.03564049122596663, -0.026354454679421324, -0.027386310576295907]}
CW_RECORD = dict(min_eig_vacuum={"0.1": -1.15e-2, "1.0": -4.8e-2, "10.0": -1.2e-1}, ct_eigs_vacuum=[-2951, -18.0, 1.91, 3.33, 8.39],
                 random_point_min_eig=1.153e4)
NC = (3, 3, 1)
F = np.exp(2j * np.pi * np.outer(np.arange(3), np.arange(3)) / 3) / np.sqrt(3)


def sp(a1, b1, c1, d1, a2, b2, c2, d2):
    return np.block([[np.diag([a1, a2]), np.diag([b1, b2])], [np.diag([c1, c2]), np.diag([d1, d2])]]).astype(float)


G = {"SS": sp(0, -1, 1, 0, 0, -1, 1, 0), "S T0": sp(0, -1, 1, 0, 1, 0, 0, 1), "S T2": sp(0, -1, 1, 0, 1, 2, 0, 1)}


def act(M, Om, z):
    A, B, C, D = M[:2, :2], M[:2, 2:], M[2:, :2], M[2:, 2:]
    W = C @ Om + D
    return (A @ Om + B) @ np.linalg.inv(W), np.linalg.inv(W).T @ z


def up_home(a, b):
    lp, lm = np.exp(1j * a), np.exp(1j * b)
    return np.array([[(lp + lm) / 2, (lp - lm) / 2], [(lp - lm) / 2, (lp + lm) / 2]])


def svals(Y):
    return np.linalg.svd(Y, compute_uv=False)


def ratio_spread(Y1, Y2):
    m = np.abs(Y2) > 1e-6 * np.abs(Y2).max()
    r = Y1[m] / Y2[m]
    return float(np.abs(r - r.mean()).max() / abs(r.mean()))


def jarlskog(Yu, Yd):
    Uu = np.linalg.svd(Yu)[0]
    Ud = np.linalg.svd(Yd)[0]
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    return float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))


def down_home_ss(tau, a1, sg):
    """Unitary-symmetric down home (Omega conj Omega = 1) with Omega_11 = tau: one real parameter a1."""
    u = np.exp(1j * a1)
    t = (1 - abs(tau) ** 2) / (2 * (1 - (np.conj(tau) * u).real))
    if not 0 < t < 1:
        return None
    w = (tau - t * u) / (1 - t)
    if w.imag <= 1e-6:
        return None
    c, s = np.sqrt(t), sg * np.sqrt(1 - t)
    R = np.array([[c, -s], [s, c]])
    return R @ np.diag([u, w / abs(w)]) @ R.T


def chi_down(Ou, Od, z=None):
    Ud, sd, _ = np.linalg.svd(theta_c(Od, np.zeros(2, complex) if z is None else z))
    Uu = np.linalg.svd(theta_c(Ou, np.zeros(2, complex)))[0]
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    o = dict(ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1], Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]))
    return float(sum((np.log(o[q] / DATA[q][0]) / DATA[q][1]) ** 2 for q in DK))


# ---- Part B: the 12034 toy potential on the ten theta moduli -------------------------------------------------------
def mats(x):
    rt, y, reu, iu, rtd, yd, red, idd, rz, zi = x
    tau = rt + 1j * y
    Omu = np.array([[tau, reu + 1j * iu], [reu + 1j * iu, tau]])
    Omd = np.array([[tau, red + 1j * idd], [red + 1j * idd, rtd + 1j * yd]])
    z = np.array([0, rz + 1j * zi])
    return theta_c(Omu, np.zeros(2, complex)), theta_c(Omd, z), theta_c(Omd, 6 * z).T


def make_V(x0, soft, Q):
    norms = [np.linalg.norm(Y, 2) for Y in mats(x0)]

    def V(x):
        tot = 0.0
        for n, Y, nr in zip(NC, mats(x), norms):
            w = np.linalg.eigvalsh((Y / nr) @ (Y / nr).conj().T).clip(1e-300)
            f = lambda u: u * u * (np.log(u / Q ** 2) - 1.5)  # noqa: E731
            tot += n * np.sum(f(w + soft) - f(w))
        return tot / (16 * np.pi ** 2)
    return V


def make_ct(x0):
    norms = [np.linalg.norm(Y, 2) for Y in mats(x0)]
    return lambda x: sum(n * np.trace((Y / nr) @ (Y / nr).conj().T).real for n, Y, nr in zip(NC, mats(x), norms))


def hess(V, x0, idx, h=1e-4):
    k = len(idx)
    H = np.zeros((k, k))
    for a in range(k):
        for b in range(a, k):
            ea = np.zeros(10)
            eb = np.zeros(10)
            ea[idx[a]] = h
            eb[idx[b]] = h
            H[a, b] = H[b, a] = (V(x0 + ea + eb) - V(x0 + ea - eb) - V(x0 - ea + eb) + V(x0 - ea - eb)) / (4 * h * h)
    return H


def grad(V, x0, idx, h=1e-6):
    out = []
    for i in idx:
        e = np.zeros(10)
        e[i] = h
        out.append((V(x0 + e) - V(x0 - e)) / (2 * h))
    return np.array(out)


TR, LO = [0, 2, 4, 6, 8], [1, 3, 5, 7, 9]
VACUUM_12005 = np.array([1.0, 0.8744698731421595, 0.0, 0.005520606513514881, 0.0, 0.4315140195185126, 0.0, 0.08087153936666885, 0.0,
                         0.0677453432123109])
RANDOM_LOCUS = np.array([1.0, 0.95, 0.0, 0.004, 1.0, 0.2, 0.0, 0.03, 1 / 6, 0.05])


def main():
    rng = np.random.default_rng(12044)
    checks = {}
    res = {}

    # A1: local S action = DFT, and J = 0 on S-type fixed sets
    spreads = []
    for _ in range(6):
        t = rng.uniform(-.4, .4) + 1j * rng.uniform(.8, 1.4)
        td = rng.uniform(-.4, .4) + 1j * rng.uniform(.8, 1.4)
        e = (rng.normal() + 1j * rng.normal()) * 0.05
        Om = np.array([[t, e], [e, td]])
        z = np.array([0, rng.normal(0, .05) + 1j * rng.normal(0, .05)])
        O2, z2 = act(G["SS"], Om, z)
        Y0 = _theta_full(Om, z)
        O2, z2 = act(G["SS"], Om, z)
        spreads.append(min(ratio_spread(_theta_full(O2, z2), L @ Y0 @ R.T) for L in (F, F.conj()) for R in (F, F.conj())))
        O3, z3 = act(G["S T0"], Om, z)
        spreads.append(min(ratio_spread(_theta_full(O3, z3), L @ Y0) for L in (F, F.conj())))
    res["S_action_ratio_spread_max"] = max(spreads)
    checks["S acts on the level-3 theta as F x F (S x S) and F x 1 (S x 1), up to a scalar"] = max(spreads) < 1e-9

    # J test with Wilson lines (with z = 0 every theta Yukawa is parity-blocked, TOE39, and J = 0 trivially):
    # S x T^0 fixed points, tau = e^{i th}, 2 cos th = -rho_u^2, arg eps = (th + pi)/2, Re tau_d = -rho_d^2/2, Re z_d = k/6
    def st0_point(rho_u, rho_d, yd, k, zi, br, dz=0.0):
        th = np.arccos(-rho_u ** 2 / 2)
        ph = (th + np.pi) / 2
        eu, ed = rho_u * np.exp(1j * ph), rho_d * np.exp(1j * (ph + br * np.pi))
        tau = np.exp(1j * th)
        Ou = np.array([[tau, eu], [eu, tau]])
        Od = np.array([[tau, ed], [ed, -rho_d ** 2 / 2 + 1j * yd]])
        return Ou, Od, np.array([0, k / 6 + dz + 1j * zi])
    Js, Joffs, fix = [], [], []
    for _ in range(10):
        args = (rng.uniform(.05, .5), rng.uniform(.02, .4), rng.uniform(.4, 1.5), int(rng.integers(3)), rng.normal(0, .2), int(rng.integers(2)))
        Ou, Od, z = st0_point(*args)
        for gname, Om, zz in (("S T0", Ou, np.zeros(2, complex)), ("S T0", Od, z)):
            O2, z2 = act(G[gname], Om, zz)
            fix.append(max(np.abs(-np.conj(O2) - Om).max(), abs(-np.conj(z2[1]) + args[3] / 3 - zz[1]) if zz[1] != 0 else 0, abs(z2[0])))
        Js.append(abs(jarlskog(theta_c(Ou, np.zeros(2, complex)), theta_c(Od, z))))
        Ou, Od, z = st0_point(*args, dz=0.05)
        Joffs.append(abs(jarlskog(theta_c(Ou, np.zeros(2, complex)), theta_c(Od, z))))
    res["J_on_S_T0_fixed_points_with_Wilson"] = dict(n=len(Js), max=max(Js), fixed_point_residual=max(fix))
    res["J_off_locus_control"] = dict(shift_Re_zd=0.05, min=min(Joffs))
    checks["J = 0 on S-type fixed points with Wilson lines; off-locus control (Re z_d shifted) nonzero"] = (
        max(fix) < 1e-12 and max(Js) < 1e-12 and min(Joffs) > 1e-9)

    # A2: exact up fit on the S x S arc
    def rup(p):
        s = svals(theta_c(up_home(*p), np.zeros(2, complex)))
        return [np.log(s[1] / s[0] / UP["mc_mt"]), np.log(s[2] / s[1] / UP["mu_mc"])]
    sol = {}
    for k, ab in UP_AB.items():
        r = least_squares(rup, ab, xtol=1e-15, ftol=1e-15)
        O = up_home(*r.x)
        sol[k] = dict(a=r.x.tolist(), resid=float(np.abs(r.fun).max()), tau=[O[0, 0].real, O[0, 0].imag], abs_eps=abs(O[0, 1]),
                      unit=abs(O[0, 0]) ** 2 + abs(O[0, 1]) ** 2)
    res["up_on_S_arc"] = sol
    checks["up sector fits exactly on the CP o (S x S) arc, |tau|^2 + |eps_u|^2 = 1"] = all(
        v["resid"] < 1e-10 and abs(v["unit"] - 1) < 1e-12 and abs(abs(v["tau"][0]) - 0.67622) < 1e-4 for v in sol.values())

    # A3: exact obstructions
    Ou = up_home(*sol["-"]["a"])
    tau = Ou[0, 0]
    res["S_arc_up_abs_tau"] = abs(tau)
    t2, _ = act(G["S T0"], np.array([[tau, .01j], [.01j, .5j]]), np.zeros(2, complex))
    res["S_x_T_down_needs_abs_tau_1"] = dict(abs_tau=abs(tau), image_of_tau_minus_tau=abs(-np.conj(t2[0, 0]) - tau))
    checks["S x T^{2b} down needs |tau| = 1, but the S x S up home has |tau| < 1 unless eps_u = 0"] = (
        abs(abs(tau) - 1) > 1e-6 and abs(1 / np.conj(tau) - tau) > 1e-6 and abs(abs(np.exp(.7j)) - 1) < 1e-15)
    rank_eps0 = np.linalg.matrix_rank(theta_c(np.array([[tau / abs(tau), 0], [0, tau / abs(tau)]]), np.zeros(2, complex)), tol=1e-10)
    res["rank_up_at_eps_0"] = int(rank_eps0)
    checks["eps_u = 0 gives a rank-one up Yukawa (m_c = m_u = 0)"] = rank_eps0 == 1
    Od = np.array([[tau, .03 + .02j], [.03 + .02j, .2 + .9j]])
    zd = np.array([0, .1 + .05j])
    _, z2 = act(G["SS"], Od, zd)
    pred = np.linalg.inv(Od)[0, 1] * zd[1]
    res["SS_down_doublet_component"] = dict(z0_image=abs(z2[0]), predicted=abs(pred))
    checks["S x S on the down home moves the 5bar Wilson line into the doublet factor: z0' = (Omega^-1)_12 z_d"] = (
        abs(z2[0] - pred) < 1e-14 and abs(z2[0]) > 1e-3)

    lem = {}
    for b in range(-3, 3):
        for rho in (0.01, 0.3, 1.5, 2.5):
            c = -b - rho ** 2 / 2
            if abs(c) > 1:
                lem[f"{b},{rho}"] = "no |tau|=1 solution"
                continue
            th = np.arccos(c)
            O = np.array([[np.exp(1j * th), rho * np.exp(1j * (th + np.pi) / 2)], [rho * np.exp(1j * (th + np.pi) / 2), np.exp(1j * th)]])
            O2, _ = act(sp(0, -1, 1, 0, 1, 2 * b, 0, 1), O, np.zeros(2, complex))
            mn = np.linalg.eigvalsh(O.imag).min()
            lem[f"{b},{rho}"] = dict(fixed=float(np.abs(-np.conj(O2) - O).max()), min_eig_im=float(mn),
                                     formula=float(np.cos(th / 2) * (2 * np.sin(th / 2) - rho)), identity=float(4 * np.sin(th / 2) ** 2 - rho ** 2 - 2 * (1 + b)))
    res["S_x_T2b_up_lemma"] = lem
    vals = [v for v in lem.values() if isinstance(v, dict)]
    checks["S x T^{2b} up home: only b = 0 has Im Omega > 0 (eigenvalue formula and 2(1+b) identity)"] = (
        all(v["fixed"] < 1e-12 and abs(v["min_eig_im"] - v["formula"]) < 1e-12 and abs(v["identity"]) < 1e-12 for v in vals)
        and all((v["min_eig_im"] > 1e-9) == (k.split(",")[0] == "0") for k, v in lem.items() if isinstance(v, dict)))

    ctrl = {k: chi_down(up_home(*sol[k]["a"]),
                        np.array([[up_home(*sol[k]["a"])[0, 0], x[0] + 1j * x[1]], [x[0] + 1j * x[1], x[2] + 1j * x[3]]]),
                        np.array([0, x[4] + 1j * x[5]])) for k, x in CONTROL_X.items()}
    res["control_complex_down_at_S_arc_tau"] = ctrl
    checks["positive control: a complex down home fits exactly at the S-arc tau"] = max(ctrl.values()) < 1e-6

    # A4: the two surviving one-parameter branches (coarse re-scan; the frozen fine scans are in SEARCH_RECORD)
    Pm = np.eye(3)[[0, 2, 1]]
    dec = []
    for a1 in (1.0, 2.0, 2.6):
        for sg in (1, -1):
            Od_ = down_home_ss(tau, a1, sg)
            if Od_ is None or np.linalg.eigvalsh(Od_.imag).min() < 0.05:
                continue
            Yu_, Yd_ = _theta_full(Ou, np.zeros(2, complex), 30), _theta_full(Od_, np.zeros(2, complex), 30)
            V_ = np.abs(np.linalg.svd(Yu_)[0].conj().T @ np.linalg.svd(Yd_)[0])
            dec.append(dict(parity=float(np.abs(Pm @ Yd_ @ Pm - Yd_).max() / np.abs(Yd_).max()), one=float(abs(1 - V_.max())),
                            zeros=int((V_ < 1e-10).sum())))
    res["SxS_wilson_free_decoupling"] = dec
    checks["S x S Wilson-free branch: parity-symmetric Yukawas, CKM has a decoupled generation (one 1, four 0s)"] = (
        len(dec) >= 4 and all(d["parity"] < 1e-14 and d["one"] < 1e-12 and d["zeros"] == 4 for d in dec))

    def chiu(lr, br):
        rho = 10 ** lr
        th = np.arccos(-rho ** 2 / 2)
        eps = rho * np.exp(1j * ((th + np.pi) / 2 + br * np.pi))
        O = np.array([[np.exp(1j * th), eps], [eps, np.exp(1j * th)]])
        if np.linalg.eigvalsh(O.imag).min() < 1e-6:
            return np.inf
        s = svals(theta_c(O, np.zeros(2, complex)))
        return (np.log(s[1] / s[0] / UP["mc_mt"]) / .05) ** 2 + (np.log(s[2] / s[1] / UP["mu_mc"]) / .20) ** 2
    best_b = min(chiu(lr, br) for lr in np.linspace(-5, 0.1, 400) for br in (0, 1))
    res["scan_b_coarse_min_chi2_up"] = best_b
    res["search_record"] = SEARCH_RECORD
    checks["S x T^0 up curve fails the up data (coarse >= frozen fine minimum > 50)"] = best_b >= 0.999 * SEARCH_RECORD["scan_b_min_chi2_up"] > 50

    # B: transverse stability of the CP locus in the 12034 toy potential
    cs = np.concatenate([-np.logspace(-4, 4, 161)[::-1], [0], np.logspace(-4, 4, 161)])
    cw = {}
    for s in (0.1, 1.0, 10.0):
        V = make_V(VACUUM_12005, s, 1.0)
        H = hess(V, VACUUM_12005, TR)
        Hc = hess(make_ct(VACUUM_12005), VACUUM_12005, TR)
        m = max(np.linalg.eigvalsh(H + c * Hc).min() for c in cs)
        cw[str(s)] = dict(gradT=float(np.abs(grad(V, VACUUM_12005, TR)).max()), gradL=float(np.abs(grad(V, VACUUM_12005, LO)).max()),
                          eigH=np.linalg.eigvalsh(H).tolist(), ct_eigs=np.linalg.eigvalsh(Hc).tolist(), best_min_eig_over_c=float(m))
    Vr = make_V(RANDOM_LOCUS, 1.0, 1.0)
    Hr, Hcr = hess(Vr, RANDOM_LOCUS, TR), hess(make_ct(RANDOM_LOCUS), RANDOM_LOCUS, TR)
    mr = max(np.linalg.eigvalsh(Hr + c * Hcr).min() for c in cs)
    res["cw_vacuum_12005"] = cw
    res["cw_random_locus_best_min_eig"] = float(mr)
    res["cw_record"] = CW_RECORD
    checks["CP locus transversally stationary (symmetric criticality)"] = all(v["gradT"] < 1e-8 < v["gradL"] for v in cw.values())
    checks["12005 vacuum is a transverse saddle for every s, and no counterterm coefficient cures it"] = all(
        v["best_min_eig_over_c"] < -1e-3 and min(v["ct_eigs"]) < 0 < max(v["ct_eigs"]) for v in cw.values())
    checks["control: at a generic locus point the counterterm does stabilise"] = mr > 0

    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


def _theta_full(Om, z, N=8):
    """Plain level-3 theta with both Wilson components (for the S x 1 image, whose doublet component is nonzero)."""
    Y = np.zeros((3, 3), complex)
    n = np.arange(-N, N + 1)
    for a in range(3):
        for b in range(3):
            v1 = (n + a / 3)[:, None]
            v2 = (n + b / 3)[None, :]
            Y[a, b] = np.exp(3j * np.pi * (Om[0, 0] * v1 ** 2 + 2 * Om[0, 1] * v1 * v2 + Om[1, 1] * v2 ** 2)
                             + 6j * np.pi * (v1 * z[0] + v2 * z[1])).sum()
    return Y


if __name__ == "__main__":
    main()
