#!/usr/bin/env python3
"""
The power budget: ternary is thermodynamically free, and error correction is the metabolism. A living
machine has a metabolism -- it spends energy to hold its low-entropy description against noise -- so a
machine that claims to be "the architecture of life" must have a quantified energy cost. This pass
gives it, from Landauer's principle. Two results. FIRST, the choice of balanced ternary costs NOTHING
thermodynamically: Landauer's bound is kT ln(2) per bit erased, and a trit erasure costs kT ln(3),
but a trit carries log2(3) = 1.585 bits, so the cost PER BIT is kT ln(3) / log2(3) = kT ln(2) --
exactly the binary value. The radix is base-INDEPENDENT in energy per unit information; base 3's
advantage (Pass 34's radix economy) is purely in DIGIT COUNT, not in dissipation -- ternary is free.
SECOND, the machine's only irreducible energy cost is ERROR CORRECTION, and it is the machine's
metabolism. The degree-2 Clifford layer is unitary (reversible) -> Landauer-free in the adiabatic
limit (Bennett); the genome (the [[66,8,3]]_3 code) is copied reversibly (von Neumann). The ONE
irreversible step is syndrome extraction: each QEC cycle measures and resets n - k = 66 - 8 = 58
syndrome qutrits, exporting their entropy, at Landauer cost (n-k) kT ln(3) per cycle. This is exactly
Schrodinger's "negative entropy" / Prigogine's dissipative structure: a living system stays ordered by
EXPORTING entropy to its environment, and the QEC cycle IS that entropy export. So the substrate's
metabolic rate is the Landauer cost of syndrome extraction: ~2.6e-19 J per cycle at 300 K, a power of
~2.6e-10 W per logical block at 1 GHz (and ~9e-15 W at a 10 mK dilution-fridge temperature). So the
power budget is: ternary dissipates nothing extra per bit (base-independent Landauer), the Clifford
datapath is reversible (free), and the sole irreducible cost is the entropy export of error
correction -- the machine's metabolism, quantified.

This computes the machine's energy budget from Landauer's principle: the base-independence of the
per-bit cost, the reversibility of the Clifford datapath, and the QEC entropy-export metabolic rate.

THE BUDGET.
    per-bit cost (base-independent).  kT ln(3) / log2(3) = kT ln(2): ternary costs NO extra energy per
        bit; the radix-economy win is in digit count, not dissipation.  (@300 K: kT ln 2 = 2.87e-21 J.)
    reversible datapath.  degree-2 Clifford gates are unitary -> Landauer-free (Bennett, adiabatic);
        the [[66,8,3]]_3 genome is copied reversibly (von Neumann constructor).
    metabolism = error correction.  the one irreversible step is syndrome extraction: n - k = 58
        syndrome qutrits measured + reset per cycle, exporting entropy at (n-k) kT ln(3) per cycle.
        = Schrodinger negative entropy / Prigogine dissipative structure (export entropy to stay ordered).
    metabolic rate.  @300 K: 2.64e-19 J/cycle; @1 GHz -> 2.64e-10 W per logical block.
                     @10 mK (dilution fridge): 8.80e-15 W per block.

Honest scope: Landauer's kT ln(b) is a thermodynamic LOWER bound (real devices dissipate orders of
magnitude more); the base-independence and the reversibility of unitary/Clifford gates (Bennett) are
standard. The substrate content is that the irreversible cost localises to the (n-k) = 58 syndrome
qutrits of the [[66,8,3]]_3 code, identified with the metabolic entropy-export of a dissipative
(living) structure. The numerical rate assumes the chosen clock and temperature. So: a quantified,
Landauer-floor power budget whose only irreducible term is the metabolism of error correction.

Verifies the base-independence of the per-bit Landauer cost, the n-k = 58 syndrome-erasure budget,
and the resulting metabolic rate at several temperatures.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    kB = 1.380649e-23  # J/K
    ln2, ln3 = math.log(2), math.log(3)
    log2_3 = math.log(3, 2)  # 1.585 bits per trit
    print(
        "== the power budget: ternary is thermodynamically free; error correction is the metabolism =="
    )

    # 1) base-independence of the per-bit Landauer cost
    T = 300.0
    cost_per_trit = kB * T * ln3
    cost_per_bit_from_trit = cost_per_trit / log2_3
    cost_per_bit = kB * T * ln2
    print(f"\n[per-bit cost is base-independent]  (T = {T:.0f} K)")
    print(
        f"  kT ln(2) = {cost_per_bit:.3e} J/bit;  kT ln(3) = {cost_per_trit:.3e} J/trit"
    )
    print(
        f"  trit carries log2(3) = {log2_3:.3f} bits -> cost/bit = kT ln3 / log2(3) = {cost_per_bit_from_trit:.3e} J"
    )
    print(
        f"  -> equals kT ln(2): ternary costs NO extra energy per bit (economy is in digit count)"
    )
    assert abs(cost_per_bit_from_trit - cost_per_bit) < 1e-30
    out["base_independence"] = {
        "T_K": T,
        "kT_ln2_per_bit": cost_per_bit,
        "kT_ln3_per_trit": cost_per_trit,
        "bits_per_trit": round(log2_3, 4),
        "cost_per_bit_via_trit": cost_per_bit_from_trit,
        "reading": "kT ln3 / log2(3) = kT ln2 exactly -> per-bit Landauer cost is base-independent; ternary is free",
    }

    # 2) reversible datapath
    print(
        f"\n[reversible datapath]  degree-2 Clifford gates are unitary -> Landauer-free (Bennett);"
    )
    print(
        f"  the [[66,8,3]]_3 genome is copied reversibly (von Neumann universal constructor)"
    )
    out["reversible_datapath"] = {
        "clifford": "degree-2 Clifford gates are unitary -> reversible, Landauer-free in the adiabatic limit (Bennett)",
        "genome_copy": "the [[66,8,3]]_3 code is copied reversibly (von Neumann constructor)",
    }

    # 3) metabolism = error correction (syndrome extraction)
    n, k = 66, 8
    synd = n - k  # 58 syndrome qutrits per cycle
    print(
        f"\n[metabolism = error correction]  the one irreversible step is syndrome extraction:"
    )
    print(
        f"  n - k = {n} - {k} = {synd} syndrome qutrits measured + reset per cycle -> entropy export"
    )
    print(
        f"  = Schrodinger negative entropy / Prigogine dissipative structure (export entropy to stay ordered)"
    )
    rows = []
    f_clock = 1e9
    for Tx, label in [
        (300.0, "room"),
        (4.0, "liquid He"),
        (0.01, "dilution fridge 10 mK"),
    ]:
        e_cycle = synd * kB * Tx * ln3
        power = e_cycle * f_clock
        rows.append(
            {
                "T_K": Tx,
                "label": label,
                "E_per_cycle_J": e_cycle,
                "power_W_at_1GHz": power,
            }
        )
        print(
            f"    T = {Tx:>6} K ({label:22s}): E/cycle = {e_cycle:.3e} J;  P@1GHz = {power:.3e} W/block"
        )
    assert synd == 58
    out["metabolism"] = {
        "irreversible_step": "syndrome extraction (measure + reset the syndrome qutrits)",
        "syndrome_qutrits_per_cycle": synd,
        "cost_per_cycle": "(n-k) kT ln(3)",
        "identification": "Schrodinger negative entropy / Prigogine dissipative structure -- entropy export = the metabolism of staying alive",
        "rate_table": rows,
    }

    print(
        "\nRESULT: the machine has a quantified metabolism. First, the choice of balanced ternary"
    )
    print(
        "  costs nothing thermodynamically: Landauer's bound is kT ln(2) per bit, a trit erasure"
    )
    print(
        "  costs kT ln(3), but a trit carries log2(3) = 1.585 bits, so cost per bit = kT ln(3) /"
    )
    print(
        "  log2(3) = kT ln(2) exactly -- base-independent. Base 3's advantage (the radix economy)"
    )
    print(
        "  is purely in digit count, not dissipation; ternary is free. Second, the only irreducible"
    )
    print(
        "  energy cost is error correction, and it is the metabolism. The degree-2 Clifford datapath"
    )
    print(
        "  is unitary, hence reversible and Landauer-free (Bennett), and the [[66,8,3]]_3 genome is"
    )
    print(
        "  copied reversibly (von Neumann); the one irreversible step is syndrome extraction -- each"
    )
    print(
        "  cycle measures and resets n - k = 58 syndrome qutrits, exporting their entropy at cost"
    )
    print(
        "  (n-k) kT ln(3) per cycle. That is exactly Schrodinger's negative entropy / Prigogine's"
    )
    print(
        "  dissipative structure: a living system stays ordered by exporting entropy, and the QEC"
    )
    print(
        "  cycle IS that export. The metabolic rate is ~2.6e-19 J/cycle at 300 K -> ~2.6e-10 W per"
    )
    print(
        "  logical block at 1 GHz (~9e-15 W at 10 mK). So: ternary dissipates nothing extra per bit,"
    )
    print(
        "  the Clifford datapath is free, and the sole irreducible cost is the entropy export of"
    )
    print(
        "  error correction -- the machine's metabolism, quantified. Honest: Landauer is a lower"
    )
    print(
        "  bound (real devices dissipate far more); the localisation to the 58 syndrome qutrits and"
    )
    print(
        "  the metabolism identification are the substrate content; the rate assumes clock + T."
    )

    out["summary"] = (
        "the power budget: ternary is thermodynamically free, and error correction is the metabolism. "
        "(1) Base-independence: Landauer's bound is kT ln(2)/bit; a trit erasure costs kT ln(3) but "
        "carries log2(3) = 1.585 bits, so cost/bit = kT ln3 / log2(3) = kT ln2 EXACTLY -- the per-bit "
        "Landauer cost is base-independent, so base 3's radix-economy win is in digit count, not "
        "dissipation; ternary is free (kT ln2 = 2.87e-21 J/bit @300 K). (2) Reversible datapath: "
        "degree-2 Clifford gates are unitary -> Landauer-free (Bennett); the [[66,8,3]]_3 genome is "
        "copied reversibly (von Neumann). (3) Metabolism = error correction: the one irreversible step "
        "is syndrome extraction -- n-k = 58 syndrome qutrits measured + reset per cycle, exporting "
        "entropy at (n-k) kT ln(3)/cycle = Schrodinger negative entropy / Prigogine dissipative "
        "structure (export entropy to stay ordered). Metabolic rate: 2.64e-19 J/cycle @300 K -> "
        "2.64e-10 W per logical block @1 GHz (8.80e-15 W @10 mK). So ternary dissipates nothing extra "
        "per bit, the Clifford datapath is free, and the sole irreducible cost is the entropy export "
        "of error correction -- the machine's metabolism. HONEST: Landauer kT ln(b) is a thermodynamic "
        "LOWER bound (real devices dissipate orders more); base-independence and Clifford reversibility "
        "(Bennett) are standard; the substrate content is the localisation of irreversible cost to the "
        "58 syndrome qutrits of [[66,8,3]]_3, identified with the metabolism of a dissipative (living) "
        "structure; the numerical rate assumes the chosen clock and temperature."
    )
    out["sources"] = [
        "Landauer's principle (kT ln 2 per bit erased; kT ln b per b-ary symbol); Bennett reversible "
        "computation (unitary/Clifford gates Landauer-free); Schrodinger 'What is Life?' (negative "
        "entropy) and Prigogine dissipative structures (entropy export); [[66,8,3]]_3 code n=66, k=8 "
        "-> n-k=58 syndrome qutrits (QEC track); von Neumann self-reproducing automata (reversible "
        "genome copy)."
    ]
    with open("data/w33_power_budget.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_power_budget.json")


if __name__ == "__main__":
    main()
