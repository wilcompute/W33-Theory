"""Pass 11938: the second small parameter -- distance from the reducible (product-torus) locus gives the geometric up
texture (1, theta, theta^2), and its O(1) coefficient is a Weber modular function of the two elliptic factors.

Setting: the E8 Cartan vev c = (1, t u) off a Witting ray, inverted to the Siegel modulus (Passes 11879/11891, V.invert)
and the level-3 theta Yukawa Y = theta_null_2(Omega) reshaped 3 x 3 (Passes 11869/11936).

1. The polar line of the stabiliser state. For every tangent direction u orthogonal to the stabiliser state e1 = (1,0,0)
   (any magic: the strange circle (0,1,e^{i phi})/sqrt2 with M2 = log 2, and random (0,x,y) with M2 = 0.38-0.69) and every
   t the theta Yukawa is EXACTLY rank one (s2 ~ 1e-18 where the inversion converges to 1e-16; s2 <~ sqrt(residual)
   otherwise): the Cartan 3-plane spanned by the Witting ray and e1-perp maps into the reducible locus (product theta <=>
   factorised torus, Passes 11869-11873). Minimising m_u/m_c = s3/s2 over CP^2 converges onto this line (0.001 reached).
   This sharpens Pass 11936, which read these directions as a "deeper cusp with a locked pair": the pair is in fact zero.
2. Geometric exponents. Off the line by an angle theta = arcsin|u1| the spectrum is (1, A theta t, B theta^2 t) near
   the Witting ray: exponents (0, 1, 2) in theta, versus (0, 1, 1) in t (Pass 11936). theta is the second small
   parameter; it is the off-diagonal modulus Omega12 (the family Wilson line of Pass 11912).
3. The Weber law. Near a product torus diag(tau1, tau2), the heat-equation expansion
   Y = sum_k (6 pi i Omega12)^k / k! f_k(tau1) (x) f_k(tau2),   f_k(tau)_c = sum_n (n + c/3)^k e^{3 pi i tau (n + c/3)^2},
   has f_1 = (0, x, -x) (the strange state) orthogonal to the even f_0, f_2, and gives the Omega12-independent invariant
        m_u m_t / m_c^2 = s1 s3 / s2^2 = |f(tau1) f(tau2)|^8 / 4,
   with f the Weber function (f^24 a root of (x - 16)^3 = j x); equivalently gamma(tau) = |eta(tau)^2/(eta(tau/2) eta(2 tau))|^8/sqrt2.
   Exact values: (i, i) -> 4, (w, w) -> 2^(2/3), (i, w) -> 2^(4/3), (1+i, 1+i) -> 1; over all frames of the two elliptic
   points |f|^8 is in {2, 4, 2^(4/3)}, so a product of CM elliptic factors gives m_u m_t/m_c^2 >= 1.
4. Confrontation. Data: m_u m_t/m_c^2 = 0.54 at M_Z (m_u = 1.23 MeV, m_c = 0.620 GeV, m_t = 168.3 GeV; ~ +-20% from m_u).
   * Elliptic (CM) factors: >= 1 -- EXCLUDED (the E8-selected square boundary curve gives the factor 2 sqrt2 alone).
   * The E8 cusp regime (small t, where the soft supertrace puts the vacuum): R ~ 0.9/t along the strange-perturbed
     direction, >> 1 -- EXCLUDED there. Search-based floor over ALL directions: min_u R t = 0.7999 at t = 0.005
     (6 Nelder-Mead runs; 4 reach 0.80-0.81 near the T / log(9/5) orbit, 2 stall at 0.88), so m_u m_t/m_c^2 >~ 0.8/t
     near any Witting ray: with m_c/m_t = 3.6e-3 this needs t >~ 1.5, outside the cusp regime.
   * Reachable at most at t = O(1), where R depends on the branch of the Coble/Maschke inversion (phi = pi, t = 0.3 / 1:
     2.78 / 0.148 on one branch, 3.23 / 5.28 on another; small-t values are branch-independent) -- a fit, not a
     prediction; and the E8 angular selector disfavours the strange direction (C_G = 5.047, the largest, Pass 11935).
Reading: the up texture's SHAPE is geometric (Omega12 is the second small parameter, exponents (0,1,2)); its coefficient
is modular (Weber), and the special (CM / E8-cusp) values miss the data by a factor >= 1.8.
"""

