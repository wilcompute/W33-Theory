# Passes 12434–12441: the adjacency-code distance, and stabilizer-state geometry

Claude track. Producer: `analysis/w33_pass12434_to_12441_distance_stabilizer_geometry.py`. Drivers:
`analysis/search_drivers_12434`, `12435`, `12437`.

**Prior repo material read first:**

- the binary *line* code theorem: d = q + 1 for all odd q (Holotrade 7c57f8e, parity lemma);
- Passes 356 and 83 (line-code distance, a different code);
- the cross-track [[40,8,6]] adjacency code (923c4eb20).

The adjacency code is a different code from the line code, so its distance was open.

## 12434: the distance of the adjacency code [[q³+q²+q+1, q² − 1, d]]

**Setup.** Let x = 1_S be a nonzero word of ker₂(A), and let s_L = |S ∩ L| for each line L.

**Lemma (all odd q).** Count the neighbours of a point y line by line; they partition into the lines through y, and q + 1 is even. This
gives

  Σ_{L ∋ y} s_L ≡ 0 (mod 2) for every point y.

**Theorem, even case (all odd q).** If every s_L is even, then |S| ≥ 2q + 2.

**Proof.**

- Take p ∈ S and a line L through p. Since s_L is even and nonzero, L contains a second point p′ ∈ S.
- Each of the q other lines through p, and each of the q other lines through p′, then carries a further point of S.
- A generalized quadrangle has no triangles. A point collinear with both p and p′ would have to lie on L. Lines through one point meet only
  there.
- So these 2q points, together with p and p′, are all distinct.

This bound equals the observed minimum stabilizer weight: 8, 12, 16 at q = 3, 5, 7.

**Odd case** (some s_L odd): an exact integer program minimizes the weight of ker₂(A), with one point fixed by transitivity.

| q | exact minimum | status |
|---|---|---|
| 3 | 6 | optimal (control) |
| 5 | 10 | optimal |
| 7 | see certificate | — |

Combined with the weight-2q logicals of 12421, this **proves d = 2q at q = 3 and 5** (computer-assisted). The general odd case is open.

**A tool for the general proof.** For any line L, every point off L sees exactly one point of L. So

  |S| = s_L + Σ_{x ∈ L} m_x, with m_x ≡ s_L − [x ∈ S] (mod 2),

where m_x counts the points of S off L that are collinear with x. In the hexads, s_L = q and a single m_x equals q.

## 12435–12436: stabilizer-state geometry, a metric made of overlaps

**The objects.**

- **Stabilizer frames:** the Lagrangians of F₃^(2n). There are 40 at n = 2, the lines (contexts) of W(3,3), and 1120 at n = 3.
- **States:** each frame holds 3ⁿ stabilizer states.
- **Distance (dual polar graph):** d(L, L′) = n − dim(L ∩ L′).

**[N] Exact check on the state vectors:**

- Every nonzero overlap satisfies |⟨ψ|φ⟩|² = 3^(−d). There are no violations over all pairs at n = 2, nor for one state against all 30240
  at n = 3.
- Sphere sizes are 1, 12, 27 (n = 2) and 1, 39, 351, 729 (n = 3), equal to q^(r(r+1)/2)·[n choose r]_q.
- At the maximal distance n, every overlap equals 3^(−n): antipodal frames are mutually unbiased bases.

**[E]** Stabilizer overlaps and mutually unbiased bases are known.

**[I] Reading:**

- **A metric made of information.** Graph distance equals −log_q(fidelity).
- **Antipodes are dual pairs.** The antipodal frames are exactly the position/momentum pairs: the "state vs update" duality is maximal
  distance in this geometry.
- **A real light cone.** One Clifford step moves a frame by at most 1, so the geometry has a light cone of radius n that grows with the
  number of qudits. The fixed W(3,q) graph had diameter 2 (12428).

## 12437: where the colour obstruction sits

