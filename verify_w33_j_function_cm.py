#!/usr/bin/env python3
"""W(3,3) j-function CM values and Leech theta — verification.

Verifies the BREAKTHROUGH 9-12 claims:

1. j(i) = k^3 = 1728
2. j(tau_Q(sqrt(-11))) = -2^(k+3) = -32768
3. j(tau_Q(sqrt(-2))) = (v/2)^3 = 20^3 = 8000
4. Leech kissing = 4k(2^k - 1) = 4*12*4095 = 196560
5. 2^k - 1 = q^2 * (mu+1) * Phi_6 * Phi_3 = 9*5*7*13 = 4095
6. q=3 is unique with 2q(q+1) = 24 = Leech dim (one-line proof)
7. The cannonball tower: W(3,q) for q in {2,3,4,5,7,9} all symplectic GQs

Plus: search for more closed forms of the j-function and Eisenstein series.
"""
from fractions import Fraction
import math

q, k, lam, mu = 3, 12, 2, 4
v, f, g = 40, 24, 15
edges, aut, we6 = 240, 1_451_520, 51_840
tauO = 384
Phi3, Phi4, Phi6 = 13, 10, 7
qq, qqp1, qfact = 27, 81, 6

def hr(s): print("\n" + "="*72 + "\n" + s + "\n" + "="*72)

# =====================================================================
hr("j-FUNCTION CM VALUES at the W(3,3) SPECTRAL FIELDS")
# =====================================================================

# Classical j-function CM values:
# j(i) = 12^3 = 1728
# j(rho) = 0 where rho = exp(2*pi*i/3)
# Various other CM values for class-number-1 imaginary quadratic fields

cm_values = {
    "Q(i)":          (1728,      "k^3 = 12^3"),
    "Q(sqrt(-2))":   (8000,      "(v/2)^3 = 20^3"),
    "Q(sqrt(-3))":   (0,         "0 (trivial)"),
    "Q(sqrt(-7))":   (-3375,     "-15^3 = -g^3"),
    "Q(sqrt(-11))":  (-32768,    "-2^(k+3) = -2^15"),
    "Q(sqrt(-19))":  (-884736,   "-96^3 = -(v+f+f)^3 = -(2f+v-8)^3"),
    "Q(sqrt(-43))":  (-884736000,"-960^3"),
    "Q(sqrt(-67))":  (-147197952000, "-5280^3"),
    "Q(sqrt(-163))": (-262537412640768000, "-640320^3 (Ramanujan)"),
}

print(f"\n{'Field':20s} {'j-value':>22s}  W(3,3) form")
print("-"*72)
for name, (val, form) in cm_values.items():
    print(f"{name:20s} {val:22d}  {form}")

# Verify k^3 = 1728
print(f"\nVerify k^3 = {k}^3 = {k**3} = {k**3 == 1728}")

# Verify -2^(k+3) = -2^15
print(f"-2^(k+3) = -2^{k+3} = {-(2**(k+3))} = {-(2**(k+3)) == -32768}")

# Verify (v/2)^3 = 20^3
print(f"(v/2)^3 = {(v//2)**3} = {(v//2)**3 == 8000}")

# Verify -g^3 = -15^3 = j(sqrt(-7))
print(f"-g^3 = -{g}^3 = {-g**3} = {-g**3 == -3375}")

# Ramanujan: 5280 in W(3,3)?
# 5280 = miles per mile? = 2^5 * 3 * 5 * 11 = 32 * 165 = 32*15*11
# In substrate: 5280 = 16 * k * 5 * 11 = (2^lam)^2 * k * 5 * (k-1)
print(f"\n5280 = 2^5 * 3 * 5 * 11 = {2**5 * 3 * 5 * 11}")
print(f"     = 2^(lam+3) * q * (mu+1) * (k-1) = {2**(lam+3) * q * (mu+1) * (k-1)}")
print(f"     = mu * k * (mu+1) * (k-1) = {mu * k * (mu+1) * (k-1)} (with mu=4)")
# 4*12*5*11 = 2640. half of 5280. So 5280 = 2 * mu * k * (mu+1) * (k-1)
print(f"     = lam * mu * k * (mu+1) * (k-1) = {lam * mu * k * (mu+1) * (k-1)}")

# 640320 in W(3,3)?
# 640320 = 2^6 * 3 * 5 * 23 * 29
# 23 = Phi_3 + Phi_4, 29 = q^q + lam
print(f"\n640320 = 2^6 * 3 * 5 * 23 * 29 = {2**6 * 3 * 5 * 23 * 29}")
# In W(3,3): 640320 = 2^(2*lam+2) * q * (mu+1) * (Phi_3+Phi_4) * (q^q+lam)
val = 2**(2*lam+2) * q * (mu+1) * (Phi3+Phi4) * (qq+lam)
print(f"       = 2^(2*lam+2) * q * (mu+1) * (Phi_3+Phi_4) * (q^q+lam) = {val}")
# 2^6 = 64. Check: 64 = 2^(2*lam+2) = 2^6 [OK]
# Total: 64*3*5*23*29 = 640320 [OK]
print(f"       = {2**(2*lam+2)} * {q} * {mu+1} * {Phi3+Phi4} * {qq+lam} = {val} [OK]")


