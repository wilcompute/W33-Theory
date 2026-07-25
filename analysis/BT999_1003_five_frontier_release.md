# Passes 999–1003 — A5 double class, signed equivariance, and ramified gluing

This packet continues directly from Passes 982–984. It replaces two remaining
sample-level statements with exact theorems, extracts the ramified 2-adic
mechanism as a finite filtration, and completes the T(8)/Chang separator.

## Pass 999 — Exact A5 double-class census

Inside `PSp(4,3)` there are exactly **432** subgroups isomorphic to `A5`, split
into two conjugacy classes of **216**. Every `C5` lies in one `A5` from each
class. The paired groups intersect in `D10`, and both classes have identical
W33 point and edge orbit profiles:

```text
vertices: 20,20
edges:    60,60,30,30,20,20,10,10
```

Thus the uniform samples in Pass 982 did not imply a single conjugacy class.

## Pass 1000 — Signed-turn spectral fingerprint

The two classes are invisible to point/edge orbit sizes and to the full signed
edge character, the `K=-6` protected block, and the `K=2` block. They are
separated exactly by an order-three character exchange:

```text
Class A: trace(K=4)=3, trace(K=10)=0
Class B: trace(K=4)=0, trace(K=10)=3
```

The corresponding exact `A5` irreducible decompositions are recorded in the
certificate.

## Pass 1001 — Full signed edge equivariance

The signed oriented-edge action commutes with `K` for **all 25,920** elements of
`PSp(4,3)`. The unsigned edge permutation commutes for only three elements, a
coordinate-dependent `C3`. This closes Pass 984's eight-sample boundary.

## Pass 1002 — Ramified kernel-growth gluing theorem

For a projector-congruence stack `S`, conductor `M`, and `nu=v2(M)`, the complete
2-primary gluing is reconstructed from

```text
kappa_j = log2 |ker(S mod 2^j)|,
Delta_j = kappa_j-kappa_(j-1),
mult(Z/2^e) = Delta_(nu-e)-Delta_(nu-e+1).
```

For W33 the kernel-growth sequence is

```text
40,80,119,158,182
```

and reconstructs `(Z/8) + (Z/2)^15`. For the cospectral T(8)/Chang family, the
single final growth bit `104` versus `103` is exactly the extra binary gluing
that separates T(8) from the Chang pair.

## Pass 1003 — Chang clique-complex separator

The complete clique towers separate all three cospectral graphs:

```text
T(8):             28,168,336,280,168,56,8
Chang(matching):  28,168,336,248,72,8
Chang(8-cycle):   28,168,336,240,48
```

Maximum clique sizes form `7,6,5`. Clique-complex Euler characteristics are
exactly `36,12,4`; reduced Euler characteristics are `35,11,3`. The latter
resonance is recorded without claiming a W33 identification.

## Verification

Each script writes a deterministic JSON ledger, supports `--check`, and is
covered by `tests/test_w33_pass999_1003.py`.

## Parallel Pass 989–998 intake warning

The concurrent prose-only batch contains several useful corrections, especially the
rejection of a literal modular-newform identification. Three later claims are not
accepted by this release:

- **Pass 990 E8 embedding:** a rank-15 eigenlattice cannot embed as a lattice in the
  rank-8 E8 lattice or in the 8-dimensional space `E8 tensor R`; the stated
  `D15 subset E8 tensor R` construction is dimensionally impossible. The assertion
  that E8 contains every positive-definite integral Gram matrix of rank at most 8 is
  also false without substantial local and discriminant-form conditions.
- **Pass 991 decoherence:** the quoted crossover, fidelity, linewidth, and room-
  temperature margins are heuristic estimates, not consequences of an executed
  Lindblad calculation for the 40-mode device. They must not be presented as a
  theorem or experimental guarantee.
- **Pass 993/994 universality language:** `k-r=10` is simultaneously the spectral
  gap and first nonzero Laplacian eigenvalue by definition, so those are not two
  independent roles. The supplied text does not prove that W33 is the smallest
  12-regular Ramanujan SRG, nor that the arithmetic rank-10 result follows from the
  same cyclotomic mechanism. Those remain separate computed facts until an
  explicit theorem connects them.

This packet leaves the concurrent files intact but marks these statements as
**unverified / stop-ship for a paper**.
