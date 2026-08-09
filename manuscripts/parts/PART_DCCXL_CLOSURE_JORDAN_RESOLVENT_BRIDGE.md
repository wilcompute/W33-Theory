# Part DCCXL: Closure Jordan-Resolvent Bridge

## Claim

DCCXXXIX gave the finite closure propagator

```text
K(a,b) = 2^{-(b-a)}  for a <= b.
```

On the six proper-time classes this is not only a table.  It is the exact
unipotent resolvent of a one-step nilpotent shift:

```text
K = (I - N)^(-1),      N = (1/2) S,
```

where `S[i,i+1]=1` is the strict one-step shift.

Because `S^6=0`, the inverse is finite:

```text
K = I + N + N^2 + N^3 + N^4 + N^5.
```

## 1. Operator form

The six causal classes are:

```text
T0, T1, T2, T3, T4, T5.
```

The generator is:

```text
N = (1/2)S.
```

Thus:

```text
N^6 = 0,        N^5 != 0.
```

The DCCXXXIX propagator is exactly:

```text
K = (I - N)^(-1).
```

So the closure semigroup is a finite Jordan/unipotent operator.

## 2. Unipotent spectrum

Since `K` is upper triangular with diagonal entries `1`:

```text
spec(K) = {1,1,1,1,1,1},
trace(K) = 6,
det(K) = 1.
```

The strict part is nilpotent:

```text
(K - I)^6 = 0,        (K - I)^5 != 0.
```

So the closure propagator has minimal polynomial:

```text
(x - 1)^6.
```

## 3. Logarithmic generator

Because `N^6=0`, the logarithm terminates exactly:

```text
log(K) = sum_{m=1}^5 N^m/m.
```

This is another finite nilpotent operator.  Its first superdiagonal is
exactly `1/2`, matching the elementary propagator weight.

## 4. Link back to the holonomy frontier

Earlier holonomy parts reduced the live frontier to a nilpotent/Jordan slot.
DCCXL shows that the new closure-time semigroup is the same algebraic kind of
object at causal-chain scale:

```text
local nilpotent slot  ->  six-level nilpotent shift  ->  unipotent propagator.
```

This does not replace the earlier holonomy witness.  It gives the proper-time
chain a compatible operator model.

## Boundary

This is a finite matrix/operator theorem.  It does not identify the finite
unipotent chain with a continuum heat kernel, Lorentzian propagator, or
physical Hamiltonian without a separate limit/dynamics theorem.

## Verified identities

The executable verifier checks:

```text
K equals the DCCXXXIX propagator table,
K = (I - N)^(-1),
N^6 = 0 and N^5 != 0,
trace(K) = 6,
det(K) = 1,
(K-I)^6 = 0 and (K-I)^5 != 0,
log(K) is nilpotent,
K(0,5) = 1/32.
```
