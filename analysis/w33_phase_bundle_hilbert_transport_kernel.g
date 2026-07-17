# Pass 63: GAP certificate for the W33 phase bundle.
#
# GAP does the finite geometry, the PSp(4,3) orbit/stabilizer computation, the
# scheduler label transport, and the exact cyclotomic qutrit eigenvectors.  The
# only Python expected around this file is a test harness that runs GAP and reads
# the JSON emitted here.

OUT := "data/w33_phase_bundle_hilbert_transport_kernel.json";;

Mod3 := function(n)
  return ((n mod 3) + 3) mod 3;
end;;

NormalizeVec := function(v)
  local vals, x, inv;
  vals := List(v, x -> Mod3(x));
  for x in vals do
    if x <> 0 then
      inv := 1;
      if x = 2 then
        inv := 2;
      fi;
      return List(vals, y -> Mod3(inv * y));
    fi;
  od;
  Error("zero vector has no projective representative");
end;;

BuildPoints := function()
  local pts, a, b, c, d, vec, nz;
  pts := [];
  for a in [0..2] do
    for b in [0..2] do
      for c in [0..2] do
        for d in [0..2] do
          vec := [a, b, c, d];
          nz := First([1..4], i -> vec[i] <> 0);
          if nz <> fail and vec[nz] = 1 then
            Add(pts, vec);
          fi;
        od;
      od;
    od;
  od;
  return pts;
end;;

AuditB := function(x, y)
  return Mod3(x[1] * y[2] - x[2] * y[1] + x[3] * y[4] - x[4] * y[3]);
end;;

SchedulerJ := function(x, y)
  return Mod3(x[1] * y[4] - x[2] * y[3] + x[3] * y[2] - x[4] * y[1]);
end;;

JoinInts := function(vals, sep)
  local out, i;
  if Length(vals) = 0 then
    return "";
  fi;
  out := String(vals[1]);
  for i in [2..Length(vals)] do
    out := Concatenation(out, sep, String(vals[i]));
  od;
  return out;
end;;

MakeLines := function(points, form)
  local lines, seen, i, j, a, b, line, image, key;
  lines := [];
  seen := [];
  for i in [1..Length(points) - 1] do
    for j in [i + 1..Length(points)] do
      if form(points[i], points[j]) = 0 then
        line := [];
        for a in [0..2] do
          for b in [0..2] do
            if a <> 0 or b <> 0 then
              image := NormalizeVec(
                List([1..4], k -> a * points[i][k] + b * points[j][k])
              );
              AddSet(line, Position(points, image));
            fi;
          od;
        od;
        key := JoinInts(line, "-");
        if not key in seen then
          Add(seen, key);
          Add(lines, line);
        fi;
      fi;
    od;
  od;
  Sort(lines);
  return lines;
end;;

AdjacencyFromLines := function(n, lines)
  local adj, line, i, j;
  adj := List([1..n], i -> List([1..n], j -> false));
  for line in lines do
    for i in [1..Length(line) - 1] do
      for j in [i + 1..Length(line)] do
        adj[line[i]][line[j]] := true;
        adj[line[j]][line[i]] := true;
      od;
    od;
  od;
  return adj;
end;;

CommonPerp := function(points, idxs, form)
  return Filtered(
    [1..Length(points)],
    p -> ForAll(idxs, i -> form(points[p], points[i]) = 0)
  );
end;;

CenterZeroGrounds := function(points, lines, form)
  local center, nb, nonn, grounds, triads, triple, pair, common, ground;
  center := 1;
  nb := Filtered([1..Length(points)], i -> i <> center and form(points[center], points[i]) = 0);
  nonn := Filtered([1..Length(points)], i -> i <> center and not i in nb);
  grounds := [];
  triads := [];
  for triple in Combinations(nonn, 3) do
    if ForAll(Combinations(triple, 2), pair -> form(points[pair[1]], points[pair[2]]) <> 0) then
      common := CommonPerp(points, triple, form);
      if Length(common) = 4 then
        Add(triads, [triple, common]);
        if ForAll(common, p -> p in nb) then
          ground := Set(Concatenation(triple, Difference(nb, common)));
          AddSet(grounds, ground);
        fi;
      fi;
    fi;
  od;
  return rec(grounds := grounds, triads := triads, nb := nb);
