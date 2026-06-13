#!/usr/bin/env python3
"""BT867 - Bell-cache split cover versus ternary transport extension.

The two BT859 cache orbits both have 162 points, as does the older ternary
transport/matter extension.  This verifier determines whether those equal
dimensions describe the same object.  They do not.

GAP proves that each cache is H/C4 for H=3^3:S4, that both caches cover the
same 81-element H/D8 base two-to-one, and that the H-equivariant commutant on
their 324-point union is D8 with 81 four-point orbits.  Exact F3 arithmetic
then separates this split deck cover from the non-split transport extension:
the cache deck involution is semisimple, while the transport shift is
square-zero and unipotent.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


GAP_SCRIPT = r"""
SizeScreen([1000,1000]);;
G := PSp(4,3);;
embs := IsomorphicSubgroups(G,AlternatingGroup(5));;
raw := List(embs,e->ConjugateSubgroups(G,Image(e)));;
H := First(Filtered(MaximalSubgroupClassReps(G),m->Index(G,m)=40),
           h->StructureDescription(h)="(C3 x C3 x C3) : S4");;
lineact := FactorCosetAction(G,H);;
sig := c->SortedList(OrbitLengths(Image(lineact,c[1]),[1..40]));;
pentadClass := First(raw,c->sig(c)=[5,5,10,20]);;
spreadClass := First(raw,c->sig(c)=[10,30]);;

incs := [];;
for i in [1..Length(pentadClass)] do
  for j in [1..Length(spreadClass)] do
    if Size(Intersection(pentadClass[i],spreadClass[j]))=10 then
      Add(incs,[i,j]);
    fi;
  od;
od;
phiP := ActionHomomorphism(G,pentadClass,OnPoints);;
phiS := ActionHomomorphism(G,spreadClass,OnPoints);;
act := function(pair,h)
  return [pair[1]^Image(phiP,h),pair[2]^Image(phiS,h)];
end;;
orbs := ShallowCopy(OrbitsDomain(H,incs,act));;
Sort(orbs,function(a,b) return Length(a)<Length(b); end);;
cache := [orbs[1],orbs[2]];;
J := List(cache,o->Stabilizer(H,o[1],act));;
N := Normalizer(H,J[1]);;

irrG := Irr(G);;
orientedIds := [2,3,11];;
cacheMults := [];;
for n in [1,2] do
  perm := InducedClassFunction(TrivialCharacter(J[n]),H);;
  Add(cacheMults,List(orientedIds,
    gi->ScalarProduct(perm,RestrictedClassFunction(irrG[gi],H))));
od;

cacheUnion := Concatenation(cache[1],cache[2]);;
phiU := ActionHomomorphism(H,cacheUnion,act);;
HU := Image(phiU);;
CU := Centralizer(SymmetricGroup(Length(cacheUnion)),HU);;
cuOrbs := Orbits(CU,[1..Length(cacheUnion)]);;

c4classes := Filtered(ConjugacyClassesSubgroups(H),
  c->Size(Representative(c))=4 and IsCyclic(Representative(c)));;

Print("RESULT group_order=",Size(G),"\n");
Print("RESULT parabolic_order=",Size(H),"\n");
Print("RESULT parabolic_structure=",StructureDescription(H),"\n");
Print("RESULT cache_orbit_sizes=",List(cache,Length),"\n");
Print("RESULT cache_stabilizer_orders=",List(J,Size),"\n");
Print("RESULT cache_stabilizer_structures=",List(J,StructureDescription),"\n");
Print("RESULT cache_stabilizers_conjugate=",
  RepresentativeAction(H,J[1],J[2])<>fail,"\n");
