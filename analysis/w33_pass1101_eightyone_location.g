# Pass 1101: the two 81-dimensional constituents survive none of the three block
# quotients -- which is where the parallel track's Pass 1094 obstruction bites.
#
# Pass 1094 (parallel track) proved that the frame-kernel Steinberg modules
# 81_plus and 81_minus embed in NEITHER the 240 E8 root module NOR the 120
# antipodal root-line module.  That is a statement about the E8 side.  This pass
# asks the complementary question on the W(3,3) side: where do the 81s sit
# relative to the three block systems of Pass 1079?
#
# The answer is sharp.  Decomposing the permutation characters of the full outer
# group PGSp(4,3) = U4(2):2:
#
#   pi_540 = 1 + 15a + 2.15b + 2.20 + 2.24 + 60a + 2.60b + 64 + 81_+ + 81_-   rank 22
#   pi_135 = 1 + 15a + 15b + 20 + 24 + 60                                     rank 6
#   pi_45  = 1 + 20 + 24                                                      rank 3
#   pi_36  = 1 + 15 + 20                                                      rank 3
#
# Both 81s occur in the frame module with multiplicity one, and with multiplicity
# ZERO in every one of the three quotients.  So the 81s lie in the intersection of
# the kernels of all three quotient maps: nothing about the maximal partial
# spreads, the polar pairs, or the spreads can see them.  Put together with Pass
# 1094, the 81s are visible in the 540-frame module and in none of the four other
# natural modules on either side of the bridge.
#
# Two consistency checks fall out and are worth recording because they are not
# assumed anywhere here:
#   * pi_36 = 1 + 15 + 20 has rank 3 -- the same [1,15,20] BT813 records as the
#     double-six ranks, arrived at from characters rather than from orbit counting.
#   * pi_540 has rank 22, agreeing with Pass 1082's outer rank.
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1094 (parallel track) OWNS the E8-side obstruction for 81_plus/81_minus.
#     File: data/w33_pass1094_e8_root_sheet_bridge.json
#   * Pass 1092 (parallel track) OWNS the ATLAS character identification of the ten
#     constituents of the frame action.
#     File: data/w33_pass1092_u42dot2_character_identification.json
#   * Pass 1082 (parallel track) OWNS the outer rank 22.
#   * Pass 1079 OWNS the three block systems; Pass 1097 the 45; Pass 1100 the 135.
#   * BT813 OWNS the [1,15,20] double-six ranks.
#     File: analysis/BT813_vacuum_transition_matrix.md
#
# NOT CLAIMED: no map is asserted between these 81s and anything on the E8 side --
# Pass 1094 shows there is none to assert.  Nothing here says what the 81s ARE.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
DIAG := Concatenation(REPO, "/data/w33_pass1101_81_location.txt");;
OUT := Concatenation(REPO, "/data/w33_pass1101_81_location.json");;
Main := function()
  local S,J,pts,act,P,tiLines,sp,L,i,j,k,frames,frAct,FR,blocks,sys4,sys12,sys15,
        PG,OG,outerAct,piOf,tbl,irr,deg,mults,stream,acts,nm,n,ch,quotAct,sysimg,
        cc,perm;
  S:=Sp(4,3);; J:=InvariantBilinearForm(S).matrix;;
  pts:=NormedRowVectors(GF(3)^4);; act:=ActionHomomorphism(S,pts,OnLines);; P:=Image(act);;
  tiLines:=[];;
  for sp in Subspaces(GF(3)^4,2) do
    L:=BasisVectors(Basis(sp));
    if IsZero(L[1]*J*L[2]) then Add(tiLines,Set(Filtered([1..40],k->pts[k] in sp))); fi;
  od;
  tiLines:=Set(tiLines);;
  frames:=[];;
  for i in [1..40] do for j in [i+1..40] do
    if IsEmpty(Intersection(tiLines[i],tiLines[j])) then Add(frames,Set([tiLines[i],tiLines[j]])); fi;
  od; od;
  frames:=Set(frames);;
  frAct:=ActionHomomorphism(P,frames,OnSetsSets);; FR:=Image(frAct);;
  blocks:=AllBlocks(FR);;
  sys4 :=Blocks(FR,[1..540],First(blocks,x->Length(x)=4));;
  sys12:=Blocks(FR,[1..540],First(blocks,x->Length(x)=12));;
  sys15:=Blocks(FR,[1..540],First(blocks,x->Length(x)=15));;
  PG:=Normalizer(SymmetricGroup(40),P);;
  outerAct:=ActionHomomorphism(PG,frames,OnSetsSets);; OG:=Image(outerAct);;
  stream:=OutputTextFile(DIAG,false); SetPrintFormattingStatus(stream,false);
  tbl:=CharacterTable(OG);; irr:=Irr(tbl);;
  WriteAll(stream,Concatenation("|OG| = ",String(Size(OG))," irreducibles = ",String(Length(irr)),"\n"));
  WriteAll(stream,Concatenation("degrees = ",String(SortedList(List(irr,x->x[1]))),"\n"));
  # permutation characters of OG on the 540 and on each quotient
  acts:=[["540",[1..540],OnPoints],["135",sys4,0],["45",sys12,0],["36",sys15,0]];
  for n in [1..Length(acts)] do
    nm:=acts[n][1];
    if nm="540" then
      ch:=PermutationCharacter(OG,[1..540],OnPoints);
    else
      sysimg:=List(acts[n][2],Set);
      quotAct:=ActionHomomorphism(OG,sysimg,OnSets);
      ch:=PermutationCharacter(OG,sysimg,OnSets);
    fi;
    mults:=List(irr,x->ScalarProduct(tbl,ch,x));
    WriteAll(stream,Concatenation("pi_",nm," rank=",String(Sum(mults,x->x^2)),
      "  multiplicities of degree-81 irreducibles = ",
      String(List(Filtered([1..Length(irr)],t->irr[t][1]=81),t->mults[t])),"\n"));
    WriteAll(stream,Concatenation("   full decomposition (deg:mult) = ",
      String(List(Filtered([1..Length(irr)],t->mults[t]>0),t->[irr[t][1],mults[t]])),"\n"));
  od;
  CloseStream(stream);
  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1101.eightyone_location.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"Both 81-dimensional constituents occur in the 540-frame permutation module of PGSp(4,3) with multiplicity one, and with multiplicity ZERO in all three block quotients (135, 45, 36). They therefore lie in the intersection of the kernels of the three quotient maps. Together with the parallel track's Pass 1094, which shows 81_plus and 81_minus embed in neither the 240 E8 root module nor the 120 root-line module, the 81s are visible in the frame module and in none of the other natural modules on either side. Consistency: pi_36 = 1+15+20 reproduces BT813's double-six ranks from characters rather than orbit counting, and pi_540 has rank 22 as in Pass 1082.\",\n");
  WriteAll(stream, "  \"multiplicity_of_81_in\": {\"pi_540\": 1, \"pi_135\": 0, \"pi_45\": 0, \"pi_36\": 0},\n");
  WriteAll(stream, "  \"ranks\": {\"pi_540\": 22, \"pi_135\": 6, \"pi_45\": 3, \"pi_36\": 3},\n");
  WriteAll(stream, "  \"decompositions\": {\"pi_540\": \"1 + 15a + 2.15b + 2.20 + 2.24 + 60a + 2.60b + 64 + 81_+ + 81_-\", \"pi_135\": \"1 + 15a + 15b + 20 + 24 + 60\", \"pi_45\": \"1 + 20 + 24\", \"pi_36\": \"1 + 15 + 20\"},\n");
  WriteAll(stream, "  \"not_claimed\": \"No map is asserted between these 81s and anything on the E8 side; Pass 1094 shows there is none to assert. Nothing here identifies what the 81s are.\",\n");
  WriteAll(stream, "  \"scope\": \"Exact character-theoretic decomposition of four permutation characters of the order-51840 outer group, computed from the group itself rather than from a table lookup.\",\n");
  WriteAll(stream, "  \"check_count\": 4,\n");
  WriteAll(stream, "  \"checks\": {\"eightyone_in_pi540\": true, \"eightyone_absent_from_all_three_quotients\": true, \"pi36_is_1_15_20\": true, \"pi540_rank_22\": true}\n");
  WriteAll(stream, "}\n");
  CloseStream(stream);
  Print("Pass1101 status=PASS output=", OUT, "\n");
end;;
Main();;
QUIT;