end;;

TransvectionPerm := function(points, v, form)
  local images, p, coeff, image;
  images := [];
  for p in points do
    coeff := form(p, v);
    image := NormalizeVec(List([1..4], k -> p[k] + coeff * v[k]));
    Add(images, Position(points, image));
  od;
  return PermList(images);
end;;

BuildAuditGroup := function(points)
  local gens, vectors, v;
  vectors := [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1]
  ];
  gens := [];
  for v in vectors do
    Add(gens, TransvectionPerm(points, v, AuditB));
  od;
  return Group(gens);
end;;

CenterOfLit := function(lit, lines)
  local fails, line, common, li;
  fails := [];
  for li in [1..Length(lines)] do
    line := lines[li];
    if Length(Intersection(line, lit)) <> 1 then
      Add(fails, li);
    fi;
  od;
  if Length(fails) <> 4 then
    return fail;
  fi;
  common := ShallowCopy(lines[fails[1]]);
  for li in fails{[2..Length(fails)]} do
    common := Intersection(common, lines[li]);
  od;
  if Length(common) <> 1 then
    return fail;
  fi;
  return common[1];
end;;

IncrementRelCounter := function(counter, relation, intersection)
  local row;
  for row in counter do
    if row[1] = relation and row[2] = intersection then
      row[3] := row[3] + 1;
      return;
    fi;
  od;
  Add(counter, [relation, intersection, 1]);
end;;

IncrementIntCounter := function(counter, key)
  local row;
  for row in counter do
    if row[1] = key then
      row[2] := row[2] + 1;
      return;
    fi;
  od;
  Add(counter, [key, 1]);
end;;

CounterValue := function(counter, key)
  local row;
  for row in counter do
    if row[1] = key then
      return row[2];
    fi;
  od;
  return 0;
end;;

GluingSpectrum := function(bundle, centers, adjacency)
  local spectrum, i, j, left, right, ca, cb, relation;
  spectrum := [];
  for i in [1..Length(bundle) - 1] do
    left := bundle[i];
    ca := centers[i];
    for j in [i + 1..Length(bundle)] do
      right := bundle[j];
      cb := centers[j];
      if ca = cb then
        relation := "same";
      elif adjacency[ca][cb] then
        relation := "collinear";
      else
        relation := "noncollinear";
      fi;
      IncrementRelCounter(spectrum, relation, Length(Intersection(left, right)));
    od;
  od;
  Sort(spectrum, function(a, b)
    if a[1] = b[1] then
      return a[2] < b[2];
    fi;
    return a[1] < b[1];
  end);
  return spectrum;
end;;

StarLines := function(lines, n)
  local star, li, p;
  star := List([1..n], i -> []);
  for li in [1..Length(lines)] do
    for p in lines[li] do
      Add(star[p], li);
    od;
  od;
  return star;
end;;

BacktrackMatching := function(star)
  local n, matched, used, recur;
  n := Length(star);
  matched := List([1..n], i -> 0);
  used := [];
  recur := function(pos)
    local center, line, where;
    if pos > n then
      return true;
    fi;
    center := pos;
    for line in star[center] do
      if not line in used then
        matched[center] := line;
        AddSet(used, line);
        if recur(pos + 1) then
          return true;
        fi;
        where := Position(used, line);
        if where <> fail then
          Remove(used, where);
        fi;
        matched[center] := 0;
      fi;
    od;
    return false;
  end;
  if not recur(1) then
    Error("no incidence-preserving point-to-line matching found");
  fi;
  return matched;
end;;

ScaleMat := function(s, M)
  return List(M, row -> List(row, x -> s * x));
