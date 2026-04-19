"""Jacobi theta functional equation and Poisson summation.

For tau in the upper half plane, set q = exp(i pi tau).  Jacobi's theta_3

    theta_3(tau) = sum_{n = -inf}^{inf}  exp(i pi n^2 tau)
                  = 1 + 2 sum_{n = 1}^{inf}  exp(i pi n^2 tau)

satisfies the two transformation laws that generate the Hecke theta
group Gamma_theta of level 2:

(A)  Periodicity.      theta_3(tau + 2) = theta_3(tau).
(B)  Modular inversion. theta_3(-1/tau) = sqrt(-i tau) theta_3(tau),
     where sqrt is the principal branch with sqrt(-i tau) > 0 on the
     positive imaginary axis.

Law (B) is **the** Jacobi theta identity (Fundamenta Nova, 1829).  Its
proof is one line after Poisson summation,

    sum_{n in Z} f(n) = sum_{k in Z} hat f(k),

applied to the Gaussian f(x) = exp(-pi t x^2) whose Fourier transform is
hat f(k) = (1/sqrt t) exp(-pi k^2 / t).  Evaluating the sum gives

    theta_3(i t) = (1/sqrt t) theta_3(i / t)   for t > 0,

and analytic continuation promotes this to the full (B).

Corollaries pinned here:

1.  Jacobi imaginary transformation on the imaginary axis (the easy,
    fully real case): theta_3(i t) = t^{-1/2} theta_3(i / t) for all
    t > 0, verified at many t.

2.  Full (B) at a handful of off-axis tau, verified numerically.

3.  Period-2 invariance theta_3(tau + 2) = theta_3(tau).

4.  Poisson summation, verified on several Gaussian widths: the two
    sides agree to double precision.

5.  Self-dual point:  theta_3(i) = pi^{1/4} / Gamma(3/4).
    This is classical.  It falls out of (B) with tau = i (fixed point)
    plus the reflection Gamma(3/4) Gamma(1/4) = pi sqrt 2.

6.  Connection to zeta(s): completed zeta
        xi(s) = (1/2) s (s-1) pi^{-s/2} Gamma(s/2) zeta(s)
    admits the Riemann integral formula
        xi(s) = (s (s-1) / 2) * integral_1^inf (t^{s/2 - 1} + t^{(1-s)/2 - 1})
                                   * (theta_3(i t) - 1)/2  dt/ ... ,
    and the functional symmetry xi(s) = xi(1 - s) follows from (B).
    (We just record the identity; the Layer 61 tests already pinned
    the symmetry numerically.)

Layer 64 -- one-line Poisson summation proof of modular inversion;
analytic backbone of Layers 55 / 56 (theta^k squares formulas) and
Layer 61 (Riemann functional equation).
"""

from __future__ import annotations

from typing import Any

import mpmath as mp


# ----------------------------------------------------------------------
# theta_3 on the upper half plane.
# ----------------------------------------------------------------------
def theta3_tau(tau: complex, N: int = 60) -> mp.mpc:
    """theta_3(tau) = 1 + 2 sum_{n=1}^{N} exp(i pi n^2 tau)."""
    tau = mp.mpc(tau)
    total = mp.mpc(1)
    ipi = mp.mpc(0, mp.pi)
    for n in range(1, N + 1):
        total += 2 * mp.exp(ipi * n * n * tau)
    return total


def theta3_imag(t: float, N: int = 60) -> mp.mpf:
    """theta_3(i t) = 1 + 2 sum_{n=1}^{N} exp(-pi n^2 t), t > 0."""
    total = mp.mpf(1)
    for n in range(1, N + 1):
        total += 2 * mp.exp(-mp.pi * n * n * t)
    return total


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_periodicity(dps: int = 50) -> dict[str, Any]:
    """theta_3(tau + 2) = theta_3(tau) at test points."""
    mp.mp.dps = dps
    rows = []
    all_match = True
    for tau in [mp.mpc(0, 1),
                mp.mpc(0.1, 0.5),
                mp.mpc(0.7, 2.0),
                mp.mpc(-0.3, 1.5)]:
        a = theta3_tau(tau, N=80)
        b = theta3_tau(tau + 2, N=80)
        diff = abs(a - b)
        match = diff < mp.mpf("1e-25")
        rows.append({"tau": str(tau), "abs_diff": float(diff),
                     "match": bool(match)})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_imaginary_inversion(dps: int = 50) -> dict[str, Any]:
    """theta_3(i t) = (1/sqrt t) theta_3(i / t) for t > 0."""
    mp.mp.dps = dps
    test_t = [mp.mpf("0.3"), mp.mpf("0.7"), mp.mpf(1),
              mp.mpf("1.5"), mp.mpf(3), mp.mpf(7)]
    rows = []
    all_match = True
    for t in test_t:
        N = 300 if t < 1 else 80  # need more terms for small t (large 1/t)
        lhs = theta3_imag(t, N=N)
        rhs = theta3_imag(1 / t, N=N) / mp.sqrt(t)
        diff = abs(lhs - rhs)
        tol = mp.mpf("1e-15")
        match = diff < tol
        rows.append({"t": float(t), "lhs": float(lhs),
                     "rhs": float(rhs), "abs_diff": float(diff),
                     "match": bool(match)})
        all_match = all_match and bool(match)
    return {"all_match": all_match, "rows": rows}


