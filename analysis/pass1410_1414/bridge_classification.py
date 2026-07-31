from __future__ import annotations

import collections
import hashlib
import itertools

import numpy as np

import _selector_five_frontiers_impl as ff
import bt713_selector_sheet_rank_filter as sheet713

from .common import GOOD, capture, rank_mod, sha

MASKS = (
    (1, 1, 1, 0), (1, 1, 0, 1), (1, 0, 1, 1), (0, 1, 1, 1),
    (1, 1, 0, 0), (1, 0, 0, 1), (0, 1, 1, 0), (0, 0, 1, 1),
)


def perfect_matchings4(line):
    a, b, c, d = tuple(line)
    return tuple(sorted([
        tuple(sorted((tuple(sorted((a, b))), tuple(sorted((c, d)))))),
        tuple(sorted((tuple(sorted((a, c))), tuple(sorted((b, d)))))),
        tuple(sorted((tuple(sorted((a, d))), tuple(sorted((b, c)))))),
    ]))


def matching_for_pair(matchings, pair):
    pair = tuple(sorted(pair))
    hits = [i for i, M in enumerate(matchings) if pair in M]
    assert len(hits) == 1
    return hits[0]


def d4_permutations():
    out = set()
    for k in range(4):
        out.add(tuple((i + k) % 4 for i in range(4)))
        out.add(tuple((k - i) % 4 for i in range(4)))
    assert len(out) == 8
    return sorted(out)


def permute_mask(mask, perm):
    return tuple(mask[perm[i]] for i in range(4))


def build_all_sheets():
    adj, lines, through, edge_line, centers, flag_index = sheet713.build()
    line_matchings = [perfect_matchings4(line) for line in lines]
    sheet_rows = {(mask, r): [] for mask in MASKS for r in range(3)}
    rectangles = []
    for c in range(40):
        for li, lj in itertools.combinations(through[c], 2):
            A = tuple(sorted(set(lines[li]) - {c}))
            B = tuple(sorted(set(lines[lj]) - {c}))
            for aa in itertools.combinations(A, 2):
                for bb in itertools.combinations(B, 2):
                    rect_edges = [tuple(sorted(e)) for e in [
                        (aa[0], bb[0]), (aa[1], bb[0]),
                        (aa[1], bb[1]), (aa[0], bb[1]),
                    ]]
                    per_mask = collections.defaultdict(list)
                    for gauges in itertools.product(*(centers[e] for e in rect_edges)):
                        paths = [sheet713.path_edges(x, y, q, edge_line) for (x, y), q in zip(rect_edges, gauges)]
                        cycle = sheet713.xor_path_edges(paths)
                        if sheet713.is_simple_levi_8_cycle(cycle):
                            mask = tuple(1 if q == c else 0 for q in gauges)
                            row = sheet713.oriented_sparse_row(cycle, flag_index)
                            per_mask[mask].append((tuple(sorted(cycle)), row))
                    assert set(per_mask) == set(MASKS)
                    for mask in MASKS:
                        vals = sorted(per_mask[mask], key=lambda t: t[0])
                        assert len(vals) == 3
                        for r, (_cycle, row) in enumerate(vals):
                            sheet_rows[(mask, r)].append(row)
                    mi = matching_for_pair(line_matchings[li], aa)
                    mj = matching_for_pair(line_matchings[lj], bb)
                    edge_i = line_matchings[li][mi].index(tuple(sorted(aa)))
                    edge_j = line_matchings[lj][mj].index(tuple(sorted(bb)))
                    rectangles.append((3 * li + mi, 3 * lj + mj, edge_i, edge_j))
    assert len(rectangles) == 2160
    assert all(len(rows) == 2160 for rows in sheet_rows.values())
    return sheet_rows, rectangles, flag_index


def dense_sheet(rows):
    S = np.zeros((2160, 160), dtype=np.int64)
    for i, row in enumerate(rows):
        for c, v in row:
            S[i, c] = v
    return S


def bridge(S, rectangles, side_char, edge_char):
    B = np.zeros((120, 160), dtype=np.int64)
    for row, (si, sj, ei, ej) in zip(S, rectangles):
        wi = -1 if edge_char and ei else 1
        wj = -1 if side_char else 1
        if edge_char and ej:
            wj *= -1
        B[si] += wi * row
        B[sj] += wj * row
    return B