end;;

MatPowSmall := function(M, n)
  local out, i;
  out := IdentityMat(Length(M));
  for i in [1..n] do
    out := out * M;
  od;
  return out;
end;;

SingleDisplacement := function(a, b, omega)
  local Xm, Zm, phase;
  Xm := [[0, 0, 1], [1, 0, 0], [0, 1, 0]];
  Zm := [[1, 0, 0], [0, omega, 0], [0, 0, omega^2]];
  phase := omega ^ Mod3(2 * a * b);
  return ScaleMat(phase, MatPowSmall(Xm, a) * MatPowSmall(Zm, b));
end;;

Pauli := function(v, omega)
  return KroneckerProduct(
    SingleDisplacement(v[1], v[2], omega),
    SingleDisplacement(v[3], v[4], omega)
  );
end;;

MinusLambdaIdentity := function(M, lambda)
  local n, out, i, j, row, value;
  n := Length(M);
  out := [];
  for i in [1..n] do
    row := [];
    for j in [1..n] do
      value := M[i][j];
      if i = j then
        value := value - lambda;
      fi;
      Add(row, value);
    od;
    Add(out, row);
  od;
  return out;
end;;

HorizontalJoin := function(A, B)
  return List([1..Length(A)], i -> Concatenation(A[i], B[i]));
end;;

NormalizeState := function(v)
  local x, inv;
  for x in v do
    if x <> 0 then
      inv := x^-1;
      return List(v, y -> y * inv);
    fi;
  od;
  Error("zero state vector");
end;;

MatVec := function(M, v)
  return List([1..Length(M)], i -> Sum([1..Length(v)], j -> M[i][j] * v[j]));
end;;

JointEigenvector := function(U, V, r, s, omega)
  local lamU, lamV, eqs, basis, vec, residualU, residualV;
  lamU := omega ^ r;
  lamV := omega ^ s;
  eqs := HorizontalJoin(
    TransposedMat(MinusLambdaIdentity(U, lamU)),
    TransposedMat(MinusLambdaIdentity(V, lamV))
  );
  basis := NullspaceMat(eqs);
  if Length(basis) <> 1 then
    return rec(dimension := Length(basis), vector := [], residual_ok := false);
  fi;
  vec := NormalizeState(basis[1]);
  residualU := MatVec(U, vec) - List(vec, x -> lamU * x);
  residualV := MatVec(V, vec) - List(vec, x -> lamV * x);
  return rec(
    dimension := 1,
    vector := vec,
    residual_ok := ForAll(Concatenation(residualU, residualV), x -> x = 0)
  );
end;;

SchedulerToAuditMap := function(points)
  return List(
    [1..Length(points)],
    i -> Position(points, NormalizeVec([points[i][1], points[i][4], points[i][3], points[i][2]]))
  );
end;;

SharedLineCount := function(center, active, star)
  local seen, a;
  seen := [];
  for a in active do
    seen := Union(seen, Intersection(star[center], star[a]));
  od;
  return Length(seen);
end;;

DecisionForOverlap := function(overlap)
  if overlap <= 1 then
    return "TIME_SLICE_SHARED_LINE";
  fi;
  if overlap = 2 then
    return "SERIALIZE_WHOLE_STAR";
  fi;
  return "ESCALATE_HOLONOMY";
end;;

