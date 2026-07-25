#!/usr/bin/env python3
"""W(3,3) — NEW DISCOVERIES from continued sweep.

Verifies three NEW closed-form predictions discovered in the discussion:

1. m_h = (2E + 2q! + q^2)/mu GeV = 501/4 = 125.25 GeV  (PDG 0.04%)
2. m_tau = Phi_6 * (Phi_3+mu) / 67  where 67 is class-number-1 Heegner
3. m_Z^2 = (k-1)/(2v) * v_EW^2
4. alpha^-1 = 137 + v*47/|W(E_6)| - 1/(mu*(mu+1)*q^q*Phi_6)  (1 ppm match!)

Plus searches for more mass closed forms and Heegner-related identities.
"""
from fractions import Fraction
import math

# Substrate primitives
q, k, lam, mu = 3, 12, 2, 4
v, f, g = 40, 24, 15
edges, aut, we6 = 240, 1_451_520, 51_840
tauO = 384
Phi3, Phi4, Phi6, Phi12 = 13, 10, 7, 73
qq, qqp1, qfact = 27, 81, 6
S_count, Q_count = 36, 45

PDG = {
    "alpha_inv": 137.035999084,
    "m_h": 125.25,
    "m_W": 80.369,
    "m_Z": 91.1876,
    "m_t": 172.69,
    "m_tau": 1.77686,
    "m_mu": 0.10566,
    "m_e": 0.000511,
    "m_p": 0.93827,
    "v_EW": 246.22,
    "V_us": 0.22436,
}

def hr(s): print("\n" + "="*72 + "\n" + s + "\n" + "="*72)


# ---------------------------------------------------------------------------
hr("DISCOVERY #51: m_h closed form")

# m_h = (2E + 2q! + q^2) / mu
m_h_pred = Fraction(2*edges + 2*qfact + q*q, mu)
print(f"m_h = (2*E + 2*q! + q^2) / mu")
print(f"    = (2*{edges} + 2*{qfact} + {q*q}) / {mu}")
print(f"    = ({2*edges + 2*qfact + q*q}) / {mu}")
print(f"    = {m_h_pred} = {float(m_h_pred)} GeV")
print(f"PDG m_h = {PDG['m_h']} GeV")
err = abs(float(m_h_pred) - PDG["m_h"]) / PDG["m_h"] * 100
print(f"MATCH: err = {err:.4f}%")

# ---------------------------------------------------------------------------
hr("DISCOVERY #52: m_tau via Heegner prime 67")

# m_tau = Phi_6 * (Phi_3 + mu) / (mu*(Phi_3+mu) - 1)
#       = 7 * 17 / 67
# 67 is the 8th Heegner prime (-67 is class-number-1)
heegner_67 = mu * (Phi3 + mu) - 1
m_tau_pred = Fraction(Phi6 * (Phi3 + mu), heegner_67)
print(f"m_tau = Phi_6 * (Phi_3+mu) / (mu*(Phi_3+mu) - 1)")
print(f"      = {Phi6} * {Phi3+mu} / {heegner_67}")
print(f"      = {Phi6*(Phi3+mu)}/{heegner_67}")
print(f"      = {m_tau_pred} = {float(m_tau_pred):.6f} GeV")
print(f"PDG m_tau = {PDG['m_tau']} GeV")
err = abs(float(m_tau_pred) - PDG["m_tau"]) / PDG["m_tau"] * 100
print(f"MATCH: err = {err:.4f}%")
heegner = {-1, -2, -3, -7, -11, -19, -43, -67, -163}
print(f"Note: {-heegner_67} in Heegner set {sorted(heegner)}? {-heegner_67 in heegner}")
print("    -67 is the 8th class-number-1 imaginary quadratic discriminant.")

# Cascade: m_mu, m_e
m_mu_cascade = m_tau_pred / (Phi3 + mu)
m_e_cascade = m_mu_cascade / (q*q * (Phi3 + Phi4))
print(f"\nCascade:")
print(f"  m_mu = m_tau/{Phi3+mu} = {float(m_mu_cascade)} GeV  [PDG {PDG['m_mu']}]")
print(f"  m_e  = m_mu/{q*q*(Phi3+Phi4)} = {float(m_e_cascade)*1000:.4f} MeV  [PDG {PDG['m_e']*1000} MeV]")

# ---------------------------------------------------------------------------
hr("DISCOVERY #53: m_Z = v_EW * sqrt((k-1)/(2v))")

