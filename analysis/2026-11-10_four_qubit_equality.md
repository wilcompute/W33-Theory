# The 48 equality rays for the four-qubit nine-basis bound

Pass 12645 certifies the sharp minimum `F = 1/16` for its specified nine Pauli bases. This replay freezes its denominator-four dual and proves the converse to the exhibited stabilizer examples. The only unit rays attaining the bound are the 48 vectors of the three once-meeting stabilizer bases.

## Exact dual and kernel

Let `U` be the uncovered Pauli labels, `T` the symmetric dual multiplier on anticommuting pairs, and `M = 14I − J − T`. There are three disjoint 14-subsets `S_i = L_i minus C` where the Lagrangian `L_i` meets the covered set `C` once. Each indicator `1_{S_i}` is in the kernel of `M`. Let `P` be the orthogonal projection onto their span. Removing one coordinate per indicator makes the remaining 117-coordinate space a complement of that span. The fraction-free Sylvester replay verifies strict positivity of the corresponding principal minor of `280(M − (I − P)/5)`. Hence `M` has exactly the three indicated null directions, and the positive spectrum has gap at least `1/5`.

## Equality and a fidelity estimate

For a unit vector `ψ`, set `x_a = ⟨ψ,P_a ψ⟩`, `v_a = x_a P_a ψ`, and `S = Σ_{a∈U} x_a²`. The real Gram of the vectors `v_a` has zeros on anticommuting pairs. Its trace is `S`, and `||Σ_a v_a||² ≥ S²` by overlap with `ψ`. Thus the dual gap gives

`S(14 − S) ≥ ⟨v,Mv⟩ ≥ ||(I−P)v||²/5`.

At equality, `F = (15−S)/16 = 1/16`, so the vectors `v_a` are constant on each `S_i` and vanish outside their union. Some group has nonzero common vector. On that group, the signed unit vectors `sign(x_a)P_a ψ` agree. Fix a label `b` in the group. The products `P_b P_a` fix `ψ` up to sign. The 14 labels in `S_i` affinely span `L_i` because a proper affine subspace has size at most eight. Therefore these products generate the full commuting stabilizer, and `ψ` lies on one of its 16 joint eigenrays. The three sets have distinct Lagrangians and therefore distinct joint eigenrays. Conversely, each such ray has 14 uncovered Pauli expectations of modulus one and attains the bound.

For an explicit stability estimate, let `δ = ||(I−P)v||²` and choose the group with largest mean-vector norm `||c||`, so `||c||² ≥ (S−δ)/42`. If `8δ/||c||² < 1`, every expectation in that group is nonzero. Write `e_a = ||v_a−c||`. Normalizing the vectors shows that the four independent products relative to an anchor `b` have signed eigenvector errors at most `2(e_b+e_a)/||c||`. The sum of the four corresponding projector failure probabilities is at most `8δ/||c||²`. The projectors commute, so their joint eigenray has squared fidelity at least `1−8δ/||c||²`. When the bound is vacuous it holds trivially. Combining with the dual gap, a normalized state with excess `ε = F−1/16` and `0 ≤ ε < 1/80` has some listed ray with squared fidelity at least `1 − 26880 ε/(1−80 ε)`. The constant is a certified estimate.

The calculation applies to the saved four-qubit nine-basis set. It gives a state-identification certificate for that measurement geometry. The three-qubit tight value and the classification of all four-qubit nine-basis sets remain separate questions. [Pass 12645](PASS12645_EXACT_FOUR_QUBIT_ONE_SIXTEENTH.md), [Graph uncertainty relation](https://doi.org/10.1103/PhysRevA.107.062211)

Run `python analysis/toe_20261110_four_qubit_equality.py` for the independent replay without a numerical SDP. The edge multipliers are stored in lexicographic order on sorted uncovered labels. [Frozen dual](../data/toe_20261110_four_qubit_equality.json)
