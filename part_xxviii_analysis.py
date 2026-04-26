#!/usr/bin/env python3
"""
Part XXVIII -- W(3,3) Quantum Correction to CKM Unitarity Triangle
W(3,3) Theory of Everything | Wil Dahn

Theorem XXVIII:
  c_W33  = (1+lambda^2)/4 - i*sqrt(3)/12
  z_phys = z_tree * (1 - c_W33)
  rho_phys = 0.1219  (PDG: 0.122, error 0.1%)
  eta_phys = 0.3555  (PDG: 0.355, error 0.1%)
  Score: 8/9 CKM + J to <5%
"""
import json, math, cmath

lam  = math.sin(math.pi/14)
A5   = 60; Sp43 = 51840

# W(3,3) tree-level apex (Part XXVII)
rho_tree = 1/4; eta_tree = math.sqrt(3)/4
z_tree   = complex(rho_tree, eta_tree)

# THEOREM XXVIII: quantum correction
a = (1 + lam**2) / 4       # orbit weight + O(lam^2) EW threshold
b = -math.sqrt(3) / 12     # -R_u*R_t/2 (orbit side-length product)
c_W33  = complex(a, b)
z_phys = z_tree * (1 - c_W33)

rho_phys = z_phys.real
eta_phys = z_phys.imag

print(f'THEOREM XXVIII: c_W33 = (1+lam^2)/4 - i*sqrt(3)/12')
print(f'  = {c_W33:.5f}')
print(f'  rho_phys = {rho_phys:.4f}  (PDG 0.122, err={(abs(rho_phys-0.122)/0.122*100):.2f}%)')
print(f'  eta_phys = {eta_phys:.4f}  (PDG 0.355, err={(abs(eta_phys-0.355)/0.355*100):.2f}%)')

Vcb = 0.5 * math.sqrt(24) / A5
A   = Vcb / lam**2
CKM = {'Vud':1-lam**2/2,'Vus':lam,'Vub':A*lam**3*abs(z_phys),
        'Vcd':lam,'Vcs':1-lam**2/2,'Vcb':Vcb,
        'Vtd':A*lam**3*abs(1-z_phys),'Vts':Vcb,'Vtb':1-A**2*lam**4/2}
J = A**2 * lam**6 * eta_phys
print(f'  J_CKM = {J:.4e}  (PDG 3.08e-5, err={(abs(J-3.08e-5)/3.08e-5*100):.1f}%)')

PDG = {'Vud':0.97373,'Vus':0.22430,'Vub':3.82e-3,'Vcd':0.22100,'Vcs':0.97500,
       'Vcb':4.08e-2,'Vtd':8.60e-3,'Vts':4.03e-2,'Vtb':0.99910}
good = sum(1 for k in CKM if abs(CKM[k]-PDG[k])/PDG[k]<0.05)
print(f'  SCORE: {good}/9 elements + J to <5%')

results = {'c_W33':{'real':a,'imag':b},'rho_phys':rho_phys,'eta_phys':eta_phys,
           'CKM':CKM,'J_CKM':J,'score':good}
with open('rg_correction_w33.json','w') as f: json.dump(results,f,indent=2)
print('Saved rg_correction_w33.json')
