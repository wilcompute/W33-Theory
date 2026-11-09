# Pass 12642: the optimal three-copy chirality witness is 16/27, attained by stabiliser states; three qubits certified at degree 6 (numerically); W(E6) dependency triage

Claude track. Builds on Passes 12636, 12639, 12640 and 12641 (with its addenda). **Not a theory of everything.** These are finite statements about two-qutrit and three-qubit Pauli measurements.

## 1. The chirality witness (`w33_chirality_third_moment.py`, `data/w33_chirality_third_moment.json`)

Take a chiral pair (L, R) of pentads over one codeword. They cover the same 20 points and are exchanged by the Kramers θ of Pass 12641. For a pure state v, define

Δ(v) = Σ_{e∈L} |⟨e|v⟩|⁶ − Σ_{e∈R} |⟨e|v⟩|⁶ = ⟨v^{⊗3}| T |v^{⊗3}⟩.

| quantity | value |
|---|---|
| second-order difference ‖Σ_L P_e^{⊗2} − Σ_R P_e^{⊗2}‖ | 5×10⁻¹⁵ (zero, since M_L = M_R) |
| spectrum of T on Sym³(C⁹) | ±√(2/3) ≈ ±0.8165 (eigenvalue bound only) |
| max_v Δ over pure states (40 BFGS starts) | 0.592592592… |
| **closed form** | **16/27, exact** |

**Why 16/27.** Let e be any stabiliser state of a left line L.
- On the left: e scores 1 in its own basis and 1/9 on each of the 36 states of the four other bases, which are mutually unbiased with it. So Σ_L p³ = 1 + 36/729.
- On the right: every left line meets the right pentad in the pattern {0, 1, 1, 1, 1}, checked for all 5. A right line meeting L in one point gives p ∈ {1/3, 1/3, 1/3, 0}, so Σ p³ = 1/9 for that line. The disjoint right line gives 9 × 1/729. So Σ_R p³ = 4/9 + 1/81.
- Hence Δ(e) = 1 + 4/81 − 37/81 = **16/27**.

All 45 left states give exactly +16/27 and all 45 right states give −16/27. The numerical optimum over all pure states coincides with this value, so **stabiliser states are optimal chirality witnesses**. The eigenvalue bound √(2/3) is not attained by any product vector v^{⊗3}.

**Mechanism (item 3: why order three).**
- At order two, the twirl Σ_{e∈B_L} P_e^{⊗2} = (1/9) Σ_{u∈L} W_u ⊗ W_u† depends only on the covered points, which L and R share.
- At order three, the sum runs over collinear pairs (u, v ∈ the same line). **L and R each have 30 collinear point pairs, and they share none.** Same points, completely different collinear pairs: that is the whole of the chirality at this level.

**Protocol, stated honestly.**
- Δ is cubic in ρ, i.e. a linear observable on ρ^{⊗3}.
- It is also obtainable from single-copy statistics: measure the 10 bases (5 left, 5 right) and form unbiased estimators of Σ p_e³.
- Hence "three-copy" names the order of the moment, not a requirement for collective measurement.
- With a stabiliser input the signal is 16/27 ≈ 0.59 out of a maximum per-pentad Σ p³ of about 1.05, so it is large, not a small effect.

## 2. Three qubits: degree-6 real SOS (`w33_threequbit_degree6.py`, `w33_threequbit_size5_orbits.py`)

**Prior state.** Pass 12636 found the 24,192 size-5 maximal partial spreads of W(5,2). Pass 12639 found min F = 1/8 numerically, and showed that the Hermitian relaxations of degree 4 and 6 fail. Pass 12640 found that the real degree-4 SOS gives 0.

**This pass.**
- **One type.** All 24,192 size-5 sets share one intersection invariant. Since 1,451,520 / 24,192 = 60, this is consistent with a single Sp(6,2) orbit with stabiliser of order 60. The A5 identification is expected but not checked here.
- **The SOS that works.** F(v)|v|² − δ|v|⁶ = ⟨v^{⊗3}|H₃|v^{⊗3}⟩ + q(v)†G q(v), where q_{(ij),k} = v_i v_j v̄_k is the charge-1 block (288 monomials) and H₃ (120) and G (288) are Hermitian PSD. The objective maximises δ (SCS).

| set | δ* (degree 6) | numeric min F | identity residual | min eig G, H |
|---|---|---|---|---|
| two qubits, size 3 (control) | 0.2500000 | 0.25 | 7×10⁻¹² | −2×10⁻⁹, −9×10⁻¹⁰ |
| three qubits, size 5 | 0.1249999831 | 0.1250000002 | 1.1×10⁻¹¹ | −1.7×10⁻⁷, −1.7×10⁻⁸ (solver tolerance) |

**Reading.** The degree-6 real certificate (with the charge-1 block) reaches the numerical minimum **1/8 = 1/d**, which makes it **tight**. Three-qubit size-5 sets are therefore strongly unextendible with F ≥ |v|⁴/8, **certified numerically, not exactly**. The identity was checked independently by evaluating both sides at 50 random points from the polynomial definitions. An exact rational or Z[ω]-rounded certificate is open; the PSD matrices sit at the boundary, as tight certificates must, so rounding needs facial reduction first.

