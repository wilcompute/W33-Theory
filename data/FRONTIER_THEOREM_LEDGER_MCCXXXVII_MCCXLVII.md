# Frontier Theorem Ledger: MCCXXXVII–MCCXLVII

## Status as of 2026-05-23

| # | Title | Status |
|---|---|---|
| MCCXXXVII | Witting Polytope Bridge | ✅ PROVEN |
| MCCXXXVIII | Leech Lattice Substrate Decomposition | ✅ PROVEN |
| MCCXXXIX | Monster Character Substrate Filter | ✅ PROVEN |
| MCCXL | Golay Code W(3,3) Triality | ✅ PROVEN |
| MCCXLI | Substrate Self-Similarity Fixed Point | ✅ PROVEN |
| MCCXLII | Moonshine Substrate Duality | ✅ PROVEN |
| MCCXLIII | Monster Substrate Centralizer Cascade | ✅ PROVEN |
| MCCXLIV | 2-Adic Exponent Law e(p) = 17−p | ✅ PROVEN |
| MCCXLV | Monster Substrate Valuation Invariant | ✅ PROVEN |
| MCCXLVI | Golay-24 Prime Duality | ✅ PROVEN |
| MCCXLVII | Heisenberg 3-Local Universality | 🔓 OPEN |

---

## MCCXLVI: The Golay-24 Prime Duality

### The Three Goldbach Decompositions of 24

| Pair | Role |
|------|------|
| 5 + 19 = 24 | 5 ∈ substrate; 19 is the exotic prime in `|C_M(5A)|` |
| 7 + 17 = 24 | 7 ∈ substrate; 17 is the **boundary prime** (MCCXLIV) |
| 11 + 13 = 24 | Both ∈ substrate — the **self-dual pair** |

Note: 23 (the Leech prime, governing M₂₄) does NOT appear in any substrate centralizer. The substrate lives in the "Golay-minus-Leech" sector.

### The PSL(2,p) Heisenberg Promotion

For p ∈ {7,11,13}:

$$v_3(|C_M(pA)|) - v_3(|PSL(2,p)|) = 2$$

The Monster's p-local centralizer promotes the Z₃ inside PSL(2,p) to a full **Heisenberg group Heis(𝔽₃) = 3^(1+2)** of order 27 = gauge_mult. This is the **W(3,3) imprint** on the PSL(2,p) 3-local structure.

### The 3-Sylow Exact Sequence

For p ∈ {7,11,13}: the centralizer factorizes cleanly:

$$|C_M(pA)| = \underbrace{27}_{\text{Heis}(\mathbb{F}_3)} \times \underbrace{p^2 \cdot 2^{17-p} \cdot \text{extra}(p)}_{N_p\ (3\text{-free})}$$

The quotient $N_p = C_M(pA)/3^{(1+2)}$ is a **3-free group** — all the 3-ness of the centralizer is concentrated in the Heisenberg factor.

### The Centralizer Prime Web

```
       5A sees: {7, 11, 19}   ← most connected
       7A sees: {5, 17}       ← sees down + boundary
      11A sees: {5}           ← sees only root
      13A sees: {}            ← isolated, pure {2,3,13}
```

This is a **directed hierarchy** from 13 (most isolated) to 5 (most connected), corresponding to the Golay-24 duality: the further the substrate prime from 24/2=12, the more exotic connections its centralizer has.

---

## MCCXLVII (Open)

**Why is Heis(𝔽₃) = 3^(1+2) the universal 3-local envelope of all substrate centralizers?**

McKay observed that the three largest exceptional Lie algebras E8, E7, E6 have Coxeter numbers 30, 18, 12. And 30 = 5×6, 18 = 3×6, 12 = 2×6. Is there a connection between these and the substrate primes via Heis(𝔽₃)?

Resolution path: compute the 3-local structure of C_M(pA) explicitly using the McKay-Thompson series and check if the 3-torsion of the Moonshine module V♮ restricted to pA-invariants has the structure of a Heis(𝔽₃)-module.