The test applies the hypercharge chirality constraints for quark doublets only, then doublets with up-type triplets, then doublets with
down-type triplets, then all colour states. The results are in the certificate.

## [N] 12438: the identities across the whole Pauli-geometry family W(2n − 1, q)

**Prior repo material:**

- Pass 92 (the W(r,q) landscape);
- BT1707 (three qubits as W(5,2), split Cayley hexagon; four qubits as W(7,2), DW(5,2));
- Pass 11373 (three qutrits, Sp(6,3));
- the doily passes (W(3,2)).

These geometries share one structure. For n qudits of prime dimension q:

- the points are the Pauli operators up to phase;
- two points are collinear iff the operators commute;
- maximal subspaces are stabilizer groups.

**The identity.** The collinearity graph is strongly regular with r − s = 2q^(n−1), so its interesting primes are 2 and p. Mod p,
r ≡ s ≡ −1 and μ ≡ 1, which gives (A + I)² ≡ J for every n. A + I is point–hyperplane incidence in PG(2n − 1, p).

**The ceiling, for every (n, q) checked.** The graph state's cut-rank is capped at

  rank_p(A + I) = 1 + C(2n + p − 2, 2n − 1) (Smith),

which is one plus the number of degree-(p − 1) monomials in the 2n phase-space coordinates. Hill-climbing attains it every time, while
random regular graphs reach about v/2.

| (n, q) | system | points v | ceiling | binary CSS (odd q) |
|---|---|---|---|---|
| (2, 2) | 2 qubits (doily) | 15 | 5 | — |
| (3, 2) | 3 qubits | 63 | 7 | — |
| (4, 2) | 4 qubits | 255 | 9 | — |
| (2, 3) | 2 qutrits | 40 | 11 | [[40, 8]] |
| (3, 3) | 3 qutrits | 364 | 22 | [[364, 28]] |
| (2, 5) | 2 ququints | 156 | 36 | [[156, 24]] |
| (2, 7) | 2 qudits, q = 7 | 400 | 85 | [[400, 48]] |

For odd q, the identity mod 2 gives A² ≡ 0 (μ is even), so the binary CSS family exists at every n.

**[I] Reading.**

- The graph state on the n-qubit commutation graph has 4ⁿ − 1 qubits, yet carries at most **2n + 1 ebits** across any cut: one per
  phase-space coordinate, plus one.
- In general, the entanglement of the commutation network is set by the dimension of its phase space, through the polynomial functions of
  degree p − 1 on F_p^(2n), not by its number of vertices.
- The network "remembers" that it came from 2n coordinates.

**Stabilizer geometry for qubits (12435, extended).**

- The frames number 15 (DW(3,2)) and 135 (DW(5,2)).
- The sphere sizes equal the formula: 1, 6, 8 and 1, 14, 56, 64.
- Every nonzero overlap equals 2^(−d), and antipodal frames are mutually unbiased.

## 12439: prior art, and what the ceiling means for computation

**Prior art.** The other track's 2026-10-22 note (Section III) already proved, for W(3,p):

- (A + I)² ≡ J;
- the non-commutation matrix B_xy = ⟨x, y⟩^(p−1) (the Fermat "is the commutator nonzero?" detector), with B² = 0 and
  rank_p B = C(p + 2, 3);
- the Jordan structure.

The 12412/12419 mechanism repeats it. The 12418 document now cites it.

Its direct rank proof explains the monomial count: the columns of B are the (p − 1)-th powers of linear functionals, which span the degree-(p
− 1) polynomials. The same holds in 2n variables, which gives the 12438 formula. What is new here:

- reading rank_p(A + I) as a graph-state entanglement ceiling;
- the extension to every n;
- the qubit result of 2n + 1.

**[E] + derived: measurement-based computation on these states.**

- **The theorem.** Van den Nest, Dür, Vidal and Briegel (PRA 75, 012337, 2007): graph states whose Schmidt-rank width grows at most
  logarithmically are efficiently classically simulable as measurement-based resources.
