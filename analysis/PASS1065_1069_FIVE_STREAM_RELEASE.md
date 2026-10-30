# Passes 1065--1069: cocycle, outer lift, two geometries, CHEVIE inclusion, and executable photonic protocol

## Release status

All five requested directions were executed against the live post-Pass-1064 `master` frontier.

- Exact executable checks: **65/65 PASS**.
- Focused release regression: **7 pytest tests passed in 0.03 s**.
- The five heavyweight certificates are isolated into separate CI jobs so one enumeration is not redundantly repeated by pytest.
- No physical experiment was run; Pass 1069 is executable control/analysis software with synthetic blinded fixtures.

## Pass 1065 — explicit Schur cocycle

Use the canonical projective section

\[
s([M])=\min_{\rm lex}\{M,-M\}\subset Sp(4,3)
\]

and define

\[
c(g,h)=\begin{cases}
0,&s(g)s(h)=s(gh),\\
1,&s(g)s(h)=-s(gh).
\end{cases}
\]

The witness enumerates all `51840` matrices of `Sp(4,3)` and the corresponding signed permutations of the `240` E8 roots in Cayley-graph lockstep. The quotient has `25920` projective classes and kernel exactly global root negation. It checks `648000` cocycle identities and `259200` generator transitions.

A shortest detected positive-generator word of length `10` projects to the identity but lifts to `-I`, and acts on the roots as the global antipodal map. Therefore the cocycle is nonzero. Since `PSp(4,3) ~= U4(2)` is perfect and its Schur multiplier has order two, the class generates `H^2(PSp(4,3),C2)`.

The finite Maslov/metaplectic comparison is intentionally at extension-class level: any nontrivial normalized Maslov cocycle represents the same unique nonzero class, although its pointwise values can differ from this matrix section by a coboundary.

Primary external anchor: the official ATLAS entry for `U4(2)` records order `25920`, multiplier `2`, outer automorphism order `2`, and identifies the double cover with `Sp4(3)`.

## Pass 1066 — lift of the outer W(E6) involution

The order-`51840` signed cover is normalized by lifts of the outer `PGSp(4,3)/PSp(4,3)` involution. Either outer-involution class generates the same group of order

\[
103680=2\cdot 51840.
\]

The extension has center order `2` and derived subgroup order `51840`. Its behavior is class-dependent:

| unsigned class | inner centralizer | signed lift | square | signed-root cycles |
|---:|---:|---:|---|---|
| 36 | 720 | order 4 | global antipode | `4^60` |
| 540 | 48 | order 2 | identity | `1^8 2^116` |

The `540`-class involution supplies a section of the outer quotient, so the full order-`103680` group is a **split** extension `Sp(4,3) semidirect C2`. Nevertheless, the `36`-class has localized pin-like behavior: neither preimage is an involution; both have order four and square to the central antipode.

The two signed conjugacy classes have sizes `72` and `1080`, respectively, and each contains both lifts `T` and `-T`. No unverified ATLAS suffix is assigned to the explicit double cover.

## Pass 1067 — exact geometry of both outer classes

An independent exact-cover search finds exactly `36` spreads of `W(3,3)`.

For every element in the outer class of size `36`:

- it fixes no point;
- it fixes exactly ten lines;
- those ten lines are pairwise disjoint and cover all forty points.

The map

\[
t\longmapsto \operatorname{Fix}_{\rm lines}(t)
\]

is a bijection from the `36` outer involutions to the `36` spreads.

For every element in the outer class of size `540`:

- it fixes eight points and six lines;
- the line-intersection graph of those six lines is `K_{2,4}`;
- the two degree-four lines are disjoint hubs;
- the other four lines are pairwise-disjoint common transversals;
- the eight hub–transversal intersections are exactly the fixed points.

There are exactly `540` unordered disjoint-line pairs, and each pair has exactly four pairwise-disjoint common transversals. The two hub lines therefore give an equivariant bijection between the `540` involutions and all disjoint-line pairs.

This unifies two formerly separate repository counts:

\[
36\leftrightarrow\text{spreads},\qquad
540\leftrightarrow\text{disjoint-line/transversal frames}.
\]

They are the two outer-involution orbits of the same `PGSp(4,3)` extension, with stabilizers `720` and `48`.

## Pass 1068 — explicit CHEVIE matrix inclusion G25 < G32

Let `omega^2+omega+1=0`. In the standard CHEVIE reflection basis, define

