#!/usr/bin/env python3
"""Representation-theoretic bridge for the W(3,3) theory stack.

This script isolates a structural seam that is stronger than the current
formula-by-formula narrative:

1. The 40-point permutation module of Aut(W33) decomposes canonically.
2. The point-line incidence operator kills the 15-dimensional sector exactly.
3. The oriented chain complex carries a unique 81-dimensional H_1 sector.

The GAP computations are driven from the actual W33 generators already present
in the repo, so this stays tied to the implemented geometry rather than a
hand-entered character table.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_finite_spectral_triple import canonical_generation_basis
from tools.analyze_balanced_orbit_stabilizer import (
    build_w33,
    get_generators,
    matrix_to_vertex_perm,
)


def build_lines_and_triangles(adjacency: np.ndarray) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    n = adjacency.shape[0]
    lines = [
        cell
        for cell in combinations(range(n), 4)
        if all(adjacency[i, j] for i, j in combinations(cell, 2))
    ]
    triangles = [
        (i, j, k)
        for i in range(n)
        for j in range(i + 1, n)
        for k in range(j + 1, n)
        if adjacency[i, j] and adjacency[i, k] and adjacency[j, k]
    ]
    return lines, triangles


def incidence_report(adjacency: np.ndarray, lines: list[tuple[int, ...]]) -> dict[str, object]:
    n = adjacency.shape[0]
    incidence = np.zeros((n, len(lines)), dtype=int)
    for column, line in enumerate(lines):
        for vertex in line:
            incidence[vertex, column] = 1

    bbt = incidence @ incidence.T
    singular_values = np.linalg.svd(incidence.astype(float), compute_uv=False)
    singular_hist = Counter(round(float(value), 10) for value in singular_values)

    eigenvalues, eigenvectors = np.linalg.eigh(adjacency.astype(float))
    eigenspaces: dict[int, list[int]] = {}
    for idx, value in enumerate(eigenvalues):
        eigenspaces.setdefault(int(round(float(value))), []).append(idx)

    image_norms: dict[int, list[float]] = {}
    for eigenvalue, indices in eigenspaces.items():
        subspace = eigenvectors[:, indices]
        norms = np.linalg.norm(incidence.T @ subspace, axis=0)
        image_norms[eigenvalue] = sorted({round(float(x), 8) for x in norms})

    return {
        "num_lines": len(lines),
        "point_degree_hist": sorted(set(incidence.sum(axis=1).tolist())),
        "line_size_hist": sorted(set(incidence.sum(axis=0).tolist())),
        "bbt_equals_a_plus_4i": bool(
            np.array_equal(bbt, adjacency + 4 * np.eye(n, dtype=int))
        ),
        "rank": int(np.linalg.matrix_rank(incidence.astype(float))),
        "singular_values": {str(k): v for k, v in sorted(singular_hist.items())},
        "image_norms_by_adjacency_eigenvalue": {
            str(k): v for k, v in sorted(image_norms.items())
        },
    }


def projector_report(adjacency: np.ndarray) -> dict[str, object]:
    n = adjacency.shape[0]
    identity = np.eye(n, dtype=float)
    all_ones = np.ones((n, n), dtype=float)
    trivial = all_ones / n
    visible_24 = (adjacency.astype(float) + 4.0 * identity) / 6.0 - all_ones / 15.0
    dark_15 = identity - trivial - visible_24

    def max_abs(matrix: np.ndarray) -> float:
        return float(np.max(np.abs(matrix)))

    return {
        "P1_formula": "J/40",
        "P24_formula": "(A + 4I)/6 - J/15",
        "P15_formula": "I - J/40 - P24",
        "P1_rank": int(np.linalg.matrix_rank(trivial)),
        "P24_rank": int(np.linalg.matrix_rank(visible_24)),
        "P15_rank": int(np.linalg.matrix_rank(dark_15)),
        "idempotent_error": {
            "P1": round(max_abs(trivial @ trivial - trivial), 12),
            "P24": round(max_abs(visible_24 @ visible_24 - visible_24), 12),
            "P15": round(max_abs(dark_15 @ dark_15 - dark_15), 12),
        },
        "orthogonality_error": round(
            max(
                max_abs(trivial @ visible_24),
                max_abs(trivial @ dark_15),
                max_abs(visible_24 @ dark_15),
            ),
            12,
        ),
    }


def _gap_perm(perm: list[int]) -> str:
    return "PermList([" + ",".join(str(value + 1) for value in perm) + "])"


def _gap_cells(cells: list[tuple[int, ...]]) -> str:
    return "[" + ",".join("[" + ",".join(str(v + 1) for v in cell) + "]" for cell in cells) + "]"


def _run_gap(script: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".g", delete=False) as handle:
        handle.write("SizeScreen([24, 1000000]);;\n")
        handle.write(script)
        temp_path = Path(handle.name)

    try:
        run = subprocess.run(
            ["gap", "-q", str(temp_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return run.stdout
    finally:
        temp_path.unlink(missing_ok=True)


def _parse_orbit_encoding(value: str) -> list[list[int]]:
    value = value.replace("\\\n", "").replace("\n", "").replace("\\", "")
    return [
        [int(part) for part in orbit.split(",")]
        for orbit in value.split(";")
        if orbit
    ]


def _parse_gap_payload(stdout: str) -> dict[str, object]:
    stdout = stdout.replace("\\\n", "")
    payload: dict[str, object] = {}
    for line in stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            continue
        if value.isdigit():
            payload[key] = int(value)
            continue
        if value in {"true", "false"}:
            payload[key] = value == "true"
            continue
        if re.fullmatch(r"\d+,\d+,\d+(;\d+,\d+,\d+)*", value):
            payload[key] = [
                [int(part) for part in chunk.split(",")]
                for chunk in value.split(";")
            ]
            continue
        try:
            payload[key] = ast.literal_eval(value)
        except Exception:
            payload[key] = value
    return payload


def fetch_local_opposite_orbits(
    point_generators: list[list[int]],
    neighbors: list[int],
    opposite: list[int],
) -> list[list[int]]:
    gap_script = "\n".join(
        [
            "gens := [" + ",".join(_gap_perm(g) for g in point_generators) + "];;",
            "G := Group(gens);;",
            "H := Stabilizer(G, 1);;",
            "nbrs := [" + ",".join(str(n + 1) for n in neighbors) + "];;",
            "opp := [" + ",".join(str(v + 1) for v in opposite) + "];;",
            "actN := ActionHomomorphism(H, nbrs);;",
            "K := KernelOfMultiplicativeGeneralMapping(actN);;",
            "orbs9 := List(Orbits(K, opp), Set);;",
            "EncodeOrbits := orbs -> JoinStringsWithSeparator("
            "List(orbs, O -> JoinStringsWithSeparator(List(O, String), \",\")), "
            "\";\""
            ");;",
            'Print("orbs9=", EncodeOrbits(orbs9), "\\n");',
        ]
    )
    stdout = _run_gap(gap_script)
    if "orbs9=" in stdout:
        return _parse_orbit_encoding(stdout.split("orbs9=", 1)[1].strip())
    raise RuntimeError("Failed to recover local opposite-point orbits")


def oriented_module_report(
    point_generators: list[list[int]],
    edges: list[tuple[int, int]],
    triangles: list[tuple[int, int, int]],
    tetrahedra: list[tuple[int, int, int, int]],
) -> dict[str, object]:
    gap_script = "\n".join(
        [
            "gens := [" + ",".join(_gap_perm(g) for g in point_generators) + "];;",
            "G := Group(gens);;",
            'Print("size=", Size(G), "\\n");',
            "tbl := CharacterTable(G);;",
            "cls := ConjugacyClasses(G);;",
            "reps := List(cls, Representative);;",
            "edges := " + _gap_cells(edges) + ";;",
            "tris := " + _gap_cells(triangles) + ";;",
            "tets := " + _gap_cells(tetrahedra) + ";;",
            "SignOfImage := function(c, g)\n"
            "  local img, pos;\n"
            "  img := List(c, x -> x^g);\n"
            "  if Set(img) <> c then return fail; fi;\n"
            "  pos := List(img, x -> Position(c, x));\n"
            "  return SignPerm(PermList(pos));\n"
            "end;;",
            "CharOnCells := function(cells, reps)\n"
            "  return List(reps, function(g)\n"
            "    return Sum(cells, function(c)\n"
            "      local s;\n"
            "      s := SignOfImage(c, g);\n"
            "      if s = fail then\n"
            "        return 0;\n"
            "      else\n"
            "        return s;\n"
            "      fi;\n"
            "    end);\n"
            "  end);\n"
            "end;;",
            "vals0 := List(reps, g -> Number([1..40], i -> i^g = i));;",
            "vals1 := CharOnCells(edges, reps);;",
            "vals2 := CharOnCells(tris, reps);;",
            "vals3 := CharOnCells(tets, reps);;",
            "char0 := Character(tbl, vals0);;",
            "char1 := Character(tbl, vals1);;",
            "char2 := Character(tbl, vals2);;",
            "char3 := Character(tbl, vals3);;",
            "h0 := TrivialCharacter(tbl);;",
            "h1 := h0 - char0 + char1 - char2 + char3;;",
            "degs := List(Irr(tbl), chi -> chi[1]);;",
            "Pretty := dec -> Filtered(List([1..Length(dec)], i -> [i, degs[i], dec[i]]), x -> x[3] <> 0);;",
            "Format := dec -> JoinStringsWithSeparator("
            "List(Pretty(dec), x -> Concatenation(String(x[1]), \",\", String(x[2]), \",\", String(x[3]))),"
            "\";\""
            ");;",
            "dec0 := List(Irr(tbl), chi -> ScalarProduct(tbl, char0, chi));;",
            "dec1 := List(Irr(tbl), chi -> ScalarProduct(tbl, char1, chi));;",
            "dec2 := List(Irr(tbl), chi -> ScalarProduct(tbl, char2, chi));;",
            "dec3 := List(Irr(tbl), chi -> ScalarProduct(tbl, char3, chi));;",
            "decH := List(Irr(tbl), chi -> ScalarProduct(tbl, h1, chi));;",
            'Print("C0=", Format(dec0), "\\n");',
            'Print("C1=", Format(dec1), "\\n");',
            'Print("C2=", Format(dec2), "\\n");',
            'Print("C3=", Format(dec3), "\\n");',
            'Print("H1=", Format(decH), "\\n");',
        ]
    )
    return _parse_gap_payload(_run_gap(gap_script))


def local_affine_shadow_report(
    point_generators: list[list[int]],
    adjacency: np.ndarray,
    neighbors: list[int],
    opposite: list[int],
) -> dict[str, object]:
    orbits = fetch_local_opposite_orbits(point_generators, neighbors, opposite)
    flags = [
        (orbit_index, neighbor)
        for orbit_index, orbit in enumerate(orbits)
        for neighbor in neighbors
        if any(adjacency[vertex - 1, neighbor] for vertex in orbit)
    ]

    gap_script = "\n".join(
        [
            "gens := [" + ",".join(_gap_perm(g) for g in point_generators) + "];;",
            "G := Group(gens);;",
            "H := Stabilizer(G, 1);;",
            "nbrs := [" + ",".join(str(n + 1) for n in neighbors) + "];;",
            "actN := ActionHomomorphism(H, nbrs);;",
            "Q := Image(actN);;",
            "K := KernelOfMultiplicativeGeneralMapping(actN);;",
            'Print("sizeH=", Size(H), "\\n");',
            'Print("sizeQ=", Size(Q), "\\n");',
            'Print("sizeK=", Size(K), "\\n");',
            'Print("structureQ=", StructureDescription(Q), "\\n");',
            "orbs9 := " + _gap_cells([tuple(v - 1 for v in orbit) for orbit in orbits]) + ";;",
            "flags := " + _gap_cells(flags) + ";;",
            "tblG := CharacterTable(G);;",
            "clsG := ConjugacyClasses(G);;",
            "tblQ := CharacterTable(Q);;",
            "irrQ := Irr(tblQ);;",
            "lin2 := First(Filtered(irrQ, chi -> chi[1] = 1 and chi <> TrivialCharacter(tblQ)));;",
            "repsQ := List(ConjugacyClasses(Q), Representative);;",
            "Format := dec -> JoinStringsWithSeparator("
            "List(Filtered(List([1..Length(dec)], i -> [i, irrQ[i][1], dec[i]]), x -> x[3] <> 0), "
            "x -> Concatenation(String(x[1]), \",\", String(x[2]), \",\", String(x[3]))), "
            "\";\""
            ");;",
            "PosInG := function(x)\n"
            "  return PositionProperty(clsG, c -> x in c);\n"
            "end;;",
            "FixedSlice := function(deg)\n"
            "  local valsG, idx, degsG, avgvals, psi;\n"
            "  degsG := List(Irr(tblG), chi -> chi[1]);\n"
            "  idx := Position(degsG, deg);\n"
            "  valsG := Irr(tblG)[idx];\n"
            "  avgvals := List(repsQ, function(q)\n"
            "    local h;\n"
            "    h := PreImagesRepresentative(actN, q);\n"
            "    return Sum(Elements(K), k -> valsG[PosInG(h*k)]) / Size(K);\n"
            "  end);\n"
            "  psi := Character(tblQ, avgvals);\n"
            "  return List(irrQ, chi -> ScalarProduct(tblQ, psi, chi));\n"
            "end;;",
            "vals9 := List(repsQ, q -> Number(orbs9, O -> Set(List(O, x -> x^PreImagesRepresentative(actN, q))) = O));;",
            "vals12 := List(repsQ, q -> Number(nbrs, x -> x^PreImagesRepresentative(actN, q) = x));;",
            "vals36 := List(repsQ, function(q)\n"
            "  local h;\n"
            "  h := PreImagesRepresentative(actN, q);\n"
            "  return Number(flags, f -> Position(orbs9, Set(List(orbs9[f[1]], x -> x^h))) = f[1] and f[2]^h = f[2]);\n"
            "end);;",
            "char9 := Character(tblQ, vals9);;",
            "char12 := Character(tblQ, vals12);;",
            "char36 := Character(tblQ, vals36);;",
            "dec9 := List(irrQ, chi -> ScalarProduct(tblQ, char9, chi));;",
            "dec12 := List(irrQ, chi -> ScalarProduct(tblQ, char12, chi));;",
            "dec36 := List(irrQ, chi -> ScalarProduct(tblQ, char36, chi));;",
            "dec15 := FixedSlice(15);;",
            "dec24 := FixedSlice(24);;",
            "dec81 := FixedSlice(81);;",
            "twist12 := List(irrQ, chi -> ScalarProduct(tblQ, char12 * lin2, chi));;",
            "twist27 := List(irrQ, chi -> ScalarProduct(tblQ, (char36 - char9) * lin2, chi));;",
            'Print("dec9=", Format(dec9), "\\n");',
            'Print("dec12=", Format(dec12), "\\n");',
            'Print("dec36=", Format(dec36), "\\n");',
            'Print("dec15=", Format(dec15), "\\n");',
            'Print("dec24=", Format(dec24), "\\n");',
            'Print("dec81=", Format(dec81), "\\n");',
            'Print("twist12=", Format(twist12), "\\n");',
            'Print("twist27=", Format(twist27), "\\n");',
            'Print("match15=", dec15 = dec9, "\\n");',
            'Print("match24=", dec24 = twist12, "\\n");',
            'Print("match81=", dec81 = twist27, "\\n");',
        ]
    )
    report = _parse_gap_payload(_run_gap(gap_script))
    report["orbits"] = orbits
    report["flags"] = flags
    return report


def connected_qutrit_shadow_report(
    point_generators: list[list[int]],
    adjacency: np.ndarray,
    neighbors: list[int],
    opposite: list[int],
) -> dict[str, object]:
    orbits = fetch_local_opposite_orbits(point_generators, neighbors, opposite)
    flags = [
        (orbit_index, neighbor)
        for orbit_index, orbit in enumerate(orbits)
        for neighbor in neighbors
        if any(adjacency[vertex - 1, neighbor] for vertex in orbit)
    ]

    gap_script = "\n".join(
        [
            "gens := [" + ",".join(_gap_perm(g) for g in point_generators) + "];;",
            "G := Group(gens);;",
            "H := Stabilizer(G, 1);;",
            "nbrs := [" + ",".join(str(n + 1) for n in neighbors) + "];;",
            "actN := ActionHomomorphism(H, nbrs);;",
            "Q := Image(actN);;",
            "K := KernelOfMultiplicativeGeneralMapping(actN);;",
            'Print("sizeH=", Size(H), "\\n");',
            'Print("sizeQ=", Size(Q), "\\n");',
            'Print("sizeK=", Size(K), "\\n");',
            'Print("structureH=", StructureDescription(H), "\\n");',
            'Print("structureQ=", StructureDescription(Q), "\\n");',
            'Print("center_has_K=", IsSubset(Center(H), K), "\\n");',
            "orbs9 := " + _gap_cells([tuple(v - 1 for v in orbit) for orbit in orbits]) + ";;",
            "flags := " + _gap_cells(flags) + ";;",
            "tblG := CharacterTable(G);;",
            "tblH := CharacterTable(H);;",
            "tblQ := CharacterTable(Q);;",
            "tblK := CharacterTable(K);;",
            "irrQ := Irr(tblQ);;",
            "FormatQ := dec -> JoinStringsWithSeparator("
            "List(Filtered(List([1..Length(dec)], i -> [i, irrQ[i][1], dec[i]]), x -> x[3] <> 0), "
            "x -> Concatenation(String(x[1]), \",\", String(x[2]), \",\", String(x[3]))), "
            "\";\""
            ");;",
            "repsQ := List(ConjugacyClasses(Q), Representative);;",
            "vals9 := List(repsQ, q -> Number(orbs9, O -> Set(List(O, x -> x^PreImagesRepresentative(actN, q))) = O));;",
            "vals12 := List(repsQ, q -> Number(nbrs, x -> x^PreImagesRepresentative(actN, q) = x));;",
            "vals36 := List(repsQ, function(q)\n"
            "  local h;\n"
            "  h := PreImagesRepresentative(actN, q);\n"
            "  return Number(flags, f -> Position(orbs9, Set(List(orbs9[f[1]], x -> x^h))) = f[1] and f[2]^h = f[2]);\n"
            "end);;",
            "char9 := Character(tblQ, vals9);;",
            "char12 := Character(tblQ, vals12);;",
            "char36 := Character(tblQ, vals36);;",
            "redFlag := char36 - char9;;",
            "affH1 := TrivialCharacter(tblQ) - char9 - char12 + char36;;",
            "dec9 := List(irrQ, chi -> ScalarProduct(tblQ, char9, chi));;",
            "dec12 := List(irrQ, chi -> ScalarProduct(tblQ, char12, chi));;",
            "dec36 := List(irrQ, chi -> ScalarProduct(tblQ, char36, chi));;",
            "decRed := List(irrQ, chi -> ScalarProduct(tblQ, redFlag, chi));;",
            "decAffH1 := List(irrQ, chi -> ScalarProduct(tblQ, affH1, chi));;",
            'Print("dec9_connected=", FormatQ(dec9), "\\n");',
            'Print("dec12_connected=", FormatQ(dec12), "\\n");',
            'Print("dec36_connected=", FormatQ(dec36), "\\n");',
            'Print("dec_red_connected=", FormatQ(decRed), "\\n");',
            'Print("dec_aff_h1_connected=", FormatQ(decAffH1), "\\n");',
            "irrG := Irr(tblG);;",
            "degsG := List(irrG, chi -> chi[1]);;",
            "idx81 := Position(degsG, 81);;",
            "rest := RestrictedClassFunction(irrG[idx81], tblH);;",
            "irrH := Irr(tblH);;",
            "degsH := List(irrH, chi -> chi[1]);;",
            "decH := List(irrH, chi -> ScalarProduct(tblH, rest, chi));;",
            "fusion := FusionConjugacyClasses(tblK, tblH);;",
            "EncodeH := dec -> JoinStringsWithSeparator("
            "List(Filtered(List([1..Length(dec)], i -> [i, degsH[i], dec[i]]), x -> x[3] <> 0), "
            "x -> Concatenation(String(x[1]), \",\", String(x[2]), \",\", String(x[3]))), "
            "\";\""
            ");;",
            "neutral := List([1..Length(irrH)], function(i)\n"
            "  if decH[i] = 0 then return 0; fi;\n"
            "  if irrH[i][fusion[2]] = degsH[i] then return decH[i]; fi;\n"
            "  return 0;\n"
            "end);;",
            "omega := List([1..Length(irrH)], function(i)\n"
            "  if decH[i] = 0 then return 0; fi;\n"
            "  if irrH[i][fusion[2]] = degsH[i] * E(3) then return decH[i]; fi;\n"
            "  return 0;\n"
            "end);;",
            "omega2 := List([1..Length(irrH)], function(i)\n"
            "  if decH[i] = 0 then return 0; fi;\n"
            "  if irrH[i][fusion[2]] = degsH[i] * E(3)^2 then return decH[i]; fi;\n"
            "  return 0;\n"
            "end);;",
            'Print("neutral_phase=", EncodeH(neutral), "\\n");',
            'Print("omega_phase=", EncodeH(omega), "\\n");',
            'Print("omega2_phase=", EncodeH(omega2), "\\n");',
        ]
    )
    report = _parse_gap_payload(_run_gap(gap_script))
    report["orbits"] = orbits
    report["flags"] = flags
    return report


def local_qutrit_packet_report(
    point_generators: list[list[int]],
    neighbors: list[int],
    opposite: list[int],
) -> dict[str, object]:
    gap_script = "\n".join(
        [
            "gens := [" + ",".join(_gap_perm(g) for g in point_generators) + "];;",
            "G := Group(gens);;",
            "H := Stabilizer(G, 1);;",
            "nbrs := [" + ",".join(str(n + 1) for n in neighbors) + "];;",
            "opp := [" + ",".join(str(v + 1) for v in opposite) + "];;",
            "K := KernelOfMultiplicativeGeneralMapping(ActionHomomorphism(H, nbrs));;",
            "tblG := CharacterTable(G);;",
            "tblH := CharacterTable(H);;",
            "irrG := Irr(tblG);;",
            "irrH := Irr(tblH);;",
            "degsG := List(irrG, chi -> chi[1]);;",
            "degsH := List(irrH, chi -> chi[1]);;",
            "idx81 := Position(degsG, 81);;",
            "rest81 := RestrictedClassFunction(irrG[idx81], tblH);;",
            "fusion := FusionConjugacyClasses(CharacterTable(K), tblH);;",
            "repsH := List(ConjugacyClasses(H), Representative);;",
            "valsOpp := List(repsH, h -> Number(opp, x -> x^h = x));;",
            "charOpp := Character(tblH, valsOpp);;",
            "decOpp := List(irrH, chi -> ScalarProduct(tblH, charOpp, chi));;",
            "dec81 := List(irrH, chi -> ScalarProduct(tblH, rest81, chi));;",
            "Fmt := dec -> JoinStringsWithSeparator("
            "List(Filtered(List([1..Length(dec)], i -> [i, degsH[i], dec[i]]), x -> x[3] <> 0), "
            "x -> Concatenation(String(x[1]), \",\", String(x[2]), \",\", String(x[3]))), "
            "\";\""
            ");;",
            "PhaseSlice := function(dec, z)\n"
            "  return List([1..Length(dec)], function(i)\n"
            "    if dec[i] = 0 then return 0; fi;\n"
            "    if irrH[i][fusion[2]] = degsH[i] * z then return dec[i]; fi;\n"
            "    return 0;\n"
            "  end);\n"
            "end;;",
            "CharFromDec := dec -> Sum([1..Length(dec)], i -> dec[i] * irrH[i]);;",
            "oppNeutral := PhaseSlice(decOpp, 1);;",
            "oppOmega := PhaseSlice(decOpp, E(3));;",
            "oppOmega2 := PhaseSlice(decOpp, E(3)^2);;",
            "stNeutral := PhaseSlice(dec81, 1);;",
            "stOmega := PhaseSlice(dec81, E(3));;",
            "stOmega2 := PhaseSlice(dec81, E(3)^2);;",
            "ktrivial3 := Filtered([1..Length(irrH)], i -> degsH[i] = 3 and irrH[i][fusion[2]] = 3);;",
            "matchAll := Filtered(ktrivial3, function(i)\n"
            "  local tenN, tenW, tenW2;\n"
            "  tenN := List(irrH, chi -> ScalarProduct(tblH, irrH[i] * CharFromDec(oppNeutral), chi));\n"
            "  tenW := List(irrH, chi -> ScalarProduct(tblH, irrH[i] * CharFromDec(oppOmega), chi));\n"
            "  tenW2 := List(irrH, chi -> ScalarProduct(tblH, irrH[i] * CharFromDec(oppOmega2), chi));\n"
            "  return tenN = stNeutral and tenW = stOmega and tenW2 = stOmega2;\n"
            "end);;",
            'Print("opp_module=", Fmt(decOpp), "\\n");',
            'Print("opp_neutral=", Fmt(oppNeutral), "\\n");',
            'Print("opp_omega=", Fmt(oppOmega), "\\n");',
            'Print("opp_omega2=", Fmt(oppOmega2), "\\n");',
            'Print("st_neutral=", Fmt(stNeutral), "\\n");',
            'Print("st_omega=", Fmt(stOmega), "\\n");',
            'Print("st_omega2=", Fmt(stOmega2), "\\n");',
            'Print("ktrivial3=", ktrivial3, "\\n");',
            'Print("match_all=", matchAll, "\\n");',
            "if Length(matchAll) > 0 then\n"
            "  tau := matchAll[1];\n"
            '  Print("tensor_neutral=", Fmt(List(irrH, chi -> ScalarProduct(tblH, irrH[tau] * CharFromDec(oppNeutral), chi))), "\\n");\n'
            '  Print("tensor_omega=", Fmt(List(irrH, chi -> ScalarProduct(tblH, irrH[tau] * CharFromDec(oppOmega), chi))), "\\n");\n'
            '  Print("tensor_omega2=", Fmt(List(irrH, chi -> ScalarProduct(tblH, irrH[tau] * CharFromDec(oppOmega2), chi))), "\\n");\n'
            "fi;",
        ]
    )
    return _parse_gap_payload(_run_gap(gap_script))


def parallel_classes_from_flags(
    neighbors: list[int],
    flags: list[tuple[int, int]],
) -> list[tuple[int, ...]]:
    incidence_by_line = {neighbor: set() for neighbor in neighbors}
    for orbit_index, neighbor in flags:
        incidence_by_line[neighbor].add(orbit_index)

    remaining = set(neighbors)
    classes: list[tuple[int, ...]] = []
    while remaining:
        seed = min(remaining)
        line_set = [seed]
        for candidate in sorted(remaining - {seed}):
            if all(
                incidence_by_line[candidate].isdisjoint(incidence_by_line[existing])
                for existing in line_set
            ):
                line_set.append(candidate)
            if len(line_set) == 3:
                break
        if len(line_set) != 3:
            raise RuntimeError("Failed to recover 3-line parallel class partition")
        for neighbor in line_set:
            remaining.remove(neighbor)
        classes.append(tuple(sorted(line_set)))

    if len(classes) != 4:
        raise RuntimeError(f"Expected 4 parallel classes, found {len(classes)}")
    return sorted(classes)


def direction_module_report(
    point_generators: list[list[int]],
    parallel_classes: list[tuple[int, ...]],
) -> dict[str, object]:
    gap_script = "\n".join(
        [
            "gens := [" + ",".join(_gap_perm(g) for g in point_generators) + "];;",
            "G := Group(gens);;",
            "H := Stabilizer(G, 1);;",
            "dirs := " + _gap_cells(parallel_classes) + ";;",
            "tblH := CharacterTable(H);;",
            "irrH := Irr(tblH);;",
            "degsH := List(irrH, chi -> chi[1]);;",
            "repsH := List(ConjugacyClasses(H), Representative);;",
            "valsDir := List(repsH, h -> Number(dirs, D -> Set(List(D, x -> x^h)) = D));;",
            "charDir := Character(tblH, valsDir);;",
            "charRed := charDir - TrivialCharacter(tblH);;",
            "Fmt := dec -> JoinStringsWithSeparator("
            "List(Filtered(List([1..Length(dec)], i -> [i, degsH[i], dec[i]]), x -> x[3] <> 0), "
            "x -> Concatenation(String(x[1]), \",\", String(x[2]), \",\", String(x[3]))), "
            "\";\""
            ");;",
            "decDir := List(irrH, chi -> ScalarProduct(tblH, charDir, chi));;",
            "decRed := List(irrH, chi -> ScalarProduct(tblH, charRed, chi));;",
            'Print("direction_perm=", Fmt(decDir), "\\n");',
            'Print("direction_reduced=", Fmt(decRed), "\\n");',
        ]
    )
    return _parse_gap_payload(_run_gap(gap_script))


def repo_heisenberg_hint_report() -> dict[str, object]:
    path = ROOT / "artifacts" / "e6_cubic_affine_heisenberg_model.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    fibers = [tuple(int(value) for value in fiber) for fiber in data["fiber_triads_e6id"]]
    heisenberg_map = {
        int(key): (tuple(int(x) for x in value["u"]), int(value["z"]))
        for key, value in data["e6id_to_heisenberg"].items()
    }
    u_points = sorted({coords[0] for coords in heisenberg_map.values()})
    z_values = sorted({coords[1] for coords in heisenberg_map.values()})
    affine_lines = [
        tuple(tuple(int(x) for x in point) for point in line["u_line"])
        for line in data["affine_u_lines"]
    ]
    return {
        "fiber_count": len(fibers),
        "fiber_size_hist": sorted({len(fiber) for fiber in fibers}),
        "u_point_count": len(u_points),
        "z_value_count": len(z_values),
        "affine_line_count": len(affine_lines),
        "flag_count": sum(len(line) for line in affine_lines),
    }


def canonical_e6_geometry_report(opposite: list[int]) -> dict[str, object]:
    path = ROOT / "artifacts" / "e6_cubic_affine_heisenberg_model.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    h27_global = [int(vertex) for vertex in data["w33"]["H27_global"]]
    coords = {
        int(key): (tuple(int(x) for x in value["u"]), int(value["z"]))
        for key, value in data["e6id_to_heisenberg"].items()
    }

    basis = canonical_generation_basis()
    source_to_local = {state.source_i27: state.local_index for state in basis}
    source_to_slot = {state.source_i27: state.slot for state in basis}
    source_to_sector = {state.source_i27: state.sector for state in basis}

    global_to_source = {vertex: idx for idx, vertex in enumerate(h27_global)}
    global_to_canonical = {vertex: source_to_local[idx] for vertex, idx in global_to_source.items()}

    origin_fiber = sorted(idx for idx, (u, _z) in coords.items() if u == (0, 0))
    neutral_nonorigin = sorted(
        idx for idx, (u, z) in coords.items() if u != (0, 0) and z == 0
    )
    charged_nonorigin = sorted(
        idx for idx, (u, z) in coords.items() if u != (0, 0) and z != 0
    )
    spinor_sources = sorted(idx for idx, sector in source_to_sector.items() if sector == "spinor")
    vector_sources = sorted(idx for idx, sector in source_to_sector.items() if sector == "vector")
    singlet_sources = sorted(idx for idx, sector in source_to_sector.items() if sector == "singlet")
    clean_origin_pair = sorted(
        idx for idx in origin_fiber if source_to_slot[idx] in {"H_2", "Hbar_2"}
    )

    rows: dict[int, list[str]] = {0: [], 1: [], 2: []}
    for idx, (u, _z) in coords.items():
        rows[u[0]].append(source_to_slot[idx])
    for key in rows:
        rows[key].sort()

    return {
        "opposite_order_matches_heisenberg_artifact": opposite == h27_global,
        "global_to_source_order_sample": [
            [vertex, global_to_source[vertex], global_to_canonical[vertex]]
            for vertex in h27_global[:9]
        ],
        "origin_fiber_sources": origin_fiber,
        "neutral_nonorigin_sources": neutral_nonorigin,
        "charged_nonorigin_sources": charged_nonorigin,
        "spinor_equals_charged_nonorigin": spinor_sources == charged_nonorigin,
        "vector_equals_neutral_nonorigin_plus_charged_origin_pair": vector_sources
        == sorted(neutral_nonorigin + clean_origin_pair),
        "singlet_equals_neutral_origin": singlet_sources == [origin_fiber[0]],
        "clean_higgs_pair_sources": clean_origin_pair,
        "clean_higgs_pair_slots": [source_to_slot[idx] for idx in clean_origin_pair],
        "rows_by_u1": rows,
    }


def steinberg_signature_report(
    point_generators: list[list[int]],
    degree: int = 81,
    prime: int = 3,
) -> dict[str, object]:
    gap_script = "\n".join(
        [
            "gens := [" + ",".join(_gap_perm(g) for g in point_generators) + "];;",
            "G := Group(gens);;",
            'Print("size=", Size(G), "\\n");',
            'Print("structure=", StructureDescription(G), "\\n");',
            "tbl := CharacterTable(G);;",
            "irr := Irr(tbl);;",
            "degs := List(irr, chi -> chi[1]);;",
            f"idx := Position(degs, {degree});;",
            'Print("index=", idx, "\\n");',
            "chi := irr[idx];;",
            "ords := OrdersClassRepresentatives(tbl);;",
            "sizes := SizesConjugacyClasses(tbl);;",
            "gsize := Size(G);;",
            f"PPart := function(n)\n"
            f"  local acc;\n"
            f"  acc := 1;\n"
            f"  while n mod {prime} = 0 do\n"
            f"    acc := acc * {prime};\n"
            f"    n := n / {prime};\n"
            f"  od;\n"
            f"  return acc;\n"
            f"end;;",
            "matches := ForAll([1..Length(ords)], function(i)\n"
            f"  if ords[i] mod {prime} = 0 then\n"
            "    return chi[i] = 0;\n"
            "  fi;\n"
            "  return AbsInt(chi[i]) = PPart(gsize / sizes[i]);\n"
            "end);;",
            f"pregular := Filtered([1..Length(ords)], i -> ords[i] mod {prime} <> 0);;",
            f"psingular := Filtered([1..Length(ords)], i -> ords[i] mod {prime} = 0);;",
            "regular_matches := Number(pregular, i -> AbsInt(chi[i]) = PPart(gsize / sizes[i]));;",
            "singular_zeroes := Number(psingular, i -> chi[i] = 0);;",
            'Print("matches=", matches, "\\n");',
            'Print("regular_matches=", regular_matches, "\\n");',
            'Print("regular_total=", Length(pregular), "\\n");',
            'Print("singular_zeroes=", singular_zeroes, "\\n");',
            'Print("singular_total=", Length(psingular), "\\n");',
        ]
    )
    return _parse_gap_payload(_run_gap(gap_script))


def pretty_decomp(data: list[list[int]]) -> str:
    return " + ".join(f"{mult}*{deg}" if mult != 1 else str(deg) for _idx, deg, mult in data)


def main() -> None:
    points, adjacency, edges = build_w33()
    adjacency_array = np.asarray(adjacency, dtype=int)
    lines, triangles = build_lines_and_triangles(adjacency_array)

    incidence = incidence_report(adjacency_array, lines)
    projectors = projector_report(adjacency_array)

    symplectic_generators = get_generators(points)
    antisymplectic = matrix_to_vertex_perm(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2]],
        points,
    )
    if antisymplectic is None:
        raise RuntimeError("Failed to build antisymplectic generator")

    psp_report = oriented_module_report(
        symplectic_generators,
        edges,
        triangles,
        lines,
    )
    full_report = oriented_module_report(
        symplectic_generators + [antisymplectic],
        edges,
        triangles,
        lines,
    )
    psp_steinberg = steinberg_signature_report(symplectic_generators)
    full_steinberg = steinberg_signature_report(symplectic_generators + [antisymplectic])
    neighbors = [idx for idx, value in enumerate(adjacency_array[0]) if value]
    opposite = [idx for idx, value in enumerate(adjacency_array[0]) if not value and idx != 0]
    local_shadow = local_affine_shadow_report(
        symplectic_generators + [antisymplectic],
        adjacency_array,
        neighbors,
        opposite,
    )
    connected_shadow = connected_qutrit_shadow_report(
        symplectic_generators,
        adjacency_array,
        neighbors,
        opposite,
    )
    local_packet = local_qutrit_packet_report(
        symplectic_generators,
        neighbors,
        opposite,
    )
    parallel_classes = parallel_classes_from_flags(neighbors, local_shadow["flags"])
    directions = direction_module_report(symplectic_generators, parallel_classes)
    heisenberg_hint = repo_heisenberg_hint_report()
    canonical_e6 = canonical_e6_geometry_report(opposite)

    print("W(3,3) REPRESENTATION BRIDGE")
    print("=" * 72)
    print()
    print("Incidence Sector")
    print(f"  lines: {incidence['num_lines']}")
    print(f"  point degrees in incidence matrix: {incidence['point_degree_hist']}")
    print(f"  points per line: {incidence['line_size_hist']}")
    print(f"  B B^T = A + 4I: {incidence['bbt_equals_a_plus_4i']}")
    print(f"  rank(B): {incidence['rank']}")
    print(f"  singular values: {incidence['singular_values']}")
    print("  image norms by adjacency eigenspace:")
    for eigenvalue, norms in incidence["image_norms_by_adjacency_eigenvalue"].items():
        print(f"    eig {eigenvalue}: {norms}")
    print()
    print("Interpretation:")
    print("  - the point-line incidence operator is an isomorphism on the 1- and 24-sectors")
    print("  - the 15-sector is killed exactly")
    print()
    print("Canonical Point-Space Projectors")
    print(f"  P1  = {projectors['P1_formula']}  (rank {projectors['P1_rank']})")
    print(f"  P24 = {projectors['P24_formula']}  (rank {projectors['P24_rank']})")
    print(f"  P15 = {projectors['P15_formula']}  (rank {projectors['P15_rank']})")
    print(f"  idempotent error: {projectors['idempotent_error']}")
    print(f"  orthogonality error: {projectors['orthogonality_error']}")
    print()
    print("PSp(4,3) Oriented Chain Modules")
    print(f"  group order: {psp_report['size']}")
    print(f"  C0: {pretty_decomp(psp_report['C0'])}")
    print(f"  C1: {pretty_decomp(psp_report['C1'])}")
    print(f"  C2: {pretty_decomp(psp_report['C2'])}")
    print(f"  C3: {pretty_decomp(psp_report['C3'])}")
    print(f"  H1: {pretty_decomp(psp_report['H1'])}")
    print()
    print("Full Aut(W33) Oriented Chain Modules")
    print(f"  group order: {full_report['size']}")
    print(f"  C0: {pretty_decomp(full_report['C0'])}")
    print(f"  C1: {pretty_decomp(full_report['C1'])}")
    print(f"  C2: {pretty_decomp(full_report['C2'])}")
    print(f"  C3: {pretty_decomp(full_report['C3'])}")
    print(f"  H1: {pretty_decomp(full_report['H1'])}")
    print()
    print("81-Dimensional Character Check")
    print(f"  connected group: {psp_steinberg['structure']} (order {psp_steinberg['size']})")
    print(f"  full group: {full_steinberg['structure']} (order {full_steinberg['size']})")
    print(f"  connected group satisfies 3-Steinberg signature: {psp_steinberg['matches']}")
    print(
        "    "
        f"{psp_steinberg['regular_matches']}/{psp_steinberg['regular_total']} regular classes match; "
        f"{psp_steinberg['singular_zeroes']}/{psp_steinberg['singular_total']} singular classes vanish"
    )
    print(f"  full group satisfies 3-Steinberg signature: {full_steinberg['matches']}")
    print(
        "    "
        f"{full_steinberg['regular_matches']}/{full_steinberg['regular_total']} regular classes match; "
        f"{full_steinberg['singular_zeroes']}/{full_steinberg['singular_total']} singular classes vanish"
    )
    print()
    print("Local AGL(2,3) Shadow At A Point")
    print(
        f"  quotient: {local_shadow['structureQ']} "
        f"(stabilizer {local_shadow['sizeH']}, quotient {local_shadow['sizeQ']}, kernel {local_shadow['sizeK']})"
    )
    print(f"  affine-point module (9 K-orbits on opposite points): {pretty_decomp(local_shadow['dec9'])}")
    print(f"  affine-line module (12 neighbors): {pretty_decomp(local_shadow['dec12'])}")
    print(f"  affine-flag module (36 incidences): {pretty_decomp(local_shadow['dec36'])}")
    print(f"  K-fixed slice of global 15-sector: {pretty_decomp(local_shadow['dec15'])}")
    print(f"  K-fixed slice of global 24-sector: {pretty_decomp(local_shadow['dec24'])}")
    print(f"  K-fixed slice of Steinberg 81-sector: {pretty_decomp(local_shadow['dec81'])}")
    print(f"  det-twisted affine-line module: {pretty_decomp(local_shadow['twist12'])}")
    print(f"  det-twisted reduced affine-flag module: {pretty_decomp(local_shadow['twist27'])}")
    print(f"  15^K = affine-point module: {local_shadow['match15']}")
    print(f"  24^K = det-twisted affine-line module: {local_shadow['match24']}")
    print(f"  81^K = det-twisted reduced affine-flag module: {local_shadow['match81']}")
    print()
    print("Connected Local Qutrit Split")
    print(
        f"  connected stabilizer: {connected_shadow['structureH']} "
        f"(quotient {connected_shadow['structureQ']}, center contains K: {connected_shadow['center_has_K']})"
    )
    print(f"  affine-point module under ASL(2,3): {pretty_decomp(connected_shadow['dec9_connected'])}")
    print(f"  affine-line module under ASL(2,3): {pretty_decomp(connected_shadow['dec12_connected'])}")
    print(f"  affine-flag module under ASL(2,3): {pretty_decomp(connected_shadow['dec36_connected'])}")
    print(f"  reduced affine-flag module: {pretty_decomp(connected_shadow['dec_red_connected'])}")
    print(f"  affine Levi H1 module: {pretty_decomp(connected_shadow['dec_aff_h1_connected'])}")
    print(f"  K-neutral 27-sector inside the 81: {pretty_decomp(connected_shadow['neutral_phase'])}")
    print(f"  K-omega 27-sector inside the 81: {pretty_decomp(connected_shadow['omega_phase'])}")
    print(f"  K-omega^2 27-sector inside the 81: {pretty_decomp(connected_shadow['omega2_phase'])}")
    print()
    print("Local Opposite-Point Qutrit Packet")
    print(f"  opposite-point permutation module: {pretty_decomp(local_packet['opp_module'])}")
    print(f"  neutral 9-packet: {pretty_decomp(local_packet['opp_neutral'])}")
    print(f"  omega 9-packet: {pretty_decomp(local_packet['opp_omega'])}")
    print(f"  omega^2 9-packet: {pretty_decomp(local_packet['opp_omega2'])}")
    print(f"  parallel classes of affine lines: {parallel_classes}")
    print(f"  direction permutation module: {pretty_decomp(directions['direction_perm'])}")
    print(f"  reduced direction module: {pretty_decomp(directions['direction_reduced'])}")
    print(f"  K-trivial 3-dimensional candidates: {local_packet['ktrivial3']}")
    print(f"  same 3-dimensional module tensors all three 9-packets to the Steinberg phases: {bool(local_packet['match_all'])}")
    if local_packet["match_all"]:
        print(f"  matching 3-dimensional irrep index: {local_packet['match_all'][0]}")
        print(f"  tau ⊗ neutral9 = {pretty_decomp(local_packet['tensor_neutral'])}")
        print(f"  tau ⊗ omega9 = {pretty_decomp(local_packet['tensor_omega'])}")
        print(f"  tau ⊗ omega^2 9 = {pretty_decomp(local_packet['tensor_omega2'])}")
    print(
        "  repo E6/Heisenberg packet counts: "
        f"{heisenberg_hint['fiber_count']} fibers, {heisenberg_hint['u_point_count']} affine points, "
        f"{heisenberg_hint['affine_line_count']} affine lines, {heisenberg_hint['flag_count']} flags"
    )
    print(
        "  local packet matches repo Heisenberg counts: "
        f"{len(local_shadow['orbits']) == heisenberg_hint['fiber_count'] and len(neighbors) == heisenberg_hint['affine_line_count'] and len(local_shadow['flags']) == heisenberg_hint['flag_count']}"
    )
    print()
    print("Canonical E6 Basis Geometry")
    print(
        "  local opposite-point order already is the repo E6 order: "
        f"{canonical_e6['opposite_order_matches_heisenberg_artifact']}"
    )
    print(
        "  sample global vertex -> source_i27 -> canonical local index: "
        f"{canonical_e6['global_to_source_order_sample']}"
    )
    print(f"  origin fiber sources: {canonical_e6['origin_fiber_sources']}")
    print(f"  nonorigin neutral layer: {canonical_e6['neutral_nonorigin_sources']}")
    print(f"  nonorigin charged layers: {canonical_e6['charged_nonorigin_sources']}")
    print(f"  spinor 16 = charged nonorigin packet: {canonical_e6['spinor_equals_charged_nonorigin']}")
    print(
        "  vector 10 = neutral nonorigin packet + charged origin pair: "
        f"{canonical_e6['vector_equals_neutral_nonorigin_plus_charged_origin_pair']}"
    )
    print(f"  singlet 1 = neutral origin state: {canonical_e6['singlet_equals_neutral_origin']}")
    print(
        "  clean Higgs pair sits on the charged origin fiber: "
        f"{canonical_e6['clean_higgs_pair_slots']} from sources {canonical_e6['clean_higgs_pair_sources']}"
    )
    for row_key, slots in canonical_e6["rows_by_u1"].items():
        print(f"  affine row u1={row_key}: {slots}")
    print()
    print("Cheeky Inference")
    print("  - H1 is a single irreducible 81-dimensional module for both symmetry groups")
    print("  - for type B2/C2 at q=3, 81 = 3^4 is the full 3-part of the connected automorphism group")
    print("  - the 81-character obeys the exact 3-Steinberg class signature")
    print("  - locally, the Steinberg sector shadows a det-twisted affine flag quotient of AG(2,3)")
    print("  - in the connected stabilizer it further splits into three honest 27-dimensional K-phases")
    print("  - the raw opposite-point packet already splits as three 9-dimensional K-phases")
    print("  - a single K-trivial 3-dimensional local module inflates those 9-packets to the three Steinberg 27-phases")
    print("  - that is the clean local 9 x 3 mechanism the repo’s E6/Heisenberg model has been hinting at")
    print("  - the repo’s canonical E6 27-basis already lives on that same local W33 chart")
    print("  - in that chart, 16+10+1 becomes charged nonorigin + (neutral nonorigin plus charged origin) + neutral origin")
    print("  - this upgrades the H1 sector from suggestive to a very strong Steinberg identification")
    print()
    print("Why this matters")
    print("  - the 81-dimensional transport sector is no longer an isolated Betti-number fact")
    print("  - it is the unique surviving irreducible in the oriented chain complex")
    print("  - the 15-dimensional point sector is line-invisible, while H1 carries the 81-sector")
    print("  - the point-clique complex is now best viewed as a Steinberg carrier, not just a data source")
    print("  - the local AGL(2,3) shadow distinguishes point, line, and flag geometry cleanly")
    print("  - the connected local split exposes a genuine 27 + 27 + 27 phase structure")


if __name__ == "__main__":
    main()
