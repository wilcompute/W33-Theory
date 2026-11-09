# Pass 12640: the doily S6 is the other track's nine 5D blocks; two ququints; three qubits at degree 8

Claude track. Continues Pass 12639. Independent exact replay by the other track: 7332f3b48 (`analysis/2026-11-09_exact_mub_sym2_blocks.md`). It certifies all 603 maximal partial spreads of W(3,3) in Z[ω] and credits Pass 12639 with the exact proof. Its finite-shot witness is d03221905, and its Q8 eight-MUB classification is a839fb66a and following.

## Item 2 + 4: two proofs, one structure (`w33_s6_sectors.py`)

The other track splits Sym²(C⁹) into nine 5-dimensional centre-of-mass sectors (s = z + w), permuted by translations.
- The five sentinel swaps of Pass 12639 **preserve every sector** (5/5).
- On a sector, their character is **3 on a transposition and 2 on a 3-cycle: the standard representation (5,1) of S6.**

So the other track's nine identical 5D cyclotomic blocks are the nine copies of (5,1) in Sym²(C⁹) = 9·(5,1). On each block the Jucys–Murphy element J₆ has the content eigenvalues 4 (×4) and −1 (×1). The exact-integer proof and the symmetric-group proof describe the same decomposition.

## Item 1: two ququints (d = 25): the sentinel principle predicts the certified sets (`w33_ququint_umub.py`)

- **Basis-free certificate.** By the twirl identity, M = (1/d) Σ_{u covered, u≠0} W_u⊗W_u† and δ* = λ_min on Sym²(C^d). The control reproduces the d = 9 pentad's 1/9.
- **Sample.** 24 random greedy maximal partial spreads of W(3,5) (156 lines, 325 splits), of sizes 14–24.

**The certified sets (δ* > 0) are exactly those whose uncovered points are uniformly covered by splits:**

| size | uncovered | split cover | δ* | closed form |
|---:|---:|---|---:|---|
| 24 | 12 | 1 split, covered once | **16/25** | M = (26 − 10S)/25 on Sym², S = ±1 |
| 22 | 24 | 2 splits, covered once | **8/25** | M = (28 − 10(S₁ + S₂))/25 |
| 14–22, all others | 24–72 | not uniform | ≤ 0 | — |

For the single-split case the proof is one line. On Sym², the local Pauli sums give T_U = 2p·S − 2 with S² = 1, so M = (d + 1 − 2pS)/d ≥ (d + 1 − 2p)/d = 16/25.

**So two-ququint sets of 24 MUBs leaving one factorisation uncovered are strongly unextendible**, as are 22-sets leaving two. The general statement for p² dimensions: a maximal partial spread whose uncovered set is one split is strongly unextendible, with F ≥ (p − 1)²|v|⁴/p². This gives 4/9 at p = 3 (the size-8 sets) and 16/25 at p = 5. The random sample found no pentad-like small sets in d = 25; whether they exist is open.

## Item 3: three qubits at degree 8

The degree-8 Hermitian bound (Sym⁴(C⁸), dimension 330) is **−0.164**, the same value as at degree 6. The Hermitian hierarchy appears stuck, consistent with the absence of any split cover. A non-Hermitian or symmetry-reduced certificate would be needed.

## Item 5: E8

Not attempted, for the reason given in Pass 12639.

## Item 5: the substrate link, on prior-art footing

The S6 that proves the bound is the doily of the 15 splits swapped by a Kramers reversal θ. By Pass 11210, θ is a genuine time reversal with **θ² = −1**: it is the T² = parity class, which needs an even number of qutrits. **So the strong unextendibility of the two-qutrit pentads follows from the Kramers time-reversal structure of two qutrits.** Each pentad's 5 sentinels are a star in the doily of one time reversal, and the bound is the content spectrum of that doily's Jucys–Murphy element.

This is a structural statement about the substrate's own time-reversal operator. It is not a dynamical prediction.

## Item 4: three qubits with charge-0 SOS terms (`w33_real_sos_threequbit.py`)

