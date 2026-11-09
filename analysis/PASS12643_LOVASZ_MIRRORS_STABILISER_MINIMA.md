# Pass 12643: three-qubit Pauli MUB sets satisfy F ≥ |v|⁴/(4φ²) exactly (Lovász number 4 + √5); qubit mirror pairs are not chiral; stabiliser states attain min F on every rung except the qutrit pentads

Claude track. Follows Pass 12642. **Not a theory of everything.** These are finite statements about Pauli measurement sets.

## 0. Corrections first

- **The 1/d pattern of Pass 12642 is a pattern of certified bounds, not of minima.** The bound 1/d is tight at d = 4 and d = 8, but **not at d = 9**: the pentads have min F = 0.14711 (Passes 12637 and 12639; reproduced here).
- **Three-qubit strong unextendibility is published.** Mandayam, Bandyopadhyay, Grassl and Wootters (arXiv:1302.3709, §4) proved it for one explicit 5-set by a Magma Gröbner basis, and wrote that "a general proof remains elusive" for their other sets. Pass 12642 should have cited this. What is new here is listed in §1.

## 1. Three qubits: all 24,192 sets, with an exact constant (`w33_mirror_orbits.py`, `w33_lovasz_theta_unextendible.py`)

**All of them are equivalent.** Orbits under transvections, which generate Sp(6,2):
- the 24,192 size-5 maximal partial spreads form **one orbit**;
- Clifford unitaries realise Sp(6,2) and preserve unbiasedness, so the single published example implies **every** size-5 set is strongly unextendible.

This settles the "general proof" question of Mandayam et al. for d = 8.

**An exact, computer-algebra-free constant.** For n qubits and a pure state, Σ over all Paulis of ⟨P⟩² = d − 1. With the twirl identity this gives

F(v) = (d − 1 − Σ_{P∈U} ⟨P⟩²)/d,  where U is the set of uncovered points.

The de Gois–Hansenne–Gühne relation (PRA 107, 062211 (2023)) states Σ ⟨A_i⟩² ≤ ϑ(G) for ±1 observables, with G the anticommutation graph. A stabiliser state attains α(G). Hence

(d − 1 − ϑ)/d ≤ min F ≤ (d − 1 − α)/d.

| set | \|U\| | α | ϑ (SDP) | result |
|---|---|---|---|---|
| two qubits, size 3 | 6 | 2 | 2.0000000 | **min F = 1/4, exact** (ϑ = α) |
| three qubits, size 5 | 28 | 6 | 6.2360680; **≤ 4 + √5 exactly** | (3 − √5)/8 ≤ min F ≤ 1/8 |

The graph on U is 12-regular. Its exact characteristic polynomial is

(λ − 12)(λ − 4)(λ + 2)⁵ (λ² + 2λ − 4)³ (λ³ − 12λ + 8)⁵,

so λ_min = −4cos(π/9). Lovász's bound for regular graphs, ϑ ≤ n(−λ_min)/(k − λ_min), gives ϑ ≤ 28cos(π/9)/(3 + cos(π/9)) = 6.6785, and therefore:

> **For every size-5 three-qubit Pauli MUB set and every v ∈ C⁸:**
> Σ_e (|⟨e|v⟩|² − |v|²/8)² ≥ **21(1 − cos(π/9)) / (8(3 + cos(π/9)))** · |v|⁴ ≈ 0.0402 |v|⁴.

**Sharper, and exact: ϑ ≤ 4 + √5** (`w33_theta_coherent_closure.py`, `data/w33_theta_coherent_closure.json`).
- The coherent closure (2-dimensional Weisfeiler–Leman) of the graph has rank 21. It splits the 28 vertices into classes of **1 + 12 + 15**, so one uncovered point is distinguished, and it has 8 edge classes.
- The reduced dual gives Y = J + Σ y_k B_k with y = (−(1 + 3√5)/2, 0, (7 − √5)/2, −(1 + 3√5)/2, −2 − √5/2, −2 − √5/2) on the symmetrised edge classes.
- Its characteristic polynomial, computed exactly over Q(√5), is

  (λ + 11)³ (λ + 4 + √5)⁵ (λ − 4 − √5)¹⁸ (λ² − (9 − 13√5)λ − 95/2 + √5/2),

  with all roots real and the largest exactly 4 + √5. So ϑ ≤ 4 + √5. The full SDP returns 6.2360680, so equality holds numerically.

> **Theorem (exact, given de Gois et al. 2023).** For every size-5 three-qubit Pauli MUB set and every v ∈ C⁸:
> Σ_e (|⟨e|v⟩|² − |v|²/8)² ≥ **(3 − √5)/8** · |v|⁴ = |v|⁴/(4φ²) ≈ 0.0955 |v|⁴.

**The distinguished vertex** (`w33_threequbit_sentinel_point.py`). The single-vertex class is the **unique uncovered point p₀ through which no Lagrangian meets the covered set in exactly one point**:
- per-vertex invariants (triangles, covered sums, once-meeting lines through it) are (36, 0, 0) for p₀, against (28, 8, 4) ×15 and (26, 10, 5) ×12 for the rest;
- all 12 of its anticommuting uncovered neighbours have uncovered sums.

So p₀ is a qubit analogue of a sentinel. It is the one uncovered point that no minimising stabiliser state (a line meeting C once) touches.

The cos(π/9) constant above is the weaker eigenvalue-only version. The golden ratio fits the order-60 (A5-type) stabiliser, but no link is proved.

