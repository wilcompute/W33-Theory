# Pass7701-7740 — H27 Fourier sector, corrected Leech duality, polarization moduli, and common-code weld

## Status

All finite statements below are certificate-backed.  The Leech order-9 quotient is **not** `F3^6`; Pass7645 proved

\[
C=\operatorname{coker}(1-g)\cong (\mathbb Z/3)^2\oplus(\mathbb Z/9)^2.
\]

Pass7653 then proved that the standard unimodular linking form gives a perfect pairing

\[
(C/3C)\times C[3]\longrightarrow \mathbb F_3,
\]

so the corrected Leech object has two canonical 40-point projective boundary layers in point-hyperplane duality for `PG(3,3)`.  Nothing in this packet revives the refuted 364-point `PG(5,3)` claim.

## 1. H27 Fourier decomposition of the local Steinberg V20 — Pass7701-7708

The 27-point rank-4 scheme found in Pass7629-7644 is exactly the Cayley partition of the qutrit Heisenberg group `H27`:

- identity: 1 element;
- `Z(H27)\{1}`: 2 elements, giving `9 K3`;
- a 16-element connection set, giving the Schläfli graph `SRG(27,16,10,8)`;
- the 8 horizontal elements `(u,0), u != 0`, giving the repo H27 distance-regular Cayley graph.

The Heisenberg group has nine linear characters and two degree-3 irreducibles.  The local Steinberg Gram operator has image

\[
V_{20}=V_8^{\rm lin}\oplus V_6^{(\omega)}\oplus V_6^{(\omega^2)},
\]

and kernel

\[
\mathbf 1\oplus V_3^{(\omega)}\oplus V_3^{(\omega^2)}.
\]

Thus the exact `20=8+6+6` split is a finite Fourier/Schrödinger decomposition, not a particle assignment.

Certificate: `data/PART_W33_PASS7701_7708_H27_FOURIER_V20.json`.

## 2. Leech dual-40 polarity closure test — Pass7709-7716

Pass7653 already owns the canonical dual `PG(3,3)` interface.  Pass7709 independently verifies the design parameters and adds the exact W33 closure test: after choosing an alternating polarity that identifies top with socle, the 40x40 cross-incidence matrix is

\[
N=I+A_{W(3,3)},
\]

so removing the diagonal gives `SRG(40,12,2,4)`.

This does **not** select a polarity from the Leech operator.  It isolates that missing identification as the exact remaining geometric obstruction.

Certificate: `data/PART_W33_PASS7709_7716_LEECH_DUAL40_PROJECTIVE_POLARITY.json`.

## 3. The Leech interface carries the PG(3,3) ternary design code — Pass7717-7724

The row span over `F3` of the 40x40 point-hyperplane incidence matrix has rank 11 and exact parameters

\[
[40,11,13]_3.
\]

Exhaustive enumeration gives weight enumerator

\[
1+80x^{13}+1560x^{18}+20280x^{22}+21060x^{24}+33696x^{25}+18800x^{27}
 +42120x^{28}+16848x^{30}+21840x^{31}+780x^{36}+82x^{40}.
\]

A weighted-column dependency search proves the dual has parameters

\[
[40,29,6]_3
\]

with 6240 minimum-weight words (3120 projectively).  These abstract code parameters are published prior art; the new repo bridge is their exact occurrence on the corrected Leech top-to-socle linking interface.

Certificate: `data/PART_W33_PASS7717_7724_LEECH_DUAL40_TERNARY_CODE.json`.

## 4. The 234 W33 choices have a 117+117 moduli geometry — Pass7725-7732

Pass5744-5751 already established that there are 234 symplectic W33 overlays on the fixed `PG(3,3)` carrier.  Pass7725 refines that old count.

There are 468 nondegenerate alternating forms on `F3^4`, hence 234 projective forms modulo `+-1`.  The Pfaffian is unchanged by projective scaling in dimension four and splits these into two families of 117.

For two polarities, compare the edge sets of their two labelled W33 graphs.  The intersection size takes exactly

\[
60,\quad 78,\quad 96,
\]

with global subdegrees `108,80,45`.  Inside either Pfaffian family, the overlap-96 relation is

\[
\operatorname{SRG}(117,36,15,9),
\]

and overlap-78 is its complement `SRG(117,80,52,60)`.  Across the two 117-families, overlap 96 gives a 45-regular bipartite relation with singular spectrum `45^1+6^90+0^26`.

The abstract `(117,36,15,9)` graph is known from the rank-3 `L4(3):2` action with point stabilizer `U4(2):2`.  Here it is realized objectwise as the moduli graph of W33 polarizations on the same 40-point carrier.  The stabilizer of one projective alternating form is

\[
PGSp_4(3)\cong W(E_6),\qquad |PGSp_4(3)|=51840,
\]

and `|PGL4(3):PGSp4(3)|=234`.

Certificate: `data/PART_W33_PASS7725_7732_SYMPLECTIC_POLARITY_MODULI_117.json`.

## 5. Main weld: the Leech code is polarization-independent — Pass7733-7740

Let `A` be the adjacency matrix for any one of the 234 W33 polarities and put

\[
N=I+A,\qquad Q=J-I-A.
\]

The W33 SRG identity reduces mod 3 to

\[
\boxed{N^2=J.}
\]

Therefore the ternary row space of `Q` is the sum-zero core of the row space of `N`.  Direct verification across **all 234** polarities gives two fixed code spaces independent of the chosen overlay:

\[
\operatorname{row}_{\mathbb F_3}(N)=C_{11},\qquad
\operatorname{row}_{\mathbb F_3}(Q)=C_{10},
\]

with

\[
C_{11}=\langle\mathbf 1\rangle\perp C_{10},
\]

where

\[
C_{11}=[40,11,13]_3,
\qquad
C_{10}=[40,10,18]_3.
\]

The `C10` space is exactly the quadratic/Veronese code already identified in Pass5744-5751; it is self-orthogonal and has weight enumerator

\[
1+1560x^{18}+21060x^{24}+18800x^{27}+16848x^{30}+780x^{36}.
\]

### Consequence

The corrected Leech order-9 bridge reaches the **common W33 ternary code layer canonically even before a W33 polarity is selected**.  The unresolved 234-fold ambiguity lives at the incidence/geometry overlay level, not at the underlying code-space level.

This is the principal breakthrough of the packet.

Certificate: `data/PART_W33_PASS7733_7740_LEECH_QUADRATIC_CODE_WELD.json`.

## Evidence boundary

- Exact: finite groups, projective geometry, Cayley schemes, code ranks/weights, all-234 overlay invariance.
- Prior art retained explicitly: the abstract `[40,10,18]_3`, `[40,11,13]_3`, `[40,29,6]_3` codes; the existence of 234 W33 overlays from Pass5751; the abstract rank-3 `SRG(117,36,15,9)`.
- New repo welds: H27 Fourier realization of V20; Pfaffian 117+117 polarization moduli and edge-overlap geometry; Leech dual-interface transport to the ternary codes; and the polarity-independent identity `C_Leech=<1> perp C_quad`.
- Open: a canonical Leech/Co0-equivariant alternating identification `C/3C -> C[3]`.  Until that exists, the Leech construction does not canonically select one W33 graph.
- No Monster VOA, Griess-algebra, Standard-Model, or hardware claim follows from this packet.
