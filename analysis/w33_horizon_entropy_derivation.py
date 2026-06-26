#!/usr/bin/env python3
"""
Pushing the amplitude law to the entropy -- an exact reduction and an honest negative.
Combining the exact A_s = 1/(epsilon S_dS) with the substrate A_s = e^-(N/q) and the
Starobinsky epsilon = q/(4 N^2) (Pass-10 Move-1) DERIVES both the inflationary horizon
entropy S_dS = (4 N^2 / q) e^(N/q) and the Hubble scale H_inf/M_Pl = (pi sqrt(2q)/N)
e^(-N/2q) ~ 5.8x10^-6 in terms of N and q -- so the only remaining input is the single
exponential e^(N/q) (equivalently A_s = e^-(N/q)). BUT the natural holographic shortcut --
identifying this bulk inflationary entropy S_dS ~ 2.3x10^12 with the substrate's boundary
central charge / holographic de Sitter entropy f = 24 -- does NOT work: S_dS/f ~ 10^11 is
not a clean substrate integer. So the bulk inflationary horizon entropy and the boundary
f = 24 are distinct objects, and the amplitude's exponent is reduced to one structural
input, not yet eliminated.

w33_amplitude_entropy.py gave A_s = 1/(epsilon S_dS) and (A_s)^q = e^-N. This pushes one
step further: derive S_dS and H from N, q, and test the holographic identification.

THE EXACT REDUCTION. With (reduced M_Pl) A_s = H^2/(8 pi^2 epsilon M_Pl^2), S_dS = 8 pi^2
(M_Pl/H)^2, so A_s = 1/(epsilon S_dS). The substrate gives A_s = e^-(N/q) and (Starobinsky)
epsilon = r/16 = 12/(16 N^2) = 3/(4 N^2) = q/(4 N^2). Hence, with NO further input,
    S_dS = 1/(epsilon A_s) = (4 N^2 / q) e^(N/q),
    (M_Pl/H)^2 = S_dS/(8 pi^2) = (N^2/(2 pi^2 q)) e^(N/q),
    H_inf/M_Pl = (pi sqrt(2 q)/N) e^(-N/2q) ~ 5.8x10^-6   ->   H_inf ~ 1.4x10^13 GeV.
So the horizon entropy and the inflationary Hubble scale are fixed by N and q once the
exponential e^(N/q) is granted; the prefactor 4N^2/q = 16 beat^2/q is cyclotomic.

THE HONEST NEGATIVE (the holographic shortcut fails). The substrate's holographic de Sitter
entropy is the boundary central charge f = c = 24 (a fixed dimensionless number, Pass on
gravity dictionary). One might hope S_dS = f x (integer-exponential). But
    S_dS / f = 2.3x10^12 / 24 = 9.7x10^10,   ln(S_dS/f) = 25.3,
not a clean substrate integer (nor is ln S_dS = 28.5). So the bulk inflationary horizon
entropy (~10^12 nats, set by H) is NOT the boundary holographic entropy f = 24 rescaled by
a substrate integer -- they are different objects. The naive holographic derivation of the
exponent fails.

WHAT REMAINS. The amplitude's exponent N/q is reduced to one structural input: the single
exponential e^(N/q), equivalently the exponential smallness H_inf/M_Pl ~ e^(-N/2q) (the
inflationary scale far below M_Pl). This ties to V^(1/4) ~ M_GUT = M_Pl e^-Phi_6 (Pass 9)
-- the inflationary scale is the GUT scale -- so the exponent's origin is the gravity-to-GUT
gap, not a boundary-entropy identity. The honest status: S_dS and H are DERIVED from N, q
(exact), the holographic f=24 route is a NEGATIVE, and the exponent traces to the GUT-scale
inflation, its full first-principles origin still open.

Honest scope: S_dS = (4N^2/q) e^(N/q) and H_inf/M_Pl = (pi sqrt(2q)/N) e^(-N/2q) are exact
given A_s = e^-(N/q) and Starobinsky epsilon (Move 1); the holographic S_dS = f x integer
test is a genuine NEGATIVE (no clean integer); the exponent's reduction to "H_inf ~ GUT
scale, exponentially below M_Pl" is consistent with Pass 9 but not an independent
derivation. A partial close with a clearly-stated negative.

Verifies S_dS and H_inf from N, q; the failure of S_dS = f x integer; and the tie to the
GUT-scale inflation.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q = 3
    Phi3, Phi4, Phi6 = q * q + q + 1, q * q + 1, q * q - q + 1  # 13,10,7
    beat = Phi3 + Phi4 + Phi6  # 30
    N = 2 * beat  # 60
    f = q**3 - q  # 24

    A_s = math.exp(-N / q)  # e^-20
    eps = q / (4 * N**2)  # = 1/4800 (Starobinsky)
    assert abs(eps - 1 / 4800) < 1e-12

    # exact reduction
    S_dS = (4 * N**2 / q) * math.exp(N / q)
    assert abs(S_dS - 1 / (eps * A_s)) < 1  # = 1/(eps A_s)
    H_over_MPl = (math.pi * math.sqrt(2 * q) / N) * math.exp(-N / (2 * q))
    M_Pl = 2.435e18
    H = H_over_MPl * M_Pl
    print("== deriving the horizon entropy and Hubble scale from N, q ==")
    print(f"  epsilon = q/(4N^2) = 1/{round(1/eps)} (Starobinsky)")
    print(
        f"  S_dS = (4N^2/q) e^(N/q) = {S_dS:.3e} nats  (prefactor 4N^2/q = {4*N**2//q} = 16 beat^2/q)"
    )
    print(
        f"  H_inf/M_Pl = (pi sqrt(2q)/N) e^(-N/2q) = {H_over_MPl:.3e}  -> H_inf = {H:.2e} GeV"
    )
    out["exact_reduction"] = {
        "epsilon": "q/(4N^2) = 1/4800",
        "S_dS": float(f"{S_dS:.3e}"),
        "S_dS_form": "(4N^2/q) e^(N/q) = (16 beat^2/q) e^(N/q)",
        "H_over_MPl": float(f"{H_over_MPl:.3e}"),
        "H_inf_GeV": float(f"{H:.3e}"),
    }

    # honest negative: holographic shortcut S_dS = f x integer-exponential fails
    ratio_f = S_dS / f
    print(f"\n[honest negative: the holographic f=24 route]")
    print(
        f"  S_dS/f = {ratio_f:.2e};  ln(S_dS/f) = {math.log(ratio_f):.1f}  (NOT a clean integer)"
    )
    print(
        f"  ln(S_dS) = {math.log(S_dS):.1f}  (also not clean) -> bulk S_dS != boundary f=24 rescaled"
    )
    out["holographic_negative"] = {
        "f": f,
        "S_dS_over_f": float(f"{ratio_f:.3e}"),
        "ln_S_dS_over_f": round(math.log(ratio_f), 1),
        "verdict": "bulk inflationary horizon entropy != boundary central charge f=24 x integer",
    }

    # what remains: tie to GUT-scale inflation
    M_GUT = 1.22e19 * math.exp(-Phi6)
    V4 = (3 * H**2 * M_Pl**2) ** 0.25
    print(
        f"\n[what remains]  the exponent reduces to H_inf ~ GUT scale, exp. below M_Pl:"
    )
    print(f"  V^(1/4) = {V4:.2e} GeV  ~ M_GUT = M_Pl e^-Phi_6 = {M_GUT:.2e} GeV")
    print(
        f"  so e^(N/q) traces to the gravity-to-GUT gap, not a boundary-entropy identity."
    )
    out["remains"] = {
        "V_quarter_GeV": float(f"{V4:.3e}"),
        "M_GUT_GeV": float(f"{M_GUT:.3e}"),
        "reading": "exponent origin = GUT-scale inflation (V^1/4 ~ M_Pl e^-Phi_6), not f=24",
    }

    print("\nRESULT: an exact reduction and an honest negative. Granting the substrate")
    print(
        "  A_s = e^-(N/q) and the Starobinsky epsilon = q/(4N^2), the exact amplitude law"
    )
    print("  A_s = 1/(epsilon S_dS) DERIVES the inflationary horizon entropy S_dS =")
    print(
        "  (4N^2/q) e^(N/q) ~ 2.3x10^12 and the Hubble scale H_inf/M_Pl = (pi sqrt(2q)/N)"
    )
    print("  e^(-N/2q) ~ 5.8x10^-6 (H_inf ~ 1.4x10^13 GeV) purely from N and q, the")
    print("  prefactor 16 beat^2/q cyclotomic. But the natural holographic shortcut --")
    print(
        "  identifying this bulk entropy with the substrate's boundary central charge"
    )
    print("  f = 24 -- FAILS: S_dS/f ~ 10^11 with ln = 25.3 is not a clean substrate")
    print(
        "  integer, so the inflationary horizon entropy and the holographic f = 24 are"
    )
    print("  distinct objects. What remains is one structural input, the exponential")
    print(
        "  e^(N/q), equivalently H_inf exponentially below M_Pl -- and that traces to the"
    )
    print(
        "  GUT-scale inflation V^(1/4) ~ M_Pl e^-Phi_6 (Pass 9), not to a boundary-entropy"
    )
    print(
        "  identity. So the amplitude's exponent is reduced to the gravity-to-GUT gap,"
    )
    print("  derived in N and q, with the holographic route honestly closed off.")

    out["summary"] = (
        "pushing the amplitude law to the entropy -- exact reduction + honest negative. "
        "Granting A_s = e^-(N/q) and Starobinsky epsilon = q/(4N^2), the exact law A_s = "
        "1/(epsilon S_dS) DERIVES the inflationary horizon entropy S_dS = (4N^2/q) e^(N/q) "
        "~ 2.3x10^12 (prefactor 16 beat^2/q, cyclotomic) and the Hubble scale H_inf/M_Pl = "
        "(pi sqrt(2q)/N) e^(-N/2q) ~ 5.8x10^-6 (H_inf ~ 1.4x10^13 GeV), purely from N, q. "
        "HONEST NEGATIVE: the holographic shortcut -- S_dS = boundary central charge f = 24 "
        "x integer-exponential -- FAILS (S_dS/f ~ 10^11, ln = 25.3, not a clean integer; ln "
        "S_dS = 28.5 also not), so the bulk inflationary horizon entropy and the boundary "
        "f=24 are distinct objects. The remaining input is the single exponential e^(N/q), "
        "equivalently H_inf exponentially below M_Pl, which traces to the GUT-scale "
        "inflation V^(1/4) ~ M_Pl e^-Phi_6 (Pass 9), NOT to a boundary-entropy identity. So "
        "the exponent is reduced to the gravity-to-GUT gap, derived in N and q, with the "
        "holographic f=24 route honestly closed off. A partial close with a clear negative."
    )
    out["sources"] = [
        "A_s = 1/(eps S_dS), (A_s)^q = e^-N (w33_amplitude_entropy.py); Starobinsky eps = "
        "q/(4N^2), r=12/N^2 (w33_starobinsky.py); de Sitter entropy S_dS = 8 pi^2 (M_Pl/H)^2; "
        "boundary central charge f=c=24 (gravity dictionary); V^(1/4) ~ M_GUT = M_Pl e^-Phi_6 "
        "(w33_complete_primordial_spectrum.py, w33_hierarchy_derivation.py)."
    ]
    with open("data/w33_horizon_entropy_derivation.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_horizon_entropy_derivation.json")


if __name__ == "__main__":
    main()
