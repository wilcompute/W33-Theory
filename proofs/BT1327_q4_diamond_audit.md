# BT1327 -- Q4 Diamond Audit

## Purpose

BT1327 promotes the BT1326 master synthesis into an executable audit.

## New files

```text
tools/bt1327_q4_diamond_audit.py
data/bt1327_q4_diamond_audit.json
```

## Result

Most BT1326 number-table identities are exact arithmetic consequences of the stated Q4/atlas data:

```text
2^4 = 16
4*2^3 = 32
120*9/2 = 540
540*4 = 2160
11^4 = 14641
540*12/2 = 3240
3240*2 = 6480
6480/4 = 1620
67*4 = 268
2^3 = 8
540*8 = 4320
540*4*32^3 = 70,778,880
```

## Found issue

The literal claim

```text
10980 = lcm(3660,1620)
```

fails as written:

```text
lcm(3660,1620) = 98820
```

So the 10,980 master epoch needs either a corrected input pair, a different operation, or an explicit non-lcm derivation.

## Interpretation

This is a useful strengthening, not a setback: the Q4 diamond is now partially machine-audited, and the remaining weak point is sharply localized to the epoch derivation.

## Next

BT1328 should repair or rederive the 10,980 epoch from the oscillator/atlas clocks, then rerun the BT1327 audit with the epoch gate restored.
