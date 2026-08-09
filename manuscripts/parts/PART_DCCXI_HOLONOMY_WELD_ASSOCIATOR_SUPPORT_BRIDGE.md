# Part DCCXI — Holonomy Weld-Associator-Support Bridge

## Why this part exists

`Part DCCX` compressed the selector wall to one welded carrier projector `P` with seam complement `Q = I - P`.

The next question is coherence:

> when orientation and weld composition are mixed, what is the finite defect-support witness?

This part extracts that witness exactly.

## Associator support law

Let

$$
P = \frac12\begin{bmatrix}1&-1\\-1&1\end{bmatrix},
\qquad
Q = I-P,
\qquad
O = \operatorname{diag}(1,-1),
\qquad
S = \begin{bmatrix}0&1\\1&0\end{bmatrix}.
$$

Using Jordan product

$$
A\circ B = \frac{AB+BA}{2},
$$

compute

$$
\mathrm{Assoc}(O,P,S) := (O\circ P)\circ S - O\circ(P\circ S).
$$

The verifier proves

$$
\mathrm{Assoc}(O,P,S)
=
\frac12\begin{bmatrix}1&0\\0&-1\end{bmatrix},
$$

and after scaling by DCCX trace `13122`:

$$
13122\,\mathrm{Assoc}(O,P,S)
=
\begin{bmatrix}6561&0\\0&-6561\end{bmatrix}.
$$

So the defect support is purely signed-diagonal with zero cross-channel support.

## Why this is a breakthrough

DCCX gave a welded object; DCCXI gives its first explicit finite coherence-defect support law.

The support is exact and deterministic:

- no cross-channel leakage,
- only signed diagonal channel support,
- fixed packet magnitude `6561` on each diagonal channel with opposite sign.

So the post-DCCX frontier is now pinned as a controlled support-kernel problem, not an unconstrained ambiguity.

## Executable artifact

Verifier:

```text
verify_dccxi_holonomy_weld_associator_support_bridge.py
```

Tests:

```text
tests/test_dccxi_holonomy_weld_associator_support_bridge.py
```

Generated summary:

```text
data/dccxi_holonomy_weld_associator_support_bridge.json
```

---
*W33-Theory | Part DCCXI | welded projector coherence defect is a finite Jordan-associator support kernel, purely signed-diagonal with exact packet magnitude `6561` per channel (opposite signs).*
