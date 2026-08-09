# Passes 4469–4494 — apartment parity, protected H10, nonsplitting, and symmetry-breaking release

## Release thesis

The `W(3,3)` building-apartment parity code is an exact 39-dimensional binary module whose nondegenerate quotient is the previously established protected logical-label space `H10=C^perp/C`.  The code sits in a genuinely nonsplit `PSp(4,3)` extension

```text
0 -> K/J (29) -> C_ap=M/J (39) -> H10=M/K (10) -> 0.
```

The bridge, the obstruction, and the symmetry-breaking threshold are all executable.

The strongest architectural conclusion is:

```text
full PSp(4,3) symmetry:
    protected sector exists canonically only as a quotient;

fix one W33 point or one W33 line:
    an equivariant 10-dimensional complement can be chosen.
```

For the tested natural geometric stabilizers, the transition occurs already at an order-648, index-40 point or line stabilizer.

## 4469 — canonical apartment-to-H10 isometry

With line–apartment incidence `H` and point–line incidence `N`,

```text
C_ap/rad(C_ap)
 ~= F_2^40/ker(N^T N)
 -- [b] -> [N b] -->
 im(N)/ker(N^T)
 = C^perp/C = H10.
```

The kernel and symplectic pairing identities are literal:

```text
N b in ker(N^T) iff N^T N b = 0,
<H^T b,H^T c> = b^T N^T N c = <N b,N c>.
```

All 1,024 quotient classes are checked.

## 4470 — one fixed-line quadratic defect

Both natural Hamming refinements `q=wt/2 mod 2` descend and are plus type `O+(10,2)` with 528 singular classes including zero.  The raw incidence bridge is symplectic but not quadratic.  Their difference is one linear functional represented by the pre-existing Pass-187 fixed class `im(A_point mod 2)/C`.  One isotropic transvection along that fixed class repairs the quadratic on all 1,024 classes.

This transvection is a comparison-map correction, not a claimed physical gate.

## 4471 — exact generalized-quadrangle orientation criterion

For finite `GQ(s,t)`, comparison of the apartment and incidence Gram matrices gives

```text
H H^T = N^T N over F_2
iff s = 3 (mod 4) and t is odd.
```

Thus the displayed `GQ(3,9)` line orientation satisfies the bridge, whereas the dual parameter orientation `GQ(9,3)` does not.  This is a characteristic-two orientation theorem, not a duality invariant and not an explanation of empirical Ramanujan-signing percentages.

## 4480–4482 — geometric generators, radical filtration, and optimal readout

Each W33 line gives a weight-162 apartment signature and the corresponding weight-4 minimum H10 logical line.  The forty classes are distinct, span H10, and carry the dual-W33 polar graph.  The fixed class pairs one with all forty; its transvection exchanges a singular W33 forty-set with a disjoint anisotropic W33 forty-set.

The 29-dimensional radical has invariant profile

```text
8 | (6 + 1) | 14,
```

with the 8-, 6-, and 14-dimensional factors passing exhaustive cyclic irreducibility scans.

A geometric protected basis can be chosen on ten lines with intersection graph

```text
P4 disjoint-union 3 K2,
```

with six intersecting pairs.  Six is optimal among ten-line nonsingular bases: a five-edge basis would be an induced `5K2`, while exact search gives W33 induced-matching number four.  Ten software parity bits recover all 1,024 protected classes.  These are post-processing bits of acquired apartment data, not ten physical apartment measurements.

## Rediscovery correction: Pass 176 owns the protected route-hull eight-core

A late repo-maintenance change exposed 1,793 research files that had accidentally been hidden by a generic `parts/` ignore rule.  Searching the newly visible corpus found a real earlier owner:

- Pass 176 already proved the protected fixed-perpendicular / route-hull eight-space bridge and its plus-type `O+(8,2)` quadratic census `136=1+135` singular versus `120` anisotropic.

Accordingly, Passes 4485–4487 are **not** claimed as discovery of that eight-core.  Their corrected new scope is apartment-side:

