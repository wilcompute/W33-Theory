#!/usr/bin/env python3
"""
BT866 - Irreducible decomposition of the oriented H2 timetable carrier.

BT862 proved that H2 of the W(3,3) triangle complex is the line
permutation module twisted by the sign of the induced S4 action on a
fixed line's tetrahedron boundary.  Equivalently,

    H2 = Ind_P^G(epsilon),

where G=PSp(4,3), P=3^3:S4 is the line parabolic, and epsilon is the
unique nontrivial linear character of P.

This GAP-backed verifier computes:

  T1  Ind_P^G(1)       = 1 + 15 + 24  (plain line module).
  T2  Ind_P^G(epsilon) = 5a + 5b + 30 (oriented H2 module).
  T3  5a and 5b are complex-conjugate over CF(3)=Q(zeta_3); 30 is
      rational.
  T4  In U4(2).2 = W(E6), 5a+5b is the restriction of one irreducible
      degree-10 character, while the degree-30 constituent has two
      inequivalent outer extensions.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


GAP_SCRIPT = r"""
Main := function()
  local G, H, linear, trivialH, signH, irr, plain, oriented;
  local plainDec, orientedDec, plainIds, orientedIds;
  local ct, ct2, fusion, irrct, irrct2, j, restricted, dec;
  local pairExtensions, thirtyExtensions, ids, mults;

  G := PSp(4,3);
  H := First(MaximalSubgroupClassReps(G),
             h -> Index(G,h)=40 and
                  StructureDescription(h)="(C3 x C3 x C3) : S4");
  linear := Filtered(Irr(H), chi -> chi[1]=1);
  trivialH := First(linear, chi -> ForAll(chi, x -> x=1));
  signH := First(linear, chi -> chi<>trivialH);
  irr := Irr(G);

  plain := InducedClassFunction(trivialH,G);
  oriented := InducedClassFunction(signH,G);
  plainDec := List(irr, chi -> ScalarProduct(plain,chi));
  orientedDec := List(irr, chi -> ScalarProduct(oriented,chi));
  plainIds := Filtered([1..Length(plainDec)], i -> plainDec[i]<>0);
  orientedIds := Filtered([1..Length(orientedDec)], i -> orientedDec[i]<>0);

  Print("group_order=",Size(G),"\n");
  Print("line_parabolic_order=",Size(H),"\n");
  Print("line_parabolic_index=",Index(G,H),"\n");
  Print("line_parabolic_structure=",StructureDescription(H),"\n");
  Print("linear_characters=",Length(linear),"\n");
  Print("plain_degree=",plain[1],"\n");
  Print("plain_norm=",ScalarProduct(plain,plain),"\n");
  Print("plain_degrees=",JoinStringsWithSeparator(
        List(plainIds,i->String(irr[i][1])),","),"\n");
  Print("oriented_degree=",oriented[1],"\n");
  Print("oriented_norm=",ScalarProduct(oriented,oriented),"\n");
  Print("oriented_indices=",JoinStringsWithSeparator(
        List(orientedIds,String),","),"\n");
  Print("oriented_degrees=",JoinStringsWithSeparator(
        List(orientedIds,i->String(irr[i][1])),","),"\n");
  Print("oriented_fields=",JoinStringsWithSeparator(
        List(orientedIds,i->String(Field(irr[i]))),","),"\n");
  Print("five_pair_conjugate=",
        ComplexConjugate(irr[orientedIds[1]])=irr[orientedIds[2]],"\n");

  ct := CharacterTable("U4(2)");
  ct2 := CharacterTable("U4(2).2");
  fusion := GetFusionMap(ct,ct2);
  irrct := Irr(ct);
  irrct2 := Irr(ct2);
  pairExtensions := [];
  thirtyExtensions := [];
  for j in [1..Length(irrct2)] do
    restricted := ClassFunction(ct,irrct2[j]{fusion});
    dec := List(irrct, chi -> ScalarProduct(restricted,chi));
    ids := Filtered([1..Length(dec)], i -> dec[i]<>0);
    mults := List(ids, i -> dec[i]);
    if ids=[2,3] and mults=[1,1] then
      Add(pairExtensions,irrct2[j][1]);
    fi;
    if ids=[11] and mults=[1] then
      Add(thirtyExtensions,irrct2[j][1]);
    fi;
  od;
  Print("outer_pair_extensions=",JoinStringsWithSeparator(
        List(pairExtensions,String),","),"\n");
  Print("outer_thirty_extensions=",JoinStringsWithSeparator(
        List(thirtyExtensions,String),","),"\n");
