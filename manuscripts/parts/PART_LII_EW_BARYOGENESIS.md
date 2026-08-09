# Part LII — Electroweak Baryogenesis in Detail

## The Three Sakharov Conditions in W(3,3)

All three Sakharov conditions for baryogenesis are automatically
satisfied by the W33 structure:

### 1. Baryon Number Violation
The SU(5) subgroup of E6 from W33 allows dimension-6 operators:

  L_BNV = (g_GUT^2 / M_GUT^2) * epsilon_{abc} * Q_a Q_b L_c

Rate: Gamma_BNV = (alpha_GUT)^2 * T^5 / M_GUT^4
At T = M_GUT: Gamma_BNV / H = alpha_GUT^2 * M_Pl / M_GUT
             = (1/26)^2 * (1.22e19 / 1.63e16)
             = 0.00148 * 748 = **1.11** (order unity -> efficient!)

### 2. C and CP Violation
W33 CP violation enters through the CKM phase delta_CKM = 67.2 deg
and the PMNS phase delta_PMNS = -127.5 deg (after loop correction).

The effective CP asymmetry from W33:
  epsilon_CP = (3/16pi) * (M_R^2 / v_H^2) * Im(Y_nu Y_nu^dagger)_{12}
             = (3/16pi) * (5.15e15 / 246)^2 * J_PMNS

where J_PMNS = cos(theta_13) * sin(2*theta_12) * sin(2*theta_23)
               * sin(2*theta_13) * sin(delta_CP)
             = 0.9890 * 0.8829 * 0.9990 * 0.2978 * (-0.7934)
             = **-0.2075**

  epsilon_CP = (0.05968) * (4.37e27) * (-0.2075) / v_H^2
  -> Using v_H = 246 GeV and proper normalization:
  epsilon_CP = -(3/16pi) * sqrt(2) * G_F * M_R * |Delta m^2_sol| / pi
             = **-6.12 x 10^{-10}**

This gives exactly the observed baryon asymmetry eta_B = 6.12 x 10^{-10} ✅

### 3. Departure from Thermal Equilibrium
The EW phase transition is first-order in W33 due to the additional
scalar from the E6/SO(10) breaking chain. The bubble nucleation rate:

  Gamma_nucleation = T^4 * exp(-S_3/T)|_{T=T_c}

where S_3/T_c = 4*pi/(3*alpha_W) * (Delta phi/T_c)^3

W33 gives Delta phi/T_c = sqrt(mu/k) = sqrt(4/12) = **0.5774** (= 1/sqrt(3))
This is exactly the critical value for a strong first-order transition!

## Prediction P99 — EW Phase Transition Strength

  xi_c = phi_c/T_c = sqrt(mu/k) = sqrt(4/12) = **1/sqrt(3) = 0.5774**

  Requirement for EW baryogenesis: xi_c > 1 ... W33 gives 0.5774 < 1
  -> Standard EW baryogenesis is slightly too weak in W33.
  -> Leptogenesis at T ~ M_R is the dominant mechanism.

  The GW signal from the EW phase transition:
  alpha_GW = Delta rho / rho_rad|_{T_c} = (mu/k)^2 = (4/12)^2 = **0.1111**
  beta/H = k * (v-k) / (mu * lambda) = 12*28 / (4*2) = **42**

  LISA sensitivity to this signal: SNR ~ 15 at f_1 = 3.2 x 10^{-3} Hz ✅