TransportPredictions := function(points, schedulerLines, schedulerToAudit, groundsByCenter)
  local activeScheduler0, activeScheduler, activeAudit, schedulerStar, predictions,
    candidate0, candidateScheduler, candidateAudit, agg, activeCenter, left, right,
    predictedShared, actualShared, uniqueCollinearCounts, distribution, row;
  activeScheduler0 := [0, 13, 14, 18, 24, 27, 30];
  activeScheduler := List(activeScheduler0, x -> x + 1);
  activeAudit := List(activeScheduler, x -> schedulerToAudit[x]);
  schedulerStar := StarLines(schedulerLines, Length(points));
  predictions := [];
  distribution := [];
  for candidate0 in [0..Length(points) - 1] do
    if not candidate0 in activeScheduler0 then
      candidateScheduler := candidate0 + 1;
      candidateAudit := schedulerToAudit[candidateScheduler];
      agg := [];
      for activeCenter in activeAudit do
        for left in groundsByCenter[candidateAudit] do
          for right in groundsByCenter[activeCenter] do
            IncrementIntCounter(agg, Length(Intersection(left, right)));
          od;
        od;
      od;
      uniqueCollinearCounts := [
        CounterValue(agg, 0) / 18,
        CounterValue(agg, 3) / 36,
        CounterValue(agg, 8) / 6
      ];
      predictedShared := Maximum(uniqueCollinearCounts);
      actualShared := SharedLineCount(candidateScheduler, activeScheduler, schedulerStar);
      IncrementIntCounter(distribution, actualShared);
      Add(predictions, rec(
        candidate_scheduler_label := candidate0,
        candidate_audit_label := candidateAudit - 1,
        predicted_shared_lines := predictedShared,
        actual_shared_lines := actualShared,
        decision := DecisionForOverlap(predictedShared),
        localized_collision_ticks := predictedShared * 1296,
        intersection_histogram := agg
      ));
    fi;
  od;
  Sort(distribution, function(a, b) return a[1] < b[1]; end);
  Sort(predictions, function(a, b) return a.candidate_scheduler_label < b.candidate_scheduler_label; end);
  return rec(
    active_scheduler_labels := activeScheduler0,
    active_audit_labels := List(activeAudit, x -> x - 1),
    predictions := predictions,
    distribution := distribution,
    all_correct := ForAll(predictions, row -> row.predicted_shared_lines = row.actual_shared_lines)
  );
end;;

JsonBool := function(b)
  if b then
    return "true";
  fi;
  return "false";
end;;

JsonString := function(s)
  return Concatenation("\"", s, "\"");
end;;

Emit := function(arg)
  local stream, out, i;
  stream := arg[1];
  out := "";
  for i in [2..Length(arg)] do
    out := Concatenation(out, String(arg[i]));
  od;
  WriteAll(stream, out);
end;;

JsonIntList := function(vals)
  local out, i;
  out := "[";
  for i in [1..Length(vals)] do
    out := Concatenation(out, String(vals[i]));
    if i < Length(vals) then
      out := Concatenation(out, ", ");
    fi;
  od;
  out := Concatenation(out, "]");
  return out;
end;;

JsonStringList := function(vals)
  local out, i;
  out := "[";
  for i in [1..Length(vals)] do
    out := Concatenation(out, JsonString(vals[i]));
    if i < Length(vals) then
      out := Concatenation(out, ", ");
    fi;
  od;
  out := Concatenation(out, "]");
  return out;
end;;

WriteIntList := function(path, vals, indent)
  local i;
  Emit(path, "[");
  for i in [1..Length(vals)] do
    if i = 1 then
      Emit(path, "\n", indent, "  ", vals[i]);
    else
      Emit(path, ",\n", indent, "  ", vals[i]);
    fi;
  od;
  if Length(vals) > 0 then
    Emit(path, "\n", indent);
  fi;
  Emit(path, "]");
end;;

WriteStringList := function(path, vals, indent)
  local i;
  Emit(path, "[");
  for i in [1..Length(vals)] do
    if i = 1 then
      Emit(path, "\n", indent, "  ", JsonString(vals[i]));
    else
      Emit(path, ",\n", indent, "  ", JsonString(vals[i]));
    fi;
  od;
  if Length(vals) > 0 then
    Emit(path, "\n", indent);
  fi;
  Emit(path, "]");
end;;

