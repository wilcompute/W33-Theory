# PART CCCCXLVI — E8 Inner-Product Rescue Trichotomy

This part pushes the E8 edge/root program deeper by expressing third-reference
rescue behavior in terms of the doubled root inner product

$$
d = a\cdot b \in \{-8,-4,0,4,8\}.
$$

## Exact pair-count structure (unordered, including diagonal)

$$
\#(d=8)=240,\quad \#(d=-8)=120,\quad \#(d=\pm4)=6720\ \text{each},\quad \#(d=0)=15120.
$$

So total pairs are

$$
240+120+6720+6720+15120 = 28920.
$$

## Rescue-profile trichotomy

Using deterministic sampled stability checks (first 50 pairs per dot class):

- $d=\pm 8 \Rightarrow$ feasible third references = $126$,
- $d=\pm 4 \Rightarrow$ feasible third references = $234$,
- $d=0 \Rightarrow$ feasible third references = $240$.

Hence strict trichotomy:

$$
126 < 234 < 240.
$$

## Interpretation

Third-reference rescue strength is controlled by pair geometry in the E8 root
system: orthogonal pairs ($d=0$) maximize feasibility, while coincident/antipodal
pairs ($d=\pm8$) are most constrained.

## Honesty boundary

This part certifies exact pair-count histograms and stable sampled rescue constants.
A full all-pairs proof of constant rescue value within each dot class remains open.
