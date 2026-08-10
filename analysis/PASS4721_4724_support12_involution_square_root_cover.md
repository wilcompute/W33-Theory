# Passes 4721–4724 — the support-12 shell resolves the unnamed 270 and lifts it to an order-4 square-root cover

## Why this lane was opened

Passes 4703–4704 closed the exact support-12 minimum shell of the apartment code: the 1,620 weight-608 minima are the corner-star thickenings `T(A)` of the 1,620 W33 apartments, and they span the canonical `[1620,38,270]` even-coefficient subcode. The immediate question was whether the minimum shell itself carries another intrinsic relation that had not already been extracted.

It does.

The verifier is:

`analysis/w33_pass4721_4724_support12_involution_square_root_cover.py`

Frozen output:

`data/PART_W33_PASS4721_4724_SUPPORT12_INVOLUTION_SQUARE_ROOT_COVER.json`

Regression:

`tests/test_w33_pass4721_4724_support12_involution_square_root_cover.py`

---

## Pass 4721 — disjoint support turns the 1,620 minima into 540 triangles

Put an edge between two support-12 thickenings when their 12-line supports are disjoint. Exhaustively:

- every thickening has exactly **2** disjoint partners;
- every connected component has size **3**;
- all three vertices of every component are mutually adjacent.

Therefore

\[
\boxed{\Delta_{12}=540K_3.}
\]

Each component consists of three pairwise-disjoint 12-line supports, so it covers 36 of the 40 W33 lines. The four-line complement is always a set of four pairwise-disjoint W33 lines.

The 540 triangles do not give 540 different complements. They give exactly

\[
\boxed{270}
\]

distinct four-line residues, each residue occurring for exactly two triangles.

So already there is an intrinsic two-cover:

\[
540\text{ support-disjointness triangles}\longrightarrow270\text{ four-line residues}.
\]

---

## Pass 4722 — correction: this is exactly the old unnamed 270-class

Pass 1830 found an inner involution class of size 270, with centralizer 192 in the full group, fixing zero W33 points and four pairwise-disjoint W33 lines. It then tried to orbit the four fixed-line indices and reported orbit size 2,880, concluding that the fixed four-line set did not determine the class.

That negative conclusion was produced by an action-domain error.

The old GAP script first defined `G` as a permutation group on the **40 W33 point positions**:

`G := Image(ActionHomomorphism(N, pts, OnLines));`

It then stored `fix` as **indices of W33 lines**, and called:

`Orbit(G, Set(fix), OnSets)`.

Thus the same numbers `1..40` were silently reinterpreted as point labels. That is not the induced action on the 40 W33 lines.

The new verifier constructs the actual induced line action and finds all inner involutions:

\[
\boxed{315=270+45}.
\]

Their fixed-line census is exactly

\[
\boxed{4^{270},\qquad16^{45}.}
\]

The 270 four-fixed-line sets are all distinct and are **exactly** the 270 residues from Pass 4721. Each residue has a unique inner involution, its `PSp(4,3)` stabilizer has order 96, and its orbit has size

\[
25920/96=270.
\]

So the corrected statement is

\[
\boxed{
\{
\text{support-12 triangle residues}
\}
=
\{
\text{four-line fixed sets of the 270 inner involutions}
\}.
}
\]

This closes the explicit “What has size 270?” question left open in Pass 1830.

A literature cross-check found the published global count `I_2(PSp(4,3))=315`, consistent with the internal `270+45` split. The searched sources did not supply this particular W33 fixed-line/support-12 identification; the repository theorem therefore rests on the executable finite model rather than on a literature attribution.

---

## Pass 4723 — the two triangle sheets are the outer order-4 square-root sheets

Fix a residue `R` and let `g` be its unique inner involution. In the full `PGSp(4,3)` action there are exactly eight outer square roots

\[
h^2=g.
\]

All eight have order four. Exactly two of them fix four W33 lines, and those two are the inverse pair

\[
\boxed{h,\;h^{-1}}.
\]

There are exactly two support-disjointness triangles above `R`. Either four-fixing square root swaps those two triangles.

The decisive test is not the count 540. It is the subgroup identity. For either triangle `C` above `R` and either four-fixing root `h`,

\[
\boxed{
\operatorname{Stab}_{PSp(4,3)}(C)
=
C_{PSp(4,3)}(h),
\qquad |\cdot|=48.
}
\]

Consequently the two transitive 540-sets are the same inner-group homogeneous space:

\[
\boxed{
\{540\text{ thickening triangles}\}
\cong_{PSp(4,3)}
\{540\text{ four-fixing outer order-4 elements}\}.
}
\]

There are two equivariant identifications, exchanged by global inversion `h <-> h^{-1}`. In both cases squaring / taking the four-line complement gives the same base:

\[
\begin{array}{ccc}
540\text{ triangles} & \longleftrightarrow & 540\text{ outer }h\\
\downarrow 2{:}1 && \downarrow h\mapsto h^2\;2{:}1\\
270\text{ residues} & = & 270\text{ inner involutions}.
\end{array}
\]

### Outer boundary

The theorem is deliberately stated for `PSp(4,3)`. In the full `PGSp(4,3)` group, the triangle stabilizer and root centralizer both have order 96 but are different subgroups; their intersection is the common inner subgroup of order 48. Thus the full extensions differ by the outer twist. We do **not** claim an untwisted `PGSp`-equivariant identification.

---

## Pass 4724 — the 270 residues factor the complement of the W33 line graph

Let `B` be the `40 x 270` incidence matrix of W33 lines versus the four-line residues. Then:

- every block has size 4;
- every W33 line lies in 27 residues;
- every skew W33 line-pair lies in exactly 3 residues;
- every intersecting line-pair lies in 0 residues.

If `A_*` is the W33 line-intersection graph, this gives the exact matrix identity

\[
\boxed{
BB^T=27I+3(J-I-A_*).
}
\]

Since the complement of `SRG(40,12,2,4)` has eigenvalues `27^1,-3^24,3^15`,

\[
\boxed{
\operatorname{spec}(BB^T)=108^1\oplus18^{24}\oplus36^{15}.
}
\]

Thus `B` has real rank 40. Over `F_2`, the 270 four-line masks span a 30-dimensional subspace:

\[
\boxed{\operatorname{rank}_{\mathbf F_2}B=30.}
\]

That modular rank is recorded as a datum only; no representation name is assigned from dimension alone.

One additional character datum drops out automatically: a representative 270-class involution fixes exactly 24 of the 1,620 support-12 thickenings, hence exactly eight of the 540 disjointness triangles.

---

## Prior-art / repo cross-check boundary

Before promotion this lane was searched against the current support-12, Golay/Leech, D4 triality, 270-class, frame, spread, and code material. The older Pass 1830 file was the key collision: it had already found the correct involution class and the four fixed lines but rejected the invariant because of the point/line action mismatch. The present result is therefore partly a **correction** and partly a genuinely new minimum-shell/square-root-cover theorem.

An external search also confirms that `PSp(4,3)` has 315 involutions in total, while recent work continues to characterize generalized quadrangles with socle `PSp_4(q)` as the classical symplectic family up to duality. Neither external fact supplies the support-12 double cover; they are consistency checks, not proof substitutes.

## Evidence boundary

Everything above is finite geometry, permutation-group theory, and binary-code incidence. No physical particle, field, lattice, or dynamical interpretation is inferred. The 540/270 counts are promoted only after explicit support maps, fixed sets, square maps, stabilizers, centralizers, and the Gram factorization are verified.
