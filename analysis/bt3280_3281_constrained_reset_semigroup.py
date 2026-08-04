#!/usr/bin/env python3
"""Passes 3280-3281: constrained epistemic-reset semigroup.

The exact 876-state Moore quotient has three typed terminal witnesses: none,
flat and curved.  Admissible phase locks, route-only operations and fail-closed
sensing/outcome transformations preserve each terminal individually.  Hence
all unauthorized words fix three distinct states and have transformation rank
at least three.  A separately authorized proof-root reset is rank one.
"""
from __future__ import annotations

import importlib.util
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3280_BT3281_CONSTRAINED_RESET_SEMIGROUP_results.json"
SRC = ROOT / "analysis" / "bt3276_3277_independent_curvature_quotient.py"


def load_verifier():
    spec = importlib.util.spec_from_file_location("bt3276_independent", SRC)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def compose_image(image, transform):
    return frozenset(transform[x] for x in image)


def main():
    m = load_verifier()
    rows = m.universe()
    full = m.np.array([m.syndrome(r) for r in rows], dtype=m.np.uint8)
    grouped = defaultdict(list)
    for i,key in enumerate(map(tuple,full[:,m.SELECTED])): grouped[key].append(i)
    initial = [tuple(v) for v in grouped.values() if len(v)>1]
    labels = m.curvature(rows)
    records = m.raw_machine(initial, full, labels, reverse=False)
    classes, signatures, rounds = m.refine(records)
    q = len(set(classes.values()))
    assert q == 876

    # One representative per quotient class.
    reps = {}
    for state,cid in classes.items(): reps.setdefault(cid,state)
    terminal = {}
    for cid,state in reps.items():
        is_terminal,action,output,children = records[state]
        if is_terminal: terminal[output] = cid
    expected = {(1,0,0),(0,1,0),(0,0,1)}
    assert set(terminal) == expected and len(set(terminal.values())) == 3
    fixed = tuple(sorted(terminal.values()))

    # Fail-closed deterministic sensing maps: apply one action/outcome only where
    # it is valid; otherwise leave the belief state unchanged.
    action_outcomes = set()
    for cid,state in reps.items():
        is_terminal,action,output,children = records[state]
        if not is_terminal:
            action_outcomes.update((action,o) for o in children)
    transforms = []
    for action,outcome in sorted(action_outcomes):
        t = list(range(q))
        for cid,state in reps.items():
            is_terminal,a,output,children = records[state]
            if not is_terminal and a == action and outcome in children:
                t[cid] = classes[children[outcome]]
        assert all(t[x] == x for x in fixed)
        transforms.append(((action,outcome),tuple(t)))

    # Route-only and phase-lock maps act outside belief or as belief permutations;
    # the identity is their conservative belief projection.
    identity = tuple(range(q))
    assert all(identity[x] == x for x in fixed)

    one_step = sorted((len(set(t)),key) for key,t in transforms)
    greedy_image = frozenset(range(q))
    greedy_trace = []
    for depth in range(1,9):
        best = min((len(compose_image(greedy_image,t)),key,t) for key,t in transforms)
        greedy_image = compose_image(greedy_image,best[2])
        greedy_trace.append({"depth":depth,"action_outcome":list(best[1]),"image_rank":len(greedy_image)})
        assert set(fixed).issubset(greedy_image)

    # Authorized reset: proof-root gate may identify all beliefs with one chosen
    # safe terminal.  Empty word has rank 876, so the shortest authorized rank-one
    # word has length exactly one.
    safe = terminal[(1,0,0)]
    authorized_reset = tuple(safe for _ in range(q))
    assert len(set(authorized_reset)) == 1

    payload = {
        "schema":"w33.pass3280_3281.constrained_reset_semigroup.v1",
        "status":"EXACT_GLOBAL_RANK_FLOOR_AND_AUTHORIZED_RESET",
        "quotient_states":q,
        "refinement_rounds":rounds,
        "terminal_witnesses":{
            "none":terminal[(1,0,0)],
            "flat":terminal[(0,1,0)],
            "curved":terminal[(0,0,1)],
        },
        "unauthorized_generators":{
            "distinct_sensing_outcome_maps":len(transforms),
            "phase_lock_belief_projection":"identity",
            "route_only_belief_projection":"typed permutation preserving all three terminals",
            "minimum_one_step_rank":one_step[0][0],
        },
        "global_unauthorized_rank_floor":3,
        "rank_floor_proof":"Every generator fixes the three distinct typed terminal witnesses pointwise. This property is closed under composition, so every unauthorized word has image rank at least three at every length.",
        "greedy_nonproof_trace":greedy_trace,
        "authorized_reset":{"rank":1,"shortest_word_length":1,"target":"none terminal","requirements":["reset authorization","matching proof root"]},
        "boundary":"The rank-three floor is exact for the explicitly defined fail-closed sensing/phase/route alphabet. It does not cover destructive hardware operations outside that contract, and the greedy trace is not a shortest-word proof.",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"states":q,"generators":len(transforms),"rank_floor":3,"authorized_length":1},sort_keys=True))


if __name__ == "__main__": main()
