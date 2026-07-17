# Pass 373: the oriented triangle-boundary image in the 240-edge carrier is
# an exact [240,120,3]_3 code.  Its parity-check columns are nonzero and
# projectively distinct, so all 480 nonzero single-edge errors have distinct
# syndromes and the complete radius-one MLUT has exactly 481 entries.

OUT373 := "data/w33_pass373_triangle_boundary_mlut.json";;

NormalizeProjective368 := function(vector)
  local position;
  position := PositionProperty(vector, entry -> not IsZero(entry));
  return Inverse(vector[position]) * vector;
end;;

Symplectic368 := function(left,right)
  return left[1]*right[3]-left[3]*right[1]
       + left[2]*right[4]-left[4]*right[2];
end;;

Bool368 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Assert368 := function(label,condition)
  if not condition then
    Error(Concatenation("Pass373 assertion failed: ",label));
  fi;
end;;

Main368 := function()
  local field,zero,one,raw,points,edges,triangles,i,j,k,triangle,row,
        boundaryRows,basis,parityRows,parityColumns,normalizedColumns,
        radiusOneSyndromes,orthogonality,checks,names,name,stream;

  field := GF(3);
  zero := Zero(field);
  one := One(field);
  raw := Tuples([zero,one,2*one],4);
  points := Set(List(Filtered(raw,vector ->
    vector<>[zero,zero,zero,zero]),NormalizeProjective368));

  edges := [];
  for i in [1..Length(points)] do
    for j in [i+1..Length(points)] do
      if IsZero(Symplectic368(points[i],points[j])) then
        Add(edges,[i,j]);
      fi;
    od;
  od;

  triangles := [];
  for i in [1..Length(points)] do
    for j in [i+1..Length(points)] do
      if [i,j] in edges then
        for k in [j+1..Length(points)] do
          if [i,k] in edges and [j,k] in edges then
            Add(triangles,[i,j,k]);
          fi;
        od;
      fi;
    od;
  od;

  boundaryRows := [];
  for triangle in triangles do
    row := List([1..Length(edges)],unused -> zero);
    row[Position(edges,[triangle[1],triangle[2]])] := one;
    row[Position(edges,[triangle[1],triangle[3]])] := -one;
    row[Position(edges,[triangle[2],triangle[3]])] := one;
    Add(boundaryRows,row);
  od;

  basis := BaseMat(boundaryRows);
  parityRows := NullspaceMat(TransposedMat(basis));
  parityColumns := List([1..Length(edges)],column ->
    List(parityRows,parityRow -> parityRow[column]));
  normalizedColumns := List(parityColumns,NormalizeProjective368);
  radiusOneSyndromes := Set(Concatenation(
    parityColumns,List(parityColumns,vector -> -vector)));
  orthogonality := basis*TransposedMat(parityRows);

  checks := rec();
  checks.w33_has_40_points := Length(points)=40;
  checks.w33_has_240_edges := Length(edges)=240;
  checks.clique_complex_has_160_triangles := Length(triangles)=160;
  checks.triangle_boundary_rank_is_120 := Length(basis)=120;
  checks.dual_parity_rank_is_120 := Length(parityRows)=120;
  checks.generator_and_parity_checks_are_orthogonal :=
    ForAll(Flat(orthogonality),IsZero);
  checks.no_zero_parity_check_column :=
    ForAll(parityColumns,column -> ForAny(column,entry -> not IsZero(entry)));
  checks.all_240_columns_are_projectively_distinct :=
    Length(Set(normalizedColumns))=240;
  checks.explicit_triangle_word_has_weight_three :=
    Minimum(List(boundaryRows,boundary ->
      Number(boundary,entry -> not IsZero(entry))))=3;
  checks.minimum_distance_is_exactly_three :=
    checks.no_zero_parity_check_column and
    checks.all_240_columns_are_projectively_distinct and
    checks.explicit_triangle_word_has_weight_three;
  checks.all_480_single_errors_have_distinct_nonzero_syndromes :=
    Length(radiusOneSyndromes)=480 and
    ForAll(radiusOneSyndromes,syndrome ->
      ForAny(syndrome,entry -> not IsZero(entry)));
  checks.complete_radius_one_mlut_has_481_entries :=
    Length(radiusOneSyndromes)+1=481;

  names := RecNames(checks);
  Assert368("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT373,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass373.triangle_boundary_mlut.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"code\": {\"object\":\"image of the oriented W33 triangle boundary map over GF(3)\",\"parameters\":\"[240,120,3]_3\",\"length\":240,\"dimension\":120,\"minimum_distance\":3},\n");
  WriteAll(stream,"  \"parity_certificate\": {\"rank\":120,\"nonzero_columns\":240,\"projective_column_classes\":240},\n");
  WriteAll(stream,"  \"decoder\": {\"correction_radius\":1,\"nonzero_single_error_syndromes\":480,\"complete_mlut_entries\":481},\n");
  WriteAll(stream,"  \"separation\": \"This [240,120,3]_3 classical boundary image is not itself the qutrit CSS code. The existing analysis/w33_css_exact_audit.py combines triangle and vertex checks and proves [[240,81,3]]_3 with d_X=3 and d_Z=4.\",\n");
  WriteAll(stream,"  \"boundary\": \"The certificate proves exact classical ternary code parameters and complete correction of one edge-symbol error; it does not by itself construct a quantum stabilizer code or a physical fault-tolerance threshold.\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool368(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);

  Print("Pass373 status=PASS checks=",Length(names)," code=[240,120,3]_3 mlut=481 output=",OUT373,"\n");
end;;

Main368();;
QUIT;