def verify_general_inversion(dps: int = 50) -> dict[str, Any]:
    """Full Jacobi: theta_3(-1/tau) = sqrt(-i tau) theta_3(tau)."""
    mp.mp.dps = dps
    test_tau = [mp.mpc(0, 1),
                mp.mpc(0, 2),
                mp.mpc("0.1", "1.5"),
                mp.mpc("-0.3", "2.0")]
    rows = []
    all_match = True
    for tau in test_tau:
        # Ensure Im(tau) large enough for fast convergence.
        N = 80 if tau.imag > mp.mpf("0.8") else 300
        lhs = theta3_tau(-1 / tau, N=N)
        rhs = mp.sqrt(mp.mpc(0, -1) * tau) * theta3_tau(tau, N=N)
        diff = abs(lhs - rhs)
        tol = mp.mpf("1e-15")
        match = diff < tol
        rows.append({"tau": str(tau),
                     "abs_diff": float(diff),
                     "match": bool(match)})
        all_match = all_match and bool(match)
    return {"all_match": all_match, "rows": rows}


def verify_theta3_i_equals_closed_form(dps: int = 50) -> dict[str, Any]:
    """theta_3(i) = pi^{1/4} / Gamma(3/4)."""
    mp.mp.dps = dps
    val = theta3_imag(mp.mpf(1), N=80)
    closed = mp.power(mp.pi, mp.mpf("0.25")) / mp.gamma(mp.mpf("0.75"))
    diff = abs(val - closed)
    return {
        "theta3_at_i": str(val),
        "pi_to_1_4_over_Gamma_3_4": str(closed),
        "abs_diff": float(diff),
        "match": bool(diff < mp.mpf("1e-25")),
    }


def poisson_gaussian_lhs(sigma: float, N: int = 80) -> mp.mpf:
    """sum_{n in Z} exp(-sigma n^2)."""
    total = mp.mpf(1)
    for n in range(1, N + 1):
        total += 2 * mp.exp(-mp.mpf(sigma) * n * n)
    return total


def poisson_gaussian_rhs(sigma: float, N: int = 80) -> mp.mpf:
    """Fourier-dual sum: sqrt(pi/sigma) sum_{k in Z} exp(-pi^2 k^2 / sigma)."""
    total = mp.mpf(1)
    for k in range(1, N + 1):
        total += 2 * mp.exp(-mp.pi * mp.pi * k * k / mp.mpf(sigma))
    return mp.sqrt(mp.pi / mp.mpf(sigma)) * total


def verify_poisson_summation(dps: int = 50) -> dict[str, Any]:
    """Gaussian Poisson: sum exp(-sigma n^2) = sqrt(pi/sigma) sum exp(-pi^2 k^2/sigma)."""
    mp.mp.dps = dps
    rows = []
    all_match = True
    for sigma in [0.3, 0.8, 1.0, 2.5, 5.0, 10.0]:
        N = 300 if sigma < 0.5 else 80
        lhs = poisson_gaussian_lhs(sigma, N=N)
        rhs = poisson_gaussian_rhs(sigma, N=N)
        diff = abs(lhs - rhs)
        tol = mp.mpf("1e-15")
        match = diff < tol
        rows.append({"sigma": sigma, "lhs": float(lhs), "rhs": float(rhs),
                     "abs_diff": float(diff), "match": bool(match)})
        all_match = all_match and bool(match)
    return {"all_match": all_match, "rows": rows}


def verify_reflection_gamma_identity(dps: int = 50) -> dict[str, Any]:
    """Gamma(3/4) Gamma(1/4) = pi sqrt 2  (Euler reflection at 1/4)."""
    mp.mp.dps = dps
    lhs = mp.gamma(mp.mpf("0.75")) * mp.gamma(mp.mpf("0.25"))
    rhs = mp.pi * mp.sqrt(2)
    diff = abs(lhs - rhs)
    return {
        "gamma_3_4_times_gamma_1_4": str(lhs),
        "pi_sqrt_2": str(rhs),
        "abs_diff": float(diff),
        "match": bool(diff < mp.mpf("1e-25")),
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    per = verify_periodicity(dps=50)
    imag = verify_imaginary_inversion(dps=50)
    gen = verify_general_inversion(dps=50)
    self_dual = verify_theta3_i_equals_closed_form(dps=50)
    poisson = verify_poisson_summation(dps=50)
    refl = verify_reflection_gamma_identity(dps=50)
    chain = {
        "theta3_period_2_invariance":
            per["all_match"],
        "jacobi_imaginary_inversion_theta3_i_t_equals_sqrt_t_inv_theta3_i_over_t":
            imag["all_match"],
        "jacobi_general_inversion_theta3_minus_1_over_tau":
            gen["all_match"],
        "theta3_at_i_equals_pi_quarter_over_gamma_3_4":
            self_dual["match"],
        "poisson_summation_on_gaussians_lhs_equals_rhs":
            poisson["all_match"],
        "euler_reflection_gamma_3_4_times_gamma_1_4_equals_pi_sqrt_2":
            refl["match"],
    }
    return {
        "periodicity": per,
        "imaginary_inversion": imag,
        "general_inversion": gen,
        "self_dual_point": self_dual,
        "poisson": poisson,
        "reflection": refl,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print(f"\ntheta_3(i) = {s['self_dual_point']['theta3_at_i'][:25]}")
    print(f"pi^(1/4)/Gamma(3/4) = {s['self_dual_point']['pi_to_1_4_over_Gamma_3_4'][:25]}")
    print(f"abs_diff = {s['self_dual_point']['abs_diff']:.3e}")
    print("\nImaginary inversion (first 3 t):")
    for row in s["imaginary_inversion"]["rows"][:3]:
        print(f"  t={row['t']:.1f}: lhs={row['lhs']:.6f}, "
              f"rhs={row['rhs']:.6f}, diff={row['abs_diff']:.3e}")
    print("\nPoisson summation (first 3 sigma):")
    for row in s["poisson"]["rows"][:3]:
        print(f"  sigma={row['sigma']}: lhs={row['lhs']:.6f}, "
              f"rhs={row['rhs']:.6f}, diff={row['abs_diff']:.3e}")
