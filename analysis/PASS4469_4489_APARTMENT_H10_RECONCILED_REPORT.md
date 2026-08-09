# Passes 4469–4492 — reconciled apartment/H10 breakthrough report

This report records the apartment-parity/protected-code lane, its reconciliation with the parallel Pass-4472–4479 packet, the pass-number collision correction, the hidden-corpus rediscovery correction, and the fixed-line extension cocycle through Pass 4492.

## Executive result

The `W(3,3)` building-apartment parity code has an exact protected quotient:

```text
0 -> 29-dimensional radical -> C_ap(39) -> H10(10) -> 0.
```

The quotient is canonically the previously certified logical-label space `H10=C^perp/C`; the map is induced by point–line incidence.  The extension is **nonsplit** as a `PSp(4,3)`-module.

A hidden-corpus audit corrected one ownership point: **Pass 176 already owned the protected 8-dimensional route-hull core** and its plus-type `O+(8,2)` quadratic structure.  The genuinely new apartment result is that this owned 8-core also sits inside the apartment radical, where the apartment form is null, and that it participates in the nonsplit 39→10 extension.

The nonsplitting obstruction localizes further.  The protected fixed line has no fixed lift in the apartment 39-space:

```text
C_ap^PSp = 0,
H10^PSp = F_2.
```

Its connecting cocycle is supported on the 23-dimensional module

```text
(K intersect R^perp)/J,
```

and incidence resolves that support as an exact extension of two older certified code objects:

```text
0 -> U/J (8, Pass 176 route hull)
  -> (K intersect R^perp)/J (23)
  -> C (15, Pass 201 sentinel code)
  -> 0.
```

Thus the obstruction-support profile `8 | 1 | 14` is not a numerological 23: it is the route-hull 8-core glued by incidence to the sentinel `[40,15,8]` code.

## Pass 4469 — canonical apartment/H10 symplectic bridge

With line–apartment incidence `H` and point–line incidence `N`,

```text
C_ap/rad(C_ap)
 ~= F_2^40/ker(N^T N)
 -- [b] -> [N b] -->
 im(N)/ker(N^T)
 = C^perp/C = H10.
```

Exact identities:

```text
N b in ker(N^T)  iff  N^T N b = 0,
<H^T b,H^T c> = b^T N^T N c = <N b,N c>.
```

All `2^10` quotient classes were checked.

## Pass 4470 — fixed-line quadratic correction

The natural Hamming refinements `q=wt/2 mod 2` descend on both 10-spaces and are both plus type `O+(10,2)` with 528 singular classes including zero.  The raw incidence map is symplectic but not quadratic.  Its defect is one linear functional represented by the pre-existing Pass-187 fixed class `im(A_point mod 2)/C`.  One transvection along that fixed isotropic class repairs the quadratic on all 1,024 classes.

## Pass 4471 — exact `GQ(s,t)` orientation criterion

Pass 4465 gives

```text
H H^T=(r-beta)I+(alpha-beta)A*+beta J,
r=(s+1)s^2t^2/2,
alpha=s^2t,
beta=s(s+1)/2,
```

while incidence gives `N^T N=(s+1)I+A*`.  Therefore

```text
H H^T = N^T N over F_2
iff s = 3 (mod 4) and t is odd.
```

`GQ(3,9)` passes in the displayed line orientation; the dual parameter orientation `GQ(9,3)` fails.  This does not explain empirical Ramanujan-signing rates.

## Passes 4480–4482 — geometric consequences

Each W33 line gives both a weight-162 apartment signature and its weight-4 minimum H10 logical line.  The forty classes are distinct, span H10, and carry the dual-W33 polar graph.  The fixed class pairs 1 with every line class; its transvection exchanges a singular W33 forty-set with a disjoint anisotropic W33 forty-set.

The 29-dimensional radical has invariant profile

```text
8 | (6 + 1) | 14,
```

with the 8-, 6-, and 14-dimensional factors passing exhaustive cyclic irreducibility scans.

An optimal geometric H10 basis is supported on ten lines with intersection graph

```text
P4 disjoint-union 3 K2,
```

and six intersecting pairs.  Five is impossible because it would require an induced `5K2`, while the exact W33 induced-matching number is four.  Ten software parities recover all 1,024 protected coordinates.  These are post-processing bits, not ten physical apartment measurements.

## Pass 176 ownership correction; Passes 4485–4487 apartment-side reconciliation

The newly tracked hidden corpus exposed an earlier theorem that must be credited.  Pass 176 already proved an incidence-fixed-line isometry

```text
f^perp/<f>  ->  route hull U/J
```

with the protected plus-type 8-space census `136=1+135` singular versus `120` anisotropic classes.  Therefore the protected E8/2E8 route-hull core is **not new** in Passes 4485–4487.

The new apartment-side result is:

- the same Pass-176 `U/J` also occurs inside the apartment radical `K/J`;
- on that radical occurrence, the apartment polar and Hamming quadratic forms vanish identically;
- through the protected quotient, the same module carries the prior nondegenerate `O+(8,2)` form;
- the parallel Pass-4477/4478 `F8/q8` implementation was reconciled in literal line coordinates with the Pass-176 route-hull construction.

