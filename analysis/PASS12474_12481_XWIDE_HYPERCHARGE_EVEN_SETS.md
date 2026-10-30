# Passes 12474–12481: SM_2541 cannot reach k_Y < 5/3 even with finer charges; a symmetry break for even line sets

Claude track. Producer: `analysis/w33_pass12474_to_12481_xwide_hypercharge_even_sets.py`. Drivers: `analysis/search_drivers_12466`
(`even_line_sets.py ... sym2`) and `analysis/search_drivers_12468` (`ysearch.py` with `XWIDE`, `KCAP` and `YS_TL`).

## 12475: the 1/18 charge menu is closed too

**The question left open by 12469.** For SM_2541_c22 the one-generation floor is k_Y = 1.187, below the 1.29 that unification needs.
In the 1/6 charge menu, no three-generation hypercharge reaches k_Y ≤ 5/3. Do finer exotic charges change that?

**The run.**

- **Menu:** every non-quark field may take Y ∈ {−2, −35/18, …, 2}, steps of 1/18.
- **Cap:** the necessary L1 condition Σ|t_j| ≤ 4√(K/2) at K = 5/3.
- **Time limit:** 4 hours per solve.
- **Termination:** the enumeration ends *infeasible*, not at a time limit, so it is complete.

**Result.** It finds only k_Y = 17/3 and 461/81 ≈ 5.69, both above 5/3, and every solution's charges are exact. So:

> **Proved:** SM_2541_c22 has no three-generation, anomaly-free hypercharge with k_Y ≤ 5/3, in either the 1/6 menu (12469) or the
> 1/18 menu (|Y| ≤ 2).

**Reading.** The one-generation floor of 1.19 is not attainable by a full spectrum: the obstruction comes from requiring three
generations together with vector-like pairs. Within this model family the window 1 ≤ k_Y < 5/3, which 12131 and 12154 require for
unification, is out of reach.

## 12474: a line-pair symmetry break for even line sets

Every point of line 0 is covered an even number of times, so some second chosen line meets line 0. The stabiliser of line 0 acts
transitively on the lines meeting it, so that second line can be fixed without loss of generality.

- **Control:** the q = 5 exact minimum of 20 is reproduced, in half the time (28 s versus 56 s).
- **q = 7: the minimum is exactly 40** (optimal, 2.2 h with the reduction; coverage {0, 2}). That **refutes** the 5(q − 1) = 30 guess
  of 12467. The minima are 6, 10, 20, 40 at q = 2, 3, 5, 7; the odd-q values fit 5·2^((q−1)/2) [conjecture, three points].
