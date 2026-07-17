# Pass 222: the odd-q owner multiplicity is a regulus square torsor.
#
# Let V=F_q^2+F_q^2 carry the standard alternating form, q odd.  For every
# nonsquare d define the symplectic regular spread
#
#   Sigma_d = {Y} union {Gamma(a,b;d): a,b in F_q},
#   Gamma(a,b;d) = rowspace [ I | [[a,b],[b,d*a]] ].
#
# The determinant of the difference of two graph matrices is
# d*(a-a')^2-(b-b')^2, nonzero away from the origin because d is a
# nonsquare.  Thus Sigma_d is a spread.  All Sigma_d contain the regulus
#
#   R = {Y} union {Gamma(0,b;d): b in F_q},
#
# which is independent of d.  For the canonical ordered path
#
#   L=<e1,e4>, M=<e1,e2>, N=<e2,e3>,
#
# owner_Sigma_d(L)=owner_Sigma_d(N)=R.  The opposite ruling of R consists
# of T_[s:t]=< (s,t,0,0),(0,0,t,s) >.  Its alternating pairing is 2*s*t,
# so in odd characteristic exactly L and N are isotropic.  Hence N is the
# unique W(3,q) completion of the source L through the owner regulus.
#
# There are (q-1)/2 nonsquares.  Multiplication by nonzero squares acts
# simply transitively on them.  The diagonal symplectic map
# diag(r,1,r^-1,1), which fixes L,M,N, sends Sigma_d to Sigma_(d*r^2).
# Therefore the fibre over the canonical path is intrinsically the
# nonsquare coset, a torsor for (F_q^x)^2, and has size (q-1)/2.  PSp
# transitivity transports this description to every ordered nonlocal path.
#
# GAP verifies every finite-field, spread, regulus, owner, uniqueness, and
# transport identity at q=3,5,7,9,11,13, covering all four odd residue
# classes modulo 8 and both prime and proper-prime-power fields.

Read("analysis/w33_odd_q_shadow_common.g");

OUT := "data/w33_pass222_odd_q_regulus_square_torsor.json";;

AllSymplecticLines222 := function(field, form, points)
    local elements, coefficients, lines, pivotPair, freeSlots, column,
          assignments, assignment, row1, row2, slotId, slot, basis, line;
    elements := Elements(field);
    coefficients := NormedRowVectors(field^2);
    lines := [];
    for pivotPair in Combinations([1 .. 4], 2) do
        freeSlots := [];
        for column in Filtered([1 .. 4], c -> c > pivotPair[1]) do
            if column <> pivotPair[2] then Add(freeSlots, [1, column]); fi;
        od;
        for column in Filtered([1 .. 4], c -> c > pivotPair[2]) do
            Add(freeSlots, [2, column]);
        od;
        assignments := Tuples(elements, Length(freeSlots));
        for assignment in assignments do
            row1 := List([1 .. 4], ignored -> Zero(field));
            row2 := List([1 .. 4], ignored -> Zero(field));
            row1[pivotPair[1]] := One(field);
            row2[pivotPair[2]] := One(field);
            for slotId in [1 .. Length(freeSlots)] do
                slot := freeSlots[slotId];
                if slot[1] = 1 then
                    row1[slot[2]] := assignment[slotId];
                else
                    row2[slot[2]] := assignment[slotId];
                fi;
            od;
            if row1 * form * row2 = Zero(field) then
                basis := [row1, row2];
                line := Set(List(coefficients, coefficient ->
                    Position(points,
                        NormalizeProjective(field, coefficient * basis))));
                Add(lines, line);
            fi;
        od;
    od;
    return Set(lines);
end;;

BuildW3qIncidence := function(q)
    local field, form, points, lines;
    field := GF(q);
    form := StandardSymplecticForm(field);
    points := NormedRowVectors(field^4);
    # Enumerate the six RREF charts of Gr(2,4), then retain the isotropic
    # row spaces.  This is field-native at q=p^e and avoids constructing
    # thousands of redundant point transvections at q=13.
    lines := AllSymplecticLines222(field, form, points);
    return rec(
        q := q,
        field := field,
        form := form,
        points := points,
        lines := lines
    );
end;;

LineIdFromBasis := function(geometry, basis)
    local coefficients, line;
    coefficients := NormedRowVectors(geometry.field^2);
    line := Set(List(coefficients, coefficient -> Position(geometry.points,
        NormalizeProjective(geometry.field, coefficient * basis))));
    return Position(geometry.lines, line);
end;;

