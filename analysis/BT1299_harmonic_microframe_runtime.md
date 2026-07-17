# BT1299 — Finite Control-Microframe Runtime

## Summary

The legacy harmonic-named stack already had the local horizon packet

```text
[72,66]_3 = 66 payload symbols + 6 parity symbols.
```

The holonet runtime already had a route compiler, a `2160` mirror bus, a
`48`-block tomotope packet ABI, and the full `51840` two-qutrit Clifford
runtime.  BT1299 identifies the missing architecture layer:

```text
8      = one worst-case recursive route digit
72     = 9 * 8 = q^2 route digits = one finite control microframe
2160   = 30 * 72 = one E8-Coxeter mirror bus
51840  = 24 * 30 * 72 = 720 * 72 = one Clifford supercycle
```

So the holonet is not merely a network with clocks attached. It is a finite
clocked control network. The word oscillator is a legacy label here, not a
claim of a physical frequency, mass, or analogue carrier.

## The New Bridge

The old runtime factorization was:

```text
|Sp(4,3)| = 24 * 45 * 48.
```

The oscillator-clock factorization is:

```text
|Sp(4,3)| = 24 * 30 * 72.
```

These are the same because:

```text
45 * 48 = 30 * 72 = 2160.
```

The basis change has ratio:

```text
45 / 30 = 72 / 48 = q / lambda = 3/2.
```

Architecturally:

- `48` is the tomotope packet ABI;
- `72` is the oscillator horizon frame;
- `45` is the polar-pair geography;
- `30` is the E8 Coxeter clock;
- `2160` is the shared mirror bus seen in either basis.

## Tomotope to control microframe

The tomotope packet ABI is the body of the microframe:

```text
48 + 24 = 72
48 + 18 = 66
72 - 66 = 6
```

The full frame adds the local Clifford lift `24=f`.  The payload adds the
`18=q*q!` active line-cone sector.  The remaining parity rank is `6=q!`.

## Network Clocking

The route compiler has per-digit bound:

```text
up to 3 binary Q3-coordinate XOR toggles + up to 5 apartment-routing slots = 8 ticks.
```

Therefore:

```text
q^2 route digits = 9 * 8 = 72 = one finite control frame.
```

Depth `q^2=9` is the first recursion depth whose worst-case route consumes one
full harmonic frame.

The durable commit clock is:

```text
T(n) = 4(7^n - 1).
```

It is always route-epoch aligned:

```text
8 | T(n) for every n.
```

It is oscillator-frame aligned exactly every ternary level:

```text
72 | T(n) iff 3 | n.
```

Thus q=3 is both the address radix and the durable frame-locking period.

## Consequence

At every recursive holonet level, each W33 instance contributes:

```text
30 control microframes to the mirror bus,
720 control microframes to the full Clifford runtime.
```

Equivalently:

```text
mirror slots  = 30 * 72 * (# W33 instances)
runtime atoms = 720 * 72 * (# W33 instances).
```

This makes the computer/network architecture a finite control scheduler:
route ticks, microframes, mirror buses, and Clifford supercycles are typed
logic-switch layers at different scales.  “Harmonic” remains only in legacy
artifact names and compatibility keys.

## Verification

```text
python3 analysis/bt1299_harmonic_microframe_runtime.py
python3 tests/test_bt1299_harmonic_microframe_runtime.py
python3 -m py_compile analysis/bt1299_harmonic_microframe_runtime.py tests/test_bt1299_harmonic_microframe_runtime.py
python3 -m json.tool data/bt1299_harmonic_microframe_runtime.json
```

## Boundary

BT1299 is an exact finite runtime/clock factorization across the existing
oscillator, holonet, and tomotope artifacts.  It does not claim a new physical
hardware threshold or a new proof of the general Cayley diameter theorem.
