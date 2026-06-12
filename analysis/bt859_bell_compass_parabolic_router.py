#!/usr/bin/env python3
"""BT859 - Bell/compass parabolic router.

The two appearances of 1296 in the architecture are not the same G-set:

* the compass carrier has 1296 incident cross-class A5 pairs whose
  intersection is D10;
* a Bell-line stabilizer has order 1296 in the full W(E6) symmetry, with
  projective image of order 648.

GAP computes the actual actions.  The line (Siegel) parabolic splits the
compass carrier into 162+162+324+648 under PSp(4,3).  The four orbits are
classified by the fixed Bell line lying in a pentad core's 5_L, 5_R, 10,
or 20 line orbit.  Hence their normalized sizes form the complete binary
prefix code 1/8+1/8+1/4+1/2=1.  The outer W(E6) involution fuses the two
chiral 162 cache orbits, leaving 324+324+648.

The dual point parabolic behaves differently: it has two regular 648
orbits projectively, and the full outer extension preserves both sheets.
Thus route chirality is gauged by the outer symmetry, while the point-side
address sheet is not.
"""
from __future__ import annotations

import ast
from fractions import Fraction
import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


GAP_SCRIPT = r"""
SizeScreen([1000,1000]);;
G := PSp(4,3);;
embs := IsomorphicSubgroups(G, AlternatingGroup(5));;
raw := List(embs, e -> ConjugateSubgroups(G, Image(e)));;
maxes := Filtered(MaximalSubgroupClassReps(G), m -> Index(G,m)=40);;
Hline := First(maxes, h -> StructureDescription(h)="(C3 x C3 x C3) : S4");;
Hpoint := First(maxes, h -> h<>Hline);;
lineact := FactorCosetAction(G,Hline);;

sig := c -> SortedList(OrbitLengths(Image(lineact,c[1]),[1..40]));;
pentadClass := First(raw, c -> sig(c)=[5,5,10,20]);;
spreadClass := First(raw, c -> sig(c)=[10,30]);;

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
AutG := AutomorphismGroup(G);;
InnG := InnerAutomorphismsAutomorphismGroup(AutG);;
outer := First(GeneratorsOfGroup(AutG), a -> not a in InnG);;

actionData := function(H)
  local perms,h,pP,pS,imgs,z,pair,K,orbs,rows,o,A,B,D,
        Hout,conj,beta,Ai,Bi,op,Kfull,forbs,fusion,fo,parts;
  perms := [];
  for h in GeneratorsOfGroup(H) do
    pP := Image(phiP,h);; pS := Image(phiS,h);; imgs := [];
    for z in [1..Length(incs)] do
      pair := incs[z];
      Add(imgs,Position(incs,[pair[1]^pP,pair[2]^pS]));
    od;
    Add(perms,PermList(imgs));
  od;
  K := Group(perms);;
  orbs := Orbits(K,[1..Length(incs)]);;
  rows := [];
  for o in orbs do
    pair := incs[o[1]];
    A := pentadClass[pair[1]];; B := spreadClass[pair[2]];;
    D := Intersection(A,B);;
    Add(rows,[Length(o),Size(Intersection(A,H)),Size(Intersection(B,H)),
      Size(Intersection(D,H)),Length(Orbit(Image(lineact,A),1)),
      Length(Orbit(Image(lineact,B),1))]);
  od;
  Sort(rows);

  Hout := Image(outer,H);;
  conj := RepresentativeAction(G,Hout,H);;
  beta := GroupHomomorphismByImages(G,G,GeneratorsOfGroup(G),
    List(GeneratorsOfGroup(G),x->Image(outer,x)^conj));;
  imgs := [];
  for z in [1..Length(incs)] do
    pair := incs[z];
    Ai := Position(pentadClass,Image(beta,pentadClass[pair[1]]));
    Bi := Position(spreadClass,Image(beta,spreadClass[pair[2]]));
    Add(imgs,Position(incs,[Ai,Bi]));
  od;
  op := PermList(imgs);;
  Kfull := Group(Concatenation(perms,[op]));;
  forbs := Orbits(Kfull,[1..Length(incs)]);;
  fusion := [];
  for fo in forbs do
    parts := Filtered(List(orbs,o->Length(Intersection(fo,o))),x->x>0);
    Sort(parts); Add(fusion,parts);
  od;
  Sort(fusion);
  return rec(projectiveOrder:=Size(K), projectiveOrbits:=SortedList(List(orbs,Length)),
    rows:=rows, fullOrder:=Size(Kfull), fullOrbits:=SortedList(List(forbs,Length)),
    fusion:=fusion);
end;;

L := actionData(Hline);;
P := actionData(Hpoint);;

Print("RESULT group_order=",Size(G),"\n");
Print("RESULT aut_order=",Size(AutG),"\n");
Print("RESULT incidences=",Length(incs),"\n");
Print("RESULT line_structure=",StructureDescription(Hline),"\n");
Print("RESULT point_structure=",StructureDescription(Hpoint),"\n");
Print("RESULT line_on_points=",SortedList(OrbitLengths(Hline,[1..40])),"\n");
Print("RESULT line_on_lines=",SortedList(OrbitLengths(Image(lineact,Hline),[1..40])),"\n");
Print("RESULT point_on_points=",SortedList(OrbitLengths(Hpoint,[1..40])),"\n");
Print("RESULT point_on_lines=",SortedList(OrbitLengths(Image(lineact,Hpoint),[1..40])),"\n");
Print("RESULT line_projective_order=",L.projectiveOrder,"\n");
Print("RESULT line_projective_orbits=",L.projectiveOrbits,"\n");
Print("RESULT line_rows=",L.rows,"\n");
Print("RESULT line_full_order=",L.fullOrder,"\n");
Print("RESULT line_full_orbits=",L.fullOrbits,"\n");
Print("RESULT line_fusion=",L.fusion,"\n");
Print("RESULT point_projective_order=",P.projectiveOrder,"\n");
Print("RESULT point_projective_orbits=",P.projectiveOrbits,"\n");
Print("RESULT point_full_order=",P.fullOrder,"\n");
Print("RESULT point_full_orbits=",P.fullOrbits,"\n");
Print("RESULT point_fusion=",P.fusion,"\n");
QUIT;
"""


