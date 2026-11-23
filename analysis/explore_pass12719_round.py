"""Pass 12719 (Claude track), items 2-5 (item 1: explore_pass12719_transformer.py).
 (2) A-terms by mediation: X = A^2/M_SS^2.  Gauge mediation: A = 0 at the messenger scale, RG-generated A/M ~ (16/3)(alpha_3/4pi) ln(M_mess/M_SS)
     ~ 0.03 -> X ~ 1e-3; gravity / anomaly mediation: X = O(1).  Hybrid y' (M_SS = 8.45e9, M_VL = 1.74 TeV) for X = 1e-3, 0.5, 1, 3, 6.
 (3) Pseudo-Goldstone quark decays: mixing m_mix = a (a/M_Pl)^(n-3) from the Z10 decay operator of dimension n, theta = m_mix / M_VL;
     Gamma ~ g^2 theta^2 M^3 / (32 pi m_W^2) (W + Z + h, Goldstone limit); c tau vs n; prompt / displaced / R-hadron / BBN regimes.
     The multiplet content (Q + U) equals B''s top-partner content (Q + T): the same 1.74 TeV prompt limit (Pass 12693).
 (4) Doublet-triplet splitting by Dimopoulos-Wilczek: W ⊃ 10_H Sigma 10'_H + M' 10' 10' with Sigma along B-L (vanishes on doublets).
     Z10 search: the 24 assignments of Pass 12718 extended by q10' with 2 q10' = 0, q10 + s + q10' = 0, 2 q10 != 0 (no GUT-scale mu),
     anomaly with the 10'; mu-term from 10 10 (Hbar H)^c / M^(2c-1): smallest allowed c and mu = a^(2c) / M_Pl^(2c-1).
 (5) Qudit error-correction economy: perfect [[5,1,3]]_d codes (exist for all prime d); physical error p_d = p f(d) with f = 1 or f = d-1
     (more excited levels, more decay channels); logical failure ~ P(weight >= 2); information log2 d per block; cost ~ d per system.
usage: py -3 analysis/explore_pass12719_round.py"""
import itertools, json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
K = 1 / (16 * math.pi ** 2)
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3 = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3"))
dl_ = lambda y: (5 / 6) * 3 * K * y[5] ** 4 - 2 * y[4] * 3 * K * y[5] ** 2 / 3


def lam_at(yp, tgt, mvl=1740.0):
    Mt0 = 172.57 - OFF3; kw = dict(rtol=1e-9, atol=1e-12, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(mvl / Mt0)), np.array(initial(172.57, 125.20, 0.1180) + [yp]), **kw).y[:, -1].copy()
    y[4] += dl_(y)
    return solve_ivp(lambda t, y: beta_vl(*y), (math.log(mvl / Mt0), math.log(tgt / Mt0)), y, **kw).y[:, -1]


# ======================================================================= (2)
MSS = 8.45e9
gm = (16 / 3) * (0.03 / (4 * math.pi)) * math.log(10)
med = []
for lab, X in (("gauge mediation (M_mess = 10 M_SS)", gm ** 2), ("gravity/anomaly, X = 0.5", 0.5), ("X = 1", 1.0), ("X = 3", 3.0), ("X = 6 (maximal)", 6.0)):
    yp = brentq(lambda p: lam_at(p, MSS)[4] - 3 * p ** 4 / (8 * math.pi ** 2) * (X - X ** 2 / 12), 0.2, 1.0, xtol=1e-6)
    med.append(dict(case=lab, X=X, y=yp))
    print(f"(2) {lab:36s}: X = {X:.1e} -> hybrid y' = {yp:.4f}")
res["mediation"] = dict(rows=med, gauge_A_over_M=gm,
                        note="gauge mediation keeps the hybrid sharp (y' = 0.472 at M_VL = 1.74 TeV); gravity/anomaly mediation spreads it to 0.435-0.47")

