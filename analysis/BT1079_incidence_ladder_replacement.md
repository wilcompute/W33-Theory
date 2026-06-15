# BT1079 — Incidence ladder replacement target

BT1079 replaces the partial-identity ladder idea with a W33-incidence-derived construction target.

## BT1075 placeholder

BT1075 used rectangular partial identities between nearest sectors:

```text
E0 <-> E4 <-> E10 <-> E16.
```

This gave the right dimensions and spectral gaps, but it was not W33-natural.

## W33-native replacement principle

The replacement ladder should be built from the incidence operators already native to the W33 chain complex:

```text
d1 : C0 -> C1
d2 : C2 -> C1
```

and their adjoints/projected restrictions.

Because the 1-Laplacian is

```text
Delta_1 = d1 d1^* + d2 d2^*,
```

any W33-natural ladder between eigensectors should be assembled from projected incidence pieces of the form

```text
P_mu B P_lambda
```

where `B` is one of the incidence/adjacency-derived operators on the 1-chain carrier.

## Candidate incidence blocks

```text
L_inc(lambda,mu) = P_mu B P_lambda
```

for nearest sector pairs:

```text
(0,4), (4,10), (10,16)
```

and their adjoints.

## Required test

For each nonzero block,

```text
[Delta_1/4, L_inc(lambda,mu)] = (mu/4 - lambda/4) L_inc(lambda,mu)
```

automatically follows if the block is exactly projected between eigenspaces. The real test is whether the incidence block is nonzero and what rank it has.

## Rank target from BT1075

The partial-identity skeleton had ranks

```text
rank(0,4)   <= 81
rank(4,10)  <= 24
rank(10,16) <= 15
```

The incidence ladder should report actual W33 ranks for these three projected blocks.

## Boundary

BT1079 replaces the placeholder by an incidence-derived construction target. It does not yet compute the projected incidence ranks, because that requires the concrete W33 boundary matrices and spectral projectors in the same script.
