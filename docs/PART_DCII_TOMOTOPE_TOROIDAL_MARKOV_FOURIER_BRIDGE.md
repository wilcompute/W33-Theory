# Part DCII — Tomotope/Toroidal Markov Fourier Bridge

Part DCI extracted the second spectral moment. This part diagonalizes the active-cycle sector in closed form.

---

## 1. Closed-form nontrivial modes

For the `7` active-cycle modes, the six nontrivial eigenvalues are:

```text
lambda_k = 1/8 + (3/4) cos(2*pi*k/7),   k = 1..6.
```

Together with the two special modes (`1` and `0`), this gives the full `8`-state Markov spectrum.

---

## 2. Exact trigonometric sums

Use the exact finite sums:

```text
sum_{k=1}^6 cos(2*pi*k/7) = -1,
sum_{k=1}^6 cos^2(2*pi*k/7) = 5/2.
```

Then:

```text
sum_{k=1}^6 lambda_k = 0,
sum_{k=1}^6 lambda_k^2 = 21/16.
```

So:

```text
Tr(P) = 1,
Tr(P^2) = 1 + 21/16 = 37/16,
Tr(P^2)-1 = 21/16.
```

This reproduces DCI exactly.

---

## 3. Transport ladder recovery

The same nontrivial packet yields:

```text
21/16 -> (x16) -> 21 -> (x2) -> 42 -> (x4 stabilizer) -> 168.
```

So the transport ladder has a closed Fourier origin in the active 7-cycle dynamics.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_markov_fourier_bridge.py
```

Output:

```text
data/tomotope_toroidal_markov_fourier_bridge.json
```

with closed-form mode packet, exact sum identities, and consistency checks against DCI.
