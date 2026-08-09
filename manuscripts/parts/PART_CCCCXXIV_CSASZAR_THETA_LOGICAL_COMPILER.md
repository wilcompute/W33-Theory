# Part CCCCXXIV: Csaszar Theta Logical Compiler

**Status:** verified local-to-global logical compiler for the Csaszar input side of `A(7)`.

## Result

Part CCCCXXIII proves that one Csaszar `K7` torus carries:

```text
[[21,2,>=3]]
```

Part CCCCXXII identifies five Csaszar modes as the input side of the seven-mode photonic harmonic algebra. Therefore the five input blocks compile to:

```text
5 * [[21,2,>=3]] = [[105,10,>=3]]
```

The logical size is not accidental:

```text
10 = 5 * 2 = theta(W33)
4  = local toric GSD = theta(complement)
10 * 4 = 40 = W33 Shannon capacity / vertex count
```

So the Lovasz theta register from CCCCXIX is exactly the ten local toric logical qubits carried by the five Csaszar input blocks.

## Ancilla Rail

The two Szilassi modes remain the ancilla side:

```text
2 * Phi6 = 14 = dim(G2)
```

This gives the clean split:

```text
theta register + G2 rail = 10 + 14 = 24
```

There is also a useful rank handoff:

```text
105 local Csaszar edge qubits
+14 G2 ancilla modes
+ 1 scalar/control line
=120
```

The result matches the W33 triangle-check rank `120`.

## Boundary

The `105+14+1=120` equality is a rank-bookkeeping closure, not a canonical operator isomorphism. This compiler does not replace the Steane/Phi6 `[[82320,81,>=81]]` protection layer and does not upgrade the Q4 packet beyond `[[1296,81,4]]`.

Artifacts:

- Script: `exploration/PART_CCCCXXIV_CSASZAR_THETA_LOGICAL_COMPILER.py`
- Results: `PART_CCCCXXIV_csaszar_theta_logical_compiler_results.json`
- Tests: `tests/test_csaszar_theta_logical_compiler_ccccxxiv.py`
