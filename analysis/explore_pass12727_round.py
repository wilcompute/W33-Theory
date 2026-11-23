"""Pass 12727 (Claude track), items 1, 2, 4 (item 3: explore_pass12727_firstlayer.py; item 5: status refresh).
 (1) Isocurvature bound for A's pre-inflation misalignment: P_iso / P_ad = (d ln Omega / d theta)^2 (H_I / 2 pi f_a)^2 / P_ad (axion = all DM),
     with Omega ~ theta^2 F(theta) (anharmonic); Planck: beta_iso < 0.038, P_ad = 2.1e-9 -> H_I,max.  Tensor-to-scalar ratio r at H_I,max.
 (2) Dark-sector fifth force of B''s coupled component: extra attraction 2 beta^2 between coupled particles; a fraction f of the halo is coupled,
     so the coupled component feels a fractional extra force ~2 beta^2 f relative to gravity inside the halo; tidal-stream / dwarf bounds on a
     DM-only fifth force of order 0.1 (Kesden-Kamionkowski-type).
 (4) Radiatively generated brane kinetic terms in the SO(10) orbifold: localised log coefficients (1/2)(b_even - b_odd) at each fixed point
     with the parity-class b's of Pass 12725; delta_i = b_loc,i ln(M_s R) / 2pi; compared with the O(1.2-1.5) tree-level coefficients needed.
usage: py -3 analysis/explore_pass12727_round.py"""
import json, math, os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = {}

# (1)
F = lambda th: math.log(math.e / (1 - (th / math.pi) ** 2)) ** (7 / 6)
lnOm = lambda th: math.log(th ** 2 * F(th))
iso = []
for fa, th in ((2.48e10, 0.99203 * math.pi), (1.7e11, 0.65065 * math.pi)):
    h = 1e-6; dln = (lnOm(th + h) - lnOm(th - h)) / (2 * h)
    Hmax = 2 * math.pi * fa * math.sqrt(0.038 * 2.1e-9) / dln
    r = 2 * Hmax ** 2 / (math.pi ** 2 * 2.1e-9 * (2.435e18) ** 2)
    iso.append(dict(f_a=fa, theta_over_pi=th / math.pi, dlnOmega_dtheta=dln, H_I_max=Hmax, r=r))
    print(f"(1) f_a = {fa:.2e}, theta_i = {th / math.pi:.4f} pi: d ln Omega / d theta = {dln:.1f} -> H_I < {Hmax:.1e} GeV (r < {r:.0e})")
res["isocurvature"] = dict(rows=iso, note="low-scale inflation: H_I <~ 1e5 GeV at the central f_a; r unobservable")

# (2)
fifth = []
for beta, f in ((0.3, 0.2), (0.2, 0.5), (0.1, 1.0)):
    extra = 2 * beta ** 2 * f
    fifth.append(dict(beta=beta, f=f, extra_force=extra, below_0p1=extra < 0.1))
    print(f"(2) beta = {beta}, coupled fraction {f}: extra attraction ~ 2 beta^2 f = {extra:.3f} ({'below' if extra < 0.1 else 'above'} the ~0.1 dark-force bound)")
res["fifth_force"] = fifth

# (4)
b = {"++": np.array([0.0, -4.0, -6.0]), "+-": np.array([-5.603, 0.0, -2.0]), "-+": np.array([-9.992, -6.0, -4.0]), "--": np.array([-0.402, -6.0, -4.0])}
ps_loc = 0.5 * ((b["++"] + b["+-"]) - (b["-+"] + b["--"]))
su5_loc = 0.5 * ((b["++"] + b["-+"]) - (b["+-"] + b["--"]))
rows = []
for MsR in (10, 15):
    d = (ps_loc + su5_loc) * math.log(MsR) / (2 * math.pi)
    D = d[2] - d[0] + 12 / 7 * (d[0] - d[1])
    rows.append(dict(MsR=MsR, delta=d.tolist(), shift=D, magnitude=float(np.abs(d).max())))
    print(f"(4) M_s R = {MsR}: localised log coefficients PS {np.round(ps_loc, 2)}, SU(5)xU(1) {np.round(su5_loc, 2)}; radiative brane shifts "
          f"{np.round(d, 2)} -> alpha_3^-1 shift {D:+.2f} (needed +1.46)")
res["radiative_brane"] = dict(ps_loc=ps_loc.tolist(), su5_loc=su5_loc.tolist(), rows=rows,
                              note="magnitudes O(1), as the tree-level repair needs, but the sign in this crude estimate adds to the deficit: the repair "
                                   "needs a tree-level brane term of opposite sign to the radiative one")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12727_round.json"), "w"), indent=1)
