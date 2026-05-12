# Part CCCCCLXXIX — Genus-Percolation Oscillator Bridge

This note links the genus harmonic oscillator, toroidal realization modes, topological cellular automata, and quantum percolation.

## 1. Oscillator backbone

The first three genus levels obey synchronized arithmetic laws:

```text
v(h) = 4 + 3h      = 4, 7, 10
E(h) = 6 + 15h     = 6, 21, 36
F(h) = 4 + 10h     = 4, 14, 24
chi(h)=v-E+F       = 2-2h
```

Thus the tetrahedron, Csaszar/Szilassi torus layer, and double-torus layer form a finite topological oscillator.

At genus one:

```text
5 Csaszar + 2 Szilassi = 7 toroidal modes.
```

Csaszar realizes maximal vertex adjacency through the K7 skeleton. Szilassi realizes maximal face adjacency through mutually adjacent faces. The tetrahedron is the self-dual ground state between the two maximum-adjacency forms.

## 2. Percolation variable

For any incidence atom `a`, introduce

```text
omega_a in {0,1},   P(omega_a=1)=p.
```

Atoms may be vertex bridges, triangle bridges, K4-line sums, seven toroidal modes, or CA update cells.

Define the occupied bridge

```text
Y_p = sum_a omega_a w_a Y_a.
```

Then define the quantum/topological visibility operator on the harmonic matter sector:

```text
C_H(p) = Y_p Y_p^* restricted to K=H1.
```

This makes percolation a direct extension of the Q81 alignment program.

## 3. Three thresholds

The model separates three thresholds:

```text
p_geom: a giant occupied incidence component appears,
p_H1:   rank C_H(p) becomes nonzero,
p_full: rank C_H(p)=81.
```

Classical percolation asks whether connected occupied paths exist. Quantum percolation asks whether coherent transport survives disorder/localization. W33 genus percolation asks whether the occupied topology sees all 81 harmonic matter modes.

## 4. Cellular automaton form

A topological CA rule becomes

```text
omega(t+1)=Rule(omega(t), local incidence, phase/holonomy).
```

The physically meaningful observables are

```text
rank C_H(t),
d_eff(t)=Tr(C_H)^2/Tr(C_H^2),
Spec(C_H(t)),
Betti vector of occupied subcomplex.
```

This connects cellular automata to quantum measurement-like activation: the rule does not only grow clusters; it changes the spectral visibility of harmonic matter directions.

## 5. New synthesis

The deterministic part is the genus oscillator:

```text
tetrahedron ground state -> seven toroidal modes -> higher-genus activation.
```

The stochastic part is percolation:

```text
which incidence atoms are occupied/coherent at probability p.
```

The quantum part is the spectrum of the occupied transport operator:

```text
H_p = Delta_internal + Y_p + Y_p^*.
```

The matter-readout part is

```text
C_H(p)=Y_pY_p^*|_K.
```

## 6. Target executable experiment

Simulate Bernoulli occupation of vertex, triangle, and toroidal-mode atoms. Estimate:

```text
p_geom,
p_H1,
p_full,
p_split,
```

where `p_split` is the first stable nontrivial spectral splitting of `C_H(p)`.

This turns the genus harmonic oscillator into a finite percolating quantum network model.
