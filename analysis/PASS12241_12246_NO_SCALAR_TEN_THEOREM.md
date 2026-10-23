# Passes 12241–12246: Theorem 7.7 — no scalar 10 in any sector

Claude track. Producer: `analysis/w33_pass12241_to_12246_no_scalar_ten_theorem.py`. Drivers:

- `analysis/search_drivers_12243/exhaust2.py`
- `analysis/search_drivers_12238/higgs_branch.py`
- `analysis/search_drivers_12230/` (Z6-II exception)
- `analysis/search_drivers_12224/twoline4.py`

## 12241: the consistent subspace

| scope | counts |
|---|---|
| one line | 165,465 consistent configurations; 294 consistent twisted-10 candidates (density 0.178%) |
| two lines, even-only sample | 366/20,000 = 1.83%, 0 scalar |

The engine-built counts of 12161–12182 are unchanged.

## 12242: the Z6-II exception

In the Witten-twisted θ² and θ⁴ sectors of the order-six twist, bosons and fermions share their right-moving weights, and
one boson record duplicates a fermion record exactly. I suspect a labelling artefact in the engine; this is not
established. **No result uses these sectors.**

## 12243: THEOREM — exhaustive two-line test

Over all consistent pairs of A4-type lines with the same A4 and 3·W1·W2 integral:

- **77,192,286 pairs**;
- 1,417,482 carry a twisted 10 (1.84%, matching the 1.83% sample);
- **0 scalar.**

Positive control: all 366 sampled hits are found.

## 12244: the hidden SU(5) of SM_2496

The roots that the shift-broken class keeps inside the hidden SU(5) are exactly the stabiliser (A2+A1) of one of the
unbroken class's scalar-10 weights. **The shift class is the Higgs branch of the hidden scalar 10**, as group theory; no
potential is computed.

## 12245: Theorem 7.7

The paper now states Theorem 7.7: no Higgs 10 on the e6+a2 route with one or two SU(5)-type lines.
