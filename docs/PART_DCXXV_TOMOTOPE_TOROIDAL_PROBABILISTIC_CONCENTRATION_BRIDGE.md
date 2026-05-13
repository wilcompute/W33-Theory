# Part DCXXV — Tomotope/Toroidal Probabilistic Concentration Bridge

This part upgrades DCXXII from a sample probability claim to a confidence-certified claim.

---

## 1. Statistical certificate

Given Bernoulli stability outcomes from DCXXII (`stable` vs `unstable`), compute the Wilson lower confidence bound at 99% confidence.

---

## 2. Robust condition

Require both:

```text
sample stability probability > 0.95,
Wilson lower bound > 0.95.
```

This means the claim remains above 95% under a conservative confidence correction.

---

## 3. Executable artifact

Script:

```text
scripts/tomotope_toroidal_probabilistic_concentration_bridge.py
```

Output:

```text
data/tomotope_toroidal_probabilistic_concentration_bridge.json
```

with confidence z-value, Wilson bound, and pass/fail identities.