- **Qubits.** Every cut has rank at most 2n + 1, and v = 4ⁿ − 1, so the width is at most 2n + 1 = O(log v). Measurement-based computation
  on the commutation-graph state of n qubits is therefore efficiently classically simulable. The Pauli geometry alone is not a
  computational resource.
- **p ≥ 3.** The width is at most 1 + C(2n + p − 2, 2n − 1) = O((log v)^(p−1)), outside the theorem's logarithmic regime. A tree tensor
  network would need bond dimension p^O((log v)^(p−1)), quasi-polynomial at best.
- **Reading [I].** The qutrit geometries sit just past the simulability line where the qubit ones stop. Whether they are universal resources
  is open.

## 12437: correction to 12432 (the colour obstruction was search-mode dependent)

The test applied loose hypercharge values with no anomaly condition. Colour-only feasibility then splits as follows:

| constraint set | feasible |
|---|---|
| quark doublets alone | all 23 |
| doublets + up-type triplets | all 23 |
| doublets + down-type triplets | all 23 |
| **all colour states** | **17 of 23** (6 colour-blocked) |

- **What was wrong.** The 12432 statement "all 23 are colour-blocked" (in 2afb7f278) holds only in the stricter base search. It is
  corrected here.
- **What is still open.** The conclusion "no three-generation hypercharge" for the new parents was also base-mode only. A full relaxed
  search on all 23 runs now, and its result is recorded in the certificate (`12437_relaxed_full`).

## 12440: prior art across the repositories (searched by result, including months-old material)

| claim in this block | prior art found | status |
|---|---|---|
| (A + I)² ≡ J (mod p); B = ⟨x, ·⟩^(p−1), B² = 0, rank_p B = C(p + 2, 3) | `2026-10-22_pascal_phinary_frobenius_jordan_five_frontiers.md` §III (other track) | **known**; cited |
| rank_p(A + I) as a graph-state entanglement ceiling; extension to W(2n − 1, q); qubits 2n + 1 | none found (corpus, Holotrade, W33-VM, W33-inspect, Theory; web) | new reading; ranks are Smith's |
| binary CSS from A² = 0; ker₂ A = even line sums; E8/2E8 plus-type logical module | `2026-10-29_W33_even_line_resolution.md` (other track); `2026-07-10_levi_five_frontiers.md` (July); Holotrade [[120,40,8]] (same method on a 120-vertex graph) | **known structure**; the q = 5 MILP distance d = 10 is new |
| stabilizer frames / spreads ↔ MUBs; ovoids ↔ MUB states | Pass 70 (2026-07-08), `2026-05-29_spread_square_we6_factorization.md`, Holotrade `context_cover_equals_mub_count_iff_q_even.py`; Calderbank–Cameron–Kantor–Seidel 1996 | **known**; the overlap = q^(−d) check is a re-verification |
| 360 two-qutrit stabilizer states | BT821 (operator–operand duality) | **known** |
| graph-state Schmidt spectra / 2-ranks on W(3,3) and Q(4,3) | `2026_10_23_cospectral_quantum_photon_point_line_dual_breakthrough.md` (cites Pass 88) | **known** (different quantities) |
| measurement-based simulability of the qubit commutation-graph state | none in the corpus; follows from Van den Nest–Dür–Vidal–Briegel 2007 | new application |
| code distance = entanglement-deficit threshold (q = 3, exhaustive) | none found | new |

**A route to a general proof of d = 2q.** The even-line resolution ker₂ A = {N y : Σ y even} reduces the distance to the minimum weight
of a nonzero even sum of lines.

- Two intersecting lines give 2q.
- Two disjoint lines give 2q + 2.
- For grids, take k lines from one ruling and m from the other. The weight is (q + 1)(k + m) − 2km, which vanishes at k = m = q + 1 and
  otherwise has minimum 2q (at k = m = 1, or k = m = q).

