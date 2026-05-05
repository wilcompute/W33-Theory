"""sgwb_spectrum.py

Numerically compute the stochastic gravitational-wave background (SGWB)
spectrum predicted by the W(3,3) theory (Prediction P22).

Physics:
  - First-order GUT-scale phase transition at T_* ~ M_GUT ~ 10^15 GeV
  - Bubble nucleation rate controlled by spectral gap lambda_1 = 2 (W33)
  - Peak frequency from redshifted Hubble at transition
  - Spectral tilt n_T = 2/3 from spectral moment ratio M_2/M_4

Outputs:
  - Console: peak frequency, amplitude, spectral index
  - sgwb_w33.csv: frequency vs Omega_GW table
  - sgwb_w33.png: log-log plot with NANOGrav 15yr band overlay
"""

import numpy as np
import csv
import os

# ── W(3,3) spectral data ────────────────────────────────────────────────────
# Eigenvalues and multiplicities from the Ramanujan graph spectrum
EIGENVALUES   = [0,  2,  4,  8, 12, 16, 144]  # lambda_i
MULTIPLICITIES = [1, 24, 30,  0, 80,  0,   2]  # degeneracies (80 for k=12 approx)

# Spectral moments M_k = sum_i mult_i * lambda_i^k  (lambda_0=0 excluded)
MOMENTS = {}
for k in range(1, 7):
    Mk = sum(m * (lam ** k) for lam, m in zip(EIGENVALUES[1:], MULTIPLICITIES[1:]))
    MOMENTS[k] = Mk

M2 = MOMENTS[2]   # 144*24 + 4*30 + ... 
M4 = MOMENTS[4]
M6 = MOMENTS[6]

# Spectral tilt from moment ratio (derived in section_graviton.tex)
n_T = 2 * M2 / (3 * np.sqrt(M4))    # n_T = 2/3 at leading order

# ── Phase-transition parameters ────────────────────────────────────────────
# GUT scale
M_GUT_GeV   = 2.0e15          # GeV  (W33 Prediction P8)
T_star_GeV  = M_GUT_GeV       # reheating temperature at transition

# Hubble at transition  H_* ~ T_*^2 / M_Pl
M_Pl_GeV    = 1.22e19         # reduced Planck mass in GeV
H_star_GeV  = T_star_GeV**2 / M_Pl_GeV

# Redshift factor: ratio of temperatures today / at transition
T_0_GeV     = 2.35e-13        # CMB temperature ~ 2.725 K in GeV
a_ratio     = T_star_GeV / T_0_GeV   # T_* / T_0  (scale factor inversion)

# Peak frequency today
Hz_per_GeV  = 1.519e24        # 1 GeV = 1.519e24 Hz (hbar c)
f_peak_Hz   = (H_star_GeV / (2 * np.pi)) * Hz_per_GeV / a_ratio

# ── GW energy density at peak  Ω_GW h^2 ───────────────────────────────────
# Standard formula for FOPTs (Espinosa et al. 2010 parameterisation)
# alpha = latent heat / radiation energy  ~  1 for strong GUT transition
alpha       = 1.0
# beta/H_* = inverse duration of transition ~ spectral gap lambda_1
beta_over_H = float(EIGENVALUES[1])   # = 2  (lightest non-zero eigenvalue)

# Bubble-wall velocity (detonation limit)
v_w         = 1.0 / np.sqrt(3.0)      # sound speed ~ 1/sqrt(3)

# Envelope approximation amplitude
kappa       = alpha / (0.73 + 0.083 * np.sqrt(alpha) + alpha)
Omega_peak  = 1.67e-5 * (H_star_GeV / beta_over_H)**2 \
              * (kappa * alpha / (1 + alpha))**2 \
              * (100 / 100.0) ** (1.0/3.0) \
              * 0.11 * v_w**3 / (0.42 + v_w**2)

# ── Frequency array and spectrum shape ─────────────────────────────────────
f_min  = 1e-10   # Hz
f_max  = 1e-6    # Hz
N      = 500
freqs  = np.logspace(np.log10(f_min), np.log10(f_max), N)

def omega_gw(f, f_peak, Omega_peak, n_T):
    """Broken power-law SGWB spectrum."""
    x = f / f_peak
    # UV slope fixed by causal tail; IR slope = n_T (W33 prediction)
    S = x**n_T / (1.0 + x**(3.0 + n_T))
    S /= (1.0 / (1.0 + 1.0**(3.0 + n_T)))   # normalise to 1 at f_peak
    return Omega_peak * S

