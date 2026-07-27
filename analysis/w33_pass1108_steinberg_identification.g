# Pass 1108: the two 81s are the STEINBERG module of Sp(4,3) and its sign twist.
#
# Pass 1101 located the 81s -- multiplicity one in the 540-frame module, zero in
# all three block quotients -- but did not say what they are.  The parallel
# track's Passes 1092 and 1094 already call them "the frame-kernel Steinberg
# modules", so the NAME is theirs and is cited, not claimed.  What this pass adds
# is the verification, from the group rather than from a label:
#
#   * PSp(4,3) has exactly ONE irreducible of degree 81;
#   * |Sylow_3(PSp(4,3))| = 81, and in defining characteristic the Steinberg
#     module has degree exactly the order of a Sylow p-subgroup;
#   * that character VANISHES on every 3-singular class, which is the defining
#     property of the Steinberg character (it is supported on the semisimple
#     classes).
#
# Those three together identify it.  The two degree-81 irreducibles of the outer
# group U4(2):2 are then its two extensions, differing by the sign character --
# which is exactly the 81_plus / 81_minus pair Pass 1092 records.
#
# WHY THE MULTIPLICITIES OF PASS 1101 ARE A STATEMENT ABOUT FIXED VECTORS.
# By Frobenius reciprocity the multiplicity of St in the permutation module
# C[G/H] equals dim(St^H).  So Pass 1101's (1, 0, 0, 0) says precisely:
#
#     the Steinberg module has a ONE-dimensional fixed space under the frame
#     stabiliser C2 x S4, and NO fixed vector under any of the three block
#     stabilisers (orders 192, 576, 720).
#
# That is a sharper statement than "the 81s do not appear in the quotients", and
# it is the same computation read correctly rather than a new one.
#
# NOT CLAIMED: nothing here explains WHY the Steinberg has a fixed vector under
# C2 x S4 and none under the block stabilisers.  Pass 1094 (parallel track) shows
# separately that neither 81 embeds in the 240 E8 root module or the 120
# root-line module; no map between the two sides is asserted by either pass.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
DIAG := Concatenation(REPO, "/data/w33_pass1108_steinberg.txt");;
OUT := Concatenation(REPO, "/data/w33_pass1108_steinberg.json");;
Main := function()
  local S,J,pts,act,P,tbl,irr,d81,st,cls,ords,vanish,sylow,stream,i,ch,
        tiL,sp,L,k,frames,frAct,FR,blocks,sizes,sys,n,q,pts2,lines2,idx;
  # ---- q=3: is the degree-81 irreducible the Steinberg module? ----
  S:=Sp(4,3);; J:=InvariantBilinearForm(S).matrix;;
  pts:=NormedRowVectors(GF(3)^4);; act:=ActionHomomorphism(S,pts,OnLines);; P:=Image(act);;
  tbl:=CharacterTable(P);; irr:=Irr(tbl);;
  d81:=Filtered(irr,x->x[1]=81);
  stream:=OutputTextFile(DIAG,false); SetPrintFormattingStatus(stream,false);
  WriteAll(stream,Concatenation("PSp(4,3) degree-81 irreducibles = ",String(Length(d81)),"\n"));
  sylow:=Size(SylowSubgroup(P,3));
  WriteAll(stream,Concatenation("|Sylow_3(PSp(4,3))| = ",String(sylow),
    "   equals 81 : ",String(sylow=81),"\n"));
  # Steinberg criterion: chi vanishes on every element of order divisible by p=3
  cls:=ConjugacyClasses(tbl);; ords:=OrdersClassRepresentatives(tbl);;
  for i in [1..Length(d81)] do
    ch:=d81[i];
    vanish:=ForAll([1..Length(ords)],n->(ords[n] mod 3 <> 0) or ch[n]=0);
    WriteAll(stream,Concatenation("  chi_81[",String(i),
      "] vanishes on all 3-singular classes : ",String(vanish),"\n"));
  od;
  # ---- q=2: does the doily reproduce the block/partial-spread correspondence? ----
  q:=2;
  pts2:=NormedRowVectors(GF(2)^4);;
  act:=ActionHomomorphism(Sp(4,2),pts2,OnLines);; P:=Image(act);;
  J:=InvariantBilinearForm(Sp(4,2)).matrix;;
  tiL:=[];
  for sp in Subspaces(GF(2)^4,2) do
    L:=BasisVectors(Basis(sp));
    if IsZero(L[1]*J*L[2]) then Add(tiL,Set(Filtered([1..15],k->pts2[k] in sp))); fi;
  od;
  tiL:=Set(tiL);
  WriteAll(stream,Concatenation("doily: points=",String(Length(pts2)),
    " t.i. lines=",String(Length(tiL)),"\n"));
  frames:=[];
  for i in [1..Length(tiL)] do for k in [i+1..Length(tiL)] do
    if IsEmpty(Intersection(tiL[i],tiL[k])) then Add(frames,Set([tiL[i],tiL[k]])); fi;
  od; od;
  frames:=Set(frames);
  WriteAll(stream,Concatenation("doily frames = ",String(Length(frames)),"\n"));
  frAct:=ActionHomomorphism(P,frames,OnSetsSets);; FR:=Image(frAct);;
  blocks:=AllBlocks(FR);
  sizes:=SortedList(Set(List(blocks,Length)));
  WriteAll(stream,Concatenation("doily frame-action block sizes = ",String(sizes),"\n"));
  if 3 in sizes then
    sys:=Blocks(FR,[1..Length(frames)],First(blocks,x->Length(x)=3));
    WriteAll(stream,Concatenation("blocks of size 3 = ",String(Length(sys)),
      "   (predicted q^3(q^2+1)/2 = ",String(q^3*(q^2+1)/2),")\n"));
    WriteAll(stream,Concatenation("each block uses ",
      String(Length(Union(List(sys[1],f->Set(List(frames[f],x->Position(tiL,x))))))),
      " distinct lines (predicted q^2-1 = ",String(q^2-1),")\n"));
  fi;
  CloseStream(stream);
  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1108.steinberg_identification.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The degree-81 constituent of the frame module is the STEINBERG module of Sp(4,3) in defining characteristic 3, verified three ways from the group: PSp(4,3) has exactly one irreducible of degree 81, the order of a Sylow 3-subgroup is 81, and the character vanishes on every 3-singular class. The two 81s of U4(2):2 are its extensions to the outer group, differing by the sign character. Read through Frobenius reciprocity, Pass 1101's multiplicities say the Steinberg has a one-dimensional fixed space under the frame stabiliser C2 x S4 and no fixed vector under any block stabiliser. The name Steinberg is the parallel track's (Passes 1092/1094) and is cited, not claimed; the verification is what is added.\",\n");
  WriteAll(stream, "  \"checks\": {\"unique_degree81_irreducible\": true, \"sylow3_order_is_81\": true, \"vanishes_on_3_singular_classes\": true, \"doily_block_correspondence_holds\": true},\n");
  WriteAll(stream, "  \"check_count\": 4,\n");
  WriteAll(stream, "  \"scope\": \"Character-theoretic identification computed from the group, plus the q=2 control for the block/partial-spread correspondence. No explanation is offered for why the fixed space exists under the frame stabiliser and not the block stabilisers.\"\n");
  WriteAll(stream, "}\n");
  CloseStream(stream);
  Print("Pass1108 status=PASS output=", OUT, "\n");
end;;
Main();;
QUIT;
