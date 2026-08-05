# Passes 3628–3634 — octad pattern census, Borel core/bridge reduction, matrix units, proof batching, and marked tomography

## Exact status

The exact verifier reports

```text
PASS_7_FRONTS 58b7e205ee0a1409230d50df6efc3abe8d67caf3125b9eaa654dd6600b7b1d25
```

The independently checkable proof batch reports

```text
PASS_REAL_STAR_BATCH c176539c7b944274fb64965275ce3f900852fe4b26f67923b2ca6a2f06e256a4
```

The focused local regression reports `6 passed`. This packet executes the five continuations from Passes 3577–3583 plus two additional high-risk constructions. It does not claim a degree-57 Moore graph, a SAT/UNSAT verdict for either Borel profile, a complete realized K8 octad orbit census, or the complete 3,720-instance proof archive.

---

## 3628 — complete abstract S8 octad pattern census

Let eight one-factorizations have pairwise intersection exactly one perfect matching. A matching occurring in at least three factorization rows determines a clique on those row labels. Distinct such cliques are edge-disjoint, because a row pair cannot share two matchings. Every uncovered row pair is a multiplicity-two matching. Thus the multiplicity pattern is equivalent to an edge-disjoint clique packing of K8 with block sizes 3 through 8, modulo S8.

Canonical augmentation exhausts this abstract pattern space. The number of S8 orbits by number r of nontrivial blocks is

\[
1,6,10,10,13,14,8,6,1
\]

for \(r=0,1,\ldots,8\), respectively. Therefore

\[
\boxed{69}
\]

abstract pair-intersection multiplicity patterns exist. Their representative digest is

```text
de3df6847357d549deb11cea22cb40e32dbd193f7be3dd1386030cdb585a2ea4
```

The maximum triple-coincidence excess is

\[
\binom83=56,
\]

attained by the sunflower common-core pattern.

**Boundary:** this is a complete abstract pattern census. Realizability by actual K8 one-factorizations, and the number of realization orbits over each abstract pattern, remain a larger exact computation. The exact background remains 105 perfect matchings and 6,240 labelled one-factorizations.

---

## 3629 — the common 30,771-variable Petersen core

The Petersen-spine presolve is strengthened from a raw equality of 30,870 residual orbit variables to a literal shared binary core.

The common variable classes are

\[
18\cdot85=1530
\]

regular-orbit internal variables,

\[
\binom{18}{2}\cdot171=26163
\]

regular–regular variables, and

\[
9\cdot18\cdot19=3\cdot18\cdot57=3078
\]

small–regular variables. Hence

\[
\boxed{1530+26163+3078=30771}.
\]

For P19, all remaining thick small-orbit channels are forced zero after the Petersen spine, leaving exactly 30,771 variables.

For P57, eighteen nonneighbor–nonneighbor thick channels survive in addition to the common core, leaving

\[
\boxed{30789=30771+18}.
\]

The solver contract digest is

```text
220f6a3a66801ce08bd18a597e9df669f256c6cec94442ba09de3f308d1aa298
```

The model retains exact lazy common-neighbor separators on ordered-pair orbital representatives.

**Boundary:** this is a solver-ready exact presolve/decomposition, not a SAT or UNSAT result.

---

## 3630 — explicit matrix units and positive cone for the Perkel conductor

The constructive representation of the conductor-19 component is upgraded from twenty-one orbital matrices to a complete matrix-unit basis in

\[
M_3\!\left(\mathbb Q(\sqrt{-19})\right).
\]

There are nine units \(E_{ij}\) and nine field units \(sE_{ij}\), with \(s^2=-19\), satisfying

\[
E_{ij}E_{kl}=\delta_{jk}E_{il},
\qquad
(sE_{ij})(sE_{kl})=-19\delta_{jk}E_{il}.
\]

The conversion to the orbital basis has 315 nonzero rational coefficients, maximum denominator 133, and digest

```text
e9d441ac71aeaffe498936989909f7d1170d84826e8a4c2485a6ecf03cdfd98a
```

The transpose involution is represented by the positive Hermitian form

\[
H=
\begin{pmatrix}
1&2s/19&-2s/19\\
-2s/19&1&2s/19\\
2s/19&-2s/19&1
\end{pmatrix}.
\]

