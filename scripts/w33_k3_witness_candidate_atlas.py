"""Pass 6253-6268: K3 witness candidate atlas (ambient upper-bound form).

The repaired scaffold downgraded the 174,816 figure to an ambient upper bound.
This script records the exact finite atlas at the corrected tier:
  candidate slots = supported rows x active columns x nonzero F3 values
without claiming every slot is admissible on the actual K3 object.
"""

N_SUPPORTED = 2428
N_ACTIVE_COLS = 36
NONZERO_F3_VALUES = 2

sectors = {
    "fan_adjacent": 24,
    "remote_K33_A": 6,
    "remote_K33_B": 6,
}

ambient_upper_bound = N_SUPPORTED * N_ACTIVE_COLS * NONZERO_F3_VALUES

print("=== K3 Witness Candidate Atlas ===")
print(f"Supported rows: {N_SUPPORTED}")
print(f"Active columns: {N_ACTIVE_COLS}")
print(f"Nonzero F3 values: {NONZERO_F3_VALUES}")
print(f"Ambient upper bound on single-entry witness slots: {ambient_upper_bound}")
print()
for name, cols in sectors.items():
    sector_bound = N_SUPPORTED * cols * NONZERO_F3_VALUES
    print(f"  {name}: cols={cols}, ambient upper bound={sector_bound}")
print()
print("Correct claim tier:")
print("  - This is an ambient upper bound, not a proved admissible search set.")
print("  - Actual admissibility on the K3 side remains open.")
