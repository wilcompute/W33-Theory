# BT873 — The Two-Zeta Duality and the Non-Backtracking Walk Census

**Status: PROVEN (Hashimoto operators for both graphs + exact Matrix-Tree, `analysis/bt873_dual_zeta_walk_census.py`, data `data/bt873_dual_zeta_walk_census.json`)**

Completing the BT870/BT872 zeta–gravity arc with the complement graph. Two
complementary graphs carry two Ihara zetas, and their Perron points write the
two Standard-Model sector dimensions.

## T1 — The non-backtracking walk census (W₃,₃)

Tr(Bⁿ) = number of length-n non-backtracking closed walks:

```text
N₁=0, N₂=0, N₃=960, N₄=13920, N₅=181440, N₆=1818240, N₇=19178880
N₃ = 960 = μ·|E| = 4·240
N₅ = 181440 = |E|·q^q·n_even = 240·27·28
Nₙ ~ 11ⁿ  (graph prime number theorem; N₇/N₆ → ~10.5 → 11)
```

The first nontrivial walk count is the Klein-bitangent-flavored
240·27·28 — the edge count, the Heisenberg-Weyl order, and n_even all in one.

## T2 — The dual zeta (matter graph Q)

Q = SRG(40,27,18,18) has its own Hashimoto operator (1080×1080): Perron
**26 = k′−1 = 2Φ₃**, with all complex eigenvalues at **|u|² = 26** (Q is
Ramanujan on its circle |u| = 1/√26). The Bass matrix at u=1 is
27I − A_Q = the Laplacian of Q, and Matrix-Tree gives

```text
v·τ(Q) = 30²⁴·24¹⁵ = 2⁶⁹·3³⁹·5²⁴   ⟹   τ(Q) = 2⁶⁶·3³⁹·5²³
```

with **3-exponent 39 = q·Φ₃ = the gauge-sector dimension**.

## T3 — The duality

| graph | role | Ihara prime | gravity τ | entropy exponent |
| --- | --- | --- | --- | --- |
| W(3,3) = SRG(40,12,2,4) | states / collinearity | 11 = k−1 | 2⁸¹·5²³ | **81 = q⁴ = matter dim** |
| Q = SRG(40,27,18,18) | matter / non-collinearity | 26 = 2Φ₃ | 2⁶⁶·3³⁹·5²³ | **39 = q·Φ₃ = gauge dim** |

The two complementary graphs' discrete-gravity partition functions carry the
two Standard-Model sector dimensions in their prime exponents — matter (q⁴)
on the states graph, gauge (q·Φ₃) on the matter graph — with the cosmological
tier charge 5²³ shared. Complementation (collinearity ↔ non-collinearity)
exchanges the matter and gauge sector dimensions in the gravitational entropy.
Both graphs satisfy the graph Riemann Hypothesis on their own critical
circles (1/√11 and 1/√26).

## Reading

The substrate is a *pair* of zeta functions — states and matter, prime 11 and
prime 26 — and the Standard-Model sector dimensions are their gravitational
entropies. Transport, gravity, matter, and gauge are four readings of two
complementary Ihara zetas; the shared cosmological 5²³ is the one charge that
survives complementation.

## Open

- The full Q zeta closed form (degree 1080) and its discriminants
  (analogues of Φ₄², −v, −μΦ₆).
- 26 = 2Φ₃ is not prime — Q's "graph PNT" has base 26; the non-Ramanujan
  arithmetic vs W33's prime 11.