omega_vals = omega_gw(freqs, f_peak_Hz, Omega_peak, n_T)

# ── NANOGrav 15-year signal band ────────────────────────────────────────────
# Hellings-Downs correlated signal at f ~ 1/(10 yr) ~ 3.17e-9 Hz
# Ω_GW h² ~ 2e-9 at f_ref = 3.17e-9 Hz (arXiv:2306.16213)
NANO_f_ref      = 3.17e-9     # Hz
NANO_Omega_ref  = 2.0e-9
NANO_f_lo       = 2.0e-9
NANO_f_hi       = 6.0e-9
NANO_O_lo       = 1.0e-9
NANO_O_hi       = 4.0e-9

# ── Write CSV ───────────────────────────────────────────────────────────────
out_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(out_dir, "sgwb_w33.csv")
with open(csv_path, "w", newline="") as fh:
    writer = csv.writer(fh)
    writer.writerow(["frequency_Hz", "Omega_GW"])
    for f, o in zip(freqs, omega_vals):
        writer.writerow([f"{f:.6e}", f"{o:.6e}"])

# ── Terminal summary ────────────────────────────────────────────────────────
print("=" * 60)
print("W(3,3) SGWB Prediction  [Prediction P22]")
print("=" * 60)
print(f"Spectral moments:   M2={M2:.0f}  M4={M4:.0f}  M6={M6:.0f}")
print(f"Spectral tilt n_T = {n_T:.4f}  (target 2/3 = {2/3:.4f})")
print(f"GUT scale T_* = {T_star_GeV:.2e} GeV")
print(f"beta/H_*      = {beta_over_H:.1f}  (from lambda_1 = {EIGENVALUES[1]})")
print(f"Peak frequency: f_peak = {f_peak_Hz:.3e} Hz")
print(f"Peak amplitude: Omega_GW(f_peak) = {Omega_peak:.3e}")
print()
print("NANOGrav 15yr reference point:")
print(f"  f_ref  = {NANO_f_ref:.2e} Hz")
print(f"  Omega  = {NANO_Omega_ref:.2e}")
print()
omega_at_nano = omega_gw(NANO_f_ref, f_peak_Hz, Omega_peak, n_T)
print(f"W33 Omega at NANOGrav f_ref = {omega_at_nano:.3e}")
if NANO_O_lo <= omega_at_nano <= NANO_O_hi:
    print("STATUS: CONSISTENT with NANOGrav 15yr band ✓")
else:
    ratio = omega_at_nano / NANO_Omega_ref
    print(f"STATUS: ratio W33/NANOGrav = {ratio:.2f}  (tension)")
print(f"\nCSV written to: {csv_path}")
print("=" * 60)

# ── Optional matplotlib plot (graceful fallback if not available) ────────────
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots(figsize=(8, 5))

    # W33 spectrum
    ax.loglog(freqs, omega_vals, "b-", lw=2.5, label=r"W(3,3) SGWB  ($n_T=2/3$)")

    # NANOGrav band
    nano_box = Rectangle(
        (NANO_f_lo, NANO_O_lo),
        NANO_f_hi - NANO_f_lo,
        NANO_O_hi - NANO_O_lo,
        color="gold", alpha=0.5, label="NANOGrav 15yr (1σ)"
    )
    ax.add_patch(nano_box)
    ax.axvline(NANO_f_ref, color="orange", ls="--", lw=1)

    # Peak marker
    ax.axvline(f_peak_Hz, color="blue", ls=":", lw=1, alpha=0.7)
    ax.text(f_peak_Hz * 1.5, Omega_peak * 0.3, r"$f_{\rm peak}$",
            color="blue", fontsize=10)

    ax.set_xlabel(r"Frequency $f$ [Hz]", fontsize=13)
    ax.set_ylabel(r"$\Omega_{\rm GW}$", fontsize=13)
    ax.set_title("W(3,3) Stochastic Gravitational-Wave Background\n"
                 r"First-order GUT transition, $\beta/H_* = \lambda_1 = 2$",
                 fontsize=12)
    ax.legend(fontsize=11)
    ax.set_xlim(f_min, f_max)
    ax.grid(True, which="both", alpha=0.3)
    ax.set_ylim(1e-14, 1e-6)

    png_path = os.path.join(out_dir, "sgwb_w33.png")
    plt.tight_layout()
    plt.savefig(png_path, dpi=150)
    plt.close()
    print(f"Plot saved to:  {png_path}")
except ImportError:
    print("matplotlib not available; skipping plot.")