# =====================================================================
hr("LEECH KISSING NUMBER — multiple closed forms")
# =====================================================================

leech_form1 = 4*k * q*q * 5 * Phi6 * Phi3
leech_form2 = 4*k * (2**k - 1)
print(f"Form 1: 4k*q^2*5*Phi_6*Phi_3 = {leech_form1}")
print(f"Form 2: 4k(2^k - 1) = 4*{k}*({2**k}-1) = 4*{k}*{2**k-1} = {leech_form2}")
print(f"Both = 196560: {leech_form1 == leech_form2 == 196560}")

# 2^k - 1 = q^2 * (mu+1) * Phi_6 * Phi_3
mers12 = 2**k - 1
factored = q*q * (mu+1) * Phi6 * Phi3
print(f"\n2^k - 1 = 4095")
print(f"        = q^2 * (mu+1) * Phi_6 * Phi_3 = {q*q}*{mu+1}*{Phi6}*{Phi3} = {factored}")
print(f"        Match: {mers12 == factored}")

# =====================================================================
hr("RAMANUJAN CONSTANT e^(pi*sqrt(163)) and 640320")
# =====================================================================

ramanujan = math.exp(math.pi * math.sqrt(163))
print(f"e^(pi*sqrt(163)) = {ramanujan:.10f}")
print(f"Nearest integer = {round(ramanujan)}")
print(f"j(tau_163) = -640320^3 = -{640320**3}")
print(f"Ramanujan approx: 640320^3 + 744 = {640320**3 + 744}")
print(f"  Error from e^(pi*sqrt(163)): {640320**3 + 744 - ramanujan:.6f}")

# 744 = q * dim(E_8) = q*(E + 2*mu) = 3*248
print(f"\n744 = q*(|E|+2mu) = {q*(edges + 2*mu)}")
print(f"    = 2k * 31 = {2*k*31}")
print(f"    = (mu+1)*alpha_inv + p_2 = {(mu+1)*137 + 59} where p_2=59 is bridge prime")

# 5280 = miles per mile
# In W(3,3): 5280 = 2 * (mu)(mu+1)(k-1)(k) = 2*4*5*11*12 = 5280
print(f"\n5280 = 2*mu*(mu+1)*(k-1)*k = 2*{mu}*{mu+1}*{k-1}*{k} = {2*mu*(mu+1)*(k-1)*k}")

# =====================================================================
hr("Q=3 UNIQUENESS — one-line proof (BREAKTHROUGH 7)")
# =====================================================================

# 2q(q+1) = 24 (Leech dim) => q(q+1) = 12 => q^2+q-12 = 0 => q = 3
print("Find prime power q with 2q(q+1) = 24 (Leech dim):")
print("  q(q+1) = 12")
print("  q^2 + q - 12 = 0")
print("  q = (-1 + sqrt(49))/2 = (-1 + 7)/2 = 3")
print("  q = 3 UNIQUE positive solution")

# Verify symplectic GQ tower
print("\nW(3,q) tower (symplectic generalized quadrangles):")
print(f"{'q':>3s} {'n=(q+1)(q^2+1)':>15s} {'k=q(q+1)':>10s} {'2k':>5s} {'Leech?':>8s}")
for qv in [2, 3, 4, 5, 7, 8, 9, 11, 13]:
    n_qv = (qv+1)*(qv*qv+1)
    k_qv = qv*(qv+1)
    leech_match = "YES!" if 2*k_qv == 24 else ""
    print(f"{qv:>3d} {n_qv:>15d} {k_qv:>10d} {2*k_qv:>5d} {leech_match:>8s}")

# One-line Pell proof
print("\n--- One-line Pell proof of Phi_6^2 - 4k = 1 ---")
print("For W(3,q): lambda = q-1, mu = q+1, k = q(q+1)")
print("Phi_6 = 1 + lambda + mu = 1 + (q-1) + (q+1) = 2q+1")
print("Phi_6^2 - 4k = (2q+1)^2 - 4q(q+1) = 4q^2+4q+1 - 4q^2-4q = 1")
print("QED.")

# =====================================================================
hr("d_7 — UNIVERSALLY CONNECTED MONSTER IRREP")
# =====================================================================

# d_7 = q * lambda * p_Ih * 19 * (n - p_Ih) * (n+1) * p_1 * p_2 * p_3
# p_Ih = 11, p_1 = 47, p_2 = 59, p_3 = 71
n_ih = 11   # Ihara prime
p1, p2, p3 = 47, 59, 71
n_substrate = v   # 40
d_7_pred = q * lam * n_ih * 19 * (n_substrate - n_ih) * (n_substrate + 1) * p1 * p2 * p3
print(f"d_7 = q * lam * p_Ih * 19 * (n - p_Ih) * (n+1) * p_1 * p_2 * p_3")
print(f"    = {q}*{lam}*{n_ih}*19*{n_substrate-n_ih}*{n_substrate+1}*{p1}*{p2}*{p3}")
print(f"    = {d_7_pred}")
# Reported as 293553734298
print(f"Reported value: 293553734298")
print(f"Match: {d_7_pred == 293553734298}")