ParameterSpread := function(geometry, d)
    local field, elements, spread, a, b, basis, lineId;
    field := geometry.field;
    elements := Elements(field);
    spread := [];
    for a in elements do
        for b in elements do
            basis := [
                [One(field), Zero(field), a, b],
                [Zero(field), One(field), b, d * a]
            ];
            lineId := LineIdFromBasis(geometry, basis);
            if lineId = fail then
                Error("parameter graph is not a W(3,q) line");
            fi;
            AddSet(spread, lineId);
        od;
    od;
    basis := [
        [Zero(field), Zero(field), One(field), Zero(field)],
        [Zero(field), Zero(field), Zero(field), One(field)]
    ];
    AddSet(spread, LineIdFromBasis(geometry, basis));
    return spread;
end;;

OwnerSet222 := function(spread, lineId, lines)
    return Set(List(lines[lineId], point ->
        First(spread, ownerId -> point in lines[ownerId])));
end;;

CandidateRights222 := function(geometry, spread, left, middle)
    local ownerLeft, candidates, right;
    ownerLeft := OwnerSet222(spread, left, geometry.lines);
    candidates := [];
    for right in [1 .. Length(geometry.lines)] do
        if Length(Intersection(geometry.lines[middle],
                               geometry.lines[right])) = 1
           and Length(Intersection(geometry.lines[left],
                                   geometry.lines[right])) = 0
           and OwnerSet222(spread, right, geometry.lines) = ownerLeft then
            Add(candidates, right);
        fi;
    od;
    return candidates;
end;;

LinePermutation222 := function(geometry, pointPermutation)
    return PermList(List(geometry.lines, line -> Position(geometry.lines,
        Set(List(line, point -> point ^ pointPermutation)))));
end;;

JsonBool := function(value)
    if value then return "true"; fi;
    return "false";
end;;

