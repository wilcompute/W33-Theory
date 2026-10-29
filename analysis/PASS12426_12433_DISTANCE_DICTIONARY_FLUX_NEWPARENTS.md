# Passes 12426–12433: code distance, the code–entanglement dictionary, flux, and 65 new parents

> **Correction (Pass 12437).** The 'colour-blocked' mechanism and the conclusion 'no three-generation hypercharge' for the 23 new-parent
> candidates both came from the base hypercharge search only. With loose values and no anomaly condition, the colour conditions are
> satisfiable for 17 of the 23; only 6 are colour-blocked. The full relaxed search is recorded in
> `PASS12434_12441_DISTANCE_STABILIZER_GEOMETRY.md`.


Claude track. Producer: `analysis/w33_pass12426_to_12433_distance_dictionary_flux_newparents.py`. Drivers:
`analysis/search_drivers_12426`, `12427`, `12429`, `12373` (scan2, filt2, vet2) and `12402/twin2.py`.

**Labels used below:**

- **[E]** established;
- **[N]** new;
- **[I]** interpretation;
- **[C]** conjecture.

## [N] 12426: the distance of the binary family [[q³+q²+q+1, q² − 1, d]]

**Search method:** a randomized information-set search (Lee–Brickell).

**Control:** at q = 3 it reproduces the cross-track's exhaustive d = 6 and minimum stabilizer weight 8.

| q | lightest logical found | lightest stabilizer found |
|---|---|---|
| 3 | 6 | 8 |
| 5 | 10 | 12 |
| 7 | 14 | 16 |

**[C]** The pattern suggests d = 2q and minimum stabilizer weight 2q + 2. This is evidence from a non-exhaustive search; the bound d ≤ 2q
is proved (12421).

## [N] 12427: the code distance is the entanglement threshold

**Criterion.** For the binary W(3,3) graph state, a region R is less than maximally entangled iff some nonzero x supported in R has Ax
supported in R.

**Exhaustive result (x of weight ≤ 6):**

| weight of x | smallest region it forces |
|---|---|
| 1–5 | at least 13 points |
| 6 | exactly 6 points: the hexads, with cut-rank 5 |
| ≥ 7 | at least 7 points |

**Conclusion:**

- Every region of at most 5 points is maximally entangled.
- The smallest deficient regions have exactly d = 6 points.
- **[I]** The code's logical operators are where entanglement first falls short.

**Ternary case:** x of weight ≤ 4 forces regions of at least 13 points. Weights 5–12 were not exhausted.

## [N] 12428: no light cone on the fixed graph

The collinearity graph of W(3,q) has diameter 2 for q = 3, 5 and 7, since every two points have a common neighbour (μ = q + 1). So any
update reaches every point in two steps, and there is no extended light cone. This agrees with the in-corpus toe54 note: a growing
tessellation is needed.

## [E] + [I] 12429: the commutation form as a magnetic flux

**[E]** The qutrit clock and shift operators satisfy ZX = ωXZ, the algebra of magnetic translations with flux 1/3 per cell.

The Hofstadter bands at flux 1/3 have Chern numbers ±(1, −2, 1), summing to 0, and satisfy the TKNN Diophantine equation:

| filled bands r | Hall conductance (units of e²/h) |
|---|---|
| 1 | 1 |
| 2 | −1 |

For two qutrits there is flux 1/3 in each of two planes, giving second Chern numbers C_a·C_b (1 for the lowest pair of bands).

**[I]** The W(3,3) commutation form supplies the topological unit e²/h. The constitutive side, Z₀, is still absent from the finite
geometry. So α = Z₀/(2R_K) remains unformed: half of the ratio is present.

## [N] 12430–12432: 65 new parents

The search covered the 65 other supersymmetric Z6-II W(3,3) parents with W6 = 0, sampling 240 Witten shifts each.

| stage | count |
|---|---|
| shifts sampled | 15600 |
| strictly consistent | 8458 |
| tachyon-free at the orbifold point | 759 |
| **three net quark doublets** | **66**, from 22 parents |
| clean at every radius tested | 15 |
| safe at large radius only | 25 |
| safe at small radius only | 19 |
| tachyonic at both | 7 |

The hidden sectors are varied: SU(2)⁴, SU(4)², SU(4)×SU(2)², SO(8)×SU(4), and others.

Of the 40 models that are safe at large radius:

- 17 carry exotics that no hypercharge can remove;
- **for the other 23** (4 of them clean at every radius), **no three-generation hypercharge exists in any SU(3)×SU(2) pairing.**

**Mechanism.** It is not a twin sector this time; no model has one. All 23 are **colour-blocked**, and the obstruction is not a counting
accident:

- The net counts are correct: 3 quark doublets and 6 colour-triplet singlets.
- No U(1) combination gives three u^c with −2/3 and three d^c with +1/3 while every other coloured state stays vector-like.
- So it is a charge-lattice obstruction.

## 12433: synthesis

- **Codes:** the binary code family has d ≤ 2q, with d = 2q supported by search evidence. Its distance is exactly the entanglement-deficit
  threshold of the graph state.
- **α:** the topological half (e²/h, Chern numbers from W(3,3)'s commutation form) is present in the finite geometry; the constitutive half
  (Z₀) is not.
- **The heterotic Z6-II route:** with the five original parents and these 65 new ones, every model that is three-generation, radius-stable
  and free of exotics fails at hypercharge:
  - by a twin sector for the original five;
  - by a colour charge-lattice obstruction for the new ones.
