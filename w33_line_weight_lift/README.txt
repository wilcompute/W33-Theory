Lift to explicit 90 non-isotropic line weights (mod 3)

This package provides an explicit linear lift from the 88D H^3 core coordinates to a 90-entry vector
indexed by the 90 non-isotropic lines of PG(3,3) (the same 90 lines used throughout the W33 construction).

Important: over GF(3), the all-ones vector lies in the augmentation module because 90 == 0 (mod 3).
Therefore the 88D quotient module is represented by 90-vectors *modulo the constant all-ones line*.
As a result, the lift is well-defined only up to adding a constant vector (c,c,...,c).

Files:
- lift_matrices_mod3.npz
  * L_88_to_90: 90x88 map from Aug88 coordinates to 90 line weights (a chosen section)
  * M_H3_to_90: 90x88 map from H3_88 coordinates to 90 line weights (M = L * T)
  * T_H3_to_Aug88: 88x88 intertwiner from H3_88 -> Aug88_twisted

- lift_helper.py
  Provides:
    lift_h3_to_line_weights(x88): compute a 90-vector of weights mod 3
    normalize_coset(w90, idx): fix a representative by forcing coordinate idx to 0 (gauge choice)

Equivariance:
Applying an automorphism to the lifted 90-vector matches the group action up to addition of a constant all-ones vector.
This is exactly the expected ambiguity for a section of the quotient by <ones>.
