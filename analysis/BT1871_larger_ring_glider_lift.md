# BT1871 — Rule-110 Larger-Ring Glider Lift

BT1871 tests whether the 30-cell ring in BT1864/BT1867 was suppressing real Rule-110 structure.

## Seed rule

Use a BC/Sturmian binary prefix with

```text
alpha = arccos(-2/3)/(2*pi)
```

and lift to ring lengths

```text
6*F for F in {5,8,13,21,34}
```

so the tested lengths are:

```text
30, 48, 78, 126, 204
```

The hole track is always:

```text
h = n mod 6.
```

## Results

```text
N=30,  steps=120: repeat found from 44 to 104, period 60
N=48,  steps=192: no repeat
N=78,  steps=312: no repeat
N=126, steps=504: no repeat
N=204, steps=816: no repeat
```

All tested rings see all eight Rule-110 neighborhoods.

Entropy remains nonzero and high:

```text
minimum entropy range across tested rings: 0.6962 ... 0.7219
maximum entropy = 1.0 in every tested ring
```

Domain walls persist:

```text
N=48:  transitions 10..34
N=78:  transitions 16..56
N=126: transitions 24..92
N=204: transitions 40..148
```

Best diagonal persistence:

```text
N=48:  v=-2 length 26
N=78:  v=0  length 130
N=126: v=0  length 198
N=204: v=0  length 388
```

## Verdict

The 30-cell ring is too small and can produce finite-box recurrence.  Larger BC/Fibonacci rings avoid repeat through `4N` steps, maintain active domain walls, and expose longer diagonal persistence.

Boundary: finite larger-ring diagnostic only; no Rule-110 universality proof or physical machine proof is claimed.
