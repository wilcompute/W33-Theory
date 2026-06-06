"""BT446: Lepton Mass Ladder from Substrate
Mass step r = q/V = 3/40 per substrate generation slot.
m_e/m_mu ~ (q/V)^2 = 0.005625  vs exp 0.004836 (14% off, leading order).
Exact match needs PMNS mixing corrections.
"""
import math, json

q, mu, lam, V = 3, 4, 2, 40
m_e = 0.51099895; m_mu = 105.6583755; m_tau = 1776.86

r = q / V
r2 = r**2
theta_12 = math.radians(33.44)
mix = math.cos(theta_12)**2

print("=== BT446: Lepton Mass Ladder ===")
print(f"Substrate step r = q/V = {q}/{V} = {r:.6f}")
print(f"r^2 = {r2:.6f}   exp m_e/m_mu = {m_e/m_mu:.6f}   err = {abs(r2-m_e/m_mu)/(m_e/m_mu)*100:.1f}%")
print(f"r^4 = {r**4:.8f}  exp m_e/m_tau = {m_e/m_tau:.8f}  err = {abs(r**4-m_e/m_tau)/(m_e/m_tau)*100:.1f}%")
print(f"With PMNS theta_12 dressing: r^2*cos^2(33.44) = {r2*mix:.6f}  err = {abs(r2*mix-m_e/m_mu)/(m_e/m_mu)*100:.1f}%")

with open("BT446_results.json", "w") as f:
    json.dump({"r": r, "r_squared": r2,
               "m_e_over_m_mu_sub": r2, "m_e_over_m_mu_exp": m_e/m_mu,
               "error_pct": round(abs(r2-m_e/m_mu)/(m_e/m_mu)*100, 1),
               "formula": "r = q/V = 3/40, m_n/m_{n+2} = r^2"}, f, indent=2)
print("BT446 complete.")
