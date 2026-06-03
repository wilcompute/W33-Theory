"""W(3,3) BREAKTHROUGH 117: SPECTRAL TRACE TOWER EXTENSION + ASYMPTOTICS.

BT116 integrated the remote BT110/111/112 spectral trace tower for k=2..8.
This BT extends the computation to k=9..12 and characterizes the
asymptotic behavior. The tower is fully determined by the V-adjacency
spectrum {12, 2, -4} with multiplicities {1, 24, 15}, so EVERY tr(A^k)
is substrate-determined.

==============================================================
ANALYTIC FORM (closed form for all k)
==============================================================

For the W(3,3) adjacency matrix on V = 40 vertices:

  tr(A^k) = 1 * k^k + f * r^k + g * s^k
          = 12^k + 24 * 2^k + 15 * (-4)^k

The substrate spectrum encodes every spectral moment.

==============================================================
EXTENSION k = 9..12
==============================================================

  tr(A^9)  = 12^9 + 24*2^9 + 15*(-4)^9
           = 5159780352 + 12288 - 3932160
           = 5,155,860,480

  tr(A^10) = 12^10 + 24*2^10 + 15*4^10
           = 61917364224 + 24576 + 15728640
           = 61,933,117,440

  tr(A^11) = 12^11 + 24*2^11 + 15*(-4)^11
           = 743008370688 + 49152 - 62914560
           = 742,945,505,280

  tr(A^12) = 12^12 + 24*2^12 + 15*4^12
           = 8916100448256 + 98304 + 251658240
           = 8,916,352,204,800

==============================================================
ASYMPTOTIC: PERRON DOMINATES
==============================================================

  tr(A^k) -> 12^k as k -> infinity

  tr(A^k) / 12^k -> 1
  (f * 2^k + g * (-4)^k) / 12^k -> 0 (subdominant)

Rate of convergence: max(|r|/k, |s|/k)^k = (4/12)^k = (1/3)^k = q^(-k).

So tr(A^k) ~ 12^k with q-exponential corrections. The CORRECTION RATE
is the substrate's qutrit base.

==============================================================
EVEN-ODD STRUCTURE
==============================================================

EVEN k:   tr(A^k) = 12^k + 24*2^k + 15*4^k  (all positive contributions)
ODD k:    tr(A^k) = 12^k + 24*2^k - 15*4^k  (alternating sign in s^k)

The minus-eigenvalue's CHIRALITY (BT79: Szilassi 42+/0-) propagates
to the trace tower's odd-k terms.

==============================================================
RATIO LADDERS (NEW substrate identities)
==============================================================

ODD-K RATIOS:
  tr(A^3) / tr(A^1) = 960 / 0  (undefined; A has trace 0)
  tr(A^5) / tr(A^3) = 234240 / 960 = 244 ~ q^q + Phi_4 * Heegner_7 = 27+170=197 (no)
  tr(A^7) / tr(A^5) = 35589120 / 234240 = 151.93 (close to alpha^-1 + Phi_4?)
  tr(A^9) / tr(A^7) = 5155860480 / 35589120 = 144.87 (k^2 = 144!)

  Approach k^2 = 144 as k grows.

EVEN-K RATIOS:
  tr(A^4) / tr(A^2) = 24960 / 480 = 52 = mu * Phi_3 = F_4 (!)
  tr(A^6) / tr(A^4) = 3048960 / 24960 = 122.15 (no clean)
  tr(A^8) / tr(A^6) = 430970880 / 3048960 = 141.35
  tr(A^10) / tr(A^8) = 61933117440 / 430970880 = 143.71
  tr(A^12) / tr(A^10) = 8916352204800 / 61933117440 = 143.97

  Approach k^2 = 144 as k grows.

==============================================================
THE RATIO -> k^2 = 144 = lambda^q^q? NO -- direct substrate
==============================================================

  k^2 = 144 = 12^2 = (q*mu)^2 = q^2 * mu^2

The asymptotic even-step trace ratio is the SQUARE OF THE GRAPH DEGREE.

==============================================================
NEW SUBSTRATE IDENTITY: F_4 dimension hit
==============================================================

  tr(A^4) / tr(A^2) = 52 = mu * Phi_3 = dim F_4 (exceptional Lie algebra!)

  The W(3,3) trace ratio at depth 4/2 EQUALS the F_4 dimension.
  Cross-link to BT73 exceptional Lie series.

==============================================================
NEW SUBSTRATE IDENTITIES (BT117)
==============================================================

  tr(A^4) / tr(A^2) = F_4 dim = 52 = mu * Phi_3
  tr(A^k) ~ k^k with subdominant ~ q^-k corrections
  Asymptotic even-ratio = k^2 = 144 = (q*mu)^2
  ODD-k traces inherit chirality from s = -4 eigenvalue
  Higher tr(A^k) for k>=9 substrate-determined via spectrum

==============================================================
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6 = 13, 10, 7
    k_eig = 12  # Perron eigenvalue
    r_eig = 2
    s_eig = -4
    f, g_neg = 24, 15

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 117: SPECTRAL TRACE TOWER EXTENSION")
    print("=" * 78)
    print()

    print("CLOSED FORM:")
    print(f"  tr(A^k) = 1 * 12^k + {f} * 2^k + {g_neg} * (-4)^k")
    print()

    print("EXTENDED COMPUTATIONS (k = 2..12):")
    for kk in range(2, 13):
        tr = 1 * k_eig ** kk + f * r_eig ** kk + g_neg * s_eig ** kk
        print(f"  tr(A^{kk}) = {tr:,}")
    print()

    print("EVEN-K RATIOS (approach k^2 = 144):")
    even_ratios = []
    for kk in (4, 6, 8, 10, 12):
        tr_num = 1 * k_eig ** kk + f * r_eig ** kk + g_neg * s_eig ** kk
        tr_den = 1 * k_eig ** (kk - 2) + f * r_eig ** (kk - 2) + g_neg * s_eig ** (kk - 2)
        ratio = tr_num / tr_den
        even_ratios.append((kk, ratio))
        print(f"  tr(A^{kk})/tr(A^{kk-2}) = {ratio:.4f}")
    print(f"  Limit: k^2 = 144 = (q*mu)^2  *** ASYMPTOTIC SUBSTRATE ***")
    print()

    print("THE F_4 SURPRISE:")
    F4_dim = mu * phi3
    tr2 = 480
    tr4 = 24960
    assert tr4 // tr2 == F4_dim == 52
    print(f"  tr(A^4) / tr(A^2) = 24960/480 = 52 = mu * Phi_3 = dim F_4!")
    print(f"  *** EXCEPTIONAL LIE DIM AT DEPTH 4/2 ***")
    print()

    print("ASYMPTOTIC:")
    print(f"  tr(A^k) / 12^k -> 1 as k -> infinity")
    print(f"  Correction rate: q^-k (substrate qutrit base)")
    print()

    print("EVEN-ODD STRUCTURE:")
    print(f"  Even k: all positive contributions (Perron dominates)")
    print(f"  Odd k: 15*(-4)^k contributes with alternating sign")
    print(f"  Chirality inherited from s = -4 eigenvalue (BT79 Szilassi link)")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 117 SUMMARY")
    print("=" * 78)
    print(f"""
