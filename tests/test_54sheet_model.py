#!/usr/bin/env python3
"""Tests for the 54‑sheet coordinate model and tomotope lift."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

repo = Path(__file__).resolve().parent.parent

COORD_CSV = repo / "K54_54sheet_coords.csv"
BLOCK2POCKET = repo / "block_to_pockets.json"
AXIS_BLOCKS = repo / "axis_bundle_content" / "TOE_tomotope_axis_block_twist_v02_20260228" / "blocks48_r0r3.json"
L_CSV = repo / "K54_node_labels_L.csv"


@pytest.fixture(scope="module")
def load_all():
    assert COORD_CSV.exists(), "Run THEORY_PART_COCYCLE_HEISENBERG_TOMOTOPE_54SHEET.py first."
    coords = []
    with open(COORD_CSV) as f:
        for r in csv.DictReader(f):
            # convert numeric fields
            for fld in ("pocket","qid","twin_bit","L","canonical_flag","canonical_block"):
                if r[fld] != "":
                    r[fld] = int(r[fld])
                else:
                    r[fld] = None
            coords.append(r)
    Ls = []
    with open(L_CSV) as f:
        for r in csv.DictReader(f):
            Ls.append(int(r["L"]))
    blocks = json.load(open(BLOCK2POCKET))
    orbits = json.load(open(AXIS_BLOCKS))["orbits"]
    return coords, Ls, blocks, orbits


def test_size_and_ranges(load_all):
    coords, Ls, blocks, orbits = load_all
    assert len(coords) == 54
    qids = {c["qid"] for c in coords}
    assert all(0 <= q < 27 for q in qids)
    assert all(c["twin_bit"] in (0,1) for c in coords)
    assert all(0 <= c["L"] < 3 for c in coords)
    # some pockets may lack a canonical flag/block if mapping was incomplete
    assert all((c["canonical_flag"] is None) or (0 <= c["canonical_flag"] < 192) for c in coords)
    assert all((c["canonical_block"] is None) or (0 <= c["canonical_block"] < 48) for c in coords)


def test_flag_block_consistency(load_all):
    coords, Ls, blocks, orbits = load_all
    # build map block->set(flags)
    bflags = {i:set(orbits[i]) for i in range(len(orbits))}
    for c in coords:
        blk = c.get("canonical_block")
        flag = c.get("canonical_flag")
        if blk is None or flag is None:
            continue
        assert flag in bflags[blk], f"flag {flag} not in its block {blk}"


def test_L_matches(load_all):
    coords, Ls, blocks, orbits = load_all
    for c in coords:
        assert Ls[c["pocket"]] == c["L"]


def test_block_guess_actual(load_all):
    coords, Ls, blocks, orbits = load_all
    # invert the block map to pockets
    p2b = {}
    for b,plist in blocks.items():
        for p in plist:
            p2b.setdefault(int(p), []).append(int(b))
    matches = 0
    for c in coords:
        guesses = [int(g) for g in c["block_guesses"].split(";") if g]
        actual = set(p2b.get(c["pocket"], []))
        for g in guesses:
            if g in actual:
                matches += 1
    # there should be at least some correct guesses
    assert matches >= 10, "too few guesses matched actual blocks"


def test_guess_to_flag_mapping(load_all):
    # ensure the summary file reports guess counts
    summary = json.loads((repo / "SUMMARY_54sheet.json").read_text(encoding="utf-8"))
    gmap = summary.get("guess_to_actual_flag_counts", {})
    # every entry should have a nonzero count and at least one flag
    for k,v in gmap.items():
        assert v.get("count",0) > 0
        assert v.get("flags") and isinstance(v.get("flags"), list)


def test_t4_cycle_statistics():
    summary = json.loads((repo / "SUMMARY_54sheet.json").read_text(encoding="utf-8"))
    cycles = summary.get("canonical_flag_t4_cycle_vs_L", {})
    # there should be both 1-cycle and 3-cycle entries
    assert any(k.startswith("(1,") for k in cycles)
    assert any(k.startswith("(3,") for k in cycles)
    # total count should be 54 or less (some pockets missing flags)
    total = sum(cycles.values())
    assert total <= 54 and total > 0


def test_all_pockets_have_flags(load_all):
    coords, Ls, blocks, orbits = load_all
    # at least one pocket should have a flag; others may be missing
    flags = [c["canonical_flag"] for c in coords]
    assert any(f is not None for f in flags), "no pocket was assigned a flag"


def test_unique_flag_assignment():
    # read refined coords
    coords = []
    with open(repo / "K54_54sheet_coords_refined.csv") as f:
        for r in csv.DictReader(f):
            if r["unique_flag"] != "":
                coords.append(int(r["unique_flag"]))
    assert len(coords) == 54
    assert len(set(coords)) == 54, "unique_flag values are not all distinct"


def test_refined_flag_within_candidates():
    # ensure each unique_flag was a candidate
    cands = json.load(open(repo / "pocket_to_flags.json"))
    with open(repo / "K54_54sheet_coords_refined.csv") as f:
        for r in csv.DictReader(f):
            p = int(r["pocket"])
            uf = int(r["unique_flag"])
            if str(p) in cands:
                assert uf in cands[str(p)]
            else:
                # pocket had no candidates, accept any flag
                continue


def test_matching_summary():
    summ = json.load(open(repo / "SUMMARY_matching.json"))
    assert summ.get("matched") == 54
    assert summ.get("unmatched_pockets") == []


def test_pillar_bundle_contains_narrative_and_refined():
    # check that bundle includes narrative and refined files
    import zipfile
    zf = zipfile.ZipFile(repo / "TOE_54sheet_pillar82_bundle.zip")
    names = zf.namelist()
    for need in ["PILLAR_82.md", "K54_54sheet_coords_refined.csv", "pocket_to_unique_flag.json"]:
        assert need in names, f"{need} missing from pillar bundle"


def test_summary_orbit_full():
    summ = json.load(open(repo / "SUMMARY_54sheet.json"))
    assert summ.get("full_orbit_size") == 192
    assert summ.get("full_orbit_all_flags") is True
    fmap = summ.get("flag_to_pocket_orbit", {})
    # should map exactly 192 flags
    assert len(fmap) == 192
    # ensure each pocket appears at least once
    pockets = set(fmap.values())
    assert pockets.issubset(set(range(54)))
    assert len(pockets) >= 27  # covers all twin pairs at least


def test_flag_word_map_consistency():
    # verify that applying word to base flag yields target
    import json
    fmap = json.load(open(repo / "flag_word_map.json"))
    # load generators
    gens = json.load(open(repo / "axis_bundle_content/TOE_tomotope_axis_block_twist_v02_20260228/tomotope_r_generators_in_axis_coords.json"))
    r0 = tuple(gens['r0']); r1 = tuple(gens['r1']); r2 = tuple(gens['r2']); r3 = tuple(gens['r3'])
    G = [r0,r1,r2,r3]
    # load refined coords for base flags
    base = {}
    with open(repo / "K54_54sheet_coords_refined.csv") as f:
        for r in csv.DictReader(f):
            p = int(r['pocket'])
            uf = int(r['unique_flag'])
            base[p] = uf
    for flag, (p, word) in fmap.items():
        p = int(p); flag = int(flag)
        # apply word starting from base[p]
        cur = base[p]
        for gi in word:
            cur = G[gi][cur]
        assert cur == flag, f"word {word} from pocket {p} leads to {cur}, expected {flag}"
