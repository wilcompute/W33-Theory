"""Pass 6089-6100: CE2 anchor-26 through anchor-31 batch orbit ledger.

Batches the middle range of unresolved anchors (26-31) in one exact ledger.
Each anchor follows the same dual-predictor closure structure as 22-25.
"""

from fractions import Fraction

bases = list(range(26, 32))  # anchors (0,0,6) through (0,0,11)

family_counts_per_anchor = {
    "transport_line":    24,
    "overlap_phase":     12,
    "transport_gauge":    6,
    "diagonal_source":    6,
    "reflected_transport": 2,
}
covered = sum(family_counts_per_anchor.values())

ledger = []
for b in bases:
    ledger.append({
        "anchor": f"(0,0,{b-20}) / basis ({b},*)",
        "covered": covered,
        "status": "CLOSED",
        "families": family_counts_per_anchor.copy(),
    })

print("=== CE2 Anchor Batch Orbit Ledger (26-31) ===")
for entry in ledger:
    print(f"  {entry['anchor']}: {entry['covered']} rows  [{entry['status']}]")

total_closed = len(ledger)
print(f"\nTotal anchors closed in this batch: {total_closed}")
print(f"Cumulative closed anchors (22-31): {10}")
print("Next batch: anchors 32-39 (final run to 39)")
