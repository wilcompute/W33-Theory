# Passes 3577–3583 — the Petersen spine, constructive Perkel matrix units, octad phases, and marked quantum walks

## Status

The exact verifier reports

```text
PASS_7_FRONTS 2a4a06836164c6eb92d971aa18ecd1369990c7bf501ae1aaf342e7b5e5bc23a4
```

The independent real proof-carrying canary reports

```text
PASS_REAL_STAR_PROOF_CANARY 2a984b9a2f51646691657a8dfe5d01b9e33496f75500ba9b79abdd5a68385390
```

This packet executes the five continuations from Passes 3549–3555 and two additional high-risk constructions. The degree-57 Moore graph remains open; no complete Borel-model solver verdict, all-octad orbit census, or all-3,720 proof archive is claimed.

---

## 3577 — the Borel quotient has a forced Petersen spine

Let

\[
B=C_{19}\rtimes C_9,
\qquad
(b,m)(c,n)=(b+4^m c,m+n).
\]

The relevant transitive B-sets have stabilizers \(B,C_9,C_3,1\) and sizes \(1,19,57,171\). Exact double-coset calculation gives

\[
C_9\backslash B/C_9:\quad1,9,9,
\]

and

\[
C_3\backslash B/C_3:\quad1,1,1,3^{18}.
\]

For profile \(P_{19}=1+9\cdot19+18\cdot171\), degree residues force the three neighbor size-19 orbits to have singleton degree two and the six nonneighbor size-19 orbits singleton degree three. Together with the fixed vertex this is a cubic graph on ten fixed points; the unique-common-neighbor and girth constraints force the Petersen graph.

For profile \(P_{57}=1+3\cdot57+18\cdot171\), the fixed vertex is adjacent to three \(C_3\)-fixed points and the singleton suborbits between the three size-57 orbits again complete a cubic ten-vertex Petersen graph. Thus both profiles possess the same forced fixed-set skeleton before any large solver search.

## 3578 — a constructive \(3\times3\) model over \(\mathbb Q(\sqrt{-19})\)

The Perkel orbital algebra has rank 21. Its conductor-19 simple component has rational dimension 18 and is abstractly \(M_3(\mathbb Q(\sqrt{-19}))\). Let \(e\) be the rank-18 primitive idempotent from the \(-3\) eigenspace inside the conductor-19 sector. The right ideal \(\mathcal A e\) has dimension six over \(\mathbb Q\), hence dimension three over \(K=\mathbb Q(\sqrt{-19})\).

The central Paley operator satisfies \(D^2=-19E_{54}\), supplying the field generator. Every orbital is represented by a \(3\times3\) matrix with entries \(a+b\sqrt{-19}\). The model has 171 nonzero entries, maximum denominator 14, exact agreement on all \(21^2=441\) products, and digest

```text
366405ad8400779a79eb6b92437b6d354ad3019eb16e9b5a81b99c5adc77eb33
```

The first three matrices are \(I_3\) and the two three-cycle permutation matrices. The decomposition is therefore a literal faithful matrix realization rather than only a dimension statement.

## 3579 — the \(K_8\) octad splits into inequivalent phases

The exact census contains 105 perfect matchings and 6,240 labelled one-factorizations of \(K_8\). Two size-eight pairwise-one-intersection families were certified and proved inequivalent under \(S_8\).

The sunflower phase has one common matching, incidence profile \(8^1 1^{48}\), trivial stabilizer, orbit size 40,320, and canonical digest

```text
18f69827ed166cc1e987f7dfa49dec4320c43fbf7765ab315e01ae560fddeb81
```

The mixed phase has empty common core, matching multiplicities \(4^1 3^2 2^{16}1^{14}\), stabilizer four, orbit size 10,080, and digest

```text
85b3249861063429a6b968446163800643cda7379042d2b6e042524c2abdfb40
```

Its compiled graph has 82 vertices, degree nine, diameter three, 76 triangles, and 375 four-cycles. These phases prove nonuniqueness but do not constitute the complete \(S_8\)-orbit census.

