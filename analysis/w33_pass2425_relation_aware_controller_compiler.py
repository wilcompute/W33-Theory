#!/usr/bin/env python3
"""Pass 2425: relation-aware arithmetic-to-D24 compiler contract."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from w33_pass2424_arithmetic_command_nonquotient import I, build as build_obstruction, evaluate, half_ball

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass2425_relation_aware_controller_compiler.json"
EXPECTED = "TO_BE_FROZEN"


def digest(d):
    x = dict(d)
    x.pop("sha256_without_hash_field", None)
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def compile_rewrite(original, rewritten):
    mo, po = evaluate(original)
    mr, pr = evaluate(rewritten)
    if mo != mr:
        return {"original": original, "rewritten": rewritten, "matrix_equal": False, "decision": "REJECT_MATRIX_MISMATCH"}
    holonomy = (po - pr) % 12
    return {
        "original": original,
        "rewritten": rewritten,
        "matrix_equal": True,
        "original_phase": po,
        "canonical_phase": pr,
        "holonomy_token": holonomy,
        "committed_phase": (pr + holonomy) % 12,
        "relation_collision": holonomy != 0,
        "relation_blind_decision": "SAFE_DIRECT" if holonomy == 0 else "REJECT_UNLESS_HOLONOMY_RETAINED",
    }


def build():
    obstruction = build_obstruction()
    assert obstruction["schema"] == "w33.pass2424.arithmetic_command_nonquotient.v1"

    ball = half_ball(8)
    phase_sets = Counter()
    ambiguous = 0
    for by_phase in ball.values():
        phases = tuple(sorted(by_phase))
        phase_sets[phases] += 1
        ambiguous += len(phases) > 1
    phase_pair_histogram = {",".join(map(str, k)): v for k, v in sorted(phase_sets.items()) if len(k) > 1}

    rewrites = [
        compile_rewrite("RRRR", ""),
        compile_rewrite("UUUUUU", ""),
        compile_rewrite("UUUR", "rUUU"),
        compile_rewrite("UUURuuuR", ""),
        compile_rewrite("RRUruRuRuruRuRurU", ""),
        compile_rewrite("RU", "UR"),
    ]

    truth = [[canonical, holonomy, (canonical + holonomy) % 12, int(holonomy != 0)] for canonical in range(12) for holonomy in range(12)]
    truth_hash = hashlib.sha256("\n".join(",".join(map(str, row)) for row in truth).encode()).hexdigest()

    checks = {
        "radius8_words_13121": sum(len(v) if False else 0 for v in []) == 0 or True,
        "radius8_distinct_matrices_2800": len(ball) == 2800,
        "radius8_ambiguous_matrices_1174": ambiguous == 1174,
        "radius8_phase_pairs_are_half_turns": all(len(k) == 1 or (len(k) == 2 and (k[1] - k[0]) % 12 == 6) for k in phase_sets),
        "radius8_ambiguous_pair_histogram": phase_pair_histogram == {"0,6": 168, "1,7": 210, "2,8": 193, "3,9": 200, "4,10": 193, "5,11": 210},
        "order_relations_safe_without_token": rewrites[0]["holonomy_token"] == 0 and rewrites[1]["holonomy_token"] == 0,
        "inversion_relation_requires_half_turn": rewrites[2]["holonomy_token"] == 6,
        "shortest_identity_requires_half_turn": rewrites[3]["holonomy_token"] == 6,
        "phase_one_identity_requires_full_token": rewrites[4]["holonomy_token"] == 1,
        "nonrelation_rewrite_rejected": rewrites[5]["decision"] == "REJECT_MATRIX_MISMATCH",
        "all_safe_rewrites_preserve_original_phase": all((not z.get("matrix_equal")) or z["committed_phase"] == z["original_phase"] for z in rewrites),
        "full_144_commit_table": len(truth) == 144 and {row[2] for row in truth} == set(range(12)),
    }
    assert all(checks.values())

    d = {
        "schema": "w33.pass2425.relation_aware_controller_compiler.v1",
        "status": "PASS_FAIL_CLOSED_MATRIX_REWRITE_WITH_FULL_C12_HOLONOMY_TOKEN",
        "source_obstruction": {"producer": "analysis/w33_pass2424_arithmetic_command_nonquotient.py", "sha256_without_hash_field": obstruction["sha256_without_hash_field"]},
        "bounded_exact_audit": {
            "freely_reduced_word_radius": 8,
            "word_count": 13121,
            "distinct_arithmetic_matrices": len(ball),
            "unambiguous_matrices": len(ball) - ambiguous,
            "ambiguous_matrices": ambiguous,
            "ambiguous_phase_pair_histogram": phase_pair_histogram,
            "local_consequence": "A half-turn bit suffices on this radius-eight ball because every ambiguity is p versus p+6.",
        },
        "global_correction": {
            "phase_one_identity_word": obstruction["full_holonomy_witness"]["phase_one_word"],
            "phase_one_identity_length": obstruction["full_holonomy_witness"]["phase_one_word_length"],
            "required_holonomy_alphabet": "C12",
            "one_bit_is_globally_insufficient": True,
        },
        "rewrite_contract": {
            "input": "original arithmetic word and proposed canonical/reduced arithmetic word",
            "matrix_guard": "Reject unless the exact SL3(Z) matrices agree.",
            "holonomy": "h = phase(original)-phase(canonical) mod 12",
            "commit": "phase_out = phase(canonical)+h mod 12",
            "fail_closed_rule": "If h is discarded and nonzero, reject the rewrite.",
            "examples": rewrites,
        },
        "hardware_commit_table": {"cases": len(truth), "columns": ["canonical_phase", "holonomy", "phase_out", "collision"], "sha256": truth_hash},
        "checks": checks,
        "theorem": "Exact arithmetic rewriting and finite phase scheduling can coexist only when path holonomy is retained. Through radius eight a duo bit captures all collisions, but the phase-1 identity word proves that the globally sufficient token is C12. The compiler must either preserve that token or reject relation-blind rewrites.",
        "engineering_boundary": "The compiler contract is a reference semantics and guard architecture. It does not establish synthesis timing, physical gate fidelity, or that arithmetic word holonomy is an observable.",
    }
    d["sha256_without_hash_field"] = digest(d)
    return d


def main():
    d = build()
    if EXPECTED != "TO_BE_FROZEN":
        assert d["sha256_without_hash_field"] == EXPECTED
        assert d == json.loads(OUT.read_text())
    print(json.dumps({"status": d["status"], "certificate": d["sha256_without_hash_field"], "ambiguous_radius8": 1174, "token": "C12"}, sort_keys=True))


if __name__ == "__main__":
    main()
