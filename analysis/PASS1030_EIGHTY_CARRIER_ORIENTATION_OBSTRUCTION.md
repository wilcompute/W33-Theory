# Pass 1030 — Eighty-carrier orientation obstruction

**Certificate:** `analysis/w33_pass1030_eighty_carrier_orientation_obstruction.py` →
`data/w33_pass1030_eighty_carrier_orientation_obstruction.json` (`14/14`,
deterministic, standard-library Python).

## The tempting identification

Pass 1023 supplies the order-three quotient

\[
240/C_3=80,
\]

leaving a residual binary \(C_2\) fibre. Independently, the point-line Levi graph
has

\[
40\text{ points}+40\text{ lines}=80\text{ vertices}.
\]

This suggests identifying binary chirality with a point-versus-line label. The
identification is false for the natural verified actions.

## Orbit obstruction

The E8 omega-triple carrier is transitive:

\[
|\mathrm{Sp}(4,3)|/648=51840/648=80.
\]

Its orbit partition is therefore

\[
[80].
\]

The natural incidence action on Levi vertices preserves type, so its orbit
partition is

\[
[40,40].
\]

Moreover, Pass 1021 proves the point and line actions are nonconjugate. Therefore
no natural equivariant bijection can identify the transitive E8 80-carrier with
the raw Levi point-line union.

## Exact-cover asymmetry

The two Levi halves also differ by a sharp combinatorial invariant:

\[
W(3,3)=(36\text{ spreads},0\text{ ovoids}),
\]

while the dual satisfies

\[
Q(4,3)=(0\text{ spreads},36\text{ ovoids}).
\]

Thus the two 40-object halves are not interchangeable even as bare incidence
orientations. E8 selects the point action, the zero-ovoid/KS-uncolourable side.

## Combined no-go with Pass 1029

Pass 1029 proves the whole Eisenstein normalizer is real-orientation preserving.
Pass 1030 proves that the obvious \(40+40\) surrogate has the wrong orbit
structure. Together:

> The chirality controller is neither an internal determinant switch nor the raw
> point-versus-line label. It must lie outside the Eisenstein tower and act above
> the incidence geometry.

## Experimental falsifier

A proposal claiming that chirality is implemented by swapping W33 points and
lines must exhibit all of the following:

1. one physical 80-state carrier;
2. an involution acting transitively across the proposed halves;
3. explicit transport of incidence and phase labels;
4. behavior compatible with the exact \(0\)-versus-\(36\) ovoid boundary.

Two disconnected 40-state banks or a mere relabeling fail automatically.

## Boundary

The dual line reading is combinatorial, not a second physical Witting-ray
realization. This theorem rules out the natural internal identification; it does
not construct the required external controller.
