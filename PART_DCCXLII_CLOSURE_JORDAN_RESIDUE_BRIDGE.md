# Part DCCXLII — Closure Jordan-Residue Bridge

## Why this part exists

DCCXL and DCCXLI gave the transfer generator and its exact resolvent kernel. Since the generator is nilpotent, ordinary diagonal spectral language is no longer the right description. This part extracts the correct finite spectral content.

## Exact nilpotent spectral picture

For the closure generator `G = (1/2)S`:

- the only eigenvalue is `0`,
- the characteristic polynomial is

  ```text
  lambda^6,
  ```

- the minimal polynomial is also

  ```text
  lambda^6,
  ```

- the Jordan form is a single length-6 block.

So the nontrivial mode content is not in distinct eigenvalues. It is in the Jordan chain and the residue tower.

## Jordan chain

Starting from `e_0`, successive applications of `G` generate the chain

```text
e_0 -> (1/2)e_1 -> (1/4)e_2 -> (1/8)e_3 -> (1/16)e_4 -> (1/32)e_5 -> 0.
```

This is the exact finite nilpotent mode ladder of the closure process.

## Residue tower

Because

```text
R(z) = I + zG + z^2 G^2 + z^3 G^3 + z^4 G^4 + z^5 G^5,
```

the resolvent is organized by the residue tower

```text
G^0, G^1, G^2, G^3, G^4, G^5.
```

These are the true response layers of the closure chain.

## Sample response profile at z = 1

The row sums of `R(1)` descend geometrically:

```text
63/32, 31/16, 15/8, 7/4, 3/2, 1.
```

So future-response mass decreases stepwise down the causal chain.

## Meaning

The emergent-time thread now has a correct nilpotent spectral interpretation:

- not a spread of eigenvalues,
- but a single zero eigenvalue with a nontrivial Jordan chain,
- and a finite residue tower governing exact response.

## Exact vs conditional

- **Exact:** the closure generator has spectral data `{0}` together with a length-6 Jordan chain and residue tower `G^0,...,G^5`.
- **Conditional:** relating this nilpotent spectral picture to continuum spectral modes requires a limiting procedure.

## Executable artifact

- Verifier: `verify_dccxlii_closure_jordan_residue_bridge.py`
- Tests: `tests/test_dccxlii_closure_jordan_residue_bridge.py`
- Data: `data/dccxlii_closure_jordan_residue_bridge.json`
