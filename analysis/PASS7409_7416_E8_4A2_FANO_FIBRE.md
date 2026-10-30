# Passes 7409–7416 — E8 4A2 Orientation Fibre = Fano-Hinge W(D4) Chart

## Status

**THEOREM-GRADE / machine verified.**

Verifier: `analysis/w33_pass7409_7416_e8_4a2_fano_fibre.py`

Certificate: `data/PASS7409_7416_E8_4A2_FANO_FIBRE_results.json`

## The local question

Passes 7401–7408 prove that every A2^4 line of E8 belongs to exactly

\[
\boxed{8}
\]

Eisenstein W(3,3) leaves.

Why eight?

Fix

\[
X=A_2^{(1)}\perp A_2^{(2)}\perp A_2^{(3)}\perp A_2^{(4)}.
\]

On each A2 factor, a fixed-point-free order-three complex structure has two Coxeter orientations, c_i or c_i^{-1}. So an oriented product is encoded by four bits.

There are initially 2^4=16 sign choices, but a W33 leaf depends on the cyclic subgroup <J>, not on the choice of generator. Replacing J by J^{-1} flips all four signs:

\[
x\sim x+1111.
\]

Therefore the fibre is exactly

\[
\boxed{\mathbb F_2^4/\langle1111\rangle,}
\]

which has eight elements.

The global double count from Pass 7406 says there are exactly eight leaves through X, so these eight orientation classes are all of them.

## Explicit Fano coordinates

There is a canonical gauge map

\[
\boxed{[x_1,x_2,x_3,x_4]\mapsto(x_1+x_4,x_2+x_4,x_3+x_4)}
\]

from F2^4/<1111> to F2^3.

The parity functional is well-defined because 1111 has even weight. The seven nonzero directions split as 4+3.

Odd directions:

\[
\boxed{100,\ 010,\ 001,\ 111.}
\]

Even directions:

\[
\boxed{110,\ 101,\ 011.}
\]

This is exactly the project's existing Fano-hinge split.

## The group action

The reflection subgroup of the four A2 factors has order

\[
|W(A_2)^4|=6^4=1296.
\]

Its four factor reflections independently invert the four Coxeter orientations. After quotienting simultaneous inversion, their image is the translation group

\[
\boxed{2^3}.
\]

The kernel of this internal action is

\[
\boxed{1296/8=162=3^4\cdot2.}
\]

The normalizer of A2^4 in W(E8) has order

\[
\boxed{|N_{W(E_8)}(A_2^4)|=696729600/11200=62208.}
\]

Hence the extendable outer quotient has order

\[
\boxed{62208/1296=48.}
\]

This is the same order-48 tetracode glue stabilizer already audited in BT1845/BT1864. Those passes transported its projective block quotient S4 of order 24 but explicitly left the local A2/Weyl lift open.

Combining the local orientation translations with that S4 gives

\[
\boxed{2^3:S_4}
\]

of order

\[
\boxed{192}.
\]

This is the Weyl group

\[
\boxed{W(D_4).}
\]

The full A2^4 normalizer acts on the eight leaves with kernel

\[
\boxed{62208/192=324.}
\]

Equivalently:

\[
\boxed{1\to K_{324}\to N_{W(E_8)}(A_2^4)\to W(D_4)\to1.}
\]

The stabilizer of one leaf in the 192-image has order 24.

## The K4,4 / Fano-hinge graph drops out automatically

Use the four odd directions as a Cayley generating set on the eight-element fibre.

Each odd direction is a perfect matching with four edges, and the four matchings are disjoint. Their union is

\[
\boxed{K_{4,4}},
\]

with parity as the 4+4 bipartition.

Thus the four odd directions give a canonical one-factorization:

\[
\boxed{K_{4,4}=M_{100}\sqcup M_{010}\sqcup M_{001}\sqcup M_{111}.}
\]

The three even directions give three more perfect matchings whose union is

\[
\boxed{2K_4}.
\]

Therefore the complete graph decomposes as

\[
\boxed{K_8=K_{4,4}\sqcup2K_4.}
\]

This is precisely the combinatorics that the earlier Fano-hinge codec work found abstractly on the eight antipodal Q4 axes.

## The new weld

The earlier repo chain had already proved F2^3 + 4 odd directions + 3 even directions + K4,4 + 2^3:S4 for the Fano-hinge/tomotope chart.

What it did **not** have was an E8 derivation of that chart.

Now it does:

\[
\boxed{\text{eight Eisenstein W33 leaves through one }A_2^4\cong\mathbb F_2^4/\langle1111\rangle\cong\mathbb F_2^3.}
\]

Under that identification,

\[
\boxed{N_{W(E_8)}(A_2^4)/K_{324}\cong W(D_4)\cong2^3:S_4,}
\]

and the four odd leaf-difference directions one-factorize the same K4,4.

So the recurring project number

\[
\boxed{192}
\]

now has a direct E8 origin:

\[
\boxed{192=\text{the induced symmetry of the 8-leaf Eisenstein fibre over }A_2^4.}
\]

## Prior-art / rediscovery boundary

BT1845 already found the transported tetracode S4 quotient of order 24.

BT1864 upgraded the glue stabilizer to order 48 and explicitly said the “local A2/Weyl/glue stabilizer refinement” remained open.

The Fano-hinge affine theorem already had an abstract 2^3:S4 group of order 192 on F2^3.

**New here is the missing bridge between those two older results:** the local A2 reflections supply the 2^3 translation subgroup, while the tetracode block quotient supplies S4, and the eight objects acted on are exactly the eight Eisenstein W(3,3) leaves through one real A2^4 subsystem of E8.

## External references checked

- Y. H. Park, *Automorphism group of the ternary tetracode*, Korean J. Math. 17 (2009), 487–493: |Aut(T)|=48 with explicit signed-coordinate generators.
- Classical W(E8) reflection-subgroup census: 11200 A2^4 subsystems.
- Reeder/Springer order-three Eisenstein structure for E8.

## Evidence boundary

The theorem is a statement about the finite E8 root system, its A2^4 normalizer, and an explicit eight-element orientation fibre.

The phrase “same Fano-hinge chart” means an explicit isomorphism of the F2^3 affine action and its 4+3 Cayley relations. It does not by itself identify a physical tomotope, optical device, or spacetime degree of freedom with an E8 subsystem.