WriteRelCounter := function(path, counter, indent)
  local i, row;
  Emit(path, "[\n");
  for i in [1..Length(counter)] do
    row := counter[i];
    Emit(path, indent, "  {\n");
    Emit(path, indent, "    \"relation\": ", JsonString(row[1]), ",\n");
    Emit(path, indent, "    \"intersection\": ", row[2], ",\n");
    Emit(path, indent, "    \"count\": ", row[3], "\n");
    Emit(path, indent, "  }");
    if i < Length(counter) then
      Emit(path, ",");
    fi;
    Emit(path, "\n");
  od;
  Emit(path, indent, "]");
end;;

WriteIntCounterObject := function(path, counter, indent)
  local i, row;
  Emit(path, "{");
  for i in [1..Length(counter)] do
    row := counter[i];
    if i = 1 then
      Emit(path, "\n", indent, "  ");
    else
      Emit(path, ",\n", indent, "  ");
    fi;
    Emit(path, JsonString(String(row[1])), ": ", row[2]);
  od;
  if Length(counter) > 0 then
    Emit(path, "\n", indent);
  fi;
  Emit(path, "}");
end;;

WriteChecks := function(path, checks)
  local i, check;
  Emit(path, "[\n");
  for i in [1..Length(checks)] do
    check := checks[i];
    Emit(path, "    {\n");
    Emit(path, "      \"name\": ", JsonString(check[1]), ",\n");
    Emit(path, "      \"pass\": ", JsonBool(check[2]), "\n");
    Emit(path, "    }");
    if i < Length(checks) then
      Emit(path, ",");
    fi;
    Emit(path, "\n");
  od;
  Emit(path, "  ]");
end;;

WriteHilbertRows := function(path, rows)
  local i, row;
  Emit(path, "[\n");
  for i in [1..Length(rows)] do
    row := rows[i];
    Emit(path, "      {\n");
    Emit(path, "        \"center_label\": ", row.center_label, ",\n");
    Emit(path, "        \"local_phase_label\": ", row.local_phase_label, ",\n");
    Emit(path, "        \"matched_line\": ", JsonIntList(row.matched_line), ",\n");
    Emit(path, "        \"generators\": [\n");
    Emit(path, "          ", JsonIntList(row.generators[1]), ",\n");
    Emit(path, "          ", JsonIntList(row.generators[2]), "\n");
    Emit(path, "        ],\n");
    Emit(path, "        \"character\": ", JsonIntList(row.character), ",\n");
    Emit(path, "        \"eigenspace_dimension\": ", row.eigenspace_dimension, ",\n");
    Emit(path, "        \"residual_ok\": ", JsonBool(row.residual_ok), ",\n");
    Emit(path, "        \"projective_vector\": ");
    WriteStringList(path, List(row.projective_vector, x -> String(x)), "        ");
    Emit(path, "\n      }");
    if i < Length(rows) then
      Emit(path, ",");
    fi;
    Emit(path, "\n");
  od;
  Emit(path, "    ]");
end;;

WritePredictions := function(path, predictions)
  local i, row;
  Emit(path, "[\n");
  for i in [1..Length(predictions)] do
    row := predictions[i];
    Emit(path, "      {\n");
    Emit(path, "        \"candidate_scheduler_label\": ", row.candidate_scheduler_label, ",\n");
    Emit(path, "        \"candidate_audit_label\": ", row.candidate_audit_label, ",\n");
    Emit(path, "        \"predicted_shared_lines\": ", row.predicted_shared_lines, ",\n");
    Emit(path, "        \"actual_shared_lines\": ", row.actual_shared_lines, ",\n");
    Emit(path, "        \"decision\": ", JsonString(row.decision), ",\n");
    Emit(path, "        \"localized_collision_ticks\": ", row.localized_collision_ticks, ",\n");
    Emit(path, "        \"intersection_histogram\": ");
    WriteIntCounterObject(path, row.intersection_histogram, "        ");
    Emit(path, "\n      }");
    if i < Length(predictions) then
      Emit(path, ",");
    fi;
    Emit(path, "\n");
  od;
  Emit(path, "    ]");
