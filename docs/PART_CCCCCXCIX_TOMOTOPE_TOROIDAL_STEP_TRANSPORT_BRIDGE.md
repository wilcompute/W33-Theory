# Part CCCCCXCIX — Tomotope/Toroidal Step-Transport Bridge

This part upgrades the toroidal/tomotope connection from packet counts to explicit transport channels.

---

## 1. Seven toroidal modes as a transport cycle

Take the realization order:

```text
(C1, C2, C3, C4, C5, S1, S2)
```

as a 7-cycle. Oriented transports are ordered pairs `(i -> j)` with `i != j`.

So:

```text
oriented transports = 7 * 6 = 42,
unoriented transports = 7*6/2 = 21.
```

This recovers the toroidal edge packet (`21`) and its orientation double (`42`) in one model.

---

## 2. Six step classes = six tomotope slots

On a 7-cycle, each oriented transport has a step `d = (j-i) mod 7` in `{1,2,3,4,5,6}`.

Hence:

```text
42 = 6 * 7,
```

with six step classes, each containing exactly seven transports.

Identify these six classes with the tomotope six-slot channels `k1..k6`.

So each tomotope slot carries exactly seven toroidal transport phases.

---

## 3. Stabilizer weighting and the 168 bridge

From the S4 edge-action bridge:

```text
|G| = 24,
slot count = 6,
slot stabilizer size = 24/6 = 4.
```

Weight each oriented transport by this local stabilizer factor:

```text
42 * 4 = 168.
```

This exactly matches:

- active toroidal packet weight (`7*24=168`),
- dual toroidal flag shell (`84+84=168`).

So the 168 is recovered as a transport-weighted invariant, not only as a static count.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_step_transport_bridge.py
```

Output:

```text
data/tomotope_toroidal_step_transport_bridge.json
```

with step classes, slot assignment, stabilizer weight, and verified identities.
