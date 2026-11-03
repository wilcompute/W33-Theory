"""Two-loop Standard Model RGEs from mu = M_t upward (g_Y, g_2, g_3, y_t, lambda; V = lambda |H|^4), with the NNLO matching of Buttazzo et al. (arXiv:1307.3536).  The one-loop y_b and y_tau are carried as spectators.
Control: y_t(M_Pl), g_i(M_Pl), lambda(M_Pl) against the published eq. 61 of that paper at its reference point.  Two loops only, so lambda(M_Pl) can differ at the 10^-3 level; the difference is reported and not hidden.
usage: py -3 sm_rge.py"""
import json
import math
from scipy.integrate import solve_ivp

K = 1 / (16 * math.pi ** 2)
MPL_BUTTAZZO = 1.22e19


def matching(mt=173.34, mh=125.15, a3=0.1184, mw=80.384):
    return dict(
        gY=0.35830 + 0.00011 * (mt - 173.34) - 0.00020 * (mw - 80.384) / 0.014,
        g2=0.64779 + 0.00004 * (mt - 173.34) + 0.00011 * (mw - 80.384) / 0.014,
        g3=1.1666 + 0.00314 * (a3 - 0.1184) / 0.0007 - 0.00046 * (mt - 173.34),
        yt=0.93690 + 0.00556 * (mt - 173.34) - 0.00042 * (a3 - 0.1184) / 0.0007,
        lam=0.12604 + 0.00206 * (mh - 125.15) - 0.00004 * (mt - 173.34),
    )


def beta_sm(y, loops=2):
    gY, g2, g3, yt, lam, yb, ytau = y
    a, b, c, t, l = gY ** 2, g2 ** 2, g3 ** 2, yt ** 2, lam
    B, T = yb ** 2, ytau ** 2
    d = [0.0] * 7
    d[0] = K * gY ** 3 * 41 / 6
    d[1] = K * g2 ** 3 * (-19 / 6)
    d[2] = K * g3 ** 3 * (-7)
    d[3] = K * yt * (9 / 2 * t + 3 / 2 * B + T - 17 / 12 * a - 9 / 4 * b - 8 * c)
    d[4] = K * (24 * l ** 2 + l * (12 * t + 12 * B + 4 * T - 9 * b - 3 * a) - 6 * t ** 2 - 6 * B ** 2 - 2 * T ** 2 + 9 / 8 * b ** 2 + 3 / 4 * a * b + 3 / 8 * a ** 2)
    d[5] = K * yb * (9 / 2 * B + 3 / 2 * t + T - 5 / 12 * a - 9 / 4 * b - 8 * c)
    d[6] = K * ytau * (5 / 2 * T + 3 * t + 3 * B - 15 / 4 * a - 9 / 4 * b)
    if loops >= 2:
        K2 = K ** 2
        d[0] += K2 * gY ** 3 * (199 / 18 * a + 9 / 2 * b + 44 / 3 * c - 17 / 6 * t)
        d[1] += K2 * g2 ** 3 * (3 / 2 * a + 35 / 6 * b + 12 * c - 3 / 2 * t)
        d[2] += K2 * g3 ** 3 * (11 / 6 * a + 9 / 2 * b - 26 * c - 2 * t)
        d[3] += K2 * yt * (-12 * t ** 2 + t * (131 / 16 * a + 225 / 16 * b + 36 * c) - 12 * l * t + 6 * l ** 2
                           + 1187 / 216 * a ** 2 - 3 / 4 * a * b + 19 / 9 * a * c - 23 / 4 * b ** 2 + 9 * b * c - 108 * c ** 2)
        d[4] += K2 * (-312 * l ** 3 - 144 * l ** 2 * t - 3 * l * t ** 2 + 30 * t ** 3 - 32 * t ** 2 * c - 8 / 3 * t ** 2 * a - 9 / 4 * t * b ** 2 + 21 / 2 * t * a * b - 19 / 4 * t * a ** 2
                      + l * t * (80 * c + 45 / 2 * b + 85 / 6 * a) + 108 * l ** 2 * b + 36 * l ** 2 * a - 73 / 8 * l * b ** 2 + 39 / 4 * l * a * b + 629 / 24 * l * a ** 2
                      + 305 / 16 * b ** 3 - 289 / 48 * b ** 2 * a - 559 / 48 * b * a ** 2 - 379 / 48 * a ** 3)
    return d


def run(y0, mu0, mu1, loops=2):
    s = solve_ivp(lambda t_, y: beta_sm(y, loops), (math.log(mu0), math.log(mu1)), y0, rtol=1e-10, atol=1e-13, method="DOP853")
    assert s.success
    return list(s.y[:, -1])


def start(mt=172.57, mh=125.20, a3=0.1180, mw=80.369, yb=0.0155, ytau=0.0100):
    m = matching(mt, mh, a3, mw)
    return [m["gY"], m["g2"], m["g3"], m["yt"], m["lam"], yb, ytau]


if __name__ == "__main__":
    ref = run(start(173.34, 125.15, 0.1184, 80.384), 173.34, MPL_BUTTAZZO)
    pub = dict(g1=0.6154, g2=0.5055, g3=0.4873, yt=0.3825, lam=-0.0143)
    got = dict(g1=ref[0] * math.sqrt(5 / 3), g2=ref[1], g3=ref[2], yt=ref[3], lam=ref[4])
    print({k: (round(got[k], 4), pub[k]) for k in pub})
    # the published slopes as a second control
    d_mt = run(start(174.34, 125.15, 0.1184, 80.384), 174.34, MPL_BUTTAZZO)[4] - ref[4]
    d_mh = run(start(173.34, 126.15, 0.1184, 80.384), 173.34, MPL_BUTTAZZO)[4] - ref[4]
    print("dlam/dMt", round(d_mt, 4), "pub -0.0066; dlam/dMh", round(d_mh, 4), "pub 0.0029")
    json.dump(dict(got=got, published=pub, dlam_dmt=d_mt, dlam_dmh=d_mh), open("sm_rge_control.json", "w"), indent=1)
