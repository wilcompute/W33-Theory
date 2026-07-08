# Pass 91 — Aut(W(3,3)) IS the Weyl group of E₆ (the symmetry capstone)

**Status: PASS** — GAP `w33_pass91_e6.g` → `w33_pass91_e6_out.txt`; witness `w33_pass91_e6.py`
(6/6 checks); test `tests/test_pass91_e6.py` (4/4).

Pass 90 found the two GQ(3,3) graphs have |Aut| = 51840 = |W(E₆)| = |Sp(4,3)|. This pass upgrades
that from an order coincidence to a **proved group isomorphism**.

## Verified in GAP
- **|Aut(W(3,3))| = 51840**; its **derived subgroup is the simple group of order 25920**, named by
  GAP `B(2,3) = O(5,3) ~ C(2,3) = S(4,3) ~ 2A(3,2) = U(4,2) ~ 2D(3,2) = O⁻(6,2)` — i.e.
  **PSp(4,3) = PSU(4,2) = PΩ₆⁻(2)** — of index 2. So **Aut(W) = PSp(4,3):2**.
- **W(E₆)** has the same order 51840 and the same simple derived subgroup, and
  **`IsomorphismGroups(Aut(W), W(E₆))` succeeds**: Aut(W(3,3)) ≅ W(E₆).

## Why it's the capstone
The whole arithmetic tower of W(3,3) sits under one exceptional symmetry, **W(E₆) = Sp(4,3)**, which
acts on the E₆ cubic-surface configuration — and every one of those orbit numbers has already
appeared in the tower:

| E₆ number | meaning | where it appears |
|---|---|---|
| 27 | lines on the cubic surface | E₆ minuscule |
| 36 | double-sixes | |
| **45** | tritangent planes | = the 45 minimum-weight codewords of C₂(W)=[40,16,8] (**Pass 85**) |
| 72 | roots of E₆ | |
| **78** | dim E₆ = 2(f+g) | = the Ihara oscillatory amplitude (**Pass 74**) |
| **240** | roots of E₈ = edges of W(3,3) | = 240 minimum-weight words of the dual [40,24] (**Pass 86**) |

So the **symmetry (W(E₆))**, the **code (45, 240)**, and the **arithmetic (zeta, class group, Smith
group, lattice, modular form)** are three faces of one exceptional object. The graph automorphism
group of the symplectic GQ W(3,q) is PΓSp(4,q); at q=3 (trivial field automorphism) this is
PSp(4,3):2 = W(E₆) = SO₅(3).

## Files
- `w33_pass91_e6.g`, `w33_pass91_e6_out.txt` — GAP certificate (derived subgroup + IsomorphismGroups).
- `w33_pass91_e6.py`, `.json` — witness (6 checks).
- `tests/test_pass91_e6.py` — 4 assertions.
