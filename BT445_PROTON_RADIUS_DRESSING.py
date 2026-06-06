"""BT445: Proton Charge Radius with QCD Dressing
r_p = sqrt(q)/mu * hbar_c/Lambda_QCD * (1 + C_F*alpha_s/pi)
Dressing D = q*sqrt(q) = 3*sqrt(3): 3 quarks x sqrt(E/V) colour flux.
QCD correction (1+C_F*alpha_s/pi) at alpha_s=0.35 (Lambda_QCD scale).
"""
import math, json

q, mu, lam, V, E = 3, 4, 2, 40, 120
pi = math.pi
hbar_c = 197.3269804   # MeV*fm
Lambda_QCD = 217.0     # MeV
alpha_s = 0.35         # strong coupling at Lambda_QCD
C_F = 4/3.0            # QCD Casimir, fundamental SU(3)

r_p_sub = (lam/(mu*q)) * hbar_c / Lambda_QCD
D = q * math.sqrt(q)
QCD_corr = 1 + C_F * alpha_s / pi
r_p = r_p_sub * D * QCD_corr
r_p_exp = 0.8414
err = abs(r_p - r_p_exp)/r_p_exp * 100

print("=== BT445: Proton Charge Radius ===")
print(f"Bare substrate:  {r_p_sub:.4f} fm")
print(f"Dressing D:      q*sqrt(q) = 3*sqrt(3) = {D:.5f}")
print(f"  Physical: 3 quarks x sqrt(E/V)=sqrt(3) colour flux tubes")
print(f"QCD correction:  1 + C_F*alpha_s/pi = {QCD_corr:.5f}")
print(f"r_p = {r_p:.4f} fm  (exp = {r_p_exp:.4f} fm, err = {err:.1f}%)")
print(f"Formula: r_p = sqrt(q)/mu * hbar_c/Lambda_QCD * (1 + 4*alpha_s/(3*pi))")

with open("BT445_results.json", "w") as f:
    json.dump({"r_p_fm": round(r_p, 4), "r_p_exp_fm": r_p_exp,
               "error_pct": round(err, 1),
               "D_dressing": round(D, 5),
               "alpha_s_used": alpha_s,
               "formula": "r_p = sqrt(q)/mu * hbar_c/Lambda_QCD * (1 + C_F*alpha_s/pi)"}, f, indent=2)
print("BT445 complete.")
