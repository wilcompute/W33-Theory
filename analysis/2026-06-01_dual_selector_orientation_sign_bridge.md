# Dual Selector / Orientation / Sign Bridge

Date: 2026-06-01

## Executive result

The previous bridge already isolated two exact facts:

1. the local three-branch qutrit selector is exact `S_3`, so the positive Jacobi
   coefficient `+1/6` has an exact source as normalized local selector averaging;
2. the local sign projector on the visible three-point permutation representation
   is exactly zero, so the negative coefficient `-1/6` cannot come from a literal
   local sign projection.

This bridge tests the next simplest hypothesis directly:

> maybe `-1/6` is explained by a naive overall dual/orientation sign flip on the
> `g_2` sector.

That hypothesis fails.

## What was tested

Using the exact `Z_3`-graded `E_8` bracket machinery from
`tools/toe_e8_z3graded_bracket_jacobi.py`, the bridge compares:

- the **canonical** bracket;
- a **sign-flipped dual-action** variant where the only change is the overall
  sign of the `g_0` action on `g_2`.

All other structure is left untouched:

- same certified `E_6` basis in the `27`,
- same canonical 45-term cubic triads,
- same `scale_sl3 = +1/6`,
- same mixed `g_1 - g_2 -> g_0` channel.

## Exact local selector boundary remains intact

The local selector packet is unchanged:

$$
P_{\mathrm{triv}} = \frac16\sum_{g\in S_3}\rho(g)
= \frac13
\begin{pmatrix}
1&1&1\\
1&1&1\\
1&1&1
\end{pmatrix},
$$

while

$$
P_{\mathrm{sign}} = \frac16\sum_{g\in S_3}\mathrm{sgn}(g)\rho(g)=0.
$$

So the visible local selector still explains `+1/6` exactly and still does **not**
explain `-1/6` locally.

## New no-go result

When `scale_sl3` is fixed at the exact rational value

$$
\frac16,
$$

both the canonical bracket and the sign-flipped variant tune the dual scale to

$$
scale_{g_2 g_2} = -\frac16.
$$

So the negative coefficient survives the naive orientation flip.

But the Jacobi behavior does **not** survive.

### Canonical bracket at exact rational scales

The canonical bracket closes all tested mixed patterns at machine precision:

- `(g_0,g_1,g_2)`: `3.6415315207705135e-14`
- `(g_1,g_1,g_2)`: `1.7763568394002505e-14`
- `(g_1,g_2,g_2)`: `1.0658141036401503e-14`

### Sign-flipped dual-action variant at the same exact rational scales

The naive sign flip breaks mixed Jacobi badly:

- `(g_0,g_1,g_2)`: `72.22222222222221`
- `(g_1,g_1,g_2)`: `1.7763568394002505e-14`
- `(g_1,g_2,g_2)`: `68.0`

So one mixed channel stays tiny, but two others explode.

## Meaning

This is the cleanest exact boundary so far on the negative coefficient.

The bridge proves three things at once:

1. `-1/6` is not a literal local sign projector;
2. `-1/6` is not removed by a naive overall dual/orientation sign flip;
3. the canonical bracket structure is doing something genuinely deeper than a
   visible local sign rule.

In short:

> the minus sign is real, exact, and structural — but not trivial.

## Best next target

The next theorem target is now sharper:

> derive `-1/6` from the full dual/oriented `g_2` structure together with the
> mixed `g_1 - g_2 -> g_0` channel, rather than from any simple sign rule on the
> visible local selector.

That is a much better frontier than vague “orientation magic.”
