# Weak family gauging at the canonical W33 E6-only candidates

With only E6 gauged and a rank-two mixed adjoint coupling, the two canonical cubic supports give explicit trial central-charge maxima. Weak family gauging is irrelevant at both. More generally, any candidate that permits marginal or relevant family gauging must contain additional free operators charged under the family group. Pure adjoint free operators cannot enable it. The calculation concerns four-dimensional unitary N=1 fixed points with the stated fields and ordinary free-chiral accidental symmetries. A trial maximum is a necessary fixed-point test, and existence of the interacting theories is open. [Both-gauge rank-two calculation](2026-11-12_canonical_uv_fixed_point.md) · [Lower-rank relevance bounds](2026-11-12_mixed_rank_relevance.md)

## Exact anomaly and trial maxima

Write r for the adjoint scalar R charge and Σ for the sum of the five bifundamental scalar R charges. Vanishing of the E6 gauge anomaly implies `3Σ+4r=15`. The spectator S is a decoupled free multiplet in this superpotential and has R charge 2/3. In the convention `β_f(g)=−b_f g³/(16π²)+…`, the leading coefficient upon weakly gauging the family current is

```text
b_f = 3(3 + Tr R_f T_family²)
    = 3/2 − 54r + 3 C
C   = Σ_free (2/3 − R_trial(O)) T_family(O).
```

The trace uses Weyl R charges and fundamental Dynkin index 1/2. The correction sum covers additional independent free operators with a family index. The spectator contribution is already in the term 3/2. This follows from the mixed R-gauge anomaly form of the supersymmetric gauge beta function. [Weak flavor gauging and the anomaly condition](https://arxiv.org/abs/2111.12092) · [Free-chiral corrections](https://arxiv.org/abs/hep-th/0308071)

The E6 gauge constraint and active cubic equations give the same X, Z and A trial charges as in the both-gauge calculation. Fixing S at 2/3 changes the central-charge polynomial. With the alternating cubic, the paired X charges are `1/2−r/3±t`, the paired Z charges are `3/2−2r/3∓t`, and the remaining X charge is `1+2r/3`. Without the alternating cubic, each X-Z pair has mean `1−r/2` and an independent splitting. The remaining X charge is again `1+2r/3`. In both cases the splitting part of the trial central charge is a negative constant times r times the squared splitting norm. It vanishes on the axis. The r derivatives there are `9(288r²−612r+245)/64` and `9(369r²−936r+488)/64`, respectively.

| Alternating cubic | Uncorrected local maximum r | Weak family coefficient b_f |
| --- | --- | --- |
| Present | `17/16−sqrt(641)/48` | `(−447+9sqrt(641))/8 ≈ −27.39` |
| Absent | `52/41−2sqrt(1082)/123` | `−5493/82+36sqrt(1082)/41 ≈ −38.11` |

The Hessian test selects the lower root in each case. The scalar charges at these points pass the polynomial chiral-operator unitarity test. With the alternating cubic, every X charge exceeds 2/9 and each Z charge exceeds 2/3. The E6 center requires any invariant with X and without Z to contain at least three X fields. Without the alternating cubic, every X and Z charge exceeds 1/3 and a matter invariant needs at least two factors. In both cases r exceeds 1/3 and the first adjoint invariant has degree two. Hence neither maximum calls for any extra free-chiral correction. The two central charges also lie below the massless Gaussian values for the same elementary content. They cannot serve as ultraviolet endpoints of a nontrivial unitary flow to that Gaussian theory. [Four-dimensional a-theorem](https://arxiv.org/abs/1107.3987)

## What an accidental sector would need to supply

Convexity of the standard corrections implies that a corrected maximum must lie in the negative-semidefinite region of the bare Hessian. With the alternating cubic this gives `0≤r≤17/16` and `t²≤(8/27)r(17/16−r)`. Without it, the two splitting squares have sum at most `(41/54)r(52/41−r)`, with `0≤r≤52/41`. At r=0 the mixed Hessian entries force all splittings to zero. Within these regions the same matter-charge estimates used at the explicit maxima exclude any family-charged operator below the unitarity bound through `r=1/6` with the alternating cubic and through `r=1/3` without it.

With C=0, weak gauging could be marginal or relevant only if `r≤1/36`. In this small interval, only the primitive pure-adjoint operators can supply corrections. The correction is independent of the splittings, which therefore vanish at a candidate maximum. Including every primitive below the bound still leaves the r derivative strictly positive. The exact lower bounds on that derivative over the larger interval `0≤r≤1/3` are 189/64 and 1953/64. Above 1/3 the adjoint primitives all clear the bound. Thus neither branch has a further maximum if free operators are restricted to the adjoint sector.

Any candidate permitting marginal or relevant family gauging must therefore have C>0. The matter bounds force `r>1/6` or `r>1/3` respectively. Since `b_f≥0` requires `C≥18r−1/2`, the required correction is strictly larger than 5/2 or 11/2. Positivity of the ungauged family current also requires `C<18r+5/2`. The full correction must lie in this interval of width three at the candidate r. Establishing whether such a sector can occur requires the interacting chiral ring and the full corrected extremization.

Run `python analysis/toe_20261112_e6_only_weak_gauging.py` from the repository root. [Exact output](../data/toe_20261112_e6_only_weak_gauging.json)
