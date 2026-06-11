# BT762 — Phase-Duo / Pluecker Reproducibility Manifest

This is the reproducible end-to-end run order for the BT753--BT761 stack.

## Goal

Move from local selector candidates to globally glued phase-duo selectors and then to the \(Q(4,3)\) Pluecker target.

The chain is:

```text
BT753 local phase+duo enumeration
BT756 local execution contract
BT761 global BT741 gluing runner
BT758 Q(4,3) finite-geometric target verifier
BT760 Q(4,3) oriented-apartment mirror harness
```

## Step 1 — local phase-duo enumeration

```bash
python analysis/bt753_phase_duo_candidate_enumerator.py \
  --out data/bt753_phase_duo_candidate_enumerator.json
```

Expected local candidate universe:

```text
{0,1} x {0,...,5} x {0,1} = 24 candidates
```

Every locally passing candidate must satisfy:

```text
selected_rows = 2160
rank_mod_1000003 = 81
root_triples_hit = 540
root_hit_distribution = {"4": 540}
root_uniform_4 = true
```

## Step 2 — attach BT741 register quotient

Produce or refresh:

```text
data/bt741_global_register_quotient.json
```

Required per-candidate fields:

```text
number_of_global_register_classes
global_register_dimension
each_class_nonempty
flat_transport
```

## Step 3 — fail-closed gluing acceptance

```bash
python analysis/bt761_phase_duo_gluing_runner.py
```

Output:

```text
data/bt761_phase_duo_gluing_results.json
```

Acceptance requires all five tests:

```text
T1 selected_rows = 2160
T2 rank_mod_1000003 = 81
T3 root_triples_hit = 540
T4 root_hit_distribution = {4: 540}
T5 global_register_dimension = 4 with 16 nonempty classes and flat transport
```

## Step 4 — verify the \(Q(4,3)\) target

```bash
python analysis/bt758_q43_plucker_model_verifier.py
```

Expected target checks:

```text
Q43_point_count_40 = true
Q43_line_count_40 = true
each_line_has_4_points = true
each_point_on_4_lines = true
point_collinearity_SRG_40_12_2_4 = true
dual_line_graph_SRG_40_12_2_4 = true
```

## Step 5 — verify oriented-apartment mirror target

```bash
python analysis/bt760_q43_duo_transport_harness.py
```

This verifies the target-side mirror/orientation reversal. It does not by itself prove the duo identification.

## Step 6 — final missing transport table

To prove the actual BT750-to-Pluecker claim, add:

```text
data/bt760_root_torsor_to_q43_transport.json
```

and require:

```text
T6a: tau(r^6 x) is defined for every local lift coordinate x
T6b: tau(r^6 x) has the same underlying Q(4,3) apartment as tau(x)
T6c: tau(r^6 x) reverses the dual-apartment orientation or applies the candidate Pluecker polarity
T6d: the action has order 2 and no fixed oriented frame
```

## Current honest boundary

BT758 and BT760 verify the \(Q(4,3)\) target and target-side mirror. BT761 enforces gluing fail-closed. The theory should not claim

```text
duo bit = Pluecker mirror
```

until the explicit root-torsor-to-\(Q(4,3)\) transport table passes T6a--T6d.
