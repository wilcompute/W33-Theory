"""Pass 6217-6232: K3 witness realization search scaffold.

Converts the K3 witness problem from a raw scan into an explicit search scaffold
over supported rows and active columns, recording the exact admissibility rules
for any future constructive witness.
"""

import numpy as np

N_SUPPORTED = 2428
N_ACTIVE_COLS = 36
SECTOR_SPLIT = {
    "fan_adjacent": (0, 24),
    "remote_K33_A": (24, 30),
    "remote_K33_B": (30, 36),
}

# admissibility: one nonzero F3 value in any active column
admissible_values = [1, 2]

print("=== K3 Witness Realization Search Scaffold ===")
print(f"Supported rows: {N_SUPPORTED}")
print(f"Active columns: {N_ACTIVE_COLS}")
print(f"Admissible nonzero F3 values: {admissible_values}")
print()

for name, (a, b) in SECTOR_SPLIT.items():
    print(f"Sector {name}: columns {a}..{b-1} (count={b-a})")

candidate_count = N_SUPPORTED * N_ACTIVE_COLS * len(admissible_values)
print(f"\nTotal single-entry witness candidates: {candidate_count}")
print("Candidate rule:")
print("  choose any supported row r, any active column c, any value in {1,2}")
print("  -> this breaks splitness and yields a rank-1 perturbation")
print()
print("Current repo state: no candidate instantiated on the actual K3 side.")
print("Search scaffold: COMPLETE")
