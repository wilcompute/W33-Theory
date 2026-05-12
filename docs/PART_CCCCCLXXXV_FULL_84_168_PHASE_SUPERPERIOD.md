# Part CCCCCLXXXV — Full 84/168 Phase Superperiod

Part CCCCCLXXXIV found the genus-one Fano/Heawood phase lock:

```text
(v,E,F) at h=1 = (7,21,14),
E=12+9,
F=12+2.
```

This part adds the full clock, including the decimal/face residue.

## 1. Three coupled periods

The genus increments are

```text
Delta v = 3,
Delta E = 15,
Delta F = 10,
Delta chi = -2.
```

Modulo the W33 local 12-clock,

```text
Delta v = 3 mod 12,
Delta E = 15 = 3 mod 12.
```

So the local vertex/edge phase repeats after

```text
12/gcd(12,3)=4
```

handle steps.

The face/decimal residue changes by

```text
Delta F = 10.
```

Relative to the 12-clock this is

```text
10 = -2 mod 12,
```

so it repeats after

```text
12/gcd(12,2)=6
```

handle steps.

The Fano/toroidal color shell has period

```text
7.
```

Therefore the full coupled phase period is

```text
lcm(4,6,7)=84.
```

## 2. Euler drift over the full period

Since

```text
Delta chi = -2
```

per handle, one full 84-step phase cycle has drift

```text
84*(-2) = -168.
```

This is the key arithmetic lock:

```text
full phase period = 84,
Euler drift = -168.
```

The number `168` is the order of the Fano-plane automorphism group

```text
|PSL(2,7)| = |GL(3,2)| = 168.
```

Thus the full genus phase clock returns to its combined local/toroidal/face residue state exactly when the accumulated Euler drift equals the Fano automorphism order in magnitude.

## 3. Interpretation

The earlier 28/56 lock came from coupling only

```text
4-period local mod12 transport
7-period Fano color shell.
```

The full 84/168 lock includes the face/decimal clock:

```text
4 local transport phase,
6 face/decimal residue phase,
7 Fano/toroidal color phase.
```

So the complete oscillator is

```text
4 x 6 x 7 with overlaps -> lcm 84,
Euler drift -> 168.
```

## 4. Clifford/percolation reading

In the Clifford-percolation model, coherent cycles require closure of:

```text
mod12 transport phase,
Fano color/XOR phase,
face/genus residue,
Clifford bivector support.
```

The 84-step period is the first global window in which these arithmetic clocks can all close.  The -168 Euler drift says that one complete arithmetic closure sweeps exactly a Fano automorphism-order amount of topological curvature.

This suggests the following principle:

```text
Fano symmetry is not an external decoration;
it is the automorphism count of one full genus phase closure.
```

## 5. New test target

For each handle step `h`, compute the state

```text
s(h) = (3h mod 12, -2h mod 12, h mod 7).
```

Then verify:

```text
period(s)=84,
chi drift over period=-168.
```

This becomes a small exact arithmetic test for the phase-clock layer.
