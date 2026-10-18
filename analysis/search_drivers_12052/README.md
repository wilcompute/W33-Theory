# Search drivers for Pass 12052 (Claude track)

Run these from this folder, in order:

1. `realforms.py` builds the Eisenstein fibration and classifies the involutions.
2. `g32.py` enumerates the Witting group G32 (155520 root permutations; writes `g32_perms.pkl`, which is not committed).
3. `census.py` computes, for every element, the fixed clock/split involutions, fixed points and fixed factorisations.

The determinant-one restriction was done inline: complex determinant via J = (2w + 1)/sqrt3. The producer freezes the
resulting Sp(4,3) table and verifies the key elements directly.
