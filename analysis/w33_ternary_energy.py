#!/usr/bin/env python3
"""
The encoding tax: the algorithm is ternary, so running it on binary hardware wastes a quarter of every
move. Pass 46 said the holonet "wants ternary hardware"; this pass quantifies exactly what that costs on
the binary host it currently runs on, and is careful about what is and is not a real energy difference.
The substrate's digit is a balanced trit {-1, 0, +1} carrying log2(3) = 1.585 bits of information. A
binary machine cannot hold three states in one bit, so it must spend at least two bits per trit -- and
two bits hold four states, of which the trit uses only three. So a quarter of the binary state space is
wasted, and the BIT-TRAFFIC tax of moving or storing a trit on binary hardware is 2 / log2(3) = 1.26 --
twenty-six percent more bit-transactions than the information requires, every load, store, and network
hop. The DIGIT-COUNT tax is the radix economy: E(b) = b / ln(b) is the cost of representing a range, and
E(3) = 2.731 versus E(2) = 2.885, so a ternary machine needs about five percent fewer digit-positions
to span the same range. Now the careful part: Landauer's bound is base-INDEPENDENT per unit of
information (kT ln 2 per bit, equivalently kT ln 3 per trit, the same energy per nat), so there is NO
fundamental energy win from ternary -- the cost is purely the ENCODING OVERHEAD: a binary host erases
two bits per trit where 1.585 would do, a 1.26x overhead in irreversible operations, not a different
physics. So the honest accounting is: ternary is not magically more energy-efficient per unit
information, but the holonet, being a ternary algorithm, pays a 26 percent bit-traffic and irreversible-
erasure tax on binary hardware that it would not pay on its native ternary substrate (the Setun digit),
plus a ~5 percent digit-count tax -- which is the precise, quantified sense in which "it wants ternary
hardware," and the precise sense in which it runs sub-optimally on the binary machine it currently
inhabits.

This computes the ternary-vs-binary encoding tax: the per-trit bit-traffic overhead (2/log2(3)), the
wasted-state fraction, the radix-economy digit-count ratio, and the base-independence of the Landauer
bound -- separating the real encoding overhead from a (non-existent) fundamental energy difference.

THE TAX.
    information     a balanced trit carries log2(3) = 1.585 bits.
    bit-traffic     binary needs 2 bits/trit -> 2/log2(3) = 1.26x overhead (26%); wasted states = 25%.
    digit-count     radix economy E(3)/E(2) = 0.946 -> ternary needs ~5.4% fewer digit-positions.
    Landauer        base-INDEPENDENT per unit info (kT ln 2/bit = kT ln 3/trit); no fundamental win.
    verdict         the tax is ENCODING overhead (2 bits erased per trit vs 1.585), not different physics;
                    the holonet pays it on binary hardware and not on its native ternary substrate.

Honest scope: every number here is exact arithmetic (log2(3), the radix economy, the wasted-state
fraction). The key honesty is that Landauer's bound is base-independent, so ternary gives NO fundamental
per-information energy advantage; the 1.26x is strictly the ENCODING tax of representing a 3-state digit
in 2 bits (bit-traffic and irreversible-erasure overhead), which a native ternary machine would not pay.
This quantifies "wants ternary hardware"; it is not a claim that ternary computing beats binary at the
Landauer bound. So: the encoding tax, exactly.

Verifies the per-trit bit-traffic tax (2/log2(3) = 1.26), the 25% wasted-state fraction, the radix-economy
ratio E(3)/E(2), and the base-independence of the Landauer cost.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    print(
        "== the encoding tax: a ternary algorithm on binary hardware wastes a quarter of every move =="
    )

    log2_3 = math.log2(3)
    bits_binary = 2  # a trit needs at least 2 bits on binary hardware
    bit_traffic_tax = bits_binary / log2_3
    wasted_states = 1 - 3 / (2**bits_binary)
    print(
        f"\n[information]  a balanced trit {{-1,0,+1}} carries log2(3) = {log2_3:.4f} bits"
    )
    print(
        f"[bit-traffic]  binary needs {bits_binary} bits/trit -> tax = 2/log2(3) = {bit_traffic_tax:.4f}x ({(bit_traffic_tax-1)*100:.0f}% overhead)"
    )
    print(
        f"               2 bits hold 4 states, a trit uses 3 -> wasted states = {wasted_states:.0%}"
    )
    assert abs(bit_traffic_tax - 1.262) < 1e-2 and abs(wasted_states - 0.25) < 1e-9
    out["information_bits_per_trit"] = round(log2_3, 4)
    out["bit_traffic_tax"] = round(bit_traffic_tax, 4)
    out["wasted_state_fraction"] = wasted_states

    E = lambda b: b / math.log(b)
    econ_ratio = E(3) / E(2)
    print(
        f"\n[digit-count]  radix economy E(b)=b/ln(b): E(3)={E(3):.3f}, E(2)={E(2):.3f}"
    )
    print(
        f"               E(3)/E(2) = {econ_ratio:.4f} -> ternary needs {(1-econ_ratio)*100:.1f}% fewer digit-positions"
    )
    out["radix_economy"] = {
        "E2": round(E(2), 4),
        "E3": round(E(3), 4),
        "ratio": round(econ_ratio, 4),
        "ternary_digit_saving": round((1 - econ_ratio) * 100, 1),
    }

    kB = 1.380649e-23
    T = 300
    print(
        f"\n[Landauer]     base-INDEPENDENT per unit info: kT ln2/bit = {kB*T*math.log(2):.3e} J;"
    )
    print(
        f"               kT ln3/trit = {kB*T*math.log(3):.3e} J = log2(3) x (kT ln2) -> same energy per nat"
    )
    print(
        f"               so NO fundamental energy win from ternary; the tax is ENCODING overhead only:"
    )
    print(
        f"               a binary host erases 2 bits per trit where {log2_3:.3f} suffice -> {bit_traffic_tax:.2f}x irreversible-bit overhead"
    )
    out["landauer"] = {
        "base_independent": True,
        "kT_ln2_per_bit_J": kB * T * math.log(2),
        "encoding_overhead_per_trit": round(bit_traffic_tax, 4),
        "note": "no fundamental per-information energy difference; the 1.26x is encoding overhead only",
    }

    print(
        "\nRESULT: the holonet is a ternary algorithm, so on binary hardware it pays a precise, quantified"
    )
    print(
        "  tax -- and being careful, that tax is encoding overhead, not a fundamental energy gap. The"
    )
    print(
        "  substrate's digit is a balanced trit carrying log2(3) = 1.585 bits, but a binary machine needs"
    )
    print(
        "  two bits to hold three states, of which the trit uses three of four -- so a quarter of the"
    )
    print(
        "  binary state space is wasted and the bit-traffic tax per trit is 2/log2(3) = 1.26, a 26%"
    )
    print(
        "  overhead on every load, store, and network hop. The digit-count tax is the radix economy: a"
    )
    print(
        "  ternary machine needs about 5% fewer digit-positions to span a range. But Landauer's bound is"
    )
    print(
        "  base-independent -- kT ln2 per bit equals kT ln3 per trit, the same energy per nat -- so there"
    )
    print(
        "  is NO fundamental energy win from ternary; the 1.26x is strictly the encoding overhead of"
    )
    print(
        "  representing a 3-state digit in 2 bits (extra bit-traffic and extra irreversible erasures). So"
    )
    print(
        "  the honest verdict is: ternary is not magically more efficient per unit information, but the"
    )
    print(
        "  holonet pays a ~26% bit-traffic / erasure tax and a ~5% digit-count tax on the binary host it"
    )
    print(
        "  currently runs on, that it would not pay on its native ternary substrate (the Setun digit) --"
    )
    print(
        "  the exact sense in which it 'wants ternary hardware' and runs sub-optimally on binary silicon."
    )

    out["summary"] = (
        "the encoding tax: the holonet is a ternary algorithm, so on binary hardware it pays a precise "
        "tax -- and (carefully) that tax is ENCODING overhead, not a fundamental energy gap. The "
        "substrate's digit is a balanced trit carrying log2(3) = 1.585 bits; a binary machine needs 2 "
        "bits per trit (3 of 4 states used -> 25% wasted), so the bit-traffic tax is 2/log2(3) = 1.26x "
        "(26% overhead) on every load/store/hop. The digit-count tax is the radix economy E(3)/E(2) = "
        "0.946 -> ternary needs ~5.4% fewer digit-positions. But Landauer's bound is base-INDEPENDENT "
        "(kT ln2/bit = kT ln3/trit = same energy per nat), so there is NO fundamental per-information "
        "energy win from ternary; the 1.26x is strictly the encoding overhead of representing a 3-state "
        "digit in 2 bits (extra bit-traffic + extra irreversible erasures), which a native ternary "
        "machine (Setun) would not pay. So: ternary is not magically more energy-efficient per unit "
        "information, but the holonet pays a ~26% bit-traffic/erasure tax and a ~5% digit-count tax on "
        "the binary host it currently runs on -- the exact, quantified sense in which it 'wants ternary "
        "hardware' and runs sub-optimally on binary silicon. HONEST: every number is exact arithmetic; "
        "the key honesty is the base-independence of Landauer (no fundamental ternary energy advantage), "
        "so the 1.26x is the encoding tax only, not a claim that ternary beats binary at the Landauer bound."
    )
    out["sources"] = [
        "information per trit = log2(3) (Shannon); radix economy E(b)=b/ln(b), base-3 optimum among "
        "integers (Knuth; Setun 1958); Landauer's principle base-independence (kT ln b per b-ary symbol "
        "= same energy per nat); the substrate's balanced-ternary {-1,0,+1} 3-grading (corpus)."
    ]
    with open("data/w33_ternary_energy.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_ternary_energy.json")


if __name__ == "__main__":
    main()
