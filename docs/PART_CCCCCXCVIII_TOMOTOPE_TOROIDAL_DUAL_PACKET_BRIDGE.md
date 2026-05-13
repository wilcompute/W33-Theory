# Part CCCCCXCVIII — Tomotope/Toroidal Dual Packet Bridge

This part explicitly connects the tomotope carrier to the two toroidal polyhedra families in one executable model.

---

## 1. Two toroidal polyhedra, one active shell

Use the dual toroidal pair:

- Császár side: `E=21`, so flags `4E=84`.
- Szilassi side: `E=21`, so flags `4E=84`.

Therefore:

```text
84 + 84 = 168.
```

That is the full active dual-toroidal shell.

---

## 2. Outside-the-box packet interpretation

From the previous tomotope six-kernel vertex lift, the packet size is exactly:

```text
|S4| = 24.
```

Now attach one `24`-packet to each toroidal realization mode:

```text
5 Csaszar modes + 2 Szilassi modes = 7 active packets.
```

So active packet weight is:

```text
7 * 24 = 168,
```

which matches the dual toroidal flag shell exactly.

---

## 3. Tomotope completion

Add one ground packet:

```text
168 + 24 = 192 = 8 * 24.
```

So the tomotope carrier is read as:

```text
7 active toroidal packets + 1 ground packet.
```

This gives a direct finite bridge between

- the two toroidal polyhedra,
- the `5+2` realization split,
- and the tomotope `8x24` packet ladder.

---

## 4. Executable artifact

Script:

```text
scripts/tomotope_toroidal_dual_packet_bridge.py
```

Output:

```text
data/tomotope_toroidal_dual_packet_bridge.json
```

with verified identities, mode-to-packet assignment, and polyhedral side counts.
