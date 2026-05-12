# Part CCCCCLXXII — Triangle-Weight Synthesis

This part records the triangle analogue of vertex-weight bridge synthesis.

For each triangle tau, define the bridge atom

```text
Y_tau = P_K M_tau P_B
```

where M_tau marks the three triangle edges.  For triangle weights b in R^160,

```text
Y(b) = sum_tau b_tau Y_tau.
```

The computed synthesis invariants are:

```text
rank(T_tri) = 120
nullity(T_tri) = 40
Spec(T_tri^* T_tri) = 0^40, (27/80)^120
```

Thus triangle weights form an isotropic 120-dimensional bridge synthesis system.

Comparison with vertex synthesis:

```text
vertex weights:   rank 39,  spectrum 0^1, (27/32)^24, (27/20)^15
triangle weights: rank 120, spectrum 0^40, (27/80)^120
```

Interpretation:

```text
vertex synthesis = anisotropic 24+15 flavor-gradient sector
triangle synthesis = isotropic 120-dimensional boundary/Higgs activation sector
```

Generic triangle-weight combinations produce matrix rank 80 for Y(b): B_120 -> K_81, matching the generic rank seen in vertex-weight combinations.

The next target is mixed vertex+triangle synthesis.
