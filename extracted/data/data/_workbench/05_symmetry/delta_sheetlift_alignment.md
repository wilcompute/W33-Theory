# Delta sheet-lift alignment (D6 vs 2T/A4)

D6 element orders vs delta:
- order-6 elements: [(3, 1), (4, 1)] (delta=1 for both)
- order-3 elements: [(1, 0), (2, 0)] (delta=0 for both)

2T/A4 lift pattern (from `data/_algebra/binary_tetrahedral_2t_element_orders.csv`):
- A4 3-cycles lift to order-6 (eps=+1) or order-3 (eps=-1).

Interpretation: delta behaves like the sheet bit choosing the order-6 vs order-3 lift of 3-cycles,
which is the same central Z2 that appears in the 2T -> A4 quotient.
