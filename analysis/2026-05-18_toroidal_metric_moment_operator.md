# Toroidal Metric Moment Operator

## Executive result

The previous bridge showed

\[
147-68=79,
\]

identifying the signed phase-frame kernel with toroidal metric edge degeneracy.

Now we lift the metric edge multiplicities themselves into a moment operator.

Across all seven realizations, the edge multiplicity histogram is

\[
1^{12},\quad 2^{48},\quad 4^4,\quad 5^1,\quad 6^3.
\]

Equivalently, there are:

- 12 metric edge classes of multiplicity 1,
- 48 of multiplicity 2,
- 4 of multiplicity 4,
- 1 of multiplicity 5,
- 3 of multiplicity 6.

This gives

\[
12+48+4+1+3=68
\]

metric edge classes and

\[
12\cdot1+48\cdot2+4\cdot4+1\cdot5+3\cdot6=147
\]

actual edge instances.

## Binomial moment operator

Define

\[
B_k=\sum_{\text{metric edge classes}}\binom{m}{k},
\]

where \(m\) is the multiplicity of a metric edge class.

Then

\[
\boxed{B_0,B_1,B_2,B_3,B_4,B_5,B_6=68,147,127,86,54,19,3.}
\]

The first two values recover the edge-kernel bridge:

\[
B_0=68,
\]

\[
B_1=147,
\]

\[
B_1-B_0=79.
\]

So

\[
\boxed{B_1-B_0=79=0^{79}\text{ phase-frame kernel}.}
\]

## The heptad subset hit

The second binomial moment is

\[
B_2=127.
\]

But

\[
127=2^7-1.
\]

So the pair-collision layer of the metric edge-class spectrum equals the number of nonempty subsets of the seven-realization heptad:

\[
\boxed{B_2=2^7-1.}
\]

That is a strong signal that the metric degeneracy structure is really seeing the full heptad, not merely the seven charts separately.

## Boolean lift and the middle eigenvalue 72

For each metric class of multiplicity \(m\), the Boolean lift is

\[
\sum_k\binom{m}{k}=2^m.
\]

Across the full seven-realization packet:

\[
\sum_k B_k=68+147+127+86+54+19+3=504.
\]

And

\[
504=7\cdot72=21\cdot24.
\]

Therefore the average Boolean edge-class lift per toroidal realization is

\[
\boxed{72.}
\]

But \(72\) is exactly the middle eigenvalue of the minimal-logical X-association spectrum:

\[
648^1,(144+36\sqrt6)^{24},\boxed{72^{30}},(144-36\sqrt6)^{24},40^{81}.
\]

So the middle eigenvalue is not floating.  It is the average Boolean lift of the toroidal metric edge-class operator.

## Raw second moment

The raw second moment is

\[
\sum m^2=401.
\]

And

\[
401=320+81.
\]

Here

\[
320=|X_{\min}^{\mathbb F_3}|,
\]

and

\[
81=H_1.
\]

The family split is even sharper:

\[
\sum_{\text{Császár}}m^2=321=320+1,
\]

while

\[
\sum_{\text{Szilassi}}m^2=80=81-1.
\]

So the raw quadratic metric moment splits across the dual families as

\[
\boxed{321+80=(320+1)+(81-1)=401.}
\]

## Higher collisions live in Császár

The Császár/Szilassi binomial split is:

\[
B^{C}_k=(45,105,108,86,54,19,3),
\]

\[
B^{S}_k=(23,42,19,0,0,0,0).
\]

So for \(k\ge3\), all higher-order metric collisions live entirely in the Császár packet.

This is structurally sensible: the Szilassi edge multiplicities are only 1 or 2, while Császár contains the higher multiplicity classes 4, 5, and 6.

## The theorem

**Toroidal Metric Moment Operator Theorem.** The seven-realization edge-class multiplicity operator has binomial moments

\[
B_k=\sum\binom{m}{k}=68,147,127,86,54,19,3.
\]

Its first difference

\[
B_1-B_0=79
\]

is the signed phase-frame kernel.  Its second binomial moment

\[
B_2=127=2^7-1
\]

is the full nonempty heptad subset count.  The total Boolean lift

\[
\sum_kB_k=504=7\cdot72=21\cdot24
\]

shows that the average Boolean lift per toroidal realization is exactly the middle eigenvalue \(72\) of the minimal-logical X-association spectrum.  The raw second moment is

\[
\sum m^2=401=320+81,
\]

splitting the minimal X-vector count from \(H_1\).

## Why this matters

The spectrum

\[
648^1,(144+36\sqrt6)^{24},72^{30},(144-36\sqrt6)^{24},40^{81}
\]

now has another direct toroidal metric reading:

\[
\boxed{72=\text{average Boolean edge-class lift per realization}.}
\]

The kernel has a metric reading:

\[
\boxed{79=B_1-B_0=147-68.}
\]

The heptad has a subset reading:

\[
\boxed{127=B_2=2^7-1.}
\]

And the raw quadratic moment has a CSS/homology reading:

\[
\boxed{401=320+81.}
\]

That means the toroidal metric edge data is not peripheral.  It is actively encoding the middle eigenvalue, the phase kernel, the heptad subset structure, and the X/H1 split.

## Honesty boundary

This is an exact finite metric-moment identity. It gives an operator interpretation of the edge multiplicity spectrum, but does not by itself prove physical dynamics, continuum geometry, or empirical observables.
