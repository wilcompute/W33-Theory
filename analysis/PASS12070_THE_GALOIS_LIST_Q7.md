# Pass 12070: the Galois list at q = 7

Claude track. Continues 12063.

## Question

By Galois's theorem, index-q clock analogues exist only for q ∈ {2, 3, 5, 7, 11}. Pass 12063 covered q = 5. What
happens at q = 7?

## Results at q = 7

All counts are exact, from GAP with |Sp(4,7)| = 276,595,200.

- **Observers.** 1176 observers, each with Lorentz group SL(2,49) (|C(J)| = 117600).
- **Relativity principle.** The point stabiliser (691,488) is transitive on the observers.
- **Clock analogues.** Two classes of index-7 subgroups, one for each S₄ class of PSL(2,7). Each contains U, has
  |K/U| = 288 and 7 conjugates, is not normal, and is transitive on the observers.
- **No rest frames.** Clock pairs have common symmetry 252 (collinear) and 48 or 288 (non-collinear). None of them fixes
  an observer.

## Conclusion

| | q = 3 | q = 5 | q = 7 |
|---|---|---|---|
| relativity principle | holds | holds | holds |
| mirror rest frames | **3 per compatible pair** | none | none |

Rest frames from compatible clocks occur only at q = 3, where the clock group is normal.

## Scope

- q = 11 was not computed.
- The pair data use one collinear and one non-collinear partner, over all 7 conjugate clock choices. Rank-3
  transitivity covers the remaining partners.

## Certificates

- Producer: `analysis/w33_pass12070_the_galois_list_q7.py`, which checks the frozen output
  `analysis/search_drivers_12070/q7.out`.
- GAP driver: `analysis/search_drivers_12070/q7.g`, about an hour to rerun.
