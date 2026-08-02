# Pass 1973 — why the nine-colour solver is stuck

This pass adds no new colouring constraint.  It characterises the five tested
search configurations using the observable that was previously conflated with
orbit reduction.

## Frozen telemetry

| configuration | branches | conflicts | conflicts / 1000 branches | branches / conflict |
|---|---:|---:|---:|---:|
| plain CP-SAT | 2,127,575 | 3,622 | 1.7024 | 587.4 |
| spread-variable fixed search | 60,909 | 1,040 | 17.0747 | 58.6 |
| geometric lex, 8 generators | 198,352 | 395 | 1.9914 | 502.2 |
| spread + lex, 8 generators | 451,460 | 59 | 0.1307 | 7,651.9 |
| spread + lex, 40 generators | 512,714 | 68 | 0.1326 | 7,539.9 |

The best tested search is still the spread-variable strategy.  The combined
models use 7.412 and 8.418 times as many branches as that baseline.  Forty
lex generators increase the eight-generator combined tree by 13.568%.

## Exact conclusion

Under the frozen seeds, worker count, search mode, and time limits, the combined
encodings are strictly dominated by spread-variable branching alone.  The
40-generator model is also dominated by the 8-generator model.  This supersedes
any claim that the exact `25,920 -> 807` orbit reduction should improve CP-SAT
search.

## Structural diagnosis

The spread strategy places the 36-by-9 aggregate variables first in a
`FIXED_SEARCH` decision order.  The lex constraints live primarily on frame
variables and become informative only after a substantial prefix has already
been chosen.  Their canonical ordering preference therefore arrives after the
fixed spread decisions have committed the search to a branch.  We call this a
**propagation-horizon mismatch**.

The combined models' conflict density is about 0.13 per thousand branches—more
than 130 times lower than the spread-only model.  This means the tested solver
walks through very long locally consistent prefixes before producing a conflict
from which CDCL can learn.  It does not prove that no small unsatisfiable core
exists; the global instance is still of unknown satisfiability.  It does show
that these encodings do not expose such a core early under the tested order.

## Consequences for the next search

1. Do not put the geometric canonicaliser inside the fixed-search model.
2. Canonicalise assignments or search cubes before solver entry, then retain the
   spread-variable decision order inside each canonical cube.
3. Compare configurations by propagation counts, deterministic time, conflicts,
   restarts, and learned-clause statistics—not only branches or orbit volume.
4. Use assumptions on independently generated cubes if an infeasible cube is
   found; only then is an unsatisfiable-core analysis meaningful.
5. Treat the 807 surviving images as a group-canonicalisation benchmark, not as
   a prediction for the nine-colour search tree.

## Computer-engineering reading

The separation suggests a two-stage accelerator rather than a larger monolithic
constraint model:

- a symmetry front end computes the 36-by-9 spread signature and canonicalises
  it under the 40 point transvections;
- an exact-cover/SAT back end branches on the canonical spread variables without
  carrying the lex inequalities.

The front end is a fixed permutation, counter, dot-product, and minimum-reduction
pipeline—well suited to FPGA implementation.  This is an engineering proposal,
not evidence that the nine-colouring exists.
