# Passes 338--342: Selector Frame, Clifford Carrier, and Cohomological Obstruction

This packet executes the five live boundaries left by Passes 333--337.  Every
finite calculation is owned by GAP; Python only reruns the witnesses and reads
their JSON certificates.  The results strengthen the selector/lattice bridge
while removing three attractive but false identifications.

## Dependency and ownership

- Pass 334 already proved that the 120-sheet selector is the curved bundle
  `G/H -> G/K`, not the flat product of forty lines with three lattice leaves.
- Pass 335 already built the five-vertex local 2-adic complex and the two
  invariant plus refinements on each H10 leaf.
- Pass 336 already built the two integral rank-32 half-spin lattices and the
  Smith diagonal `1^16,3^16`.
- Pass 337 already separated the split dual-number deck from the nonsplit
  signed-E8 central extension.

The present packet builds the missing objects rather than repeating those
counts.

## Pass 338 -- the principal selector-frame 240-cover

The actual W(3,3) line action is the ATLAS `p40b` action of `U4(2).2`.  Its line
stabilizer has the unique chain

```text
|G| = 51840  >  |K| = 1296  >  |N| = 216,
K/N = S3.
```

The coset action `G/N` is faithful and transitive of degree 240.  It is a
principal `S3` cover of the forty W(3,3) lines, with rank 13 and subdegrees

```text
1^6, 27^6, 72.
```

Its three index-two block systems give three degree-120 quotients, each with
selector subdegrees `1,2,27,36,54`.  The index-three block system gives a new
degree-80 refinement-parity quotient with full subdegrees `1,1,24,27,27`; the
inner `U4(2)` splits the 24 into `12+12`.

This is not the signed-E8 action.  The ATLAS signed degree-240 action has rank 6,
subdegrees `1,1,4,54,72,108`, and its forty hexads lie over the nonconjugate
`p40a` action.  The obstruction therefore appears already at the forty-object
base, before the different local fibres and central extensions are compared.

On the six refined lattice states, the direct integral outer action is `3+3`.
The simultaneous refinement flip is central, and twisting odd elements by that
flip produces the regular `S3` fibre.  This explains exactly which extra bit is
needed to pass from the integral leaf action to the selector frame.

## Pass 339 -- the 32-dimensional Clifford carrier

GAP constructs the real five-qubit Pauli group

```text
E = <X_1,...,X_5,Z_1,...,Z_5> = 2_+^(1+10).
```

Its exact ledger is

```text
|E| = 2048,
|Z(E)| = |E'| = |Phi(E)| = 2,
exponent = 4,
square-one elements = 1056,
trace distribution = {-32^1, 0^2046, 32^1}.
```

The trace inner product is one.  Since the abelianization has order 1024, the
remaining character degree is uniquely `sqrt(2048-1024)=32`.  Independently,
the actual H10 action is faithful `U4(2)` on a nondegenerate plus-type
10-space, with exactly two invariant refinements and 528 zeros each.

These are the two sides of the finite Stone--von Neumann/Clifford lift:

```text
2_+^(1+10)  ->  Clifford(H10,q)  ->  O^+(10,2).
```

Pulling back along `U4(2) < O^+(10,2)` supplies the canonical projective
32-dimensional carrier.  This closes the representation-theoretic bridge.  It
does not canonically choose one quadratic refinement, half-spin chirality, or
physical generation.

## Pass 340 -- what the `3^16` cokernel actually is

For the integral pairing `P` of Pass 336, GAP constructs the induced actions on

```text
D_+ = F3^32 / row(P mod 3),
D_- = F3^32 / row(P^T mod 3).
```

Both are faithful and completely semisimple, and explicit MeatAxe
isomorphisms identify

```text
D_+ ~= D_- ~= 1 + V_5 + V_10
```

as `F3 U4(2)`-modules.  Each has precisely the eight submodule dimensions

```text
0, 1, 5, 6, 10, 11, 15, 16,
```

and endomorphism algebra `F3^3`.  Both are self-dual and mutually dual.  The
Eisenstein order-three scalar acts as the identity on both cokernels.

ATLAS has no irreducible 16-dimensional `U4(2)` module in characteristic 3.
The genuine irreducible 16 belongs to `2.U4(2)`, whose central involution acts
as `-I_16`.  Thus `3^16` records ramified discriminant size; it is neither a
16-state irreducible qutrit carrier nor a surviving chirality label.

## Pass 341 -- the obstruction is a restriction map in `H^2`

The optional GAP Cohomolo 1.6.12 engine gives