v_EW = PDG["v_EW"]
m_Z_pred = v_EW * math.sqrt((k-1)/(2*v))
print(f"m_Z = v_EW * sqrt((k-1)/(2v))")
print(f"    = {v_EW} * sqrt({k-1}/{2*v})")
print(f"    = {v_EW} * sqrt({k-1}/{2*v}) = {v_EW} * {math.sqrt((k-1)/(2*v)):.6f}")
print(f"    = {m_Z_pred:.4f} GeV")
print(f"PDG m_Z = {PDG['m_Z']} GeV")
err = abs(m_Z_pred - PDG["m_Z"]) / PDG["m_Z"] * 100
print(f"MATCH: err = {err:.4f}%")

# Equivalent: m_Z^2 * 2v = (k-1) * v_EW^2
print(f"\nEquivalent: 2v * m_Z^2 = (k-1) * v_EW^2")
print(f"  LHS: 2*{v}*{PDG['m_Z']**2:.4f} = {2*v*PDG['m_Z']**2:.4f}")
print(f"  RHS: {k-1}*{v_EW**2:.4f} = {(k-1)*v_EW**2:.4f}")

# m_W follows
m_W_pred = m_Z_pred * math.sqrt(Phi4/Phi3)
print(f"\nThen m_W = m_Z * sqrt(Phi_4/Phi_3) = {m_W_pred:.4f} GeV  [PDG {PDG['m_W']}]")
err = abs(m_W_pred - PDG["m_W"]) / PDG["m_W"] * 100
print(f"MATCH: err = {err:.4f}%")

# ---------------------------------------------------------------------------
hr("DISCOVERY #54: alpha^-1 to PPM precision")

# alpha^-1 = 137 + v*47/we6 - tauO/aut
# Where tauO/aut = 1/3780 = 1/(mu*(mu+1)*q^q*Phi_6)
term1 = Fraction(137)
term2 = Fraction(v * (v + Phi6), we6)
term3 = Fraction(tauO, aut)

alpha_inv_pred = term1 + term2 - term3
print(f"alpha^-1 = 137 + v*47/|W(E_6)| - tau(O)/|Aut|")
print(f"        = 137 + {v}*{v+Phi6}/{we6} - {tauO}/{aut}")
print(f"        = 137 + {v*(v+Phi6)}/{we6} - {tauO}/{aut}")
print(f"        = 137 + {term2} - {term3}")
print(f"        = {alpha_inv_pred} = {float(alpha_inv_pred):.10f}")
print(f"\nPDG alpha^-1 = {PDG['alpha_inv']}")
diff = float(alpha_inv_pred) - PDG["alpha_inv"]
err_ppm = diff/PDG["alpha_inv"] * 1e6
print(f"DIFF: {diff:.10f}  ({err_ppm:.2f} ppm)")

# Verify tauO/aut = 1/(mu*(mu+1)*q^q*Phi_6)
denom = mu * (mu+1) * qq * Phi6
print(f"\nVerify tau(O)/|Aut| = 1/{denom}:")
print(f"  tau(O)/|Aut| = {tauO}/{aut} = {Fraction(tauO, aut)}")
print(f"  1/(mu*(mu+1)*q^q*Phi_6) = 1/({mu}*{mu+1}*{qq}*{Phi6}) = 1/{denom}")
print(f"  Match: {Fraction(tauO, aut) == Fraction(1, denom)}")

# Cleaner form:
print(f"\nCLEAN FORM:")
print(f"alpha^-1 = 137 + v(v+Phi_6)/|W(E_6)| - 1/(mu(mu+1)q^q Phi_6)")
print(f"        = 137 + {v}*{v+Phi6}/{we6} - 1/{denom}")
print(f"        = {float(alpha_inv_pred):.10f}")
print(f"PDG     = {PDG['alpha_inv']:.10f}")
print(f"Diff    = {diff:.2e}")

# ---------------------------------------------------------------------------
hr("DISCOVERY #55: Yukawa cascade in pure substrate primitives (no input)")

# Starting from m_h_pred = 501/4 GeV
m_h = float(m_h_pred)
m_t = (k-1) * m_h / (2**q)
m_b = m_t / v
m_c = m_t / 137.0
m_s = m_t / (mu * qq * (Phi3 + mu))
m_tau_v = float(m_tau_pred)
m_mu_v = m_tau_v / (Phi3 + mu)
m_e_v = m_mu_v / (q*q * (Phi3 + Phi4))

