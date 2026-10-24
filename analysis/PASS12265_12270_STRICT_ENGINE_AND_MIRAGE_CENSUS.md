# Passes 12265–12270: the missing check found, the engines reconciled, every flagged model repaired

Claude track. Producer: `analysis/w33_pass12265_to_12270_strict_engine_and_mirage_census.py`. Drivers:
`analysis/search_drivers_12265` … `_12268`.

## 12265: corpus-wide audit against two builds of the engine

All 4514 T6/Z3 model files in the corpus were run through three checks:

- the stock non-SUSY orbifolder ("lenient");
- a patched build ("strict"; see 12268);
- the Python Plöger audit.

| lenient | strict | audit | models |
|---|---|---|---|
| loads | loads | clean | 2434 |
| loads | rejects | (7f) only | **497** |
| rejects | rejects | (7d) fails | 1577 |
| rejects | rejects | clean | 6 (they fail the shift-shift condition (7c), which the audit does not test) |

The audit and the engines agree exactly. The stock engine **does** enforce (7d) mod 2 and **skips** (7e)/(7f). That corrects the
12259 wording "checks (7f) only mod 1": it does not check them at all.

Status of the lead models:

- **Consistent:** S002, the 104 A8 Standard Models, the 12111 bases and SM_2496 (Z6-II).
- **Lenient-only:** T115 (N008_F1_04_S037_T115, used in 12121–12155).

## 12266: the engine disagreement resolved

The `*_n0`-patched orbifolder 1.2.1 build was rebuilt with sector output. The earlier link failure had a simple cause: the patched
sources had never been compiled.

On the 12254 models the rebuilt engine reproduces the stored output. It agrees with the non-SUSY engine **field for field** in the
untwisted sector and both Z3-twisted sectors, 10 counts included.

It has **no Witten-twisted sector at all**. Every Witten-twisted fixed brane fails the local condition N(V_loc² − v_loc²) = 0 mod 2
and is dropped: 55 warnings per model, the control included. Every extra 10 of the non-SUSY engine sits in a Witten-twisted sector.
The disagreement is therefore an artefact of the patched engine, not of the models.

## 12267: mirage-torsion repairs, census

Shifting one torus' Wilson lines by a lattice vector D changes the Plöger data by a homomorphism of E8×E8. A repair therefore exists
iff the defect lies in the image subgroup, which is built exactly from the 480 roots.

- **Repairs found:** all 497 lenient-only models are repairable. 486 can be repaired on one torus and have a second independent
  repair; 11 need shifts on two tori.
- **Comparison:** the stock spectrum of each input against the strict spectrum of each repair, covering gauge factors, U(1)
  directions, and every field with its sector, fixed point, dimensions and U(1) charges.
- **Result: identical in 983/983.** T115 is included (750 fields).

So every lenient-only corpus model is the stock-engine shadow of a consistent model with the **same** spectrum. The consistent-subset
restatement of 12259/12261 was too strict, and **the original counts stand**: 12163, 12182, the twisted-10 models and T115.

Why this holds at order three is tested in 12271: there it is a property of the order, not luck.

## 12268: the bug and the fix

In `COrbifoldGroup::CheckModularInvariance` the failure flag for the Wilson-line products is set only inside
`if (info) if (verbose) {...}`, and `verbose` is hard-coded false. `CRandomModel::Create` has the same pattern for an ill-defined
orbifold group.

- **Patch:** `search_drivers_12268/nonsusy_orbifolder_strict.patch`. Local binaries are in `~/orb/nsostrict`.
- **Driver pre-check:** `ploger_gate.py`. It agrees with the strict engine on 4508/4514; the 6 exceptions are the (7c) inputs, which
  are outside its scope.

## 12269: main checkout

Still blocked; see the round report. One parallel-track file truly differs:
`hardware/tb_w33_linebus_phase_frame_random_20261023.sv`.
