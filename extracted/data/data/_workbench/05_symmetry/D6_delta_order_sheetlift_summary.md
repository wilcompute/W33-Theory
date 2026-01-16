# D6 delta vs element order (sheet-lift diagnostic)

Counts by order (delta=0 vs delta=1):
- order 1: delta=0 -> 1, delta=1 -> 0
- order 2: delta=0 -> 3, delta=1 -> 4
- order 3: delta=0 -> 2, delta=1 -> 0
- order 6: delta=0 -> 0, delta=1 -> 2

Observation: delta=1 picks out the order-6 elements, while order-3 elements are delta=0.
This mirrors the 2T->A4 lift: a 3-cycle in A4 lifts to order-6 or order-3 depending on the central sheet (eps=±1).
