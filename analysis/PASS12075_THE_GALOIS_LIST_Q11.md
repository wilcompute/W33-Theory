# Pass 12075: the Galois list at q = 11

Claude track. Completes 12063 and 12070.

## Results at q = 11

All counts are exact, from GAP with |Sp(4,11)| = 25,721,308,800.

- **Observers.** 7260 observers, each with Lorentz group SL(2,121).
- **Relativity principle.** The point stabiliser (17,569,200) is transitive on the observers.
- **Clock analogues.** Two classes of index 11, one for each A₅ class of PSL(2,11). Each has order 1,597,200 and 11
  conjugates, is not normal, and is transitive on the observers.
- **No rest frames.** No clock pair fixes an observer: the common symmetry is 1100 for collinear pairs and 120 or 1200
  for non-collinear pairs.

## The whole Galois list

| q | 3 | 5 | 7 | 11 |
|---|---|---|---|---|
| observers | 36 | 300 | 1176 | 7260 |
| relativity principle | holds | holds | holds | holds |
| clock group normal | yes | no | no | no |
| mirror rest frames | 3 per compatible pair | none | none | none |

Only q = 3 has rest frames.

## Certificates

- Producer: `analysis/w33_pass12075_the_galois_list_q11.py`, which checks the frozen output
  `analysis/search_drivers_12075/q11.out`.
- GAP driver: `analysis/search_drivers_12075/q11.g`.
