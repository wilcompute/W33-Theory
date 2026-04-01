"""
SOLVE_HIGGS_RG_RUNNING.py
==========================
Run lambda_H from Lambda_GUT = Phi4^k = 10^12 GeV down to M_Z
using SM 2-loop RGEs with W(3,3) boundary conditions:
  lambda_H(Lambda_GUT) = 2*f2/f4 = 0.15909...
  y_top(Lambda_GUT)    = 1 - 1/k^2 = 143/144
  g_3(Lambda_GUT)      = sqrt(4*pi*alpha_s_GUT) ~ 0.6
  g_2(Lambda_GUT)      = sqrt(4*pi*alpha_GUT)   ~ 0.63
  g_1(Lambda_GUT)      = g_2 (GUT unification)

Target: lambda_H(M_Z) = 0.1299 (PDG) => m_H = 125.25 GeV.
"""

import numpy as np
from math import pi, sqrt, log, log10
import json

q, k, g_sp, f_sp, v_graph = 3, 12, 15, 24, 40
Phi3, Phi4, Phi6, mu, two_k1, km1 = 13, 10, 7, 4, 23, 11
ev_r, ev_s = 2, -4

# Physical
M_Z    = 91.1876   # GeV
M_TOP  = 172.69    # GeV
M_H    = 125.25    # GeV
V_EW   = 246.22    # GeV
LAMBDA_H_PDG = M_H**2 / (2*V_EW**2)
ALPHA_S_MZ   = 0.1179
ALPHA_EM_MZ  = 1/127.9
SIN2_TW_MZ   = 0.23122

# W(3,3) boundary conditions at GUT scale
f2 = f_sp*ev_r**2 + g_sp*ev_s**2  # = 336
f4 = f_sp*ev_r**4 + g_sp*ev_s**4  # = 4224
lambda_H_GUT = 2*f2/f4              # = 0.15909
y_top_GUT    = 1 - 1/k**2           # = 143/144 = 0.99306
Lambda_GUT   = Phi4**k              # = 10^12 GeV (W(3,3) GUT scale)

print("=" * 70)
print("W(3,3) HIGGS RG RUNNING")
print("=" * 70)
print(f"  Lambda_GUT = Phi4^k = {Phi4}^{k} = {Lambda_GUT:.3e} GeV")
print(f"  lambda_H(GUT) = 2*f2/f4 = 2*{f2}/{f4} = {lambda_H_GUT:.8f}")
print(f"  y_top(GUT)   = 1 - 1/k^2 = {y_top_GUT:.8f}")
print(f"  Target lambda_H(M_Z) = {LAMBDA_H_PDG:.8f}")
print()

# GUT gauge couplings: assume partial unification at W(3,3) GUT scale
# alpha_GUT ~ 1/CS_level = 1/137 at GUT (tree level)
alpha_GUT = 1/(k**2 - Phi6)  # = 1/137
g2_GUT = sqrt(4*pi*alpha_GUT)
g1_GUT = g2_GUT  # GUT unification
g3_GUT = g2_GUT  # strong = EW at GUT

print(f"  g2_GUT = sqrt(4*pi/137) = {g2_GUT:.6f}")
print(f"  g3_GUT = g2_GUT = {g3_GUT:.6f}  (GUT unification)")
print()

# ======================================================
# 1-loop SM RGEs (in units where t = log(mu/mu_0))
# d/dt lambda = (1/16pi^2) * beta_lambda
# beta_lambda = 24*lambda^2 + 12*lambda*y_t^2 - 6*y_t^4
#              - 3*lambda*(3*g2^2 + g1^2) + (9/8)*g2^4 + ...
# d/dt y_t = (1/16pi^2) * y_t * (9/2*y_t^2 - 8*g3^2 - 9/4*g2^2 - 17/12*g1^2)
# d/dt g3 = (1/16pi^2) * (-7*g3^3)   [1-loop, 6 flavours]
# d/dt g2 = (1/16pi^2) * (-19/6*g2^3) [1-loop SM]
# d/dt g1 = (1/16pi^2) * (+41/10*g1^3) [U(1)_Y, GUT normalised]
# ======================================================

def beta_lambda(lam, yt, g1, g2, g3):
    return (24*lam**2 + 12*lam*yt**2 - 6*yt**4
            - 3*lam*(3*g2**2 + g1**2)
            + (9/8)*(3*g2**4 + 2*g2**2*g1**2 + g1**4) )

def beta_yt(lam, yt, g1, g2, g3):
    return yt * (9/2*yt**2 - 8*g3**2 - 9/4*g2**2 - 17/12*g1**2)

def beta_g3(g3):
    return -7*g3**3

def beta_g2(g2):
    return -(19/6)*g2**3

def beta_g1(g1):
    return (41/10)*g1**3

# RK4 integration from t=log(Lambda_GUT/M_Z) down to t=0
t_start = log(Lambda_GUT/M_Z)   # ~ 23.8
t_end   = 0.0
N_steps = 100000
dt      = (t_end - t_start) / N_steps  # negative (running down)
loop_factor = 1/(16*pi**2)

lam = lambda_H_GUT
yt  = y_top_GUT
g1  = g1_GUT
g2  = g2_GUT
g3  = g3_GUT

print(f"Running from t = log({Lambda_GUT:.1e}/{M_Z}) = {t_start:.4f} to t=0")
print(f"N_steps = {N_steps}, dt = {dt:.6f}")
print()

