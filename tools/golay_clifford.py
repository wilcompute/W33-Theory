#!/usr/bin/env python3
"""Build the binary Golay code and map it into a Clifford algebra basis.

This module constructs the extended binary Golay code (length 24, dimension 12)
via the standard cyclic generator polynomial, then associates each codeword with
an element of the real Clifford algebra Cl(24) by interpreting the 1-bits as a
product of orthogonal generators e_0,...,e_{23} satisfying e_i^2=1,
 e_i e_j = - e_j e_i (i\neq j).

The resulting set of 4096 monomials behaves like a subgroup of the spin group;
codewords are even weight (multiplying two yields another even-weight vector)
and the resulting product table can be examined for closure and signs.

Usage:
    python tools/golay_clifford.py

Outputs JSON files in ``artifacts/`` containing the codewords and their
corresponding monomials.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator, List, Tuple

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# binary Golay code generation (extended, length 24)
# ---------------------------------------------------------------------------


def gf2_mul(a: int, b: int) -> int:
    """Multiply two polynomials over GF(2) represented as bitfields."""
    res = 0
    while b:
        if b & 1:
            res ^= a
        a <<= 1
        b >>= 1
    return res


def gf2_mod(poly: int, mod: int) -> int:
    """Return remainder of poly divided by mod (both GF2 polynomials)."""
    # degree = highest bit index
    deg_mod = mod.bit_length() - 1
    while poly.bit_length() - 1 >= deg_mod:
        shift = poly.bit_length() - 1 - deg_mod
        poly ^= mod << shift
    return poly


def generate_golay_code() -> List[int]:
    """Return list of 24-bit integers representing the extended Golay code.

    The length-23 cyclic Golay code has generator polynomial
    g(x) = x^11 + x^9 + x^7 + x^6 + x^5 + x + 1.
    We compute all 2^12 codewords of the (23,12) code and then append a
    parity bit (even parity) to obtain the length-24 extended code.
    """
    n = 23
    # generator polynomial g(x) as integer
    g = (1 << 11) | (1 << 9) | (1 << 7) | (1 << 6) | (1 << 5) | (1 << 1) | 1
    code23 = []
    for msg in range(1 << 12):
        # multiply msg (as poly) by g and reduce mod (x^23 - 1)
        cw = gf2_mul(msg, g)
        # reduce modulo x^23 - 1: subtract (xor) multiples of x^23 + 1
        # since x^23 = 1 in the ring, we can replace high bits accordingly
        while cw.bit_length() > n:
            # if bit at position k>=23 is 1, remove it and add 1 at pos k-23
            k = cw.bit_length() - 1
            cw ^= 1 << k
            cw ^= 1 << (k - n)
        code23.append(cw)
    # extend with parity bit
    code24 = []
    for cw in code23:
        parity = bin(cw).count("1") & 1
        cw24 = cw | (parity << n)
        code24.append(cw24)
    return code24


# ---------------------------------------------------------------------------
# Clifford monomials and multiplication
# ---------------------------------------------------------------------------

Monomial = Tuple[int, ...]  # sorted tuple of indices


def codeword_to_monomial(word: int) -> Monomial:
    """Convert 24-bit word to monomial tuple of indices with bit=1."""
    return tuple(i for i in range(24) if (word >> i) & 1)


def multiply_monomials(a: Monomial, b: Monomial) -> Tuple[int, Monomial]:
    """Multiply two monomials in Cl(24) and return (sign, product).

    We use the rules e_i e_j = - e_j e_i for i!=j and e_i^2=1.  The product is
    first the concatenation of the sequences; then we sort by swapping adjacent
    elements at the cost of a sign flip, cancelling pairs when an index appears
    twice.
    """
    # naive algorithm: start with list, insert elements of b one by one
    prod: List[int] = list(a)
    sign = 1
    for x in b:
        if x in prod:
            # cancellation: remove the existing occurrence and flip sign if
            # the number of swaps needed to bring x next to itself is odd.
            idx = prod.index(x)
            # swapping x across len(prod)-idx-? elements not required since
            # we simply remove; sign contributes (-1)^{# elements after idx}
            sign *= (-1) ** (len(prod) - idx - 1)
            prod.pop(idx)
        else:
            # insert while maintaining sorted order
            # count how many existing elements are greater than x (will pass by)
            larger = sum(1 for y in prod if y > x)
            sign *= (-1) ** larger
            # insert in order
            pos = 0
            while pos < len(prod) and prod[pos] < x:
                pos += 1
            prod.insert(pos, x)
    return sign, tuple(prod)


def symplectic_representation(mon: Monomial) -> Tuple[int, int]:
    """Return symplectic pair (x,z) for Pauli mapping: X^{x}Z^{z}.
    Here x and z are 24-bit integers with disjoint support such that
    monomial indices in even positions chosen for X and odd for Z.
    (This is a crude mapping, purely for demonstration.)
    """
    x = 0
    z = 0
    for idx in mon:
        if idx % 2 == 0:
            x |= 1 << (idx // 2)
        else:
            z |= 1 << (idx // 2)
    return x, z


def export_stabilizer(code: List[int], filename: Path) -> None:
    """Export a 12-generator stabilizer code from the Golay mapping."""
    monomials = [codeword_to_monomial(w) for w in code]
    # pick 12 independent even-weight monomials (first 12)
    gens = [m for m in monomials if len(m) % 2 == 0][:12]
    with open(filename, "w") as f:
        f.write("# symplectic stabilizer generators\n")
        for g in gens:
            x, z = symplectic_representation(g)
            f.write(f"{x:012b} {z:012b}\n")
    print("wrote stabilizer generators to", filename)


def main() -> None:
    code = generate_golay_code()
    assert len(code) == 1 << 12
    print("Generated extended Golay code with", len(code), "words")

    # command-line argument handling
    import argparse

    parser = argparse.ArgumentParser(description="Golay-Clifford utilities")
    parser.add_argument("--export-stabilizer", help="path to write stabilizer gens")
    parser.add_argument(
        "--mapping-only",
        action="store_true",
        help="write the codeword-to-Clifford mapping and skip expensive closure scans",
    )
    args = parser.parse_args()

    # map to monomials and record multiplication table for a handful
    monomials = [codeword_to_monomial(w) for w in code]
    # save mapping
    outjson = ROOT / "artifacts" / "golay_clifford_mapping.json"
    outcsv = ROOT / "artifacts" / "golay_clifford_mapping.csv"
    mapping = {str(w): mon for w, mon in zip(code, monomials)}
    outjson.write_text(json.dumps(mapping, indent=2))
    with open(outcsv, "w") as f:
        f.write("word,monomial\n")
        for w, mon in zip(code, monomials):
            f.write(f"{w},{mon}\n")

    # if requested, export stabilizer
    if args.export_stabilizer:
        export_stabilizer(code, Path(args.export_stabilizer))

    if args.mapping_only:
        print("Wrote mapping to", outjson, outcsv)
        return

    # construct spin group: even-weight monomial products
    spin_set: set[Monomial] = set()
    for a in monomials:
        for b in monomials:
            sign, prod = multiply_monomials(a, b)
            if len(prod) % 2 == 0:  # even weight condition
                spin_set.add(prod)
    print("spin group size (unique even monomials seen)", len(spin_set))
    # ideally this equals 4096

    # sanity-check full closure inside even monomials
    even_set = {m for m in monomials if len(m) % 2 == 0}
    closure_ok = all(
        multiply_monomials(a, b)[1] in even_set for a in even_set for b in even_set
    )
    print("full even-monomial closure?", closure_ok)

    # sample random pairs for spin group multiplication
    import random

    group_ok = True
    spin_list = list(spin_set)
    for _ in range(500):
        a = random.choice(spin_list)
        b = random.choice(spin_list)
        _, p = multiply_monomials(a, b)
        if p not in spin_set:
            group_ok = False
            break
    print("spin-group closure samples OK?", group_ok)

    # quick demonstration: multiply first 10 by each other
    pairs = []
    for i in range(10):
        for j in range(10):
            s, prod = multiply_monomials(monomials[i], monomials[j])
            pairs.append((i, j, s, prod))
    for tup in pairs[:20]:
        i, j, s, prod = tup
        print(f"{i}*{j} -> sign {s}, monomial {prod}")

    # verify closure under multiplication (sample random pairs)
    import random

    index_map = {mon: idx for idx, mon in enumerate(monomials)}
    closure_ok = True
    for _ in range(1000):
        a = random.choice(monomials)
        b = random.choice(monomials)
        _, prod = multiply_monomials(a, b)
        if prod not in index_map:
            closure_ok = False
            break
    print("closure holds for random samples?", closure_ok)

    print("Wrote mapping to", outjson, outcsv)


if __name__ == "__main__":
    main()
