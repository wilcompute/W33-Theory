# BT911 — Profile-to-observable Fitter with Guardrails

BT911 builds a constrained fitter over the BT907 substrate-generated rational inventory.

## Guardrails

The fitter is deliberately conservative:

1. no continuous real parameters;
2. only substrate-generated fractions;
3. misses must be reported rather than forced;
4. the profile layer stays separate from the shifted-reflection Yukawa support skeleton;
5. the BT910 \(+1\) sentinel coordinate is not an extra generation.

## Exact inventory matches

| observable | fraction | substrate formula |
|---|---:|---|
| Cabibbo scaffold | \(9/178\) | \(q^2/(\Phi_3^2+q^2)\) |
| PMNS solar archive | \(4/13\) | \(\mu/\Phi_3\) |
| PMNS reactor archive | \(2/91\) | \(\lambda/(\Phi_6\Phi_3)\) |
| PMNS atmospheric archive | \(7/13\) | \(\Phi_6/\Phi_3\) |
| Koide archive | \(2/3\) | equal \(S_3\) singlet/doublet norm |
| contextual fraction | \(1/10\) | \(1/\Phi_4\) |
| KS budget | \(36/40=9/10\) | \((q!)^2/v\) |

## Boundary

This is still not a measured-data derivation. It is a guarded exact-inventory fitter showing that the current profile coordinate system covers the archived numerical scaffold without free continuous parameters.

## Conclusion

\[
\boxed{\text{The profile observable package is exactly inventory-generated, but remains a coordinate match until tied to measured masses and uncertainties.}}
\]

## Witness

```text
analysis/bt911_profile_observable_fitter.py
data/PART_BT911_PROFILE_OBSERVABLE_FITTER_results.json
```
