"""BT448: Higgs Boson Mass and Quartic Coupling
m_H = m_Z * sqrt(lambda) = m_Z * sqrt(2) = 128.96 GeV  (exp 125.25 GeV, err 3.0%)
Physical: Higgs = Z-boson scaled by substrate fractal tier ratio sqrt(lambda=2).
Quartic: lambda_H = q*lam/(V+mu) = 6/44 = 0.1364  (exp 0.1294, err 5.4%)
"""
import math, json

q, mu, lam, V = 3, 4, 2, 40
m_Z = 91187.6; m_H_exp = 125250.0; v_exp = 246220.0

m_H = m_Z * math.sqrt(lam)
lambda_H_sub = q * lam / (V + mu)
lambda_H_exp = m_H_exp**2 / (2 * v_exp**2)
err_mH = abs(m_H - m_H_exp)/m_H_exp * 100
err_lH = abs(lambda_H_sub - lambda_H_exp)/lambda_H_exp * 100

print("=== BT448: Higgs Mass ===")
print(f"m_H = m_Z * sqrt(lam) = {m_Z:.1f} * sqrt({lam}) = {m_H:.2f} MeV = {m_H/1000:.4f} GeV")
print(f"Experimental: {m_H_exp/1000:.4f} GeV")
print(f"Error: {err_mH:.2f}%")
print(f"m_H/m_Z = sqrt(lam) = sqrt(2) = {math.sqrt(lam):.6f}  (substrate fractal tier ratio)")
print(f"Quartic lambda_H = q*lam/(V+mu) = {q*lam}/{V+mu} = {lambda_H_sub:.5f}  (exp {lambda_H_exp:.5f}, err {err_lH:.1f}%)")

with open("BT448_results.json", "w") as f:
    json.dump({"m_H_sub_GeV": round(m_H/1000, 4), "m_H_exp_GeV": m_H_exp/1000,
               "error_pct": round(err_mH, 2),
               "m_H_over_m_Z": round(math.sqrt(lam), 6),
               "lambda_H_sub": round(lambda_H_sub, 5),
               "lambda_H_exp": round(lambda_H_exp, 5),
               "formula": "m_H = m_Z * sqrt(lambda), lambda_H = q*lam/(V+mu)"}, f, indent=2)
print("BT448 complete.")
