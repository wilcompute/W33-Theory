# BT857 — Chirality Bookkeeping: Absolute Pentads, Absolute Tetrads, Gauge Dodecahedra

**Status: PROVEN (machine-verified, `analysis/bt857_chirality_bookkeeping.py`, data `data/bt857_chirality_bookkeeping.json`)**

The compass needle's three chiral pairs are not chiral in the same way. One
normalizer computation settles the bookkeeping: the core A₅ sits in N = S₅
(order 120, BT843), and the action of the odd coset on each pair decides
whether its handedness is PSp-invariant (absolute) or gauge (relative).

## The verdict table

| chiral pair | odd element of S₅ | chirality |
| --- | --- | --- |
| pentads {P_L, P_R} | **fixes each** (forced: two global PSp-orbits) | **absolute** |
| tetrad partitions {T₁, T₂} | **fixes each** | **absolute** |
| dark dodecahedra {D₁, D₂} | **swaps them** | **relative (gauge)** |

## Consequences

- **No-go:** no PSp-invariant can correlate a specific dark dodecahedron
  with the pentad handedness — the dodecahedral choice is a gauge bit,
  invisible to every equivariant observable. (The two lifts of the
  dark-chart Petersen graph, BT855, are exchanged by the odd symmetry.)
- **Existence:** because pentads *and* tetrad partitions are both absolute,
  the question "which tetrad partition goes with which pentad" has a
  PSp-invariant answer — a canonical LEFT/RIGHT pairing exists across the
  lit and dark sectors (its explicit invariant is queued).
- The substrate again holds both chirality types simultaneously — absolute
  (cf. BT746's torsor chirality) and relative (cf. the duo bits) — now
  within a single compass needle: the lit sector and the tetrad layer are
  oriented; the dodecahedral layer is orientation-free.

## Machine reading

The needle carries two invariant orientation bits (pentad, tetrad) and one
gauge bit (dodecahedron). In bus terms (BT856: dark charts = mirror slots),
the transport layer inherits the two absolute bits as routable state while
the dodecahedral gauge bit is local hidden freedom — exactly the right
structure for a parity-protected flag: observable handedness for addressing,
unobservable handedness as a free local reference.

## Open

- Exhibit the explicit pentad↔tetrad pairing invariant (meets/shadow
  signature distinguishing T₁ from T₂ relative to P_L).
- Does the gauge dodecahedral bit extend to a global Z₂ gerbe over the 216
  cores, or is it independently gauge per needle?