- the Pass-176 `U/J` eight-core also occurs inside the newly discovered apartment radical;
- the apartment occurrence is form-null while the protected occurrence carries the prior nondegenerate form;
- the independent parallel Pass-4477/4478 coordinates reconcile exactly with the Pass-176 route-hull coordinates.

This correction is encoded in the verifier, frozen JSON, manuscript insert, public card/page, and regression tests.

## 4488 — the apartment extension is nonsplit

For

```text
0 -> K/J (29) -> E=M/J (39) -> V=M/K=H10 (10) -> 0,
```

an equivariant section `S` must satisfy `Pi S=I` and `G_E S=S G_V`.  For four `PSp(4,3)` generators this is a binary affine system with 390 unknowns and 1,660 equations:

```text
rank(A)=389,
rank([A|b])=390.
```

Therefore no full-group equivariant section exists.

Moreover,

```text
dim Hom_PSp(H10,C_ap)=1.
```

Its unique nonzero map has rank 9 and is exactly

```text
T([b])=[A* b] mod J,
```

with image `I/J` inside the radical, one-dimensional kernel, and zero projection back to H10.

## 4490 — fixed-point explanation

The large affine obstruction has a one-line representation-theoretic explanation:

```text
E^PSp = 0,
V^PSp = F_2.
```

The ambient transitive 40-line permutation module has fixed space exactly `J=<1>`, so quotienting by `J` kills every fixed apartment vector.  Protected H10 retains one fixed line.  Any equivariant section would have to lift that protected fixed vector to a fixed apartment vector; none exists.

Equivalently, the connecting map

```text
V^PSp -> H^1(PSp(4,3),K/J)
```

is nonzero on the unique protected fixed class.

## 4491–4492 — the extension cocycle is route hull glued to sentinel code

For a lift `e` of the protected fixed class, the cocycle

```text
c_g=G_E(g)e-e
```

has `PSp(4,3)`-module closure

```text
(K intersect R^perp)/J,
```

of dimension 23, with profile

```text
8 | 1 | 14.
```

It cannot be gauge-shifted into the 9-dimensional `I/J` subspace: the restricted affine support equations have coefficient rank 30 and augmented rank 31.  A representative exists in the full 23-space.

Incidence then resolves that 23-space into two older certified code objects:

```text
0 -> U(route hull,9)
  -> K intersect R^perp (24)
  --N--> C(sentinel,15)
  -> 0,
```

and, after quotienting the line all-ones vector,

```text
0 -> U/J (8, Pass 176)
  -> (K intersect R^perp)/J (23)
  -> C (15, Pass 201)
  -> 0.
```

Pass 187 supplies the fixed-line / irreducible-14 filtration of the sentinel code.  Thus the cocycle support is structurally

```text
route-hull 8 | sentinel (1 | 14).
```

This is the new incidence weld exposed by the apartment extension.

## 4493 — tested natural geometric symmetry-breaking threshold

The same section equations were restricted to canonical geometric stabilizers.

### Full group

```text
PSp(4,3), order 25920, index 1:
rank 389 / 390 -> no section.
```

### Fix one line

```text
line stabilizer, order 648, index 40:
rank 370 / 370,
affine section-family dimension 20,
dim E^H = dim V^H = 3.
```

### Fix one point

```text
point stabilizer, order 648, index 40:
rank 370 / 370,
affine section-family dimension 20,
dim E^H = dim V^H = 3.
```

### Fix an incident point-line flag

```text
flag stabilizer, order 162, index 160:
rank 338 / 338,
affine section-family dimension 52.
```

### Fix one apartment setwise

```text
apartment stabilizer, order 16, index 1620:
rank 308 / 308,
affine section-family dimension 82.
```

Therefore, **among the tested canonical geometric stabilizers**, fixing one point or one line is already sufficient to choose an equivariant protected complement.  This is not a classification of every subgroup of `PSp(4,3)` and does not prove that no larger non-geometric subgroup splits the extension.

Architecturally:

