# Pass 4936 — Chamber packet matrix units and the HoloBox family checksum

## Result

The rank-48 chamber packet from Passes 4324 and 4334 is not merely a
four-dimensional Clifford-like algebra with two isoclinic rank-24 carriers.
It is now split explicitly over the rationals:

\[
\boxed{\mathcal A_{48}\cong M_2(\mathbb Q)}.
\]

The isomorphism is witnessed by four literal `160 x 160` rational matrices
that satisfy every matrix-unit product.  On the packet representation this is
one two-state multiplicity algebra repeated on 24 representation lanes.  It is
not a claim that the repository has constructed 24 physical qubits.

The same certificate supplies a precise, limited bridge to HoloBox.  Summing
the three deterministic `HP` transitions, or the three deterministic `HL`
transitions, removes their chart-dependent selector labels.  After compression
to the packet and one affine normalization, those two family sums are exact
involutions in the matrix algebra.  This is a selector-family checksum, not an
intertwiner for any one opcode.

## Inputs owned by earlier passes

[Pass 4324](w33_pass4324_4327_chamber_hecke_hashimoto.g) constructs the chamber
panel matrices \(P,L\), the rank-48 projector

\[
\Pi=\Pi_{48}=-\Omega^2/60,
\qquad \Omega=LP-PL,
\]

and the four-dimensional packet basis

\[
\{\Pi,X,\Omega,X\Omega\},
\qquad X=(P+L-2I)\Pi,
\]

with exact relations

\[
X^2=6\Pi,
\qquad \Omega^2=-60\Pi,
\qquad X\Omega=-\Omega X.
\]

[Pass 4334](w33_pass4334_point_line_chiral_carrier.g) constructs the literal
point and line projectors \(Q_p,Q_\ell\), each of rank 24, and proves

\[
Q_pQ_\ell Q_p=\frac38Q_p,
\qquad
Q_\ell Q_pQ_\ell=\frac38Q_\ell,
\qquad
\operatorname{im}\Pi=\operatorname{im}Q_p\oplus
\operatorname{im}Q_\ell.
\]

The direct sum is a zero-intersection sum, not an orthogonal sum.

## The carriers inside the old packet basis

Exact GAP coordinate solving gives

\[
\boxed{
Q_p=\frac12\Pi+\frac18X+\frac1{48}X\Omega,
\qquad
Q_\ell=\frac12\Pi+\frac18X-\frac1{48}X\Omega.}
\]

Thus the object-level point/line carriers of Pass 4334 live inside exactly the
same four-dimensional algebra as the operators of Pass 4324.  The combined
flattened matrix family has rank four; no larger algebra was silently added.

## Literal rational matrix units

Put

\[
e_{11}=Q_p,
\qquad e_{22}=\Pi-Q_p,
\]

\[
e_{21}=(\Pi-Q_p)Q_\ell Q_p,
\qquad
e_{12}=\frac{64}{15}Q_pQ_\ell(\Pi-Q_p).
\]

The normalization follows from

\[
\frac38\left(1-\frac38\right)=\frac{15}{64}.
\]

GAP checks all sixteen products

\[
\boxed{e_{ij}e_{k\ell}=\delta_{jk}e_{i\ell}}.
\]

In the old packet basis the two off-diagonal units are

\[
e_{12}=\frac{10X-4\Omega-X\Omega}{30},
\qquad
e_{21}=\frac{10X+4\Omega-X\Omega}{128}.
\]

Consequently

\[
N_+=10X+4\Omega-X\Omega,
\qquad
N_-=10X-4\Omega-X\Omega
\]

are a literal nilpotent pair:

\[
N_+^2=N_-^2=0,
\qquad
N_-N_+=3840e_{11},
\qquad
N_+N_-=3840e_{22}.
\]

This is the decisive split-algebra witness.  It is stronger than recognizing
the abstract four-dimensional multiplication table because it names primitive
corners and normalized cross maps on the actual chamber carrier.

## Exact two-state switch algebra

Define

\[
Z=e_{11}-e_{22},
\qquad S=e_{12}+e_{21}.
\]

Then

\[
\boxed{Z^2=S^2=\Pi,\qquad ZS=-SZ,\qquad (SZ)^2=-\Pi.}
\]

Here \(Z\) tags the two rational corners and \(S\) exchanges them.  This is an
exact algebraic logic switch on the multiplicity coordinate.  The rational
normalization is not orthogonal; an orthonormal cross-map would require a
square root.  No unitary-gate or hardware-cost claim is made.

## HoloBox: what the checksum proves

The HoloBox chamber ISA uses the six panel-transition labels

```text
HP0 HP1 HP2  HL0 HL1 HL2
```

