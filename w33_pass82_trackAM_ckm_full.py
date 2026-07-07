#!/usr/bin/env python3
"""
PASS 82 - TRACK AM: FULL 3x3 CKM MATRIX FROM W33
==================================================

SOURCE: w33_paper.tex, Section 13 (CKM Matrix)

From paper Theorem (CKM Elements):
  |V_us| = (lambda+Phi6)/v = (2+7)/40 = 9/40 = 0.225
  |V_cb| = mu/Theta^2 = 4/100 = 1/25 = 0.04
  |V_ub| = lambda/(v*Phi3) = 2/(40*13) = 2/520 = 1/260

Wolfenstein parameterisation from paper:
  A = mu/(q+lambda) = 4/(3+2) = 4/5 = 0.8
  lambda_W = |V_us| = 9/40 = 0.225
  rho-ieta from V_ub: |V_ub| = A*lambda_W^3 * sqrt(rho^2+eta^2)

CP violation from paper:
  sin(delta_CP) = (mu^2-1)/(mu^2+1) = 15/17
  J_CKM = |V_us|*|V_cb|*|V_ub|*sin(delta_CP)
         = (9/40)*(1/25)*(1/260)*(15/17) = 27/884000 ~ 3.054e-5

Full 3x3 CKM via Wolfenstein expansion (to O(lambda^4)).
"""

import numpy as np
import json
from fractions import Fraction

# W33 parameters
q       = 3
v       = 40
k       = 12
lambda_ = 2
mu      = 4
Theta   = 10
Phi3    = 13
Phi6    = 7

# PDG CKM values
PDG = {
    "Vud": (0.97373, 0.00031),
    "Vus": (0.22500, 0.00068),
    "Vub": (0.003690, 0.000110),
    "Vcd": (0.22486, 0.00068),
    "Vcs": (0.97349, 0.00016),
    "Vcb": (0.04053, 0.00150),
    "Vtd": (0.008693, 0.000290),
    "Vts": (0.03978, 0.00150),
    "Vtb": (0.999118, 0.000032),
    "J":   (3.08e-5, 0.13e-5),
}


def w33_wolfenstein():
    """
    W33 Wolfenstein parameters from w33_paper.tex Section 13.
    lambda_W = |V_us| = (lambda+Phi6)/v = 9/40
    A = mu/(q+lambda) = 4/5
    sin(delta_CP) = (mu^2-1)/(mu^2+1) = 15/17
    """
    lam_W = Fraction(lambda_ + Phi6, v)          # 9/40
    A_W   = Fraction(mu, q + lambda_)            # 4/5
    Vus   = Fraction(lambda_ + Phi6, v)          # 9/40
    Vcb   = Fraction(mu, Theta**2)               # 4/100 = 1/25
    Vub   = Fraction(lambda_, v * Phi3)          # 2/520 = 1/260
    sin_delta = Fraction(mu**2 - 1, mu**2 + 1)  # 15/17

    # Rho and eta from Vub = A * lam_W^3 * sqrt(rho^2+eta^2)
    # |Vub| = (1/260), A*lam_W^3 = (4/5)*(9/40)^3
    A_lam3 = A_W * lam_W**3
    rho_eta_mag = float(Vub) / float(A_lam3)  # magnitude of (rho-bar+i*eta-bar)

    # Use sin_delta to fix ratio rho/eta
    # sin(delta) = eta/sqrt(rho^2+eta^2) => eta = rho_eta_mag * sin(delta)
    sin_d = float(sin_delta)  # 15/17
    cos_d = np.sqrt(1 - sin_d**2)
    rho_bar = rho_eta_mag * cos_d
    eta_bar = rho_eta_mag * sin_d

    return {
        "lambda_W": float(lam_W),
        "lambda_W_exact": str(lam_W),
        "A": float(A_W),
        "A_exact": str(A_W),
        "Vus": float(Vus),
        "Vus_exact": str(Vus),
        "Vcb": float(Vcb),
        "Vcb_exact": str(Vcb),
        "Vub": float(Vub),
        "Vub_exact": str(Vub),
        "sin_delta_CP": float(sin_delta),
        "sin_delta_exact": str(sin_delta),
        "rho_bar": round(rho_bar, 4),
        "eta_bar": round(eta_bar, 4),
    }


def w33_ckm_matrix(wolf):
    """
    Full 3x3 CKM matrix from Wolfenstein parameters (O(lambda^4)).
    """
    lam = wolf["lambda_W"]
    A   = wolf["A"]
    rho = wolf["rho_bar"]
    eta = wolf["eta_bar"]

    # Standard Wolfenstein parameterisation to O(lambda^4)
    Vud = 1 - lam**2/2 - lam**4/8
    Vus = lam
    Vub = A * lam**3 * (rho - 1j*eta)

    Vcd = -lam + A**2*lam**5*(1 - 2*rho)/2
    Vcs = 1 - lam**2/2 - A**2*lam**4/2
    Vcb = A * lam**2

    Vtd = A * lam**3 * (1 - rho + 1j*eta)
    Vts = -A * lam**2 + A*lam**4*(1 - 2*rho)/2
    Vtb = 1 - A**2*lam**4/2

    CKM = np.array([
        [Vud, Vus, Vub],
        [Vcd, Vcs, Vcb],
        [Vtd, Vts, Vtb]
    ], dtype=complex)

    return CKM


def ckm_jacobian(CKM):
    """Compute Jarlskog invariant."""
    # J = Im(V11*V22*V12*.V21*)
    J = np.imag(
        CKM[0,0]*CKM[1,1]*np.conj(CKM[0,1])*np.conj(CKM[1,0])
    )
    return J


