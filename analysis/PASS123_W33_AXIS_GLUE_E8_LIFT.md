# Pass 104 — W33 Local Axes Are the Anisotropic \(E_8/2E_8\) Root Lines

## Result

Pass 104 closes the object-level gap left by the earlier axis spectral bridge
and Passes 92/101:

\[
\boxed{
\{\text{120 W33 local pencil-octahedron axes}\}
\;\longrightarrow\;
\{x\in C^\perp/C:Q(x)=1\}
\;\xrightarrow[\cong]{\text{quadratic isometry}}\;
\{\pm\alpha:\alpha\in\Phi(E_8)\}.
}
\]

The first arrow is intrinsic.  At a W33 point \(p\), an axis partitions the
four lines through \(p\) into two line-pairs.  For either endpoint
\(\{L_i,L_j\}\), define

\[
h(p;L_i,L_j)=(L_i\cup L_j)\setminus\{p\}.
\]

This is a six-point support and hence a weight-6 binary word.  If
\(\{L_k,L_\ell\}\) is the opposite endpoint, then

\[
h(p;L_i,L_j)+h(p;L_k,L_\ell)=N(p)\in C,
\]

where \(N(p)\) is the 12-neighbor word of \(p\), a row of the W33 adjacency
matrix.  Therefore the two endpoints determine one class in \(C^\perp/C\).
The 120 axes give 120 distinct classes, all anisotropic.

The earlier W33 axis graph and the Pass 101 glue graph are not only
cospectral:

\[
A_{\rm axis}(a,b)=1
\iff
B([h_a],[h_b])=0.
\]

The verifier checks equality of all \(120^2\) adjacency entries.

## Exact \(E_8\) lift

The script uses the existing W33-derived tetracode \(E_8\) coordinates from
`analysis/w33_tetracode_e8_root_system_bridge.py`.  It extracts the exact
simple-root basis, reduces the lattice modulo \(2\), constructs hyperbolic
bases for both eight-dimensional plus-type quadratic spaces, and obtains an
explicit linear isometry

\[
T:C^\perp/C\longrightarrow E_8/2E_8.
\]

Exhaustive checks over all 256 vectors and all \(256^2\) ordered pairs give:

- quadratic-form failures: \(0\);
- bilinear-form failures: \(0\);
- 120 distinct anisotropic images;
- all 120 antipodal \(E_8\) root lines;
- entrywise equality with the \(E_8\) root-line orthogonality graph
  \(\operatorname{SRG}(120,63,30,36)\);
- all 240 signed roots after choosing the existing chamber;
- ordered Gram profile
  \[
  \{-2:240,\,-1:13440,\,0:30240,\,1:13440,\,2:240\}.
  \]

The published graph-theory identification agrees with this certificate:
Schmidt defines the orthogonality graph on the 120 antipodal \(E_8\) root
lines and records the same parameters
\(\operatorname{SRG}(120,63,30,36)\)
([Algebraic Combinatorics 7 (2024), 515–528](https://doi.org/10.5802/alco.335)).
The 120-ray interpretation of the 240 roots is also used by Waegell and
Aravind in their \(E_8\) Kochen–Specker construction
([arXiv:1502.04350](https://arxiv.org/abs/1502.04350)).

## What changed after the two-day GitKraken audit

The fetched `origin-https/master` history from the previous two days contains
two dense lines of work:

1. Passes 64–97 move through the VM/contextuality, Ihara-zeta, binary-code,
   Construction-A, Smith/critical-group, \(W(E_6)\), and \(E_8/2E_8\)
   arithmetic chain.
2. BT1806–BT1889 develop the Witting transaction runtime and a separate
   selector/tetracode \(E_8\) representative pipeline, including explicit
   representatives, quotient dashboards, phase invariants, and runtime
   mappings.

Repository and Continuity searches then exposed older, decisive facts that
prevented duplicating those commits:

- the exact 240-root tetracode verifier already exists;
- the exact \(E_8\to E_6\times A_2\) coordinate split already exists;
- the 120 local W33 axes and their SRG parameters already exist;
- the edge/root dictionary has an explicit no-go boundary.

The genuinely missing statement was the natural map from a labeled W33 local
axis to a labeled glue class.  Pass 104 supplies that map and composes it with
the exact root coordinates.

## Boundary and correction

This does **not** turn the 240 global edges of W33 into the 240 \(E_8\) roots.
The repository already proves that the W33 line graph has degree 22 whereas
one-threshold \(E_8\) root graphs have degree 56 or 126, and that the relevant
\(W(E_6)\) orbit structures do not support the claimed edge-equivariant map.

The exact 240-element W33 carrier is instead:

\[
40\ \text{points}\times 3\ \text{local axes}\times 2\ \text{axis endpoints}
=240.
\]

The axis-to-coset map is intrinsic.  The displayed rational root coordinates
and the assignment of the two endpoints to \(+\alpha\) and \(-\alpha\) use a
deterministic hyperbolic-basis and chamber gauge; they are explicit but not
canonical under arbitrary relabeling.

## Reproduce

```bash
./.venv/bin/python w33_pass123_axis_glue_e8_lift.py
./.venv/bin/python -m pytest -q tests/test_pass104_axis_glue_e8_lift.py
```

Artifacts:

- `w33_pass123_axis_glue_e8_lift.py`
- `w33_pass123_axis_glue_e8_lift.json`
- `tests/test_pass104_axis_glue_e8_lift.py`