import json
import sys
from pathlib import Path

import mpmath as mp
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11890_11892_vacuum_phase_diagram as V  # noqa: E402
import w33_pass11923_stabiliser_higgs_lock as H23  # noqa: E402
from w33_pass11869_11873_siegel_level3_two_qutrits import j_of_tau, theta_null_2  # noqa: E402

OUT = ROOT / "data" / "w33_pass11938_weber_up_texture.json"
W = np.exp(2j * np.pi / 3)
E1 = np.array([1, 0, 0], complex)
R_DATA = 1.23e-3 * 168.26 / 0.620**2


def eta(t):
    return complex(mp.exp(2j * mp.pi * t / 24) * mp.qp(mp.exp(2j * mp.pi * t)))


def weber(t):
    return np.exp(-1j * np.pi / 24) * eta((t + 1) / 2) / eta(t)


def spec(Om):
    sv = np.linalg.svd(theta_null_2(Om, N=60).reshape(3, 3), compute_uv=False)
    return sv / sv[0]


def r_product(t1, t2, eps=1e-4):
    sv = spec(np.array([[t1, eps], [eps, t2]]))
    return float(sv[2] / sv[1] ** 2)


def perp_samples(rng):
    out = [np.array([0, 1, np.exp(1j * phi)]) / np.sqrt(2) for phi in (np.pi, 0.0, 1.0484)]
    for _ in range(3):
        v = rng.normal(size=2) + 1j * rng.normal(size=2)
        out.append(np.r_[0, v] / np.linalg.norm(v))
    return out


def strange(phi):
    return np.array([0, 1, np.exp(1j * phi)]) / np.sqrt(2)


def cartan_spec(u, t, rng, guess=None):
    c = np.r_[1, t * u]
    c = c / np.linalg.norm(c)
    Om, res, guess = V.invert(c, rng, guess)
    return spec(Om), float(res), guess


