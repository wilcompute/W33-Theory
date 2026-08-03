# Passes 2809–2815 — the tetrahedral support shell closes objectwise

## Executive result

Pass 2808 found a 15-fiber support quotient of the 40 W33 points. This release executes all five stated continuations and two deliberately unconventional probes. The result is one coherent exact package:

1. the twelve tetrahedral face/pairing charts are the twelve existing Type-A selector operators, each a distinct `2160 x 160` signed matrix of rank 81;
2. the signed support classes carry a complete abstract tomotope incidence model, not merely its f-vector;
3. the 81 affine frame states admit an information-optimal seven-bit codec, while the 40 projective W33 addresses admit an information-optimal six-bit codec;
4. the quotient's `1+9+5` eigenspaces are a q-independent `D8` module;
5. the support quotient exists over every finite field `GF(q)`, including even and odd prime powers;
6. the W(3,q) random walk lumps exactly to this 15-state shell;
7. the eight full-support phase classes are a parity-code controller for the eight tomotope cells, and the 16 triangular faces are exactly the edges of `K4,4` between the two cell classes.

The aggregate release certifies **78 exact checks**. RTL simulation, synthesis, placement, timing and power remain separately firewalled until the dedicated remote workflow is observed.

## Repository reconciliation before novelty

The search was intentionally vocabulary-wide because this repository has repeatedly solved the same object under different names. BT699 established `2160 x 24 = 51840` valid local presentations and `24 = 8 masks x 3 channels`; BT713 constructed the signed `2160 x 160` operators; BT720 identified the four Type-A masks and three Fano channels; BT723 verified all twelve ranks are 81. Pass 2809 therefore closes the remaining objectwise dictionary rather than rediscovering the sheets.

For the tomotope, BT805 established the tetrahedral `PG(3,2)` cell model, BT850 computed 192 flags, automorphism order 96, two flag orbits and class `2_{0,1,2}`, and the Q4/Reye track identified the `12_4,16_3` medial layer. Pass 2810 reproduces those invariants from a signed-support incidence construction and treats agreement as a cross-check.

Broad searches over Markdown, Python, JSON, HTML, LaTeX, RTL, tests, archive notes and continuity files found no earlier exact result matching the seven-bit support codec, all-finite-field quotient formula, strong lumpability/Kemeny law, or parity/minority-coordinate controller. The GitHub code index missed known files during the audit, so this is a bounded search result, not a universal absence claim.

## Pass 2809 — exact selector face/pairing intertwiner

The four Type-A masks `0111, 1011, 1101, 1110` are the four tetrahedral faces. The channel dictionary is

```text
011 <-> (01)(23)
101 <-> (02)(13)
110 <-> (03)(12)
```

Regenerating BT713 gives twelve signed `2160 x 160` matrices. Every row has weight 8; all twelve matrices have rank 81 and distinct SHA-256 hashes; they choose twelve distinct cycles on every rectangle; their union rank is 81; and the face parameter action is `D8`-equivariant.

## Pass 2810 — signed-support realization of the tomotope

Ranks 0, 1 and 2 are projective signed support vectors in `{0,+1,-1}^4/{v~-v}` of weights 1, 2 and 3, with incidence by signed restriction. Four three-support cells have hemioctahedral profile `(3,6,4)`. Four positive-product full-support sign vectors have tetrahedral profile `(4,6,4)`. Every face lies in one cell of each type.

The resulting incidence geometry has f-vector `(4,12,16,8)`, 192 flags, automorphism group order 96, flag orbits `96+96`, and class `2_{0,1,2}`. Colors 0, 1 and 2 preserve the flag orbits; color 3 exchanges them.

## Pass 2811 — support-first frame codec and RTL

Enumerative coding reaches the information bounds exactly:

```text
81 affine states      -> 7 bits, codes 0..80
40 projective classes -> 6 bits, addresses 0..39
```

