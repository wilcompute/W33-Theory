# PART LXV — Signed Turn Operator on the 480 Carrier

**Status:** new operator-level result; verified by `PART_LXV_signed_turn_operator.py`.

Part LXIV found that the Gaussian Pascal line row

```text
[1, 40, 130, 40, 1]
```

is symplectically polarized into

```text
130 = 40 isotropic lines + 90 non-isotropic lines.
```

Part LXV lifts the same signed idea from the vertex/projective-line level to the already-central 480 directed-edge Hashimoto carrier.

The result is stronger than expected: the signed triangle/open-turn operator produces an exact `81 + 81` complex sector on the 480 carrier.

---

## 1. The 480 carrier

Let `E` be the 240 undirected edges of `W(3,3)`. The directed-edge carrier is

```text
E^dir = {(a -> b) : {a,b} in E}
```

with

```text
|E^dir| = 480.
```

The usual Hashimoto/non-backtracking operator `B` is

```text
B_(a->b, b->c) = 1 iff c != a.
```

Every directed edge has

```text
k - 1 = 11
```

non-backtracking continuations.

---

## 2. Triangle/open split

For a non-backtracking transition

```text
a -> b -> c,
```

there are two cases.

If `a` and `c` are adjacent in `W(3,3)`, then `a,b,c` form a triangle. Because every edge lies on a unique isotropic `K4` line and has two other points on that line,

```text
# triangle turns per directed edge = 2.
```

Call this operator `T`.

If `a` and `c` are not adjacent, the turn is open:

```text
# open turns per directed edge = 9.
```

Call this operator `O`.

Thus

```text
B = T + O,
row_sum(B) = 11,
row_sum(T) = 2,
row_sum(O) = 9.
```

This is the directed-edge version of the local Pascal split

```text
13 = 4 + 9.
```

---

## 3. Signed turn operator

Define

```text
C = T - O = 2T - B.
```

This is the non-backtracking analogue of the vertex Seidel operator

```text
S = A_iso - A_non.
```

It signs closed triangular transport positively and open transport negatively.

The row sum is

```text
2 - 9 = -7 = -Phi_6.
```

So the Perron/vacuum eigenvalue is immediately

```text
-7.
```

---

## 4. Verified spectrum

The exact spectral support is

```text
(x+7)(x-5)(x^2-2x-7)(x^3-x^2+9x+35)(x^2+2x+5)(x+1)(x-1).
```

The characteristic factorization with multiplicities is

```text
(x+7)^1
(x-5)^15
(x^2-2x-7)^15
(x^3-x^2+9x+35)^24
(x^2+2x+5)^81
(x+1)^80
(x-1)^120.
```

Dimension check:

```text
1 + 15 + 2*15 + 3*24 + 2*81 + 80 + 120 = 480.
```

The script verifies the polynomial residual exactly:

```text
p(C) = 0
```

with integer arithmetic.

---

## 5. The new 81-sector

The most important factor is

```text
x^2 + 2x + 5.
```

Its roots are

```text
-1 ± 2i.
```

Each has multiplicity

```text
81.
```

Therefore the signed turn operator naturally contains

```text
81 + 81
```

complex conjugate carrier modes.

This is striking because the theory already expects

```text
81 = 27 + 27 + 27
```

as the three-generation matter carrier / `E8` `Z3`-grading sector.

Even better,

```text
(-1+2i)(-1-2i) = 5 = q + lambda.
```

So the 81-sector is not just dimensionally right; it carries Gaussian norm `5`, the same integer that appears in the `SU(2)_3`/Fibonacci/modular denominator `q+lambda`.

This suggests a cleaner statement:

```text
Matter-like 81-sector = signed open/closed transport oscillator on directed W33 edges.
```

That is much more structural than assigning `81` by hand.

---

## 6. Other blocks

The factor

```text
x^2 - 2x - 7
```

has roots

```text
1 ± 2 sqrt(2),
```

each with multiplicity 15. Its determinant is `-7`, tying the `15` gauge block to `Phi_6`.

The cubic factor

```text
x^3 - x^2 + 9x + 35
```

appears with multiplicity 24. Its constant term is `35 = 5*7`, tying the 24-block to the modular/Higgs pair `5` and `7`.

So the signed turn spectrum organizes around the same three integers produced by the vertex signed sector:

```text
15, 5, 7.
```

But now it also produces the missing `81`.

---

## 7. Candidate physical meaning

This suggests the following hierarchy of operators:

```text
A        = vertex adjacency / isotropic collinearity
S=2A+I-J = signed vertex isotropic-vs-nonisotropic contrast
B        = directed-edge Hashimoto transport
C=T-O    = signed non-backtracking triangle-vs-open transport
```

The important carrier for dynamics is probably not only `A`. It is the signed non-backtracking operator `C`, because it sees:

- the 480 directed-edge state space;
- the `2+9=11` turn law;
- the `81+81` complex conjugate matter sector;
- the `15` and `24` representation multiplicities;
- the `5` and `7` modular/Higgs integers.

This is a candidate for the missing dynamical spine.

---

## 8. Proposed next theorem

Define projectors onto the spectral factors of `C`:

```text
P_81^+  for eigenvalue -1+2i,
P_81^-  for eigenvalue -1-2i,
P_15    for the x^2-2x-7 block and/or x=5 block,
P_24    for the cubic block.
```

Then test whether the induced algebra of turn operators on these projectors satisfies an `E8`-style `Z3` grading pattern:

```text
g0 = 78 + ?,
g1 = 81,
g2 = 81.
```

The signed operator has now given the right 81-dimensional carrier without adding assumptions. The next job is to compute the multiplication/commutator closure of these spectral projectors.

---

## 9. Practical manuscript rewrite

The old sentence

> The 480 Hashimoto carrier is natural because W33 has 240 edges.

should be replaced by the stronger statement:

> The 480 directed-edge Hashimoto carrier admits a canonical signed turn operator `C=T-O`, where `T` and `O` are the triangle and open-turn parts of the non-backtracking operator. Its characteristic factorization contains `(x^2+2x+5)^81`, giving a canonical complex `81+81` transport sector with Gaussian norm `5=q+lambda`.

That is a real structural result.