```text
full W33 symmetry  -> quotient representation is mandatory;
point/line gauge   -> equivariant representative section becomes available.
```

A linear section is a finite-module gauge choice, not automatically a physical decoder or hardware implementation.

## Pass-number reconciliation

- Reservation `b1b44324fe076be81354f1a68d199f95124f3913` owns 4469–4473 and predates the overlapping parallel reservation.
- Parallel reservation `d300fa184fa5665fd539f39b2d6ab4b23c08a39d` owns 4474–4479; the abandoned local 4474–4478 continuation was deleted and renumbered to 4480–4484.
- Passes 4485–4489 are reserved at `cad42db3a8db303eb5d82b138e517085630eb7b6`.
- Passes 4490–4494 are separately reserved for the fixed-point/cocycle/symmetry-breaking continuation.

## Manuscript and public integration

The root manuscript wrappers contain the 4469–4471, 4480–4483, 4485–4488, and 4490–4492 shared inserts.  The 4493 insert is registered in the current-frontier integration path, with a guarded one-shot recovery workflow that restores the immediately previous manifest version if the manifest was truncated before appending 4493.

Standalone public theorem pages are landed for:

- line-signing/apartment parity and the H10 bridge;
- geometric H10 readout;
- apartment core self-gluing / nonsplitting;
- fixed-line extension cocycle;
- symmetry-breaking section threshold.

The additive public-card registry contains the parallel 4472–4479 packet and all of these continuation cards.

**Current infrastructure boundary:** the connector still has not provided a reliable visible confirmation that the giant `docs/index.html` has materialized all newly registered cards.  The source cards, standalone pages, registry and reconciliation workflows are on `master`; literal index materialization must remain reported as unconfirmed until directly observed.

## Evidence and CI

Executable witnesses:

- `analysis/w33_pass4469_apartment_css_h10_intertwiner.py`
- `analysis/w33_pass4470_apartment_h10_quadratic_fixed_layer.py`
- `analysis/w33_pass4471_general_gq_apartment_incidence_bridge.py`
- `analysis/w33_pass4480_line_logical_apartment_twins.py`
- `analysis/w33_pass4481_apartment_radical_module_filtration.py`
- `analysis/w33_pass4482_ten_line_protected_readout.py`
- `analysis/w33_pass4485_apartment_core_self_gluing.py`
- `analysis/w33_pass4486_repeated_core_form_resurrection.py`
- `analysis/w33_pass4487_parallel_pauli_core_coordinate_weld.py`
- `analysis/w33_pass4488_apartment_extension_nonsplitting.py`
- `analysis/w33_pass4490_fixed_point_nonsplitting_obstruction.py`
- `analysis/w33_pass4491_fixed_line_extension_cocycle.py`
- `analysis/w33_pass4492_cocycle_support_route_sentinel_extension.py`
- `analysis/w33_pass4493_symmetry_breaking_section_threshold.py`

Focused regression/evidence workflows cover each packet plus a release guard for manifest/public-registry truncation and prior-owner drift.

## External literature boundary

Relevant primary-source context includes Chandler–Sin–Xiang on finite symplectic incidence modules and Crnković–Hawtin–Švob on generalized-quadrangle codes.  Targeted searches did not reveal the exact apartment 39→10 bridge, fixed-line quadratic repair, nonsplit extension, cocycle support, or point/line symmetry-breaking section threshold.

The only defensible priority wording is **“no earlier occurrence found for these apartment-extension statements in the searched sources/corpus,” not “proved novel.”**

## Nonclaims

This release does **not** establish:

- a second physical CSS code or new species of logical qubit;
- a physical implementation of the fixed transvection;
- ten physical measurements replacing apartment syndrome acquisition;
- E8 dynamics in the radical copy;
- a four-qubit hardware device merely from the finite Pauli realization;
- particle/cosmological meanings for module dimensions `8,6,1,14`;
- a physical error current from the cohomological cocycle;
- an all-subgroup classification of extension splitting;
- a symmetry-preserving direct-sum protected register under full `PSp(4,3)` symmetry.
