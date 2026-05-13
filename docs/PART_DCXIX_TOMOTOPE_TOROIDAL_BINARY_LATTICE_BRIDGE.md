# Part DCXIX — Tomotope/Toroidal Binary Lattice Bridge

This part rewrites the shell bridge in binary exponent coordinates.

---

## 1. Exponent normalization

Using base shell `21`:

```text
21 = 21*2^0,
42 = 21*2^1,
84 = 21*2^2,
168 = 21*2^3.
```

So the shell ladder becomes the integer lattice path:

```text
0 -> 1 -> 2 -> 3.
```

---

## 2. Operators as shifts

On exponents:

```text
D(n)=n+1,
Q(n)=n-1,
W(1)=3.
```

Confluence equalities become exact shift identities:

```text
Q(W(1)) = D(1) = 2,
W(1) = D(D(1)) = 3.
```

---

## 3. Horizon-gap duality in lattice form

Horizon pairs:

```text
linear:  (8,14),
energy:  (4,7).
```

Gap form:

```text
14-8 = 6,
7-4  = 3,
6 = 2*3.
```

So duality is visible directly as an integer gap law on the same scaffold.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_binary_lattice_bridge.py
```

Output:

```text
data/tomotope_toroidal_binary_lattice_bridge.json
```

with exponent ladder, shift identities, and horizon-gap duality checks.
