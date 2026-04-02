"""Exact l6 gauge-return split constrained by the W(3,3) exceptional dictionary.

The corrected V24 l6 table is the first higher-tower level that returns to the
gauge block. This module packages the exact split that matters for the next
step in the quark/gauge program.

What is established:
  - corrected l6 has total support 86 = 72 E6 roots + 6 A2 roots + 8 Cartan;
  - the dominant democratic input pattern (0,0,1,1,2,2) lands only in
    generation-preserving E6 roots plus Cartan;
  - the six smaller asymmetric generation patterns land only in the six A2
    roots, i.e. the generation-mixing part of g0;
  - on the full 81 matter states the supported l6 gauge operators have ranks
    72 + 6 + 8 = 86, while on the spinor 48 they compress to 40 + 6 + 8 = 54.

What is not claimed:
  - a completed quark Yukawa solution;
  - that l6 by itself closes the quark residual;
  - the missing 4D refinement/scaling theorem.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
EXPLORATION_DIR = Path(__file__).resolve().parent
if str(EXPLORATION_DIR) not in sys.path:
    sys.path.insert(0, str(EXPLORATION_DIR))

from exploration._artifact_paths import resolve_repo_data_path
from w33_fermionic_connes_sector import canonical_spinor_basis


L6_PATH = resolve_repo_data_path(
    ROOT, Path("V24_output_v13_full") / "l6_patch_sextuples_full.jsonl"
)
META_PATH = resolve_repo_data_path(
    ROOT,
    Path("extracted_v13")
    / "W33-Theory-master"
    / "artifacts"
    / "e8_root_metadata_table.json",
)
SC_PATH = resolve_repo_data_path(
    ROOT, Path("artifacts") / "e8_structure_constants_w33_discrete.json"
)


@dataclass(frozen=True)
class L6GenerationPatternSummary:
    """Exact output-kind split for one corrected l6 generation pattern."""

    pattern: tuple[int, int, int, int, int, int]
    entry_count: int
    e6_term_count: int
    a2_term_count: int
    cartan_term_count: int


@dataclass(frozen=True)
class L6ExceptionalGaugeReturnCertificate:
    """Packaged exact corrected-l6 gauge-return theorem."""

    total_entry_count: int
    single_entry_count: int
    multi_entry_count: int
    full_support_size: int
    e6_root_support_size: int
    a2_root_support_size: int
    cartan_support_size: int
    democratic_pattern: tuple[int, int, int, int, int, int]
    democratic_summary: L6GenerationPatternSummary
    asymmetric_summaries: tuple[L6GenerationPatternSummary, ...]
    e6_uniform_term_count: int
    a2_uniform_term_count: int
    sorted_cartan_term_counts: tuple[int, ...]
    e6_generation_preserving: bool
    a2_generation_mixing_only: bool
    cartan_generation_preserving: bool
    full_matter_action_ranks: tuple[int, int, int]
    spinor_action_ranks: tuple[int, int, int]
    full_matter_total_rank: int
    spinor_total_rank: int
    route_interpretation: str


def _sorted_counter_items(counter: Counter) -> tuple[tuple[int, int], ...]:
    return tuple(sorted((int(k), int(v)) for k, v in counter.items()))


@lru_cache(maxsize=1)
def _structure_data() -> dict[str, object]:
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    sc = json.loads(SC_PATH.read_text(encoding="utf-8"))
    cartan_dim = int(sc["basis"]["cartan_dim"])
    sc_roots = [tuple(root) for root in sc["basis"]["roots"]]
    row_by_orbit = {tuple(row["root_orbit"]): row for row in meta["rows"]}

    idx_grade = {ci: "cartan" for ci in range(cartan_dim)}
    idx_i3 = {ci: None for ci in range(cartan_dim)}
    idx_i27 = {ci: None for ci in range(cartan_dim)}
    out_kind = {ci: "cartan" for ci in range(cartan_dim)}
    sc_by_generation_source = {}

    for root_index, orbit in enumerate(sc_roots):
        sc_idx = cartan_dim + root_index
        row = row_by_orbit[orbit]
        idx_grade[sc_idx] = row["grade"]
        idx_i3[sc_idx] = row.get("i3")
        idx_i27[sc_idx] = row.get("i27")
        if row["grade"] == "g1":
            sc_by_generation_source[(row["i3"], row["i27"])] = sc_idx
        elif row["grade"] == "g0":
            out_kind[sc_idx] = (
                "e6" if tuple(row.get("su3_weight", [])) == (0, 0) else "a2"
            )
        else:
            out_kind[sc_idx] = row["grade"]

    bracket = {}
    for key, terms in sc["brackets"].items():
        left, right = (int(value) for value in key.split(","))
        bracket[(left, right)] = tuple((int(out), int(coeff)) for out, coeff in terms)

    return {
        "cartan_dim": cartan_dim,
        "idx_grade": idx_grade,
        "idx_i3": idx_i3,
        "idx_i27": idx_i27,
        "out_kind": out_kind,
        "sc_by_generation_source": sc_by_generation_source,
        "bracket": bracket,
    }


def _bracket(i: int, j: int) -> tuple[tuple[int, int], ...]:
    bracket = _structure_data()["bracket"]
    if i == j:
        return ()
    if i < j:
        key = (i, j)
        sign = 1
    else:
        key = (j, i)
        sign = -1
    return tuple((out, sign * coeff) for out, coeff in bracket.get(key, ()))


@lru_cache(maxsize=1)
def _l6_scan() -> dict[str, object]:
    idx_i3 = _structure_data()["idx_i3"]
    out_kind = _structure_data()["out_kind"]

    total_entries = 0
    single_entries = 0
    multi_entries = 0
    pattern_entry_counter: Counter = Counter()
    pattern_term_kind_counter: dict[
        tuple[int, int, int, int, int, int], Counter
    ] = defaultdict(Counter)
    output_term_counter: Counter = Counter()

    with L6_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            total_entries += 1
            pattern = tuple(sorted(idx_i3[idx] for idx in record["in"]))
            pattern_entry_counter[pattern] += 1
            if "out" in record:
                single_entries += 1
                out = int(record["out"])
                output_term_counter[out] += 1
                pattern_term_kind_counter[pattern][out_kind[out]] += 1
            else:
                multi_entries += 1
                for out, coeff in record["terms"]:
                    out_idx = int(out)
                    output_term_counter[out_idx] += 1
                    pattern_term_kind_counter[pattern][out_kind[out_idx]] += 1

    support_outputs = tuple(sorted(output_term_counter))
    e6_support = tuple(out for out in support_outputs if out_kind[out] == "e6")
    a2_support = tuple(out for out in support_outputs if out_kind[out] == "a2")
    cartan_support = tuple(out for out in support_outputs if out_kind[out] == "cartan")

    return {
        "total_entries": total_entries,
        "single_entries": single_entries,
        "multi_entries": multi_entries,
        "pattern_entry_counter": pattern_entry_counter,
        "pattern_term_kind_counter": pattern_term_kind_counter,
        "output_term_counter": output_term_counter,
        "support_outputs": support_outputs,
        "e6_support": e6_support,
        "a2_support": a2_support,
        "cartan_support": cartan_support,
    }


def _state_sc_indices_full_matter() -> tuple[int, ...]:
    sc_by_generation_source = _structure_data()["sc_by_generation_source"]
    return tuple(
        sc_by_generation_source[(generation, source_i27)]
        for generation in range(3)
        for source_i27 in range(27)
    )


def _state_sc_indices_spinor() -> tuple[int, ...]:
    sc_by_generation_source = _structure_data()["sc_by_generation_source"]
    return tuple(
        sc_by_generation_source[(generation, state.source_i27)]
        for generation in range(3)
        for state in canonical_spinor_basis()
    )


def _action_rank_and_generation_split(
    support_indices: tuple[int, ...],
    state_sc_indices: tuple[int, ...],
) -> tuple[int, int, int]:
    idx_grade = _structure_data()["idx_grade"]
    idx_i3 = _structure_data()["idx_i3"]
    sc_to_position = {sc_idx: pos for pos, sc_idx in enumerate(state_sc_indices)}
    columns = []
    same_generation = 0
    cross_generation = 0

    for output_idx in support_indices:
        matrix = np.zeros((len(state_sc_indices), len(state_sc_indices)), dtype=float)
        for source_idx, source_position in sc_to_position.items():
            source_generation = idx_i3[source_idx]
            for target_idx, coeff in _bracket(output_idx, source_idx):
                if idx_grade.get(target_idx) != "g1":
                    continue
                target_position = sc_to_position.get(target_idx)
                if target_position is None:
                    continue
                matrix[target_position, source_position] += coeff
                if idx_i3[target_idx] == source_generation:
                    same_generation += 1
                else:
                    cross_generation += 1
        columns.append(matrix.reshape(-1))

    rank = int(np.linalg.matrix_rank(np.stack(columns, axis=1)))
    return rank, same_generation, cross_generation


@lru_cache(maxsize=1)
def build_l6_exceptional_gauge_return_certificate() -> L6ExceptionalGaugeReturnCertificate:
    scan = _l6_scan()
    output_term_counter = scan["output_term_counter"]
    pattern_entry_counter = scan["pattern_entry_counter"]
    pattern_term_kind_counter = scan["pattern_term_kind_counter"]

    pattern_summaries = []
    for pattern, entry_count in sorted(
        pattern_entry_counter.items(), key=lambda item: (-item[1], item[0])
    ):
        kind_counter = pattern_term_kind_counter[pattern]
        pattern_summaries.append(
            L6GenerationPatternSummary(
                pattern=pattern,
                entry_count=int(entry_count),
                e6_term_count=int(kind_counter.get("e6", 0)),
                a2_term_count=int(kind_counter.get("a2", 0)),
                cartan_term_count=int(kind_counter.get("cartan", 0)),
            )
        )

    democratic_summary = pattern_summaries[0]
    asymmetric_summaries = tuple(pattern_summaries[1:])

    e6_uniform_counts = {
        int(output_term_counter[out]) for out in scan["e6_support"]
    }
    a2_uniform_counts = {
        int(output_term_counter[out]) for out in scan["a2_support"]
    }
    sorted_cartan_term_counts = tuple(
        sorted(int(output_term_counter[out]) for out in scan["cartan_support"])
    )

    full_e6_rank, full_e6_same, full_e6_cross = _action_rank_and_generation_split(
        scan["e6_support"], _state_sc_indices_full_matter()
    )
    full_a2_rank, full_a2_same, full_a2_cross = _action_rank_and_generation_split(
        scan["a2_support"], _state_sc_indices_full_matter()
    )
    full_cartan_rank, full_cartan_same, full_cartan_cross = _action_rank_and_generation_split(
        scan["cartan_support"], _state_sc_indices_full_matter()
    )

    spinor_e6_rank, _, _ = _action_rank_and_generation_split(
        scan["e6_support"], _state_sc_indices_spinor()
    )
    spinor_a2_rank, _, _ = _action_rank_and_generation_split(
        scan["a2_support"], _state_sc_indices_spinor()
    )
    spinor_cartan_rank, _, _ = _action_rank_and_generation_split(
        scan["cartan_support"], _state_sc_indices_spinor()
    )

    route = (
        "Treat corrected l6 as the first exact gauge-return rung. The dominant "
        "democratic sextuple sector (0,0,1,1,2,2) lands only in "
        "generation-preserving E6 roots plus Cartan, while the six smaller "
        "asymmetric sextuple sectors land only in the six A2 roots, i.e. the "
        "generation-mixing part of g0."
    )

    return L6ExceptionalGaugeReturnCertificate(
        total_entry_count=int(scan["total_entries"]),
        single_entry_count=int(scan["single_entries"]),
        multi_entry_count=int(scan["multi_entries"]),
        full_support_size=len(scan["support_outputs"]),
        e6_root_support_size=len(scan["e6_support"]),
        a2_root_support_size=len(scan["a2_support"]),
        cartan_support_size=len(scan["cartan_support"]),
        democratic_pattern=democratic_summary.pattern,
        democratic_summary=democratic_summary,
        asymmetric_summaries=asymmetric_summaries,
        e6_uniform_term_count=next(iter(e6_uniform_counts)),
        a2_uniform_term_count=next(iter(a2_uniform_counts)),
        sorted_cartan_term_counts=sorted_cartan_term_counts,
        e6_generation_preserving=full_e6_cross == 0 and full_e6_same > 0,
        a2_generation_mixing_only=full_a2_same == 0 and full_a2_cross > 0,
        cartan_generation_preserving=full_cartan_cross == 0 and full_cartan_same > 0,
        full_matter_action_ranks=(full_e6_rank, full_a2_rank, full_cartan_rank),
        spinor_action_ranks=(spinor_e6_rank, spinor_a2_rank, spinor_cartan_rank),
        full_matter_total_rank=full_e6_rank + full_a2_rank + full_cartan_rank,
        spinor_total_rank=spinor_e6_rank + spinor_a2_rank + spinor_cartan_rank,
        route_interpretation=route,
    )
