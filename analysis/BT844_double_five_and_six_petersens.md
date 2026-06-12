# BT844 — The Double-Five Refuted, and 4·K₁₀ = 12 Petersens

**Status: PROVEN (machine-verified, `analysis/bt844_double_five_and_six_petersens.py`, data `data/bt844_double_five_six_petersens.json`)**

Follow-up to BT843's two-compass discovery. One conjecture refuted, four
theorems found, including a complete answer to where the pentads live and a
classical-graph-theory capstone.

## Refutation first (the honest ledger)

**Conjectured:** the pentad core's two 5-orbits bisect its spread (a
"double-five"). **FALSE.** All 12 A₅ subgroups of a spread stabilizer are
*transitive* on the spread's 10 lines. The [5,5,10,20] signature reads
differently: the **10-orbit IS the spread**, and the two pentads live among
the **30 outside lines**.

## T2 — Twelve cores per schedule (the two compasses united)

Each spread stabilizer S₆ contains exactly **12 A₅ subgroups** — the two
S₆-classes, which are exactly the two PSp-classes of BT843:

- **6 duad cores**, signature [10,30] (spread + rest whole),
- **6 pentad cores**, signature [5,5,10,20] (spread transitive + two outside
  pentads + 20).

So **both 216-compasses fiber over the same 36 schedules**: 432 = 36 × 12
icosahedral cores in all, 12 per schedule. The two GAP 6-block systems
quotient to the same library.

## T1 — What a pentad is

Each pentad is **5 pairwise-disjoint lines covering 20 points** — a
half-spread constellation outside the schedule. Pentad orbit: **216, with
stabilizer of order 120 (S₅)**. ~~Since 216 cores × 2 pentads = 432 slots but
only 216 distinct pentads, every pentad serves exactly 2 cores.~~
**[CORRECTED by BT845: there are 432 distinct pentads in TWO chiral orbits
of 216; each pentad serves exactly ONE core, and every core pairs one LEFT
with one RIGHT pentad. Pentads are also maximal partial spreads — contained
in zero schedules.]**

**T1b — the interlock:** the two pentads of one core can *not* be mutually
disjoint (P₁ ∪ P₂ would be a 10-line spread sharing 0 lines with the marked
spread, violating the BT835 overlap law "1 or 4"). Computed: every line of P₁
meets **exactly 4** of the 5 lines of P₂ — the cross-incidence is
**K₅,₅ minus a perfect matching**. The overlap law forces the pentagram
pairing.

## T3 + T4b — The Petersen capstone: 4·K₁₀ = 12 Petersens

- The 6 duad cores' 15-orbits are Petersen graphs covering each of the 45
  pairs **exactly twice**: 2·K₁₀ = 6 Petersens.
- The 6 pentad cores *also* split the 45 pairs [15,30], and their 15-orbits
  are **also Petersen graphs** (SRG(10,3,0,1) verified).
- All 12 together: every pair covered **exactly μ = 4 times**:

```text
4·K₁₀ = 12 Petersens          (multiplicity = μ, the substrate primitive)
```

Classical context: Schwenk's problem (1983) — K₁₀ **cannot** be edge-partitioned
into 3 Petersen graphs (the famous eigenvalue-parity obstruction). The
substrate's schedule carries the canonical *resolvable double*: the
obstruction at multiplicity 1 dissolves at multiplicity 2 per class, 4 overall,
and the multiplicity is the substrate primitive μ = 4.

## Machine reading

- A schedule's internal 45 switching-pairs carry a 12-fold redundant
  hemi-dodecahedral addressing scheme: 12 icosahedral "compass needles" per
  timetable, each reading the 45 pairs as Petersen-15 + 30, with uniform
  4-fold pair coverage. Error-tolerant context addressing for free.
- The 216 pentads (stab S₅) are a new hardware register: half-spread
  constellations, each shared by exactly 2 cores — the pairing makes the
  216 pentads into a 2-regular exchange graph (cycle structure open).

## Open

- The pentad exchange graph: 216 pentads, each in 2 cores' pairs → disjoint
  cycles; compute the cycle type.
- Which 2 cores share a pentad — same schedule or different schedules? (If
  different, pentads are inter-schedule bridges — wormholes in the library.)
- The 20-orbit of the pentad core: structure (it is the other half of the
  outside world, 30 = 5+5+20).
- K₅,₅ minus a matching is the bipartite complement of the pentagram — does
  the matching itself (5 distinguished line-pairs) carry the F₅ register?