# ======================================================================= (3)
aG, MPl, MVL, g, mW = 4.1e16, 2.435e18, 1740.0, 0.652, 80.37
HBC = 1.97327e-16
dec = []
for nd in range(11, 21):
    mm = aG * (aG / MPl) ** (nd - 3); th = min(mm / MVL, 1.0)
    Gam = g ** 2 * th ** 2 * MVL ** 3 / (32 * math.pi * mW ** 2)
    ctau = HBC / Gam; tau = ctau / 2.998e8
    reg = "prompt" if ctau < 1e-4 else ("displaced" if ctau < 1.0 else ("R-hadron (detector-stable)" if tau < 0.1 else "BBN-excluded"))
    dec.append(dict(n=nd, m_mix=mm, theta=th, ctau_m=ctau, tau_s=tau, regime=reg))
    print(f"(3) decay operator dim {nd}: mixing {mm:.1e} GeV, theta {th:.1e}, c tau = {ctau:.1e} m, tau = {tau:.1e} s -> {reg}")
res["pgb_decay"] = dict(rows=dec, collider="Q + U has the same quantum numbers as B''s Q + T: prompt pair limit 1.74 TeV (3x rate), long-lived R-hadron ~1.9 TeV; "
                                       "HL-LHC to ~2.1 TeV. Collider searches cannot tell hybrid from B'; y' and its M_VL dependence can.")

# ======================================================================= (4) DW doublet-triplet + Z10
N = 10
Tidx = {"16": 2, "10": 1, "45": 8, "54": 12}
dw = []
for q16, s, qh, qhb in itertools.product(range(N), range(N), range(N), range(N)):
    q10 = (-2 * q16) % N; t = 0; y = 0
    if (2 * s) % N or (y + 5 * ((qh + qhb) % N)) % N: continue
    p = (qh + qhb) % N
    if not any((2 * q16 + 2 * qhb + c * p) % N == 0 for c in range(4)): continue
    harm = min([k + j + 2 + 2 * c for k in range(1, 9) for j in range(4) for c in range(5) if (k * s + (1 + c) * p) % N == 0] + [99])
    if harm < 11: continue
    dd = min([3 + k + j + 2 * c for k in range(10) for j in range(4) for c in range(6) if ((k + 1) * s + q16 + qhb + c * p) % N == 0] + [99])
    mm = aG * (aG / MPl) ** (dd - 3) if dd < 99 else 0.0
    if not (1.7e-10 <= mm <= 300): continue
    if (2 * q10) % N == 0: continue                                         # GUT-scale mu forbidden
    for q10p in range(N):
        if (2 * q10p) % N or (q10 + s + q10p) % N: continue
        anom = (3 * q16 * 2 + q10 * 1 + q10p * 1 + s * 8 + t * 12 + qh * 2 + qhb * 2) % 5
        if anom: continue
        cmu = next((c for c in range(1, 8) if (2 * q10 + c * p) % N == 0), None)
        mu = aG ** (2 * cmu) / MPl ** (2 * cmu - 1) if cmu else 0.0
        dw.append(dict(q16=q16, q10=q10, q10p=q10p, s=s, qh=qh, qhb=qhb, harm=harm, decay_dim=dd, mu_c=cmu, mu=mu))
print(f"(4) Z10 assignments with quality, BBN-safe PGB decay, no GUT-scale mu, Dimopoulos-Wilczek 10 Sigma 10' + 10'10' allowed and anomaly-free: {len(dw)}")
for x in dw[:4]:
    print(f"(4)   q16={x['q16']} q10={x['q10']} q10'={x['q10p']} s={x['s']} qH={x['qh']} qHbar={x['qhb']}: mu from 10 10 (Hbar H)^{x['mu_c']} -> mu ~ {x['mu']:.1e} GeV")
res["dw"] = dict(n=len(dw), solutions=dw[:20],
                 note="the B-L VEV of the 45 is exactly the Dimopoulos-Wilczek direction: triplets get mass a, doublets stay light; 10 Sigma 10' "
                      "involves no VEV field, so it does not lift the Goldstones at tree level (SUSY non-renormalisation)")