end;
Main();
QUIT;
"""


def run_gap() -> str:
    gap = shutil.which("gap")
    if gap:
        process = subprocess.run(
            [gap, "-q"],
            input=GAP_SCRIPT,
            text=True,
            capture_output=True,
            check=True,
            timeout=60,
        )
        return process.stdout

    gap_bash = Path("C:/Program Files/GAP-4.15.1/runtime/bin/bash.exe")
    if not gap_bash.exists():
        raise RuntimeError("GAP is required for BT866 and was not found")
    tmp = ROOT / ".tmp"
    tmp.mkdir(exist_ok=True)
    script_path = tmp / "bt866_h2_decomposition.g"
    script_path.write_text(GAP_SCRIPT, newline="\n")
    drive = str(script_path)[0].lower()
    rest = str(script_path)[2:].replace("\\", "/")
    cygwin_path = f"/cygdrive/{drive}{rest}"
    process = subprocess.run(
        [
            str(gap_bash),
            "--norc",
            "-c",
            f"/opt/gap-4.15.1/gap.exe -q -b '{cygwin_path}'",
        ],
        cwd=str(gap_bash.parent),
        text=True,
        capture_output=True,
        check=True,
        timeout=120,
    )
    return process.stdout


def parse_csv_ints(value: str) -> list[int]:
    return [] if not value else [int(x) for x in value.split(",")]


def main() -> None:
    raw = run_gap()
    parsed: dict[str, str] = {}
    for line in raw.splitlines():
        if "=" in line:
            key, value = line.strip().split("=", 1)
            parsed[key] = value

    required = {
        "group_order",
        "line_parabolic_order",
        "line_parabolic_index",
        "line_parabolic_structure",
        "linear_characters",
        "plain_degree",
        "plain_norm",
        "plain_degrees",
        "oriented_degree",
        "oriented_norm",
        "oriented_indices",
        "oriented_degrees",
        "oriented_fields",
        "five_pair_conjugate",
        "outer_pair_extensions",
        "outer_thirty_extensions",
    }
    missing = required - set(parsed)
    if missing:
        raise AssertionError(f"GAP output missing keys: {sorted(missing)}")

    plain_degrees = parse_csv_ints(parsed["plain_degrees"])
    oriented_degrees = parse_csv_ints(parsed["oriented_degrees"])
    oriented_fields = parsed["oriented_fields"].split(",")
    pair_extensions = parse_csv_ints(parsed["outer_pair_extensions"])
    thirty_extensions = parse_csv_ints(parsed["outer_thirty_extensions"])

    checks = {
        "psp_order": int(parsed["group_order"]) == 25920,
        "line_parabolic": (
            int(parsed["line_parabolic_order"]) == 648
            and int(parsed["line_parabolic_index"]) == 40
            and parsed["line_parabolic_structure"] == "(C3 x C3 x C3) : S4"
        ),
        "unique_nontrivial_linear_character": (
            int(parsed["linear_characters"]) == 2
        ),
        "plain_line_module_1_15_24": (
            int(parsed["plain_degree"]) == 40
            and int(parsed["plain_norm"]) == 3
            and plain_degrees == [1, 15, 24]
        ),
        "oriented_h2_5_5_30": (
            int(parsed["oriented_degree"]) == 40
            and int(parsed["oriented_norm"]) == 3
            and oriented_degrees == [5, 5, 30]
        ),
        "five_pair_is_eisenstein_conjugate": (
            parsed["five_pair_conjugate"] == "true"
            and oriented_fields[:2] == ["CF(3)", "CF(3)"]
            and oriented_fields[2] == "Rationals"
        ),
        "outer_weyl_fuses_fives_to_ten": pair_extensions == [10],
        "thirty_has_two_outer_extensions": thirty_extensions == [30, 30],
    }
    assert all(checks.values()), checks

    output = {
        "theorem": "BT866 H2 oriented irreducible decomposition",
        "group": {
            "projective": "PSp(4,3) = U4(2)",
            "order": 25920,
            "outer_extension": "U4(2).2 = W(E6)",
        },
        "line_parabolic": {
            "structure": parsed["line_parabolic_structure"],
            "order": int(parsed["line_parabolic_order"]),
            "index": int(parsed["line_parabolic_index"]),
            "linear_characters": int(parsed["linear_characters"]),
        },
        "plain_line_module": {
            "construction": "Ind_P^G(1)",
            "decomposition_degrees": plain_degrees,
            "formula": "1 + 15 + 24",
            "degree": int(parsed["plain_degree"]),
            "character_norm": int(parsed["plain_norm"]),
        },
        "oriented_h2_module": {
            "construction": "Ind_P^G(sign_S4)",
            "decomposition_degrees": oriented_degrees,
            "formula": "5_omega + 5_omega2 + 30",
            "degree": int(parsed["oriented_degree"]),
            "character_norm": int(parsed["oriented_norm"]),
            "constituent_fields": oriented_fields,
            "five_pair_complex_conjugate": True,
        },
        "outer_weyl_extension": {
            "five_pair": "5_omega + 5_omega2 restricts from one irreducible 10",
            "degree_10_extensions_found": pair_extensions,
            "thirty_sector": "the rational 30 has two inequivalent extensions",
            "degree_30_extensions_found": thirty_extensions,
        },
        "homology_dictionary": {
            "H0": "1",
            "H1": "Steinberg 81",
            "H2": "5_omega + 5_omega2 + 30",
            "euler_dimension": "1 - 81 + 40 = -40",
        },
        "boundary": (
            "The 5+5bar pair has the same outer-fusion pattern as the two "
            "BT859 chiral cache branches, but an objectwise intertwiner is "
            "not yet proved. The two extensions of the 30-sector expose an "
            "outer parity choice; identifying it with the BT857 local gauge "
            "bit remains open."
        ),
        "checks": checks,
    }
    with open("data/bt866_h2_oriented_irreducible_decomposition.json", "w") as handle:
        json.dump(output, handle, indent=2)

    print("BT866 H2 oriented irreducible decomposition")
    print("  plain line module:    1 + 15 + 24")
    print("  oriented H2 module:   5_omega + 5_omega2 + 30")
    print("  fields:               CF(3), CF(3), Q")
    print("  W(E6) outer lift:     5+5bar -> irreducible 10")
    print("  rational 30-sector:   two outer extensions")
    print("  wrote data/bt866_h2_oriented_irreducible_decomposition.json")
    print("BT866 PASS")


if __name__ == "__main__":
    main()