def ckm_paper_jacobian():
    """J_CKM from paper formula: (9/40)*(1/25)*(1/260)*(15/17)"""
    Vus = Fraction(9, 40)
    Vcb = Fraction(1, 25)
    Vub = Fraction(1, 260)
    sin_delta = Fraction(15, 17)
    J = Vus * Vcb * Vub * sin_delta
    return J, float(J)


def compare_ckm(CKM, wolf):
    """Compare CKM elements to PDG."""
    names = [["Vud","Vus","Vub"],["Vcd","Vcs","Vcb"],["Vtd","Vts","Vtb"]]
    rows = []
    for i in range(3):
        for j in range(3):
            name = names[i][j]
            pred = abs(CKM[i,j])
            if name in PDG:
                obs, sig = PDG[name]
                pull = (pred - obs) / sig
                verdict = "EXACT" if abs(pull) <= 1.0 else "NEAR-MISS" if abs(pull) <= 3.0 else "QUALITATIVE"
            else:
                obs, sig, pull, verdict = None, None, None, "N/A"
            rows.append({
                "name": name,
                "prediction": round(pred, 6),
                "observed": obs,
                "sigma": sig,
                "pull": round(pull, 3) if pull is not None else None,
                "verdict": verdict,
            })
    return rows


def main():
    print("=" * 72)
    print(" PASS 82 - TRACK AM: FULL 3x3 CKM MATRIX")
    print(" Source: w33_paper.tex Section 13")
    print("=" * 72)

    wolf = w33_wolfenstein()
    print(f"\n  Wolfenstein parameters (from paper):")
    print(f"    lambda_W = {wolf['lambda_W_exact']} = {wolf['lambda_W']:.5f}  (PDG: 0.22500)")
    print(f"    A        = {wolf['A_exact']} = {wolf['A']:.4f}  (PDG: 0.8244)")
    print(f"    Vub      = {wolf['Vub_exact']} = {wolf['Vub']:.6f}  (PDG: 0.003690)")
    print(f"    sin(delta) = {wolf['sin_delta_exact']} = {wolf['sin_delta_CP']:.5f}")
    print(f"    rho_bar  = {wolf['rho_bar']:.4f}")
    print(f"    eta_bar  = {wolf['eta_bar']:.4f}")

    CKM = w33_ckm_matrix(wolf)
    print(f"\n  Full 3x3 |CKM| matrix:")
    labels = ["u","c","t"]
    qlabels = ["d","s","b"]
    print(f"         d         s         b")
    for i,l in enumerate(labels):
        row = "  " + l + "  "
        for j in range(3):
            row += f"  {abs(CKM[i,j]):.6f}"
        print(row)

    comp = compare_ckm(CKM, wolf)
    print(f"\n  CKM comparison with PDG:")
    print(f"  {'Name':>6} {'Pred':>10} {'Obs':>10} {'Pull':>8}  Verdict")
    for c in comp:
        if c['observed'] is not None:
            pull_str = f"{c['pull']:+.3f}" if c['pull'] is not None else "N/A"
            print(f"  {c['name']:>6} {c['prediction']:>10.6f} {c['observed']:>10.6f} {pull_str:>8}  {c['verdict']}")

    J_frac, J_float = ckm_paper_jacobian()
    J_matrix = ckm_jacobian(CKM)
    J_pdg, J_sig = PDG["J"]
    pull_J = (J_float - J_pdg) / J_sig
    print(f"\n  Jarlskog invariant:")
    print(f"    Paper formula: J = {J_frac} = {J_float:.4e}")
    print(f"    Matrix computation: J = {J_matrix:.4e}")
    print(f"    PDG: {J_pdg:.3e} +/- {J_sig:.2e}")
    print(f"    Pull: {pull_J:+.3f} sigma")
    verdict_J = "EXACT" if abs(pull_J) <= 1.0 else "NEAR-MISS" if abs(pull_J) <= 3.0 else "QUALITATIVE"
    print(f"    Verdict: {verdict_J}")

    # Unitarity check
    unit = np.abs(CKM @ CKM.conj().T - np.eye(3)).max()
    print(f"\n  CKM unitarity violation: max|V V^dag - I| = {unit:.2e}")

    exact_count = sum(1 for c in comp if c.get('verdict') == 'EXACT')
    result = {
        "pass": 82,
        "track": "AM",
        "title": "Full 3x3 CKM Matrix from W33",
        "source": "w33_paper.tex Section 13",
        "wolfenstein": wolf,
        "ckm_comparison": comp,
        "J_paper_formula": str(J_frac),
        "J_paper_float": J_float,
        "J_matrix": J_matrix,
        "J_PDG": J_pdg,
        "J_pull": round(pull_J, 3),
        "J_verdict": verdict_J,
        "unitarity_violation": unit,
        "exact_count": exact_count,
        "total_elements": len([c for c in comp if c['observed'] is not None]),
        "key_theorem": (
            f"W33 CKM: |Vus|=9/40, |Vcb|=1/25, |Vub|=1/260, "
            f"J=27/884000={J_float:.3e} (PDG: {J_pdg:.3e}, pull {pull_J:+.3f}sigma). "
            f"Verdict: {verdict_J}. {exact_count}/9 elements exact match."
        ),
        "status": "COMPLETE",
    }
    with open("w33_pass82_trackAM_ckm_full.json", "w") as fout:
        json.dump(result, fout, indent=2)
    print("\n  Witness JSON -> w33_pass82_trackAM_ckm_full.json")
    return result


if __name__ == "__main__":
    main()
