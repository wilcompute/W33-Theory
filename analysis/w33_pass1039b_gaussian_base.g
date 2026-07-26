# Pass 1039b: what is the base of the GAUSSIAN (d = 4) tower?
#
# Pass 1039 found that only d = 3, 4, 6 give a transitive derived subgroup on the
# 240 roots, that d = 3 and d = 6 are the same tower (G32, blocks [2,3,6], base 40),
# and that d = 4 is a genuine sibling: Shephard-Todd G31, order 46080, derived
# 23040, transitive, blocks [2,4,16].  Blocks of size 16 give 240/16 = 15, and 15
# is the number of points of the doily W(2,2).
#
# So the obvious question: is the Gaussian base the doily?  If it is, the substrate's
# q = 3 story has an exact q = 2 sibling and "q = 3 is forced" needs a reason beyond
# the tower's existence.  If it is not, the 15 is a coincidence of counting.
#
# Reference points for the comparison, computed rather than assumed:
#   * W(2,2) doily: 15 points, 15 lines, 3 points per line, collinearity graph
#     srg(15,6,1,3), automorphism group Sp(4,2) = S6 of order 720.
#   * The d = 3 base for contrast: 40 points, rank 3, srg(40,12,2,4).

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1039b_gaussian_base.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1039b_diagnostic.txt");;

A := function(l, c) if not c then Error(Concatenation("Pass1039b failed: ", l)); fi; end;;
B := function(v) if v then return "true"; fi; return "false"; end;;

SRG := function(adj, n)
  local kk, lam, mu, i, j, common, ok;
  kk := Length(adj[1]); lam := fail; mu := fail; ok := true;
  for i in [1..n] do
    if Length(adj[i]) <> kk then ok := false; fi;
    for j in [1..n] do
      if i <> j then
        common := Length(Intersection(adj[i], adj[j]));
        if j in adj[i] then
          if lam = fail then lam := common; elif lam <> common then ok := false; fi;
        else
          if mu = fail then mu := common; elif mu <> common then ok := false; fi;
        fi;
      fi;
    od;
  od;
  return rec(ok := ok, n := n, k := kk, lambda := lam, mu := mu);
end;;

