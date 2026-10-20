# Passes 12111–12115: three chiral generations

Claude track. Producer: `analysis/w33_pass12111_to_12115_three_generations.py`. Models, engine outputs and drivers:
`analysis/search_drivers_12111/`.

## 12111: three generations

**Setup.** Start from the non-SUSY Z2W × Z3 models of 12106:

- Witten Z2 = (−1)^F × the split fermion parity;
- the e6 + a2 three-family shift;
- result so far: 3 × (16, 3̄) = 9 chiral 16s.

Then add **one order-3 Wilson line in the family direction**, W = α/3 with α a root of the family a2.

**Results.** Using the corpus N = 0 engines (converted and original builds); control: stock Z3 has 438 fields, 0
tachyons, net 36.

- **7 consistent models: gauge SO(10) × hidden, net chiral 16s = 3 exactly** (all untwisted), **no tachyonic fields**,
  and anomalies cancel.
- With two family Wilson lines the net is 0.

These are tachyon-free, anomaly-free non-SUSY heterotic orbifolds with exactly three chiral SO(10) generations. They are
built from Kramers² as fermion parity, the three-family shift, and a family Wilson line.

**Scope.** Non-SUSY three-generation orbifolds exist in the literature; the claim here is that the clock-grading
construction yields them. Hidden-sector and vector-like exotics are present. Yukawas, moduli and vacuum energy are not
addressed.

## 12112: the corpus Standard Models in W(3,3)

- The clock event lies in the split factorisation in 29 of 87 models, against 17.4 expected by chance.
- The Wilson-line a2 is an event fibre in only 9 of 87.

That is a mild enrichment and no sharp rule. The models are related variants, so the significance is only indicative.

## 12113: tachyons

There are none in the seven three-generation models.

## 12114: the Z6-II rejection condition

The orbifolder's own diagnostic identifies it: gcd(N_V, N_W)·(V·W) ≡ 0 **mod 2**, whereas my filter used mod 1. It
separates the 12 accepted models from the 24 rejected ones exactly.

## 12115: family textures from an SU(3)-family adjoint

- At first order the texture stays antisymmetric.
- The lowest symmetric texture is the cofactor matrix: Y ~ adj(A) = diag(a2a3, a3a1, a1a2).
- No hierarchy follows without a pattern for the vacuum value.
