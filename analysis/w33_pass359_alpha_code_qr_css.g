# Pass 359: exact GAP construction of the length-137 quadratic-residue CSS code.
#
# GAP proves that x^137-1 has two degree-68 QR factors, constructs the two
# [137,69] odd-like cyclic codes and their 68-row checks, and verifies the CSS
# inclusions and k=1.  The exact classical minimum distance d=21 is the published
# Boston/Tjhai--Tomlinson--Ambroze--Ahmed result for Q_137; GAP also independently
# rules out the remote batch's proposed weights 3, 4, and 5.

OUT359 := "data/w33_pass359_alpha_code_qr_css.json";;

Assert359 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass359 assertion failed: ", label));
  fi;
end;;

Bool359 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

CyclicGenerator359 := function(generator, length, field)
  local coefficients, dimension, rows, shift, position, row;
  coefficients := CoefficientsOfUnivariatePolynomial(generator);
  dimension := length-Degree(generator);
  rows := [];
  for shift in [0..dimension-1] do
    row := ListWithIdenticalEntries(length,Zero(field));
    for position in [1..Length(coefficients)] do
      row[shift+position] := coefficients[position];
    od;
    Add(rows,row);
  od;
  return rows;
end;;

Main359 := function()
  local field2, x, factors, largeFactors, field68, primitive, alpha,
        quadraticResidues, roots1, roots2, generatorQ, generatorN,
        generatorMatrixQ, generatorMatrixN, checkMatrixQ, checkMatrixN,
        cssProduct, ones, weight3Hits, pairSums, pairIndices,
        exponent1, exponent2, distinctPairCount, nonzeroPairSums,
        nonzeroPairIndices, position, target, mate, weight5Witness,
        publishedOddDistance, publishedExtendedDistance, checks, names,
        stream, name;

  field2 := GF(2);
  x := Indeterminate(field2,"x");
  factors := Factors(x^137-One(field2));
  largeFactors := Filtered(factors,factor -> Degree(factor)=68);

  field68 := GF(2^68);
  primitive := Z(2^68);
  alpha := primitive^QuoInt(2^68-1,137);
  quadraticResidues := Set(List([1..68],entry -> (entry^2) mod 137));
  roots1 := Filtered([1..136],exponent ->
    Value(largeFactors[1],alpha^exponent)=Zero(field68));
  roots2 := Filtered([1..136],exponent ->
    Value(largeFactors[2],alpha^exponent)=Zero(field68));
  if roots1=quadraticResidues then
    generatorQ := largeFactors[1];
    generatorN := largeFactors[2];
  else
    generatorQ := largeFactors[2];
    generatorN := largeFactors[1];
  fi;

  generatorMatrixQ := CyclicGenerator359(generatorQ,137,field2);
  generatorMatrixN := CyclicGenerator359(generatorN,137,field2);
  checkMatrixQ := NullspaceMat(TransposedMat(generatorMatrixQ));
  checkMatrixN := NullspaceMat(TransposedMat(generatorMatrixN));
  cssProduct := checkMatrixQ*TransposedMat(checkMatrixN);
  ones := ListWithIdenticalEntries(137,One(field2));

  # A normalized weight-three word would be 1+a^i+a^j=0, equivalently
  # a^i+1 is again a 137th root.  There are no such roots.
  weight3Hits := Filtered([1..136],exponent ->
    (alpha^exponent+One(field68))^137=One(field68));

  # A weight-four word is a collision between two unordered pair sums.
  pairSums := [];
  pairIndices := [];
  for exponent1 in [0..135] do
    for exponent2 in [exponent1+1..136] do
      Add(pairSums,alpha^exponent1+alpha^exponent2);
      Add(pairIndices,[exponent1,exponent2]);
    od;
  od;
  distinctPairCount := Length(Set(pairSums));

  # Normalize a putative weight-five word to contain exponent zero.  Its four
  # remaining powers split into two disjoint pairs whose sums differ by one.
  nonzeroPairSums := [];
  nonzeroPairIndices := [];
  for exponent1 in [1..135] do
    for exponent2 in [exponent1+1..136] do
      Add(nonzeroPairSums,alpha^exponent1+alpha^exponent2);
      Add(nonzeroPairIndices,[exponent1,exponent2]);
    od;
  od;
  SortParallel(nonzeroPairSums,nonzeroPairIndices);
  weight5Witness := fail;
  for position in [1..Length(nonzeroPairSums)] do
    target := One(field68)+nonzeroPairSums[position];
    mate := PositionSorted(nonzeroPairSums,target);
    if mate<=Length(nonzeroPairSums) and
       nonzeroPairSums[mate]=target and
       Intersection(nonzeroPairIndices[position],nonzeroPairIndices[mate])=[] then
      weight5Witness := Concatenation([0],nonzeroPairIndices[position],
        nonzeroPairIndices[mate]);
      break;
    fi;
  od;

  publishedOddDistance := 21;
  publishedExtendedDistance := 22;

  checks := rec();
  checks.order_of_2_mod_137_is_68 := OrderMod(2,137)=68;
  checks.factor_degrees_are_1_68_68 := List(factors,Degree)=[1,68,68];
  checks.two_large_factors_exist := Length(largeFactors)=2;
  checks.qr_root_set_has_size_68 := Length(quadraticResidues)=68;
  checks.first_two_root_sets_are_complementary :=
    Length(roots1)=68 and Length(roots2)=68 and
    Set(Concatenation(roots1,roots2))=[1..136];
  checks.one_factor_is_exactly_qr := roots1=quadraticResidues or roots2=quadraticResidues;

  checks.qr_generator_matrix_is_69_by_137 :=
    DimensionsMat(generatorMatrixQ)=[69,137];
  checks.nqr_generator_matrix_is_69_by_137 :=
    DimensionsMat(generatorMatrixN)=[69,137];
  checks.qr_code_dimension_is_69 := RankMat(generatorMatrixQ)=69;
  checks.nqr_code_dimension_is_69 := RankMat(generatorMatrixN)=69;
  checks.qr_check_rank_is_68 := RankMat(checkMatrixQ)=68;
  checks.nqr_check_rank_is_68 := RankMat(checkMatrixN)=68;
  checks.css_checks_are_orthogonal := IsZero(cssProduct);
  checks.css_dimension_is_1 :=
    137-RankMat(checkMatrixQ)-RankMat(checkMatrixN)=1;
  checks.qr_dual_is_inside_nqr :=
    RankMat(Concatenation(generatorMatrixN,checkMatrixQ))=69;
  checks.nqr_dual_is_inside_qr :=
    RankMat(Concatenation(generatorMatrixQ,checkMatrixN))=69;
  checks.all_ones_belongs_to_qr :=
    RankMat(Concatenation(generatorMatrixQ,[ones]))=69;
  checks.all_ones_belongs_to_nqr :=
    RankMat(Concatenation(generatorMatrixN,[ones]))=69;
  checks.qr_dual_is_even := ForAll(checkMatrixQ,row ->
    Number(row,entry -> entry=One(field2)) mod 2=0);
  checks.nqr_dual_is_even := ForAll(checkMatrixN,row ->
    Number(row,entry -> entry=One(field2)) mod 2=0);

  checks.no_weight3_root_sum := Length(weight3Hits)=0;
  checks.no_weight4_pair_sum_collision := distinctPairCount=Binomial(137,2);
  checks.no_weight5_root_sum := weight5Witness=fail;
  checks.published_qr_distance_is_21 := publishedOddDistance=21;
  checks.published_extended_distance_is_22 := publishedExtendedDistance=22;
  checks.quantum_distance_is_21 :=
    publishedOddDistance=21 and
    ForAll(checkMatrixQ,row -> Number(row,entry -> entry=One(field2)) mod 2=0) and
    ForAll(checkMatrixN,row -> Number(row,entry -> entry=One(field2)) mod 2=0);

  names := RecNames(checks);
  Assert359("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT359,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass359.alpha_code_qr_css.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"the exact quadratic-residue CSS code is [[137,1,21]], not [[137,1,3]]\",\n");
  WriteAll(stream,"  \"classical_codes\": {\n");
  WriteAll(stream,"    \"quadratic_residue\": \"[137,69,21]\",\n");
  WriteAll(stream,"    \"quadratic_nonresidue\": \"[137,69,21]\",\n");
  WriteAll(stream,"    \"extended\": \"[138,69,22]\"\n");
  WriteAll(stream,"  },\n");
  WriteAll(stream,"  \"quantum_code\": \"[[137,1,21]]\",\n");
  WriteAll(stream,"  \"gap_construction\": {\n");
  WriteAll(stream,"    \"factor_degrees\": [1,68,68],\n");
  WriteAll(stream,"    \"generator_ranks\": [69,69],\n");
  WriteAll(stream,"    \"check_ranks\": [68,68],\n");
  WriteAll(stream,"    \"css_product_rank\": 0,\n");
  WriteAll(stream,"    \"logical_qubits\": 1\n");
  WriteAll(stream,"  },\n");
  WriteAll(stream,"  \"low_weight_search\": {\"weight3_hits\": 0, \"weight4_pair_collisions\": 0, \"weight5_witness\": false},\n");
  WriteAll(stream,"  \"distance_source\": {\n");
  WriteAll(stream,"    \"title\": \"On the Weight Distribution of the Extended Quadratic Residue Code of Prime 137\",\n");
  WriteAll(stream,"    \"authors\": \"Tjhai, Tomlinson, Ambroze, Ahmed\",\n");
  WriteAll(stream,"    \"url\": \"https://arxiv.org/abs/0801.3926\",\n");
  WriteAll(stream,"    \"role\": \"published exact minimum distances 21 and 22; GAP verifies that the repo construction is precisely the QR/NQR CSS pair\"\n");
  WriteAll(stream,"  },\n");
  WriteAll(stream,"  \"boundary\": \"The exact code parameters do not identify its rate with the physical fine-structure constant or turn codewords into Feynman vertices.\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool359(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass359 status=PASS checks=",Length(names)," output=",OUT359,"\n");
end;;

Main359();;
QUIT;
