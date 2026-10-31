# Passes 12506–12513: braiding five metaplectic anyons acts transitively on the minimal codewords; the q = 9 "240" is not E₈

Claude track. Producer: `analysis/w33_pass12506_to_12513_quantum_bridges.py`. Drivers in `analysis/search_drivers_12466`:
`braid_codewords.py` and `e8_icosian_probe.py`. Context:

- the other track's TL₆ / SU(2)₄ braid representation (ad8846e59);
- its A₅ × C₂ torsion work on the q = 9 set (937445da5, 6343cdf59);
- Pass 173's route code;
- 12501's q = 9 stabiliser.

## 12507: braiding acts on the minimal even line sets of W(3,3)

The other track (ad8846e59) realised the Temperley–Lieb algebra TL₆ at δ = √3, the SU(2)₄ / metaplectic point, on two qutrits. Its
braid generators are the order-3 Clifford "tick" gates, i.e. symplectic **transvections** T_p(x) = x + ω(x,p)p along an induced path
p₀ … p₄ in the noncommutation graph.

So the braid group B_k acts on W(3,3) and on the **216 minimal even line sets**: Pass 173's route codewords, one PSp(4,3)-orbit.
`braid_codewords.py` checks the braid relations and far commutation, then computes:

| braid group | generators | image on the 40 points | orbits on the 216 codewords |
|---|---|---|---|
| B₃ | 2 | order **24** = SL(2,3), binary tetrahedral | 11 (4 × 12, 7 × 24) |
| B₄ | 3 | order **648** | **108 + 108** |
| B₅ | 4 | order 25,920 = PSp(4,3) | **216 (transitive)** |
| B₆ | 5 | 25,920 | 216 |

**The B₄ image (order 648)** has centre of order 3, derived subgroup of order 216, and a quotient by the centre of order 216 whose
element-order profile is exactly that of the Hessian group **ASL(2,3) = 3²:SL(2,3)** (orders 1, 2, 3, 4, 6 with counts 1, 9, 80, 54,
72). Cui–Wang report that the braid image of the one-qutrit SU(2)₄ metaplectic model is a subgroup of SU(3) of order 648 with centre
Z₃, whose quotient by the centre is the Hessian group of order 216. Order, centre and quotient profile all match. Isomorphism is not
proved here [C].

**Reading [I].** With metaplectic anyons as the braiding substrate:

- **five anyons** suffice for braiding alone to move any minimal codeword of the two-qutrit line code to any other;
- **four anyons** split the 216 into two halves of 108, the same 108 + 108 split as Pass 173's "two chiral orbits of 216" on the
  signed shell, now produced by braiding;
- **three anyons** give the binary tetrahedral group.

## 12506: the 240 covered points of the q = 9 set are not an E₈ root system

The 48-line set at q = 9 covers 240 points, and its stabiliser contains 2I (McKay: 2I ↔ E₈; the E₈ roots are the icosians). Testing
the obvious hypothesis (`e8_icosian_probe.py`):

- **Orbits.** The 480 non-swap stabiliser matrices act as 240 permutations of the 240 points. They are **not regular**: there are two
  orbits of 120, merged by the X ↔ Y swap. 2I acts as A₅ with four free orbits of 60.
- **Geometry.** The collinearity graph on the 240 points is 32-regular with an irregular spectrum. The E₈ root graph, computed from
  the roots in the same script as a control, is 56-regular with spectrum 56, 28, 8, −2, −4.

**Verdict:** a numerical coincidence with an orbit-level echo (two halves of 120 swapped by an involution, as E₈ = 2I ⊔ τ·2I), but no
E₈ root geometry. Recorded as a negative so it is not re-chased. The other track's A₅ × C₂ (order 120) action on this set (937445da5)
is a subgroup of 12501's full order-480 stabiliser.

## 12508: what the literature says about these bridges

- **Two-qutrit geometry.** W(3,3) is the commutation geometry of two qutrits, with automorphisms tied to W(E₆) (Planat–Saniga and
  coauthors, 2007). State-independent contextuality from two-qubit states does **not** generalise to odd-prime qudits, which agrees
  with 12499.
- **Metaplectic anyons.** SU(2)₄ braiding is not universal: its image is a finite Clifford group, and universality needs an extra
  non-Clifford gate or a measurement (Cui–Wang 2015; Cui–Hong–Wang). The other track's TL₆ / SU(2)₄ representation sits inside this
  known picture.
- **Golden gates.** Parzanchevski–Sarnak golden gates use finite subgroups of PU(2) (octahedral = single-qubit Clifford mod phase;
  icosahedral), with reductions related to Ramanujan Cayley graphs of PSL(2,p) (Lubotzky–Phillips–Sarnak). The exceptional subgroups
  of PGL(2,q) that stabilise our minimal even sets (S₄ for the cube at q = 7, A₅ at q = 9 and q = 11) are abstractly the same groups.
  **This is an analogy [I], not a computed map.** A concrete bridge would have to match a specific reduction of the golden-gate lattice
  with the stabiliser in PSp(4,q). It has not been built.

## 12509: is 48 the minimum at q = 9? (status)

`q9_le46.py` (12502) asks whether an even line set of size ≤ 46 exists. Its result is recorded in `q9_le46.json` when the run
finishes. Only INFEASIBLE would be a proof.

## Sources

- M. Planat, A.-C. Baboin, M. Saniga, *Multi-line geometry of qubit-qutrit and higher-order Pauli operators* (2007), and *On the Pauli
  graphs of N-qudits*, arXiv:quant-ph/0701211.
- S. X. Cui, Z. Wang, *Universal quantum computation with metaplectic anyons*, J. Math. Phys. 56 (2015), arXiv:1405.7778; S. X. Cui,
  S.-M. Hong, Z. Wang, *Universal quantum computation with weakly integral anyons*, arXiv:1504.03383.
- O. Parzanchevski, P. Sarnak, *Super-Golden-Gates for PU(2)*, Adv. Math. (2018), arXiv:1704.02106.
- *Two-letter words and a fundamental homomorphism ruling geometric contextuality*, arXiv:1605.07118.