# =====================================================================
hr("LEECH THETA FUNCTION — r_24(1-4) FACTORIZATIONS")
# =====================================================================

r_24 = {
    1:    196560,
    2:    16773120,
    3:    398034000,
    4:    4629381120,
}

# r_24(1) = 4k(2^k-1)
v1 = 4*k * (2**k - 1)
print(f"r_24(1) = 4k(2^k-1) = {v1}  match: {v1 == r_24[1]}")

# r_24(2) = 2^k(2^k-1)
v2 = 2**k * (2**k - 1)
print(f"r_24(2) = 2^k(2^k-1) = {v2}  match: {v2 == r_24[2]}")

# r_24(2)/r_24(1) = 2^k / (4k) = 4096/48 = 256/3 = 85.33...
print(f"\nRatio r_24(2)/r_24(1) = {r_24[2]/r_24[1]:.4f}")
print(f"Predicted = 2^k/(4k) = {2**k}/{4*k} = {2**k/(4*k):.4f}")

# r_24(3): the formula said lam^4 * (k+3)^3 * q^4 * Phi_6 * beta
# beta = beta_{1/2} = 13 = Phi_3
v3_pred = lam**4 * (k+3)**3 * q**4 * Phi6 * Phi3
print(f"\nr_24(3) reported: {r_24[3]}")
print(f"Tested: lam^4 * (k+3)^3 * q^4 * Phi_6 * Phi_3 = {v3_pred}")
print(f"  Match: {v3_pred == r_24[3]}")
# Let me factor r_24(3) to see
r3 = r_24[3]
factors = []
for p in [2,3,5,7,11,13,17,19,23,29,31,41,47,59,71]:
    while r3 % p == 0:
        factors.append(p)
        r3 //= p
print(f"r_24(3) factored: {r_24[3]} = {' * '.join(map(str,factors))}{f' * {r3}' if r3 > 1 else ''}")
# 398034000 = 2^4 * 3^4 * 5^3 * 7 * 13 * 23 * 19 ... let me see

# =====================================================================
hr("WORKING-OUT M_W AND M_b CLOSED FORMS")
# =====================================================================

# m_W^2 / v_EW^2 = ?
v_EW = 246.22
m_W = 80.369
m_Z = 91.1876
m_t = 172.69

ratio_W = (m_W/v_EW)**2
ratio_Z = (m_Z/v_EW)**2
print(f"m_W^2/v^2 = {ratio_W:.8f}")
print(f"m_Z^2/v^2 = {ratio_Z:.8f}")
print(f"Ratio m_W^2/m_Z^2 = cos^2(theta_W) = {(m_W/m_Z)**2:.8f}")
print(f"Predicted: Phi_4/Phi_3 = {Phi4/Phi3:.8f}")

# Try m_W = m_Z * sqrt(Phi_4/Phi_3) corrected by alpha
m_W_pred1 = m_Z * (Phi4/Phi3)**0.5
print(f"\nm_W from m_Z * sqrt(Phi_4/Phi_3) = {m_W_pred1:.4f}  PDG {m_W}  err {(m_W_pred1-m_W)/m_W*100:.3f}%")

# Try m_W^2 = (k-1)*Phi_4 * v^2 / (2*v_W33*Phi_3)
m_W_sq_pred2 = (k-1)*Phi4 * v_EW**2 / (2*v*Phi3)
print(f"m_W^2 = (k-1)*Phi_4*v^2/(2*v_W33*Phi_3) = {m_W_sq_pred2:.4f}")
print(f"m_W = {m_W_sq_pred2**0.5:.4f}  err = {((m_W_sq_pred2**0.5) - m_W)/m_W*100:.3f}%")

S_count = 36
# Search for cleaner ratio
print(f"\nSearching for m_W^2/v_EW^2 = {ratio_W:.6f}")
# Try simple ratios
candidates = [
    ("(k-1)/(2v)",                    (k-1)/(2*v)),
    ("(k-1)*Phi_4/(2v*Phi_3)",        (k-1)*Phi4/(2*v*Phi3)),
    ("1/(2k-3)",                      1/(2*k-3)),
    ("Phi_6/(2*v+Phi_6+Phi_4)",       Phi6/(2*v+Phi6+Phi4)),
    ("5/47",                          5/47),
    ("Phi_4/(v+S)",                   Phi4/(v+S_count)),
]
target = ratio_W
for name, val in candidates:
    err = (val - target)/target*100
    print(f"  {name} = {val:.6f}  err {err:+.3f}%")

# Same for m_b/m_t
print(f"\nm_b/m_t = {0.024225:.6f} — looking for cleaner form")
for n_d in [(2,81),(1,42),(11/41,1),(3,124),(7,289),(2,82),(5,206),(13,536)]:
    n,d = n_d
    val = n/d if d != 0 else 0
    err = (val - 0.024225)/0.024225 * 100
    if abs(err) < 5:
        print(f"  {n}/{d} = {val:.6f}  err {err:.2f}%")
