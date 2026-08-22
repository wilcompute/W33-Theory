# Pass7425–7440 — global Eisenstein-leaf geometry and a concrete 2026 Vogel test

## Status

**PASS with explicit external-identification boundaries.**

Executable producers:

- `analysis/w33_pass7425_7432_e8_2240_leaf_geometry.py`
- `analysis/w33_pass7433_7440_e6_vogel_split_casimir.py`

Frozen certificates:

- `data/PART_W33_PASS7425_7432_E8_2240_LEAF_GEOMETRY.json`
- `data/PART_W33_PASS7433_7440_E6_VOGEL_SPLIT_CASIMIR.json`

These passes continue the already-published Pass7401–7424 global A2 scheme. They also audit the substantive parallel commits from 22 August 2026: the corrected Eisenstein 240→40 bridge, the J-stable A2/D4 dictionaries, the 36-spread scheme, and the calibrated q=9 C2/LNS lane.

---

## 1. The 2240 Eisenstein W33 leaves form a rigid global geometry

Pass7401–7408 counted 2240 conjugate Eisenstein W33 leaves from the regular-C3 normalizer. Here the full orbit is explicitly enumerated from the 240 E8 roots and the eight simple reflections.

For a fixed leaf `L`, the intersection sizes with all 2240 leaves are exactly

\[
|L\cap L'|\in\{40,13,4,1,0\}
\]

with multiplicities

\[
\boxed{1,40,390,1080,729}.
\]

Globally the unordered nontrivial pair census is

\[
13^{44800},\qquad4^{436800},\qquad1^{1209600},\qquad0^{816480}.
\]

### Which global A2 relations occur inside a W33 leaf?

The global 1120-A2 association scheme has the orthogonality relation plus three nonorthogonal relations distinguished by common-neighbor counts 10, 16 and 40.

A leaf contains precisely

\[
\boxed{240\text{ orthogonal pairs}+540\text{ }\mu=16\text{ pairs}}
\]

and **no** `mu=10` or `mu=40` pairs.

Moreover every globally orthogonal pair lies in exactly eight leaves and every global `mu=16` pair lies in exactly eight leaves. The other two pair relations lie in none.

If `F` is the `1120 x 2240` A2-versus-leaf incidence matrix, this gives the exact identity

\[
\boxed{FF^T=80I+8(A_{\perp}+A_{16}).}
\]

Using the first eigenmatrix of the Pass7417–7424 A2 Gelfand pair gives

\[
\operatorname{spec}(FF^T)=3200^1\oplus288^{300}\oplus0^{819}.
\]

Hence

\[
\boxed{\operatorname{rank}_{\mathbb R}F=301=1+300.}
\]

The executable replay additionally gives

\[
\boxed{\operatorname{rank}_{\mathbb F_2}F=\operatorname{rank}_{\mathbb F_3}F=301.}
\]

After the constant component is removed, the columns therefore form a tight frame spanning **exactly the 300-dimensional irreducible constituent** of the 1120-point A2 Gelfand pair.

---

## 2. The leaf-overlap graph is distance-regular

Join two leaves when their intersection contains 13 A2 subsystems.

The resulting graph has

\[
\boxed{2240\text{ vertices},\qquad k=40}
\]

and is bipartite of diameter four. Its distance partition is

\[
\boxed{1,40,390,1080,729}
\]

and its intersection array is

\[
\boxed{\{40,39,36,27;1,4,13,40\}.}
\]

Distance and A2-overlap are the same invariant:

\[
d=0,1,2,3,4
\quad\Longleftrightarrow\quad
|L\cap L'|=40,13,4,1,0.
\]

Its spectrum is

\[
\boxed{40^1\oplus12^{300}\oplus0^{1638}\oplus(-12)^{300}\oplus(-40)^1.}
\]

Each bipartition half has 1120 vertices. The halved graph is

\[
\boxed{\operatorname{SRG}(1120,390,146,130)}
\]

with spectrum

\[
390^1\oplus26^{300}\oplus(-10)^{819}.
\]

### Local reconstruction of W33 from neighboring leaves

Fix a leaf `L`. Its 40 adjacent leaves meet `L` in 40 thirteen-subsets. Those subsets are **exactly**

\[
\boxed{\{p\}\cup p^\perp,\qquad p\in W(3,3),}
\]

the 40 closed neighborhoods of the internal W33 graph.

Thus the 40-point geometry is visible not merely *inside* an Eisenstein leaf but through how that leaf meets its 40 nearest neighboring complex structures.

### Spectral projector polynomial

Let `A` be the adjacency matrix of the 2240-leaf graph. From the distance-polynomial recurrence and the overlap values,

\[
F^TF=40I+13A_1+4A_2+A_3
\]

