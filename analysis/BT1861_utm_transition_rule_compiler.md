# BT1861 — UTM Transition-Rule Compiler

BT1858 supplied a 12-symbol executable tape alphabet:

```text
{S,L} x Z/6Z
```

BT1861 adds a local transition-rule compiler on that alphabet.

## Alphabet

```text
S = 0
L = 1
hole track = Z/6Z
composite symbols = 12
```

## Binary gap-track rule

Use a Rule-110-style radius-one binary update on the gap track:

```text
111 -> 0
110 -> 1
101 -> 1
100 -> 0
011 -> 1
010 -> 1
001 -> 1
000 -> 0
```

## Hole-track rule

The hole/parity track advances deterministically:

```text
h -> h + 1 mod 6
```

## Compiled transition

For neighboring tape symbols

```text
(a,h_a), (b,h_b), (c,h_c)
```

the compiled local rule is

```text
T((a,h_a),(b,h_b),(c,h_c)) = (rule110(a,b,c), h_b + 1 mod 6)
```

This covers all:

```text
12^3 = 1728
```

local neighborhoods and outputs one of the 12 composite symbols.

## Sample transitions

```text
S0 S1 L2 -> L2
L2 L3 L4 -> S4
L5 S0 L1 -> L1
S4 S5 S0 -> S0
```

## Verdict

BT1858 supplied the tape alphabet.  BT1861 supplies the local transition compiler.

Boundary: this is a symbolic local-rule compiler.  It does not yet prove a full physical universal-machine simulation or halting/gadget construction.
