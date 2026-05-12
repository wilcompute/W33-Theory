# Part CCCCCLXXIV — K4-Line Kernel of Triangle Synthesis

Part CCCCCLXXII found that triangle-weight synthesis has

```text
T_tri : R^160 -> Hom(B,K)
rank(T_tri)=120
nullity(T_tri)=40
Spec(T_tri^*T_tri)=0^40,(27/80)^120
```

This part identifies the 40-dimensional kernel.

W(3,3) has 40 K4 lines.  Each line contains 4 vertices and therefore 4 triangles.  For a line L, define

```text
ell_L = sum_{tau subset L, |tau|=3} e_tau  in R^160.
```

Then

```text
T_tri(ell_L)=0.
```

The 40 vectors ell_L are independent and span the full kernel:

```text
ker(T_tri) = span{ell_L : L a K4 line of W(3,3)}.
```

Therefore the active triangle synthesis space is

```text
R^160 / <line triangle sums>
```

and has dimension

```text
160 - 40 = 120.
```

This sharpens the triangle result:

```text
triangle/Higgs activation = triangles modulo K4-line sums.
```

Combined with Part CCCCCLXXIII,

```text
vertex synthesis image: 39-dimensional subspace
triangle synthesis image: 120-dimensional quotient by line sums
complement dimension: 81
```

So the bridge hierarchy is now

```text
R^160 / line-sums  =  39 vertex-gradient modes + 81 homological modes.
```

This is the cleanest current form of the incidence-frame Higgs/Yukawa space:

```text
line sums are invisible,
vertex gradients are a distinguished 39-subsector,
the remaining 81-sector matches H1.
```
