# BT738 — Toroidal Knight Quotient Cube Theorem

## Search trail

This pass started from the existing hypercube/knight material rather than inventing a disconnected branch. Two repo files were the key anchors:

- `exploration/PART_CCCCXIII_TOROIDAL_KNIGHT_HYPERCUBE_PACKET.py` proves the 4x4 toroidal knight graph is `Q4` and that the chosen knight tour is a Gray-code Hamilton cycle.
- `analysis/w33_BREAKTHROUGH_157_Cl4_Q4_knight_gray_unification.py` records the older four-way identification

```text
Cl4 Clifford frame = Q4 hypercube = toroidal 4x4 knight tour = Gray code.
```

BT738 asks the next quotient question: what does the CCCCXIII Gray/knight clock look like after the antipodal axis quotient

```text
Q4 -> Q4/{+-} ~= K4,4 ?
```

## New result

Use the standard Fano-axis quotient label

```text
axis(p) = {(0,p), (1,1-p)},  p in F2^3.
```

The CCCCXIII 16-step toroidal knight Gray cycle descends to the 8-axis sequence

```text
000,100,110,010,011,111,101,001,
110,010,000,100,101,001,011,111.
```

Both halves visit all eight antipodal axes. The step generators in the K4,4 quotient are

```text
100,010,100,001,100,010,100,111,
100,010,100,001,100,010,100,111.
```

So the generator step counts are

```text
100: 8, 010: 4, 001: 2, 111: 2.
```

The full Fano quotient graph is

```text
K4,4 = Cay(F2^3, {100,010,001,111}),
```

with 8 vertices and 16 edges. The projected Gray trace has only 12 unique quotient edges. The four omitted edges are

```text
000--001,
010--101,
011--100,
110--111.
```

Those four omitted edges form a perfect matching of the eight quotient axes.

Therefore the projected support is

```text
K4,4 minus a perfect matching.
```

That graph is cubic, connected, has 8 vertices and 12 edges, and every vertex has distance profile

```text
1,3,3,1.
```

So it is exactly a 3-cube:

```text
K4,4 - M ~= Q3.
```

## Theorem

The CCCCXIII 16-step toroidal knight Gray cycle on `Q4` descends under the antipodal axis quotient to an 8-axis `K4,4` walk whose unique quotient-edge support is `K4,4` minus a perfect matching, hence a `Q3` cube with 8 vertices and 12 edges.

Equivalently:

```text
Q4 codec clock
  -> antipodal K4,4 axis quotient
  -> Q3 lambda-cube support + one missing perfect matching.
```

The missing matching records the duality/hinge closure not contained in the projected Gray trace.

## Interpretation

This is the cleanest bridge from the hypercube-functor language back into the repo's finite geometry:

```text
full 4-bit codec clock        : Q4
axis quotient / type space    : K4,4
visible hypothesis trace      : Q3
hidden closure datum          : missing perfect matching
```

So the toroidal knight tour is not merely a Hamiltonian clock on `Q4`. After antipodal quotienting, it becomes a lambda-cube-style 3-axis support plus a separate hinge/duality matching.

## Boundary

This theorem proves the graph/clock/quotient support statement. It does not claim the projected `Q3` alone is the full Levi `H1` selector. The rank-81 Levi selector still requires the BT714/BT724 hinge-selected sheets.

The executable verifier is currently committed as:

```text
analysis/bt735_toroidal_knight_quotient_cube.py
```

The BT738 note exists to avoid collision with the independently-added BT735 selector-payload exporter stack.
