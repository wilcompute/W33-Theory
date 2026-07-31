# Pass 1341: genuine GAP/AtlasRep/Repsn comparison surface.
#
# The Python certificate freezes a literal rational 20-dimensional model for
# Atlas-standard generators c,d of W(E6)=U4(2).2. This GAP program independently
# affords every degree-20 Atlas character and freezes image sizes, generator
# orders, and CTblLib rows. Equality is character-level (basis independent),
# not a claim that two arbitrary afforded bases are byte-identical.
#
# Prior ownership: w33_pass1333_atlasrep_species20.g already certifies the
# [0,3,0] degree-20 multiplicity pattern on the selected 432 carrier. Pass 1341
# reuses that result and adds the exact frozen 25-class character match.

SizeScreen([10000,10000]);
Assert1341 := function(label, condition)
    if not condition then Error(Concatenation("Pass 1341 failed: ",label)); fi;
    Print("PASS: ",label,"\n");
end;

Assert1341("AtlasRep loaded",LoadPackage("atlasrep")=true);
Assert1341("CTblLib loaded",LoadPackage("ctbllib")=true);
Assert1341("TomLib loaded",LoadPackage("tomlib")=true);
Assert1341("Repsn loaded",LoadPackage("repsn")=true);

encodedWords1341 := [
    "(cdcdcddcdcdddcdd)^4",
    "(cdd)^4",
    "(cdcdcddcdcdddcdd)^2",
    "(cdcdd)^4",
    "(ccdcdddcddd)^2",
    "(cddcdcdddcdd)^2",
    "(cdd)^2",
    "cdcdcddcdcdddcdd",
    "(cd)^2",
    "(cdcdd)^2",
    "ccdcdddcddd",
    "cddcdcdddcdd",
    "(cdcdcdd)^2",
    "d",
    "cdcdd",
    "(ccdcdcddcdcdddcddcddcdcdddcdd)^3",
    "(cdcdddcdd)^3",
    "(cdcdcdd)^3",
    "dcdcdcdd",
    "ccdcdcddcdcdddcddcddcdcdddcdd",
    "dcdd",
    "cdcdddcdd",
    "cdd",
    "cd",
    "cdcdcdd"
];;
expectedTraceVector1341 := [
    20,4,4,2,5,-1,0,0,0,-2,1,1,1,-1,0,10,2,2,2,1,1,-1,0,0,-1
];;

EvaluateLetters1341 := function(letters,mats)
    local result,letter;
    result:=mats[1]^0;
    for letter in letters do
        if letter='c' then result:=result*mats[1];
        elif letter='d' then result:=result*mats[2];
        else Error("Pass 1341 encoded word has an unknown letter");
        fi;
    od;
    return result;
end;

EvaluateEncodedWord1341 := function(encoded,mats)
    local close,letters,exponent,base;
    if encoded[1]='(' then
        close:=Position(encoded,')');
        letters:=encoded{[2..close-1]};
        exponent:=IntChar(encoded[close+2])-IntChar('0');
    else
        letters:=encoded;
        exponent:=1;
    fi;
    base:=EvaluateLetters1341(letters,mats);
    return base^exponent;
end;

G:=AtlasGroup("U4(2).2");
Assert1341("Atlas group exists",G<>fail);
Assert1341("Atlas group order 51840",Size(G)=51840);

tbl:=CharacterTable("U4(2).2");;
irrTbl:=Irr(tbl);;
pos20:=Filtered([1..Length(irrTbl)],i->irrTbl[i][1]=20);;
Assert1341("three degree-20 CTblLib rows",Length(pos20)=3);
Assert1341("frozen 25-class row is CTblLib character 11",
    irrTbl[11]=expectedTraceVector1341 and 11 in pos20);

irrG:=Irr(G);;
pos20G:=Filtered([1..Length(irrG)],i->irrG[i][1]=20);;
Assert1341("three degree-20 Atlas-group rows",Length(pos20G)=3);

records:=[];;
for i in pos20G do
    rho:=IrreducibleAffordingRepresentation(irrG[i]);;
    Assert1341(Concatenation("affording representation ",String(i)),
        IsAffordingRepresentation(irrG[i],rho));
    mats:=List(GeneratorsOfGroup(G),g->Image(rho,g));;
    Assert1341(Concatenation("20x20 matrices ",String(i)),
        ForAll(mats,m->DimensionsMat(m)=[20,20]));
    wordTraces:=List(encodedWords1341,
        word->TraceMat(EvaluateEncodedWord1341(word,mats)));
    Add(records,rec(
        character_position:=i,
        image_order:=Size(Image(rho)),
        generator_orders:=List(mats,Order),
        product_order:=Order(mats[1]*mats[2]),
        traces:=List(mats,TraceMat),
        word_traces_match_frozen:=wordTraces=expectedTraceVector1341
    ));
od;
Assert1341("all degree-20 afforded images are faithful",
    ForAll(records,record->record.image_order=51840));
Assert1341("all afforded standard-generator orders are 2,9,10",
    ForAll(records,record->
        record.generator_orders=[2,9] and record.product_order=10));
Assert1341("unique afforded character matches the frozen 25-class row",
    List(Filtered(records,record->record.word_traces_match_frozen),
        record->record.character_position)=[11]);

tom:=TableOfMarks("U4(2).2");;
orders:=OrdersTom(tom);;
permchars:=PermCharsTom(tbl,tom);;
rows432:=Filtered([1..Length(orders)],i->orders[i]=120 and permchars[i][1]=432);;
rows480:=Filtered([1..Length(orders)],i->orders[i]=108 and permchars[i][1]=480);;
mult432:=List(rows432,i->List(pos20,j->ScalarProduct(permchars[i],irrTbl[j])));;
mult480:=List(rows480,i->List(pos20,j->ScalarProduct(permchars[i],irrTbl[j])));;
Assert1341("432 carrier has degree-20 multiplicity three",
    ForAny(mult432,x->SortedList(x)=[0,0,3]));
Assert1341("480 carrier has degree-20 multiplicity one",
    ForAny(mult480,x->SortedList(x)=[0,0,1]));

Print("RESULT degree20_table_positions=",pos20,"\n");
Print("RESULT afforded_records=",records,"\n");
Print("RESULT index432_records=",List([1..Length(rows432)],i->[rows432[i],mult432[i]]),"\n");
Print("RESULT index480_records=",List([1..Length(rows480)],i->[rows480[i],mult480[i]]),"\n");
Print("PASS 1341 COMPLETE\n");
QUIT_GAP(0);
