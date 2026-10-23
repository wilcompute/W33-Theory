# Passes 12253–12258: a standalone note; a cross-engine audit; the rule on all 104 A8 SMs

Claude track. Producer: `analysis/w33_pass12253_to_12258_note_and_cross_engine.py`.

## 12253: the note

`papers/no_higgs_10/main.tex` (compiled to `main.pdf`) is a self-contained note on Theorem 7.7. It covers the setup, the
statistics rule with its proof, the theorem with the coset-table enumeration and its controls, and the caveats. Its numbers
are checked by the producer.

## 12254: the cross-engine audit

**Wilson-line modular invariance.** The independent engine (orbifolder 1.2.1) requires 3·W_a·W_b ∈ 2ℤ across tori
(Plöger et al., mirage torsion); the non-SUSY engine requires only ∈ ℤ.

| models | satisfy the stronger form |
|---|---|
| A8 Standard Models | 104/104 |
| twisted-10 models | 88/153 |
| of which three-generation | 32/58 |

**Matter content.**

- On the base control the two engines agree on the gauge group and on the chiral 16s.
- On the candidate models the independent engine keeps fewer Witten-twisted 10s.
- **The counts of twisted fermionic 10s are engine-dependent. The absence of a scalar 10 is not.**

## 12255: the rule on all 104 A8 SMs

From left weights alone, the rule reproduces the engine's statistics for 74,174/74,174 fields.

## 12256: the extra U(1) of SM_2496

The extra U(1) mixes with the anomalous U(1) (Tr = −6.57). Each class has exactly one anomalous U(1), so both have
massless rank 15, while a 10 vev gives 14. **The 12249 correction stands.**

## 12257: main checkout

Not synced. A parallel-track hardware file still differs from origin.