The full degree-4 real SOS for a U(1)-invariant quartic consists of Hermitian charge ±2 terms plus charge-0 terms (v†Cv)². It is an SDP over a 64×64 Gram matrix of Hermitian C's plus a Sym² block.
- **Controls.** The two-qutrit pentad gives 1/9, unchanged. Four spread bases give 0, against −4/9 for the Hermitian bound: tighter, as expected.
- **Three-qubit size-5 sets: δ = 0.** The bound improves from −5/8 to 0 but does not become positive. That is only the trivial F ≥ 0, since F is a sum of squares.
- **Conclusion.** No degree-4 SOS certificate exists for the three-qubit case. Their strong unextendibility (numerical min 1/8) needs a higher-degree real SOS or an algebraic argument; it stays open.

## Item 2: structured sets in d = 25, and a refinement of the principle (`w33_ququint_sentinel_search.py`)

The integer program finds maximal partial spreads whose uncovered points are uniformly covered by splits, minimising size; HiGHS was given 600 s per run. The control (q = 3, m = 2) finds a pentad: 5 lines, 5 sentinels, δ* = 1/9.
- **q = 5, m = 2:** a set of 13 lines with 13 sentinels covering every uncovered point exactly twice (the pentad analogue). **δ* = −0.32: not certified.** Here λ_max(R) = 9, above the threshold m(d − 1)/(2p) + s/p = 7.4.
- **q = 5, m = 1:** 14 lines, 6 disjoint sentinels. δ* = −0.16, with λ_max(R) = 4 against a threshold of 3.6.

Both runs hit the time limit, so minimality is not proved.

**Refined principle.** A uniform split cover makes M affine in the swaps, but certification also needs λ_max(R) below the threshold. The two-qutrit pentads pass because their five swaps generate the doily S6, whose Jucys–Murphy element has λ_max = 4. The d = 25 double covers found here do not have that structure. Whether some d = 25 double cover generates a symmetric group with a small enough Jucys–Murphy spectrum is open; a search could add "the swaps satisfy star-transposition relations" as a constraint.

## Round of 2026-11-09 evening: audit, package, zero forcing, Kramers sectors

**Item 5: audit of this session's claims against the older corpus.** Results grepped by content across `analysis/*.md`, excluding this session's files:

| result | finding |
|---|---|
| Jucys–Murphy / doily-S6 proof | no earlier hits |
| strong unextendibility | no earlier hits; only the other track's audits of these passes |
| unextendible 8-MUB sets | no earlier hits |
| Sym² block structure | no earlier hits |
| reflection = Kramers time reversal | **prior art, Pass 11210** (corrected above) |
| triality on 135 = 45 × 3 frames | **related prior art, BT3769** ("a triality-twisted Lagrangian frame action") |

BT3769 does not state the unitary-Z₃ / antiunitary-transposition split of Pass 12637, but it should be cited alongside it.

**Item 3: packaged.** One shareable page (private until shared): https://claude.ai/artifact/F9piRZo3UkxGiuURXFLHwV. It contains the theorem, the four-step proof, the sentinel theorem with its table of cases, the operational corollary (the other track's) and the geometry. The repository version is `analysis/NOTE_STRONG_UNEXTENDIBILITY_PROOF.md`.

**Item 2: three qubits by zero forcing** (`w33_qubit_zero_forcing.py`). The qubit version keeps only commuting pairs, because anticommuting terms cancel. It is inconclusive, and too weak: it leaves alive even the two-qubit size-3 sets, which the SOS bound proves strongly unextendible. The three-qubit size-5 sets remain open; the next honest step is a symmetry-reduced degree-6 real SOS.

**Item 4: Kramers sectors (structural only).** By Pass 11210, θ² equals the parity operator P: x → −x on F₃⁴, so P is the Pauli group's −1 automorphism realised on C⁹. On the parity −1 sector (dimension 4), θ² = −1. Hence any θ-invariant Hamiltonian commuting with P has Kramers doublets there: two doublets in the 4-dimensional sector. Whether these align with a pentad's sentinel structure would need an explicit antiunitary Clifford θ on C⁹, which is not constructed here.