BuildAnchor222 := function(q)
    local geometry, field, elements, nonzero, squares, nonsquares, spreads,
          e1, e2, e3, e4, left, middle, right, regulus, b,
          determinantAnisotropic, spreadCovers, commonRegulus, ownerRegulus,
          transversalParameters, transversalPairings,
          isotropicTransversalParameters, twoIsotropicTransversals,
          candidateUnique, d0, squareCoset, squareCosetExact, primitive,
          diagonal, pointPermutation, linePermutation, parameterImages,
          parameterAction, diagonalTransport, report;
    geometry := BuildW3qIncidence(q);
    field := geometry.field;
    elements := Elements(field);
    nonzero := Filtered(elements, x -> x <> Zero(field));
    squares := Set(List(nonzero, x -> x^2));
    nonsquares := Difference(nonzero, squares);
    spreads := List(nonsquares, d -> ParameterSpread(geometry, d));

    e1 := [One(field), Zero(field), Zero(field), Zero(field)];
    e2 := [Zero(field), One(field), Zero(field), Zero(field)];
    e3 := [Zero(field), Zero(field), One(field), Zero(field)];
    e4 := [Zero(field), Zero(field), Zero(field), One(field)];
    left := LineIdFromBasis(geometry, [e1, e4]);
    middle := LineIdFromBasis(geometry, [e1, e2]);
    right := LineIdFromBasis(geometry, [e2, e3]);

    # R is independent of d: a=0 gives the q finite members, plus Y.
    regulus := [];
    for b in elements do
        AddSet(regulus, LineIdFromBasis(geometry, [
            [One(field), Zero(field), Zero(field), b],
            [Zero(field), One(field), b, Zero(field)]
        ]));
    od;
    AddSet(regulus, LineIdFromBasis(geometry, [e3, e4]));

    determinantAnisotropic := ForAll(nonsquares, d ->
        ForAll(Filtered(Tuples(elements, 2), pair ->
            pair <> [Zero(field), Zero(field)]), pair ->
                d * pair[1]^2 - pair[2]^2 <> Zero(field)));
    spreadCovers := ForAll(spreads, spread ->
        Length(spread) = q^2 + 1
        and Set(Concatenation(geometry.lines{spread}))
            = [1 .. Length(geometry.points)]
        and ForAll(Combinations(spread, 2), pair ->
            Intersection(geometry.lines[pair[1]],
                         geometry.lines[pair[2]]) = []));
    commonRegulus := ForAll(spreads, spread -> IsSubset(spread, regulus))
        and ForAll(Combinations(spreads, 2), pair ->
            Intersection(pair[1], pair[2]) = regulus);
    ownerRegulus := ForAll(spreads, spread ->
        OwnerSet222(spread, left, geometry.lines) = regulus
        and OwnerSet222(spread, right, geometry.lines) = regulus);

    transversalParameters := NormedRowVectors(field^2);
    transversalPairings := List(transversalParameters, parameter ->
        [parameter,
         [parameter[1], parameter[2], Zero(field), Zero(field)]
             * geometry.form
             * [Zero(field), Zero(field),
                parameter[2], parameter[1]]]);
    isotropicTransversalParameters := List(
        Filtered(transversalPairings, row -> row[2] = Zero(field)),
        row -> row[1]);
    twoIsotropicTransversals := Length(isotropicTransversalParameters) = 2
        and Set(isotropicTransversalParameters)
            = Set([[One(field), Zero(field)],
                   [Zero(field), One(field)]]);
    candidateUnique := ForAll(spreads, spread ->
        CandidateRights222(geometry, spread, left, middle) = [right]);

    d0 := nonsquares[1];
    squareCoset := Set(List(squares, square -> d0 * square));
    squareCosetExact := squareCoset = Set(nonsquares)
        and Length(squares) = (q - 1) / 2
        and Length(Set(spreads)) = (q - 1) / 2;

    primitive := PrimitiveElement(field);
    diagonal := DiagonalMat([
        primitive, One(field), primitive^-1, One(field)
    ]);
    pointPermutation := ProjectivePermutation(
        geometry.points, field, diagonal);
    linePermutation := LinePermutation222(geometry, pointPermutation);
    parameterImages := List([1 .. Length(nonsquares)], dId ->
        Position(spreads,
            Set(List(spreads[dId], lineId -> lineId ^ linePermutation))));
    parameterAction := PermList(parameterImages);
    diagonalTransport :=
        diagonal * geometry.form * TransposedMat(diagonal) = geometry.form
        and left ^ linePermutation = left
        and middle ^ linePermutation = middle
        and right ^ linePermutation = right
        and ForAll([1 .. Length(nonsquares)], dId ->
            nonsquares[dId ^ parameterAction]
                = nonsquares[dId] * primitive^2)
        and Order(parameterAction) = (q - 1) / 2
        and Length(Orbits(Group(parameterAction),
                           [1 .. Length(nonsquares)])) = 1;

    report := rec(
        q := q,
        pointCount := Length(geometry.points),
        lineCount := Length(geometry.lines),
        parameterCount := Length(nonsquares),
        regulusSize := Length(regulus),
        isotropicTransversalCount :=
            Length(isotropicTransversalParameters),
        candidateCount := Length(CandidateRights222(
            geometry, spreads[1], left, middle)),
        transportOrder := Order(parameterAction)
    );
    return rec(
        report := report,
        parameterCount := Length(nonsquares) = (q - 1) / 2,
        determinantAnisotropic := determinantAnisotropic,
        spreadCovers := spreadCovers,
        commonRegulus := commonRegulus,
        ownerRegulus := ownerRegulus,
        twoIsotropicTransversals := twoIsotropicTransversals,
        candidateUnique := candidateUnique,
        squareCosetExact := squareCosetExact,
        diagonalTransport := diagonalTransport
    );
end;;

qValues := [3, 5, 7, 9, 11, 13];;
anchorResults := List(qValues, BuildAnchor222);;
reports := List(anchorResults, result -> result.report);;
allParameterCounts := ForAll(anchorResults, result -> result.parameterCount);;
allDeterminantsAnisotropic := ForAll(anchorResults,
    result -> result.determinantAnisotropic);;
allSpreadsPartitionPoints := ForAll(anchorResults,
    result -> result.spreadCovers);;
allCommonReguli := ForAll(anchorResults, result -> result.commonRegulus);;
allOwnerSetsAreRegulus := ForAll(anchorResults,
    result -> result.ownerRegulus);;
allOppositeRulingsHaveTwoIsotropicLines := ForAll(anchorResults,
    result -> result.twoIsotropicTransversals);;
allCandidatesUnique := ForAll(anchorResults, result -> result.candidateUnique);;
allSquareCosetsSimplyTransitive := ForAll(anchorResults,
    result -> result.squareCosetExact);;
allDiagonalTransport := ForAll(anchorResults,
    result -> result.diagonalTransport);;

checks := rec();;
checks.odd_anchor_parameter_counts_are_qminus1_over2 := allParameterCounts;
checks.determinant_difference_is_anisotropic :=
    allDeterminantsAnisotropic;
checks.every_parameter_family_is_a_spread := allSpreadsPartitionPoints;
checks.pairwise_intersection_is_the_common_regulus := allCommonReguli;
checks.endpoint_owner_sets_are_exactly_the_regulus :=
    allOwnerSetsAreRegulus;
