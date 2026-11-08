"""How large must a protecting Z_N be for a periodic (axion-type) fading coupling?  Two conditions, plus a geometric one.
(i) Quality: the Z_N-invariant operator c_N Phi^N / M_P^(N-4) with |Phi| = f/sqrt2 and c_N = O(1) must not exceed the dark-energy density:
      N ln(sqrt2 M_P / f) >~ ln(M_P^4 / rho_DE)       (rho_DE = (2.3 meV)^4; O(1) coefficient is a hypothesis about UV effects).
(ii) One-loop partner cancellation (cyclic partners, arXiv:2610.30253): residual ~ eps^N M^4/(16 pi^2) below rho_DE, with eps ~ b f / M_P (Chat's 75f2a7e02 benchmark: eps = 0.053 at f = M_P, b = 0.053), M = 16 keV.
(iii) Monotonic mass history: the fitted field excursion since recombination is Delta phi = 0.26-0.85 M_P (class_fit_*.json); a periodic mass with period 2 pi f stays monotonic over it only if pi f >~ Delta phi, i.e. f >~ 0.08-0.27 M_P.
Reports N_min(i), N_min(ii) versus f and the binding value at the geometric floor.
usage: py -3 quality_N.py"""
import json
import math

MP = 2.435e27  # eV
RHO = (2.3e-3) ** 4
M = 16e3
b = 0.053
L = math.log(MP ** 4 / RHO)
out = dict(lnMP4_over_rho=L, rows=[])
dphi = []
for ds in ("dovekie", "desy5"):
    fdat = json.load(open(f"class_fit_{ds}.json"))
    for m in ("free_neg", "free_pos"):
        i = fdat[m]["info"]
        dphi.append(i["phi0"] - i["phi_rec"])
fmin = [d / math.pi for d in dphi]
out["delta_phi"] = dphi
out["f_min_monotonic"] = fmin
for f_over_mp in (1.0, 0.5, 0.27, 0.1, 0.08, 1e-2, 1e-3, 1e-6):
    f = f_over_mp * MP
    n_q = L / math.log(math.sqrt(2) * MP / f)
    eps = b * f_over_mp
    n_cw = math.log(M ** 4 / (16 * math.pi ** 2 * RHO)) / math.log(1 / eps)
    mono = f_over_mp >= min(fmin)
    out["rows"].append(dict(f_over_MP=f_over_mp, N_quality=n_q, N_loop=n_cw, eps=eps, monotonic_possible=mono))
    print("f = %.0e M_P: N >= %.0f (quality), %.1f (loop); monotonic over fitted excursion: %s" % (f_over_mp, n_q, n_cw, mono))
print("ln(M_P^4/rho_DE) = %.1f; fitted Delta phi = %s M_P -> f >= %s M_P" % (L, [round(d, 2) for d in dphi], [round(x, 2) for x in fmin]))
json.dump(out, open("quality_N.json", "w"), indent=1)
