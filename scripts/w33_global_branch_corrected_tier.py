"""Pass 6269-6284: global branch theorem at corrected claim tier.

Restates the branch theorem after scaffold claim-tier repair.
Only items still supported at the corrected tier are promoted.
"""

exact_items = [
    "CE2 global orbit closure complete.",
    "K3 deformation theory is unobstructed in the abelian F3 setting.",
    "Current K3 split shadow scan found no nonzero active-column witness.",
    "CE2/K3 evidence repair and scaffold claim-tier repair are complete.",
]

conditional_items = [
    "Transport-cocycle scaffold is only a conditional metric toy, not an identification theorem.",
    "K3 witness candidate count is only an ambient upper bound, not a realized admissible set.",
]

open_items = [
    "An actual K3-side nonzero witness.",
    "A repo-native transport cocycle that closes the family-flag comparison.",
    "A non-conditional global branch/orientation theorem.",
]

print("=== Global Branch Theorem (Corrected Tier) ===")
print("\nExact items:")
for x in exact_items:
    print(f"  [EXACT] {x}")
print("\nConditional items:")
for x in conditional_items:
    print(f"  [CONDITIONAL] {x}")
print("\nOpen items:")
for x in open_items:
    print(f"  [OPEN] {x}")

completion_ratio = len(exact_items) / (len(exact_items) + len(conditional_items) + len(open_items))
print(f"\nCorrected structural closure ratio: {completion_ratio:.2%}")
print("Status: branch theorem remains open at corrected claim tier.")
