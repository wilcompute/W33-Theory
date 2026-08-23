# Pass7589-7596: produce an actual fixed-point-free order-9 Co0 matrix witness.
# The companion Python pass computes the Smith form of I-g.  This directly audits
# whether determinant 729 really means an elementary F3^6 quotient.
LoadPackage("atlasrep");;
REPO:=GAPInfo.SystemEnvironment.W33_REPO;;
OUT:=Concatenation(REPO,"/data/PART_W33_PASS7589_7596_LEECH_ORDER9_MATRIX.txt");;
A:=function(msg,c) if not c then Error(Concatenation("Pass7589 failed: ",msg)); fi; end;;

r:=AtlasGenerators("2.Co1",9);;
A("Atlas integral Co0 representation",r<>fail);;
gens:=r.generators;; G:=Group(gens);; one:=One(G);; I:=IdentityMat(24);;
found:=false;;
for tries in [1..50000] do
  x:=Random(G);
  if x^9=one and x^3<>one and TraceMat(x)=-3 and DeterminantMat(I-x)=729 then
    found:=true;; break;
  fi;
od;
A("fixed-point-free order9 witness found",found);;
mat:=List(x,row->List(row,Int));;
PrintTo(OUT,mat,"\n");;
Print("PASS7589_GAP_STATUS=PASS\n");
Print("CO0_ORDER9_TRIES=",tries,"\n");
Print("CO0_ORDER9_TRACE=",TraceMat(x),"\n");
Print("CO0_ORDER9_DET_I_MINUS=",DeterminantMat(I-x),"\n");
Print("CO0_ORDER9_MATRIX_FILE=",OUT,"\n");
QUIT;