def main():
    rng = np.random.default_rng(11938)
    res = dict(pass_id=11938, R_data_MZ=R_DATA)
    circ = []
    for u in perp_samples(rng):
        for t in (0.01, 0.5):
            sv, r, _ = cartan_spec(u, t, rng)
            circ.append(dict(u_re=u.real.tolist(), u_im=u.imag.tolist(), t=t, residual=r, s2=float(sv[1]),
                             M2=float(H23.magic(u))))
    res["stabiliser_polar_line"] = circ
    th_rows, g = [], None
    for th in (0.1, 0.03, 0.01):
        u = np.cos(th) * strange(np.pi) + np.sin(th) * E1
        for t in (0.01, 0.005):
            sv, r, g = cartan_spec(u, t, rng, g)
            th_rows.append(dict(theta=th, t=t, residual=r, s2=float(sv[1]), s3=float(sv[2])))
    res["theta_scan"] = th_rows
    pick = lambda th, t, k: next(x[k] for x in th_rows if x["theta"] == th and x["t"] == t)
    res["theta_slopes"] = [float(np.log(pick(0.1, 0.01, k) / pick(0.01, 0.01, k)) / np.log(10)) for k in ("s2", "s3")]
    res["t_slopes"] = [float(np.log(pick(0.03, 0.01, k) / pick(0.03, 0.005, k)) / np.log(2)) for k in ("s2", "s3")]
    weber_err = []
    for _ in range(10):
        t1, t2 = [rng.uniform(-1, 1) + 1j * rng.uniform(0.5, 2) for _ in range(2)]
        eps = 1e-4 * np.exp(1j * rng.uniform(0, 2 * np.pi))
        weber_err.append(abs(r_product(t1, t2, eps) / (abs(weber(t1) * weber(t2)) ** 8 / 4) - 1))
    res["weber_law_max_rel_err"] = float(max(weber_err))
    cub = []
    for t in (1j, W, 0.3 + 0.9j, -0.2 + 1.4j):
        x = weber(t) ** 24
        cub.append(abs((x - 16) ** 3 - j_of_tau(t) * x) / max(1, abs(j_of_tau(t) * x)))
    res["weber_cubic_max_err"] = float(max(cub))
    ell = {"i,i": (1j, 1j, 4.0), "w,w": (W, W, 2 ** (2 / 3)), "i,w": (1j, W, 2 ** (4 / 3)), "1+i,1+i": (1 + 1j, 1 + 1j, 1.0)}
    res["elliptic_values"] = {k: r_product(a, b) for k, (a, b, _) in ell.items()}
    frames = {"i": set(), "w": set()}
    for base, key in ((1j, "i"), (W, "w")):
        stack = [(base, 0)]
        while stack:
            t, d = stack.pop()
            if t.imag >= 0.3:
                frames[key].add(round(abs(weber(t)) ** 8, 8))
            if d < 4:
                stack += [(-1 / t, d + 1), (t + 1, d + 1), (t - 1, d + 1)]
    res["elliptic_frame_f8_values"] = {k: sorted(v) for k, v in frames.items()}
    fmin = min(min(v) for v in frames.values())
    cusp, g = [], None
    for t in (0.03, 0.1, 0.3, 1.0):
        u = np.cos(0.01) * strange(np.pi) + np.sin(0.01) * E1
        sv, r, g = cartan_spec(u, t, rng, g)
        cusp.append(dict(t=t, residual=r, R=float(sv[2] / sv[1] ** 2)))
    res["strange_plane_R"] = cusp
    res["checks"] = {k: bool(v) for k, v in dict(
        circle_is_log2_random_is_not=all(abs(x["M2"] - np.log(2)) < 1e-12 for x in circ[:6])
        and any(abs(x["M2"] - np.log(2)) > 1e-3 for x in circ[6:]),
        polar_line_rank_one=all(x["s2"] <= 20 * np.sqrt(x["residual"]) + 1e-12 and x["residual"] < 1e-9 for x in circ)
        and 100 * max(x["s2"] for x in circ) < pick(0.1, 0.01, "s2"),        # control: theta = 0.1 off the line
        geometric_exponents_012_in_theta=abs(res["theta_slopes"][0] - 1) < 0.05 and abs(res["theta_slopes"][1] - 2) < 0.05,
        exponents_11_in_t=all(abs(s - 1) < 0.03 for s in res["t_slopes"]),
        weber_law=res["weber_law_max_rel_err"] < 1e-6,
        weber_cubic=res["weber_cubic_max_err"] < 1e-10,
        elliptic_exact_values=all(abs(res["elliptic_values"][k] / v[2] - 1) < 1e-6 for k, v in ell.items()),
        elliptic_frames_f8=set(round(x, 6) for v in frames.values() for x in v) == {2.0, 4.0, round(2 ** (4 / 3), 6)},
        cm_products_excluded=fmin ** 2 / 4 >= 1 - 1e-9 > R_DATA * 1.5,
        cusp_regime_R_over_t=all(abs(x["R"] * x["t"] - 0.89) < 0.03 for x in cusp[:2]) and cusp[0]["R"] > 20 * R_DATA,
        R_falls_towards_order_one_t=min(cusp[2]["R"], cusp[3]["R"]) < cusp[0]["R"] / 5,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"], res["theta_slopes"], res["t_slopes"],
          res["elliptic_values"], res["elliptic_frame_f8_values"], [round(x["R"], 3) for x in cusp])


if __name__ == "__main__":
    main()
