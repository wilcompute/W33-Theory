# Part DCCXLVI — Nilpotent Action Jet-Tower Bridge

## Why this part exists

DCCXLIII gave the nilpotent logarithm action, DCCXLIV its first variation,
and DCCXLV its Hessian.  Since the action is a finite polynomial, the entire
variation hierarchy is also finite.

## Exact jet tower

For the closure action

```text
A(z) = -log(I - zG) = sum_{d=1}^5 z^d G^d / d,
```

the verifier proves the closed form at `z=1`:

```text
A^(r)(1)_(ij) = ((d-1)! / (d-r)!) / 2^d   for d=j-i >= r >= 1,
A(1)_(ij)    = 1 / (d 2^d)               for d=j-i >= 1,
```

and zero otherwise.

So:

```text
A^(6)(z) = 0.
```

## Support law

The `r`-th derivative starts on the `r`-th superdiagonal:

```text
r = 0: action starts on first superdiagonal,
r = 1: variation starts on first superdiagonal,
r = 2: Hessian starts on second superdiagonal,
r = 3: third variation starts on third superdiagonal,
...
r = 5: fifth variation has only the top superdiagonal,
r = 6: zero.
```

This is the exact finite analogue of a truncated variational hierarchy.

## Top-path profile

Along the maximal `T0 -> T5` path, the jet profile is:

```text
A(1)      = 1/160,
A'(1)     = 1/32,
A''(1)    = 1/8,
A'''(1)   = 3/8,
A''''(1)  = 3/4,
A'''''(1) = 3/4,
A''''''(1)= 0.
```

All entries in the finite jet tower are nonnegative at `z=1`.

## Meaning

The closure-action chain now has a complete finite variational calculus:

```text
action -> variation -> Hessian -> higher jets -> exact termination.
```

This is stronger than having an action and a Hessian separately.  It proves
that the entire local response hierarchy is controlled by the same nilpotent
generator and terminates after exactly six proper-time levels.

## Exact vs conditional

- **Exact:** the nilpotent closure action has a complete finite jet tower
  through order five, with order six exactly zero.
- **Conditional:** interpreting this finite jet tower as continuum
  variational calculus requires a separate scaling limit.

## Executable artifact

- Verifier: `verify_dccxlvi_nilpotent_action_jet_tower_bridge.py`
- Tests: `tests/test_dccxlvi_nilpotent_action_jet_tower_bridge.py`
- Data: `data/dccxlvi_nilpotent_action_jet_tower_bridge.json`