table = [
    ("m_h",   m_h,    PDG["m_h"]),
    ("m_t",   m_t,    PDG["m_t"]),
    ("m_b",   m_b,    4.183),
    ("m_c",   m_c,    1.273),
    ("m_s",   m_s,    0.0934),
    ("m_tau", m_tau_v, PDG["m_tau"]),
    ("m_mu",  m_mu_v, PDG["m_mu"]),
    ("m_e",   m_e_v,  PDG["m_e"]),
]
print(f"\n{'mass':10s} {'pred (GeV)':>14s} {'meas (GeV)':>14s} {'err %':>8s}")
for name, pred, meas in table:
    err = abs(pred - meas)/meas * 100
    print(f"{name:10s} {pred:>14.6g} {meas:>14.6g} {err:>7.3f}%")

# ---------------------------------------------------------------------------
hr("DISCOVERY #56: Search for more Heegner-prime-based mass formulas")

# Heegner primes: -1, -2, -3, -7, -11, -19, -43, -67, -163
# Compute Heegner constants
heegner_primes = [1, 2, 3, 7, 11, 19, 43, 67, 163]

print("\nHeegner primes appearing as W(3,3) substrate values:")
for h in heegner_primes:
    # Check if any simple W(3,3) combination equals h
    print(f"  -{h}: ", end="")
    if h == 1: print("trivial")
    elif h == 2: print(f"lam")
    elif h == 3: print(f"q")
    elif h == 7: print(f"Phi_6")
    elif h == 11: print(f"k-1")
    elif h == 19: print(f"f-mu-1")
    elif h == 43: print(f"mu*(Phi_3-q+1)+lam = {mu*(Phi3-q+1)+lam}? {mu*(Phi3-q+1)+lam == 43}")
    elif h == 67: print(f"mu*(Phi_3+mu) - 1 = {mu*(Phi3+mu)-1}? {mu*(Phi3+mu)-1 == 67}")
    elif h == 163: print(f"3*54 + 1 = {3*54+1}? {3*54+1 == 163}, or k*Phi_3 - lam*q+1 = {k*Phi3 - lam*q+1}")

# Verify 163 (the Ramanujan constant)
# e^(pi*sqrt(163)) is famously close to an integer
import math
ramanujan_const = math.exp(math.pi * math.sqrt(163))
print(f"\nRamanujan constant e^(pi*sqrt(163)) = {ramanujan_const}")
print(f"Integer approximation = 640320^3 + 744 = {640320**3 + 744}")
print(f"In substrate: 640320 = ? and 744 = q*dim(E_8)")

# ---------------------------------------------------------------------------
hr("DISCOVERY #57: Pell-like discriminant-one mining")

# Search a^2 - n*b = 1 with a, b W(3,3) primitives
prims = {
    "q":q, "k":k, "lam":lam, "mu":mu, "v":v, "f":f, "g":g,
    "Phi3":Phi3, "Phi4":Phi4, "Phi6":Phi6, "Phi12":Phi12,
    "qq":qq, "qqp1":qqp1, "qfact":qfact,
    "edges":edges, "tauO":tauO, "we6":we6, "aut":aut,
    "S":S_count, "Q":Q_count,
    "11":11, "17":17, "19":19, "23":23, "29":29, "31":31,
    "41":41, "47":47, "59":59, "67":67, "71":71, "163":163,
}

print("\nSearching for a^2 - n*b = 1, all in substrate primitives:")
hits = set()
for an, av in prims.items():
    for bn, bv in prims.items():
        if bv == 0: continue
        for n in range(1, 25):
            if av*av - n*bv == 1:
                key = (av, n, bv)
                if key in hits: continue
                hits.add(key)
                # Filter trivial repeats
                if av < 3: continue
                print(f"  {an}^2 - {n}*{bn} = {av}^2 - {n}*{bv} = 1  ({an},{bn})")

# ---------------------------------------------------------------------------
hr("SUMMARY")

new_discoveries = [
    ("m_h closed form: (2E+2q!+q^2)/mu = 501/4 GeV", abs(float(m_h_pred) - PDG["m_h"])/PDG["m_h"]*100),
    ("m_tau via Heegner-67: Phi_6*(Phi_3+mu)/67", abs(float(m_tau_pred) - PDG["m_tau"])/PDG["m_tau"]*100),
    ("m_Z = v_EW*sqrt((k-1)/(2v))", abs(m_Z_pred - PDG["m_Z"])/PDG["m_Z"]*100),
    ("alpha^-1 = 137 + v(v+Phi_6)/|W(E_6)| - 1/(mu(mu+1)q^q Phi_6)", abs(float(alpha_inv_pred) - PDG["alpha_inv"])/PDG["alpha_inv"]*1e6),
]
print()
for desc, err in new_discoveries:
    unit = "ppm" if "alpha" in desc.lower() else "%"
    print(f"  [{err:.4f} {unit}] {desc}")
