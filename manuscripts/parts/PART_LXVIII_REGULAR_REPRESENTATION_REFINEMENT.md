# PART LXVIII — Regular-Representation Refinement of the Generation Split

**Status:** structural refinement of Part LXVII  
**Depends on:** `PART_LXVII_order3_generation_split.py` and results JSON

Part LXVII proves that every order-3 symplectic transvection acts on the canonical homology carrier `H1` with eigenvalue multiplicities

```text
1:       27,
omega:   27,
omega^2: 27.
```

Equivalently,

```text
charpoly(g | H1_C) = (x - 1)^27 (x^2 + x + 1)^27.
```

Part LXVIII records the representation-theoretic consequence:

\[
\boxed{H^1_{\mathbb C}\cong U\otimes \mathbb C[C_3],\qquad \dim U=27.}
\]

That is, the canonical matter carrier is **twenty-seven copies of the regular representation of `C3`**.

---

## 1. Why this matters

Earlier versions of the theory used the arithmetic identity

\[
81=27+27+27
\]

as the generation split.  Part LXVII/LXVIII replaces that with the stronger statement

\[
H^1_{\mathbb C}
=H^1_{(0)}\oplus H^1_{(1)}\oplus H^1_{(2)},
\qquad
\dim H^1_{(i)}=27,
\]

where the three summands are the Fourier eigenspaces of an actual order-3 symplectic action.

The split is therefore not imposed.  It is the regular-fiber decomposition of the canonical homology sector.

---

## 2. Representation-theoretic statement

Let `g` be any projective symplectic transvection of order 3 acting on the triangle chain complex of `W(3,3)`.  Let

\[
H^1=\ker d_1\cap\ker d_2^T
\]

or, equivalently from Part LXVI,

\[
H^1=E_{-6}(K),
\]

where `K=Q^T(T-O)Q` is the signed 1-chain turn operator.

Then, over `C`,

\[
H^1_{\mathbb C}
=E_1(g)\oplus E_\omega(g)\oplus E_{\omega^2}(g),
\]

with

\[
\dim E_1(g)=\dim E_\omega(g)=\dim E_{\omega^2}(g)=27.
\]

Since the regular representation of `C3` has character

\[
\chi_{\mathrm{reg}}=(3,0,0),
\]

the character of `H1` is

\[
\chi_{H^1}=(81,0,0)=27\chi_{\mathrm{reg}}.
\]

Therefore

\[
\boxed{H^1_{\mathbb C}\cong 27\,\mathbb C[C_3].}
\]

---

## 3. Real versus complex structure

This distinction should be explicit in the manuscript.

Over `C`:

\[
H^1_{\mathbb C}=27\oplus27\oplus27.
\]

Over `R`:

\[
H^1_{\mathbb R}=27\oplus54,
\]

where the `54` is a real rotation sector carrying the conjugate pair of nontrivial complex characters.

Thus the generation split is naturally complex/Fourier-theoretic.

---

## 4. Bridge to the E8 Z3 grading

The next target is now sharply defined.

The target exceptional decomposition is

\[
E_8 = \mathfrak g_0\oplus\mathfrak g_1\oplus\mathfrak g_2,
\qquad
\dim(\mathfrak g_0,\mathfrak g_1,\mathfrak g_2)=(86,81,81),
\]

with

\[
\mathfrak g_0=E_6\oplus A_2,
\qquad
86=78+8.
\]

The W33 side now supplies a canonical 81-dimensional regular-fiber carrier:

\[
H^1_{\mathbb C}\cong U\otimes\mathbb C[C_3],\qquad \dim U=27.
\]

A contragredient or dual copy can supply the second 81-sector dimensionally:

\[
H^1\oplus (H^1)^*\oplus (E_6\oplus A_2)
\quad\leadsto\quad
81+81+86=248.
\]

This is not yet a bracket construction.  It is the correct representation-theoretic skeleton on which a bracket construction should be tested.

---

## 5. What remains open

Part LXVIII does **not** claim to have constructed the E8 Lie bracket.  It proves the regular-representation shape of the matter carrier.  The next theorem must construct or falsify a natural product/bracket of the form

\[
H^1_{(i)}\times H^1_{(j)}\longrightarrow H^1_{(i+j\,\mathrm{mod}\,3)}
\]

or a larger closure

\[
H^1\times (H^1)^*\longrightarrow E_6\oplus A_2.
\]

This is now the sharp next bottleneck.

---

## 6. Regression tests

The corresponding regression tests are in

```text
tests/test_regular_representation_lxviii.py
```

They verify:

- `H1` character equals `27` times the regular `C3` character;
- the three Fourier projector ranks are `27,27,27`;
- the real/complex decomposition distinction is explicit;
- the E8 `Z3` skeleton dimension identity is recorded;
- no E8 bracket-closure claim is made yet.
