# Pass 4950 — quarantine of the false 33-vertex W33 packet

## Verdict

The landed `PASS4801_4812_SRG_CONSTELLATION_BREAKTHROUGH.md` packet is not a
provisional interpretation of W33.  Its foundational graph does not exist.
For a strongly regular graph, the parameters must satisfy

\[
  (v-k-1)\mu=k(k-\lambda-1).
\]

The proposed \((33,8,2,2)\) values give

\[
  (33-8-1)2=48,
  \qquad
  8(8-2-1)=40.
\]

Since \(48\ne40\), there is no
\(\operatorname{SRG}(33,8,2,2)\).  Every theorem in the packet that depends on
that graph—including the 7-point completion, spectral tower, critical-group
map, Fano obstruction, and physics consequences—therefore has no object.

## Independent group firewall

Native GAP also closes the proposed group route independently.  In its natural
degree-33 projective-line action,

\[
  |PSL(2,32)|=32{,}736,
  \qquad
  \text{point subdegrees }[1,32].
\]

The action is 2-transitive, so a graph invariant under it is either empty or
complete; an invariant 8-regular graph is impossible.  Moreover,

\[
  32{,}736\nmid51{,}840=|Sp(4,3)|,
\]

so the claimed subgroup embedding cannot exist.  GAP further verifies that
\(SU(2,32)\) and \(PSL(2,32)\) both have order 32,736 and are isomorphic, so
the packet's proposed proper unitary inclusion does not create a second group.

The stated spectrum fails independently as well.  Eigenvalues
\(8,\sqrt6,-\sqrt6\) on 33 vertices would require an integral multiplicity
difference \(d\) satisfying \(6d^2=64\), and no such integer exists.

## Canonical replacement

The same witness rebuilds W33 from the four-dimensional symplectic space over
\(\mathbf F_3\).  The actual point-collinearity graph has

\[
  \operatorname{SRG}(40,12,2,4),
  \qquad |PSp(4,3)|=25{,}920,
  \qquad |PGSp(4,3)|=51{,}840.
\]

This agrees with the repository's long-standing certified carrier.  Canonical
Passes 4801--4812 remain owned by their earlier committed artifacts; the false
packet did not acquire those numbers by reusing them in filenames.

## Disposition and evidence

The three invalid artifacts are removed from the active corpus:

- `PASS4801_4812_SRG_CONSTELLATION_BREAKTHROUGH.md`
- `PASS4801_gap_verification.g`
- `analysis/PASS4801_4812_srg_constellation_insert.tex`

Their provenance and refutation remain visible here and in:

- GAP owner: `analysis/w33_pass4950_false_srg33_w33_quarantine.g`
- frozen certificate: `data/PART_W33_PASS4950_FALSE_SRG33_QUARANTINE.json`
- regression: `tests/test_w33_pass4950_false_srg33_quarantine.py`
- native result: `19/19 checks; status=PASS`

## Boundary

This is an exact falsification and corpus-repair result.  It does not classify
all strongly regular graphs, derive physics from the genuine W33 graph, or
turn the numerical difference \(40-33=7\) into a Fano-plane construction.