# Milestones
milestones = {log(M_TOP/M_Z): "M_top", log(1e6/M_Z): "10^6",
              log(1e9/M_Z): "10^9", log(1e12/M_Z): "10^12=GUT"}
log_print = {round(v,2): k_m for k_m, v in milestones.items()}

def rk4_step(lam, yt, g1, g2, g3, dt):
    def derivs(l,y,g1v,g2v,g3v):
        f = loop_factor
        return (f*beta_lambda(l,y,g1v,g2v,g3v),
                f*beta_yt(l,y,g1v,g2v,g3v),
                f*beta_g1(g1v),
                f*beta_g2(g2v),
                f*beta_g3(g3v))
    k1 = derivs(lam,yt,g1,g2,g3)
    k2 = derivs(lam+dt*k1[0]/2, yt+dt*k1[1]/2, g1+dt*k1[2]/2,
                g2+dt*k1[3]/2, g3+dt*k1[4]/2)
    k3 = derivs(lam+dt*k2[0]/2, yt+dt*k2[1]/2, g1+dt*k2[2]/2,
                g2+dt*k2[3]/2, g3+dt*k2[4]/2)
    k4 = derivs(lam+dt*k3[0], yt+dt*k3[1], g1+dt*k3[2],
                g2+dt*k3[3], g3+dt*k3[4])
    return (lam + dt*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6,
            yt  + dt*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6,
            g1  + dt*(k1[2]+2*k2[2]+2*k3[2]+k4[2])/6,
            g2  + dt*(k1[3]+2*k2[3]+2*k3[3]+k4[3])/6,
            g3  + dt*(k1[4]+2*k2[4]+2*k3[4]+k4[4])/6)

print_every = N_steps // 8
t = t_start
print(f"{'t':8s}  {'mu(GeV)':12s}  {'lambda_H':10s}  {'y_top':8s}  {'g3':8s}  {'g2':8s}  {'g1':8s}")
print(f"{t:8.4f}  {M_Z*np.exp(t):12.3e}  {lam:10.6f}  {yt:8.6f}  {g3:8.6f}  {g2:8.6f}  {g1:8.6f}")
for step in range(N_steps):
    lam, yt, g1, g2, g3 = rk4_step(lam, yt, g1, g2, g3, dt)
    t += dt
    if step % print_every == 0 or abs(t) < abs(dt)*2:
        print(f"{t:8.4f}  {M_Z*np.exp(t):12.3e}  {lam:10.6f}  {yt:8.6f}  {g3:8.6f}  {g2:8.6f}  {g1:8.6f}")

lambda_MZ = lam
y_top_MZ = yt
g3_MZ = g3; g2_MZ = g2; g1_MZ = g1

print()
print(f"=" * 70)
print(f"FINAL VALUES AT M_Z:")
print(f"  lambda_H(M_Z) = {lambda_MZ:.8f}  (PDG {LAMBDA_H_PDG:.8f})")
print(f"  error = {(lambda_MZ - LAMBDA_H_PDG)/LAMBDA_H_PDG * 100:+.3f}%")
mH_pred = V_EW * sqrt(2*lambda_MZ) * sqrt(2)  # m_H = v*sqrt(2*lambda)*sqrt(2)? 
# Correct: m_H^2 = 2*lambda_H*v^2 (tree) so m_H = v*sqrt(2*lambda_H)
mH_pred_v2 = V_EW * sqrt(2*lambda_MZ)
print(f"  m_H = v*sqrt(2*lambda_H) = {mH_pred_v2:.3f} GeV  (PDG {M_H:.2f} GeV)")
print(f"  m_H error = {(mH_pred_v2-M_H)/M_H*100:+.3f}%")
print(f"  y_top(M_Z) = {y_top_MZ:.6f}  (PDG input: {M_TOP*sqrt(2)/V_EW:.6f})")
print(f"  alpha_s(M_Z) = g3^2/(4pi) = {g3_MZ**2/(4*pi):.6f}  (PDG {ALPHA_S_MZ:.6f})")
# sin^2 theta_W at M_Z:
sin2_MZ = g1_MZ**2/(g1_MZ**2+g2_MZ**2) / (3/5)  # GUT normalised g1
print(f"  g2(M_Z)={g2_MZ:.4f}, g1(M_Z)={g1_MZ:.4f}")

results = {
    "lambda_H_GUT": lambda_H_GUT, "lambda_H_MZ": lambda_MZ,
    "lambda_H_PDG": LAMBDA_H_PDG,
    "lambda_H_error_pct": (lambda_MZ-LAMBDA_H_PDG)/LAMBDA_H_PDG*100,
    "mH_predicted": mH_pred_v2, "mH_PDG": M_H,
    "mH_error_pct": (mH_pred_v2-M_H)/M_H*100,
    "y_top_GUT": y_top_GUT, "y_top_MZ": y_top_MZ,
    "g3_MZ": g3_MZ, "g2_MZ": g2_MZ, "g1_MZ": g1_MZ,
    "alpha_s_MZ_pred": g3_MZ**2/(4*pi), "alpha_s_MZ_PDG": ALPHA_S_MZ,
    "Lambda_GUT": Lambda_GUT,
    "conjecture": "lambda_H(GUT)=2f2/f4 with y_top=1-1/k^2 RG flows to m_H~125 GeV"
}
with open("higgs_rg_results.json","w") as fh: json.dump(results,fh,indent=2)
print("\nDone. Results in higgs_rg_results.json")
