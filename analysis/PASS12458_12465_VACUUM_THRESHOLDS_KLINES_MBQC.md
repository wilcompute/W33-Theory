# Passes 12458–12465: SM_2541 has a vacuum but cannot unify; the k-line lemma; W graph states and MBQC

Claude track. Producer: `analysis/w33_pass12458_to_12465_vacuum_thresholds_klines_mbqc.py`. Drivers: `analysis/search_drivers_12458` to
`12462`.

## 12458: the SM_2541 vacuum — the FI term is cancelled by singlets, and every fractional state lifts there

**Setup.** Take the 42 full singlets of SM_2541_c22: SM singlets that are also singlets of every hidden non-abelian factor, with Y = 0. The
anomalous direction is T_anom, the sum of all weights of all massless Weyl fermions. With v_i = |⟨s_i⟩|², D-flatness with the FI term reads

  Σ v_i q(s_i) = −c q(T_anom),  v_i ≥ 0,  c > 0.

**Results for c22** [E]:

- q(T_anom) lies in the span of the singlet charges. This is exact over the rationals: the rank is 6 with and without it.
- Every singlet lies in some homogeneous D-flat direction, so the cone of charges equals their span.
- So **all 42 singlets can be switched on together** in a D-flat direction that cancels the FI term, for either sign of the FI term.
- In that direction every fractional state lifts: 90 by Dirac pairs and 2 by Majorana self-masses. With c22's lowest hypercharge,
  k_Y = 11/3, all 52 fractional states lift, again with 2 self-masses.
- **Family-wide:** the same holds for all 52 SM_2541 models.

**Correction made during the pass.** The first LP run returned an *empty* support for both FI signs. The cause was the box bound v ≤ 10
together with the normalisation c = 1: a charge vector of norm about 108 was out of reach. The exact span check exposed it. A negative
control (a target outside the span) correctly gives an empty support.

**Not computed:**

- the non-SUSY one-loop potential, its minimisation, and the VEV sizes;
- non-abelian D-flatness (not needed here, since only full singlets get VEVs).

There are no F-terms in a non-SUSY model.

## 12459: thresholds cannot unify SM_2541 — the lineage is closed at unification

**Method.** I used the 12359 machinery: the large-volume Dixon–Kaplunovsky–Louis (DKL) form, with 6D coefficients computed from the massless
spectra of *both* fixed tori. For c22 these are fresh strict-engine runs of the θ² and θ³ sub-orbifolds (940 and 624 fields), with the
Wilson lines on each fixed torus switched off.

**c22, all six anomaly-free hypercharges** (k_Y = 17/3, 11/3, 53/9, 35/9, 17/3, 41/9):

- The exact 3×3 solve always needs either a negative torus volume or a negative 1/α_s.
- The best physical fit (all volumes and 1/α_s non-negative) leaves a residual of **at least 33.9 in 1/α**.
- Control: the same fitter reproduces 12359's SM_2913 residual of 9.72 exactly. SM_2913 was already rejected at that residual.

**All 52 models:** no physical solution, and the best residual is at least **34.3**.

**Verdict.** SM_2541 now passes three generations, an anomaly-free Y, large-radius safety, the absence of exotics, the fractional charges
and the vacuum, and **fails at gauge coupling unification**. k_Y ≥ 11/3 is too large for any large-volume threshold of this geometry.
This assumes the DKL form holds for a non-SUSY orbifold, as argued in 12359. The linear term is power-law Kaluza–Klein running and is
robust; the constant and logarithmic terms are not. This closes the SM_2541 lineage.

## 12460: the k-line lemma

**Lemma (proved).** Let S be the mod-2 sum of k distinct lines of a generalized quadrangle of order (q,q). Then

  |S| ≥ k(q + 2 − k).

*Proof.* Each line of the sum meets each of the other k − 1 lines in at most one point. So at least q + 2 − k of its points lie on no other
line, and those points are in S. These sets are disjoint for different lines.

**Consequences.**