end;;

points := BuildPoints();;
auditLines := MakeLines(points, AuditB);;
schedulerLines := MakeLines(points, SchedulerJ);;
adjacency := AdjacencyFromLines(Length(points), auditLines);;
groundData := CenterZeroGrounds(points, auditLines, AuditB);;
G := BuildAuditGroup(points);;

bundle := [];;
for seed in groundData.grounds do
  bundle := Union(bundle, Orbit(G, seed, OnSets));
od;;
Sort(bundle);;
centers := List(bundle, lit -> CenterOfLit(lit, auditLines));;
groundsByCenter := List([1..Length(points)], i -> []);;
for i in [1..Length(bundle)] do
  Add(groundsByCenter[centers[i]], bundle[i]);
od;;
for i in [1..Length(groundsByCenter)] do
  Sort(groundsByCenter[i]);
od;;

stab := Stabilizer(G, groundData.grounds[1], OnSets);;
subdegrees := List(Orbits(stab, bundle, OnSets), Length);;
Sort(subdegrees);;
gluingSpectrum := GluingSpectrum(bundle, centers, adjacency);;

auditStar := StarLines(auditLines, Length(points));;
matching := BacktrackMatching(auditStar);;
omega := E(3);;
hilbertRows := [];;
eigenDims := [];;
residualOK := true;;
for center in [1..Length(points)] do
  lineId := matching[center];
  line := auditLines[lineId];
  genVecs := [points[line[1]], points[line[2]]];
  U := Pauli(genVecs[1], omega);
  V := Pauli(genVecs[2], omega);
  for phaseLabel in [0..8] do
    eig := JointEigenvector(U, V, QuoInt(phaseLabel, 3), phaseLabel mod 3, omega);
    Add(eigenDims, eig.dimension);
    if not eig.residual_ok then
      residualOK := false;
    fi;
    Add(hilbertRows, rec(
      center_label := center - 1,
      local_phase_label := phaseLabel,
      matched_line := List(line, p -> p - 1),
      generators := genVecs,
      character := [QuoInt(phaseLabel, 3), phaseLabel mod 3],
      eigenspace_dimension := eig.dimension,
      residual_ok := eig.residual_ok,
      projective_vector := eig.vector
    ));
  od;
od;;

schedulerToAudit := SchedulerToAuditMap(points);;
transport := TransportPredictions(points, schedulerLines, schedulerToAudit, groundsByCenter);;
distributionExpected := [[1, 7], [2, 9], [3, 9], [4, 8]];;

checks := [
  ["GAP finite field point count is 40", Length(points) = 40],
  ["audit W(3,3) line count is 40", Length(auditLines) = 40],
  ["scheduler W(3,3) line count is 40", Length(schedulerLines) = 40],
  ["center zero has nine affine-plane grounds", Length(groundData.grounds) = 9],
  ["PSp(4,3) point group order is 25920", Size(G) = 25920],
  ["bundle is one 360-state GAP orbit", Length(bundle) = 360],
  ["bundle fibers are 40 centers times nine states", Set(List(groundsByCenter, Length)) = [9]],
  ["GAP stabilizer order is 72", Size(stab) = 72],
  ["GAP subdegrees match Pass 62 rank 15", subdegrees = [1, 3, 4, 8, 8, 24, 24, 24, 24, 24, 24, 24, 24, 72, 72]],
  ["incidence matching uses all 40 lines once", Set(matching) = [1..40]],
  ["each matched line contains its center", ForAll([1..Length(points)], i -> i in auditLines[matching[i]])],
  ["exact qutrit eigenspaces are all one-dimensional", Set(eigenDims) = [1]],
  ["exact cyclotomic residuals are zero", residualOK],
  ["scheduler-to-audit coordinate map is bijective", Set(schedulerToAudit) = [1..40]],
  ["transport kernel predicts every scheduler overlap", transport.all_correct],
  ["transport distribution matches scheduler fixture", transport.distribution = distributionExpected]
];;
allPass := ForAll(checks, row -> row[2]);;

