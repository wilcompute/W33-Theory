# Passes 1611–1615 — torsion filtration, independent XORs, determinant-two bridge, and the frame/octet coherent configuration

## Executive result

This packet executes the five continuation fronts opened after Passes 1601–1605 while explicitly reconciling the parallel Passes 1537–1541 and the separately reserved 1606–1610 glue track.

The verifier rebuilds `W(3,3)`, the canonical frame/edge matrix

\[
M\in\{0,1\}^{540\times240},
\]

the 45 intrinsic induced `K4,4` octets

\[
K\in\{0,1\}^{45\times240},
\]

and the half-incidence matrix

\[
J=\frac12MK^{\mathsf T}\in\{0,1\}^{540\times45}.
\]

All **31/31** checks pass. The exact conclusions are:

1. the 30-dimensional elementary two-torsion module has composition factors \(1,8,1,6,14\), with socle-series dimensions \(1,9,10,16,30\);
2. the 8-factor is irreducible over \(\mathbb F_2\) but has endomorphism field \(\mathbb F_4\), while the 6- and 14-factors have scalar endomorphism field \(\mathbb F_2\);
3. a deterministic set of 30 octets per color yields a solver-ready native-XOR export of 270 equations and exactly reproduces the global rank increase \(2100\to2340\);
4. every exact cover has the same octet signature \(J^{\mathsf T}x=8\mathbf1\), so Bockstein torsion is provably blind to cover orbit and four-packing extendibility;
5. the saturated unsigned-to-signed free-15 bridge is integral with determinant exactly 2, explaining the unique parity defect in the Smith factor 6;
6. the frame/octet action is a two-fiber coherent configuration of rank \(32+3+5+5=45\); the right octet fiber is the rank-three `SRG(45,32,22,24)` scheme and canonically splits as \(1+24+20\).

The global Hoffman nine-coloring remains open.

---

## Pass 1611 — the complete binary torsion composition series

Pass 1601 proved

\[
\operatorname{Tor}_2(\operatorname{coker}M)\cong(\mathbb Z/2)^{30}.
\]

The Bockstein realization identifies this as the quotient of the 45-dimensional binary octet space by the 15-dimensional reduction of the integral kernel. The four standard symplectic transvections give an exact \(30\)-dimensional \(\mathbb F_2PSp(4,3)\)-module.

The verifier constructs the invariant chain

\[
0<V_1<V_9<V_{10}<V_{16}<V_{30}
\]

with dimensions

\[
\boxed{1,9,10,16,30}.
\]

The successive composition-factor dimensions are

\[
\boxed{1,8,1,6,14}.
\]

Irreducibility is not inferred from dimensions. For every nonzero vector orbit in each factor, the verifier computes the linear span and checks that it equals the whole factor. The orbit data are:

- dimension 8: orbit sizes \(120,135\), both spanning 8;
- dimension 6: orbit sizes \(27,36\), both spanning 6;
- dimension 14: twelve nonzero-vector orbits, every one spanning 14.

The 8-factor has a two-dimensional commutant. Its non-scalar endomorphism satisfies

\[
T^2+T+I=0,
\]

so its endomorphism field is exactly \(\mathbb F_4\). The 6- and 14-factors have one-dimensional commutants.

This is an exact composition-series statement. No external Brauer-character label is assigned.

---

## Pass 1612 — reduced native-XOR solver export

Pass 1539 established all 405 exact cardinality cuts

\[
\sum_{f:J_{fo}=1}x_{fc}=8,
\qquad o=1,\ldots,45,\quad c=1,\ldots,9,
\]

and proved their parity rank gain. Pass 1612 adds the missing solver artifact: a deterministic independent set of 30 octet columns per color.

The selected octet indices are

```text
0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,
16,18,19,20,21,22,24,25,27,28,29,30,31,33,34
```

For each of the nine colors this supplies 30 native XOR equations, each supported on 72 frame variables and having right-hand side zero. The deterministic exporter emits a sidecar containing

\[
\boxed{270}
\]

native XOR clauses.

Exact ranks:

\[
\boxed{2100\longrightarrow2340}
\]

for the global parity system, and

\[
\boxed{2109\longrightarrow2349}
\]

after the standard nine-variable symmetry fixing.

The 270 selected equations achieve the same final rank as all 405 cuts. The export hash is

```text
f104065b227f2bee0af61afb52d9e95feac232b4bd2397f72bc3c0cd2caa9109
```

This is a solver-strengthening artifact, not a satisfiability verdict.

---

## Pass 1613 — four-packing torsion-signature blindness

For any exact-cover indicator \(x\in\{0,1\}^{540}\),

\[
M^{\mathsf T}x=\mathbf1_{240}.
\]

Since \(2J=MK^{\mathsf T}\) and every octet has 16 edges,

\[
2J^{\mathsf T}x
=KM^{\mathsf T}x
=K\mathbf1
=16\mathbf1.
\]

