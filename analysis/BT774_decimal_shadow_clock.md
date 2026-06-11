# BT774 — The Decimal Shadow of the Rectangle Clock

PART CLXIII formalized the 1/7 reptend hint statically (base Phi4 = 10,
denominator Phi6 = 7, period 2q = 6, missing {3,6,9} = {q,2q,q^2});
PART CLXIV tied the mod-12 wheel to the toroidal genus marks {0,3,4,7}.
Since then the Z12 wheel became a concrete group: the rectangle stabilizer
clock (BT746), with duo bit r^6 (BT750) and 12 reflections = lifts (BT749).
BT774 proves the decimal expansion of 1/7 is that clock's shadow.

## The dictionary (all verified exactly)

```text
decimal digit clock of 1/7 = Z6     = Z12 / <r^6>  (clock mod duo bit)
duo bit r^6                          invisible to the decimal shadow
Midy 9-complement (10^3 = -1 mod 7)  = quarter-turn r^3
   1+8 = 4+5 = 2+7 = 9,  142 + 857 = 999
user's {3, 6, 9}                     = {Midy shift, duo bit, complement}
quarter marks {0,3,6,9}              = <3>, the unique Z4 subgroup of Z12
units {1,5,7,11} = (Z/12)*           7 generates Z12: "the cyclical one"
6 "the middle"                       = unique central involution of Z12
genus marks {0,3,4,7} (CLXIV)        = CRT sumset {0,3} + {0,4}
10^6 - 1 = 999999                    = 3^3 * 7 * 11 * 13 * 37
                                       (q^3, Phi6, p_Ih, Phi3, 37)
reptend digit sum                    = 1+4+2+8+5+7 = 27 = q^3
```

## The W33 theorem (new, computational)

In the rectangle's D12 the reflections advance at DOUBLE speed under the
rotation clock:

```text
r^k s0 r^{-k} = s_{2k mod 12}    (verified for all k, exact)
```

Consequences:

1. The dihedral-phase orbit is the EVEN sublattice of Z12 — the exact
   structural analogue of the quadratic-residue orbit {1,2,4} = 10^{even}
   mod 7 inside the reptend (even-position digits {1,2,5}, odd {4,8,7}).
2. r^6 maps to 2*6 = 0: the duo bit acts trivially on phases.  The same
   bit that the decimal expansion of 1/7 cannot see is the bit the
   dihedral phase clock cannot see.  "Decimal shadow" is literal: both
   are quotients by the center <r^6>.

## Reading

The user's observation — 3,6,9 missing from the one-digit reptend world,
6 as the transition, 7 as the cyclic one after the middle — is the
subgroup lattice of the substrate's own selector clock:
Z12 = Z4 x Z3, quarter marks = the Z4, third marks = the Z3, center = duo,
units = the four clock generators, and 7 both generates the wheel
(gcd(7,12)=1) and carries the full decimal cycle (10 is a primitive root
mod 7).  The toroidal genus marks of the Csaszar/Szilassi pair are the
CRT shadow of the same lattice.

## Boundary

Open: whether the QR/even-phase split of the reptend maps onto the BT773
anchor structure (12 P-anchors per rectangle vs 6 even phases x duo); and
the percolation/oscillator scripts' mod-12 thresholds re-read through the
clock subgroup lattice.
