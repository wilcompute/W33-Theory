# Part DCCXLI — Closure Resolvent-Kernel Bridge

## Why this part exists

DCCXL gave the exact one-step generator `G = (1/2)S`. The next natural step is to sum all generated propagations into a closed-form response kernel.

## Exact resolvent

Because `G` is nilpotent of index 6, the Neumann series truncates exactly:

```text
R(z) = (I - zG)^(-1) = I + zG + z^2 G^2 + z^3 G^3 + z^4 G^4 + z^5 G^5.
```

So the closure resolvent is a finite polynomial, not just a formal infinite series.

## Closed-form entries

The verifier proves the exact entry formula

```text
R(z)_(ij) = (z/2)^(j-i)   for j >= i,
R(z)_(ij) = 0             for j < i.
```

Thus the resolvent is the exact Green/response kernel of the closure transfer generator.

## Sample consequences

At `z = 1`:

- maximal response from `T_0` to `T_5` is

  ```text
  R(1)_(0,5) = 1/32,
  ```

- the full future-response mass from `T_0` is

  ```text
  sum_j R(1)_(0,j) = 1 + 1/2 + 1/4 + 1/8 + 1/16 + 1/32 = 63/32.
  ```

At `z = 2`:

- all upper-triangular entries become `1`, since `(2/2)^(j-i)=1`.

## Meaning

The emergent-time chain now has:

- generator,
- semigroup,
- and exact resolvent kernel.

So the closure-time structure supports not just evolution, but full finite response theory.

## Exact vs conditional

- **Exact:** the discrete closure generator has a finite exact resolvent kernel.
- **Conditional:** interpreting this as a continuum Green's function still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dccxli_closure_resolvent_kernel_bridge.py`
- Tests: `tests/test_dccxli_closure_resolvent_kernel_bridge.py`
- Data: `data/dccxli_closure_resolvent_kernel_bridge.json`