def analyze():
    _public, cap = capture()
    g = cap["g"]
    sheet_rows, rectangles, flag_index = build_all_sheets()
    Dlevi = ff.levi_boundary(flag_index)
    projectors = []
    for item in sorted(cap["character_projectors"], key=lambda x: x["block_index"]):
        projectors.append((item, ff.orbital_matrix_mod(g, item["projector"], GOOD)))

    d4 = d4_permutations()
    mask_records = {}
    for mask in MASKS:
        orbit = sorted({permute_mask(mask, p) for p in d4})
        stabilizer = sum(permute_mask(mask, p) == mask for p in d4)
        mask_records["".join(map(str, mask))] = {
            "d4_orbit": ["".join(map(str, x)) for x in orbit],
            "d4_orbit_size": len(orbit),
            "d4_stabilizer_order": stabilizer,
            "weight": sum(mask),
        }

    reference = dense_sheet(sheet_rows[((1, 1, 1, 0), 0)])
    assert rank_mod(reference) == 81
    sheets = []
    bridges = []
    class_counter = collections.Counter()
    sheet_rank_counter = collections.Counter()
    bridge_rank_counter = collections.Counter()

    for mask in MASKS:
        for residual in range(3):
            S = dense_sheet(sheet_rows[(mask, residual)])
            srank = rank_mod(S)
            boundaryless = not np.any(Dlevi @ S.T)
            assert boundaryless
            same_e4 = srank == 81 and rank_mod(np.vstack([reference, S])) == 81
            sheet_rank_counter[srank] += 1
            sheet_key = f"{''.join(map(str, mask))}_r{residual}"
            sheet_bridges = []
            for side_char, edge_char in itertools.product((0, 1), repeat=2):
                B = bridge(S, rectangles, side_char, edge_char)
                brank = rank_mod(B)
                assert not np.any(Dlevi @ B.T)
                sector_ranks = []
                for item, P in projectors:
                    PB = P @ (B % GOOD) % GOOD
                    sector_ranks.append(rank_mod(PB))
                rec = {
                    "sheet": sheet_key,
                    "mask": "".join(map(str, mask)),
                    "residual": residual,
                    "side_character": side_char,
                    "edge_character": edge_char,
                    "sheet_rank": srank,
                    "bridge_rank": brank,
                    "boundaryless": True,
                    "same_steinberg_rowspace": same_e4,
                    "mackey_sector_ranks": sector_ranks,
                    "nonzero": int(np.count_nonzero(B)),
                    "max_abs_entry": int(np.max(np.abs(B))),
                    "sha256": hashlib.sha256(B.astype(np.int64).tobytes()).hexdigest(),
                }
                bridges.append(rec)
                sheet_bridges.append(rec["sha256"])
                bridge_rank_counter[brank] += 1
                class_counter[(srank, brank, tuple(sector_ranks), rec["nonzero"], rec["max_abs_entry"])] += 1
            sheets.append({
                "sheet": sheet_key,
                "mask": "".join(map(str, mask)),
                "residual": residual,
                "rank": srank,
                "boundaryless": True,
                "same_steinberg_rowspace": same_e4,
                "bridge_hashes": sheet_bridges,
            })

    classes = []
    for key, count in sorted(class_counter.items(), key=lambda x: str(x[0])):
        srank, brank, sector_ranks, nonzero, max_abs = key
        classes.append({
            "sheet_rank": srank,
            "bridge_rank": brank,
            "mackey_sector_ranks": list(sector_ranks),
            "nonzero": nonzero,
            "max_abs_entry": max_abs,
            "count": count,
        })

    result = {
        "theorem": "Pass 1412 Complete Rank-81 Apartment-Bridge Classification",
        "family_size": 96,
        "sheet_count": 24,
        "sign_characters_per_sheet": 4,
        "mask_d4_data": mask_records,
        "sheet_rank_distribution": {str(k): v for k, v in sorted(sheet_rank_counter.items())},
        "bridge_rank_distribution": {str(k): v for k, v in sorted(bridge_rank_counter.items())},
        "rank81_sheet_count": sum(x["rank"] == 81 for x in sheets),
        "rank81_bridge_count": sum(x["bridge_rank"] == 81 for x in bridges),
        "all_rank81_sheets_equal_full_levi_cycle_space": all(x["same_steinberg_rowspace"] for x in sheets if x["rank"] == 81),
        "classification_classes": classes,
        "sheets": sheets,
        "bridges": bridges,
        "conclusion": "All eight masks, three residual coordinates, and four side/edge sign characters are exhausted. Every full-rank sheet is identified objectwise with the same Levi Steinberg-81 row space; bridge ranks and all fourteen Mackey source ranks are frozen for every gauge.",
        "boundary": "D4 acts intrinsically on the four mask positions. Residual labels are the deterministic cycle ordering from the exact lift enumerator; no unverified S3 action on those labels is asserted.",
    }
    result["sha256"] = sha(result)
    return result