\[
R_v=I+(\omega-1)\frac{vv^*}{\langle v,v\rangle}
\]

for the four directions

\[
(0,0,-1,0),\ (1,1,1,0),\ (0,1,0,0),\ (1,-1,0,-1).
\]

The four matrices are rank-one reflections of order three. Adjacent generators satisfy the length-three braid relation and nonadjacent generators commute.

The first three generators fix `e4` pointwise. Their upper-left `3 x 3` blocks are exactly the CHEVIE `G25` generators. With

\[
J=\begin{pmatrix}I_3\\0\end{pmatrix}:\mathbb C^3\hookrightarrow\mathbb C^4,
\]

one has, generator by generator,

\[
R_iJ=Jr_i\qquad(i=1,2,3).
\]

Thus the conjugator in the standard CHEVIE bases is the identity/block inclusion—not a numerically fitted matrix.

Exact `Q(omega)` arithmetic checks all reflection and braid relations. Independent reduction modulo `7`, with `omega -> 2`, enumerates

\[
|G_{25}|=648,\qquad |G_{32}|=155520,
\]

and proves that the pointwise `e4` stabilizer in `G32` has order `648` and equals the embedded `G25`. The degree products `6*9*12` and `12*18*24*30` match the group orders.

Primary external anchors: CHEVIE’s standard complex-reflection data for `G25` and `G32`; the repository witness reconstructs and verifies the matrices independently.

## Pass 1069 — defect-aware photonic compiler and analyzer

The Pass-1064 preregistration is now executable.

### Control compiler

The compiler emits a forty-row movable-defect macro schedule, one row for each point-star gauge. Each gauge cycle expands to:

1. vacuum/dark calibration;
2. bright-reference calibration;
3. all `36` nonstar contexts;
4. the four contexts in the selected movable point-star.

Every context expands into four binary projector/no-click interrogation blocks. The macro therefore expands to

\[
40\bigl(2+40\cdot4\bigr)=6480
\]

elementary operations. This numerical equality with any other repository `6480` count is explicitly recorded as arithmetic only, not as a new structural theorem.

Each calibrated group permutation is compiled into an exact transposition/EOM swap network and reconstructed as a regression check. The primary central-`C3` arm contributes eight frozen process sequences: four orderings for each of the two central candidates.

### Analysis engine

The analyzer freezes:

- dark-rate, efficiency, and detector-imbalance gates;
- context-stratified parametric bootstrap with a fixed seed;
- noncontextual witness bound `7`;
- central-`C3` thresholds `<=9`, `10--17`, and `>=18`;
- a fail-closed joint decision matrix.

Four blinded synthetic fixtures exercise all four conclusive branches:

1. contextual + point/Hessian;
2. noncontextual + point/Hessian;
3. contextual + dual;
4. noncontextual + dual.

A fifth regression corrupts the dark calibration and is forced to `inconclusive_no_claim`. The committed blinding key is labeled synthetic-fixture-only; real acquisition requires an external key and hardware calibration identifiers.

No acquisition time, optical angle, achieved efficiency, or physical statistical power is claimed.

## Verification

Machine-readable results:

- `data/w33_pass1065_schur_cocycle.json`
- `data/w33_pass1066_outer_lift.json`
- `data/w33_pass1067_outer_class_geometry.json`
- `data/w33_pass1068_chevie_g25_g32_matrices.json`
- `data/w33_pass1069_photonic_pipeline.json`

Executable witnesses:

- `analysis/w33_pass1065_schur_cocycle.py`
- `analysis/w33_pass1066_outer_lift.py`
- `analysis/w33_pass1067_outer_class_geometry.py`
- `analysis/w33_pass1068_chevie_g25_g32_matrices.py`
- `analysis/w33_pass1069_photonic_protocol_compiler.py`

Hardware-facing artifacts:

- `hardware/w33_pass1069_photonic_manifest.json`
- `hardware/w33_pass1069_control_schedule.csv`
- `hardware/w33_pass1069_synthetic_blinded.json`
- `hardware/w33_pass1069_synthetic_key.json`

The committed manifest and blinded fixture are compact control/index surfaces. Running the compiler regenerates the expanded exact candidate banks, sequence maps, context tables, and raw synthetic shot records.

Regression:

- `tests/test_w33_pass1065_1069.py`
- `.github/workflows/pass1065_1069_exact.yml`