**What this establishes.**
- It is exact, given two published theorems: de Gois et al., and Lovász 1979, Theorem 9.
- It is quantitative, and it covers every set (via the single orbit).
- The tight value 1/8 is still certified only numerically (Pass 12642, degree-6 SOS).
- ϑ ≤ 4 + √5 is exact (the dual certificate); equality is numerical.
- Splitting edges by whether u + v is covered is *not* regular: the 28 vertices fall into several stabiliser types, and that two-parameter dual reaches only 6.42. The exact ϑ needs the full orbital algebra.

**Prior art in the repo:** the repo does not use the Lovász bound this way. External: Mandayam et al. (qualitative, one set, Gröbner); de Gois et al. (the inequality).

## 2. Mirror pairs one rung down (`w33_threequbit_mirror_pairs.py`, `w33_threequbit_witness_closed_form.py`)

| | two qutrits (pentads, control) | three qubits (size 5) |
|---|---|---|
| sets / covered point sets | 432 / 216 | 24,192 / 12,096 |
| fibre size | 2 (all) | 2 (all) |
| partners share lines | 0 | 0 |
| shared collinear pairs | 0 of 30 | **15 of 105** |
| second-moment difference | 7×10⁻¹⁶ | 3×10⁻¹⁵ |
| optimal 3rd-moment witness | 16/27 | **9/16** |
| attained by stabiliser states | yes, all 45 | yes, all 40 |
| meeting pattern, left line vs right set | {0, 1, 1, 1, 1} (points) | **{1, 1, 1, 1, 3}** for all 120,960 left lines |
| Sp-orbits / partners in same orbit | 2 × 216 / **0** | 1 × 24,192 / **all 12,096** |

**Closed form for qubits.** A stabiliser state scores 1 + 4·8/8³ = 17/16 on its own set. On the partner set it scores 1/4 + 4·(1/16) = 1/2, because a basis meeting its line in a k-dimensional subspace contributes (2^k/8)². So the witness is 17/16 − 1/2 = **9/16**.

**Reading.**
- Both rungs have exactly two sets per covered point set, and the two are separated only at third order.
- At two qutrits the partners lie in opposite PSp(4,3)-orbits, so only antiunitaries (the Kramers θ) swap them. That is **genuine chirality**.
- At three qubits a Clifford unitary swaps them. In characteristic 2, −1 = 1, so complex conjugation fixes every Pauli line, and there is no Kramers-type antiunitary to do the swapping.
- **Mirror pairs survive on both rungs; chirality is an odd-characteristic phenomenon.** This matches the earlier corpus statement that p = 3 is where the chirality torsor lives (memory: "chirality torsor = frame orientation, flipped only by antiunitaries").

## 3. Is min F the stabiliser value? (`w33_minF_covered_points.py`)

For a stabiliser state of a line M, F = (p − 1)|M ∩ C|/d. So min F ≤ (p − 1) m*/d, where m* = min_M |M ∩ C| ≥ 1 by maximality.

| set | stabiliser value (p − 1)m*/d | numerical min F | equal? |
|---|---|---|---|
| two qubits, 3 | 1/4 | 0.25 | yes |
| three qubits, 5 | 1/8 | 0.125 | yes |
| two qutrits, pentad | 2/9 = 0.222 | **0.14711** | **no** |
| two qutrits, 8 | 4/9 | 0.4444 | yes |
| two ququints, 13 lines (m = 2 cover) | 4/25 | **0.16000000** | yes |
| two ququints, 13 lines (second m = 2 cover) | 4/25 | 0.16000000 | yes |
| two ququints, 14 lines (m = 1 covers, both) | 8/25 = 0.32 (every line meets C at least twice) | **0.17333333** (≈ 13/75, not identified exactly) | **no** |

**d = 25 is strongly unextendible after all (numerically).** The 13-line uniform double cover, for which the degree-4 certificate fails (δ* = −0.32, Pass 12640), has min F = 4/25 > 0. The failure was a weakness of degree 4, not a sign of extendibility.

**The 14-line single covers are strongly unextendible numerically too** (min F = 0.1733 > 0; degree-4 δ* = −0.16).

**Non-stabiliser optima occur twice**: at the pentads (2/9 against 0.147) and at the d = 25 single covers (8/25 against 0.173). The m = 2 double covers in d = 25 are stabiliser-optimal, but the pentads are also double covers. So "m = 1" is not the rule, and no rule is claimed. The meeting histograms are recorded in `data/w33_ququint_stabiliser_value.json`.

## 4. Scope notes filed (item 3)

- `W33_CLAIM_STATUS_LEDGER.md`: four new rows (Pass 1866 reason, MCCCLXXI over-read, three-qubit status with priority, the 1/d tightness correction).
- `w33_pass1861_1866_*.md`: scope note appended (the result holds for all odd q, via Gow; the result itself is unchanged).
- MCCCLXXI is an early speculative file and is left as is. Its over-read is recorded in the ledger.

## 5. Literature (item 5)

- **Mandayam et al.:** see §0.
- **De Gois et al.:** see §1.
- **Third-moment / chirality witness:** one standard search found no prior treatment of higher moments separating MUB sets with equal second moments. Index-of-coincidence work (e.g. arXiv:1407.6816) shows second moments depend only on purity for complete sets. That is not a novelty claim, just a record of what was searched.

## Open

- An exact primal for ϑ = 4 + √5 (equality); what the distinguished uncovered point is.
- The exact tight 1/8.
- An exact certificate for the d = 25 minimum 4/25 (the qudit analogue of the Lovász route needs non-dichotomic observables; de Gois et al. treat this in a weighted form).
- Which sets have non-stabiliser optima (pentads; d = 25 single covers), and what the optimal states are; the exact value of 0.17333.
