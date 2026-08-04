## Passes 3020–3024 — two diameters, a 46 % machine, and the rank-3 mechanism

---

## Pass 3020 — the pairs are **not** stabilizer codes, and the reason is now visible

Pass 2990 found orthogonal pairs of stabilizer states inside `(span singles)^⊥` and noted
that spanning a 2-space is not the same as being a stabilizer code. The sufficiency test:

```text
witnesses 17, orthogonal pairs 13
pair (0,4)  : 7 common stabilizing Paulis, F_2 rank 3
pair (2,9)  : 7 common stabilizing Paulis, F_2 rank 3
pair (4,8)  : 7 common stabilizing Paulis, F_2 rank 3
pair (5,16) : 7 common stabilizing Paulis, F_2 rank 3
pair (6,8)  : 7 common stabilizing Paulis, F_2 rank 3
pair (6,9)  : 7 common stabilizing Paulis, F_2 rank 3

maximum common-stabilizer rank : 3     (5 is needed)
pairs spanning a genuine code  : 0
```

> **Rank 3, uniformly, where 5 is required.** No pair spans a stabilizer code. The Pass
> 2990 result was necessary and not sufficient, and this is the sufficiency test failing.

### But rank 3 points somewhere

A rank-3 stabilizer group has an **eight**-dimensional code, not a two-dimensional one. If
such a code lies inside the complement it would annihilate every single error *and* have
ample room for a magic output.

> That is the next question, and it is a better one than the three that preceded it.

**Four passes, three formulations, one mechanism.** Rank-one branches exist; they are
useless (a rank-one range is a stabilizer state, confirmed independently by the other
track's 649,940-subspace search the same day); orthogonal pairs exist; none spans a code.
The gap between *spanning a subspace* and *being a joint eigenspace* is exactly where the
route stops.

---

## Pass 3021 (outside the programme) — the machine has **two** diameters

Two numbers measured independently, never put together:

```text
address transport diameter (parallel track, Pass 3005) :  2
frame ISA diameter          (this track, Pass 2866)    : 19
worst case for an arbitrary (address, frame) operation : 21
```

> **Geometry is cheap; algebra is expensive.** Moving a packet to any of the 40 addresses
> costs at most **two** shears, because the geometry has diameter 2. Transforming the
> Pauli frame arbitrarily costs up to **nineteen** instructions, because that is a walk in
> a four-million-element group.

**Ninety per cent of the machine's worst-case work is frame algebra**, and routing
optimisation addresses ten per cent of the problem. That is a scheduling priority neither
number could give alone.

---

## Pass 3022 (outside the programme) — the machine is **46 % efficient**

```text
erased per routed, read operation : 7.989 bits
delivered by the readout          : 3.673 bits
THERMODYNAMIC EFFICIENCY          : 45.98 %
```

And the network law follows directly. Depth `n` costs `8n` header bits, and `N = 40ⁿ`:

> **`E(N) = 143.35 · log₄₀ N` meV** — the thermodynamic cost of delivering a packet is
> **logarithmic in the size of the entire network**. Four billion leaves costs 860 meV.

The 54 % shortfall is not waste in the engineering sense: it is the routing header, which
is consumed by construction, plus the part of the frame the support readout cannot see.
Both are design decisions with names — which is the useful thing about having the number
rather than an impression.

---

## Pass 3024 — the overhaul, and the overfull box that finally died

**New in the paper**: the two-diameter law and its scheduling consequence; the efficiency
and the network energy law; and a spec box tracing the whole three-copy route from
rank-one witnesses to the rank-3 obstruction, ending with the eight-dimensional question
rather than a verdict.

**The 45 pt overfull box is gone.** Four attempts to narrow the representation-contract
table failed; rebuilding it as a description list instead of a tabular cleared it
immediately.

> Worth keeping as a small lesson: when four successive narrowings do not fit a table,
> the problem is the shape, not the widths.

**Zero overfull boxes, 21 sections, 4 parts, 388 KB.**

---

## Ledger

| claim | status |
|---|---|
| no orthogonal pair spans a stabilizer code | **proved** — rank 3, need 5 |
| \quad a rank-3 group gives an 8-dim code | **open** — the next question |
| two diameters: 2 and 19, total 21 | **derived** from two measurements |
| 90 % of worst-case work is frame algebra | derived |
| thermodynamic efficiency 45.98 % | **derived** |
| `E(N) = 143.35 log₄₀ N` meV | derived |
| overfull box | **fixed** by changing the table's shape |

## Prior art

- Parallel track Pass 3005 — owns the address-transport diameter 2 and the
  0/1080/480 shear census.
- Parallel track Pass 2977 — owns the independent confirmation that rank-one hits are
  stabilizer-output false leads.

## Still open

- Does an 8-dimensional stabilizer code lie inside `(span singles)^⊥`?
- A SAT decision on the Hamiltonian self-test.
