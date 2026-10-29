# Passes 12442–12449: the odd case of d = 2q, SM_2541's neighbourhood, universality, and a cross-repo prior-art tool

> **Oldest prior art (found with `scripts/check_prior_art_all_repos.py`, Pass 12446).** For W(3,3) the identity (A + I)² ≡ J (mod 3)
> has been in the repository since **2026-03-12**: `tests/test_finite_field_methods_computation.py` (from the SRG equation, with rank
> of (A − 2I)² = 1). It recurs in Pass 157 (2026-07-09, eigenlattice prime collision) and in the 2026-10-22 note (general p).


Claude track. Producer: `analysis/w33_pass12442_to_12449_oddcase_sm2541_universality_priorart.py`. Drivers:
`analysis/search_drivers_12442` and `12373` (scan3, filt3, vet3); tool: `scripts/check_prior_art_all_repos.py`.

**Prior art and ownership.**

- q = 5, d = 10 is cdde9b06b's (other track).
- q = 7, 10 ≤ d ≤ 14 is 055804fc2's (other track).
- The even-line resolution ker₂ A = {Ny : Σy even} is the other track's 2026-10-29 note.
- The LU(3,q) / dual-GQ code literature: Kim–Peled–Perepelitsa–Pless–Friedland; Kim–Mellinger–Storme 2007; Pepe–Storme–Van de Voorde
  2010. It works mainly in the geometry's own characteristic. Binary codes with q odd are the cross-characteristic case, which the corpus
  notes Petit–Van de Voorde exclude.

## 12442: the odd case of d = 2q — a reduction and a lemma

Let S be the support of a nonzero word of ker₂(A), with s_L = |S ∩ L|.

- **(F1)** At every point, the sum of s_L over the lines through it is even. So the set T of odd-intersection lines covers every point an
  even number of times. That makes T a codeword of the binary line code (the LU(3,q)-type code): **the odd case reduces to small-weight
  words of that code.**
- **(F2)** For a line L and a point x ∈ L, let m_x(L) be the number of points of S off L that are collinear with x. Then
  m_x(L) ≡ s_L − [x ∈ S] (mod 2).
- **(F3)** |S| = s_L + Σ_{x∈L} m_x(L).

**Lemma (proved).** Let L be a line with s_L = a odd, x₀ ∈ L ∖ S, and M an odd line through x₀ (one exists by F1), with c = s_M. Then

  |S| ≥ q + max(a, c) + #(points of S on the other q − 1 lines through x₀).

The proof uses two facts: a point off M sees exactly one point of M, and a generalized quadrangle has no triangles.

- **Consequence:** |S| ≥ 2q whenever some odd line meets S in q points. This is the hexad situation, where the bound is tight.
- **Numerical test:** 0 violations over 30,836 (q = 3) and 251,468 (q = 5) configurations from real kernel words. The bound is tight 480
  and 602 times.
- **Open:** odd lines that all meet S in few points (for example a = c = 1). Closing this needs the count from points outside S, or the
  small-weight structure of the line code.

## 12445: entanglement width and universality

The q-ary ceiling 1 + C(2n + q − 2, 2n − 1) grows like (log_q v)^(q−1)/(q−1)!.

| family | ceiling | compared with log v |
|---|---|---|
| qubits | 2n + 1 = log₂(v + 1) + 1 | logarithmic |
| qutrits, n = 2, 3, 4 | 11, 22, 37 | log₃ v = 3.4, 5.4, 7.4: faster than logarithmic |

**Consequence.**

- Qubit Pauli-geometry graph states are efficiently classically simulable (Van den Nest–Dür–Vidal–Briegel).
- Qutrit and higher ones meet the necessary condition for efficient universality.
- Their actual universality is **not decided**.

## 12446: a cross-repository prior-art checker

`py -3 scripts/check_prior_art_all_repos.py "PATTERN" ...`

- **What it searches:** every repository under C:/Repos (and `--roots` for others, for example WSL), in .md / .py / .tex / .json files.
- **What it reports:** per repository, the matching files with each file's first-commit date, oldest first.
- **Snapshots:** clones such as W33-VM-* and W33-inspect are marked separately.
- **Why it exists:** it answers the user's request to check prior art everywhere, including months back.

## 12443–12444: SM_2541 is a family, and the obstruction is lineage-wide

**The scan.** I sampled 6000 of the parent SM_2541's 28,550 admissible Witten shifts.

| stage | count |
|---|---|
| strictly consistent | 2959 |
| tachyon-free at the orbifold point | 694 |
| three net quark doublets | 62 |
| safe at large radius on both tori | 52 (all tachyonic at small R5) |
| free of hypercharge-independent exotics | all 52 |

**The hypercharge.** All 52 admit a three-generation hypercharge that is anomaly-free: orthogonal to the roots and to the anomalous U(1).
k_Y takes four values:

| k_Y | models |
|---|---|
| 17/3 | 30 |
| 53/9 | 15 |
| 41/9 | 5 |
| 35/9 | 2 |

**The obstruction.** In every one of the 52, the exact all-orders lifting test leaves **exactly one (1,2,0) pair** of fractionally charged
doublets massless. So the obstruction is structural for this lineage, not an accident of one shift.

**A loophole under test (12444b).** The doublet's hypercharge depends on which Y is used. Several distinct hypercharges per model are now
being enumerated for c22 (k_Y = 17/3) and c2872 (k_Y = 35/9), with each one re-tested; the result is in the certificate.

**12444b, result: the loophole is closed.** I enumerated 6 distinct relaxed hypercharges each for c22 and c2872.

- **All 12 are anomaly-free.** Both models share the same menu: k_Y = 17/3, **11/3** (the lowest; 52 fractional fermions), 53/9, 35/9 and
  41/9.
- **Under every one of them, exactly one (1,2,0) pair stays unliftable.** The obstruction does not depend on the hypercharge.

**Verdict for the SM_2541 lineage.** It gives three generations, anomaly-free hypercharges and large-radius stability, but always has one
massless fractionally charged doublet pair, and k_Y ≥ 11/3.

## 12449: synthesis

- **The d = 2q problem** now has three pieces:
  - an even-case theorem (≥ 2q + 2);
  - an odd-case lemma that is tight on the hexads;
  - the reduction of what remains (odd lines meeting S in few points) to small words of the binary LU(3,q)-type line code.
- **Universality.** Qutrit and higher Pauli-geometry graph states pass the necessary width condition; qubit ones are simulable.
- **The prior-art tool works across repositories.** It moved the oldest citation for (A + I)² ≡ J back to 2026-03-12.
- **The string route's best family (SM_2541)** fails on a hypercharge-independent fractional doublet pair.
