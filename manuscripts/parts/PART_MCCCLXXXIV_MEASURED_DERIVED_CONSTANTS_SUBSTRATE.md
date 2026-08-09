# Part MCCCLXXXIV — Measured and Derived Constant Substrate Witnesses

This part extends the SI defining-constant substrate chain to nearby
measured, conventional, and SI-derived constants.

The boundary is explicit: these are unit-scaled decimal witnesses, not
dimensionless predictions.  The verifier keeps exact conventional standards,
exact SI-derived constants, and rounded measured CODATA mantissas in separate
classes.

## Verified Witnesses

| Constant | Status | Unit-scaled integer | Substrate form |
|---|---:|---:|---|
| Newtonian constant `G` | CODATA measured rounded mantissa | `667430` | `r*F5*p11*(Phi12*p10+(q!)^2)` |
| Standard gravity `g0` | conventional exact | `980665` | `F5*Phi6*(Phi12*(q^q*Phi3+2^F5)+q!*Phi4)` |
| Standard atmosphere | conventional exact | `101325` | `q*F5^2*Phi6*(2^Phi6+F5*Phi3)` |
| Proton mass energy equivalent | CODATA measured rounded mantissa | `938272` | `2^F5*(Phi4^2+q^2)*(mu^4+Phi3)` |
| Faraday constant | SI-derived exact, rounded display mantissa | `9648533` | `p11*(mu*alpha_int-1)*(mu*alpha_int+q*Phi6)` |
| Molar gas constant | SI-derived exact, rounded display mantissa | `8314463` | `(F5*Phi3+r*Phi6*Phi12)*(Phi6*L_eff-2^Phi6)` |

## New Molar-Gas Lock

The gas constant was not resolved in the prompt hint.  The verifier finds:

```text
R * 10^6 rounded = 8,314,463
8,314,463 = 1087 * 7649
1087 = F5*Phi3 + r*Phi6*Phi12 = 5*13 + 2*7*73
7649 = Phi6*L_eff - 2^Phi6 = 7*1111 - 128
```

Here `L_eff = 1111` is the alpha effective-volume denominator
`p_Ih*((k-lambda)^2+1)`.

## Classification Boundary

`G` and the proton mass are measured CODATA values.  The promoted integers are
rounded displayed mantissas, not exact definitions.

`g0` and `1 atm` are exact conventional standards.

`F = N_A e` and `R = N_A k_B` are exact SI-derived constants after the 2019 SI
redefinition, but the integers above are rounded display mantissas.

## Verification

Run:

```bash
python3 analysis/w33_MCCCLXXXIV_measured_derived_constants_substrate.py
```

The verifier checks all six substrate forms, their factorization boundary, and
the new molar-gas decomposition.
