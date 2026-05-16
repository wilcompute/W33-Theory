# Part DCCLXV — Running Reciprocity-Invariant Bridge

## Why this part exists

DCCLXIV proved rigidity: with fixed weak scalar `x=3/13`, deformation gives

```text
x K_lambda = 1/lambda,
```

so exact reciprocity holds only at `lambda=1`.

The natural next question is whether a compensated/running scalar restores an exact invariant.

## Running compensation law

Define

```text
x_lambda = lambda x,
K_lambda = K/lambda,
```

with base `K=13/3`.

Then the verifier proves exactly:

```text
x_lambda K_lambda = 1
```

for every sampled rational `lambda` in the deformation family.

## Interpretation

- **Bare coupling view:** `x` fixed, reciprocity breaks away from `lambda=1`.
- **Running coupling view:** `x_lambda=lambda x`, reciprocity is restored as a strict invariant.

So the branch has an exact compensated duality, not just a one-point coincidence.

## Meaning

This adds a renormalization-style layer to the closure program:

- rigidity of bare reciprocal pairing,
- and exact restoration via a unique linear running law.

It is the strongest formalization so far of your “inverse Koide side” intuition under deformation.

## Exact vs conditional

- **Exact:** in the lazy deformation family, `x_lambda=lambda x` gives exact invariant `x_lambda K_lambda=1`.
- **Conditional:** uniqueness/universality of this running law beyond lazy deformations still requires a broader theorem.

## Executable artifact

- Verifier: `verify_dcclxv_running_reciprocity_invariant_bridge.py`
- Tests: `tests/test_dcclxv_running_reciprocity_invariant_bridge.py`
- Data: `data/dcclxv_running_reciprocity_invariant_bridge.json`
