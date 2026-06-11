# BT757 — Phase-Duo Gluing Verifier

## Statement

BT753 and BT754 test the local phase-duo selector candidates

\[
(\epsilon,\phi,\delta)\in\{0,1\}\times\{0,\ldots,5\}\times\{0,1\}.
\]

The missing global test is the BT741 gluing condition:

\[
\boxed{\text{local selector rows must descend to one flat global }\mathbb F_2^4\text{ register.}}
\]

BT757 records the verifier specification and the fail-closed rule.

## Inputs

The verifier consumes:

```text
data/bt753_phase_duo_candidate_enumerator.json
```

and the BT741 local-register quotient relation from the existing selector-bundle layer.

## Test T5: gluing

For a candidate \(c=(\epsilon,\phi,\delta)\), build the relation graph whose vertices are the local BT753 rows and whose edges identify two rows when BT741 says their local register coordinates represent the same transported global register coordinate.

The candidate passes T5 exactly when:

```text
number_of_global_register_classes = 16
global_register_dimension = 4
each class is nonempty
transport is flat around every lifted Levi 8-cycle presentation
```

Equivalently, the quotient must be a full affine 

\[
\mathbb F_2^4
\]

register, not the 56-component fragmented object seen by a single unglued BT718 sheet.

## Fail-closed rule

A candidate is globally accepted only if all five tests pass:

```text
T1 selected_rows = 2160
T2 rank_mod_1000003 = 81
T3 root_triples_hit = 540
T4 root_hit_distribution = {4: 540}
T5 BT741 global_register_dimension = 4
```

If the BT741 quotient relation is missing, stale, or not linked to the BT753 row identifiers, the verifier must emit:

```text
global_status = "pending_gluing_relation"
accepted_candidates = []
```

This is intentional. Rank-81 local selection is necessary, not sufficient.

## Why this matters

BT741 proved that the `1110` mask bundle has a flat global \(\mathbb F_2^4\) register, while a single BT718 sheet fragments into many components. BT757 is the firewall preventing a locally full-rank phase-duo selector from being mistaken for a globally glued selector.

## Boundary

This artifact is the gluing verifier contract. It does not assert that any of the 24 BT753 candidates has passed T5 until the BT741 quotient is run against the BT753 row IDs and a result JSON is pushed.
