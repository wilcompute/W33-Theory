#!/usr/bin/env python3
"""Part XXIX: Vub analysis and final CKM closure | W(3,3) TOE | Wil Dahn"""
import json, math, cmath

lam = math.sin(math.pi/14)
A5 = 60
Vcb = 0.5*math.sqrt(24)/A5
A = Vcb/lam**2
z_tree = complex(1/4, math.sqrt(3)/4)
c_W33 = complex((1+lam**2)/4, -math.sqrt(3)/12)
z_phys = z_tree*(1-c_W33)

CKM = {
    "Vud": 1-lam**2/2,
    "Vus": lam,
    "Vub": A*lam**3*abs(z_phys),
    "Vcd": lam,
    "Vcs": 1-lam**2/2,
    "Vcb": Vcb,
    "Vtd": A*lam**3*abs(1-z_phys),
    "Vts": Vcb,
    "Vtb": 1-A**2*lam**4/2
}
J = A**2*lam**6*z_phys.imag

PDG = {
    "Vud": 0.97373, "Vus": 0.22430, "Vub": 3.435e-3,
    "Vcd": 0.22100, "Vcs": 0.97500, "Vcb": 4.08e-2,
    "Vtd": 8.60e-3, "Vts": 4.03e-2, "Vtb": 0.99910
}

n = sum(1 for k in CKM if abs(CKM[k]-PDG[k])/PDG[k] < 0.05)
if abs(J-3.08e-5)/3.08e-5 < 0.05:
    n += 1

print(f"Final score: {n}/10 CKM observables to <5%")
print(f"  rho_bar={z_phys.real:.4f}, eta_bar={z_phys.imag:.4f}")

Vub_gf = 0.811*0.2243**3*math.sqrt(0.122**2+0.355**2)
print(f"  Vub={CKM['Vub']:.4e} (global fit {Vub_gf:.4e}, err={abs(CKM['Vub']-Vub_gf)/Vub_gf*100:.1f}%)")
print(f"  J_CKM={J:.4e} (PDG 3.08e-5, err={abs(J-3.08e-5)/3.08e-5*100:.1f}%)")

print(f"\nFull CKM table vs PDG global fit:")
print(f"{'Element':<6} {'W33':>10} {'PDG fit':>10} {'Error':>8}")
for k, v in CKM.items():
    err = abs(v-PDG[k])/PDG[k]*100
    print(f"{k:<6} {v:>10.6f} {PDG[k]:>10.6f} {err:>7.2f}%")
Jerr = abs(J-3.08e-5)/3.08e-5*100
print(f"{'J_CKM':<6} {J:>10.4e} {3.08e-5:>10.2e} {Jerr:>7.2f}%")

with open("part_xxix_results.json","w") as f:
    json.dump({"CKM": CKM, "J": J, "rho_bar": z_phys.real, "eta_bar": z_phys.imag, "score": n}, f, indent=2)
print("Saved part_xxix_results.json")
