"""Item 3: S also decays to Higgs pairs through the portal.  Does that change the freeze-in abundance?
Freeze-in from decays of S in equilibrium uses the PARTIAL width Gamma(S -> NN) (inverse decays keep S thermal), so Gamma(S -> hh) changes Y_N only if S drops out of equilibrium and then decays late (a 'superWIMP' piece Y_S,fo * BR(NN)).
Estimates (real singlet, portal (lambda/2) S^2 |H|^2 with <S> = v_S, so a trilinear lambda v_S S |H|^2 gives Gamma(S -> hh + VV) ~ lambda^2 v_S^2 / (8 pi m_S) counting four Goldstone/Higgs states; rough):
  check Gamma_tot >> H(T = m_S) (S decays promptly, stays thermal) and BR(NN) = Gamma_NN / Gamma_tot;
  superWIMP bound: Y_S,fo <= Y_eq(x ~ 20) and Omega_late = Omega(Y_S,fo * BR) versus the freeze-in 0.12.
Corridor points from sterile_lya.json.  usage: py -3 sterile_hh.py"""
import json
import math

MPL, GS = 1.22e19, 106.75
d = json.load(open("sterile_lya.json"))
out = []
for w in d["window"]:
    if not w["open"]:
        continue
    M, mS, vS = w["M_keV"] * 1e-6, w["m_S"], w["v_S"]
    y = math.sqrt(2) * M / vS
    lam = math.sqrt(w["lambda_min"] * w["lambda_max"])
    G_nn = y ** 2 * mS / (16 * math.pi)
    G_hh = lam ** 2 * vS ** 2 / (8 * math.pi * mS)
    H = 1.66 * math.sqrt(GS) * mS ** 2 / MPL
    BR = G_nn / (G_nn + G_hh)
    x = 20.0
    Yeq = 0.145 * (1 / GS) * x ** 1.5 * math.exp(-x)  # g = 1 real scalar, rough
    om_late = 2.744e8 * M * 2 * Yeq * BR
    row = dict(M_keV=w["M_keV"], m_S=mS, lam=lam, Gamma_NN=G_nn, Gamma_hh=G_hh, H_at_mS=H, prompt=G_hh > 1e3 * H, BR_NN=BR, omega_superwimp_upper=om_late)
    out.append(row)
    print("M %d keV m_S %d: Gamma_hh %.1e GeV vs H %.1e (x%.0e), BR(NN) %.1e, late-decay Omega <= %.1e" % (w["M_keV"], mS, G_hh, H, G_hh / H, BR, om_late))
json.dump(out, open("sterile_hh.json", "w"), indent=1)