**The ladder now reads**:
- d = 4: degree 4 suffices;
- d = 9: degree 4, exact, via the S6 / Jucys–Murphy argument;
- d = 8: degree 6 is needed and suffices numerically.

In every rung the bound is **exactly 1/d**. That is a pattern on three cases, not a theorem.

## 3. W(E6) dependency triage (item 4)

1,260 `analysis/*.py|*.md` files mention W(E6), PGSp(4,3) or 51,840. The 340 of Pass 12641 came from a narrower pattern. Of the 1,260, 35 also contain a general-q or general-p phrase. Each was read in context:

| verdict | files |
|---|---|
| **over-read (false as stated)** | `w33_MCCCLXXI_dual_substrate_pauli.py`: "W(E_{q+3}) for general q". This is false: q = 2 gives \|W(E5)\| = \|W(D5)\| = 1920 against \|Sp(4,2)\| = 720, and q = 5 gives \|W(E8)\| = 696,729,600 against \|PGSp(4,5)\| = 9,360,000. It is an early speculative file; flagged, not edited. |
| general-q claim proved without W(E6), so fine | `w33_pass433_abelian_pds_tower_theorem.py` (it explicitly replaces the W(E6) Sylow route), `BT2088_*`/`PASS2088_*` (orbit sizes for odd q), `BT2200_*`, `w33_pass279_sqrt21_search.py` (SRG discriminant), `W33_HONEST_SYNTHESIS.md` (rank from SRG multiplicities), `2026-10-29_*` (gcd from SRG eigenvalues), `w33_pass12063_clocks_beyond_q3.py`, `w33_pass2789_2792_*` (states "at every q tested"), `w33_pass1877_1881_*`, `PASS12637_*` (Satake boundary) |
| scoped correctly by its author | `w33_pass1861_1866_*`. The "every q" part, the spread trap, was computed at q = 2, 3, 5. The no-phase result is explicitly attributed to W(E6) being a reflection group (see the control below). |
| grep false positives ("q = 3" literal, "for all p" meaning all points, "arbitrary channel") | `SOLVE.py`, `SOLVE_IT.py`, `THEORY_OF_EVERYTHING.py`, `bt1299_*`, `bt1350_*`, `toe_20261104_*`, `w33_BREAKTHROUGH_*` (2), `w33_levi_five_frontiers.py`, `w33_pass11252_*`, `w33_pass11457_*`, `w33_pass11498_*`, `w33_pass4232_*`, `PASS11533_*`, `BT1330_*`, `BT2470_*`, `PASS358_359_*`, `2026-07-29_*`, `2026-10-09_*`, `2026-10-15_*`, `2026-10-31_*`, `2026-11-04_*` |

**Control for the no-phase result.** Do PGSp(4,q) for q ≠ 3 also have only real-type irreducibles? GAP (`w33_pgsp_frobenius_schur.g`, using the group's own invariant form plus a diagonal similitude):

| group | order | Frobenius–Schur indicators (+1 / 0 / −1) |
|---|---|---|
| PGSp(4,3) = W(E6) | 51,840 | 25 / 0 / 0 |
| PSp(4,3) | 25,920 | 10 / **10** / 0 |
| PGSp(4,5) | 9,360,000 | **47 / 0 / 0** |
| PSp(4,5) | 4,680,000 | 34 / 0 / 0 |

**Correction of attribution for Pass 1866** (the result stands; the reason given for it changes).
- PGSp(4,5) is not a Weyl group, yet every one of its irreducibles is of real type.
- The general reason: PGSp(4,q) ≅ SO(5,q) for odd q, Gow (1985) showed the finite orthogonal groups O(n,q), q odd, are totally orthogonal, and O(5,q) = SO(5,q) × {±1}.
- So **the absence of an invariant phase holds for every odd q**. "W(E6) is a reflection group" is the q = 3 coincidence W(E6) ≅ SO(5,3), not the mechanism.
- The phase that PSp(4,3) has (10 complex irreducibles, the Weil chirality of Passes 353 and 355) is killed by the similitude, the diagonal outer automorphism.
- At q ≡ 1 (mod 4), PSp is already totally orthogonal, consistent with Pass 353's table.
- Prior art in the repo: Passes 353 and 355 cite Gow and Vinroot for Sp and PSp. The orthogonal-group half (Gow's O(n,q) theorem applied to SO(5,q) ≅ PGSp(4,q)) is not used there. The q = 3, 5 tables above are this pass's computation; all q is Gow's theorem, cited, not re-proved.

**Net.** One genuine over-read, in an early speculative file. One *reverse* case: a result attributed to W(E6) (no invariant phase, Pass 1866) is in fact **more** general than its stated reason. Every general-q theorem in the flagged set is proved from Sp(4,q), SRG or orbit data, not from W(E6). The p = 3-only results (strong unextendibility at 1/9 via the doily S6, the no-phase theorem) state their scope correctly. The triage covers the 35 files with general-q wording, not all 1,260.

## Open

- An exact three-qubit certificate (rounding, or an A5-reduced derivation).
- Whether min F = 1/d holds for every size-minimal maximal set in higher rungs: d = 25 failed to certify (Pass 12641), and its minimum has not been computed.
- The other track's exact replay of Pass 12641.