- For 2 ≤ k ≤ q the bound is at least 2q.
- For k = q + 1, a no-triangle step gives |S| ≥ min(2q + 2, q² + 1). If some line met all q others at distinct points, those q lines
  would have to be pairwise skew (two of them meeting would form a triangle with it), and then |S| ≥ q² + 1. Otherwise every line has at
  most q − 1 shared points, and |S| ≥ 2(q + 1).
- So **every kernel word of W(3,q) that is a sum of at most q + 1 lines has weight at least 2q.**

**Relation to the other track.** Their exhaustive q = 7 computation over three-line unions (7d27e910c: 10,586,800 triples) is the case
k ≤ 3. The lemma extends it to every odd q and every k ≤ q + 1, by hand.

**Exhaustive check at q = 3.**

| k | minimum weight of a k-line sum |
|---|---|
| 2 | 6 |
| 3 | 8 |
| 4 | 8 |
| 5 | 8 (beyond the proved range) |
| 6 | 8 (beyond the proved range) |

There are 0 violations. A correction to my own framing: ker₂A has dimension 24 at q = 3. The 8 is the number of logical qubits.

**Open.** Kernel words of weight below 2q whose every representation needs at least q + 2 lines. Combined with 12450's d ≥ q + 3, the
q = 7 question now reduces to such words.

## 12461: smallest deficient region at q = 5 — still open

**A counting lemma (proved).** Let x be supported in a region R, with Ax also supported in R. Take any ℓ in supp x, with t neighbours in
supp x. Then

  |R| ≥ (q + 1)(q + 1 − |x|) + |x| + t.

So |x| ≤ q forces |R| ≥ 2q + 1.

**Search.** I added this lemma to CP-SAT as cuts. The q = 3 control stays exact. At q = 5, the question "is there a region of size ≤ 9?"
is UNKNOWN in both symmetry cases after 1800 s each. **Status: open.** Deficient region = distance stays proved only at q = 3.

## 12462: Pauli geometries as MBQC resources

- **Embedding lemma (proved).**
  - *Statement.* Every graph on N vertices is an *induced* subgraph of the collinearity graph of W(2N − 1, q), for every q.
  - *Construction.* Set u_i = (e_i, g_i) in F_q^N ⊕ F_q^N. Choose g_i so that ω(u_i, u_j) is zero exactly on the edges.
  - *Checked* on grids, a random graph, and W(3,3) itself, for q = 2, 3, 5.
  - *Consequence.* A Z measurement deletes a vertex of a qudit graph state, up to local corrections. So Pauli measurements on W graph states
    reach every graph state, cluster states included.
- **But the overhead is super-polynomial for any fixed p.**
  - Every cut-rank is capped by the ceiling 1 + C(2n + p − 2, 2n − 1) (12418), which is polylogarithmic in the number of points v.
  - Schmidt-rank-width simulation then runs in time polynomial in v for p = 2 and quasi-polynomial for p = 3.
  - The qudit form of the simulation theorem is argued, not cited verbatim.
  - So W(2n − 1, p) families are universal only with super-polynomial overhead. **This sharpens 12445**, whose width condition is
    necessary but not sufficient.
- **Induced cluster grids found** (every embedding found was verified to be induced):

| polar space | grids |
|---|---|
| W(3,2), W(3,3) | 2×3 yes; 3×3 no (also 3×4, 4×4 no in W(3,3)) |
| W(5,2) | 3×3 no |
| W(5,3) | 3×3 yes |
| W(3,5) | up to 4×5 yes; 5×5 to 8×8 UNKNOWN (1500 s each) |

The grid size grows with q, not with the rank.

## 12465: synthesis

- **String route.** SM_2541 clears every test so far except unification, which fails by at least 34 in 1/α across all 52 models and
  every hypercharge tested. The non-SUSY Z6-II SO(16)² route is now closed at unification as well as at the earlier filters.
- **Codes.** The k-line lemma gives weight ≥ 2q for all sums of at most q + 1 lines. Together with d ≥ q + 3 (12450), the open part of
  d = 2q is pinned down.
- **Computation.** W graph states reach every graph state by Pauli measurements, but at fixed qudit dimension they are classically
  simulable with polynomial or quasi-polynomial overhead.