Main := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples, W,
        w, g, o, tries, C, K, b16, sys15, hom, Q, homC, QC, sub, orbital, adj, srg,
        S, pts, act, P, ptAdj, srgDoily, S15, conj, checks, names, stream, tag;

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

  # regular element of order 4, identified by Springer: |C| = 8*12*20*24 = 46080
  w := fail; tries := 0;
  while w = fail and tries < 5000 do
    tries := tries + 1;
    g := PseudoRandom(W); o := Order(g);
    if o mod 4 = 0 then
      g := g ^ (o / 4);
      if Order(g) = 4 and Size(Centralizer(W, g)) = 46080 then w := g; fi;
    fi;
  od;
  A("found regular order-4 element", w <> fail);
  C := Centralizer(W, w);
  K := DerivedSubgroup(C);
  A("|C| = 46080", Size(C) = 46080);
  A("|K| = 23040", Size(K) = 23040);

  b16 := First(AllBlocks(K), b -> Length(b) = 16);
  A("a block of size 16 exists", b16 <> fail);
  sys15 := Blocks(K, [1..240], b16);
  A("15 blocks", Length(sys15) = 15);

  hom := ActionHomomorphism(K, sys15, OnSets);
  Q := Image(hom);
  # the FULL centraliser gives the full automorphism group of the base; the derived
  # subgroup gives its simple half -- exactly as Sp(4,3) -> U4(2) sits index 2 in
  # W(E6) on the Eisenstein side.
  homC := ActionHomomorphism(C, sys15, OnSets);
  QC := Image(homC);
  sub := SortedList(List(Orbits(Stabilizer(Q, 1), [1..15]), Length));

  orbital := First(Orbits(Stabilizer(Q, 1), [1..15]), t -> Length(t) = 6);
  adj := [];
  if orbital <> fail then
    adj := List([1..15], x -> Set(List(orbital, t ->
      t ^ RepresentativeAction(Q, 1, x))));
    srg := SRG(adj, 15);
  else
    srg := rec(ok := false, n := 15, k := 0, lambda := 0, mu := 0);
  fi;

  # the doily itself, built independently: 15 points of PG(3,2), collinear iff
  # the symplectic form vanishes
  S := Sp(4,2);
  pts := NormedRowVectors(GF(2)^4);
  A("15 projective points over GF(2)", Length(pts) = 15);
  act := ActionHomomorphism(S, pts, OnLines);
  P := Image(act);
  ptAdj := List([1..15], x -> Filtered([1..15], y ->
    y <> x and IsZero(pts[x] * InvariantBilinearForm(S).matrix * pts[y])));
  srgDoily := SRG(ptAdj, 15);

  S15 := SymmetricGroup(15);
  conj := IsConjugate(S15, Q, P);

  checks := rec();
  checks.gaussian_tower_is_G31 := Size(C) = 46080 and Size(K) = 23040;
  checks.base_has_fifteen_points := Length(sys15) = 15;
  checks.derived_quotient_is_A6_of_order_360 := Size(Q) = 360 and IsSimple(Q);
  checks.full_centraliser_quotient_is_Sp42_of_order_720 := Size(QC) = 720;
  checks.quotient_is_rank_three := sub = [1,6,8];
  checks.quotient_graph_is_srg_15_6_1_3 :=
    srg.ok and srg.k = 6 and srg.lambda = 1 and srg.mu = 3;
  checks.doily_is_srg_15_6_1_3 :=
    srgDoily.ok and srgDoily.k = 6 and srgDoily.lambda = 1 and srgDoily.mu = 3;
  checks.gaussian_base_IS_the_doily := IsConjugate(S15, QC, P);
  checks.derived_half_is_index_two_in_it := Index(QC, Q) = 2;

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("|Q| = ", String(Size(Q)), "\n"));
  WriteAll(stream, Concatenation("subdegrees = ", String(sub), "\n"));
  WriteAll(stream, Concatenation("srg(quotient) = k=", String(srg.k), " lam=",
    String(srg.lambda), " mu=", String(srg.mu), " regular=", B(srg.ok), "\n"));
  WriteAll(stream, Concatenation("srg(doily) = k=", String(srgDoily.k), " lam=",
    String(srgDoily.lambda), " mu=", String(srgDoily.mu), "\n"));
  WriteAll(stream, Concatenation("conjugate in S15 = ", B(conj), "\n"));
  WriteAll(stream, Concatenation("kernel of 15-action = ",
    String(Size(Kernel(hom))), "\n"));
  CloseStream(stream);
  A("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1039b.gaussian_base.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The Gaussian d = 4 tower fibers the 240 E8 roots 16:1 onto the DOILY. Its 15-block quotient is rank 3 with subdegrees [1,6,8] and orbital graph srg(15,6,1,3); the DERIVED subgroup gives A6 of order 360 and the full centraliser gives Sp(4,2) = S6 of order 720, which is conjugate in S15 to the W(2,2) point action built independently. The simple-half / full-automorphism split is exactly the Eisenstein pattern, where Sp(4,3) gives U4(2) inside W(E6). So the Eisenstein 240 -> 40 fibration over W(3,3) has an exact Gaussian sibling 240 -> 15 over W(2,2).\",\n");
  WriteAll(stream, Concatenation("  \"centraliser\": ", String(Size(C)), ",\n"));
  WriteAll(stream, Concatenation("  \"derived\": ", String(Size(K)), ",\n"));
  WriteAll(stream, Concatenation("  \"base_points\": ", String(Length(sys15)), ",\n"));
  WriteAll(stream, Concatenation("  \"quotient_order\": ", String(Size(Q)), ",\n"));
  WriteAll(stream, Concatenation("  \"quotient_subdegrees\": ", String(sub), ",\n"));
  WriteAll(stream, Concatenation("  \"conjugate_to_doily\": ", B(conj), ",\n"));
  WriteAll(stream, "  \"comparison\": {\"d3_eisenstein\": \"240 -> 40, W(3,3), Sp(4,3)/U4(2), srg(40,12,2,4)\", \"d4_gaussian\": \"240 -> 15, W(2,2) doily, Sp(4,2) = S6, srg(15,6,1,3)\"},\n");
  WriteAll(stream, "  \"reading\": \"'q = 3 is forced' cannot rest on the existence of the Eisenstein tower, because the Gaussian tower exists too and lands on the doily -- the other symplectic quadrangle the corpus already works with. Whatever singles out q = 3 has to be a property the two towers do not share, and this pass supplies the sibling against which any such claim must now be checked.\",\n");
  WriteAll(stream, "  \"scope\": \"Identification of the d = 4 base only. It does not claim the two towers are equivalent, and does not adjudicate any q = 3 selection argument -- it removes one argument that was never valid.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1039b status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main();;
QUIT;
