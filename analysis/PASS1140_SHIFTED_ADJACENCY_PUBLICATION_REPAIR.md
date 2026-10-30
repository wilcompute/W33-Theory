# Pass 1140: Shifted-Adjacency Publication Repair

## Outcome

Pass 1133 established the correct point-carrier functional calculus and
Pass 1137 exposed its reversible complement switch.  Pass 1140 closes the
publication and enforcement gap: the maintained papers, executable
propagator, README, legacy status boundaries, and full-corpus guard now agree.

For the \(W(3,3)\) adjacency matrix \(A\),

\[
D=A-I,\qquad
\operatorname{spec}(D)=11^1\oplus1^{24}\oplus(-5)^{15},
\]

\[
(D-11I)(D-I)(D+5I)=0,
\qquad
\det(I-xD)=(1-11x)(1-x)^{24}(1+5x)^{15}.
\]

The positive generator \(H=D^2\) satisfies

\[
\boxed{H=13I+4\overline A,\qquad
288D=H^2-98H+385I}.
\]

Its heat and unambiguous zeta data are

\[
\operatorname{Tr}(e^{-tH})
=e^{-121t}+24e^{-t}+15e^{-25t},
\]

\[
\zeta_{|D|}(s)=11^{-s}+24+15\,5^{-s},
\qquad
\zeta_H(s)=121^{-s}+24+15\,25^{-s}.
\]

The signed semigroup \(e^{-tD}\) is retained as a separate object and is no
longer called a positive heat kernel.

## Publication repair

- `w33_paper.tex` now proves the exact full-carrier cubic, determinant,
  trace tower, complement switch, positive heat flow, and zeta semantics.
- `W33_FOR_EVERYONE.tex` explains the same theorem as a reversible
  \(240\)-edge/\(540\)-nonedge logic switch. <!-- {540:point-nonedge} -->
- `README.md` now states the correct 28-graph boundary: the explicit
  symplectic construction selects \(W(3,3)\); the SRG parameters do not.
- `W36_PAPER.tex` is visibly labeled a superseded historical synthesis,
  and its spectral chapter and conclusion have been replaced by audited
  finite statements.
- `w33_paper_v2.tex` is visibly labeled a superseded provenance draft and
  routes readers to the maintained surfaces.

No \(32\)-dimensional point-carrier restriction is retained.  Since the
point representation is multiplicity-free \(1\oplus24\oplus15\), such a
restriction is not \(D\)-invariant.

## Executable propagator repair

`analysis/w33_propagator_spectral_action.py` now:

- uses the exact projector numerators
  \[
  (D-I)(D+5I),\quad -(D-11I)(D+5I),\quad
  (D-11I)(D-I)
  \]
  with denominators \(160,60,96\);
- verifies ranks \(1,24,15\);
- emits deterministic JSON with no timestamp;
- distinguishes positive heat, signed semigroup, \(\zeta_{|D|}\), and
  \(\zeta_{D^2}\);
- returns exact rational zeta values at integral arguments.

The corrected trace tower begins

\[
40,-40,520,-520,24040,114200.
\]

## Honest quarantine census

The previous committed report listed only five files.  The rebuilt full
active-corpus audit finds

\[
\boxed{124\ \text{matches}
=124\ \text{explicitly classified}
+0\ \text{unregistered descendants}}.
\]

`data/w33_shifted_adjacency_retraction_ledger.json` explicitly distinguishes
legacy quarantines, corrected comparison artifacts, audit surfaces, the alias
registry, and the formula-search meta-index.  Registration quarantines a file;
it does not validate the historical claim.

The guard now:

- prunes Git, caches, hidden build trees, extracted bundles, and simulation
  output at directory boundaries;
- scans every eligible root-level file plus the active corpus roots;
- detects negative literals without invalid word boundaries;
- avoids redundant Windows/WSL `stat` calls;
- parallelizes only full-release I/O while preserving sorted report order;
- keeps changed-file pre-commit checks sequential and minimal.

The honest pre-merge full run fell from \(8\) minutes \(58\) seconds to
\(26.4\) seconds on the same checkout.

Pass 1144 subsequently supplied four fail-closed primary retraction
records and a four-entry Git-blob manifest.  The merged v3 ledger preserves
the full 129-path classification while adding those exact commit/blob
provenances and honest pending markers.  The mixed MLXXI--MLXXX executable
is labeled `RETRACTED_IN_PART`, matching its certificate: only
MLXXII--MLXXV and MLXXX are retracted by this audit.

## Reproducibility

```text
python3 analysis/w33_propagator_spectral_action.py
python3 scripts/check_shifted_adjacency_descendants.py \
  --write-report data/w33_shifted_adjacency_descendant_audit.json
python3 -m pytest -q tests/test_w33_propagator_spectral_action.py
python3 -m pytest -q \
  tests/test_pass1140_shifted_adjacency_publication_repair.py
```

Verified results:

- corrected propagator regression: `11 passed`;
- Pass 1140 publication/guard regression: `6 passed`;
- full descendant audit after the Pass 1144 merge: `PASS`, summary
  `124/124/0`.

## Scope

This repair establishes the exact finite operator and makes current
publication status honest.  It does not infer anomaly cancellation, a
Standard-Model carrier, masses, couplings, continuum dynamics, or a hardware
implementation from spectral coefficients.
