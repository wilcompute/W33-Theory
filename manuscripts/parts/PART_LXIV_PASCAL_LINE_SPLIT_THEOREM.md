# PART LXIV — Pascal Line-Split and Seidel Sector Operator

**Status:** theorem-level structural upgrade; verified by `PART_LXIV_pascal_line_split.py`.

This pass does not add another broad physics section. It extracts a rigid theorem from the Pascal/q-Pascal material and uses it to expose a cleaner dynamical object.

The core result is

```text
[4 choose 2]_3 = 130 = 40 + 90.
```

This is not merely arithmetic. It is the exact decomposition of the 130 projective lines of `PG(3,3)` into 40 totally isotropic lines and 90 non-isotropic lines under the symplectic form.

That split partitions the complete graph `K_40` into the 240 edges of `W(3,3)` and the 540 edges of its complement.

---

## 1. Why the Pascal material was pointing here

The existing Pascal Information Functor section identifies the Gaussian Pascal row

```text
[1, 40, 130, 40, 1].
```

The sharper interpretation is:

```text
40  = number of projective points of PG(3,3),
130 = number of projective lines of PG(3,3).
```

So this is not Pascal producing familiar W33 constants after the fact. It is the Grassmannian row over `F_3`, and the middle term is the full line geometry from which the graph is extracted.

---

## 2. Symplectic polarization of the line Grassmannian

Use the standard symplectic form

```text
omega(u,v) = u1*v3 - u3*v1 + u2*v4 - u4*v2 mod 3.
```

A projective line `L=<u,v>` is totally isotropic iff `omega(u,v)=0`.

The 130 projective lines split as

```text
# isotropic lines     = (q+1)(q^2+1) = 4*10 = 40,
# non-isotropic lines = 130 - 40 = 90 = q^2(q^2+1).
```

Therefore

```text
Lines(PG(3,3)) = L_iso disjoint-union L_non,
130 = 40 + 90.
```

This identifies the previously important `90 K4` sector with a canonical object:

```text
90 K4s = non-isotropic projective lines of PG(3,3).
```

---

## 3. Complete graph partition

Every projective line contains `q+1=4` points, hence contributes `C(4,2)=6` point-pairs. Since every two distinct projective points determine a unique projective line,

```text
C(40,2)=780=130*6.
```

The line split induces

```text
40*6 = 240,
90*6 = 540.
```

But

```text
240 = |E(W(3,3))|,
540 = |E(complement W(3,3))|.
```

So

```text
K_40 = union_{L isotropic} K4(L)  disjoint-union  union_{M non-isotropic} K4(M).
```

The first term is `W(3,3)`. The second term is its complement.

This gives the graph an exact projective origin:

```text
W(3,3) = isotropic half of the Gr(2,4)(F_3) Pascal line row.
```

---

## 4. Local form: 13 = 4 + 9

Through each point of `PG(3,3)` pass

```text
[3]_3 = 13
```

projective lines. The symplectic line split refines this as

```text
13 = 4 + 9.
```

Through every point:

- 4 isotropic lines;
- 9 non-isotropic lines.

Each line contributes 3 other points, hence

```text
4*3 = 12 = k,
9*3 = 27 = v-k-1.
```

So the local SRG decomposition

```text
39 = 12 + 27
```

is induced by the projective-line decomposition

```text
13 = 4 + 9.
```

This gives a sharper origin for the `H_27` opposite sector:

```text
H_27(p) = union of the 9 non-isotropic projective lines through p, with p removed.
```

---

## 5. The vertex signed sector operator

Let `A` be the W33 adjacency matrix. Let `A_N` be the complement adjacency matrix. Since

```text
A_N = J - I - A,
```

define the signed sector/Seidel operator

```text
S = A - A_N = 2A + I - J.
```

This matrix has entries

```text
S_ij = +1  if i != j and omega(i,j)=0,
S_ij = -1  if i != j and omega(i,j)!=0,
S_ii = 0.
```

The verified spectrum is

```text
Spec(S) = {-15^(1), 5^(24), (-7)^(15)}.
```

Its minimal polynomial is

```text
(S + 15I)(S - 5I)(S + 7I) = 0.
```

This is the first signed contrast operator produced by the Pascal line split.

---

## 6. Consequence

The physical dictionary should not use only the 40 isotropic K4s. The 90 non-isotropic K4s are the exact complement sector of the same Gaussian Pascal line row.

The natural action upgrade is a two-sector line action:

```text
S_line = beta_I * sum_{L isotropic} W_L + beta_N * sum_{M non-isotropic} W_M + S_matter.
```

The canonical non-free signed choice is

```text
beta_I = +1,
beta_N = -1.
```

That gives the vertex operator `S=A-A_N`, and in Part LXV the same idea is lifted to the 480 directed-edge carrier.
