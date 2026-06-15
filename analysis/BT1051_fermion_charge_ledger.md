# BT1051 — Fermion charge ledger on the 162 carrier

BT1051 extends BT1049 from the weakslot normalization to the full 162-carrier bookkeeping.

## Carrier factors

```text
H = C^2_chiral x C^3_generation x C^3_fiber x C^3_weakslot x C^3_color
```

The U(1) generator from BT1049 acts only on the weakslot/color factor:

```text
Y0 = diag(2/3, -1/3, -1/3) tensor I_color
```

## Multiplicities

The remaining carrier multiplicity outside weakslot/color is:

```text
2_chiral * 3_generation * 3_fiber = 18
```

Inside one weakslot/color block:

```text
singlet slot: 3 color states with charge  2/3
doublet slots: 6 color states with charge -1/3
```

Therefore on the full 162 carrier:

```text
charge +2/3 multiplicity = 18 * 3 = 54
charge -1/3 multiplicity = 18 * 6 = 108
```

## Trace checks

```text
Tr_162(Y0)   = 54*(2/3) + 108*(-1/3) = 0
Tr_162(Y0^2) = 54*(4/9) + 108*(1/9) = 36
```

Thus the full-carrier normalized generator is:

```text
Y162_hat = Y0 / 6
```

so that

```text
Tr_162(Y162_hat^2) = 1.
```

## Boundary

This is the charge ledger for the BT1038 carrier slots. It is not yet the full Standard Model hypercharge table because the particle/antiparticle and left/right representation assignment has not been fixed.
