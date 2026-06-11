# BT785 — 480 as Ten Local 48-Packets

The GraphTheory note records five independent derivations of the same W33 number:

```text
2E                 = 2 * 240 = 480
3T                 = 3 * 160 = 480
Tr(A^2)            = v*k     = 480
Tr(L0)             = v*k     = 480
curvature total    = 6 * 80  = 480
```

BT781 found the local 48-unit:

```text
cube chart half:       C2^3:S3, order 48
rank-4 derived half:   C2^4:C3, order 48
```

BT785 combines them:

```text
480 = 10 * 48
```

with

```text
10 = k - r = 12 - 2
```

So each 480 derivation decomposes into exactly ten 48-packets:

```text
directed edges          480 / 48 = 10
oriented triangles       480 / 48 = 10
closed 2-walk trace      480 / 48 = 10
vertex Laplacian trace   480 / 48 = 10
curvature total          480 / 48 = 10
```

Useful factorizations of 48:

```text
48 = 4*k
48 = 2*24
48 = 12*mu
48 = 16*q
48 = (q+1)*k
```

The resulting packet formula is:

```text
480 = (k-r) * 48
```

This ties together the cube chart stabilizer, the rank-4 48 split, the rank-32
packet map, and the DEC trace identities.
