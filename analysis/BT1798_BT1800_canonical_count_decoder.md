# BT1798--BT1800 canonicalization, count lift, and decoder

## BT1798 — transport canonicalization probe

BT1795 found one exact transport from the 27 Hesse pair-frontier points to the H27/Payne shell. BT1798 asks whether that transport is canonical.

The result is a useful warning:

```text
exact source automorphisms: 216
sampled transports: 1000
distinct support-line images in sample: 504
most common image multiplicity in sample: 2
literal uniqueness: false
```

So BT1795 is not unique as a literal map. The right object is an orbit of transports under the source hypergraph automorphisms and the Schläfli/E6 target symmetries, not a single hand-picked bijection.

Honest boundary: full orbit classification under the full Schläfli/E6 automorphism group is still open. NetworkX VF2 is sufficient to disprove uniqueness but not the right engine for the complete `W(E6)` orbit decomposition.

## BT1799 — count-lift reconstruction test

BT1799 asks whether the BT1781 count vector can be explained by simple H27 support data after BT1795.

The count vector is:

```text
[528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560]
```

Total:

```text
9980
```

The transported support-line kinds are:

```text
old: 11
new: 7
```

The simple hypotheses fail:

```text
uniform F3-residue lift with four lifts per residue -> requires counts multiple of 64 -> false
coarse binary/quartic lift -> requires counts multiple of 8 -> false
old/new support kind only -> false, because both classes carry several count values
```

So the 9980 vector is not explained by H27 support membership, old/new line type, or any uniform residue lift. It requires an additional nonuniform 12-symbol fibre rule above the BT1795 transport.

## BT1800 — double-six syndrome decoder

BT1800 promotes the BT1796 double-six incidence matrix into a decoder specification.

Input matrix:

```text
18 transported table-lines x 36 double-six checks
M(table, double-six)=1 iff the transported H27 support line intersects the double-six in two points
```

Known balanced incidence from BT1796:

```text
row sum = 24
column sum = 12
rank_F2 = 16
rank_F3 = 13
```

Therefore:

```text
left nullity over F2  = 2
right nullity over F2 = 20
left nullity over F3  = 5
right nullity over F3 = 23
```

The all-ones vector lies in both left and right nullspaces over both fields because the row and column sums vanish modulo 2 and modulo 3:

```text
24 = 0 mod 2, 0 mod 3
12 = 0 mod 2, 0 mod 3
```

Decoder interpretation:

```text
36 double-sixes = syndrome checks
18 transported Hesse table-lines = error/table domain
observable rank = 16 over F2, 13 over F3
redundant check/gauge freedoms = 20 over F2, 23 over F3
row-side relations = 2 over F2, 5 over F3
```

This is not yet the full tuple decoder, because the missing 12-symbol fibre rule is still absent. But it identifies the syndrome ranks and nullity constraints any final BT1781 recovery must satisfy.

## Bottom line

```text
BT1798: transport is not literally unique; canonical object is an orbit
BT1799: 9980 counts force a nonuniform 12-symbol fibre rule
BT1800: double-six incidence gives a rank-deficient syndrome code, not the full decoder yet
```

## Files

- `analysis/bt1798_transport_canonicalization.py`
- `data/bt1798_transport_canonicalization.json`
- `analysis/bt1799_count_lift_reconstruction.py`
- `data/bt1799_count_lift_reconstruction.json`
- `analysis/bt1800_double_six_syndrome_decoder.py`
- `data/bt1800_double_six_syndrome_decoder.json`
- `analysis/BT1798_BT1800_canonical_count_decoder.md`
