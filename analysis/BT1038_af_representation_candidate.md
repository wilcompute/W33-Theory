# BT1038 — A_F representation candidate

BT1038 constructs an explicit block-representation candidate for
`A_F = C + H + M3(C)` on the W33 doubled fermion carrier.

## Carrier

```text
H_ferm = C^2_chiral x C^3_generation x C^3_fiber x C^3_weakslot x C^3_color
       = 2 * 3 * 3 * 3 * 3
       = 162
```

The weakslot is decomposed as:

```text
C^3 = C_singlet + C^2_weak_doublet
```

## Algebra action

| algebra block | candidate action |
| --- | --- |
| `C` | acts on the singlet / unimodular U(1) direction |
| `H` | acts on the weak doublet through Pauli/quaternion matrices |
| `M3(C)` | acts on the color slot |

## Lie profile

```text
u(1)  = 1
su(2) = 3
su(3) = 8
total = 12
```

This matches the finite W33 centralizer profile `[1,3,8]`.

## Boundary

This is an explicit representation candidate. The first-order condition and the
inner-one-form span calculation remain BT1039 targets.

## Witnesses

```text
analysis/bt1038_af_representation_candidate.py
data/bt1038_af_representation_candidate.json
```
