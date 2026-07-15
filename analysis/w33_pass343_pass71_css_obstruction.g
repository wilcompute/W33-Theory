# Pass 343: exact GAP audit of the old Pass 71 adjacency/complement CSS claim.
#
# For the W(3,3) collinearity adjacency matrix A over F_2, the proposed
# checks were H_X=A and H_Z=J-I-A.  The strongly regular relation gives
# A^2=0 mod 2, but A*H_Z^T=A rather than zero.  Thus this pair is not CSS
# and does not construct the advertised [[360,9,>=9]] extension.

OUT343 := "data/w33_pass343_pass71_css_obstruction.json";;

Assert343 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass343 assertion failed: ", label));
  fi;
end;;

Bool343 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

NormalizePoint343 := function(vector)
  local position, inverse;
  position := PositionProperty(vector, entry -> entry<>0);
  if vector[position]=1 then inverse:=1; else inverse:=2; fi;
  return List(vector, entry -> (entry*inverse) mod 3);
end;;

Symplectic343 := function(left, right)
  return (left[1]*right[3]-left[3]*right[1]
    +left[2]*right[4]-left[4]*right[2]) mod 3;
end;;

Main343 := function()
  local field, raw, points, dimension, adjacency, complement,
        row, column, product, zero, square, productWeight,
        edgeCount, nonedgeCount, checks, names, stream, name;

  field := GF(2);
  raw := Filtered(Tuples([0,1,2],4), vector -> ForAny(vector,entry -> entry<>0));
  points := Set(List(raw,NormalizePoint343));
  dimension := Length(points);

  adjacency := NullMat(dimension,dimension,field);
  for row in [1..dimension] do
    for column in [row+1..dimension] do
      if Symplectic343(points[row],points[column])=0 then
        adjacency[row][column] := One(field);
        adjacency[column][row] := One(field);
      fi;
    od;
  od;

  complement := NullMat(dimension,dimension,field);
  for row in [1..dimension] do
    for column in [1..dimension] do
      if row<>column and adjacency[row][column]=Zero(field) then
        complement[row][column] := One(field);
      fi;
    od;
  od;

  zero := NullMat(dimension,dimension,field);
  square := adjacency*adjacency;
  product := adjacency*TransposedMat(complement);
  productWeight := Sum(List(product, vector ->
    Number(vector, entry -> entry=One(field))));
  edgeCount := Sum(List(adjacency, vector ->
    Number(vector, entry -> entry=One(field))))/2;
  nonedgeCount := Sum(List(complement, vector ->
    Number(vector, entry -> entry=One(field))))/2;

  checks := rec();
  checks.projective_point_count_is_40 := dimension=40;
  checks.adjacency_is_40_by_40 := DimensionsMat(adjacency)=[40,40];
  checks.every_adjacency_row_has_weight_12 := ForAll(adjacency, vector ->
    Number(vector, entry -> entry=One(field))=12);
  checks.edge_count_is_240 := edgeCount=240;
  checks.every_complement_row_has_weight_27 := ForAll(complement, vector ->
    Number(vector, entry -> entry=One(field))=27);
  checks.nonedge_count_is_540 := nonedgeCount=540;
  checks.adjacency_square_is_zero_mod_2 := square=zero;
  checks.css_product_equals_adjacency := product=adjacency;
  checks.css_product_is_nonzero := product<>zero;
  checks.css_product_rank_is_16 := RankMat(product)=16;
  checks.css_product_weight_is_480 := productWeight=480;
  checks.proposed_css_condition_is_false := product<>zero;

  names := RecNames(checks);
  Assert343("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT343,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass343.pass71_css_obstruction.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"the Pass 71 adjacency/complement pair is not CSS: H_X H_Z^T = A, not zero\",\n");
  WriteAll(stream,"  \"field\": \"F2\",\n");
  WriteAll(stream,"  \"matrix_identity\": \"H_X H_Z^T = A\",\n");
  WriteAll(stream,"  \"css_condition_satisfied\": false,\n");
  WriteAll(stream,"  \"css_product_rank\": 16,\n");
  WriteAll(stream,"  \"css_product_weight\": 480,\n");
  WriteAll(stream,"  \"retracted_claim\": \"[[360,9,>=9]] from this base pair\",\n");
  WriteAll(stream,"  \"boundary\": \"row weights 12 and 27 are not code-distance lower bounds; no 360-dimensional extension is built here\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool343(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass343 status=PASS checks=",Length(names)," output=",OUT343,"\n");
end;;

Main343();;
QUIT;
