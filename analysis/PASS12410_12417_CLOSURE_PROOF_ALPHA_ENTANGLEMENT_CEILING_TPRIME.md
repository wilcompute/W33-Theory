# Passes 12410–12417: the closure theorem proved and corrected, α as an impedance ratio, an entanglement ceiling, and T′ on W(3,3)

Claude track. Producer: `analysis/w33_pass12410_to_12417_closure_proof_alpha_ceiling_tprime.py`. Drivers:
`analysis/search_drivers_12410`, `12412`, `12413`.

**Labels used below:**

- **[E]** established (cited);
- **[N]** new here;
- **[I]** interpretation.

## [N] 12410: the finite closure theorem, proved and corrected

**Setting.** F = F_q with q odd. L = Λ²F⁴ is a 6-dimensional space carrying the wedge pairing P, a hyperbolic quadratic space. κ ∈ End(L)
is P-symmetric with κ² = −1.

**Theorem.**

1. *(q ≡ 3 mod 4, so −1 is not a square.)* κ = ±(the Hodge star of an elliptic metric g). The metric is unique up to scalars, and every
   such κ arises. Closure alone produces a Lorentzian-type light cone, exactly as over ℝ.
2. *(q ≡ 1 mod 4, so −1 is a square.)* κ is ±(the Hodge star of a hyperbolic metric) **iff** tr κ = 0. The solutions with tr κ ≠ 0 are not
   metric; the simplest is κ = i·I.

**Proof.**

1. **The eigen-decomposition.** Put K = F(i). Over K, L ⊗ K = U ⊕ U′, where U = ker(κ − i) and U′ = ker(κ + i).
   - P-symmetry gives P(u, u′)·(i − (−i)) = 0, so U ⟂ U′.
   - P is nondegenerate, so both U and U′ are nondegenerate.
   - Conversely, every P-orthogonal nondegenerate decomposition defines such a κ.
2. **When i ∉ F.** Frobenius σ commutes with κ and sends i to −i, so U′ = σ(U). Hence dim U = 3.
   - U ⟂ σU says exactly that U is totally isotropic for the Hermitian form h(x, y) = P(x, σy): a generator of H(5, q²) on which P is
     nondegenerate.
   - By Witt's theorem for the pair (P, h), these generators form one orbit of O⁺(6, q). Its stabilizer is the F-points of O(U) ≅ O(3, q²).
   - So the number of solutions is |GO⁺(6, q)| / |GO(3, q²)| = q⁴(q² − 1)(q³ − 1).
3. **When i ∈ F.** U is a rational nondegenerate subspace of any dimension a = 0, …, 6, and tr κ = i(2a − 6). This vanishes iff a = 3,
   since p ≥ 5 here.
4. **Matching the Hodge stars.**
   - The Hodge star of a metric g satisfies (P⁻¹G₂(g))² = det(g)·I.
   - A scalar s with s²·det(g) = −1 exists iff −det(g) is a square. For q ≡ 3 (mod 4) that means g is elliptic; for q ≡ 1 (mod 4), g is
     hyperbolic.
   - The self-dual space of g is 3-dimensional, and Urbantke's formula inverts the map (U ↦ conformal class of g).
   - Counting metric Hodge stars (2|GL(4, q)| / ((q − 1)|GO^ε(4, q)|)) gives exactly the number of a = 3 solutions.
   - This is the content of the isomorphisms O⁺(6, q) ~ SL(4, q) and O⁻(4, q) ~ PSL(2, q²) ~ O(3, q²).

**Checks:**

- q = 3: exhaustive, 16848 solutions, all metric (12369).
- Urbantke sampling: q = 7 and 11, all elliptic; q = 5 and 13, a = 3 only, all hyperbolic (12404).
- Counts agree for q = 3 … 13 (12405).
- Non-metric solutions at q = 5: κ = 2I and a 1 + 5 split, both P-symmetric with κ² = −1 and tr κ ≠ 0.
- Exact totals:

  | q | all closure solutions | Hodge stars (a = 3) | share |
  |---|---|---|---|
  | 5 | 2,834,952 | 2,015,000 | 71% |
  | 13 | 12,304,306,952 | 10,662,392,520 | 87% |

**Correction.** Passes 12402–12409 stated "closure always gives a metric" for every odd q. That holds only for q ≡ 3 (mod 4); both files
now carry a note.