Therefore

\[
\boxed{J^{\mathsf T}x=8\mathbf1_{45}}
\]

for **every** exact cover.

Consequently every four-cover packing has signature

\[
\boxed{32\mathbf1_{45}},
\]

and its 300-frame residual carrier has signature

\[
\boxed{72\mathbf1-32\mathbf1=40\mathbf1}.
\]

This is a useful negative theorem: the Bockstein/torsion signature cannot distinguish exact-cover orbits, cannot correlate with the known blocked four-packing, and cannot by itself predict fifth-cover extendibility. Any successful obstruction must use nonlinear, orbit-sensitive, or higher-order data.

---

## Pass 1614 — the determinant-two saturated free-15 bridge

Let \(C\) be the unsigned free-15 bridge and \(F\) the signed-turn bridge from Pass 1604. Their coordinate Smith data are

\[
\operatorname{SNF}(C)=1^{10}\oplus3^5,
\]

\[
\operatorname{SNF}(F)=1^{10}\oplus3^4\oplus6.
\]

Pass 1614 constructs saturated integer bases \(B_C,B_F\) for their rational 15-spaces and exact coordinate matrices

\[
C=B_CR_C,
\qquad
F=B_FR_F.
\]

Because \(C\) and \(F\) have the same rational kernel, there is a unique rational matrix \(Q\) satisfying

\[
QR_C=R_F.
\]

The verifier proves that \(Q\) is integral and

\[
\boxed{|\det Q|=2}.
\]

Hence

\[
\boxed{\operatorname{coker}Q\cong\mathbb Z/2}.
\]

This is the exact origin of the lone even factor in the signed bridge. The unsigned and signed free-15 lattices are rationally isomorphic, but the canonical integral map lands in an index-two sublattice. A primitive missing-coset vector is frozen by hash; it has support 128 and squared norm 152.

Thus the factor 6 is resolved as

\[
6=2\cdot3:
\]

the 3 belongs to the common ternary lattice structure, while the 2 is the unique orientation-parity embedding defect.

---

## Pass 1615 — the rank-45 frame/octet coherent configuration

The inner projective group and its full outer extension act faithfully on the 45 octets:

\[
|PSp(4,3)|=25920,
\qquad
|PGSp(4,3)|=51840.
\]

The octet action has rank three, with subdegrees

\[
\boxed{1,32,12}.
\]

Its nontrivial relation is

\[
A_{45}=\operatorname{SRG}(45,32,22,24).
\]

Therefore the rational octet permutation module is multiplicity-free and splits canonically as

\[
\boxed{\mathbf1\oplus V_{24}\oplus V_{20}}.
\]

The half-incidence Gram identity is

\[
\boxed{J^{\mathsf T}J=66I+3A_{45}+6\mathbf J},
\]

with spectrum

\[
432^1\oplus72^{24}\oplus54^{20}.
\]

Since \(J\) has rational rank 45, it injects these three canonical modules into the 540-frame carrier.

### Full two-fiber orbital count

For the inner group:

- frame–frame orbitals: 32;
- octet–octet orbitals: 3;
- frame-to-octet cross orbitals: 5;
- octet-to-frame reverse orbitals: 5.

Thus the complete two-fiber coherent configuration has rank

\[
\boxed{32+3+5+5=45}.
\]

A frame stabilizer has octet subdegrees

\[
\boxed{6,24,1,8,6},
\]

and an octet stabilizer has frame subdegrees

\[
\boxed{72,288,12,96,72}.
\]

The actual relation \(J_{fo}=1\) is exactly the unique cross orbital of degree 6 per frame and 72 per octet.

### Important non-closure boundary

The five values of \(JJ^{\mathsf T}\) give the uniform row profile

\[
6^1,\quad3^{32},\quad2^{15},\quad1^{300},\quad0^{192}.
\]

But this five-value partition is **not** itself an association scheme: squaring the intersection-1 relation yields eight different values on that same relation. The correct closure is the full rank-32 frame orbital algebra, not the coarse five-value Gram partition.

Modular ranks are

\[
\operatorname{rank}_{2}J=44,
\quad
\operatorname{rank}_{3}J=44,
\quad
\operatorname{rank}_{5}J=45,
\]

while

\[
\operatorname{rank}_{2}(J^{\mathsf T}J)=14,
\quad
\operatorname{rank}_{3}(J^{\mathsf T}J)=0,
\quad
\operatorname{rank}_{5}(J^{\mathsf T}J)=45.
\]

---

## Evidence boundary

Everything in this packet is a finite matrix, lattice, permutation-group, or parity identity rebuilt from projective coordinates. The native XOR file is an exact consequence of the resolution equations. The packet does not prove that a nine-cover resolution exists or does not exist, does not claim a decoder threshold, and does not identify the modular factors with named Brauer characters without an independent character-table certificate.
