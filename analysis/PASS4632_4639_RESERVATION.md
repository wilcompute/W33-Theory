# Passes 4632--4639 execution ledger

All five queued attacks and three outside-box probes were executed on `master`.  This range was originally reserved before later 4640--4655 parallel lanes; integration was therefore performed after re-fetching the live manuscript/public surfaces, without overwriting those later-numbered packets.

## Pass 4632 -- periodic homology module separation

For the Pass4575 two-periodic binary incidence complex,

- `H36 = ker(R)/im(R^T)` has dimension 24;
- `H27 = ker(R^T)/im(R)` has dimension 15.

The point-side 40-object W33 carrier reconstructed from the compatible-F4 structures has binary adjacency rank 16, giving comparison layers

- `Q24 = F2^40/row(A)`;
- `Q15 = row(A)/<1>`.

Exact PSp(4,3)-equivariance equations give one-dimensional Hom spaces in all four directions, but the unique nonzero maps have ranks

- H36 -> Q24: 9;
- Q24 -> H36: 1;
- H27 -> Q15: 14;
- Q15 -> H27: 1.

Thus the equal-dimensional modules are not isomorphic.  The result replaces a dimension coincidence with an explicit shared-subquotient/extension separation theorem.

## Pass 4633 -- corrected Golay sextet and exact M24 section stabilizer

Re-executing the Pass4615 720-match search found that its historical frozen JSON was stale.  The corrected unique zero-coordinate assignment is

`(21,20,19,18,22,17)`

with tetrads

`(0,2,7,21), (1,6,16,20), (3,4,13,19), (5,8,18,23), (9,11,14,22), (10,12,15,17)`.

The stale Pass4615 JSON was repaired on master.

Conjugating the standard 24-point M24 generators into the repository Golay coordinates and using exact Schreier orbit/stabilizer computation gives

- M24 order from orbit/stabilizer: 244,823,040;
- sextet orbit: 1,771;
- sextet stabilizer: 138,240;
- action on six tetrads: S6 of order 720, kernel 192.

The actual six-zero-coordinate transversal has orbit 64 inside the sextet.  Its stabilizer K has order 2,160.  K is faithful and transitive on the 18 active coordinates and on the 45 section octads; its section-codeword orbits are 1+18+45.

## Pass 4634 -- complete support-11 apartment-code census

The native XOR/popcount engine exhaustively evaluated

`C(40,11) = 2,311,801,440`

support-11 coefficient subsets.  There are exactly 153 weights.  The minimum is 614 with multiplicity 12,960; the maximum is 1,026 with multiplicity 1,080.  The complete 153-entry histogram is frozen in the result JSON.

Complete labelled support spectra are now exact through support 11.  Supports 12--20 and the complete 2^39 numerical enumerator remain OPEN.

## Pass 4635 -- six-signature primitive-C8 collision criterion

Every four-line apartment contribution to primitive C8 degree four falls into exactly four local line-multiplicity signatures:

- `1111|22`;
- `1115|`;
- `1133|`;
- `1111|4`.

Every K1,3 contribution falls into exactly two:

- `1111|22`;
- `1113|2`.

The primitive coefficient is one eighth of the raw signature mass, so collision is exactly equality of the four apartment masses and two star masses.

Exact anchors:

- GQ(2,2): apartment `224+64`, star `96+192`; both total 288, hence 36=36;
- GQ(2,4): 60 versus 36;
- GQ(4,2): 2812 versus 792;
- W33=GQ(3,3): 712 versus 180.

This explains the GQ(2,2) failure as cancellation between different walk species.  Closed arbitrary-(s,t) formulas for the six masses remain OPEN.

## Pass 4636 -- Construction-A Golay/Leech obstruction

For `L(C)=(1/sqrt(2)){x in Z^24 : x mod 2 in C}`:

- det L(C6) = 2^12 = 4096;
- det L(G24) = 1;
- `[L(G24):L(C6)] = |G24/C6| = 64`.

Both lattices retain exactly 48 norm-2 coordinate roots.  Therefore the 64-coset glue reaches the rooted A1^24 Niemeier Construction-A lattice, not rootless Leech.  A further neighbor/shift/holy-construction step is genuinely required.

## Pass 4637 -- outside box: sextet transversals are the section codewords

Under K, the selected 64 sextet transversals and the 64 C6 codewords both split as 1+18+45.  Stabilizer-fixed-point tests leave exactly one equivariant map on the 18-orbits and exactly one on the 45-orbits, with the chosen zero transversal forced to the zero word.  Therefore there is a unique K-equivariant bijection, transporting the C6 XOR law to an F2^6 affine structure on that 64-transversal orbit.

## Pass 4638 -- outside box: Golay glue is the six-tetrad permutation module

The six-dimensional quotient G24/C6 has K-image order 720 and kernel order 3, exactly as the six-tetrad permutation action.  The full intertwiner space has dimension 2; its three nonzero maps have ranks 1,6,6.  Thus two full-rank K-equivariant isomorphisms identify the 64 Construction-A glue cosets with the binary six-tetrad permutation geometry.

## Pass 4639 -- outside box: 63-point double-differential cancellation

On all 63 nonzero vectors of U6, split the polar matrix into cross-shell `D0` and within-shell `Delta`.  Both are commuting square-zero maps of rank 12 and have the same 12-dimensional image.  Their characteristic-two sum is the full polar matrix of rank 6.

The homology dimension therefore jumps from

`63 - 2*12 = 39`

to

`63 - 2*6 = 51`.

The full row code is the [63,6,32] simplex code, so the resulting CSS code is `[[63,51,3]]`.

## Release state

- executable verifiers and frozen JSON certificates are on `master`;
- the stale Pass4615 sextet JSON is repaired;
- the shared theorem insert is wired into `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex` after the already-live 4648--4655 packet;
- the public card/page are registered through the safe extension manifest; `docs/index.html` is not directly overwritten;
- focused regression tests and an exact regeneration workflow are installed;
- the support-11 job is kept as its own exhaustive workflow job rather than being replaced by a small-shell smoke test.

Evidence boundaries remain fail-closed: equal dimensions are not module identities; the full enumerator is open beyond support 11; all-(s,t) C8 mass formulas are open; the Construction-A endpoint is explicitly not Leech; and none of the finite code/group/lattice theorems is promoted to a physical identification.
