# The near-ovoid / blocker / GQ(4,2) quotient tower

This packet records the exact quotient structure exposed by combining the
minimum-vector trade lattice with Holotrade's bidirectional
near-ovoid/minimum-blocker correspondence.

## 1. The 720 trade directions are the 720 nonorthogonal edges

The trade lattice has 45 antipodal minimum-vector lines.  Its orthogonality
graph is `GQ(4,2)=SRG(45,12,3,3)`, so its complement has

\[
45\cdot32/2=720
\]

edges.  The 720 unoriented local near-ovoid trade directions are **exactly**
these 720 complementary edges.  Each trade direction occurs in ten of the 480
oriented defect-dipole fibres.

For every defect dipole `(a,c)`, its six optimal completions admit a canonical
labelling by six minimum-vector lines such that the trade between completions
`i,j` is precisely the complementary-GQ edge joining their two labels.  Thus
each defect dipole determines a distinguished `K6` in the 45-state
nonorthogonality graph.  There are 480 such `K6`s and every complementary edge
lies in exactly ten of them.

## 2. The 360 minimum blockers map 8-to-1 onto the 45 carrier

Fix a W33 point `c`.  The nine minimum blockers with centre `c` have 36
pairwise differences.  These 36 differences are trade directions and form the
complete graph on a canonical nine-set `O_c` of minimum-vector lines.  The
nine blockers therefore receive canonical labels by the nine vertices of
`O_c`.

Across all 40 centres this labels all 360 blockers, and every one of the 45
minimum-vector lines occurs as a blocker label exactly eight times.  Hence

\[
\boxed{360\longrightarrow45\quad\text{with fibre size }8.}
\]

The 40 canonical nine-sets satisfy

\[
|O_a\cap O_c|=
\begin{cases}
3,&a\sim c,\\
1,&a\not\sim c.
\end{cases}
\]

Therefore W33 adjacency itself is reconstructed from this family of forty
nine-subsets inside the GQ(4,2) carrier.

## 3. The 2880 near-ovoids map 64-to-1 onto the same 45 carrier

Holotrade proved that every optimal near-ovoid `N` has a unique defect centre
`a` and that `N+{a}` is a minimum blocker; conversely every minimum blocker has
exactly eight admissible deletions giving optimal near-ovoids.  Composing that
8-to-1 map with the blocker-to-45 map gives

\[
\boxed{2880\longrightarrow360\longrightarrow45}
\]

with fibre sizes `8` and `8`, hence exactly **64 near-ovoids over each of the
45 GQ(4,2) points**.

The two independently constructed routes to the 45-state carrier agree: the
label obtained from the parent blocker is the same minimum-vector line that
labels the completion inside its six-state defect fibre.

## 4. Closed parametrization of every optimal near-ovoid

Let `a` be the near-ovoid defect centre and `c` the centre of its parent minimum
blocker.  The two points are distinct and collinear.  The six completions of
that oriented defect dipole are exactly the labels

\[
O_c\setminus O_a.
\]

Because adjacent W33 points satisfy `|O_a cap O_c|=3` and `|O_c|=9`, the set has
size six.  Hence every optimal near-ovoid is canonically parametrized by

\[
\boxed{(a,c,m):\ a\sim c,\quad m\in O_c\setminus O_a.}
\]

Counting now becomes structural rather than computational:

\[
40\cdot12\cdot6=2880.
\]

## Boundary

All maps here are finite incidence/group-action maps.  The result identifies a
new exact W33-to-GQ(4,2) quotient geometry.  It does not identify the 45-state
carrier with an unrelated physical state space without an additional physical
intertwiner.
