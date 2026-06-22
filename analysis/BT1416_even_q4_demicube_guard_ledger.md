# BT1416 — Even-Q4 Demicube Guard Ledger Theorem

## Commit frontier used

This continues the BT1410--BT1415 local-front-end chain:

- BT1410: the Witting delayed-query frame compiler gives the `640 = 40*4*4` admission ROM, with `480` off-diagonal data handshakes and `160` contextual witness apertures.
- BT1411: the `40` Witting tetrads compile to sparse analyzer unitaries with the optical-family split `1+12+27`.
- BT1412: the toroidal Q4 clock supplies the eight-word every-other even projection and the `24 - 3 = 21` toroidal boundary.
- BT1413--BT1415: Q4 plaquettes compile to tomotope/Q6 flags, the Csaszar/Szilassi port supplies the active `168 = 21*2*4` toroidal slots, and the even-Q4/Steinberg ledger fills `27*8 + 24 = 240` CSS front-end rows.

## New theorem

The BT1412 even projection is not merely a distance-2 binary clock code. It is the four-dimensional demihypercube graph on the eight even Q4 words.

Let

\[
E(Q_4)=\{x\in\mathbb F_2^4: |x|\equiv0\pmod2\}.
\]

Connect two even words when their Hamming distance is two. The verifier proves

\[
\boxed{E(Q_4)_{d=2}\cong K_{2,2,2,2}},
\]

with

\[
|V|=8,\qquad |E|=24,\qquad \deg=6.
\]

The complement inside the complete graph on the eight even words is exactly four antipodal pairs. Therefore the even layer decomposes as four antipodal axes, and every pair of axes contributes one `K_{2,2}` block:

\[
\boxed{24=\binom42\cdot4}.
\]

## Guard-row interpretation

Every square plaquette of Q4 has two even and two odd vertices. Taking the even diagonal gives a bijection

\[
\boxed{
\{\text{Q4 square plaquettes}\}
\longleftrightarrow
\{\text{distance-2 edges in the even demicube}\}.
}
\]

So the `24` Q4 plaquette guard rows in BT1415 are not a loose count. They are the binary incidence rows of the demicube edges.

The guard matrix has

\[
24\text{ rows},\qquad 8\text{ columns},\qquad \operatorname{rank}_{\mathbb F_2}=7.
\]

The rank is exactly the even-parity incidence subspace. The missing odd direction is supplied by the singleton Steinberg-state rows in the full ledger:

\[
27\cdot8=216
\]

single-state syndrome rows, so the complete front-end ledger is

\[
\boxed{216+24=240}
\]

with full rank

\[
\boxed{\operatorname{rank}_{\mathbb F_2}=8}.
\]

Each even state is touched by

\[
27+6=33
\]

rows: twenty-seven singleton Steinberg-cycle rows and six plaquette guard rows.

## Machine checks

```json
{
  "complement_is_4_antipodal_edges": true,
  "even_layer_has_24_edges": true,
  "even_layer_has_8_vertices": true,
  "even_layer_is_6_regular": true,
  "even_layer_is_K2222": true,
  "even_ticks_are_even": true,
  "full_ledger_has_240_rows": true,
  "full_ledger_rank_F2_is_8": true,
  "full_ledger_state_degree_is_33": true,
  "guard_rank_F2_is_7": true,
  "q4_faces_biject_to_even_edges": true,
  "q4_has_16_vertices": true,
  "q4_has_24_square_faces": true,
  "q4_has_32_edges": true,
  "six_axis_pairs_each_have_4_edges": true
}
```

## Boundary

This is a binary Q4 front-end certificate. It does not construct the protected \(\mathbb F_3\) Steinberg module, prove a new CSS stabilizer code, or calibrate a physical chip. It supplies the exact 24-row guard incidence layer missing from the BT1415 narrative and explains how the binary Q4 side interfaces with the existing ternary CSS/Steinberg side.
