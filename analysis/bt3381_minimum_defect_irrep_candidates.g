# BT3381: classify the order-36 support stabilizer inside the W33 line parabolic
# and decompose the resulting degree-720 permutation characters.
LoadPackage("ctbllib");

JoinInts := function(values)
  return JoinStringsWithSeparator(List(values, String), ",");
end;

Main := function()
  local G, line, N, hom, subgroupClasses, edgeCandidates, records;
  local eclass, E, normals, U, two, H, pi, irr, dec, ids, degrees, mults;
  local key, seen, out, i;

  G := PSp(4,3);
  line := First(MaximalSubgroupClassReps(G), h ->
    Size(h)=648 and StructureDescription(h)="(C3 x C3 x C3) : S4");
  if line=fail then Error("line parabolic not found"); fi;
  N := FittingSubgroup(line);
  if Size(N)<>27 then Error("line radical order is not 27"); fi;
  hom := NaturalHomomorphismByNormalSubgroup(line,N);

  subgroupClasses := ConjugacyClassesSubgroups(line);
  edgeCandidates := Filtered(subgroupClasses, c ->
    Size(Representative(c))=108 and
    Size(Image(hom,Representative(c)))=4);
  if Length(edgeCandidates)=0 then Error("no order-108 edge stabilizer candidates"); fi;

  irr := Irr(G);
  records := [];
  seen := [];
  for eclass in edgeCandidates do
    E := Representative(eclass);
    normals := Filtered(NormalSubgroups(E), U -> Size(U)=9 and IsSubgroup(N,U));
    two := SylowSubgroup(E,2);
    if Size(two)<>4 then Error("edge Sylow-2 order is not four"); fi;
    for U in normals do
      H := Group(Concatenation(GeneratorsOfGroup(U),GeneratorsOfGroup(two)));
      if Size(H)=36 and IsSubgroup(E,H) then
        pi := InducedClassFunction(TrivialCharacter(H),G);
        dec := List(irr,chi->ScalarProduct(pi,chi));
        ids := Filtered([1..Length(dec)],i->dec[i]<>0);
        degrees := List(ids,i->irr[i][1]);
        mults := List(ids,i->dec[i]);
        key := Concatenation(StructureDescription(H),"|",JoinInts(degrees),"|",JoinInts(mults));
        if not key in seen then
          Add(seen,key);
          Add(records,[
            StructureDescription(E),
            StructureDescription(H),
            Size(Normalizer(G,H)),
            ScalarProduct(pi,pi),
            degrees,
            mults,
            ids
          ]);
        fi;
      fi;
    od;
  od;

  out := OutputTextFile("data/PART_BT3381_MINIMUM_DEFECT_IRREP_candidates.tsv",false);
  SetPrintFormattingStatus(out,false);
  PrintTo(out,"schema\tw33.bt3381.minimum_defect_irrep_candidates.v1\n");
  AppendTo(out,"group_order\t",Size(G),"\n");
  AppendTo(out,"line_structure\t",StructureDescription(line),"\n");
  AppendTo(out,"line_order\t",Size(line),"\n");
  AppendTo(out,"radical_structure\t",StructureDescription(N),"\n");
  AppendTo(out,"edge_candidate_classes\t",Length(edgeCandidates),"\n");
  AppendTo(out,"unique_character_candidates\t",Length(records),"\n");
  for i in [1..Length(records)] do
    AppendTo(out,"candidate\t",i,
      "\tedge=",records[i][1],
      "\tstabilizer=",records[i][2],
      "\tnormalizer_order=",records[i][3],
      "\tcharacter_norm=",records[i][4],
      "\tdegrees=",JoinInts(records[i][5]),
      "\tmultiplicities=",JoinInts(records[i][6]),
      "\tirr_indices=",JoinInts(records[i][7]),"\n");
  od;
  CloseStream(out);

  Print("BT3381 candidates=",Length(records)," edge_classes=",Length(edgeCandidates),"\n");
end;

Main();
QUIT;
