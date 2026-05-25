"""W(3,3) PRIME-SEQUENCE SUBSTRATE IDENTITIES.

The integer parts of substrate-constant predictions occur at
substrate-determined positions in the prime sequence.

CORE IDENTITY:

  alpha^(-1)_integer = 137 = p_33 = p_(q * p_Ih)

where p_n is the n-th prime number.  At q=3, p_Ih=11, q*p_Ih=33,
and the 33rd prime is exactly 137.

HEEGNER-PRIME-INDEX TABLE:

  Heegner_n  Heegner number   Prime index   Index in substrate
  ---------  --------------   -----------   -------------------
  H_1        1                (not prime)   --
  H_2        2                p_1            1
  H_3        3                p_2            2
  H_4        7                p_4            mu (substrate)
  H_5        11               p_5            mu + 1 = Csaszar realiz.
  H_6        19               p_8            2^q (substrate byte)
  H_7        43               p_14           2*Phi_6 = dim G_2
  H_8        67               p_19           Heegner_6 = sig_-(K3)
  H_9        163              p_38           2*Heegner_6 = 2*sig_-(K3)

So the Heegner numbers (for n >= 4) occur at substrate-meaningful
prime positions:

  H_4 = p_mu, H_5 = p_(mu+1), H_6 = p_(2^q),
  H_7 = p_(2*Phi_6), H_8 = p_(H_6), H_9 = p_(2*H_6).

The cleanest substrate META-IDENTITY: H_8 = p_(H_6).

OTHER PRIME-INDEX SUBSTRATE IDENTITIES:

  alpha^(-1)_integer = 137 = p_33 = p_(q * p_Ih)
  m_Z (GeV) = 91 (NOT prime; 91 = 7 * 13 = Phi_6 * Phi_3)
  m_W (GeV) = 80 (NOT prime; 80 = 2v)
  Heegner_67 (m_tau denom) = 67 = p_(Heegner_6) = p_(H_6)

The deepest one: alpha^(-1) integer part is the prime indexed by
the product q * p_Ih, the substrate's fundamental-quantum times
Ihara prime.

CONNECTION TO PRIME GAPS:

The prime gap g_n = p_(n+1) - p_n at substrate-meaningful positions:

  At n=33 (alpha index): p_33 = 137, p_34 = 139. Gap g_33 = 2 (twin prime!).
  At n=19 (Heegner_67 index): p_19 = 67, p_20 = 71. Gap g_19 = 4 = mu.
  At n=14 (Heegner_7 index): p_14 = 43, p_15 = 47. Gap g_14 = 4 = mu.

So alpha^(-1) sits at a TWIN PRIME position (137, 139), and the
upper Heegner numbers sit at mu-gap positions.
"""
from __future__ import annotations

import json
from pathlib import Path
from sympy import primerange


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
P_IH = K_CODEC - 1
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1


def first_primes(n: int) -> list[int]:
    return list(primerange(2, 1000))[:n]


def heegner_prime_indices() -> list[dict]:
    """Find prime index of each Heegner number."""
    primes = first_primes(50)
    heegners = {1: 1, 2: 2, 3: 3, 4: 7, 5: 11, 6: 19, 7: 43, 8: 67, 9: 163}

    rows = []
    for n, h in heegners.items():
        if h in primes:
            idx = primes.index(h) + 1  # 1-indexed
        else:
            idx = None
        rows.append({
            "Heegner_n": n,
            "value":      h,
            "prime_idx":  idx,
        })
    return rows


def alpha_prime_position() -> dict:
    """alpha^(-1) integer = 137 = p_33 = p_(q * p_Ih)."""
    primes = first_primes(50)
    pos_of_137 = primes.index(137) + 1
    substrate_index = Q * P_IH  # = 33
    return {
        "alpha_inv_integer":  137,
        "prime_index":        pos_of_137,
        "substrate_index":    substrate_index,
        "form":               "alpha^(-1) = p_(q * p_Ih)",
        "match":              pos_of_137 == substrate_index,
        "twin_prime_check":   "p_33 = 137, p_34 = 139 (twin prime gap = 2)",
    }


def prime_gap_at_substrate_positions() -> list[dict]:
    primes = first_primes(50)
    rows = []
    for substrate_name, idx in [
        ("alpha index (q*p_Ih)", Q * P_IH),
        ("Heegner_6 index", 8),
        ("Heegner_67 index", 19),
        ("Heegner_43 index", 14),
        ("k index", K_CODEC),
        ("v/2 index", 20),
    ]:
        if idx <= len(primes) - 1:
            p = primes[idx - 1]   # 1-indexed
            p_next = primes[idx]
            gap = p_next - p
            rows.append({
                "substrate_position": substrate_name,
                "index_n":            idx,
                "p_n":                p,
                "p_{n+1}":            p_next,
                "gap":                gap,
            })
    return rows


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
            },
        },
        "heegner_prime_indices":   heegner_prime_indices(),
        "alpha_prime_position":     alpha_prime_position(),
        "prime_gap_at_substrate":   prime_gap_at_substrate_positions(),
        "headline": (
            "Striking prime-sequence substrate identities:\n"
            "  alpha^(-1)_int = 137 = p_(q * p_Ih) = p_33  (33rd prime)\n"
            "  Heegner_67 = 67 = p_(Heegner_6) = p_19      (19th prime)\n"
            "  Heegner_9 = 163 = p_(2 * Heegner_6) = p_38   (38th prime)\n"
            "Alpha sits at a TWIN PRIME (137, 139) position; upper "
            "Heegners sit at mu-gap (g=4) positions in the prime sequence."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_prime_sequence_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) PRIME-SEQUENCE SUBSTRATE IDENTITIES")
    print("=" * 78)

    print(f"\nHeegner numbers and their prime indices:")
    print(f"  {'H_n':>5s}  {'value':>5s}  {'prime_idx':>10s}")
    for r in payload["heegner_prime_indices"]:
        idx_str = str(r["prime_idx"]) if r["prime_idx"] else "--"
        print(f"  {r['Heegner_n']:>3d}    {r['value']:>4d}  {idx_str:>8s}")

    a = payload["alpha_prime_position"]
    print(f"\nAlpha prime-position identity:")
    print(f"  alpha^(-1)_int = {a['alpha_inv_integer']}")
    print(f"  prime index: p_{a['prime_index']} = {a['alpha_inv_integer']}")
    print(f"  substrate: q * p_Ih = {a['substrate_index']}")
    print(f"  match: {a['match']}")
    print(f"  {a['twin_prime_check']}")

    print(f"\nPrime gaps at substrate-meaningful positions:")
    for r in payload["prime_gap_at_substrate"]:
        print(f"  {r['substrate_position']:>25s} (n={r['index_n']}): p={r['p_n']}, gap={r['gap']}")

    print(f"\nHEADLINE:")
    print(payload["headline"])

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
