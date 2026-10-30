# Passes 394–398: cover theorem, section classification, Dirac lift, sealed lab ingestion, and formula-universe freeze

## Baseline

This packet continues the live July 17 spine through Pass 393. It preserves the central lesson of Passes 386–393—phase, type, and section data must remain explicit—but closes all five queued workstreams rather than restating them.

## Pass 394 — the antipodal cover theorem

Fix a point at infinity in `W(3,q)`. Every opposite point has a unique coordinate representative

\[
(x,1,y,z)\longleftrightarrow(x,y,z)\in\mathbb F_q^3.
\]

The inherited collinearity law is

\[
(x,y,z)\sim(x',y',z')\iff z'-z=yx'-xy'.
\]

Projection to `(x,y)` partitions the graph into `q²` phase fibres of size `q`. There are no edges inside a fibre, and every pair of distinct fibres is joined by one perfect matching. The common-neighbor equation is one nonzero linear equation in two field variables, so for every odd prime power

\[
\boxed{\{q^2-1,q(q-1),1;1,q,q^2-1\}}.
\]

The distance-three classes are exactly the phase fibres. The executable witness verifies `q=3,5,7`; the queued `q=7` rung is `{48,42,1;1,7,48}` on 343 vertices.

## Pass 395 — all 81 Heisenberg sections classified

An inverse-closed section above the eight nonzero elements of `H/Z(H)` is a function `f` satisfying `f(-v)=-f(v)`. There are exactly `3⁴=81` such sections. The full automorphism group has order `432`.

| orbit | size | stabilizer | verdict |
|---|---:|---:|---|
| linear sections | 9 | 48 | distance-regular `(9,3,3)` cover |
| nonlinear sections | 72 | 6 | regular cover, not distance-regular |

The W33 connection set lies in the 9-orbit, exactly the graphs of linear functionals. Its array is `{8,6,1;1,3,8}` with constant `c₂=3`. In the 72-orbit, different-fibre common-neighbor counts are `0`, `2`, or `3`. Thus the canonical W33/Godsil–Hensel-valid section is the unique `Aut(H)` orbit satisfying distance regularity.

## Pass 396 — explicit chain/Dirac Plücker lift

The Pass-387 point/line bijections are emitted as permutation matrices and satisfy

\[
N_Q=R_{\rm line}M_W^TR_{\rm point}^T,
\qquad
D_Q=JD_WJ^T.
\]

Modulo two, `A_W=M M^T` and `A_Q=M^T M` square to zero. Their ranks are `16` and `10`, so

\[
\boxed{\dim H(A_W)=8,\qquad\dim H(A_Q)=20.}
\]

The incidence maps induce rank zero between these homologies. The Dirac rank packet `(50,26,2,0)` gives

\[
J_4^{\oplus2}\oplus J_3^{\oplus22}\oplus J_1^{\oplus6}.
\]

The two sides are therefore explicitly conjugate at chain level but remain separated after characteristic-two homology.

## Pass 397 — sealed laboratory ingestion

The production CLI has three stages: `seal`, `analyze`, and `unblind`. Production requires caller-supplied physical raw counts, calibration, and blind key files. There is no synthetic fallback.

The contract rejects post-seal byte changes, device mismatches, leaked labels, incomplete phase schedules, count-conservation failures, a key frozen after acquisition, or a key revealed before blinded analysis freezes. Test fixtures require explicit test mode and always carry

```text
claim_eligible = false
physical_experiment_completed = false
```

No physical experiment is claimed here.

## Pass 398 — formula-search universe

The scanner traverses the broad result-bearing corpus, extracts numerical relations with physics semantics, and groups them by exact normalized formula and structural formula with all numerical literals replaced by placeholders. Every family records all source locations, occurrence multiplicity, constants, and nearby status language.

The release workflow runs the scanner over the complete checkout and commits `data/w33_formula_search_universe_v1.json` whenever the frozen multiplicity denominator changes. A formula absent from this universe, or lacking a registry entry that freezes its data, null family, and tuning policy, receives no prospective credit.

## Unified conclusion

\[
\boxed{\text{The recurring missing object is a section of a typed finite bundle.}}
\]

The cover theorem identifies the phase fibres. The section classification identifies the unique distance-regular section orbit. The Plücker lift makes type reversal an explicit chain map while preserving distinct homologies. The laboratory path requires externally supplied, hash-locked records. The formula universe prevents a post-hoc numerical section from being promoted to prediction.
