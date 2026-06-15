# BT1037 — Inner-fluctuation test harness

BT1037 locks the representation-level tests needed to turn the BT1035/BT1036
module bridge into a real Connes inner-fluctuation proof.

## Targets

```text
gauge one-form profile = [1, 3, 8]
gauge one-form total   = 12
matter zero modes      = 81
doubled fermion carrier = 162
cellular QFT carrier    = 240
```

Higgs trace targets:

```text
tr_F(Phi^2)
tr_F(Phi^4)
tr_F(Delta_1 Phi^2)
```

## Locked tests

| test | status |
| --- | --- |
| `A_F` representation exists on the W33 carrier | pending matrices |
| first-order condition | pending matrices |
| self-adjoint/unimodular inner one-form span has profile `1+3+8` | target locked |
| Higgs off-diagonal scalar sector has computable traces | pending matrices |

## Honest status

This harness does not claim success. It names the next exact computation:
construct explicit `A_F` representation matrices and run the commutator-span test.

## Witnesses

```text
analysis/bt1037_inner_fluctuation_test_harness.py
data/bt1037_inner_fluctuation_test_harness.json
```
