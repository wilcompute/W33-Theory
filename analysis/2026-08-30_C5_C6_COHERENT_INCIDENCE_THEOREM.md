# The 216 x 540 sentinel circuit coherent incidence geometry

The sentinel binary matroid contains one PSp(4,3)-orbit of 216 five-circuits and one orbit of 540 six-circuits. Acting on all `216*540=116640` ordered cross-pairs gives exactly 17 orbitals.

The cross-pairs split by support intersection size as follows:

- intersection 0: 54,000 pairs in 8 orbitals;
- intersection 1: 51,840 pairs in 6 orbitals;
- intersection 2: 6,480 pairs in 1 orbital;
- intersection 3: 4,320 pairs in 2 orbitals.

The maximal-overlap relation `|C5 cap C6|=3` is a particularly rigid biregular incidence geometry. Each five-circuit is incident with 20 six-circuits, each six-circuit with 8 five-circuits, and the relation splits into two PSp orbitals of 2,160 pairs each. Thus each colour has degrees 10 and 4 on the two sides.

For a fixed six-circuit, its six minimum-support labels induce `3K2`. Every maximal-overlap five-circuit chooses exactly one endpoint from each of those three matching edges. The eight neighbours are therefore canonically a 3-cube after choosing an endpoint orientation. The order-48 six-circuit stabilizer `C2 x S4` acts on these eight neighbours through its faithful `S4` quotient; the central `C2` is the kernel. The local action splits the cube into two invariant tetrahedra `4+4`, represented by the two parity classes. Endpoint reversals may exchange the words "even" and "odd", but not the intrinsic unordered 4+4 partition.

This gives an exact two-colour maximal-overlap incidence structure linking the 216 and 540 circuit shells.

Reproducibility:
- `analysis/w33_20260830_c5_c6_coherent_incidence.py`
- `data/PART_W33_20260830_C5_C6_COHERENT_INCIDENCE.json`
- exact-continuation run `33337524115` passed.

Boundary: the local cube parity resembles other project chirality splittings, but no identification with Holotrade or photonic chirality is asserted without an equivariant map.
