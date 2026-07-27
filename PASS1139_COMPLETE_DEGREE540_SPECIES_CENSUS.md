# Pass 1139: Complete Degree-540 Species Census

## The theorem

Let \(G=\operatorname{PSp}(4,3)\cong U_4(2)\), of order \(25920\).  A
transitive \(G\)-set of degree \(540\) is \(G/H\) for a subgroup \(H\) of
order \(48\).  GAP 4.12.1 and the \(U_4(2)\) table of marks prove that there
are exactly five conjugacy classes of such subgroups, at TOM positions
\(77,\ldots,81\).  Hence there are exactly five isomorphism classes of
transitive degree-\(540\) \(G\)-sets:

| TOM | \(\operatorname{IdGroup}(H)\) | structure | rank | canonical carrier |
|---:|---:|---|---:|---|
| 77 | \([48,33]\) | \(((C_4\times C_2):C_2):C_3\) | 25 | `{540:point-nonedge}` |
| 78 | \([48,48]\) | \(C_2\times S_4\) | 28 | `{540:double-six-nonincident}` |
| 79 | \([48,49]\) | \(C_2^2\times A_4\) | 27 | `{540:gq42-arc}` |
| 80 | \([48,30]\) | \(A_4:C_4\) | 21 | `{540:outer-4c}` |
| 81 | \([48,48]\) | \(C_2\times S_4\) | 32 | `{540:line-nonedge}` |

The two \(C_2\times S_4\) rows are not conjugate: their normalizers have
orders \(96\) and \(48\), and their coset ranks are \(28\) and \(32\).
Cardinality, stabilizer order, and even abstract stabilizer isomorphism are
therefore insufficient identity tests.

In TOM order \(77,\ldots,81\), the complete joint-rank matrix is

\[
\begin{pmatrix}
25&16&15&15&16\\
16&28&25&20&25\\
15&25&27&20&25\\
15&20&20&21&19\\
16&25&25&19&32
\end{pmatrix}.
\]

Its diagonal is the five-rank fingerprint

\[
\boxed{25,\ 28,\ 27,\ 21,\ 32}.
\]

## The missing rank-28 object

The unique \(S_6\) subgroup at TOM position \(114\) has index \(36\), the
classical carrier of the \(36\) double-sixes of the \(27\) cubic-surface
lines.  In the natural \(27\)-line action its orbits have sizes

\[
12+15=27.
\]

The \(12\)-orbit is the set of lines in a double-six.  Its flag stabilizer is
\(A_5=\operatorname{SmallGroup}(60,5)\), at TOM position \(85\).  The
complementary \(15\)-orbit has stabilizer
\(C_2\times S_4=\operatorname{SmallGroup}(48,48)\), conjugate to TOM
position \(78\).  Therefore the full double-six/cubic-line table splits
equivariantly as

\[
\boxed{
36\cdot27
=36\cdot12+36\cdot15
=432+540. <!-- {540:double-six-nonincident} -->
}
\]

The \(432\) incident flags are the projective \(A_5\) carrier appearing in
Pass 1137.  The \(540\) nonincident flags are the previously unnamed rank-28
degree-\(540\) species.  Thus Pass 1137's \(A_5\) shadow and Pass 1139's
\(C_2\times S_4\) complement are the two halves of one cubic incidence
object.

## Exact carrier identifications

The verifier constructs three species directly from coset geometry:

- the two non-self-dual index-\(40\) actions have subdegrees
  \(1,12,27\); their unordered complement orbitals are the point- and
  line-nonedge carriers at TOM \(77\) and \(81\);
- the unique index-\(45\) action has subdegrees \(1,12,32\); its ordered
  valency-\(12\) orbital has \(45\cdot12=540\) Hashimoto arcs and stabilizer
  \([48,49]\), hence TOM \(79\);
- the \(36\times27\) cubic incidence table identifies TOM \(78\) as above.

The ATLAS group \(W(E_6)=U_4(2):2\) has exactly three conjugacy classes of
elements of size \(540\), named \(4A,2D,4C\), with element orders <!-- {540:mixed} -->
\(4,2,4\) and centralizer order \(96\).  Intersecting those centralizers
with \(G=W(E_6)'\) gives TOM positions

\[
4A\longmapsto77,\qquad
2D\longmapsto81,\qquad
4C\longmapsto80.
\]

Consequently \(4A\) is the point-nonedge carrier, \(2D\) is the skew-line
carrier, and the \(4C\) restriction supplies the rank-21 species.

## Prior ownership and correction

Pass 161 already owned the first three natural carriers—point nonedges,
skew-line pairs, and \(\operatorname{GQ}(4,2)\) Hashimoto arcs—and their
ranks \(25,32,27\).  Passes 1067–1079 owned the \(2D\)/skew-frame geometry,
and Pass 1137 owned the \(432\)-point \(A_5\) shadow.  Pass 1139 consumes
those results and adds the exhaustive table-of-marks census, the \(4C\)
species, the rank-\(28\) cubic complement, and every pairwise joint rank.

This supersedes the Pass 1117/1128/1136 wording that treated the point- and
line-nonedge carriers as the entire degree-\(540\) universe.  Their warning
remains valid but becomes stronger: never identify a \(540\) from the
number or the factorization \(51840=540\cdot96\); name the carrier.

## Reproducibility

```text
gap -q analysis/w33_pass1139_complete_degree540_species.g
python3 -m pytest -q tests/test_pass1139_gap_complete_degree540_species.py
python3 -m json.tool data/w33_pass1139_complete_degree540_species.json
```

Artifacts:

- GAP verifier:
  `analysis/w33_pass1139_complete_degree540_species.g`;
- deterministic certificate:
  `data/w33_pass1139_complete_degree540_species.json`;
- focused regression:
  `tests/test_pass1139_gap_complete_degree540_species.py`.

## Scope

This is an exact theorem about finite permutation groups, tables of marks,
coset actions, and cubic-surface incidence.  The shared number \(540\) does
not identify an object and carries no automatic physical or continuum
interpretation.