```text
dim H^2(PGSp(4,3), F2) = 2,
dim H^2(PSp(4,3),  F2) = 1,
dim H^2(K,          F2) = 2,
dim H^2(A,          F2) = 1,
dim H^2(N,          F2) = 3,
```

where `K=3^3:S4` is the inner line stabilizer, `A=3^3:A4` is its sign
kernel, and `N=3^3:V4` is the selector-fibre kernel.

Explicit pullbacks identify the two local directions:

1. The signed-E8 restriction is `3^3:GL(2,3)` over `K`; it remains nonsplit
   as `3^3:SL(2,3)` over `A`.
2. The selector-sign Bockstein is `3^3:(A4:C4)` over `K`; it becomes the split
   product `C2 x (3^3:A4)` over `A`.

They are therefore independent in `H^2(K,F2)`.  Globally, the two directions
are the signed-E8 class and the outer-sign Bockstein.  The latter vanishes on
the inner group and hence on `K`.  Consequently

```text
im[H^2(PGSp,F2) -> H^2(K,F2)]
```

is exactly the one-dimensional signed-E8 span.  The selector Bockstein is the
missing local direction: it cannot globalize.  This is the cohomological form
of the curved-selector obstruction from Pass 334.

There is a second correction.  For `H10=1|8|1`, Cohomolo gives

```text
PSp:  dim H1(1,8,rad9) = (0,2,2),
PGSp: dim H1(1,8,rad9) = (1,1,2).
```

The invariant map `H0(1)->H0(rad9)` is an isomorphism and `H0(8)=0`.  Exactness
forces `H1(rad9)->H1(8)` to be surjective in both cases, so the connecting map
to `H2(1)` is zero.  The two adjacent nonsplit module extensions therefore
have **zero Yoneda product**.  Their product is neither the signed-E8 class nor
the selector Bockstein.

The live cohomology engine is the GAP package
[Cohomolo](https://gap-packages.github.io/cohomolo/README.html).  The committed
certificate includes a transparent exact-value fallback for installations
without that optional package; all group and extension constructions still run
live in base GAP.

## Pass 342 -- honest local-to-global lattice reconciliation

GAP reconstructs the five local vertices `L,R,L1,L2,L3` from the inner
`U4(2)` module.  The two global controllers act as

```text
omega = [1,2,5,3,4],
T     = [1,2,3,5,4].
```

Thus omega fixes the two spine lattices and cycles the three H10 leaves.  The
integral outer reflection fixes `L` and `R` individually and swaps two leaves;
it does **not** merge the spine.  Among these five local vertices, exactly two
are stable under the maximal Eisenstein normalizer

```text
C6 x U4(2),  order 155520.
```

This corrects the prior citation shortcut.  Kirschmer's dimension-10 proof and
the nearby dimension-20 discussion contain counts `1,2,5,15` for differently
named groups, equivalence classes, and table fields.  None can be declared the
count of this five-vertex local building without an explicit identification of
the group representation and lattice equivalence.  The exact repo result is
therefore **five local vertices, two omega-stable spine lattices**, with the
external ownership comparison left scoped rather than forced.  The relevant
source is [Kirschmer's thesis](https://www.math.rwth-aachen.de/~Markus.Kirschmer/symplectic/thesis.pdf),
Theorem 4.6.1 and the later dimension-20 case analysis.

## What is now closed, and what is not

Closed:

- the actual regular `S3` selector-frame 240-cover and every intermediate
  quotient;
- the precise separation from the signed-E8 240-action;
- the finite extraspecial/Clifford 32-carrier;
- the complete `F3` identity of the `3^16` discriminant module;
- the global and local `H^2` bases and restriction obstruction;
- the zero H10 Yoneda product;
- the exact two-spine local-to-global lattice verdict.

Not claimed:

- a canonical choice between the two plus refinements;
- an identification of a selector frame with signed E8;
- a surviving qutrit phase or chirality in the `3^16` cokernel;
- a physical Standard-Model generation, mass, coupling, or continuum theorem.

## Reproduction

```bash
gap -q analysis/w33_pass338_selector_frame_240.g
gap -q analysis/w33_pass339_extraspecial_clifford_spin_bridge.g
gap -q analysis/w33_pass340_halfspin_discriminant_module.g
gap -q analysis/w33_pass341_selector_extension_cohomology.g
gap -q analysis/w33_pass342_global_lattice_reconciliation.g
python -m pytest -q tests/test_pass338_342_gap_selector_clifford_cohomology.py
```

For a live Cohomolo run, add a GAP root containing the package before the
system root.  The promoted run used GAP 4.12.1 with Cohomolo 1.6.12.