**[I] Reading.** "Closure alone forces a light cone" is a property of fields like ℝ, in which −1 has no square root. Where i is already
present, closure must be supplemented by tr κ = 0, the absence of an axion-like part.

## [E] + [I] 12411: α is a constitutive impedance over a topological impedance

- **[E]** R_K = h/e² is topological: the Hall conductance is (e²/h) × (a Chern number) (TKNN 1982).
- **[E]** Z₀ = √(μ₀/ε₀) is the scalar of the vacuum constitutive Hodge star.
- **[E]** α = Z₀/(2R_K) (CODATA; checked to 6×10⁻¹³ in 12406).
- **[I]** In this repo's split, α is the ratio of a **transfer** impedance to a **counting** impedance. A theory that predicts α must therefore
  compute the vacuum Hodge star in units fixed by a topological invariant.
  - Neither the finite closure theorem nor the Kähler count supplies such a unit, because on F_q both scales are ±1.
  - This is the precise gap.

## [N] 12412: an entanglement ceiling for the qutrit W(3,3) graph state

The qutrit graph state on the 40 points of W(3,3) has entanglement S(A) = rank₃ Γ[A, Ā] across a cut.

**Theorem.** S(A) ≤ 11 for every region A.

**Proof.** W(3,3) is strongly regular with parameters (40, 12, 2, 4), so A² = 8I − 2A + 4J. Mod 3 this gives (A + I)² ≡ J. Every
off-diagonal block of A is a block of N = A + I, so rank₃ Γ[A, Ā] ≤ rank₃ N = 11, which is computed. Also N ≡ M·Mᵀ (mod 3), where M is the
point–line incidence matrix, since MMᵀ = 4I + A.

**Checks:**

- Hill-climbing reaches 11 for |A| = 15 and 20. Random 20-point regions give 11 every time.
- Random 12-regular graphs reach 20 (control).
- Over F₂ the cap is the 2-rank of A, which is 16.

**Small regions:**

| region | S |
|---|---|
| a line (4 points) | 4 |
| a point-perp (13 points) | 6 |
| the 12 neighbours of a point | 7 |

**[I] Reading.** The 40-qutrit network can carry at most 11 trits of entanglement between any two parts, whatever their sizes: a bounded
"screen" capacity, not a volume law.

**Prior art.** The corpus's graph-phase area law (2026-10-23) concerns chains of 40-state sites, a different object. The 3-rank 11 of
M·Mᵀ for W(3,3) was not found in a quick search; publication not checked.

## [N] 12413: the binary tetrahedral group on W(3,3), and where T′ doublets live

SL(2,3), the derived subgroup of the stabilizer of the quantum i, acts on three sets:

| object | orbits | decomposition |
|---|---|---|
| 40 points | 4, 4, 4, 4, 12, 12 | 6·1 ⊕ 2·1′ ⊕ 2·1″ ⊕ 10·3 |
| 40 contexts | 4, 6, 6, 12, 12 | 5·1 ⊕ 4·1′ ⊕ 4·1″ ⊕ 9·3 |
| 80 nonzero vectors | 8, 8, 8, 8, 24, 24 | 6·1 ⊕ 2·1′ ⊕ 2·1″ ⊕ 10·3 ⊕ 4·2 ⊕ 8·2′ ⊕ 8·2″ |

The characters come from element orders, using real parts, and are checked against the regular representation.

On projective objects (points, contexts), −1 acts trivially, so only A₄ irreducibles appear. The T′ doublets 2, 2′ and 2″ appear only on
vectors.

**[E]** A₄ is the tetrahedral lepton-flavour group (Ma–Rajasekaran; Altarelli–Feruglio). T′ adds doublets used for quarks.

**[I]** The geometry offers A₄ triplets and singlets on projective objects, and T′ doublets only at the "spinor" (vector) level. This
mirrors the A₄/T′ lepton/quark split. Nothing here derives three generations.

## 12414: the relaxed hypercharge search

The final count is recorded in the certificate. When it was written, 58 of 59 were done with 0 solutions.

## 12417: synthesis

- The light-cone theorem is now a proved classification, with the q ≡ 1 (mod 4) correction.
- α is pinned down as a constitutive-over-topological impedance ratio.
- The W(3,3) qutrit network has a hard 11-trit entanglement ceiling.
- The quantum-i symmetry contains the tetrahedral flavour groups, A₄ on points and T′ on vectors.
