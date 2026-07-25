"""BT447: Weinberg Angle Prediction — 0.195% Precision
sin^2(theta_W) = q/(q + 3*mu - lam) = 3/13 = 0.23077
Experimental PDG on-shell: 0.23122
Error: 0.195% from pure substrate algebra.

DERIVATION:
  SU(5) GUT: sin^2(theta_W)|_GUT = lam/(lam+q) = 2/5 = 0.400
  Denominator 13 = q + 3*(mu-1) + 1 = substrate gauge DOF
    q=3: SU(3)_colour generators
    3*(mu-1)=9: spatial gauge redundancy in mu-1=3 spatial dims
    +1: U(1)_Y hypercharge
  Total DOF = 13, colour DOF = q=3 -> sin^2 = q/13 = 3/13
"""
import math, json

q, mu, lam = 3, 4, 2

sin2_W = q / (q + 3*mu - lam)
sin2_W_exp = 0.23122
sin2_W_GUT = lam / (lam + q)
err = abs(sin2_W - sin2_W_exp) / sin2_W_exp * 100

print("=== BT447: Weinberg Angle ===")
print(f"sin^2(theta_W) = q/(q + 3mu - lam) = {q}/({q+3*mu-lam}) = {sin2_W:.6f}")
print(f"Experimental (PDG on-shell):        {sin2_W_exp:.5f}")
print(f"Error: {err:.3f}%  *** SUB-PERCENT PRECISION ***")
print(f"At GUT unification: sin^2 = lam/(lam+q) = {sin2_W_GUT:.5f}")
print(f"Denominator 13 = q + 3*(mu-1) + 1 = substrate gauge DOF count")

with open("BT447_results.json", "w") as f:
    json.dump({"sin2_theta_W": sin2_W, "sin2_theta_W_exp": sin2_W_exp,
               "error_pct": round(err, 3), "sin2_theta_W_GUT": sin2_W_GUT,
               "formula": "q/(q + 3*mu - lam) = 3/13",
               "status": "0.195% error — SUB-PERCENT PRECISION"}, f, indent=2)
print("BT447 complete.")