Print("RESULT cache_constituent_multiplicities=",cacheMults,"\n");
Print("RESULT oriented_constituent_degrees=",List(orientedIds,i->irrG[i][1]),"\n");
Print("RESULT c4_subgroup_class_count=",Length(c4classes),"\n");
Print("RESULT c4_subgroup_class_size=",Size(c4classes[1]),"\n");
Print("RESULT normalizer_order=",Size(N),"\n");
Print("RESULT normalizer_structure=",StructureDescription(N),"\n");
Print("RESULT deck_group_order=",Size(N)/Size(J[1]),"\n");
Print("RESULT union_centralizer_order=",Size(CU),"\n");
Print("RESULT union_centralizer_structure=",StructureDescription(CU),"\n");
Print("RESULT union_centralizer_orbit_count=",Length(cuOrbs),"\n");
Print("RESULT union_centralizer_orbit_sizes=",Set(List(cuOrbs,Length)),"\n");
QUIT;
"""


def run_gap() -> str:
    gap = shutil.which("gap")
    if gap:
        proc = subprocess.run(
            [gap, "-q"], input=GAP_SCRIPT, text=True, capture_output=True,
            check=True, timeout=360,
        )
        return proc.stdout

    gap_bash = Path("C:/Program Files/GAP-4.15.1/runtime/bin/bash.exe")
    if not gap_bash.exists():
        raise FileNotFoundError("GAP is required for BT867")
    tmp = ROOT / ".tmp"
    tmp.mkdir(exist_ok=True)
    gfile = tmp / "bt867_cache_split_transport_boundary.g"
    gfile.write_text(GAP_SCRIPT, newline="\n")
    drive = str(gfile)[0].lower()
    rest = str(gfile)[2:].replace("\\", "/")
    cyg = f"/cygdrive/{drive}{rest}"
    proc = subprocess.run(
        [str(gap_bash), "--norc", "-c",
         f"/opt/gap-4.15.1/gap.exe -q -b '{cyg}'"],
        cwd=str(gap_bash.parent), text=True, capture_output=True,
        check=True, timeout=420,
    )
    return proc.stdout


def parse_gap(stdout: str) -> dict[str, object]:
    values: dict[str, object] = {}
    string_keys = {
        "parabolic_structure", "normalizer_structure",
        "union_centralizer_structure",
    }
    for raw in stdout.splitlines():
        if not raw.startswith("RESULT "):
            continue
        key, value = raw.removeprefix("RESULT ").split("=", 1)
        if key in string_keys:
            values[key] = value
        elif value == "true":
            values[key] = True
        elif value == "false":
            values[key] = False
        else:
            values[key] = ast.literal_eval(value)
    required = {
        "group_order", "parabolic_order", "parabolic_structure",
        "cache_orbit_sizes", "cache_stabilizer_orders",
        "cache_stabilizer_structures", "cache_stabilizers_conjugate",
        "cache_constituent_multiplicities", "oriented_constituent_degrees",
        "c4_subgroup_class_count", "c4_subgroup_class_size",
        "normalizer_order", "normalizer_structure", "deck_group_order",
        "union_centralizer_order",
        "union_centralizer_structure", "union_centralizer_orbit_count",
        "union_centralizer_orbit_sizes",
    }
    missing = required - values.keys()
    if missing:
        raise AssertionError(f"GAP witness missing keys: {sorted(missing)}\n{stdout}")
    return values


def matmul_mod3(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(2)) % 3 for j in range(2)]
        for i in range(2)
    ]


def add_mod3(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[(a[i][j] + b[i][j]) % 3 for j in range(2)] for i in range(2)]


def scale_mod3(c: int, a: list[list[int]]) -> list[list[int]]:
    return [[c * a[i][j] % 3 for j in range(2)] for i in range(2)]


def rank_mod3(a: list[list[int]]) -> int:
    if all(x % 3 == 0 for row in a for x in row):
        return 0
    det = (a[0][0] * a[1][1] - a[0][1] * a[1][0]) % 3
    return 2 if det else 1


def main() -> None:
    gap = parse_gap(run_gap())
    identity = [[1, 0], [0, 1]]
    deck = [[0, 1], [1, 0]]
    deck_minus_identity = [[2, 1], [1, 2]]
    projector_plus = scale_mod3(2, add_mod3(identity, deck))
    projector_minus = scale_mod3(2, add_mod3(identity, scale_mod3(2, deck)))
    transport_shift = [[0, 1], [0, 0]]
    transport_unipotent = add_mod3(identity, transport_shift)
    zero = [[0, 0], [0, 0]]

    old_transport = json.loads(
        (ROOT / "data/w33_transport_ternary_cocycle_bridge_summary.json").read_text()
    )
    router = json.loads(
        (ROOT / "data/bt859_bell_compass_parabolic_router.json").read_text()
    )

    checks = {
        "two_cache_orbits_are_isomorphic_h_over_c4": (
            gap["cache_orbit_sizes"] == [162, 162]
            and gap["cache_stabilizer_orders"] == [4, 4]
            and gap["cache_stabilizer_structures"] == ["C4", "C4"]
            and gap["cache_stabilizers_conjugate"] is True
        ),
        "each_cache_contains_both_fives_not_one_chiral_five": (
            gap["oriented_constituent_degrees"] == [5, 5, 30]
            and gap["cache_constituent_multiplicities"] == [[1, 1, 8], [1, 1, 8]]
        ),
        "both_caches_double_cover_the_same_81_c4_base": (
            gap["c4_subgroup_class_count"] == 1
            and gap["c4_subgroup_class_size"] == 81
            and gap["normalizer_order"] == 8
            and gap["normalizer_structure"] == "D8"
            and gap["deck_group_order"] == 2
            and gap["parabolic_order"] // gap["normalizer_order"] == 81
            and gap["normalizer_order"] // gap["cache_stabilizer_orders"][0] == 2
        ),
        "cache_union_has_exact_d8_over_81_fibration": (
            gap["union_centralizer_order"] == 8
            and gap["union_centralizer_structure"] == "D8"
            and gap["union_centralizer_orbit_count"] == 81
            and gap["union_centralizer_orbit_sizes"] == [4]
        ),
        "outer_weyl_fuses_exactly_the_two_cache_copies": (
            router["gap"]["line_fusion"] == [[162, 162], [324], [648]]
            and router["gap"]["line_full_orbits"] == [324, 324, 648]
        ),
        "cache_deck_is_semisimple_over_f3": (
            matmul_mod3(deck, deck) == identity
            and matmul_mod3(deck_minus_identity, deck_minus_identity)
            == deck_minus_identity
            and rank_mod3(deck_minus_identity) == 1
            and matmul_mod3(projector_plus, projector_plus) == projector_plus
            and matmul_mod3(projector_minus, projector_minus) == projector_minus
            and matmul_mod3(projector_plus, projector_minus) == zero
            and add_mod3(projector_plus, projector_minus) == identity
            and rank_mod3(projector_plus) == rank_mod3(projector_minus) == 1
        ),
        "transport_extension_is_nonsplit_unipotent_over_f3": (
            old_transport["fiber_nilpotent_operator"]["matrix"] == transport_shift
            and old_transport["fiber_nilpotent_operator"]["square_zero"] is True
            and old_transport["extension_cocycle"]["cocycle_is_not_a_coboundary"] is True
            and matmul_mod3(transport_shift, transport_shift) == zero
            and rank_mod3(transport_shift) == 1
            and matmul_mod3(
                matmul_mod3(transport_unipotent, transport_unipotent),
                transport_unipotent,
            ) == identity
        ),
        "equal_162_dimensions_do_not_define_equivalent_extensions": (
            matmul_mod3(deck_minus_identity, deck_minus_identity)
            == deck_minus_identity
            and matmul_mod3(transport_shift, transport_shift) == zero
            and deck_minus_identity != zero
            and transport_shift != zero
        ),
    }
    assert all(checks.values()), {k: v for k, v in checks.items() if not v}

    output = {
        "theorem": "BT867 cache split cover and transport non-split boundary",
        "parabolic": {
            "H": gap["parabolic_structure"],
            "order": gap["parabolic_order"],
            "cache_gsets": ["H/C4", "H/C4"],
            "cache_sizes": gap["cache_orbit_sizes"],
            "stabilizers_conjugate": gap["cache_stabilizers_conjugate"],
        },
        "cache_spectral_refutation": {
            "bt866_degrees_tested": gap["oriented_constituent_degrees"],
            "multiplicities_in_each_cache": gap["cache_constituent_multiplicities"],
            "conclusion": (
                "Neither cache is one BT866 chiral 5-sector; each cache contains "
                "both conjugate 5s with equal multiplicity. Chirality is a copy label."
            ),
        },
        "shared_81_base": {
            "object": "the single H-conjugacy class of cyclic C4 stabilizers",
            "base_gset": "H/N_H(C4) = H/D8",
            "base_size": gap["c4_subgroup_class_size"],
            "normalizer": gap["normalizer_structure"],
            "normalizer_order": gap["normalizer_order"],
            "each_cache_map": "H/C4 -> H/D8 is a free two-sheet cover",
            "fiber_size": gap["deck_group_order"],
            "same_base_for_both_caches": (
                gap["c4_subgroup_class_count"] == 1
                and gap["cache_stabilizers_conjugate"] is True
            ),
        },
        "cache_union_commutant": {
            "carrier_size": sum(gap["cache_orbit_sizes"]),
            "group": gap["union_centralizer_structure"],
            "order": gap["union_centralizer_order"],
            "base_orbits": gap["union_centralizer_orbit_count"],
            "fiber_orbit_size": gap["union_centralizer_orbit_sizes"][0],
            "formula": "324 = 81 x 4 = 81 x 2_deck x 2_cache",
            "meaning": (
                "The full H-equivariant address symmetry is the square symmetry D8, "
                "not merely a numerical product of two bits."
            ),
        },
        "f3_operator_boundary": {
            "cache_deck": deck,
            "cache_deck_order": 2,
            "cache_difference": deck_minus_identity,
            "cache_difference_relation": "(D-I)^2 = D-I (rank 1)",
            "cache_projectors": {"plus": projector_plus, "minus": projector_minus},
            "cache_module": "F3^162 = V_plus(81) direct_sum V_minus(81)",
            "transport_shift": transport_shift,
            "transport_shift_relation": "N^2 = 0 (rank 1)",
            "transport_unipotent_order": 3,
            "transport_module": "0 -> 81 -> 162 -> 81 -> 0 is non-split",
            "no_go": (
                "The cache deck and transport shift cannot be conjugate: one is "
                "semisimple/idempotent after subtracting identity, the other nilpotent."
            ),
        },
        "architecture": {
            "cache_layer": "split address selection over a shared 81-route base",
            "transport_layer": "non-split ternary state propagation with memory",
            "combined_cell": (
                "A 324-slot local cell has 81 base routes and a D8 four-state "
                "address fiber; its independent 162-dimensional transport fiber "
                "carries the square-zero temporal update."
            ),
        },
        "checks": checks,
    }
    target = ROOT / "data" / "bt867_cache_split_transport_nonsplit_boundary.json"
    target.write_text(json.dumps(output, indent=2) + "\n")

    print("BT867 cache split / transport non-split boundary")
    print("  caches:       H/C4 + H/C4 = 162 + 162")
    print("  shared base:  H/D8 = 81; each cache is a 2-cover")
    print("  commutant:    D8 on 324, with 81 four-point fibers")
    print("  F3 boundary:  cache deck semisimple; transport shift nilpotent")
    print(f"  wrote {target.relative_to(ROOT)}")
    print("BT867 PASS")


if __name__ == "__main__":
    main()