This is a self-gluing/reconciliation result around an owned core, not a new claim of the core itself.

## Pass 4488 — nonsplit apartment extension

The exact sequence

```text
0 -> K/J (29) -> M/J (39) -> M/K=H10 (10) -> 0
```

has no `PSp(4,3)`-equivariant section.  The 1,660-equation affine section system in 390 unknowns has

```text
rank(A)=389,
rank([A|b])=390.
```

Moreover

```text
dim Hom_PSp(H10,C_ap)=1.
```

The unique nonzero map has rank 9 and is exactly

```text
T([b])=[A* b] mod J,
```

with image `I/J` in the radical, one-dimensional kernel, and zero projection back to H10.

## Pass 4490 — fixed-point explanation of nonsplitting

The large affine certificate has a one-line conceptual reason.  The transitive 40-line permutation module has fixed space exactly `J=<1>`, so after quotienting by `J`,

```text
(M/J)^PSp = 0.
```

Protected H10 has one fixed line:

```text
(M/K)^PSp = F_2.
```

An equivariant section would have to lift that nonzero protected fixed class to a nonzero fixed apartment class; none exists.  In the long exact fixed-point/cohomology sequence, the connecting map

```text
H10^PSp -> H^1(PSp,K/J)
```

is therefore nonzero/injective on the one-dimensional fixed line.

## Pass 4491 — fixed-line cocycle support

Choose a lift `e` of the protected fixed class `v`.  The generator defects

```text
c_g=G_E(g)e-e
```

represent the connecting cocycle.  Their `PSp`-module closure has dimension 23 and equals

```text
(K intersect R^perp)/J.
```

Its invariant chain is

```text
J < U < I < K intersect R^perp
1 < 9 < 10 < 24,
```

so after quotienting by `J` the support profile is

```text
8 | 1 | 14.
```

The affine support equations show the cocycle cannot be gauged into `I/J` (dimension 9) but can be represented in the 23-space.  Thus the route-side 6-factor of the full radical `8 | (6+1) | 14` is not required by this fixed-line obstruction.

## Pass 4492 — route-hull/sentinel resolution of the 23-space

Let `C=ker N^T` be the Pass-201 `[40,15,8]` sentinel code.  Incidence restricts to

```text
0 -> U -> W=K intersect R^perp --N--> C -> 0,
```

with dimensions `9 -> 24 -> 15`.  The image is all of `C` and the kernel is the Pass-176 route hull `U=R intersect R^perp`.  Since line `J` lies in `U`,

```text
0 -> U/J (8) -> W/J (23) -> C (15) -> 0.
```

Pass 187 supplies the fixed-line/irreducible-14 filtration of `C`, so the cocycle support is structurally

```text
8 | (1 | 14).
```

This is the new code-level weld: the nonsplitting obstruction is supported on an incidence extension of the old Pass-176 route hull by the old Pass-201 sentinel code.

## Pass-number reconciliation

- Reservation `b1b44324fe076be81354f1a68d199f95124f3913` owns 4469–4473 and predates the parallel 4472–4479 reservation.
- Parallel reservation `d300fa184fa5665fd539f39b2d6ab4b23c08a39d` predates the abandoned local 4474–4478 reservation by 27 seconds; the colliding continuation was removed from current `master` and renumbered to 4480–4484.
- Passes 4485–4489 are reserved at `cad42db3a8db303eb5d82b138e517085630eb7b6`.
- Passes 4490–4494 are reserved separately for the fixed-point/cocycle continuation.

## Rediscovery guard after the hidden-corpus repair

A parallel maintenance commit exposed 1,793 research files that a generic `parts/` ignore rule had accidentally hidden from Git.  Searching that newly visible corpus found the Pass-176 protected route-hull theorem above, forcing the ownership correction.  Targeted searches still did not reveal an earlier apartment `39→10` quotient bridge, apartment-radical self-gluing, nonsplitting theorem, or fixed-line cocycle-support result.  Broad code search was intermittently unavailable/502.

The defensible wording is therefore **“no earlier occurrence found for the apartment extension results in the searched corpus,” not “proved novel.”**

Relevant primary-source background remains Chandler–Sin–Xiang on finite symplectic incidence modules and Crnković–Hawtin–Švob on generalized-quadrangle codes.

## Manuscript/public integration boundary

All three manuscript wrappers include the apartment/H10 bridge, geometric continuation, and nonsplitting/self-gluing inserts.  The standalone public theorem pages and additive public-card registry are landed.  A safe `docs/index.html` reconciler workflow is present, but the connector still has not surfaced a bot commit materializing the new cards into the giant `docs/index.html`; literal index materialization remains unconfirmed.

## Nonclaims

This packet does not establish a second physical CSS code, an implemented transvection, ten physical measurements replacing syndrome acquisition, E8 dynamics in the radical copy, a four-qubit hardware implementation from the finite Pauli core, particle meanings for `8,6,1,14`, or a symmetry-preserving direct-sum protected register.  Pass 4488/4490 prove the last one impossible under full `PSp(4,3)` symmetry.