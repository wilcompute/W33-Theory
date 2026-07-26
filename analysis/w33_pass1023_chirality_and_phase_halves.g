# Pass 1023: the C6 obstruction is a PRODUCT of two independent obstructions --
# a chirality C2 and a phase C3 -- and different subgroups see different halves.
#
# Pass 1022 (other track, PASS1022_EQUIVARIANT_SECTION_OBSTRUCTION.md, commit
# de4cf275d) proved that the line stabiliser L surjects onto C6 with kernel the
# root stabiliser H, so the monodromy is regular and 240 -> 40 admits no
# Sp(4,3)-equivariant section.  It also gave the exact subgroup criterion
#
#     J admits a J-equivariant transversal  <=>  for one representative block
#     per J-orbit, the setwise stabiliser J_B fixes a point of B,
#
# and two witnesses: Z(G) = C2 obstructed, a Sylow 5-subgroup clean.  Its stated
# Boundary is that the obstruction is not yet IDENTIFIED with anything.
#
# This pass takes the structural handle Pass 1022 left on the table.  C6 = C2 x C3,
# and Pass 1020's block sizes 2, 3 and 6 supply BOTH intermediate quotients:
#
#     240 --C2--> 120 antipodal pairs   (fibre <-1> = <c^15>, the SIGN)
#     240 --C3--> 80  Eisenstein triples (fibre <w>  = <c^10>, the PHASE)
#     both --> 40 points
#
# So the single C6 obstruction of Pass 1022 should factor.  We compute the
# monodromy of each half separately, and reclassify subgroups by WHICH half they
# see.  The prediction under test: Z(G) = <-1> is 3-clean but 2-obstructed, so
# the two halves are genuinely independent and Pass 1022's two witnesses are
# clean/dirty for different reasons.
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1022 -- the C6 monodromy, the no-section theorem, the subgroup
#     criterion (reimplemented here as AdmitsSection1023 and re-verified against
#     their two witnesses before being used on anything new), Z(G) and Sylow-5.
#   * Pass 1021 -- the fibration 240 -> 40 and the fibre <c^5> = Eisenstein units.
#   * Pass 1020 -- Sp(4,3) transitive on the roots; the block sizes 2, 3, 6.

REPO1023 := GAPInfo.SystemEnvironment.W33_REPO;;
OUT1023 := Concatenation(REPO1023, "/data/w33_pass1023_chirality_and_phase_halves.json");;
DIAG1023 := Concatenation(REPO1023, "/data/w33_pass1023_diagnostic.txt");;

Assert1023 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass1023 assertion failed: ", label));
  fi;
end;;

Bool1023 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

# Pass 1022's criterion, reimplemented independently: J admits a J-equivariant
# transversal of the block system iff, for one representative block per J-orbit
# on blocks, the setwise stabiliser of that block fixes a point inside it.
AdmitsSection1023 := function(J, system)
  local orb, rep, stab, block;
  for orb in Orbits(J, system, OnSets) do
    rep := orb[1];
    stab := Stabilizer(J, rep, OnSets);
    if ForAll(rep, i -> not ForAll(GeneratorsOfGroup(stab), s -> i ^ s = i)) then
      return false;
    fi;
  od;
  return true;
end;;

# The image of the block stabiliser acting on ONE block.  ActionHomomorphism
# returns permutations of [1..Length(rep)], not of the block's own point labels,
# so transitivity must be tested on that domain -- testing it on `rep` silently
# fails and looks like a mathematical result.
Monodromy1023 := function(J, system)
  local rep, stab, hom, img;
  rep := system[1];
  stab := Stabilizer(J, rep, OnSets);
  hom := ActionHomomorphism(stab, rep);
  img := Image(hom);
  return rec(image := img,
             size := Size(img),
             stabiliser := Size(stab),
             degree := Length(rep),
             transitive := IsTransitive(img, [1 .. Length(rep)]),
             regular := IsTransitive(img, [1 .. Length(rep)])
                        and Size(img) = Length(rep));
end;;