TRACE TOWER EXTENDED TO k = 12.

ALL tr(A^k) ARE SUBSTRATE-DETERMINED:
  Closed form tr(A^k) = 12^k + 24*2^k + 15*(-4)^k

NEW SUBSTRATE IDENTITY:
  tr(A^4) / tr(A^2) = dim F_4 = mu * Phi_3 = 52  *** EXCEPTIONAL LIE DIM ***

ASYMPTOTIC RATIO -> k^2 = 144 = (q*mu)^2:
  Even-step trace ratio converges to the SQUARE OF GRAPH DEGREE.
  Correction rate ~ q^-k (substrate qutrit base).

EVEN-ODD STRUCTURE:
  Odd-k traces inherit chirality from negative eigenvalue s = -4.
  Connects to BT79 Szilassi chirality (42+/0-).

The entire infinite trace tower of A factors through substrate
primitives. Every spectral moment of W(3,3) is computable from
the substrate spectrum {{12, 2, -4}} = {{k, r, s}} with multiplicities
{{1, 24, 15}} = {{1, f, g_neg}}.
""")

    out = Path("data") / "w33_BREAKTHROUGH_117_trace_tower_extension.json"
    out.parent.mkdir(exist_ok=True)
    traces = {kk: 1 * k_eig ** kk + f * r_eig ** kk + g_neg * s_eig ** kk for kk in range(2, 13)}
    out.write_text(json.dumps({
        "closed_form": "tr(A^k) = 12^k + 24*2^k + 15*(-4)^k",
        "extended_values": traces,
        "asymptotic_even_ratio": "k^2 = 144 = (q*mu)^2",
        "correction_rate": "q^-k",
        "F4_surprise": "tr(A^4)/tr(A^2) = 52 = dim F_4",
        "chirality_link": "odd-k via s = -4 eigenvalue (BT79 Szilassi 42+/0-)",
        "new_substrate_identities": [
            "tr(A^4)/tr(A^2) = dim F_4 (exceptional Lie)",
            "even-step ratio asymptote = k^2 = (q*mu)^2 = 144",
            "correction rate = q^-k (qutrit base)",
        ],
        "conclusion": (
            "Trace tower extended to k=12. All tr(A^k) substrate-determined "
            "via closed form 12^k + 24*2^k + 15*(-4)^k. tr(A^4)/tr(A^2) = "
            "52 = dim F_4 is a striking new substrate identity. Asymptotic "
            "even ratio = k^2 = 144 = (q*mu)^2. Chirality propagates from "
            "s = -4 to odd-k trace terms."
        ),
    }, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
