# Part DCCLXI — Octahedral First-Return / Renewal Bridge

## Why this part exists

DCCLX gave exact return probabilities and generating function. This part resolves those returns into first-return events and verifies exact renewal structure.

## Exact renewal law

Let `p_t = P^t(i,i)` be return probability and `f_t` first-return probability. The verifier proves

```text
p_0 = 1,
p_t = sum_{k=1}^t f_k p_{t-k}   (t>=1).
```

and reconstructs returns from first returns on a long window with machine precision.

## Exact first-return values and moments

The verifier confirms:

- `f_1 = 0`,
- `f_2 = 1/4`,
- `f_3 = 1/8`,
- total first-return mass is `1`,
- mean return from first-return law is exactly `6`.

So recurrence is fully captured by first-passage events with the same Kac mean as before.

## Exact generating-function identity

For

```text
G(z)=sum_{t>=0} p_t z^t,
F(z)=sum_{t>=1} f_t z^t,
```

the verifier proves

```text
G(z)=1/(1-F(z)),
F(z)=1-1/G(z).
```

It also matches both `G` and `F` series to the closed-form `G` from DCCLX.

## Meaning

The octahedral closure walk now has:

- exact return profile,
- exact first-return decomposition,
- exact renewal generating identity.

This is the cleanest exact first-passage/renewal bridge so far in the closure transport program.

## Exact vs conditional

- **Exact:** first-return probabilities satisfy full renewal reconstruction and generating-function identities.
- **Conditional:** continuum first-passage interpretation still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dcclxi_octahedral_first_return_renewal_bridge.py`
- Tests: `tests/test_dcclxi_octahedral_first_return_renewal_bridge.py`
- Data: `data/dcclxi_octahedral_first_return_renewal_bridge.json`