# ----- (4b) escape: 10' mass from a singlet X (W_X = Z (X^5 - v), Z neutral), 10' X 10' instead of 10'10'
dw2 = []
for q16, s_, qh, qhb in itertools.product(range(N), range(N), range(N), range(N)):
    q10 = (-2 * q16) % N
    if (2 * s_) % N or (5 * ((qh + qhb) % N)) % N or (2 * q10) % N == 0: continue
    p_ = (qh + qhb) % N
    if not any((2 * q16 + 2 * qhb + c * p_) % N == 0 for c in range(4)): continue
    for x in range(0, N, 2):                                                 # 5x = 0 mod 10
        q10p = (-q10 - s_) % N
        if (2 * q10p + x) % N: continue
        harm = min([k + j + 2 + 2 * c + e for k in range(1, 9) for j in range(4) for c in range(5) for e in range(5)
                    if (k * s_ + (1 + c) * p_ + e * x) % N == 0] + [99])
        if harm < 11: continue
        dd = min([3 + k + j + 2 * c + e for k in range(10) for j in range(4) for c in range(6) for e in range(5)
                  if ((k + 1) * s_ + q16 + qhb + c * p_ + e * x) % N == 0] + [99])
        mm = aG * (aG / MPl) ** (dd - 3) if dd < 99 else 0.0
        if not (1.7e-10 <= mm <= 300): continue
        if (3 * q16 * 2 + q10 + q10p + s_ * 8 + qh * 2 + qhb * 2) % 5: continue
        mus = [(e, c, aG ** (e + 2 * c) / MPl ** (e + 2 * c - 1)) for e in range(0, 7) for c in range(0, 5)
               if e + c > 0 and (2 * q10 + e * x + c * p_) % N == 0]
        e_, c_, mu = min(mus, key=lambda t: t[0] + 2 * t[1]) if mus else (None, None, 0.0)
        dw2.append(dict(q16=q16, q10=q10, q10p=q10p, s=s_, qh=qh, qhb=qhb, x=x, harm=harm, decay_dim=dd, mu_ops=(e_, c_), mu=mu))
print(f"(4b) with the 10' mass from a singlet X (10' X 10', W_X = Z (X^5 - v)): {len(dw2)} assignments pass quality, decay, no GUT mu, DW and anomaly")
for x_ in sorted(dw2, key=lambda t: abs(math.log10(t['mu'] / 1e10)) if t['mu'] else 99)[:3]:
    print(f"(4b)   q16={x_['q16']} q10={x_['q10']} q10'={x_['q10p']} s={x_['s']} qH={x_['qh']} qHbar={x_['qhb']} x={x_['x']}: harmful from dim {x_['harm']}, "
          f"decay dim {x_['decay_dim']}, mu from 10 10 X^{x_['mu_ops'][0]} (Hbar H)^{x_['mu_ops'][1]} ~ {x_['mu']:.1e} GeV")
res["dw"]["theorem"] = "Sigma^2, 10'10' and 10 Sigma 10' allowed imply 2 q10 = 0 for every Z_N: 10 10 (a GUT-scale mu) is then allowed"
res["dw"]["with_singlet"] = dict(n=len(dw2), solutions=sorted(dw2, key=lambda t: abs(math.log10(t['mu'] / 1e10)) if t['mu'] else 99)[:20])

# ======================================================================= (5) qudit codes
qd = []
p = 1e-3
for f_name, f in (("f = 1", lambda dd: 1.0), ("f = d - 1", lambda dd: dd - 1.0)):
    for dd in (2, 3, 5, 7):
        pd = p * f(dd)
        pf = 1 - (1 - pd) ** 5 - 5 * pd * (1 - pd) ** 4
        info = math.log2(dd)
        qd.append(dict(model=f_name, d=dd, p_phys=pd, p_fail=pf, info_bits=info, info_per_cost=info / (5 * dd), fail_per_bit=pf / info))
        print(f"(5) [[5,1,3]]_{dd} ({f_name}): p_phys {pd:.1e}, logical failure {pf:.1e}, {info:.2f} bits per block, failure per encoded bit {pf / info:.1e}, "
              f"bits per unit control cost {info / (5 * dd):.3f}")
res["qudit"] = dict(rows=qd, note="with level-independent errors, qutrits win (same failure, 1.58x information; radix economy favours d = 3); if errors grow "
                                  "with excited levels (f = d - 1), the logical failure per encoded bit is 2.5x worse for qutrits; literature: qutrit magic "
                                  "state distillation has higher thresholds (Campbell-Anwar-Browne 2012)")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12719_round.json"), "w", encoding="utf-8"), indent=1, default=str)
print("wrote data/explore_pass12719_round.json")
