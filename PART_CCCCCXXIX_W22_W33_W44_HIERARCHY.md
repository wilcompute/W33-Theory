# PART_CCCCCXXIX_W22_W33_W44_HIERARCHY.md

## The Master Equation Selects q = 3

The master equation underlying the W(3,3) theory is
\[
q! = 2q,
\]
which has a unique positive-integer solution \(q=3\) (since \(3!=6=2\cdot3\)).

The nearby cases show why only \(q=3\) works:

| \(q\) | \(q!\) | \(2q\) | \(q!-2q\) | GQ exists? |
|---|---|---|---|---|
| 2 | 2 | 4 | \(-2\) | Yes, W(2,2) |
| **3** | **6** | **6** | **0** | **Yes, W(3,3)** |
| 4 | 24 | 8 | \(+16\) | Yes, W(4,4) |

Only \(q=3\) forces the equation to zero.

## The Three Graphs

### W(2,2) — the Doily
- Parameters: SRG(15, 6, 1, 3)
- Related to \(E_6\): the 27 lines of a cubic surface are encoded by the collinearity graph of W(2,2)
- Automorphism group: \(\mathrm{Sp}(4,2)\cong S_6\), order 720

### W(3,3) — the Standard Model Graph
- Parameters: SRG(40, 12, 2, 4)
- Related to \(E_8\): the 240 roots, 480 directed roots, and the unique positive-integer solution \(q=3\)
- Automorphism group: \(\mathrm{PSp}(4,3)\), order 25920
- Ramanujan, optimal expander, exactly periodic quantum walk

### W(4,4)
- Parameters: SRG(85, 20, 3, 5)
- Related to a unital \(U(4)\)
- Master equation gives \(q!-2q=16\neq 0\): no selection
- Automorphism group: \(\mathrm{PSp}(4,4)\), order 979200

## The E6 – E8 Mirror

The passage W(2,2) → W(3,3) mirrors the Lie-algebraic embedding
\[
E_6 \hookrightarrow E_8.
\]
This is not accidental: the 27-dimensional \(E_6\) module indexes the 27 lines of the cubic surface (= lines of W(2,2)), while the 248-dimensional \(E_8\) contains all information about W(3,3). The fact that \(q=3\) is the unique master-equation solution means that \(E_8\), not \(E_6\) or \(F_4\), is the algebraic container of the physically realistic structure.