reduces to

\[
\boxed{F^TF=\frac1{52}A(A+12I)(A+40I).}
\]

Consequently the A2 incidence annihilates the `0,-12,-40` eigenspaces and retains precisely `40^1 + 12^300`; centering kills the trivial 40-space and leaves only the positive 12-eigenspace of dimension 300.

### External graph boundary

Current graph databases/documentation contain a 1120-vertex dual-polar graph `DSp(6,3)` / `OrthogonalDualPolarGraph(0,3,3)` with intersection array

\[
\{39,36,27;1,4,13\}.
\]

Its extended-bipartite-double construction has the same numerical pattern as the new 2240 graph. This is a strong identification target, **not yet an isomorphism theorem here**: no explicit E8-leaf ↔ polar-space map is frozen in this pass.

---

## 3. A real 2026 Vogel test: E6 `27 x 78`

The old `VOGEL_SYNTHESIS_COMPLETE.md` contains speculative suggestions that the repo's characteristic-3 648-dimensional quotient might be a new Vogel-plane object. Those suggestions remain unproved.

The new literature gives a much cleaner target. A. P. Isaev, *Vogel universality and beyond*, arXiv:2601.01612 (2026), derives split-Casimir characteristic identities and invariant projectors for `T x Y_n`; for exceptional algebras `T` is the minimal fundamental representation. The E6 case directly matches this repo's established 27-dimensional minuscule/Schlaefli carrier.

Rebuilding E6 solely from the repo Cartan matrix gives fundamental dimensions

\[
27,351,2925,351,27,78.
\]

At `n=1`, Weyl's dimension formula verifies

\[
\boxed{27\otimes78=1728\oplus27\oplus351.}
\]

The quadratic Casimirs in the normalization `C_2(ad)=24` are

\[
C_2(27)=\frac{52}{3},\quad
C_2(78)=24,\quad
C_2(1728)=\frac{130}{3},\quad
C_2(351)=\frac{100}{3}.
\]

Therefore the normalized split Casimir

\[
\widehat C=\frac{C_2(R)-C_2(27)-C_2(78)}{2C_2(78)}
\]

has eigenvalues

\[
\boxed{\frac1{24},\quad-\frac12,\quad-\frac16},
\]

exactly the `n=1` E6 specialization of Isaev's formulas.

Hence

\[
\boxed{(\widehat C-1/24)(\widehat C+1/2)(\widehat C+1/6)=0.}
\]

The three invariant projectors are explicitly

\[
P_{1728}=\frac{576}{65}(\widehat C+1/2)(\widehat C+1/6),
\]

\[
P_{27}=\frac{72}{13}(\widehat C-1/24)(\widehat C+1/6),
\]

\[
P_{351}=-\frac{72}{5}(\widehat C-1/24)(\widehat C+1/2).
\]

The trace moments also reproduce

\[
\boxed{\operatorname{Tr}\widehat C^3=-\frac14\operatorname{Tr}\widehat C^2}.
\]

This is the first current Vogel result in the repo that is tied to the frontier by an actual characteristic operator and projector calculus rather than a shared dimension.

### Vogel boundaries

- Isaev's 2026 `T x Y_n` exceptional formula explicitly excludes E8; E8's smallest nontrivial fundamental representation is already the adjoint, so this particular extension beyond the usual adjoint Vogel setting does not supply an E8 analogue.
- The 648-dimensional characteristic-3 quotient is **not** identified by this calculation. A future claim would require its actual bracket, Killing/Casimir data and representation theory to match a universal object.
- The May 2026 revival of Vogel's diagrammatic `Lambda`-algebra by Khudoteplov and Sleptsov is relevant as a second, diagrammatic test bed, but no repo diagrammatic weight system has yet been constructed.

---

## Parallel-commit audit incorporated

The pass explicitly preserves the following same-day corrections and advances:

1. the false `33=27+6` W33 interpretation is superseded by the machine-verified Eisenstein `240 -> 40` bridge;
2. the 40 W33 points are J-stable A2 root subsystems and W33 lines are A2^4 subsystems;
3. the 90 selected D4s are the J-stable D4s and form four-point partial-ovoid charts, not W33 lines;
4. the 36-spread/double-six bridge already exists in Pass4992–4999 and is not reclaimed;
5. the calibrated q=9 lane proves the current 51-set has stabilizer exactly C2 but leaves `alpha(W(3,9))` open.

## Evidence boundary

All new promoted statements are deterministic finite root-system, incidence, graph, representation or Casimir computations. Named external graph identifications remain candidates until an explicit map is built. No Standard Model, coupling, hardware, q=9 optimality, or new modular-Vogel-algebra claim follows from this packet.