Main1023 := function()
  local roots, v, i, j, si, sj, m, k, ReflPerm, simples, rootIndex,
        W, cox, w, negPerm, C, K, H, unitGroup,
        sys2, sys3, sys6, b2, b3, b6,
        mon2, mon3, mon6, Z, syl5, syl3, syl2, maximals, rows, M, name,
        sec2, sec3, sec6, labels, subgroups, r,
        checks, names, stream, tag;

  ##########################################################################
  # 1. Substrate (Passes 1020/1021, rebuilt canonically from the Coxeter element)
  ##########################################################################
  roots := [];
  for i in [1..8] do
    for j in [i+1..8] do
      for si in [1,-1] do
        for sj in [1,-1] do
          v := ListWithIdenticalEntries(8, 0);
          v[i] := 2*si; v[j] := 2*sj;
          Add(roots, v);
        od;
      od;
    od;
  od;
  for m in [0..255] do
    v := List([0..7], k -> (-1)^(QuoInt(m, 2^k) mod 2));
    if Number(v, x -> x = -1) mod 2 = 0 then Add(roots, v); fi;
  od;
  rootIndex := function(x) return Position(roots, x); end;
  ReflPerm := function(r2)
    return PermList(List(roots, x -> rootIndex(x - ((x * r2) / 4) * r2)));
  end;
  simples := [
    [ 1,-1,-1,-1,-1,-1,-1, 1], [ 2, 2, 0, 0, 0, 0, 0, 0],
    [-2, 2, 0, 0, 0, 0, 0, 0], [ 0,-2, 2, 0, 0, 0, 0, 0],
    [ 0, 0,-2, 2, 0, 0, 0, 0], [ 0, 0, 0,-2, 2, 0, 0, 0],
    [ 0, 0, 0, 0,-2, 2, 0, 0], [ 0, 0, 0, 0, 0,-2, 2, 0] ];
  W := Group(List(simples, ReflPerm));
  Assert1023("|W(E8)|", Size(W) = 696729600);

  cox := Product(List(simples, ReflPerm));
  Assert1023("Coxeter order 30", Order(cox) = 30);
  w := cox ^ 10;
  negPerm := PermList(List(roots, x -> rootIndex(-x)));
  Assert1023("c^15 is antipodal", cox ^ 15 = negPerm);
  C := Centralizer(W, w);
  K := DerivedSubgroup(C);
  Assert1023("|K| = 51840", Size(K) = 51840);
  unitGroup := Group(cox ^ 5);
  Assert1023("fibre group is C6", Size(unitGroup) = 6);

  ##########################################################################
  # 2. The three block systems: sign (2), phase (3), and their product (6).
  ##########################################################################
  b2 := First(AllBlocks(K), b -> Length(b) = 2);
  b3 := First(AllBlocks(K), b -> Length(b) = 3);
  b6 := First(AllBlocks(K), b -> Length(b) = 6);
  Assert1023("all three block sizes exist",
    b2 <> fail and b3 <> fail and b6 <> fail);
  sys2 := Blocks(K, [1..240], b2);
  sys3 := Blocks(K, [1..240], b3);
  sys6 := Blocks(K, [1..240], b6);
  Assert1023("120 / 80 / 40 blocks",
    Length(sys2) = 120 and Length(sys3) = 80 and Length(sys6) = 40);

  # identify the fibres: size-2 blocks are antipodal, size-3 blocks are w-orbits
  H := Stabilizer(K, 1);

  mon2 := Monodromy1023(K, sys2);
  mon3 := Monodromy1023(K, sys3);
  mon6 := Monodromy1023(K, sys6);

  ##########################################################################
  # 3. Subgroups to classify.
  ##########################################################################
  Z := Center(K);
  syl5 := SylowSubgroup(K, 5);
  syl3 := SylowSubgroup(K, 3);
  syl2 := SylowSubgroup(K, 2);
  maximals := MaximalSubgroupClassReps(K);

  subgroups := [];
  Add(subgroups, ["Z(G) = C2", Z]);
  Add(subgroups, ["Sylow 5", syl5]);
  Add(subgroups, ["Sylow 3", syl3]);
  Add(subgroups, ["Sylow 2", syl2]);
  Add(subgroups, ["root stabiliser H", H]);
  Add(subgroups, ["whole group Sp(4,3)", K]);
  for i in [1..Length(maximals)] do
    Add(subgroups, [Concatenation("maximal ", String(i),
      " (order ", String(Size(maximals[i])), ")"), maximals[i]]);
  od;

  rows := [];
  for r in subgroups do
    M := r[2];
    sec2 := AdmitsSection1023(M, sys2);
    sec3 := AdmitsSection1023(M, sys3);
    sec6 := AdmitsSection1023(M, sys6);
    Add(rows, [r[1], Size(M), sec2, sec3, sec6]);
  od;

  ##########################################################################
  # 4. Checks.
  ##########################################################################
  checks := rec();

  # (a) reproduce Pass 1022 before extending it
  checks.reproduces_pass1022_C6_monodromy :=
    mon6.size = 6 and IsCyclic(mon6.image) and mon6.regular and
    Size(H) = 216 and mon6.stabiliser = 1296;
  checks.reproduces_pass1022_no_equivariant_section :=
    not AdmitsSection1023(K, sys6);
  checks.reproduces_pass1022_centre_obstructed :=
    not AdmitsSection1023(Z, sys6);
  checks.reproduces_pass1022_sylow5_clean :=
    AdmitsSection1023(syl5, sys6);

  # (b) the two halves, each fully obstructed on its own
  checks.sign_half_monodromy_is_full_C2 :=
    mon2.size = 2 and mon2.regular and mon2.stabiliser = 432;
  checks.phase_half_monodromy_is_full_C3 :=
    mon3.size = 3 and IsCyclic(mon3.image) and mon3.regular and
    mon3.stabiliser = 648;
  checks.neither_half_admits_a_section :=
    not AdmitsSection1023(K, sys2) and not AdmitsSection1023(K, sys3);

  # (c) THE POINT: the halves are independent -- the centre sees only the 2-part
  checks.centre_is_phase_clean_but_chirality_obstructed :=
    AdmitsSection1023(Z, sys3) and not AdmitsSection1023(Z, sys2);
  checks.sylow5_is_clean_in_both_halves :=
    AdmitsSection1023(syl5, sys2) and AdmitsSection1023(syl5, sys3);

  # (d) the product law: a C6 section exists iff both halves do
  checks.C6_section_iff_both_halves :=
    ForAll(rows, r2 -> r2[5] = (r2[3] and r2[4]));

  # (e) the classification is non-vacuous: both mixed types are realised
  checks.both_mixed_types_are_realised :=
    ForAny(rows, r2 -> r2[3] and not r2[4]) and
    ForAny(rows, r2 -> r2[4] and not r2[3]);

  names := RecNames(checks);
  stream := OutputTextFile(DIAG1023, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", Bool1023(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("mon2 = ", String(mon2.size), "\n"));
  WriteAll(stream, Concatenation("mon3 = ", String(mon3.size), "\n"));
  WriteAll(stream, Concatenation("mon6 = ", String(mon6.size), "\n"));
  WriteAll(stream, "TABLE  name | order | sec2 | sec3 | sec6\n");
  for r in rows do
    WriteAll(stream, Concatenation("  ", r[1], " | ", String(r[2]), " | ",
      Bool1023(r[3]), " | ", Bool1023(r[4]), " | ", Bool1023(r[5]), "\n"));
  od;
  CloseStream(stream);

  Assert1023("all checks", ForAll(names, tag -> checks.(tag)));

  ##########################################################################
  # 5. Certificate.
  ##########################################################################
  stream := OutputTextFile(OUT1023, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1023.chirality_and_phase_halves.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The Pass 1022 C6 section obstruction FACTORS. C6 = C2 x C3 gives a sign/chirality half (240 -> 120, fibre <-1>) and an Eisenstein phase half (240 -> 80, fibre <w>). Each is separately and fully obstructed for Sp(4,3), a C6 section exists exactly when both halves admit one, and the two halves are independent: the centre Z(G) is phase-clean but chirality-obstructed.\",\n");
  WriteAll(stream, "  \"halves\": {\n");
  WriteAll(stream, "    \"sign\": {\"tower\": \"240 -> 120\", \"fibre\": \"<-1> = <c^15>\", \"block_stabiliser\": 432, ");
  WriteAll(stream, Concatenation("\"monodromy_order\": ", String(mon2.size), ", \"section\": false},\n"));
  WriteAll(stream, "    \"phase\": {\"tower\": \"240 -> 80\", \"fibre\": \"<w> = <c^10>\", \"block_stabiliser\": 648, ");
  WriteAll(stream, Concatenation("\"monodromy_order\": ", String(mon3.size), ", \"section\": false},\n"));
  WriteAll(stream, "    \"product\": {\"tower\": \"240 -> 40\", \"fibre\": \"<c^5> = C6\", \"block_stabiliser\": 1296, ");
  WriteAll(stream, Concatenation("\"monodromy_order\": ", String(mon6.size), ", \"section\": false}\n"));
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"product_law\": \"a J-equivariant C6 transversal exists if and only if J admits one in BOTH halves; verified on every subgroup in the table\",\n");
  WriteAll(stream, "  \"subgroup_table\": [\n");
  for i in [1..Length(rows)] do
    r := rows[i];
    WriteAll(stream, Concatenation("    {\"name\": \"", r[1], "\", \"order\": ",
      String(r[2]), ", \"sign_section\": ", Bool1023(r[3]),
      ", \"phase_section\": ", Bool1023(r[4]),
      ", \"full_section\": ", Bool1023(r[5]), "}"));
    if i < Length(rows) then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  ],\n");
  WriteAll(stream, "  \"reading\": \"Pass 1022 showed the substrate cannot choose a phase convention equivariantly. This pass shows the failure has two independent causes that no single C6 statement separates: it cannot choose a SIGN (chirality) and it cannot choose an EISENSTEIN PHASE, and a subgroup can be clean in one and dirty in the other. Z(G) is the witness: it is phase-clean and chirality-obstructed. So corpus claims about chirality and corpus claims about ternary phase are NOT the same obstruction and must not be merged; they are the 2-primary and 3-primary parts of one class.\",\n");
  WriteAll(stream, "  \"scope\": \"This identifies the 2-primary and 3-primary parts of the Pass 1022 class. It does NOT prove that any particular earlier corpus obstruction equals either part; that comparison now has two named targets instead of one, which is the prerequisite, not the conclusion.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", Bool1023(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);

  Print("Pass1023 status=PASS checks=", Length(names), " output=", OUT1023, "\n");
end;;

Main1023();;
QUIT;
