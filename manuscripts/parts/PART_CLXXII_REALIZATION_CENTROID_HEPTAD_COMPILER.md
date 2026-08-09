# Part CLXXII — Realization Centroid / Heptad Compiler

**Date:** 2026-05-02  
**Status:** centroid/projector theorem for the seven realization coordinate sets

---

## 1. Source hint

The uploaded `.pages` file converts cleanly to text and contains the raw coordinate charts for five Császár realizations and two Szilassi realizations.  The formatted repo file `data/Toroidal-Polyhedra-Realizations.txt` contains the same coordinate data plus edge-length, volume, symmetry, and realization metadata.  The formatted file confirms that the five Császár entries share the same 14-triangle incidence and the two Szilassi entries share the same 7-hexagon incidence.  fileciteturn232file0

The repo also already contains `exploration/w33_toroidal_heptad_projector_bridge.py`, which reads the seven concrete Euclidean models as an operator heptad.  Its key rule is exactly the centroid rule: Császár realizations are read through their seven vertices, while Szilassi realizations are read through their seven face centroids.  It then centers each shell and builds rank-3 projectors.  fileciteturn235file0

---

## 2. Centroid reading rule

The correct dual reading is:

\[
\text{Császár shell}=\text{seven vertices},
\]

but

\[
\text{Szilassi shell}=\text{seven face centroids}.
\]

This is forced by duality: the Szilassi model has fourteen vertices but seven faces, so the dual heptad lives at face centroids, not raw vertices.

The user’s observation that the `C#` constants show up in some vertices is exactly right: those constants are chart-specific anchors.  But the invariant construction appears only after centering the correct heptad shell.

---

## 3. Operator heptad structure

The seven realizations produce seven rank-3 shell projectors.

The dictionary is:

\[
5+2=7=\Phi_6.
\]

The five Császár realizations give the threshold family:

\[
5=J.
\]

The two Szilassi realizations give the binary dual family:

\[
2=q-1.
\]

Together they give the toroidal heptad:

\[
7=\Phi_6.
\]

---

## 4. Mean and centered shell

The heptad splits as

\[
7=1+6.
\]

The one-dimensional piece is the mean projector/origin line.

The six-dimensional piece is the centered shell:

\[
6=2q.
\]

So subtracting the mean leaves the rank seed.

---

## 5. Family refinement

The centered shell refines as

\[
4+1+1=6.
\]

Here:

\[
4=q+1
\]

is the centered Császár family shell:

\[
5-1=4.
\]

The centered Szilassi family contributes

\[
2-1=1.
\]

The primal-dual family separation contributes another

\[
1.
\]

Thus

\[
4+1+1=6=2q.
\]

The full heptad refines as

\[
4+3=7,
\]

where the external three are the Szilassi mode, primal-dual separation, and mean line.

---

## 6. Carrier completion by tetrahedron origin

The toroidal heptad alone is

\[
5+2=7=\Phi_6.
\]

Adding the tetrahedron origin gives

\[
1+5+2=8.
\]

But

\[
8=J^{-1}\pmod{13}.
\]

Thus the tetrahedron completes the toroidal heptad from threshold closure to carrier residue:

\[
\Phi_6+1=J^{-1}.
\]

---

## 7. Theorem statement

**The seven realization coordinate sets should be read as an operator heptad.**  The five Császár vertex shells plus the two Szilassi face-centroid shells give

\[
\Phi_6=7
\]

rank-3 projectors.  Removing the mean gives a

\[
6=2q
\]

centered shell.  The centered shell refines as

\[
4+1+1,
\]

and the full heptad refines as

\[
4+3.
\]

Adding the tetrahedron origin completes the toroidal heptad from

\[
\Phi_6=7
\]

to

\[
J^{-1}=8.
\]

---

## 8. Regression status

Local validation of the CLXXII test file:

```text
5 passed in 0.04s
```

The tests verify:

1. heptad counts and carrier completion,
2. centered-shell dimensions,
3. full refinement and mean line,
4. threshold/carrier inverse and step,
5. audit-level consistency.

---

## 9. Next move

The next target is a concrete centroid/constant signature table for all seven realization charts.  The useful data to extract are:

1. which `C#` constants occur as vertex coordinates,
2. which `C#` constants occur as face-centroid coordinates,
3. the centered z-shell signature for each realization,
4. the rank-3 shell projector signature,
5. whether the `C#` anchors partition into the same \(5+2\), \(1+6\), or \(4+3\) packets.
