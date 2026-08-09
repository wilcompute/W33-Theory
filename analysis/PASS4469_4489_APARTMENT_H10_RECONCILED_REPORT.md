# Passes 4469–4489 — reconciled apartment/H10 breakthrough report

This report records the independent apartment-parity/protected-code lane, its reconciliation with the parallel Pass-4472–4479 packet, the pass-number collision correction, the rediscovery boundary after 1,793 hidden research files became tracked, and the remaining public-index limitation.

## Executive result

The `W(3,3)` building-apartment parity code is not an unrelated 39-bit-ish syndrome object sitting beside the older binary CSS layer.  Its nondegenerate quotient is canonically the same protected 10-dimensional logical-label space `H10=C^perp/C`, with a one-fixed-line quadratic correction.  The full apartment code is a nonsplit `PSp(4,3)`-extension

```text
0 -> 29-dimensional radical -> 39-dimensional apartment code -> H10(10) -> 0.
```

Inside that extension the same literal irreducible quotient `U/J` of dimension 8 appears twice: once as a submodule of the radical and once as the middle factor of protected `H10=1|8|1`.  It is form-null on the radical side but carries the protected plus-type `O+(8,2)` form on the quotient side.  The independent parallel Pass-4477/4478 E8/2E8 and real four-Pauli phase-space core was welded to this `U/J` in explicit coordinates.

The extension does **not** split equivariantly.  A `PSp(4,3)`-equivariant section would solve a 1,660-equation binary affine system in 390 unknowns; the coefficient rank is 389 and the augmented rank is 390.  Moreover

```text
dim Hom_PSp(H10, C_ap) = 1,
```

and the unique nonzero map has rank 9:

```text
[b] -> [A* b] mod J,
```

landing entirely back in the radical with one-dimensional kernel.  Hence symmetry permits a 10→9 return channel into the radical, not an invariant 10-dimensional protected complement.

## Pass chain

### Pass 4469 — canonical symplectic bridge

With point–line incidence `N` and line–apartment incidence `H`,

```text
C_ap/rad(C_ap)
 ~= F_2^40/ker(N^T N)
 -- [b] -> [N b] -->
 im(N)/ker(N^T)
 = C^perp/C = H10.
```

The kernel and pairing are literal:

```text
N b in ker(N^T)  iff  N^T N b = 0,
<H^T b,H^T c> = b^T N^T N c = <N b,N c>.
```

### Pass 4470 — fixed-line quadratic correction

The natural Hamming refinements `q=wt/2 mod 2` descend on both 10-spaces; each is plus type `O+(10,2)` with 528 singular classes including zero.  The raw incidence bridge is symplectic but not quadratic.  Its defect is one nonzero linear functional, represented by the unique isotropic class whose H10 image spans the pre-existing Pass-187 fixed layer

```text
im(A_point mod 2)/C.
```

One transvection along that fixed class repairs the quadratic on all 1,024 quotient classes.

### Pass 4471 — exact generalized-quadrangle orientation criterion

For `GQ(s,t)`, Pass 4465 gives

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

The displayed line orientation of `GQ(3,9)` passes; the dual parameter orientation `GQ(9,3)` fails.  This is an orientation-sensitive characteristic-two theorem, not a duality invariant and not an explanation of empirical Ramanujan-signing rates.

### Passes 4480–4482 — geometric consequences

Each geometric line gives both a weight-162 apartment signature and its weight-4 minimum H10 logical line.  The forty classes are distinct, span H10 and carry the dual-W33 polar graph.  The fixed class is uniquely characterized by pairing 1 with all forty.  Its transvection exchanges a singular W33 forty-set with a disjoint anisotropic W33 forty-set.

The 29-dimensional radical has invariant profile

```text
8 | (6 + 1) | 14,
```

with the 8-, 6- and 14-dimensional factors passing exhaustive cyclic irreducibility scans.

A geometric H10 basis exists on ten lines whose intersection graph is

```text
P4 disjoint-union 3 K2,
```

with six intersecting pairs.  Six is optimal because a five-edge nonsingular alternating graph would be an induced `5K2`, while exact search gives W33 induced-matching number four.  Ten software parity bits `p_i=<y,g_i>` recover all protected coordinates by `c=pG^{-1}`.  These are post-processing bits of acquired apartment data, not ten physical apartment measurements.

### Passes 4485–4487 — repeated eight-core and parallel weld

Set

```text
M=F_2^40,
K=ker A*,
I=im A*,
R=ker N,
U=R intersect I,
J=<1>.
```

The map `A*` induces `M/K ~= I`, and the chain `J<U<I` is the protected `1|8|1` filtration.  Thus its middle factor is literally `U/J`; that same `U/J` is already a submodule of the apartment radical `K/J`.

The form structures differ sharply:

```text
radical occurrence U/J: polar rank 0, q identically zero;
protected occurrence U/J: polar rank 8, O+(8,2), 135 nonzero singular + 120 anisotropic.
```

The parallel Pass-4477/4478 construction was then placed into the same ambient line coordinates.  Its fixed vector maps to `J`, its fixed perpendicular maps exactly to `U`, its `F8` Gram matrix equals the lift-defined protected Gram matrix entry by entry, and its invariant quadratic agrees with `wt(Nb)/2` on all 256 classes.  Therefore the parallel E8/2E8 and real four-Pauli finite phase-space packet uses exactly this ambient `U/J` quotient.

### Pass 4488 — nonsplitting obstruction

The exact extension

```text
0 -> K/J (29) -> M/J (39) -> M/K=H10 (10) -> 0
```

has no `PSp(4,3)`-equivariant linear section.  The affine section system has

```text
unknowns = 390,
equations = 1660,
rank(A) = 389,
rank([A|b]) = 390.
```

The homogeneous intertwiner space has dimension one.  Its unique nonzero element is the rank-9 return map `[b]->[A*b] mod J`, with image `I/J` in the radical and one-dimensional kernel.

## Parallel-pass reconciliation

- Reservation `b1b44324fe076be81354f1a68d199f95124f3913` for Passes 4469–4473 predates the parallel 4472–4479 reservation, so this track retains 4469–4473.
- The independent reservation `d300fa184fa5665fd539f39b2d6ab4b23c08a39d` for 4472–4479 predates this track's abandoned 4474–4478 reservation by 27 seconds.  The colliding continuation was therefore removed from current `master` and renumbered to 4480–4484.
- Passes 4485–4489 were separately reserved at `cad42db3a8db303eb5d82b138e517085630eb7b6`.
- The parallel 4472–4479 theorem packet remains present through the frontier manifest; the new 4480–4489 inserts are additive and explicitly cross-reference, rather than overwrite, that work.

## Manuscript integration

Current wrappers for all three root manuscripts include the shared bridge, geometric continuation and nonsplitting/self-gluing inserts:

- `w33_paper.tex`
- `photonic_holonet.tex`
- `holonet_machine_blueprint.tex`

The machine blueprint remains the stricter evidence-typed document; the Photonic Holonet paper itself already warns that its engineering claims have had less adversarial testing than the finite mathematics.  The new inserts therefore keep the architecture boundary explicit: the protected space is a quotient and the extension is nonsplit; no invariant direct-sum hardware register is inferred.

## Public-site integration

Landed standalone theorem pages:

- `docs/line-signing-apartment-parity.html`
- `docs/apartment-h10-geometric-readout.html`
- `docs/apartment-core-self-gluing.html`

The canonical public-extension registry now contains additive cards for the 4469–4471 bridge, the parallel 4472–4479 packet, the 4480–4483 readout continuation, and the 4485–4488 nonsplitting/self-gluing packet.  A safe `docs/index.html` reconciler workflow is present.  As of this report, the connector has **not surfaced a bot commit materializing the newly registered cards into the giant `docs/index.html`**, so literal index materialization remains unconfirmed and must not be reported as complete.

## Rediscovery guard after the hidden-corpus repair

During this work a parallel maintenance commit exposed 1,793 research files that a generic Python-template `parts/` ignore rule had hidden from Git for the life of the project.  That changed the rediscovery surface materially.  Targeted searches against the newly visible corpus for the exact `N^T N -> H10` bridge, `U/J` apartment self-gluing and nonsplitting formulation did not reveal an earlier occurrence; broad code search was intermittently unavailable/502 during the audit.  The defensible statement remains **“no occurrence found in the searched repository/source corpus,” not “proved novel.”**

Relevant primary-source background searches include Chandler–Sin–Xiang on finite symplectic incidence modules and Crnković–Hawtin–Švob on generalized-quadrangle codes.  They provide the correct literature lane but the searched sources did not display this exact apartment-parity quotient bridge.

## Physical and interpretive boundaries

This packet does not establish:

- a second physical CSS code or new logical-qubit species;
- an implemented transvection gate;
- ten physical measurements replacing apartment-syndrome acquisition;
- E8 dynamics in the radical copy;
- a four-qubit hardware implementation merely because the protected 8-core has a four-Pauli phase-space realization;
- a particle interpretation of modular dimensions `8,6,1,14`;
- an explanation of empirical line-signing/Ramanujan success percentages;
- a symmetry-preserving direct-sum separation of radical and protected sectors (Pass 4488 proves the opposite).

## Evidence files

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

Focused regression/evidence workflows:

- `.github/workflows/w33_pass4469_4473_apartment_h10_bridge.yml`
- `.github/workflows/w33_pass4480_4484_apartment_h10_continuation.yml`
- `.github/workflows/w33_pass4485_4489_apartment_core_self_gluing.yml`
