# Part MDCLXXXIII: Clifford Antipodal A5 Selector Group

## Claim Boundary

MDCLXXXIII identifies the raw Clifford antipodal selector as an `A5` torsor.

It does not yet construct the W33 spread selector.

## Input

MDCLXXXI showed that the `36` Clifford `L/R` cross-pairs are count-equal to
the `36` W33 spreads but not scheme-equal.

MDCLXXXII showed that the raw Clifford selector is a block design on `60`
antipodal `600`-cell addresses:

```text
36 blocks of size 10
60 addresses
each address appears 6 times
```

## Construction

Every antipodal address lies in exactly one cell of each `L` row and exactly
one cell of each `R` column.

Therefore each address defines a permutation:

```text
{six L fibrations} -> {six R fibrations}
```

The verifier extracts the `60` permutations from the incidence data and checks
their algebra.

## Result

The `60` permutations:

```text
are all distinct;
contain the identity;
are closed under composition;
are closed under inverse;
are all even permutations.
```

Their order profile is:

```text
order 1:  1
order 2: 15
order 3: 20
order 5: 24
```

This is exactly the conjugacy/order profile of the icosahedral rotation group:

```text
A5
```

The action on the six Clifford fibrations is two-transitive:

```text
for each ordered source pair and ordered target pair, exactly 2 elements realize it
```

Each `L/R` cell is an action fiber:

```text
|{g in A5 : g(i)=j}| = 10
```

## Reading

The raw Clifford selector is not an arbitrary `36`-block design.  It is the
degree-six action of `A5`.

So the selector ladder is now:

```text
600-cell antipodal quotient = 60 addresses
60 addresses = A5 torsor in degree-six action
36 L/R cells = action fibers i -> j, each of size 10
```

The remaining selector problem is correspondingly sharper:

```text
twist the A5 degree-six torsor into the W33 spread association scheme
```

This is the exact finite algebraic target for the next bridge.

## Artifacts

- Analysis: `analysis/w33_clifford_antipodal_a5_selector_group.py`
- Tests: `tests/test_w33_clifford_antipodal_a5_selector_group.py`
- Result: `PART_MDCLXXXIII_CLIFFORD_ANTIPODAL_A5_SELECTOR_GROUP_results.json`
