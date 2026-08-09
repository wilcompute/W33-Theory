# PART LXX — E6 Cubic Stabilizer Obstruction

**Status:** obstruction found; next target sharpened  
**Depends on:** Parts LXIX and the existing H27/cubic-surface audit scripts

Part LXIX reduced the next bottleneck to a precise question:

\[
\boxed{
\text{Can W33 construct a canonical }78\text{-dimensional }E_6\text{-like algebra acting on }U=27?
}
\]

A tempting candidate already present in the repo is the cubic built from the `36` internal triangles of the local `H27` shell.  Part LXX tests that candidate directly.

---

## 1. Candidate tested

Fix a base vertex `p` of `W(3,3)` and let

\[
H27(p)=\{x\in V(W33):x\ne p,\ x\not\sim p\}.
\]

This is the 27-point local shell.  It contains exactly `36` internal W33 triangles.

The candidate cubic is

\[
c_{36}(x)=\sum_{(a,b,c)\in\Delta_{36}}x_ax_bx_c.
\]

This is the obvious unsigned cubic from the internal triangle structure.

---

## 2. Stabilizer calculation

For a cubic tensor `c`, an infinitesimal stabilizer is a matrix `X in gl(27)` satisfying

\[
\sum_i X_{ia}c_{ibc}
+\sum_i X_{ib}c_{aic}
+\sum_i X_{ic}c_{abi}=0
\]

for every unordered triple `(a,b,c)`.

For the true Cartan/E6 cubic on the `27`, the infinitesimal stabilizer should have dimension

\[
\dim E_6=78.
\]

But for the unsigned `36`-triangle W33 cubic, the computation gives

\[
\boxed{\dim\operatorname{stab}(c_{36})=6.}
\]

Therefore

\[
\boxed{c_{36}\text{ is not the }E_6\text{ cubic}.}
\]

---

## 3. Consequence

This is not a failure of the W33 program.  It is a useful obstruction.

It proves that the `36` internal triangles alone are insufficient.  The missing `9` fibers cannot be treated as cosmetic or optional.  They are structurally necessary.

The correct candidate must involve the full tritangent count

\[
36+9=45,
\]

with signs/phases or a more refined incidence rule.

---

## 4. New target

The next theorem target is now precise:

> Construct the signed/full `45`-tritangent cubic `c_45` on the local `H27` shell and compute its infinitesimal stabilizer.  The target is
>
> \[
> \dim\operatorname{stab}(c_{45})=78.
> \]
>
> If this holds, W33 has a concrete candidate for the missing `E6` action on `U=27`.  If it fails, the E8-branching program must look elsewhere for the `E6` action.

---

## 5. Updated closure chain

The honest state is now:

```text
W33 signed transport -> H1 canonical carrier -> C3-regular generation fiber -> E8 branching skeleton
```

but the next missing link remains:

```text
H27 full signed 45-tritangent cubic -> E6 action on U=27.
```

Part LXX rules out the naïve shortcut:

```text
36 internal triangles alone -> E6 cubic
```

because the stabilizer is `6`, not `78`.

---

## 6. Regression test

The corresponding regression test is

```text
tests/test_e6_cubic_stabilizer_lxx.py
```

It verifies:

- `H27` has `36` internal triangles;
- the infinitesimal stabilizer of the unsigned `36`-triangle cubic has dimension `6`;
- this is not the `78`-dimensional `E6` stabilizer;
- the next target must be the signed/full `45`-tritangent cubic.
