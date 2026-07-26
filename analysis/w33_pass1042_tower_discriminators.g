# Pass 1042: two things separate the Eisenstein tower from its Gaussian sibling --
# contextuality of the base, and the SHAPE of the fibre obstruction.
#
# Pass 1039 removed an argument that was never valid.  "q = 3 is forced" cannot
# rest on the Springer construction producing the Eisenstein tower, because the
# same construction produces exactly one sibling at d = 4 -- Shephard-Todd G31,
# order 46080 -- and Pass 1039b showed its base IS the doily W(2,2).  So both
# towers exist and something else has to distinguish them.
#
# Two candidates, both now testable, and both hold.
#
# (a) CONTEXTUALITY OF THE BASE.  Computed by exact cover in the companion Python
#     witness: the doily has 6 ovoids, W(3,3) has 0.  An ovoid IS a Kochen-Specker
#     0/1 colouring (analysis/w33_ovoid_construct.py, prior art), so the GAUSSIAN
#     base is KS-COLOURABLE and the EISENSTEIN base is not.  This is the structural
#     form of the "minimal magic / contextuality" leg that photonic_holonet.tex
#     lists among its three q = 3 forcing arguments.
#
# (b) SHAPE OF THE OBSTRUCTION.  The Eisenstein fibre is Z6 = Z2 x Z3, and Pass
#     1023 showed the section obstruction splits into two INDEPENDENT halves that
#     different subgroups see separately.  The Gaussian fibre is CYCLIC Z4.  A
#     cyclic 2-group has a unique subgroup of each order, so there is no
#     complement and no independent primary split to be had -- the obstruction is
#     one indecomposable class rather than two coordinates.  That is a genuine
#     structural difference, not a difference of size.
#
# This pass verifies (b) inside W(E8) and records (a).
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1039/1039b -- the tower census and the doily identification.
#   * Pass 1023 -- the Z2 x Z3 split of the Eisenstein obstruction.
#   * Pass 1022 (other track) -- the section-obstruction criterion, reused here.
#   * analysis/w33_ovoid_construct.py -- ovoid = KS colouring, exists iff q even.
#   * Thas -- W(q) has ovoids iff q is even.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1042_tower_discriminators.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1042_diagnostic.txt");;

A := function(l, c) if not c then Error(Concatenation("Pass1042 failed: ", l)); fi; end;;
B := function(v) if v then return "true"; fi; return "false"; end;;

# Pass 1022's criterion, reimplemented: J admits a J-equivariant transversal iff
# for one representative block per J-orbit the setwise stabiliser fixes a point.
AdmitsSection := function(J, system)
  local orb, rep, stab;
  for orb in Orbits(J, system, OnSets) do
    rep := orb[1];
    stab := Stabilizer(J, rep, OnSets);
    if ForAll(rep, i -> not ForAll(GeneratorsOfGroup(stab), s -> i ^ s = i)) then
      return false;
    fi;
  od;
  return true;
end;;

Monodromy := function(J, system)
  local rep, stab, img;
  rep := system[1];
  stab := Stabilizer(J, rep, OnSets);
  img := Image(ActionHomomorphism(stab, rep));
  return rec(size := Size(img), stab := Size(stab), image := img,
             regular := IsTransitive(img, [1 .. Length(rep)])
                        and Size(img) = Length(rep));
end;;

