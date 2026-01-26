# Continuation: PG(3,2) + Symplectic Polarity (W(3,2)) Analysis

## Executive outcomes (computed)

### 1) Two inequivalent 5-cap types in PG(3,2) (under GL(4,2))
Enumerating all 5-point caps (no three collinear) in PG(3,2) yields **1008** caps, splitting into exactly **two** GL(4,2)-orbits:

- **Quadratic (elliptic-quadric) 5-caps**: orbit size **168**
- **Non-quadratic 5-caps**: orbit size **840**

Your two observed 5-point sets:
- Missing-support cap: {" ".join(sorted(S_missing))}
- sec0_m2 completion cap: {" ".join(sorted(S_apex))}

both lie in the **non-quadratic orbit (size 840)**.

A quadratic 5-cap example is:
0001 1000 1011 1101 1111

So the “missing supports form an ovoid” statement is correct in the *cap sense* (no three collinear), but it is **not** an elliptic quadric in these PG(3,2) coordinates (and not GL-equivalent to one).

### 2) Symplectic structure: W(3,2) “doily” lines and incidence
Using the standard symplectic form J (two-qubit Pauli geometry), there are **15 isotropic lines** (the W(3,2) lines), each of the form {u, v, u+v} with <u,v>=0.

Intersection profile of either 5-cap with isotropic lines is perfectly balanced:
- 5 lines meet the cap in 0 points
- 5 lines meet the cap in 1 point
- 5 lines meet the cap in 2 points

The tomotope-selected 10 PG points (complement of the missing-support cap) meet isotropic lines as:
- 5 lines in 1 point
- 5 lines in 2 points
- 5 lines in 3 points (i.e., the 10-set contains 5 entire isotropic lines)

### 3) The two observed 5-caps are symplectically equivalent
Within Sp(4,2) (order 720), the orbit of the missing-support 5-cap has size **360** (stabilizer size 2). The sec0_m2 completion cap is in the **same** Sp-orbit.

An explicit symplectic matrix mapping missing-support cap -> sec0_m2 completion cap is saved as:
- symplectic_matrix_maps_missing_to_apex.csv
- symplectic_map_missing_to_apex.json

### 4) Hyperplane 27 fiber structure explains the “missing-support” phenomenon
For the affine constraint a0-a1-a2+a3 = 1 (mod 3), the 27 solutions fiber over the 15 PG support patterns.

Fiber sizes are:
- 10 supports with fiber size 1
- 4 supports with fiber size 3
- 1 support (1111) with fiber size 5

Your missing-support cap is **exactly 5 of the fiber-size-1 supports**, i.e. tomotope omits **all** phase-functions in those fibers (forced omissions), and omits the remaining 7 phase-functions from inside the multi-fiber supports.

## What this buys us
- We now know the tomotope’s “15 line” selection corresponds to a **very specific omission pattern** in the Z3-hyperplane: *all lifts over a 5-point nonquadratic cap of singleton fibers*.
- The two “special 5-sets” you see (missing-support vs sec0_m2 completion) are not unrelated quirks; they are in the same **symplectic equivalence class** and have identical W(3,2) intersection statistics.

## Next immediate test (recommended)
Use the symplectic map M to transport the full tomotope 10-set and compare:
- which isotropic lines become “full” (k=3) under the map,
- whether the “forced completion apex” behavior corresponds to a canonical hub point/perp-plane in W(3,2),
- and then lift this back to the Z3 hyperplane to see which coefficient patterns are being singled out.