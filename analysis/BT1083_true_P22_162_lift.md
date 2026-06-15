# BT1083 — Lift the true P22 projector into the 162-slot carrier

BT1083 replaces the diagonal BT1068 slot template with a linear lift of the true BT1080 projector.

## Per-generation carrier split

The 162-slot carrier is grouped as three generation blocks of dimension 54:

```text
C^162 = G0 direct_sum G1 direct_sum G2,
rank(Gg)=54.
```

Use the first W33-native lift ansatz

```text
Gg = C40_core(g) direct_sum R14(g).
```

Here `C40_core(g)` carries the BT1080 transvection action, while `R14(g)` is the residual slot space not seen by the 40-point transvection carrier.

## Lifted projector

On each generation block define

```text
P22_lift(g) = P22_true_on_C40(g) direct_sum 0_R14(g).
```

Then

```text
rank P22_lift(g) = 22.
```

The physical projector on each generation is

```text
P32(g) = I_54(g) - P22_lift(g)
      = (I_40 - P22_true_on_C40(g)) direct_sum I_14(g).
```

Hence

```text
rank P32(g) = (40-22) + 14 = 18 + 14 = 32.
```

## Total ranks

Taking the direct sum over three generations gives

```text
rank P66_linear = 3*22 = 66
rank P96_linear = 3*32 = 96
P66_linear^2 = P66_linear
P96_linear^2 = P96_linear
P66_linear P96_linear = 0.
```

## Meaning

The complement is now the real BT876 grade-zero space lifted generationwise: fixed basis vectors plus shell-cycle sums. The physical 96-block is the off-grade 18-dimensional transvection complement plus a 14-dimensional residual carrier in each generation.

## Boundary

The remaining noncanonical choice is the identification of the 40-dimensional transvection core inside each 54-dimensional generation block. BT1083 fixes the linear projector once that core inclusion is chosen.