def run_gap(script: str) -> str:
    gap = shutil.which("gap")
    if gap:
        proc = subprocess.run(
            [gap, "-q"], input=script, text=True, capture_output=True,
            check=True, timeout=120,
        )
        return proc.stdout

    gap_bash = Path("C:/Program Files/GAP-4.15.1/runtime/bin/bash.exe")
    if not gap_bash.exists():
        raise FileNotFoundError("GAP is required for BT859")
    tmp = ROOT / ".tmp"
    tmp.mkdir(exist_ok=True)
    gfile = tmp / "bt859_bell_compass_parabolic_router.g"
    gfile.write_text(script, newline="\n")
    drive = str(gfile)[0].lower()
    rest = str(gfile)[2:].replace("\\", "/")
    cyg = f"/cygdrive/{drive}{rest}"
    proc = subprocess.run(
        [str(gap_bash), "--norc", "-c",
         f"/opt/gap-4.15.1/gap.exe -q -b '{cyg}'"],
        cwd=str(gap_bash.parent), text=True, capture_output=True,
        check=True, timeout=180,
    )
    return proc.stdout


def parse_gap(stdout: str) -> dict[str, object]:
    values: dict[str, object] = {}
    string_keys = {"line_structure", "point_structure"}
    for raw in stdout.splitlines():
        if not raw.startswith("RESULT "):
            continue
        key, value = raw.removeprefix("RESULT ").split("=", 1)
        values[key] = value if key in string_keys else ast.literal_eval(value)
    required = {
        "group_order", "aut_order", "incidences", "line_structure",
        "point_structure", "line_on_points", "line_on_lines",
        "point_on_points", "point_on_lines", "line_projective_order",
        "line_projective_orbits", "line_rows", "line_full_order",
        "line_full_orbits", "line_fusion", "point_projective_order",
        "point_projective_orbits", "point_full_order", "point_full_orbits",
        "point_fusion",
    }
    missing = required - values.keys()
    if missing:
        raise AssertionError(f"GAP witness missing keys: {sorted(missing)}\n{stdout}")
    return values


def main() -> None:
    gap = parse_gap(run_gap(GAP_SCRIPT))
    expected_rows = [
        [162, 12, 2, 2, 5, 30],
        [162, 12, 2, 2, 5, 30],
        [324, 6, 6, 2, 10, 10],
        [648, 3, 2, 1, 20, 30],
    ]
    prefix = {
        "mirror_dark20": {"orbit": 648, "weight": "1/2", "word": "0"},
        "schedule10": {"orbit": 324, "weight": "1/4", "word": "10"},
        "cache5_left": {"orbit": 162, "weight": "1/8", "word": "110"},
        "cache5_right": {"orbit": 162, "weight": "1/8", "word": "111"},
    }
    kraft = sum(Fraction(row["weight"]) for row in prefix.values())
    checks = {
        "compass_incidence_count": gap["incidences"] == 1296,
        "two_parabolics_are_dual": (
            gap["line_on_points"] == [4, 36]
            and gap["line_on_lines"] == [1, 12, 27]
            and gap["point_on_points"] == [1, 12, 27]
            and gap["point_on_lines"] == [4, 36]
        ),
        "line_projective_prefix_orbits": gap["line_projective_orbits"] == [162, 162, 324, 648],
        "line_orbits_have_objectwise_signatures": gap["line_rows"] == expected_rows,
        "prefix_code_is_complete": kraft == 1,
        "outer_fuses_only_cache_chirality": (
            gap["line_full_orbits"] == [324, 324, 648]
            and gap["line_fusion"] == [[162, 162], [324], [648]]
        ),
        "point_projective_sheets_are_regular": (
            gap["point_projective_order"] == 648
            and gap["point_projective_orbits"] == [648, 648]
        ),
        "point_sheets_survive_outer_extension": (
            gap["point_full_order"] == 1296
            and gap["point_full_orbits"] == [648, 648]
            and gap["point_fusion"] == [[648], [648]]
        ),
    }
    assert all(checks.values()), {k: v for k, v in checks.items() if not v}

    out = {
        "theorem": "BT859 Bell-compass parabolic router",
        "gap": gap,
        "prefix_decoder": prefix,
        "kraft_sum": str(kraft),
        "interpretation": {
            "projective_line_router": "0=dark mirror, 10=schedule, 110/111=left/right pentad cache",
            "full_line_router": "outer W(E6) gauges cache chirality: 11 is one cache class",
            "point_addressing": "two 648 address sheets remain distinct; each is a PSp-parabolic torsor",
            "boundary": "1296 count equality is not a regular G-set identification",
        },
        "checks": checks,
    }
    target = ROOT / "data" / "bt859_bell_compass_parabolic_router.json"
    target.write_text(json.dumps(out, indent=2) + "\n")

    print("BT859 Bell-compass parabolic router")
    print("  PSp line orbits: 162_L + 162_R + 324 + 648")
    print("  full line orbits: 324_cache + 324_schedule + 648_mirror")
    print("  prefix decoder: 110/111, 10, 0 (Kraft sum = 1)")
    print("  point router: two regular 648 sheets, not outer-fused")
    print(f"  wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
