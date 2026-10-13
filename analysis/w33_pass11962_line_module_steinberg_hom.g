#############################################################################
## Pass 11962 -- the 40-line module and the Steinberg St_81 of PSp(4,3).
##
##   PERM = the 40-line permutation module (1 + 15 + 24),  St = degree-81 irreducible.
##   For a subgroup H:
##     HOM(H)   = < Res PERM, Res St >_H           (dimension of intertwiners)
##     EMBED(H) = for every irrep chi of H: <Res PERM,chi> <= <Res St,chi>
##   EMBED(H) is exactly the condition for an INJECTIVE H-equivariant map (a lossless
##   storage embedding), by complete reducibility over C.
##   ORBITS(H) = number of H-orbits on the 40 lines = <Res PERM, 1_H> (Burnside).  Since
##   <Res St, 1_H> bounds the invariant directions in the carrier, ORBITS(H) > that
##   bound already forbids an embedding.
#############################################################################

Symp := function(u,v) return (u[1]*v[3]-u[3]*v[1]+u[2]*v[4]-u[4]*v[2]) mod 3; end;;
Nrm := function(v) local c; c := First(v, x->x<>0); return List(v, x -> (x*(c^-1 mod 3)) mod 3); end;;
Pts := Set(List(Filtered(Tuples([0..2],4), v -> v<>[0,0,0,0]), Nrm));;
if Length(Pts) <> 40 then Error("40 points"); fi;
LinesSet := Set(List(Filtered(Combinations([1..40],2), pr -> Symp(Pts[pr[1]],Pts[pr[2]])=0),
  pr -> Set(List(Filtered(Tuples([0..2],2), t -> t<>[0,0]),
     t -> Position(Pts, Nrm(List([1..4], k -> (t[1]*Pts[pr[1]][k]+t[2]*Pts[pr[2]][k]) mod 3)))))));;
LinesSet := Filtered(LinesSet, l -> Length(l)=4);;
if Length(LinesSet) <> 40 then Error("40 lines"); fi;

TransMat := function(v, c)
  local I4; I4 := IdentityMat(4);
  return List([1..4], i -> List([1..4], j -> (I4[i][j] + c*Symp(I4[i],v)*v[j]) mod 3));
end;;
SpG := Group(List(Concatenation(List(Pts, v -> [TransMat(v,1), TransMat(v,2)])), m -> m*One(GF(3))));;
if Size(SpG) <> 51840 then Error("Sp(4,3) order"); fi;
ActPoints := m -> PermList(List(Pts, v -> Position(Pts, Nrm(List(v*m, IntFFE)))));;
PSpPts := Group(List(GeneratorsOfGroup(SpG), ActPoints));;
if Size(PSpPts) <> 25920 then Error("PSp(4,3) order"); fi;
ActLines := g -> PermList(List(LinesSet, l -> Position(LinesSet, Set(List(l, p -> p^g)))));;
G := Group(List(GeneratorsOfGroup(PSpPts), ActLines));;
if Size(G) <> 25920 or Length(Orbit(G,1)) <> 40 then Error("line action"); fi;

pc := PermutationCharacter(G, Stabilizer(G, 1));;
T := CharacterTable(G);; irr := Irr(T);;
dec := List(irr, c -> ScalarProduct(T, c, pc));;
perm := Filtered([1..Length(irr)], i -> dec[i] <> 0);;
if List(perm, i -> [irr[i][1], dec[i]]) <> [[1,1],[15,1],[24,1]] then Error("1+15+24"); fi;
stPos := Filtered([1..Length(irr)], i -> irr[i][1] = 81);;
if Length(stPos) <> 1 then Error("unique St"); fi;
St := irr[stPos[1]];;

S3 := SylowSubgroup(G, 3);;
RS := RestrictedClassFunction(St, S3);;
tS := UnderlyingCharacterTable(RS);;
regular := ForAll([1..Length(ConjugacyClasses(tS))], i ->
  (Representative(ConjugacyClasses(tS)[i]) = One(S3) and RS[i] = 81) or
  (Representative(ConjugacyClasses(tS)[i]) <> One(S3) and RS[i] = 0));;

SmallId := function(H)
  if Size(H) <= 2000 and Size(H) <> 1024 then return IdGroup(H); fi;
  return [Size(H), 0];
end;;