## 12437 (result): the full relaxed search finds one hypercharge — SM_2541_c22

**One candidate passes.** Among the 23 radius-safe, exotic-free new-parent candidates, **exactly one** admits a three-generation hypercharge:
Z6II_06_SM_20260917_2541_c22.

**What it has:**

- **Hypercharge:** t = (0⁸; 1/6, 0, 0, −5/6, −1/6, 5/6, −7/6, 1/6), lying entirely in the second E8 together with the visible SU(3)×SU(2).
  The hidden group is SU(2)⁴ in the first E8.
- **Normalisation:** k_Y = 2t² = 17/3, with Tr Y = 0.
- **Chiral content:** exactly three Standard-Model generations.
- **Anomaly-free:** t is orthogonal to every non-abelian root and to the anomalous U(1) direction (t · T_anom = 0, with |T_anom|² = 2816).
  The base search missed it only because some of its fields need hypercharge values outside the base search's allowed sets.
- **Radius:** tachyon-free at large radius on both fixed tori; tachyonic at small R5 (18 states).
- **Spectrum:** no hypercharge-independent exotics; 36 Higgs-doublet scalar listings.

**Why it fails:**

- **Massless fractional charges.** 90 of its 92 fractional-charge fermions pair at all orders. One (1,2,0) pair (electric charges ±1/2) is
  forbidden at every order by the exact lattice test. A lone doublet cannot give itself a mass, and no Higgs coupling has the right
  hypercharge. So it keeps massless fractionally charged states, which experiment excludes.
- **k_Y = 17/3 is the hard normalisation.** Pass 12156 estimated that k_Y = 17/3 needs a string-scale threshold of about −2636 (the
  fraction-free route).

**Verdict.** This is the closest model the heterotic Z6-II route has produced: three generations, an anomaly-free hypercharge, and
large-radius stability. It is still excluded, by one unliftable fractional pair and its k_Y.

## 12434 (q = 7)

The exact program hit its 50-minute limit with a 97.5% optimality gap, so it is not solved. At q = 7, d = 14 remains search evidence
(12426).

## 12441: synthesis

- **Codes.** d = 2q is proved at q = 3 and 5 (exact). Stabilizer weight 2q + 2 is proved for the even case, at all q. The even-line
  resolution (other track) is the route to a general proof.
- **Entanglement.** The ceiling 1 + C(2n + p − 2, 2n − 1) holds across W(2n − 1, q). For qubits it is 2n + 1, so measurement-based
  computation on these states is efficiently simulable. The rank formulas are classical and prior in the corpus; the entanglement and
  computation readings are new.
- **Stabilizer geometry.** Overlap = q^(−d), with antipodes mutually unbiased. This re-verifies the known MUB/spread dictionary (Pass 70,
  May 29 spread note, Holotrade).
- **Strings.** The 12432 colour claim is corrected (17/23 colour-feasible). One genuine three-generation, anomaly-free, radius-stable
  hypercharge model was found; it fails on one fractional pair and k_Y = 17/3.

## Cross-track ownership (same day, by commit time)

| result | owner (earlier commit) | this block |
|---|---|---|
| q = 5 distance d = 10, [[156,24,10]] | **cdde9b06b** (14:25, other track) | independent exact MILP confirmation (14:41), cited |
| q = 7: 10 ≤ d ≤ 14 | **055804fc2** (14:46, other track) | my exact MILP timed out; their bound stands |
| rank-3 dual polar C₃(3) (1120 frames), shells and spectrum | **30997a710** (15:13, other track) | additions: overlap = q^(−d) on state vectors, antipodes mutually unbiased, qubit DW(3,2)/DW(5,2) |
| even-case bound 2q + 2 (no-triangle proof) | — | this block |
| graph-state ceiling across W(2n − 1, q); qubits 2n + 1 → simulable MBQC | — | this block (ranks prior in-corpus) |
| 12432 correction; SM_2541_c22 | — | this block |
