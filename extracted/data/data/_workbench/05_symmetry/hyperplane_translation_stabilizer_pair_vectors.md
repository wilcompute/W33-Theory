# Stabilizer action on 4 translation-vector pairs

Pairs (v and -v) chosen from the size-8 orbit of translation vectors:
- pair 0: v=(0, 1, 1), -v=(0, 2, 2), t=(2, 0, 1, 2), m_shift=(2,2,0,2), b=(2,0,2,2)
- pair 1: v=(1, 0, 1), -v=(2, 0, 2), t=(2, 1, 0, 2), m_shift=(2,0,2,2), b=(2,2,0,2)
- pair 2: v=(1, 1, 0), -v=(2, 2, 0), t=(2, 1, 1, 0), m_shift=(2,0,0,1), b=(2,2,2,0)
- pair 3: v=(1, 1, 1), -v=(2, 2, 2), t=(0, 1, 1, 2), m_shift=(0,1,1,1), b=(0,2,2,2)

Permutation multiset on these 4 pairs is in `hyperplane_translation_stabilizer_pair_permutations.csv`.
The induced action on the four pairs is S4; the sign bit gives the central Z2 (see `hyperplane_translation_stabilizer_pair_perms_with_sign_summary.md`).
Here b=(t0, -t1, -t2, t3) gives the sum-zero coordinate model where S4 acts by permuting the four b-positions.
