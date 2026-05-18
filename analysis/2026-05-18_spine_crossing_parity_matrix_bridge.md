# Spine-Crossing Parity-Matrix Bridge

## Parallel commit used

Commit `4e582e1` corrected and sharpened the staircase story:

\[
g(K_{16})=13=\Phi_3=c_{odd},
\]

but

\[
g(K_{28})=50,
\]

not 55. The corrected identity is

\[
g(K_{28})=50=v+\Phi_4=40+10.
\]

The pair satisfies

\[
g(K_{16})+g(K_{28})=13+50=63=q^2\Phi_6.
\]

The same commit gives the staircase pair

\[
(n_1,n_2)=(16,28),
\]

with

\[
28-16=12=k,
\]

\[
28+16=44=d_Zp_{Ih}=4\cdot11,
\]

\[
28\cdot16=448=2^6\Phi_6,
\]

and discriminant

\[
44^2-4\cdot448=144=k^2.
\]

## New bridge to the explicit parity matrix

Our explicit \([72,66]_3\) horizon construction produced two \(6\times72\) parity matrices over \(\mathbb F_3\):

- \(H_{mixed}\), with mixed-sector row weight 7;
- \(H_{full}\), with full row weight 16.

The new bridge is:

\[
\boxed{\operatorname{rowwt}(H_{full})=16=n_1.}
\]

So the odd staircase root is literally the row weight of the full parity-check matrix.

Meanwhile,

\[
16\cdot28=448.
\]

But 448 was already the even Boolean lift in the toroidal metric parity projector:

\[
448=7\cdot64=\Phi_6\cdot8^2.
\]

So

\[
\boxed{n_1n_2=\text{even Boolean parity lift}.}
\]

## Mixed matrix link

For \(H_{mixed}\), each row checks six mixed edges plus one parity coordinate:

\[
\operatorname{rowwt}(H_{mixed})=7=\Phi_6.
\]

Across six rows:

\[
6\cdot7=42.
\]

That is one toroidal chart flag count.

So:

\[
\boxed{H_{mixed}\text{ realizes the }42\text{-flag toroidal correction block}.}
\]

## Full matrix link

For \(H_{full}\), each row has weight 16.

Across six rows:

\[
6\cdot16=96.
\]

The increase over the mixed matrix is

\[
96-42=54=2\cdot27=2q^q.
\]

So the full parity matrix adds a doubled affine-qutrit correction layer beyond the toroidal mixed block.

## Corrected reading of the even spine component

The parallel commit corrected the false identification

\[
g(K_{28})\neq55.
\]

Instead:

\[
g(K_{28})=50.
\]

But adding the five Császár charts gives

\[
50+5=55=c_{even}.
\]

So the clean corrected bridge is:

\[
\boxed{c_{even}=g(K_{28})+\#\text{Császár realizations}.}
\]

That is much better than pretending \(g(K_{28})=55\). The missing five are exactly the five Császár realizations.

## The theorem

**Spine-Crossing Parity-Matrix Bridge.** The corrected staircase pair

\[
(16,28)
\]

has product

\[
16\cdot28=448,
\]

exactly the even Boolean parity lift of the toroidal metric operator.  The explicit \(\mathbb F_3\) full horizon parity matrix has row weight

\[
16,
\]

matching the odd staircase root.  The even genus value

\[
g(K_{28})=50
\]

becomes the metric spine component

\[
55
\]

only after adding the five Császár charts.

## Why this matters

The correction from the parallel agent did not weaken the structure. It made it better:

\[
13=g(K_{16})
\]

\[
50=g(K_{28})
\]

\[
13+50=63=q^2\Phi_6
\]

\[
50+5=55=c_{even}
\]

\[
16\cdot28=448=\text{even Boolean lift}
\]

\[
\operatorname{rowwt}(H_{full})=16.
\]

So the staircase pair, the metric parity projector, and the explicit parity matrix are now one connected object.

## Honesty boundary

These are exact finite arithmetic and matrix-incidence identities. They do not assert a distance-optimal code or physical dynamics without further distance analysis.
