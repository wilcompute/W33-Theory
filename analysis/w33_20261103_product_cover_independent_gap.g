# Independent GAP engine check; frozen native534-point and GF17 data.
# Regenerate the data with w33_20261103_product_cover_coupling_tradeoff.py.
w33Repo := GAPInfo.SystemEnvironment.W33_REPO;;
Read(Concatenation(w33Repo,"/data/w33_20261103_product_cover_gap_input.g"));;
w33L := Group(List(w33Raw{[1..6]}, p -> PermList(p{[1..54]})));;
w33K := Group(List(w33Raw, p -> PermList(List(p{[55..534]}, x -> x-54))));;
w33G := Group(List(w33Raw, PermList));;
if Size(w33L)<>30720 or Size(DerivedSubgroup(w33L))<>30720 then Error("signed perfect group check");fi;
if Size(w33K)<>46080 or Size(w33G)<>1415577600 then Error("paired group check");fi;
w33Core := PCore(w33K,2);;
if Size(w33Core)<>64 then Error("Clifford2-core check");fi;
w33Quotient := FactorGroup(w33K,w33Core);;
if Size(w33Quotient)<>720 or IsomorphismGroups(w33Quotient,SymmetricGroup(6))=fail then Error("S6 quotient check");fi;
w33F := GF(17);;
w33Matrices := List(w33Matrices, M -> List(M, row -> List(row, x -> x*One(w33F))));;
w33Columns := function(gens)
 local result,i,j,B;
 result:=[];
 for i in [1..4] do for j in [1..4] do
  B:=NullMat(4,4,w33F);B[i][j]:=One(w33F);
  Add(result,Concatenation(List(gens,U -> Flat(TransposedMat(U)*B*U-B))));
 od;od;
 return result;
end;;
w33OldNullity:=16-RankMat(w33Columns(w33Matrices{[1..6]}));;
w33NewNullity:=16-RankMat(w33Columns(w33Matrices));;
if w33OldNullity<>1 or w33NewNullity<>0 then Error("bilinear dimension check");fi;
PrintTo(Concatenation(w33Repo,"/data/w33_20261103_product_cover_gap_verification.json"),
 "{\n  \"status\": \"PASS_INDEPENDENT_GAP_PRODUCT_COVER\",\n  \"signed_order\": ",Size(w33L),
 ",\n  \"signed_derived_order\": ",Size(DerivedSubgroup(w33L)),",\n  \"spinor_order\": ",Size(w33K),
 ",\n  \"paired_order\": ",Size(w33G),",\n  \"spinor_2_core_order\": ",Size(w33Core),
 ",\n  \"spinor_quotient_is_S6\": true,\n  \"old_bilinear_nullity\": ",w33OldNullity,
 ",\n  \"new_bilinear_nullity\": ",w33NewNullity,",\n  \"GAP_version\": \"",GAPInfo.Version,"\"\n}\n");
QUIT;