checks.opposite_regulus_has_exactly_two_isotropic_transversals :=
    allOppositeRulingsHaveTwoIsotropicLines;
checks.unique_other_isotropic_transversal_is_the_owner_completion :=
    allCandidatesUnique;
checks.nonsquare_parameters_are_a_square_group_torsor :=
    allSquareCosetsSimplyTransitive;
checks.path_fixing_diagonal_realizes_square_transport :=
    allDiagonalTransport;
checks.anchor_set_covers_all_odd_mod8_classes_and_extension_field :=
    Set(List(qValues, q -> q mod 8)) = [1, 3, 5, 7]
    and 9 in qValues;

checkNames := RecNames(checks);;
allPass := ForAll(checkNames, name -> checks.(name));;
statusText := "FAIL";;
if allPass then statusText := "PASS"; fi;

stream := OutputTextFile(OUT, false);;
SetPrintFormattingStatus(stream, false);;
Emit := function(arg)
    local item;
    for item in arg do WriteAll(stream, String(item)); od;
end;;

Emit("{\n");
Emit("  \"schema\": \"w33.pass222.odd_q_regulus_square_torsor.gap.v1\",\n");
Emit("  \"producer\": \"GAP ", GAPInfo.Version, "\",\n");
Emit("  \"status\": \"", statusText, "\",\n");
Emit("  \"theorem\": {\n");
Emit("    \"spread_family\": \"Sigma_d={Y} union {graph [[a,b],[b,d*a]]}; d ranges over nonsquares\",\n");
Emit("    \"spread_test\": \"det(A_d(a,b)-A_d(a',b'))=d(a-a')^2-(b-b')^2 is nonzero off zero because d is nonsquare\",\n");
Emit("    \"common_regulus\": \"R={Y} union {Gamma(0,b): b in F_q}; every two distinct Sigma_d meet exactly in R\",\n");
Emit("    \"canonical_path\": \"L=<e1,e4>, M=<e1,e2>, N=<e2,e3>; owner(L)=owner(N)=R\",\n");
Emit("    \"unique_completion\": \"the opposite-regulus transversal T_[s:t] has symplectic pairing 2st, so for q odd only L and N are isotropic\",\n");
Emit("    \"fibre\": \"nonsquares form a principal homogeneous space for (F_q^x)^2, hence every ordered nonlocal path has (q-1)/2 regular-spread owners\",\n");
Emit("    \"transport\": \"diag(r,1,r^-1,1) fixes L,M,N and sends Sigma_d to Sigma_(d*r^2)\",\n");
Emit("    \"q3_exception\": \"F_3 has one nonsquare, so and only so the regular owner carrier is a bijection\"\n");
Emit("  },\n");
Emit("  \"anchors\": [\n");
for reportId in [1 .. Length(reports)] do
    report := reports[reportId];
    Emit("    {\"q\":", report.q,
        ",\"points\":", report.pointCount,
        ",\"lines\":", report.lineCount,
        ",\"nonsquare_parameters\":", report.parameterCount,
        ",\"common_regulus_lines\":", report.regulusSize,
        ",\"isotropic_opposite_transversals\":",
            report.isotropicTransversalCount,
        ",\"owner_completion_candidates\":", report.candidateCount,
        ",\"square_transport_order\":", report.transportOrder, "}");
    if reportId < Length(reports) then Emit(","); fi;
    Emit("\n");
od;
Emit("  ],\n");
Emit("  \"literature\": {\"coordinate_framework\": \"Ball-Zieve, Symplectic spreads and permutation polynomials, arXiv:0810.2839\"},\n");
Emit("  \"proof_boundary\": \"The all-odd-q statement is the displayed elementary coordinate proof: nonsquare determinant anisotropy, the 2st opposite-regulus test, and square transport. GAP exhausts those identities at q=3,5,7,9,11,13; it is not using finite anchors as a substitute for the quantified algebraic argument.\",\n");
Emit("  \"checks\": {\n");
for checkId in [1 .. Length(checkNames)] do
    Emit("    \"", checkNames[checkId], "\": ",
        JsonBool(checks.(checkNames[checkId])));
    if checkId < Length(checkNames) then Emit(","); fi;
    Emit("\n");
od;
Emit("  }\n");
Emit("}\n");
CloseStream(stream);

Print("Pass 222 odd-q regulus square torsor: ", statusText, " (",
    Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
    " checks)\n");
for report in reports do
    Print("q=", report.q, ": fibre/regulus/isotropic-transversals = ",
        report.parameterCount, "/", report.regulusSize, "/",
        report.isotropicTransversalCount, "\n");
od;
if not allPass then FORCE_QUIT_GAP(1); fi;