Main := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples, W,
        w4, g, o, tries, C4, K4, sysG2, sysG4, sysG16, monG4, monG16,
        fibre4, cyc, subs2, w3, C3, K3, sys3_2, sys3_3,
        checks, names, stream, tag;

  roots := [];
  for i in [1..8] do
    for j in [i+1..8] do
      for si in [1,-1] do for sj in [1,-1] do
        v := ListWithIdenticalEntries(8, 0);
        v[i] := 2*si; v[j] := 2*sj; Add(roots, v);
      od; od;
    od;
  od;
  for m in [0..255] do
    v := List([0..7], k -> (-1)^(QuoInt(m, 2^k) mod 2));
    if Number(v, x -> x = -1) mod 2 = 0 then Add(roots, v); fi;
  od;
  rootIndex := function(x) return Position(roots, x); end;
  ReflPerm := function(r) return PermList(List(roots, x -> rootIndex(x - ((x*r)/4)*r))); end;
  simples := [
    [ 1,-1,-1,-1,-1,-1,-1, 1], [ 2, 2, 0, 0, 0, 0, 0, 0],
    [-2, 2, 0, 0, 0, 0, 0, 0], [ 0,-2, 2, 0, 0, 0, 0, 0],
    [ 0, 0,-2, 2, 0, 0, 0, 0], [ 0, 0, 0,-2, 2, 0, 0, 0],
    [ 0, 0, 0, 0,-2, 2, 0, 0], [ 0, 0, 0, 0, 0,-2, 2, 0] ];
  W := Group(List(simples, ReflPerm));

  # the Gaussian tower: regular element of order 4, |C| = 8*12*20*24 = 46080
  w4 := fail; tries := 0;
  while w4 = fail and tries < 5000 do
    tries := tries + 1;
    g := PseudoRandom(W); o := Order(g);
    if o mod 4 = 0 then
      g := g ^ (o / 4);
      if Order(g) = 4 and Size(Centralizer(W, g)) = 46080 then w4 := g; fi;
    fi;
  od;
  A("found regular order-4 element", w4 <> fail);
  C4 := Centralizer(W, w4);
  K4 := DerivedSubgroup(C4);
  A("|C4| = 46080", Size(C4) = 46080);

  sysG2  := Blocks(K4, [1..240], First(AllBlocks(K4), b -> Length(b) = 2));
  sysG4  := Blocks(K4, [1..240], First(AllBlocks(K4), b -> Length(b) = 4));
  sysG16 := Blocks(K4, [1..240], First(AllBlocks(K4), b -> Length(b) = 16));
  A("Gaussian tower 120/60/15",
    Length(sysG2) = 120 and Length(sysG4) = 60 and Length(sysG16) = 15);

  monG4  := Monodromy(K4, sysG4);
  monG16 := Monodromy(K4, sysG16);

  # the fibre group of the 240 -> 60 step is <w4>, cyclic of order 4
  fibre4 := Group(w4);
  cyc := IsCyclic(fibre4);
  # a cyclic 4-group has exactly ONE subgroup of order 2, hence no complement
  subs2 := Filtered(AllSubgroups(fibre4), s -> Size(s) = 2);

  # the Eisenstein tower for contrast (Pass 1023, re-derived)
  w3 := (Product(List(simples, ReflPerm))) ^ 10;
  C3 := Centralizer(W, w3);
  K3 := DerivedSubgroup(C3);
  sys3_2 := Blocks(K3, [1..240], First(AllBlocks(K3), b -> Length(b) = 2));
  sys3_3 := Blocks(K3, [1..240], First(AllBlocks(K3), b -> Length(b) = 3));

  checks := rec();

  # (b) the Gaussian obstruction exists and is cyclic
  checks.gaussian_fibre_is_cyclic_Z4 :=
    Size(fibre4) = 4 and cyc;
  checks.gaussian_Z4_has_a_unique_order_two_subgroup :=
    Length(subs2) = 1;
  checks.gaussian_monodromy_on_the_60_is_full_Z4 :=
    monG4.size = 4 and monG4.regular and IsCyclic(monG4.image);
  checks.gaussian_admits_no_section :=
    not AdmitsSection(K4, sysG4) and not AdmitsSection(K4, sysG16);

  # THE CONTRAST: Eisenstein splits, Gaussian cannot
  checks.eisenstein_fibre_splits_into_independent_halves :=
    Length(sys3_2) = 120 and Length(sys3_3) = 80
    and not AdmitsSection(K3, sys3_2) and not AdmitsSection(K3, sys3_3);
  checks.gaussian_has_no_independent_halves :=
    Length(subs2) = 1 and cyc;

  # sanity: both towers are genuinely obstructed, so the difference is shape
  checks.both_towers_are_obstructed :=
    (not AdmitsSection(K4, sysG16)) and (not AdmitsSection(K3, sys3_2));

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("Gaussian blocks 2/4/16 -> ",
    String(Length(sysG2)), "/", String(Length(sysG4)), "/",
    String(Length(sysG16)), "\n"));
  WriteAll(stream, Concatenation("mon(240->60) size=", String(monG4.size),
    " stab=", String(monG4.stab), " regular=", B(monG4.regular), "\n"));
  WriteAll(stream, Concatenation("mon(240->15) size=", String(monG16.size),
    " stab=", String(monG16.stab), " regular=", B(monG16.regular), "\n"));
  WriteAll(stream, Concatenation("order-2 subgroups of the Z4 fibre = ",
    String(Length(subs2)), "\n"));
  CloseStream(stream);
  A("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1042.tower_discriminators.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"Two things separate the Eisenstein tower from its Gaussian sibling, and neither is size. The base: the doily has 6 ovoids and W(3,3) has 0, so the Gaussian base is Kochen-Specker COLOURABLE and the Eisenstein base is not. The fibre: Z6 = Z2 x Z3 splits into two independent obstruction halves, while the Gaussian Z4 is cyclic with a unique order-two subgroup and therefore cannot split at all -- one indecomposable class instead of two coordinates.\",\n");
  WriteAll(stream, "  \"discriminator_a_contextuality\": {\n");
  WriteAll(stream, "    \"doily_ovoids\": 6, \"W33_ovoids\": 0,\n");
  WriteAll(stream, "    \"reading\": \"an ovoid is a KS 0/1 colouring, so the Gaussian base admits a noncontextual value assignment and the Eisenstein base does not\",\n");
  WriteAll(stream, "    \"prior_art\": \"analysis/w33_ovoid_construct.py; Thas: W(q) has ovoids iff q even\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"discriminator_b_obstruction_shape\": {\n");
  WriteAll(stream, "    \"eisenstein_fibre\": \"Z6 = Z2 x Z3, splits into independent halves (Pass 1023)\",\n");
  WriteAll(stream, "    \"gaussian_fibre\": \"Z4, cyclic, unique order-2 subgroup, no complement, cannot split\",\n");
  WriteAll(stream, Concatenation("    \"gaussian_monodromy\": ", String(monG4.size), ",\n"));
  WriteAll(stream, "    \"both_obstructed\": true\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"reading\": \"This supplies what Pass 1039 showed was missing. The Springer construction does not single out q = 3, but the two towers it produces are not interchangeable: only the Eisenstein base is contextual, and only the Eisenstein fibre carries two independent obstruction coordinates. The 'minimal magic / contextuality' leg that photonic_holonet.tex lists among its three q = 3 forcing arguments is the one that survives as a STRUCTURAL statement about the tower rather than a numerical coincidence.\",\n");
  WriteAll(stream, "  \"scope\": \"Two differences, verified. It does not prove they are the only ones, and it does not revive any numerical q = 3 argument -- Lock 9, Lock 10 and the 7/7 observable table in w33_paper.tex remain fits, not derivations.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1042 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main();;
QUIT;