Its eigenvalues are

\[
1,
\qquad
1-\frac{2\sqrt{57}}{19},
\qquad
1+\frac{2\sqrt{57}}{19},
\]

all positive. Every two-by-two principal minor equals

\[
\boxed{15/19},
\]

and

\[
\boxed{\det H=7/19}.
\]

For a transpose-symmetric conductor element \(X\), the matrix \(H\rho(X)\) is Hermitian. Positivity of \(X\) on this module is therefore exactly equivalent to nonnegativity of its principal minors.

---

## 3631 — sixteen real proof-carrying star-complement instances

The proof-DAG archive is expanded from one genuine canary to sixteen deterministic genuine spectral survivors. Every frozen record contains the complete compatibility adjacency bitsets, a maximum-clique witness, and the independently checkable upper-bound proof DAG.

The compatibility graph sizes range from

\[
48\text{ to }159.
\]

The exact maximum-clique histogram is

\[
\boxed{8^1,9^1,10^1,11^3,12^1,13^2,16^2,31^5}.
\]

The ordered record Merkle root is

```text
c176539c7b944274fb64965275ce3f900852fe4b26f67923b2ca6a2f06e256a4
```

The compressed frozen payload is split into six repository parts and reconstructed before checking. Every proof digest and record digest is independently recomputed.

**Boundary:** this is a genuine multi-instance proof archive, not the complete canonical 3,720-instance archive. Some larger compatibility graphs create deep proof DAGs and require checkpointed per-record resource limits.

---

## 3632 — the minimum geometry-sensitive marked resolvent has rank three

For an SRG, a marked resolvent restricted to a set \(S\) has the form

\[
R_S(z)=a(z)I+b(z)A[S]+c(z)J.
\]

The second determinant coefficient recovers the induced edge count. Markers of size one cannot distinguish W33 from Gewirtz. Markers of size two cannot either, because both graphs contain edges and nonedges.

At size three, W33 has a marked triangle while Gewirtz is triangle-free. Therefore

\[
\boxed{\text{minimum marker size}=3}.
\]

Moreover every W33 triangle decodes a unique K4 line: any adjacent pair has exactly \(\lambda=2\) common neighbors, and those are the other two points of that line.

For a W33 triangle the two marked channels are

\[
r_{\rm std}(z)=\frac{z+1}{(z-2)(z+4)}
\]

with multiplicity two, and

\[
r_{\rm triv}(z)=\frac{z^2-8z-36}{(z-12)(z-2)(z+4)}.
\]

This crosses the spectrum-only boundary with the smallest possible marker.

---

## 3633 BONKERS — P57 is an exact rank-18 extension of P19's core

The two Borel fronts are not merely equal-dimensional after thin-variable removal. They possess a common 30,771-variable binary core, and P57 has exactly eighteen additional nonneighbor bridge variables:

\[
\boxed{P_{57}=P_{19}^{\rm core}\oplus\mathbb F_2^{18}}
\]

at the variable-contract level. This gives a direct paired-solver strategy: solve the common core once and branch only on an eighteen-bit extension for P57.

---

## 3634 BONKERS — exact Gram arithmetic in the conductor-19 field

The invariant positive form has the unusually rigid principal-minor data

\[
H[ij]=15/19
\]

for every two-coordinate principal minor and

\[
\det H=7/19.
\]

These are exact arithmetic positivity certificates. No physical or numerological mechanism is inferred from them.

---

## Reproduction

```bash
python analysis/bt3628_3634_octad_borel_matrix_proof_tomography.py
python analysis/bt3631_real_star_proof_batch.py --json /tmp/pass3631.json
pytest -q tests/test_bt3628_bt3634_octad_borel_matrix_proof_tomography.py
```

## Evidence firewall

- The degree-57 Moore graph remains open.
- The realized K8 octad orbit census remains open beyond the complete 69-pattern abstract deck.
- Neither Borel profile has a SAT/UNSAT verdict.
- Sixteen proof DAGs are frozen; the full 3,720 archive is not claimed.
- Marked-resolvent results are mathematical graph dynamics, not laboratory measurements.
- No PDF, FPGA, optical, particle, spacetime, or physical claim follows until its dedicated evidence is observed.