Print("== Pass 63: GAP Hilbert dictionary and transport kernel ==\n\n");;
for row in checks do
  if row[2] then
    Print("  [PASS]  ", row[1], "\n");
  else
    Print("  [FAIL]  ", row[1], "\n");
  fi;
od;;
Print("\nGAP features used: GF-style projective arithmetic, Group/Size, Orbit, Stabilizer, Orbits, OnSets, E(3), KroneckerProduct, NullspaceMat.\n");;
Print("wrote ", OUT, "\n");;

jsonOut := OutputTextFile(OUT, false);;
SetPrintFormattingStatus(jsonOut, false);;
Emit(jsonOut, "{\n");;
Emit(jsonOut, "  \"pass\": 63,\n");;
Emit(jsonOut, "  \"title\": \"GAP Hilbert transport kernel\",\n");;
Emit(jsonOut, "  \"gap\": {\n");;
Emit(jsonOut, "    \"version\": ", JsonString(GAPInfo.Version), ",\n");;
Emit(jsonOut, "    \"features_used\": [\n");;
Emit(jsonOut, "      {\n");;
Emit(jsonOut, "        \"feature\": \"projective GF(3)\",\n");;
Emit(jsonOut, "        \"use\": \"enumerates W33 points and lines\"\n");;
Emit(jsonOut, "      },\n");;
Emit(jsonOut, "      {\n");;
Emit(jsonOut, "        \"feature\": \"Group and Size\",\n");;
Emit(jsonOut, "        \"use\": \"closes six transvections as PSp(4,3)\"\n");;
Emit(jsonOut, "      },\n");;
Emit(jsonOut, "      {\n");;
Emit(jsonOut, "        \"feature\": \"Orbit with OnSets\",\n");;
Emit(jsonOut, "        \"use\": \"moves nine grounds into a 360-state bundle\"\n");;
Emit(jsonOut, "      },\n");;
Emit(jsonOut, "      {\n");;
Emit(jsonOut, "        \"feature\": \"Stabilizer and Orbits\",\n");;
Emit(jsonOut, "        \"use\": \"gets stabilizer 72 and rank 15\"\n");;
Emit(jsonOut, "      },\n");;
Emit(jsonOut, "      {\n");;
Emit(jsonOut, "        \"feature\": \"E(3)\",\n");;
Emit(jsonOut, "        \"use\": \"keeps qutrit phases exact\"\n");;
Emit(jsonOut, "      },\n");;
Emit(jsonOut, "      {\n");;
Emit(jsonOut, "        \"feature\": \"KroneckerProduct\",\n");;
Emit(jsonOut, "        \"use\": \"builds exact two-qutrit Paulis\"\n");;
Emit(jsonOut, "      },\n");;
Emit(jsonOut, "      {\n");;
Emit(jsonOut, "        \"feature\": \"NullspaceMat\",\n");;
Emit(jsonOut, "        \"use\": \"solves exact eigenspaces\"\n");;
Emit(jsonOut, "      }\n");;
Emit(jsonOut, "    ]\n");;
Emit(jsonOut, "  },\n");;
Emit(jsonOut, "  \"geometry\": {\n");;
Emit(jsonOut, "    \"point_count\": ", Length(points), ",\n");;
Emit(jsonOut, "    \"audit_line_count\": ", Length(auditLines), ",\n");;
Emit(jsonOut, "    \"scheduler_line_count\": ", Length(schedulerLines), ",\n");;
Emit(jsonOut, "    \"audit_form\": \"x1y2-x2y1+x3y4-x4y3\",\n");;
Emit(jsonOut, "    \"scheduler_form\": \"x1y4-x2y3+x3y2-x4y1\",\n");;
Emit(jsonOut, "    \"scheduler_to_audit_coordinate_transform\": \"(a,b,c,d) -> (a,d,c,b)\",\n");;
Emit(jsonOut, "    \"scheduler_to_audit_label_map\": ");;
WriteIntList(jsonOut, List(schedulerToAudit, x -> x - 1), "    ");;
Emit(jsonOut, "\n");;
Emit(jsonOut, "  },\n");;
Emit(jsonOut, "  \"bundle\": {\n");;
Emit(jsonOut, "    \"group_order\": ", Size(G), ",\n");;
Emit(jsonOut, "    \"orbit_size\": ", Length(bundle), ",\n");;
Emit(jsonOut, "    \"fiber_sizes\": ");;
WriteIntList(jsonOut, List(groundsByCenter, Length), "    ");;
Emit(jsonOut, ",\n");;
Emit(jsonOut, "    \"stabilizer_order\": ", Size(stab), ",\n");;
Emit(jsonOut, "    \"rank\": ", Length(subdegrees), ",\n");;
Emit(jsonOut, "    \"subdegrees\": ");;
WriteIntList(jsonOut, subdegrees, "    ");;
Emit(jsonOut, ",\n");;
Emit(jsonOut, "    \"gluing_spectrum\": ");;
WriteRelCounter(jsonOut, gluingSpectrum, "    ");;
Emit(jsonOut, "\n");;
Emit(jsonOut, "  },\n");;
Emit(jsonOut, "  \"hilbert_dictionary\": {\n");;
Emit(jsonOut, "    \"scope\": \"explicit gauge; not canonical duality\",\n");;
Emit(jsonOut, "    \"row_count\": ", Length(hilbertRows), ",\n");;
Emit(jsonOut, "    \"normalization\": \"first_nonzero_is_1\",\n");;
Emit(jsonOut, "    \"matched_line_count\": ", Length(Set(matching)), ",\n");;
Emit(jsonOut, "    \"eigenspace_dimensions\": ");;
WriteIntList(jsonOut, eigenDims, "    ");;
Emit(jsonOut, ",\n");;
Emit(jsonOut, "    \"residuals_exactly_zero\": ", JsonBool(residualOK), ",\n");;
Emit(jsonOut, "    \"rows\": ");;
WriteHilbertRows(jsonOut, hilbertRows);;
Emit(jsonOut, "\n");;
Emit(jsonOut, "  },\n");;
Emit(jsonOut, "  \"transport_kernel\": {\n");;
Emit(jsonOut, "    \"reading\": \"intersections predict admission after label transport\",\n");;
Emit(jsonOut, "    \"active_scheduler_labels\": ", JsonIntList(transport.active_scheduler_labels), ",\n");;
Emit(jsonOut, "    \"active_audit_labels\": ", JsonIntList(transport.active_audit_labels), ",\n");;
Emit(jsonOut, "    \"line_context_runtime_ticks\": 1296,\n");;
Emit(jsonOut, "    \"runtime_ticks_per_star\": 5184,\n");;
Emit(jsonOut, "    \"prediction_accuracy\": ", JsonBool(transport.all_correct), ",\n");;
Emit(jsonOut, "    \"candidate_overlap_distribution\": ");;
WriteIntCounterObject(jsonOut, transport.distribution, "    ");;
Emit(jsonOut, ",\n");;
Emit(jsonOut, "    \"predictions\": ");;
WritePredictions(jsonOut, transport.predictions);;
Emit(jsonOut, "\n");;
Emit(jsonOut, "  },\n");;
Emit(jsonOut, "  \"investor_frame\": \"GAP turns the tax into a Hilbert-addressed fuel bundle.\",\n");;
Emit(jsonOut, "  \"checks\": ");;
WriteChecks(jsonOut, checks);;
Emit(jsonOut, ",\n");;
Emit(jsonOut, "  \"all_pass\": ", JsonBool(allPass), "\n");;
Emit(jsonOut, "}\n");;
CloseStream(jsonOut);;

if not allPass then
  Error("Pass 63 GAP certificate failed");
fi;
