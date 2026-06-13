# BT907 — Profile-parameter Search Beyond Scaffold

BT907 searches the substrate-generated rational angle inventory rather than simply placing the BT904 rotations by hand.

## Search space

The inventory is generated from the W33 primitives

\[
\lambda=2,
q=3,
\mu=4,
\Phi_6=7,
\Phi_4=10,
k=12,
\Phi_3=13,
g=15,
f=24.
\]

Closure operations include primitive sums, products, and quadratic sums up to the working bound.

## Hits

The search recovers the full archived profile scaffold:

\[
\sin^2\theta_C=\frac{q^2}{\Phi_3^2+q^2}=\frac9{178},
\]

\[
\sin^2\theta_{12}=\frac\mu{\Phi_3}=\frac4{13},\qquad
\sin^2\theta_{13}=\frac\lambda{\Phi_6\Phi_3}=\frac2{91},\qquad
\sin^2\theta_{23}=\frac{\Phi_6}{\Phi_3}=\frac7{13}.
\]

The denominators are substrate-generated:

\[
13=\Phi_3,\qquad 91=\Phi_6\Phi_3,\qquad 178=\Phi_3^2+q^2.
\]

## Profile packing

The four rotations fit on four disjoint two-planes of the \(q^2=9\) multiplicity space. They consume eight coordinates and leave one neutral/sentinel coordinate.

\[
\boxed{\mathbb C^9 = (2+2+2+2)+1.}
\]

## Boundary

This is still not a measured-data fit. It is stronger than BT904 because the profile scaffold is found by a substrate-generated rational inventory search rather than manually asserted.

## Witness

```text
analysis/bt907_profile_parameter_search.py
data/PART_BT907_PROFILE_PARAMETER_SEARCH_results.json
```
