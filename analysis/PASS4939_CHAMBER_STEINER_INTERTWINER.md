# Pass 4939 — the Steiner 24-space is explicitly the chamber line lane

## Result

This pass closes a gap that dimension counts could not close.  The rank-24
Steiner fiber-constant sector from Pass 4874 and the rank-24 chamber line lane
from Pass 4936 were originally joined under an unresolved point/line label.
Pass 4949's characteristic-three fingerprint fixes that label: the Steiner
quotient is the \(Q(4,3)\) line carrier.  The corrected explicit maps are

\[
F_{S\leftarrow L}=\frac14L_SP_{24}^{(\ell)}L_\ell^{\mathsf T},\qquad
F_{L\leftarrow S}=\frac13L_\ell P_{24}^{(\ell)}L_S^{\mathsf T},
\]

where

\[
P_{24}^{(\ell)}=-\frac1{60}(A_\ell-12I)(A_\ell+4I).
\]

Here \(L_S\) is the \(120\times40\) lift from the forty three-element
Steiner fibers and \(L_\ell\) is the \(160\times40\) lift from incident
chambers to their W33 lines.  Their Gram factors are exactly

\[
L_S^{\mathsf T}L_S=3I,\qquad L_\ell^{\mathsf T}L_\ell=4I.
\]

The native GAP witness proves

\[
\operatorname{rank}F_{S\leftarrow L}
=\operatorname{rank}F_{L\leftarrow S}=24
\]

and the stronger partial-inverse identities

\[
F_{L\leftarrow S}F_{S\leftarrow L}=Q_L,\qquad
F_{S\leftarrow L}F_{L\leftarrow S}=Q_S,
\]

where

\[
Q_L=\frac14L_\ell P_{24}^{(\ell)}L_\ell^{\mathsf T},\qquad
Q_S=\frac13L_SP_{24}^{(\ell)}L_S^{\mathsf T}.
\]

Thus this is an object-level isomorphism on the projected carriers, not a
coincidence between two ranks.

## Exact reconstruction

The GAP owner does not begin from an abstract three-copy model.  It rebuilds
the actual finite chain:

- the \(27+36\) singular/nonsingular points of the six-dimensional minus
  quadratic space over \(\mathbb F_2\);
- the 72 sixers and 36 double-sixes;
- the 120 Steiner triangles;
- the four PSp pair orbits of sizes \(120,1620,2160,3240\);
- the intrinsic \(40\times3\) fibers and their 2,160-pair adjacency lift;
- the quotient \(Q(4,3)\) line-intersection graph;
- its forty maximal \(K_4\) point pencils and 160 incident line-point
  chambers.

The bare partition into forty Steiner triads is classical and remains credited
to the Frame-era cubic-surface literature through Pass 4870.  Pass 4870 owns
the quotient identification with \(W(3,3)\); Pass 4949 owns its corrected
line-side orientation.  Pass 4939 adds the rational transport maps.

## Point-line orientation firewall

The line graph and reconstructed point graph are both
\(\operatorname{SRG}(40,12,2,4)\), both have group orders 25,920 and 51,840,
both have subdegrees \(1,12,27\), and both split rationally as
\(1\oplus24\oplus15\).  None of those invariants can orient the carrier.

The exact separator is modular.  Over \(\mathbb F_3\), put \(N=A+I\).  On
the Steiner quotient line carrier GAP obtains

\[
\operatorname{rank}N=15,\qquad \operatorname{rank}N^2=1,
\qquad 14\mid11\mid14
\]

on the 39-dimensional augmentation.  Reconstructing the forty maximal
\(K_4\) pencils and joining pencils that share a line gives the W33 point
carrier, where

\[
\operatorname{rank}N=11,\qquad \operatorname{rank}N^2=1,
\qquad 10\mid19\mid10.
\]

Thus the two 40-point actions are not the same modular carrier.  The explicit
Steiner transport targets \(Q_L\), the chamber **line** lane; it does not
identify the Steiner sector with the chamber point lane.

## Equivariance and uniqueness

The witness transports a native generating set of \(PSp(4,3)\), together with
one outer \(PGSp/PSp\) generator, through the 120 Steiner triangles, forty
line fibers, forty point pencils, and 160 chambers.  Both maps intertwine every
one of those generators.  The induced group orders are

\[
|PSp(4,3)|=25920,\qquad |PGSp(4,3)|=51840.
\]

The PSp quotient action has subdegrees \(1,12,27\).  Its rational permutation
module has the three distinct primitive sectors

\[
1\oplus24\oplus15.
\]

The witness now verifies the common-sector commutant directly rather than
inferring it from the rank-three decomposition.  It restricts the native PSp
generators and the outer PGSp generator to \(\operatorname{im}P_{24}\), writes
all \(24^2=576\) rational endomorphism variables, and forms the three blocks
of commutator equations.  There are 1,728 scalar equations.  Their reduction
modulo the good prime 101 has rank 575.  Reduction cannot increase rational
rank, while the rational scalar identity is explicitly in the kernel, so

\[
575\leq \operatorname{rank}_{\mathbb Q}\mathcal C\leq575.
\]

Thus the rational centralizer has dimension \(576-575=1\), with the identity
as its scalar basis.  Since the displayed equivariant maps are mutual partial
inverses on the two projected carriers, their common Hom space is likewise
one-dimensional.  Therefore the nonzero equivariant intertwiner is unique up
to rational scalar; the normalizations \(1/4\) and \(1/3\) are forced by the
two fiber sizes and make the displayed partial inverses exact.  The
rank-three split \(1\oplus24\oplus15\) is now a consistency check, not the
owner of the one-dimensionality claim.

The literal solve proves uniqueness on the corrected line lane.  Combining
that lane with Pass 4936's certified \(M_2(\mathbb Q)\) multiplicity algebra
then gives the scoped packet identity

\[
\boxed{
\text{Pass 4936 rank-48 packet}
\cong V_{24}^{\mathrm{Steiner}}\otimes\mathbb Q^2
}
\]

The first copy here is explicitly the chamber line lane; the second is supplied
by the already-certified matrix unit carrying it to the other packet corner.
The Pass 4870 quotient identification remains unique only up to PGSp, and no
preferred labeling of the three members in each Steiner fiber is introduced.

## Evidence

- GAP owner: `analysis/w33_pass4939_chamber_steiner_intertwiner.g`
- Frozen certificate:
  `data/PART_W33_PASS4939_CHAMBER_STEINER_INTERTWINER.json`
- Regression: `tests/test_w33_pass4939_chamber_steiner_intertwiner.py`
- Native result: `24/24 checks; status=PASS`

## Boundary

The theorem is finite and rational, and it concerns only the fiber-constant
24-dimensional Steiner sector and the chamber line lane.  It explicitly does
not identify the line and point carriers; their characteristic-three
augmentation filtrations differ.  It does not touch the transverse \(20+60\)
sector, intertwine any individually charted HP/HL selector, implement a
HoloBox state transfer, or imply a continuum field, particle, mass, coupling,
or security property.
