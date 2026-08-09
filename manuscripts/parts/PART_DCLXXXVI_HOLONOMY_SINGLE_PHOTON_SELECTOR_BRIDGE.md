# Part DCLXXXVI — Holonomy Single-Photon Selector Bridge

## Why this part exists

`Part DCLXXXV` showed that the exact mixed-plane nilpotent witness is the quotient of the local deterministic qutrit feed-forward cycle.

The next question is whether the full local branch law is already the missing selector law.

This part proves that it is.

## Local selector group

On one three-branch affine fiber, define the two canonical maps

$$
\tau(a)=a+1 \pmod 3,
\qquad
\rho(a)=-a \pmod 3.
$$

The verifier proves the exact relations

$$
\tau^3 = e,
\qquad
\rho^2 = e,
\qquad
\rho \tau \rho = \tau^{-1}.
$$

So the local selector group is exactly

$$
\langle \tau, \rho \rangle \cong S_3.
$$

That means the deterministic qutrit branch law is not merely ternary.

It already carries the exact `S3` selector symmetry.

## Local-to-global carrier scaling

The verifier then imports the existing H4 selector audit and the DCLXIV affine shell and proves the exact count chain

$$
27 = 9\cdot 3
$$

for the local affine bulk, and simultaneously

$$
60\cdot 27 = 1620.
$$

Here:

- `27` is the DCLXIV mobile affine bulk,
- `60` is the number of ordered adjacent line pairs in the H4 selector audit,
- `1620` is the global nonlocal quadrangle carrier.

So the `27`-point local photonic bulk is exactly the local packet size whose `60` copies build the existing global selector carrier.

## Binary lift

`Part DCLXXXV` also proved that each local `3`-branch packet lifts to a `6`-state packet in the full `81`-state Pauli frame.

So the exact picture is now:

- projective selector branches: `3`,
- local selector symmetry: `S3`,
- lifted single-photon packet: `6`,
- local bulk packet: `27`,
- global selector carrier: `1620 = 60\cdot 27`.

## Why this is a breakthrough

This closes the selector gap more tightly than before.

The missing selector law is not something still waiting outside the single-photon runtime.

It is already present locally in the deterministic qutrit update rule, and the existing `1620` carrier is exactly the global completion of that same local law.

So the chain is now:

1. deterministic single-photon qutrit update,
2. exact local `S3` selector symmetry,
3. exact `27`-point local affine bulk,
4. exact global `1620` selector carrier.

## Executable artifact

Verifier:

```text
verify_dclxxxvi_holonomy_single_photon_selector_bridge.py
```

Tests:

```text
tests/test_dclxxxvi_holonomy_single_photon_selector_bridge.py
```

Generated summary:

```text
data/dclxxxvi_holonomy_single_photon_selector_bridge.json
```

---
*W33-Theory | Part DCLXXXVI | the deterministic single-photon qutrit update law already carries the exact local `S3` selector symmetry, and its `27`-point affine bulk scales by the `60` ordered adjacent pairs to the existing global `1620` selector carrier.*
