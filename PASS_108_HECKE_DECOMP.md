# Pass 108: Hecke Eigenform Decomposition of Theta_{Lambda_C}

## Space Structure

| Property | Value |
|----------|-------|
| Space | M_20(Gamma_0(2)) |
| dim total | 6 |
| dim S_20 (cusp) | 4 (= 2 old + 2 new) |
| dim Eisenstein | 2 |
| W_2=+1 eigenspace dim | 3 |

## Plus Eigenspace Basis

1. **E_20^inf** -- Eisenstein series for cusp at infinity
2. **f_old+** = Delta(tau)*E_8(tau) + Delta(2tau)*E_8(2tau) -- W_2=+1 old form
3. **f_new+** -- unique W_2=+1 newform at level 2, weight 20; has a_2 = -512 = -2^9

The newform eigenvalue a_2 = -512 follows from: W_2(f) = -a_2/2^9 * f = +f => a_2 = -2^9.

## Decomposition

Theta_Lambda_C = alpha * E_20^inf + beta * f_old+ + gamma * f_new+

- alpha = 1 (from q^0 constant term)
- beta, gamma: rational, determined by q^4=80 and q^8=14640 once f_new+ q-expansion is known
- **Large Eisenstein/cusp cancellation**: E_20[q^4] ~ 2.08e10 >> 80 (analogous to Leech/E_12/Delta)

## Key Structural Results (all proved)

1. Theta in W_2=+1 eigenspace (O+(8,2) plus-type disc form)
2. Theta uniquely determined by 3 coefficients in 3-dim space
3. f_new+ has a_2 = -2^9 (Atkin-Lehner + W_2 eigenvalue)
4. beta, gamma are rational (integer theta + rational Hecke action)
