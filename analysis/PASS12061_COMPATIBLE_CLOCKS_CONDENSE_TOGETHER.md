# Pass 12061: compatible clocks condense together

Claude track. Builds on 12055 (the microscopic tick model) and 12060 (rest frames).

## Question

Suppose the tick condensate carries two clocks. Do they prefer jointly measurable (collinear) events, which give
rest frames by 12060, or non-collinear ones, which leave spin only?

## Exact spectra

H = h_a + h_b, with h = I − Π_k(p). Write β = 1/T and x = e^(−β).

| Pair type | Spectrum of H | Partition function |
|---|---|---|
| same point | {1⁶, 2³} | Z = 6x + 3x² |
| collinear | {0, 1⁴, 2⁴} | Z = 1 + 4x + 4x² |
| non-collinear | {(1 ∓ 1/√3)³, 2³} | Z = 6x cosh(β/√3) + 3x² |

## Theorem

- Z_col − Z_far = 4x[sinh²(β/2) − 3 sinh²(β/(2√3))] > 0 for all β > 0, because sinh(t)/t is increasing.
- Z_col − Z_same = (1 − x)² > 0.
- Hence **F_col < F_far < F_same at every temperature.**
- At high temperature the collinear–far gap closes only at fourth order: β⁴/18 − β⁵/18 + … (sympy series).
- Unequal weights (t, 1 − t) keep the same ordering on a 19 × 5 grid of t and T.

## Reading

Two clocks condense on compatible events. The reason is that compatible ticks share a zero mode, while mutually
unbiased (non-collinear) ticks do not. By 12060, such a pair defines exactly three mirror rest frames.

## Scope

12055 still prefers a single tick at fixed total rate. Why the condensate would carry two ticks is not derived here.

## Correction during the pass

My hand expansion gave a fourth-order coefficient of 1/12. sympy gives 1/18, and the producer now asserts the sympy
series.

Producer: `analysis/w33_pass12061_compatible_clocks_condense_together.py`.


## Withdrawn reading (Pass 12072)

The sentence "by 12060, such a pair defines exactly three mirror rest frames" assumed that Clifford ticks are clocks. Pass 12072 proves there is no equivariant tick-to-clock map, so that reading is **withdrawn**. The spectra and the inequality F_col < F_far < F_same stand. Pass 12068 further shows that a capacity cost condenses a whole context, never a pair.