HomEmb := function(H)
  local rp, rs, tH, irH, hom, emb, orb, trSt;
  rp := RestrictedClassFunction(pc, H);
  rs := RestrictedClassFunction(St, H);
  tH := UnderlyingCharacterTable(rp);
  irH := Irr(tH);
  hom := ScalarProduct(tH, rp, rs);
  emb := ForAll(irH, c -> ScalarProduct(tH, rp, c) <= ScalarProduct(tH, rs, c));
  orb := Length(Orbits(H, [1..40]));
  trSt := ScalarProduct(tH, rs, TrivialCharacter(H));
  return [Size(H), hom, emb, orb, trSt, SmallId(H)];
end;;

reps := List(ConjugacyClassesSubgroups(G), Representative);;
rows := List(reps, HomEmb);;
emb := Filtered(rows, r -> r[3]);;
noemb := Filtered(rows, r -> not r[3]);;
orbExplained := Filtered(noemb, r -> r[4] > r[5]);;
orbUnexplained := Filtered(noemb, r -> r[4] <= r[5]);;
maxes := List(ConjugacyClassesMaximalSubgroups(G), Representative);;
bad := Filtered(rows, r -> r[4] <> ScalarProduct(RestrictedClassFunction(pc, reps[Position(rows, r)]),
                                                 TrivialCharacter(reps[Position(rows, r)])));;
h27 := Filtered(rows, r -> r[1] = 27);;

Print("RESULT_PERM_DECOMP 1+15+24\n");
Print("RESULT_UNIQUE_ST81 true\n");
Print("RESULT_HOM_FULL ", Sum(perm, i -> dec[i]*ScalarProduct(T, irr[i], St)), "\n");
Print("RESULT_SYLOW3_ID ", IdGroup(S3), "\n");
Print("RESULT_ST_REGULAR_ON_SYLOW3 ", regular, "\n");
Print("RESULT_HOM_SYLOW3 ", HomEmb(S3)[2], "\n");
Print("RESULT_EMBED_SYLOW3 ", HomEmb(S3)[3], "\n");
Print("RESULT_SYLOW3_ORBITS_ON_40 ", HomEmb(S3)[4], " TRIVIAL_IN_ST ", HomEmb(S3)[5], "\n");
Print("RESULT_N_CLASSES ", Length(rows), "\n");
Print("RESULT_N_HOM_NONZERO ", Number(rows, r -> r[2] <> 0), "\n");
Print("RESULT_N_EMBED ", Length(emb), "\n");
Print("RESULT_MAX_ORDER_EMBED ", Maximum(List(emb, r -> r[1])), "\n");
Print("RESULT_MIN_ORDER_NOEMBED ", Minimum(List(noemb, r -> r[1])), "\n");
Print("RESULT_N_NOEMBED ", Length(noemb), "\n");
Print("RESULT_N_NOEMBED_EXPLAINED_BY_ORBITS ", Length(orbExplained), "\n");
Print("RESULT_NOEMBED_NEEDING_OTHER_IRREPS ", List(orbUnexplained, r -> [r[1], r[6]]), "\n");
Print("RESULT_BURNSIDE_MISMATCHES ", Length(bad), "\n");
Print("RESULT_MAXIMAL_ORDERS_AND_EMBED ", List(maxes, M -> [Size(M), HomEmb(M)[3]]), "\n");
Print("RESULT_ORDER27_ROWS ", List(h27, r -> [r[6], r[2], r[3], r[4], r[5]]), "\n");
Print("RESULT_HOM_FULL_ZERO_BUT_ALL_PROPER_NONZERO ",
      ForAll(Filtered(rows, r -> r[1] < 25920), r -> r[2] <> 0) and HomEmb(G)[2] = 0, "\n");

# St restricted to every order-27 subgroup is exactly three copies of the regular character.
ThreeRegular := function(H)
  local rs, tH;
  rs := RestrictedClassFunction(St, H);
  tH := UnderlyingCharacterTable(rs);
  return ForAll(Irr(tH), c -> ScalarProduct(tH, rs, c) = 3*c[1]);
end;;
o27 := Filtered(reps, H -> Size(H) = 27);;
Print("RESULT_ST_ON_ORDER27_IS_THREE_REGULAR ", List(o27, ThreeRegular), "\n");
Print("RESULT_ORDER27_IDS ", List(o27, IdGroup), "\n");

# Holotrade's K81 = Reg(H27) x Reg(C3): H27 is extraspecial of order 27, C3 external.
Print("RESULT_H27xC3_IDS ", [IdGroup(DirectProduct(SmallGroup(27,3), CyclicGroup(3))),
                            IdGroup(DirectProduct(SmallGroup(27,4), CyclicGroup(3)))], "\n");
Print("RESULT_ORDER81_CLASSES ", Length(Filtered(reps, H -> Size(H) = 81)), "\n");
Print("PASS w33_pass11962_line_module_steinberg_hom\n");
QUIT;
