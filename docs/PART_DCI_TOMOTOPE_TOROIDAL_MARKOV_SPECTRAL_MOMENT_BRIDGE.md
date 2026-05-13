# Part DCI — Tomotope/Toroidal Markov Spectral-Moment Bridge

Part DC provided an exact 8-state Markov chain (`7` active + `1` ground). This part extracts an exact spectral moment and ties it to the toroidal transport counts.

---

## 1. Exact moment

For the transition matrix `P`:

```text
Tr(P)  = 1,
Tr(P^2)= 37/16.
```

Because the chain has eigenvalue packet `1, 0, (six nontrivial modes)`, the nontrivial squared-mode moment is:

```text
M2_nontrivial = Tr(P^2) - 1 = 21/16.
```

---

## 2. Transport recovery from spectral scaling

Scale by `16`:

```text
16 * M2_nontrivial = 21,
```

which matches the toroidal unoriented transport count.

Double it:

```text
2 * 21 = 42,
```

matching the oriented transport count from Part CCCCCXCIX.

Weight by the slot stabilizer `4`:

```text
42 * 4 = 168,
```

matching the active toroidal/tomotope packet weight.

So the bridge from spectral moment to transport ladder is exact:

```text
21/16 -> 21 -> 42 -> 168.
```

---

## 3. Executable artifact

Script:

```text
scripts/tomotope_toroidal_markov_spectral_moment_bridge.py
```

Output:

```text
data/tomotope_toroidal_markov_spectral_moment_bridge.json
```

with exact rational identities and cross-checks against the earlier transport bridge.
