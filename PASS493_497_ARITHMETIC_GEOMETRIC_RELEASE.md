# Passes 493–497 — arithmetic/geometric determinant-depth release

This release executes all five directions opened after Pass 492.

## 493 — decisive mixed-characteristic falsifiers

Exact fraction-free cyclotomic determinants give:

| ring | size | arithmetic budget `v_lambda(|R|)` | projective budget `|P^1(R)|` | attained depth |
|---|---:|---:|---:|---:|
| `Z/9[x]/(3x,x^2-3)` | 27 | 18 | 36 | **18** |
| `GR(9,2)` | 81 | 24 | 90 | **24** |
| `Z/9 x F_3` | 27 | 18 | 48 | **18** |

Thus the Pass-492 size-only Hjelmslev extension is refuted.

## 494 — incidence mechanism

For `R_n=Z/p^n`, reduction `P^1(R_n) -> P^1(R_(n-1))` is a uniform `p`-sheeted cover. Its incidence matrix satisfies

`A_n A_n^T = p I`,

and

`tr(A_n A_n^T)=|P^1(R_n)|=p^n+p^(n-1)`.

The cyclic depth is therefore a canonical Hjelmslev Gram trace.

## 495 — candidate phase diagram

All 13 current exact points fit

- character order `p`: `d=v_lambda(|R|)+4`;
- character order `p^r`, `r>1`: `d=min(v_lambda(|R|), |P^1(R)|)`.

The second branch remains conjectural. Eight future predictions are frozen, including `Z/49 -> 56`, `GR(25,2) -> 80`, and `(Z/9) x F_9 -> 24`.

## 496 — relative norm and negative result

Hermitian fixation gives

`N_K/Q(Delta)=N_K+/Q(Delta)^2`,

so full norms are squares and lambda-depth is even. The Hjelmslev magnitude is not the cyclotomic different: equality would require `n(p-1)=p+2`, impossible for odd prime `p` and integer `n>=2`.

## 497 — hardware observable

Weyl orthogonality fixes `||B||_F^2=q(q^2-1)` and makes normalized iid first-order phase-noise gain equal to one in expectation. A deterministic 500-section `q=9` census found maximum absolute Cohen effect size `0.156` and maximum empirical KS distance `0.112` for ordinary Euclidean proxies.

The replacement is a Galois phase cycle over `Gal(K+/Q)`: multiply determinant-gap measurements across the real embeddings to obtain the relative norm and recover lambda-depth through exact `p`-divisibility.

## Validation boundary

The algebraic identities and exact witnesses are certified. The higher-conductor minimum law is explicitly preregistered as a conjecture, not promoted to a theorem.