## 3580 — a real proof-carrying star-complement canary

The independent star-complement source regenerates the first two canonical extension stages \(22,784\). A deterministic random stream with seed 3559 locates a genuine third-stage spectral survivor after 106 draws and 37 valid candidates, with second-largest eigenvalue approximately \(1.8890814415<2\).

The exact compatibility graph has 52 vertices and maximum clique

\[
\boxed{11}.
\]

The witness carries an independently checked upper-bound proof DAG:

```text
proof  a07611183bd01fad1b60134aebba7dc3a8ec0ce7bc29fd7c46ea8c4146010b50
record 2a984b9a2f51646691657a8dfe5d01b9e33496f75500ba9b79abdd5a68385390
```

The canary is a genuine spectral survivor but is not assigned a canonical index in the complete 3,720 ledger.

## 3581 — marked resolvents cross the spectrum-only boundary

For an SRG,

\[
(zI-A)^{-1}=a(z)I+b(z)A+c(z)J.
\]

W33 and Gewirtz share

\[
a(z)=\frac{z+2}{(z-2)(z+4)},\qquad b(z)=\frac1{(z-2)(z+4)},
\]

while their \(J\)-channels retain degrees 12 and 10. For a marked set \(S\), \(R_S(z)=aI+bA[S]+cJ\). The second coefficient of \(\det(I-\tau R_S)\) contains \(-e(S)b(b+2c)\), so the induced edge count is exactly recoverable.

A W33 line is a marked \(K_4\) with six edges. Every four-set in the triangle-free Gewirtz graph has at most four. The rank-four marker therefore detects geometry that unmarked analytic functions cannot. For a W33 line the determinant ratio is

\[
\left(1-\tau\frac{z-11}{(z-12)(z-2)}\right)
\left(1-\tau\frac{z+1}{(z-2)(z+4)}\right)^3.
\]

## 3582 BONKERS — both Borel profiles leave exactly 30,870 variables

The Petersen spine fixes every thin variable. For \(P_{19}\), it fixes \(9+\binom92=45\), so \(30915-45=30870\). For \(P_{57}\), it fixes \(3+3\cdot3+3=15\), so \(30885-15=30870\). Hence

\[
\boxed{P_{19}\text{ and }P_{57}\text{ have the same residual dimension }30870}.
\]

This equality is invisible in the raw Burnside counts.

## 3583 BONKERS — a triangle-free graph with the Moore order but wrong curvature

The sunflower compiles to a degree-nine graph on

\[
82=1+9+9\cdot8
\]

vertices, the numerical Moore bound for degree nine. It is triangle-free but has diameter three, 3,024 four-cycles, 1,728 nonadjacent pairs with zero common neighbors, 936 with one, and 288 with seven. Its characteristic polynomial is

\[
(x-9)(x-8)^3(x-1)^{32}(x+1)^{24}(x+8)^4(x^2+x-8)^9.
\]

It satisfies the order and regularity shell while redistributing the unique-common-neighbor law into uncovered and sevenfold-overcoupled sectors. Order saturation and triangle-freeness are not sufficient; uniform \(\mu=1\) is the decisive curvature.

## Reproduction

```bash
python analysis/bt3577_3583_petersen_matrix_octad_marked_walk.py
python analysis/bt3580_star_proof_canary.py --json evidence/pass3577_3583/canary.json
pytest -q tests/test_bt3577_bt3583_petersen_matrix_octad_marked_walk.py
```

## Claim boundaries

- The degree-57 Moore graph remains open.
- The Petersen-spine models are exact presolve reductions, not SAT/UNSAT verdicts.
- Two inequivalent K8 octad phases are proved; the complete orbit classification is not claimed.
- One genuine proof-carrying spectral survivor is executed; the complete 3,720 archive is not claimed.
- Marked-resolvent formulas are mathematical graph dynamics, not measured hardware behavior.
