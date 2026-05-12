# Part CCCCCLXXIII — Mixed Vertex/Triangle Synthesis

Parts CCCCCLXXI and CCCCCLXXII studied two families of incidence-frame bridge atoms:

```text
vertex atoms:   Y_v   = P_K M_v P_B,       v in V,    |V|=40
triangle atoms: Y_tau = P_K M_tau P_B,     tau in T,  |T|=160
```

The mixed synthesis family is

```text
Y(a,b) = sum_v a_v Y_v + sum_tau b_tau Y_tau.
```

The computed ranks are:

```text
rank(span{Y_v}) = 39
rank(span{Y_tau}) = 120
rank(span{Y_v, Y_tau}) = 120
```

Therefore

```text
span{Y_v} is contained in span{Y_tau}.
```

So vertex synthesis does not enlarge the triangle synthesis image.  Instead, vertex weights give a distinguished 39-dimensional anisotropic subspace inside the 120-dimensional isotropic triangle synthesis image.

Interpretation:

```text
triangle synthesis = full 120-dimensional incidence-frame boundary/Higgs activation space
vertex synthesis   = 39-dimensional gradient/flavor subspace inside it
```

This gives a clean hierarchy:

```text
single triangle atom: rank 2
single vertex atom: rank 8
vertex synthesis image: dimension 39
tiangle synthesis image: dimension 120
mixed incidence image: dimension 120
```

The next problem is to identify the 81-dimensional complement of the vertex subspace inside the triangle synthesis image, since

```text
120 = 39 + 81.
```

That is exactly the same numerical split appearing in the W(3,3) chain data:

```text
rank(d1)=39,
H1 dimension=81,
B-sector dimension=120.
```

Thus the mixed result suggests a decomposition of the triangle/Higgs activation space into

```text
120 = 39 vertex-gradient modes + 81 homological/matter-coupled modes.
```