with the checked-in lexicographic choice of the three alternatives.  In the
GAP witness, let \(S_{HP,i}\) and \(S_{HL,i}\) be their deterministic `0/1`
transition matrices.  The individual matrices depend on the chosen chart, but
their sums do not:

\[
S_{HP,0}+S_{HP,1}+S_{HP,2}=P,
\qquad
S_{HL,0}+S_{HL,1}+S_{HL,2}=L.
\]

Compress and normalize those family sums:

\[
H_p=\frac{\Pi P\Pi-\Pi}{2}=2Q_p-\Pi,
\qquad
H_\ell=\frac{\Pi L\Pi-\Pi}{2}=2Q_\ell-\Pi.
\]

GAP proves

\[
H_p^2=H_\ell^2=\Pi,
\qquad
H_pH_\ell+H_\ell H_p=-\frac12\Pi.
\]

Therefore a verifier can compare the complete `HP` family or complete `HL`
family against an intrinsic packet operator without preserving the arbitrary
selector numbers.  That is the exact HoloBox connection established here.

It does **not** show that any individual `HPi` or `HLi` transition preserves the
packet, nor does it add a guest instruction to
[`w33_fractal_microvm_runtime.py`](w33_fractal_microvm_runtime.py).  The runtime
also contains `ADD`, `RECV`, `YIELD`, and `HALT`; none of those operations is
modeled by this algebra.  Applying the checksum independently at any resolved
recursive address is possible because every HoloBox state contains a chamber,
but a recursive-network functor or compositional checksum law has not been
constructed.

## The aggregate turn has infinite order

Let

\[
T=H_pH_\ell.
\]

Exact arithmetic gives

\[
\boxed{2T^2+T+2\Pi=0},
\]

and, on the full 160-dimensional chamber space,

\[
\chi_T(t)=t^{112}\left(t^2+\frac12t+1\right)^{24},
\qquad
\operatorname{rank}T=48,
\qquad
\operatorname{tr}T=-12.
\]

On \(\operatorname{im}\Pi\), the quadratic factor has discriminant
\(-15/4\), so it is irreducible over \(\mathbb Q\).  Its roots are not
algebraic integers: their irreducible monic polynomial has the nonintegral
coefficient \(1/2\).  They therefore cannot be roots of unity.  The aggregate
turn has infinite order on the packet.

This is an important negative boundary: the two family reflections do not hide
a finite opcode clock.

## Prior art and ownership

- Pass 4324 owns the four-dimensional chamber packet and its
  \(X,\Omega\) relations.
- Pass 4334 owns the literal point/line rank-24 carriers and their squared
  isoclinic cosine \(3/8\).
- [Pass 4777](w33_pass4777_matrix_units_outer.py) already constructed literal
  rational matrix units in a different rank-40 residue-orbital block.  Pass
  4936 applies that matrix-unit style to the chamber packet; it is not the
  repository's first use of the method.
- Relations of the form \(PQP=\tau P\) are standard in projection
  representations of Temperley--Lieb algebras; see
  [arXiv:1503.06461](https://arxiv.org/abs/1503.06461).  No literature-priority
  claim is made for the general two-projection mechanism.

The repository-specific advance is the exact object-level identification:
the Pass 4334 W33 point/line carriers split the Pass 4324 chamber packet, and
the HoloBox selector-family sums land on the resulting rational reflections.

## Falsifiers frozen by the witness

The claim fails if any of the following occurs:

1. the old packet basis and the four proposed matrix units span more than four
   dimensions;
2. any one of the sixteen matrix-unit products fails;
3. either nilpotent square or either factor-3840 product fails;
4. the three deterministic selector matrices do not sum to their panel
   adjacency matrix;
5. either compressed family sum differs from its stated reflection;
6. the turn fails its quadratic, rank, trace, inverse-in-the-corner, or exact
   characteristic polynomial.

All six falsifier classes are included among the 20 exact checks.

## Reproduce

```console
gap -q analysis/w33_pass4936_chamber_packet_matrix_units.g
pytest -q tests/test_w33_pass4936_chamber_packet_matrix_units.py
```

Expected GAP status:

```text
Pass 4936 chamber packet matrix units: 20/20 checks; status=PASS
```

The pytest regression executes GAP in an isolated temporary directory and
requires the regenerated certificate to match
[`PART_W33_PASS4936_CHAMBER_PACKET_MATRIX_UNITS.json`](../data/PART_W33_PASS4936_CHAMBER_PACKET_MATRIX_UNITS.json)
byte for byte.

## Evidence boundary

This is an exact finite rational matrix theorem and a selector-family aggregate
checksum.  It proves no individual-selector intertwiner, deterministic HoloBox
guest-state update, recursive composition law, operating-system isolation,
security property, physical qubit, laboratory implementation, continuum
limit, particle, mass, or coupling identification.
