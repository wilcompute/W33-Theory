# Passes 2200–2206 Exact Release

## Status

`PASS_WITH_Q11_REPRESENTATION_BOUNDARY`

Aggregate semantic SHA-256:

`84af8784ec8c3109632e519d9a5278a26735466d358b46453016bf03b895b3c7`

## Results

### 2200 — corrected quadratic targets

The historical Pass-2015 table selected arbitrary same-degree irreducibles.  The target-identified table is

| target | Sym²(90) | Λ²(90) |
|---:|---:|---:|
| 15 | 3 | 0 |
| 24 | 5 | 0 |
| 30 | 3 | 2 |
| 81 | 7 | 5 |

Both gauge blocks are symmetric-only.  The explicit Pass-2051 tensors are valid surjective generators, not complete Hom bases.

### 2201–2202 — all-odd-q regular-spread theorem

Regular symplectic spreads are elliptic hyperplane sections of `Q(4,q)`.  The invariant

`Delta(x,y)=4Q(x)Q(y)-B(x,y)^2`

separates one-line and `q+1`-line intersections.  The `q+1` relation is strongly regular for every odd q with

- `v=q^2(q^2-1)/2`,
- `k=q(q-2)(q^2+1)/2`,
- `lambda=q(q^3-4q^2+7q-8)/2`,
- `mu=q(q-2)(q-1)^2/2`,
- eigenvalues `q(q-2)` and `-q`.

Literal checks at q=3,5,7,11 include the new q=11 row `(v,k,lambda,mu)=(7260,6039,5038,4950)`.

### 2203 — Ree–Tits control

The q=27 Ree–Tits slice `g(x,y)=-x^21-y^9` passes all 729 Ball–Zieve permutation tests.  A closed 144-spread regular suborbit has intersection histogram

`19^34, 28^76, 37^28, 46^4, 55^2`.

Thus the regular `{1,q+1}` scheme does not extend unchanged to this non-Desarguesian spread.

### 2204 — actual phase-controller image

The abstract independent-clock group `(C4 x C6):C2` has order 48.  On the canonical single complex structure, the representation

`(a,b,e) -> (3a+2b mod 12,e)`

has kernel `{(0,0,0),(2,3,0)}` and image `C12:C2` of order 24.  A faithful order-48 controller requires two independent complex phase registers.

### 2205 — q=7/q=11 boundary

The geometric `i` exists at q=7 and q=11 because `-1` is nonsquare.  Complex characters are already observed at q=7.  A universal D4 incompatibility theorem is not promoted: the q=3 statement depends on a specific signed-edge complex pair, while no canonical cross-q “90” has been selected, and the diagonal outer action must be checked representation by representation.

### 2206 — RTL reference

`rtl/w33_spread_mixer36.sv` implements the exact 36-lane adjacency masks and the faithful 24-state phase image.  The algebraic verifier checks

- `A^2=9I+6J`,
- spectrum `15^1,3^15,(-3)^20`,
- signed `W+4` width safety for `W=16`,
- two-hop arithmetic,
- the `C12:C2` image and two-element kernel.

No HDL compiler or synthesis suite was available locally, so timing, area, power and fabrication are not claimed.

## Frozen certificates

- regular-spread scheme: `4b8b08837e00d7f440950fa29049d49409986355568ed5cf9bb860aa4220b939`
- Ree–Tits control: `7e1eaac9fec07d0dcb821855c12722177485cdc524df49f6c1448f17b30a03db`
- quadratic/controller audit: `f385072260077f141cb89ad75c1657b5d238ec7646ea3c0ef7862c647955fece`
- RTL reference: `a20a186134409abe976b84312785435fe5906a72dc38b6071251810fa657180d`

Both `w33_paper.tex` and `photonic_holonet.tex` include the shared Pass-2206 insert.

## Boundaries

Field reduction, polar-space spectra, the Ree–Tits spread and the Ball–Zieve coordinate criterion retain literature ownership.  The nonregular calculation is a counterexample to uniform extension, not a classification.  The order-48 group is an abstract two-register model; its canonical single-J image has order 24.  No finite block is identified with a measured charge, colour, generation, neutrino, coupling, or spacetime degree of freedom.