The address factors through a four-bit support mask and relative sign phase; a polarity bit restores the second affine representative. Exhaustive round trips and frozen permutation tables cover `F_p`, `CX_p->f`, `CX_f->p`, and `Z_p`. Hardware sources are `rtl/w33_pass2811_support_first_codec.sv` and its exhaustive testbench.

## Pass 2812 — q-independent D8 module

For the stabilizer `D8` of one coordinate matching, the quotient eigenspaces decompose as

```text
q(q+1), dim 1: A1
q-1,    dim 9: 3A1 + B1 + B2 + 2E
-(q+1), dim 5: A1 + 2B1 + E
```

Thus the support shell is `5A1 + 3B1 + B2 + 3E`, with no `A2` constituent. Exact projectors reproduce this at q=2,3,5,7,11. This is a module for the chosen matching stabilizer, not the full symplectic group.

## Pass 2813 — all-finite-field support theorem

For every finite field `GF(q)`, including even and odd prime powers, put `s_S=(q-1)^(|S|-1)`, `r=|T intersect tau(S)|`, and

```text
N_r(q)=((q-1)^r+(q-1)(-1)^r)/q.
Q_ST=(q-1)^(|T|-r)N_r(q)/(q-1)-delta_ST.
```

Then

```text
spec(Q)=q(q+1)^1+(q-1)^9+(-(q+1))^5,
diag(s)Q=Q^Tdiag(s),
Q^2=(q^2-1)I-2Q+(q+1)1s^T.
```

Symbolic identities are supplemented by objectwise witnesses at q=2,3,4,5,7,8,9,11. Only q=3 specializes to the tomotope capacity vector `(4,12,16,8)`.

## Pass 2814 — outside-box result I: exact lumped Markov clock

The unbiased random walk on `W(3,q)` is strongly lumpable through support. Its 15-state transition matrix is `P=Q/(q(q+1))`, with stationary law `pi_S=(q-1)^(|S|-1)/((q+1)(q^2+1))` and spectrum

```text
1^1+((q-1)/(q(q+1)))^9+(-1/q)^5.
```

The absolute relaxation rate is exactly `1/q`, and

```text
K_support=9q(q+1)/(q^2+1)+5q/(q+1).
```

At q=3, the nontrivial eigenvalues are `1/6,-1/3`, `K_support=291/20`, `K_full=801/20`, and the internal residual is `51/2`. This is a finite random-walk theorem, not a physical-time derivation.

## Pass 2815 — outside-box result II: parity-code tomotope controller

Normalize a full-support sign vector to start with `+1` and record the other three signs as bits. The even words `000,011,101,110` form the `[3,2,2]` single-parity-check code and label the tetrahedral cells. Every odd word has a unique minority coordinate; deleting it labels the hemioctahedral cell. The map is `S4`-equivariant.

The sixteen triangular faces are all pairs `(hemioctahedron,tetrahedron)`, so top incidence is exactly `K4,4` with faces as edges. One XOR computes cell type; a four-way minority decoder selects the odd cell. Hardware source: `rtl/w33_pass2815_tomotope_cell_classifier.sv`.

## Reproduction

```bash
python analysis/bt2809_2815_release.py --verify-frozen
pytest -q tests/test_bt2809_2815_seven_frontiers.py
```

The focused test suite is `7/7`; the release aggregate is `78/78`. Remote hardware evidence is handled by `.github/workflows/w33_pass2809_2815_seven_frontiers.yml`.

## External anchors

- B. Monson, D. Pellicer and G. I. Williams, *The Tomotope*, Ars Mathematica Contemporanea 5 (2012), 355–370, DOI `10.26493/1855-3974.189.e64`.
- D. R. Barr and M. U. Thomas, *An Eigenvector Condition for Markov Chain Lumpability*, Operations Research 25 (1977), 1028–1031, DOI `10.1287/opre.25.6.1028`.

These references anchor the abstract-tomotope and Markov-lumpability language. All identities in this release are proved by executable repository witnesses.
