#############################################################################
# Pass 540 -- the q=3 spectral merge is D4 chirality, q=5 targeted tests,
# and the exact Burnside count over Z/9.
#
# GAP 4.12.1 owns every mathematical computation in this witness.  The file
# deliberately does not import the Python witnesses from Passes 487--539.
#############################################################################

ROOT := DirectoryCurrent();
OUT := Filename(ROOT, "data/w33_pass540_symplectic_separator_chainring.json");

ModN := function(x, n)
  return x mod n;
end;

NegVec := function(v, n)
  return List(v, x -> (-x) mod n);
end;

MatVec := function(g, v, n)
  return [ (g[1][1] * v[1] + g[1][2] * v[2]) mod n,
           (g[2][1] * v[1] + g[2][2] * v[2]) mod n ];
end;

SL2Matrices := function(n)
  local ans, a, b, c, d;
  ans := [];
  for a in [0..n-1] do
    for b in [0..n-1] do
      for c in [0..n-1] do
        for d in [0..n-1] do
          if (a*d-b*c) mod n = 1 then
            Add(ans, [[a,b],[c,d]]);
          fi;
        od;
      od;
    od;
  od;
  return ans;
end;

InverseSL2 := function(g, n)
  return [[g[2][2] mod n, (-g[1][2]) mod n],
          [(-g[2][1]) mod n, g[1][1] mod n]];
end;

DetMod := function(g, n)
  return (g[1][1]*g[2][2]-g[1][2]*g[2][1]) mod n;
end;

GL2Matrices := function(p)
  local ans, a, b, c, d;
  ans := [];
  for a in [0..p-1] do
    for b in [0..p-1] do
      for c in [0..p-1] do
        for d in [0..p-1] do
          if (a*d-b*c) mod p <> 0 then Add(ans,[[a,b],[c,d]]); fi;
        od;
      od;
    od;
  od;
  return ans;
end;

InverseGL2 := function(g, p)
  local det, inv;
  det := DetMod(g,p);
  inv := PowerModInt(det,p-2,p);
  return [[(inv*g[2][2]) mod p,(-inv*g[1][2]) mod p],
          [(-inv*g[2][1]) mod p,(inv*g[1][1]) mod p]];
end;

PairReps := function(n)
  local reps, a, b, v, nv;
  reps := [];
  for a in [0..n-1] do
    for b in [0..n-1] do
      if not (a = 0 and b = 0) then
        v := [a,b];
        nv := NegVec(v,n);
        if v < nv then Add(reps, v); fi;
      fi;
    od;
  od;
  Sort(reps);
  return reps;
end;

ValueAt := function(sec, v, n, reps)
  local nv, r, pos;
  nv := NegVec(v,n);
  if v < nv then r := v; else r := nv; fi;
  pos := Position(reps, r);
  if v = r then return sec[pos]; fi;
  return (-sec[pos]) mod n;
end;

ActSection := function(sec, g, n, reps)
  local gi;
  gi := InverseSL2(g,n);
  return List(reps, r -> ValueAt(sec, MatVec(gi,r,n), n, reps));
end;

ActSectionDetTwist := function(sec, g, p, reps)
  local gi, det;
  gi := InverseGL2(g,p);
  det := DetMod(g,p);
  return List(reps,r->(det*ValueAt(sec,MatVec(gi,r,p),p,reps)) mod p);
end;

AffineWitness := function(left, right, p, reps, gl)
  local g, base, r, s, shifted, i;
  for g in gl do
    base := ActSectionDetTwist(left,g,p,reps);
    for r in [0..p-1] do
      for s in [0..p-1] do
        shifted := [];
        for i in [1..Length(reps)] do
          Add(shifted,(base[i]+r*reps[i][1]+s*reps[i][2]) mod p);
        od;
        if shifted=right then return [g,r,s]; fi;
      od;
    od;
  od;
  return fail;
end;

ZeroOffsetGLWitness := function(left, right, p, reps, gl)
  local g;
  for g in gl do
    if ActSectionDetTwist(left,g,p,reps)=right then return g; fi;
  od;
  return fail;
end;

CanonicalSection := function(sec, group, n, reps)
  return Minimum(List(group, g -> ActSection(sec,g,n,reps)));
end;

CoordinateProduct := function(sec, n)
  local ans, x;
  ans := 1;
  for x in sec do ans := (ans*x) mod n; od;
  return ans;
end;

SymplecticBracket := function(u, v, p)
  return (u[1]*v[2]-u[2]*v[1]) mod p;
end;

BracketProduct := function(sec, p, reps)
  local scaled, ans, i, j;
  scaled := List([1..Length(reps)],i->List(reps[i],x->(sec[i]*x) mod p));
  ans := 1;
  for i in [1..Length(scaled)-1] do
    for j in [i+1..Length(scaled)] do
      ans := (ans*SymplecticBracket(scaled[i],scaled[j],p)) mod p;
    od;
  od;
  return ans;
end;

# For q=3, the coefficient of X^3 Y in
# Product_i omega(reps[i],(X,Y)).  Unlike BracketProduct, this coefficient is
# independent of the ordering of the four projective classes.
MooreDicksonKappaQ3 := function(reps, p)
  local ans, i, j, term;
  ans := 0;
  for i in [1..Length(reps)] do
    term := reps[i][1] mod p;
    for j in [1..Length(reps)] do
      if j<>i then term := (term*(-reps[j][2])) mod p; fi;
    od;
    ans := (ans+term) mod p;
  od;
  return ans;
end;

StabilizerSize := function(sec, group, p, reps)
  return Number(group,g->ActSection(sec,g,p,reps)=sec);
end;

SignedActionData := function(g, n, reps)
  local gi, perm, signs, i, u, nu, r, pos;
  gi := InverseSL2(g,n);
  perm := [];
  signs := [];
  for i in [1..Length(reps)] do
    u := MatVec(gi,reps[i],n);
    nu := NegVec(u,n);
    if u < nu then r := u; Add(signs,1); else r := nu; Add(signs,-1); fi;
    pos := Position(reps,r);
    Add(perm,pos);
  od;
  return [perm,signs];
end;

BlockForSection := function(sec, p, reps)
  local z, B, i, v, nv, c, a, b, x, e, row, col;
  z := E(p);
  B := NullMat(p,p,Cyclotomics);
  for i in [1..Length(reps)] do
    v := reps[i];
    nv := NegVec(v,p);
    c := sec[i];
    for a in [1..2] do
      if a = 1 then v := reps[i]; c := sec[i];
      else v := nv; c := (-sec[i]) mod p; fi;
      for x in [0..p-1] do
        e := (c + 2*x*v[2] + v[1]*v[2]) mod p;
        row := ((x+v[1]) mod p)+1;
        col := x+1;
        B[row][col] := B[row][col] + z^e;
      od;
    od;
  od;
  return B;
end;

CharpolyData := function(sec, p, reps, flat)
  local B, D, cp;
  B := BlockForSection(sec,p,reps);
  D := B-flat;
  cp := CharacteristicPolynomial(D);
  return [String(cp), CoefficientsOfUnivariatePolynomial(cp)];
end;

GaloisConjugatePolynomial := function(poly, k)
  local coefficients, x;
  coefficients := CoefficientsOfUnivariatePolynomial(poly);
  x := Indeterminate(Cyclotomics);
  return Sum([1..Length(coefficients)],i->GaloisCyc(coefficients[i],k)*x^(i-1));
end;

HeisenbergMultiply := function(g, h, p)
  return [(g[1]+h[1]) mod p,
          (g[2]+h[2]) mod p,
          (g[3]+h[3]-g[1]*h[2]+h[1]*g[2]) mod p];
end;

HeisenbergIndex := function(g, p)
  return g[1]*p^2+g[2]*p+g[3]+1;
end;

CayleyAdjacency := function(sec, p, reps)
  local elements, connection, i, v, nv, c, A, row, g, s, h;
  elements := Tuples([0..p-1],3);
  connection := [];
  for i in [1..Length(reps)] do
    v := reps[i]; nv := NegVec(v,p); c := sec[i];
    Add(connection,[v[1],v[2],c]);
    Add(connection,[nv[1],nv[2],(-c) mod p]);
  od;
  A := NullMat(p^3,p^3);
  for row in [1..Length(elements)] do
    g := elements[row];
    for s in connection do
      h := HeisenbergMultiply(g,s,p);
      A[row][HeisenbergIndex(h,p)] := 1;
    od;
  od;
  return A;
end;

LocalNonneighborProfile := function(A)
  local A2, values, j;
  A2 := A*A;
  values := [];
  for j in [2..Length(A)] do
    if A[1][j]=0 then Add(values,A2[1][j]); fi;
  od;
  return Collected(values);
end;

CriticalGroupProfile := function(A)
  local n, degree, L, keep, divisors;
  n := Length(A);
  degree := Sum(A[1]);
  L := degree*IdentityMat(n)-A;
  keep := [2..n];
  divisors := ElementaryDivisorsMat(L{keep}{keep});
  return Collected(List(Filtered(divisors,x->AbsInt(x)<>1),AbsInt));
end;

ValuationInt := function(x, p)
  local n, v;
  if x = 0 then return 999999; fi;
  n := AbsInt(NumeratorRat(x));
  v := 0;
  while n mod p = 0 do n := QuoInt(n,p); v := v+1; od;
  return v;
end;

LambdaValuation := function(x, p)
  local norm, k;
  if x = 0 then return 999999; fi;
  norm := 1;
  for k in [1..p-1] do norm := norm * GaloisCyc(x,k); od;
  if not IsRat(norm) then Error("cyclotomic norm did not land in Q"); fi;
  return ValuationInt(norm,p);
end;

CoefficientProfile := function(coeffs, p)
  local q, ans, k, pos;
  q := Length(coeffs)-1;
  ans := [];
  # coeffs are constant-first.  Skip e1 (the x^(q-1) coefficient) and
  # record e2,...,eq; signs do not affect lambda-adic valuation.
  for k in [2..q] do
    pos := q-k+1;
    Add(ans, LambdaValuation(coeffs[pos],p));
  od;
  return ans;
end;

LineInvariant := function(sec, p, reps)
  local lines, ratioCounts, squareProductCounts, v, a, b, inva, r, cls,
        pr, sq, totalProduct;
  lines := Concatenation(List([0..p-1], t -> [1,t]), [[0,1]]);
  ratioCounts := [0,0,0];
  squareProductCounts := [0,0];
  for v in lines do
    a := ValueAt(sec,v,p,reps);
    b := ValueAt(sec,List(v,x->(2*x) mod p),p,reps);
    if a = 0 or b = 0 then Error("LineInvariant requires full support"); fi;
    inva := PowerModInt(a,p-2,p);
    r := (b*inva) mod p;
    # Scalar reparametrisation v -> 2v sends r -> -1/r.  At p=5 its
    # orbits are {1,4}, {2}, {3}; count those coordinate-free classes.
    if r = 1 or r = 4 then cls := 1;
    elif r = 2 then cls := 2;
    else cls := 3; fi;
    ratioCounts[cls] := ratioCounts[cls]+1;
    pr := (a*b) mod p;
    sq := (pr*pr) mod p;
    if sq = 1 then squareProductCounts[1] := squareProductCounts[1]+1;
    elif sq = 4 then squareProductCounts[2] := squareProductCounts[2]+1;
    else Error("unexpected nonzero square at p=5"); fi;
  od;
  totalProduct := CoordinateProduct(sec,p);
  return [totalProduct,ratioCounts,squareProductCounts];
end;

AddToSetMap := function(map, key, value)
  local pos;
  pos := PositionProperty(map, x -> x[1] = key);
  if pos = fail then Add(map,[key,[value]]);
  elif not value in map[pos][2] then Add(map[pos][2],value); fi;
end;

LCGFullSupport := function(state, len, p)
  local sec, i;
  sec := [];
  for i in [1..len] do
    state := (1103515245*state + 12345) mod 2147483647;
    Add(sec,(state mod (p-1))+1);
  od;
  return [state,sec];
end;

BurnsideSignedSections := function(n)
  local group, reps, total, totalFull, totalPrimitive, totalDeep, profile,
        shellProfile, g, dat, perm, signs, seen, free, freePrimitive,
        freeDeep, negative, i, j, sign, cycle, pos, fixed, fullFixed, shell;
  group := SL2Matrices(n);
  reps := PairReps(n);
  total := 0;
  totalFull := 0;
  totalPrimitive := 0;
  totalDeep := 0;
  profile := [];
  shellProfile := [];
  for g in group do
    dat := SignedActionData(g,n,reps);
    perm := dat[1]; signs := dat[2];
    seen := [];
    free := 0;
    freePrimitive := 0;
    freeDeep := 0;
    negative := 0;
    for i in [1..Length(reps)] do
      if not i in seen then
        j := i; sign := 1; cycle := [];
        while not j in cycle do
          Add(cycle,j); AddSet(seen,j);
          sign := sign*signs[j];
          j := perm[j];
        od;
        if n=9 and reps[i][1] mod 3=0 and reps[i][2] mod 3=0 then
          shell := "deep";
        else shell := "primitive"; fi;
        if sign = 1 then
          free := free+1;
          if shell="deep" then freeDeep:=freeDeep+1;
          else freePrimitive:=freePrimitive+1; fi;
        else negative:=negative+1; fi;
      fi;
    od;
    fixed := n^free;
    total := total+fixed;
    totalPrimitive := totalPrimitive+n^freePrimitive;
    totalDeep := totalDeep+n^freeDeep;
    if negative=0 then fullFixed:=(n-1)^free;
    else fullFixed:=0; fi;
    totalFull:=totalFull+fullFixed;
    pos := PositionProperty(profile,x->x[1]=free);
    if pos=fail then Add(profile,[free,1]); else profile[pos][2]:=profile[pos][2]+1; fi;
    pos:=PositionProperty(shellProfile,x->x[1]=freePrimitive and x[2]=freeDeep);
    if pos=fail then Add(shellProfile,[freePrimitive,freeDeep,1]);
    else shellProfile[pos][3]:=shellProfile[pos][3]+1; fi;
  od;
  Sort(profile,function(a,b) return a[1]<b[1]; end);
  Sort(shellProfile,function(a,b)
    if a[1]=b[1] then return a[2]<b[2]; fi;
    return a[1]<b[1];
  end);
  if total mod Length(group) <> 0 then Error("Burnside average is not integral"); fi;
  if totalFull mod Length(group) <> 0 then Error("full-support Burnside average is not integral"); fi;
  return rec(modulus:=n,groupOrder:=Length(group),pairCount:=Length(reps),
             sectionCount:=n^Length(reps),orbits:=QuoInt(total,Length(group)),
             fullSupportSections:=(n-1)^Length(reps),
             fullSupportOrbits:=QuoInt(totalFull,Length(group)),
             primitiveShellOrbits:=QuoInt(totalPrimitive,Length(group)),
             deepShellOrbits:=QuoInt(totalDeep,Length(group)),
             positiveCycleProfile:=profile,jointShellCycleProfile:=shellProfile);
end;

FullSupportProductBurnside := function(n)
  local group, reps, totals, g, dat, perm, signs, seen, possible,
        cycleOptions, i, j, cycle, sign, options, a, value, product,
        distribution, nextDistribution, residue, option, answer;
  group := SL2Matrices(n);
  reps := PairReps(n);
  totals := List([0..n-1],x->0);
  for g in group do
    dat := SignedActionData(g,n,reps);
    perm := dat[1]; signs := dat[2];
    seen := [];
    possible := true;
    cycleOptions := [];
    for i in [1..Length(reps)] do
      if not i in seen then
        j := i; cycle := []; sign := 1;
        while not j in cycle do
          Add(cycle,j); AddSet(seen,j);
          sign := sign*signs[j];
          j := perm[j];
        od;
        if sign=-1 then
          possible := false;
          break;
        fi;
        options := [];
        for a in [1..n-1] do
          j := i; value := a; product := 1;
          repeat
            product := (product*value) mod n;
            value := (signs[j]*value) mod n;
            j := perm[j];
          until j=i;
          Add(options,product);
        od;
        Add(cycleOptions,options);
      fi;
    od;
    if possible then
      distribution := List([0..n-1],x->0);
      distribution[2] := 1;
      for options in cycleOptions do
        nextDistribution := List([0..n-1],x->0);
        for residue in [0..n-1] do
          for option in options do
            nextDistribution[((residue*option) mod n)+1] :=
              nextDistribution[((residue*option) mod n)+1]+distribution[residue+1];
          od;
        od;
        distribution := nextDistribution;
      od;
      totals := List([1..n],i->totals[i]+distribution[i]);
    fi;
  od;
  if not ForAll(totals,x->x mod Length(group)=0) then
    Error("product-refined Burnside average is not integral");
  fi;
  answer := List([0..n-1],i->[i,QuoInt(totals[i+1],Length(group))]);
  return answer;
end;

#############################################################################
# A. Exhaustive q=3 orbit separator and D4/Q4 reading.
#############################################################################
p3 := 3;
reps3 := PairReps(p3);
sp3 := SL2Matrices(p3);
all3 := Tuples([0..2],Length(reps3));
canon3 := Set(List(all3,s->CanonicalSection(s,sp3,p3,reps3)));
full3 := Filtered(canon3,s->ForAll(s,x->x<>0));
prod3 := List(full3,s->CoordinateProduct(s,p3));
flat3 := BlockForSection(List([1..Length(reps3)],i->0),p3,reps3);
cp3 := List(full3,s->CharpolyData(s,p3,reps3,flat3)[1]);
signProducts3 := List(sp3,g->Product(SignedActionData(g,p3,reps3)[2]));
pairPerms3 := Set(List(sp3,g->SignedActionData(g,p3,reps3)[1]));
gl3 := GL2Matrices(p3);
glSwap3 := First(gl3,g->DetMod(g,p3)=2 and
  ActSectionDetTwist(full3[1],g,p3,reps3)=full3[2]);
glProductCharacter3 := Set(List(gl3,g->[DetMod(g,p3),
  CoordinateProduct(ActSectionDetTwist(List([1..Length(reps3)],i->1),g,p3,reps3),p3)]));
productInvariant3 := ForAll(all3,s->ForAll(sp3,g->
  CoordinateProduct(ActSection(s,g,p3,reps3),p3)=CoordinateProduct(s,p3)));
reorientedReps3 := ShallowCopy(reps3);
reorientedReps3[1] := NegVec(reorientedReps3[1],p3);
reorientedFull3 := ShallowCopy(full3[1]);
reorientedFull3[1] := (-reorientedFull3[1]) mod p3;
kappa3 := MooreDicksonKappaQ3(reps3,p3);
reorientedKappa3 := MooreDicksonKappaQ3(reorientedReps3,p3);
selectorPoints3 := List([1..Length(reps3)],i->
  List(reps3[i],x->(full3[1][i]*x) mod p3));
reorientedSelectorPoints3 := List([1..Length(reorientedReps3)],i->
  List(reorientedReps3[i],x->(reorientedFull3[i]*x) mod p3));
oddReorderedReps3 := ShallowCopy(reps3);
oddReorderedReps3[1] := reps3[2];
oddReorderedReps3[2] := reps3[1];
oddReorderedFull3 := ShallowCopy(full3[1]);
oddReorderedFull3[1] := full3[1][2];
oddReorderedFull3[2] := full3[1][1];
oddReorderedSelectorPoints3 := List([1..Length(oddReorderedReps3)],i->
  List(oddReorderedReps3[i],x->(oddReorderedFull3[i]*x) mod p3));

checks := rec();
checks.q3_group_order_24 := Length(sp3)=24;
checks.q3_seven_orbits := Length(canon3)=7;
checks.q3_two_full_support_orbits := Length(full3)=2;
checks.q3_product_is_invariant := productInvariant3;
checks.q3_signed_action_is_even := Set(signProducts3)=[1];
checks.q3_projective_image_is_A4 := Length(pairPerms3)=12 and
  ForAll(pairPerms3,x->SignPerm(PermList(x))=1);
checks.q3_product_separates_full_support_pair := Set(prod3)=[1,2];
checks.q3_lex_six_bracket_matches_moore_coefficient :=
  ForAll(full3,s->BracketProduct(s,p3,reps3)=
    (kappa3*CoordinateProduct(s,p3)) mod p3);
checks.q3_oriented_product_and_moore_coefficient_transform_correctly :=
  selectorPoints3=reorientedSelectorPoints3 and
  CoordinateProduct(full3[1],p3)<>CoordinateProduct(reorientedFull3,p3) and
  (kappa3*CoordinateProduct(full3[1],p3)) mod p3=
    (reorientedKappa3*CoordinateProduct(reorientedFull3,p3)) mod p3 and
  BracketProduct(full3[1],p3,reps3)=
    BracketProduct(reorientedFull3,p3,reorientedReps3);
checks.q3_odd_reordering_flips_bracket_not_moore_coefficient :=
  Set(selectorPoints3)=Set(oddReorderedSelectorPoints3) and
  MooreDicksonKappaQ3(oddReorderedReps3,p3)=kappa3 and
  CoordinateProduct(oddReorderedFull3,p3)=CoordinateProduct(full3[1],p3) and
  BracketProduct(oddReorderedFull3,p3,oddReorderedReps3)=
    (-BracketProduct(full3[1],p3,reps3)) mod p3;
checks.q3_charpoly_merges_that_pair := Length(Set(cp3))=1;
checks.q3_det_minus_one_covariance_swaps_chiralities := glSwap3<>fail;
checks.q3_GL_product_character_is_quadratic := glProductCharacter3=[[1,1],[2,2]];
checks.q3_full_orbit_stabilisers_are_C3_sized :=
  List(full3,s->StabilizerSize(s,sp3,p3,reps3))=[3,3];
checks.q3_full_support_is_Q4_split_8_plus_8 :=
  Length(Filtered(all3,s->ForAll(s,x->x<>0) and CoordinateProduct(s,3)=1))=8 and
  Length(Filtered(all3,s->ForAll(s,x->x<>0) and CoordinateProduct(s,3)=2))=8;

#############################################################################
# B. q=5 full-support targeted sample and finer symplectic invariants.
#############################################################################
p5 := 5;
reps5 := PairReps(p5);
sp5 := SL2Matrices(p5);
signProducts5 := List(sp5,g->Product(SignedActionData(g,p5,reps5)[2]));
flat5 := BlockForSection(List([1..Length(reps5)],i->0),p5,reps5);
sampleTarget := 3000;
state := 5402026;
canon5 := [];
attempts := 0;
while Length(canon5)<sampleTarget do
  draw := LCGFullSupport(state,Length(reps5),p5);
  state := draw[1];
  sec := CanonicalSection(draw[2],sp5,p5,reps5);
  if not sec in canon5 then Add(canon5,sec); fi;
  attempts := attempts+1;
  if attempts>100000 then Error("failed to obtain q=5 orbit sample"); fi;
od;

rows5 := [];
profileMap5 := [];
featureMap5 := [];
cpMap5 := [];
invariance5 := true;
for i in [1..Length(canon5)] do
  sec := canon5[i];
  cpdat := CharpolyData(sec,p5,reps5,flat5);
  cpkey := cpdat[1];
  prof := CoefficientProfile(cpdat[2],p5);
  feat := LineInvariant(sec,p5,reps5);
  Add(rows5,[sec,cpkey,prof,feat]);
  AddToSetMap(profileMap5,String(prof),cpkey);
  AddToSetMap(featureMap5,Concatenation(String(prof),"|",String(feat)),cpkey);
  AddToSetMap(cpMap5,cpkey,sec);
  for g in sp5 do
    if LineInvariant(ActSection(sec,g,p5,reps5),p5,reps5)<>feat then
      invariance5 := false;
    fi;
  od;
od;

mergeKeys5 := Filtered(cpMap5,x->Length(x[2])>1);
splitProfiles5 := Filtered(profileMap5,x->Length(x[2])>1);
ambiguousFeature5 := Filtered(featureMap5,x->Length(x[2])>1);
profileDebt5 := Sum(profileMap5,x->Length(x[2])-1);
featureDebt5 := Sum(featureMap5,x->Length(x[2])-1);
gl5 := GL2Matrices(p5);
mergeRecords5 := [];
for hit in mergeKeys5 do
  zeroWitness := ZeroOffsetGLWitness(hit[2][1],hit[2][2],p5,reps5,gl5);
  affineWitness := AffineWitness(hit[2][1],hit[2][2],p5,reps5,gl5);
  Add(mergeRecords5,[hit[1],hit[2][1],hit[2][2],
    LineInvariant(hit[2][1],p5,reps5),LineInvariant(hit[2][2],p5,reps5),
    zeroWitness,affineWitness,
    StabilizerSize(hit[2][1],sp5,p5,reps5),
    StabilizerSize(hit[2][2],sp5,p5,reps5)]);
od;
zeroOffsetMerges5 := Length(Filtered(mergeRecords5,x->x[6]<>fail));
shiftRequiredMerges5 := Length(Filtered(mergeRecords5,x->x[6]=fail and x[7]<>fail));
affineMerges5 := zeroOffsetMerges5+shiftRequiredMerges5;
genuineMerges5 := Length(Filtered(mergeRecords5,x->x[7]=fail));
firstZeroOffsetMerge5 := First(mergeRecords5,x->x[6]<>fail);
firstShiftRequiredMerge5 := First(mergeRecords5,x->x[6]=fail and x[7]<>fail);
firstGenuineMerge5 := First(mergeRecords5,x->x[7]=fail);
zeroOffsetWitnessDeterminants5 := Collected(List(
  Filtered(mergeRecords5,x->x[6]<>fail),x->DetMod(x[6],p5)));
glProductCharacter5 := Set(List(gl5,g->[DetMod(g,p5),
  CoordinateProduct(ActSectionDetTwist(List([1..Length(reps5)],i->1),g,p5,reps5),p5)]));
if firstGenuineMerge5<>fail then
  rawPolyGenuine5 := List([firstGenuineMerge5[2],firstGenuineMerge5[3]],s->
    CharacteristicPolynomial(BlockForSection(s,p5,reps5)));
  rawCpGenuine5 := List(rawPolyGenuine5,String);
  rationalNormGenuine5 := rawPolyGenuine5[1]*
    GaloisConjugatePolynomial(rawPolyGenuine5[1],2);
  rationalNormCoefficients5 := CoefficientsOfUnivariatePolynomial(rationalNormGenuine5);
  pass456Pair5 := [
    [0,3,4,1,1,0,2,0,1,1,2,2],
    [0,2,3,0,2,2,4,1,0,3,3,2]
  ];
  pass479Pairs5 := [
    [[0,1,3,0,1,3,1,1,0,3,4,3],[1,2,2,4,4,4,1,1,0,4,0,0]],
    [[3,3,0,2,3,1,0,3,3,0,0,4],[0,3,3,4,2,4,3,0,2,1,4,1]],
    [[4,1,4,1,4,3,0,3,2,4,4,0],[2,4,2,2,3,3,0,3,0,2,1,3]],
    [[2,0,0,3,3,1,2,3,0,0,1,0],[2,0,4,4,1,3,3,3,4,2,0,2]],
    [[3,1,2,1,0,1,4,1,3,3,1,4],[0,4,2,4,0,3,0,2,3,0,0,2]]
  ];
  pass482Pairs5 := [
    [[0,0,0,2,0,1,2,1,3,2,3,0],[2,4,0,1,3,2,1,0,4,2,2,3]],
    [[0,0,4,4,3,3,2,1,0,4,3,0],[4,4,1,2,2,2,1,0,3,1,4,1]]
  ];
  priorExplicitPairs5 := Concatenation(
    [pass456Pair5],pass479Pairs5,pass482Pairs5);
  priorExplicitEndpoints5 := Concatenation(priorExplicitPairs5);
  retainedNormFactors5 := List(priorExplicitPairs5,pair->
    CharacteristicPolynomial(BlockForSection(pair[1],p5,reps5)) *
    GaloisConjugatePolynomial(
      CharacteristicPolynomial(BlockForSection(pair[1],p5,reps5)),2));
  priorAffineMatches5 := List(
    [firstGenuineMerge5[2],firstGenuineMerge5[3]],s->
      Filtered(priorExplicitEndpoints5,t->AffineWitness(s,t,p5,reps5,gl5)<>fail));
  newPairOutsideEightExplicitPre540Pairs5 :=
    ForAll(priorAffineMatches5,x->Length(x)=0);
  sheetCoincidence5 := rawPolyGenuine5[1]=rawPolyGenuine5[2] and
    GaloisConjugatePolynomial(rawPolyGenuine5[1],2)=
      GaloisConjugatePolynomial(rawPolyGenuine5[2],2);
  sheetsDistinct5 := rawPolyGenuine5[1]<>
    GaloisConjugatePolynomial(rawPolyGenuine5[1],2);
  newAdjacency5 := List([firstGenuineMerge5[2],firstGenuineMerge5[3]],s->
    CayleyAdjacency(s,p5,reps5));
  fullGraphPolynomials5 := List(newAdjacency5,CharacteristicPolynomial);
  fullGraphExpected5 := (Indeterminate(Rationals)-24)*
    (Indeterminate(Rationals)+1)^24*rationalNormGenuine5^10;
  newLocalProfiles5 := List(newAdjacency5,LocalNonneighborProfile);
  newCriticalGroupProfiles5 := List(newAdjacency5,CriticalGroupProfile);
  expectedCriticalGroupProfile5 :=
    [[5,16],[25,5],[125,13],[2028949923625,10]];
  pass456LocalProfiles5 := List(pass456Pair5,s->
    LocalNonneighborProfile(CayleyAdjacency(s,p5,reps5)));
  toPass456Witnesses5 := List(
    [firstGenuineMerge5[2],firstGenuineMerge5[3]],s->
      List(pass456Pair5,t->AffineWitness(s,t,p5,reps5,gl5)));
  if toPass456Witnesses5[1][1]<>fail and toPass456Witnesses5[2][2]<>fail then
    sameAffinePairAsPass456 := true;
    pass456Orientation5 := "direct";
    pass456Witnesses5 := [toPass456Witnesses5[1][1],toPass456Witnesses5[2][2]];
  elif toPass456Witnesses5[1][2]<>fail and toPass456Witnesses5[2][1]<>fail then
    sameAffinePairAsPass456 := true;
    pass456Orientation5 := "swapped";
    pass456Witnesses5 := [toPass456Witnesses5[1][2],toPass456Witnesses5[2][1]];
  else
    sameAffinePairAsPass456 := false;
    pass456Orientation5 := "new_affine_pair";
    pass456Witnesses5 := [];
  fi;
else
  rawPolyGenuine5 := [];
  rawCpGenuine5 := [];
  rationalNormGenuine5 := fail;
  rationalNormCoefficients5 := [];
  newLocalProfiles5 := [];
  newCriticalGroupProfiles5 := [];
  expectedCriticalGroupProfile5 := [];
  pass456LocalProfiles5 := [];
  fullGraphPolynomials5 := [];
  fullGraphExpected5 := fail;
  toPass456Witnesses5 := [];
  sameAffinePairAsPass456 := false;
  pass456Orientation5 := "no_sample_collision";
  pass456Witnesses5 := [];
  priorAffineMatches5 := [];
  retainedNormFactors5 := [];
  newPairOutsideEightExplicitPre540Pairs5 := false;
  sheetCoincidence5 := false;
  sheetsDistinct5 := false;
fi;
separatorWitness5 := fail;
for i in [1..Length(rows5)] do
  if separatorWitness5=fail then
    for j in [i+1..Length(rows5)] do
      if rows5[i][3]=rows5[j][3] and rows5[i][2]<>rows5[j][2]
         and rows5[i][4]<>rows5[j][4] then
        separatorWitness5 := [rows5[i],rows5[j]];
        break;
      fi;
    od;
  fi;
od;

checks.q5_group_order_120 := Length(sp5)=120;
checks.q5_full_support_sample_3000_orbits := Length(canon5)=3000;
checks.q5_line_feature_is_symplectic_invariant := invariance5;
checks.q5_targeted_full_support_finds_a_sample_merge := Length(mergeKeys5)>0;
checks.q5_sample_contains_affine_inequivalent_merge := firstGenuineMerge5<>fail;
checks.q5_merge_partition_is_complete :=
  zeroOffsetMerges5+shiftRequiredMerges5+genuineMerges5=Length(mergeRecords5);
checks.q5_every_sample_merge_bucket_has_exactly_two_orbits :=
  ForAll(mergeKeys5,x->Length(x[2])=2);
checks.q5_zero_offset_merges_have_square_det_minus_one :=
  zeroOffsetWitnessDeterminants5=[[4,zeroOffsetMerges5]];
checks.q5_GL_product_character_is_quadratic :=
  glProductCharacter5=[[1,1],[2,4],[3,4],[4,1]];
checks.q5_genuine_D_merge_is_raw_block_merge :=
  Length(rawCpGenuine5)=2 and rawCpGenuine5[1]=rawCpGenuine5[2];
checks.q5_genuine_full_support_pair_is_not_pass456_affine_pair :=
  not sameAffinePairAsPass456;
checks.q5_pair_is_outside_eight_explicit_pre540_affine_pairs :=
  newPairOutsideEightExplicitPre540Pairs5;
checks.q5_pair_uses_known_sheet_coincidence_mechanism :=
  sheetCoincidence5 and sheetsDistinct5;
checks.q5_genuine_full_support_graphs_are_nonisomorphic :=
  Length(newLocalProfiles5)=2 and newLocalProfiles5[1]<>newLocalProfiles5[2];
checks.q5_genuine_pair_has_identical_exact_critical_groups :=
  Length(newCriticalGroupProfiles5)=2 and
  newCriticalGroupProfiles5[1]=expectedCriticalGroupProfile5 and
  newCriticalGroupProfiles5[2]=expectedCriticalGroupProfile5;
checks.q5_large_smith_factor_has_prime_cofactor :=
  2028949923625=125*16231599389 and IsPrimeInt(16231599389);
checks.q5_genuine_full_support_graphs_are_exactly_cospectral :=
  Length(fullGraphPolynomials5)=2 and fullGraphPolynomials5[1]=fullGraphPolynomials5[2];
checks.q5_full_graph_factorisation_matches_Wedderburn_blocks :=
  Length(fullGraphPolynomials5)=2 and fullGraphPolynomials5[1]=fullGraphExpected5;
checks.q5_new_graphs_are_not_pass456_graphs :=
  ForAll(newLocalProfiles5,x->not x in pass456LocalProfiles5);
checks.q5_new_spectral_norm_is_integral_degree10 :=
  Length(rationalNormCoefficients5)=11 and ForAll(rationalNormCoefficients5,IsInt);
checks.q5_new_spectrum_differs_from_pass456 :=
  rationalNormCoefficients5<>[-209,-39730,96910,4955,-37925,792,4220,-15,-120,0,1];
checks.q5_new_spectrum_differs_from_all_eight_retained_pair_factors :=
  Length(retainedNormFactors5)=8 and
  ForAll(retainedNormFactors5,f->f<>rationalNormGenuine5);
checks.q5_full_support_profile_splitting_occurs := Length(splitProfiles5)>0;
checks.q5_new_feature_separates_a_split_profile := separatorWitness5<>fail;
checks.q5_augmented_feature_reduces_ambiguity :=
  featureDebt5<profileDebt5;
checks.q5_signed_action_is_even := Set(signProducts5)=[1];
checks.q5_SL2_is_perfect := Size(DerivedSubgroup(SL(2,5)))=120;

#############################################################################
# C. Exact Burnside count over Z/9, with the field q=3 control.
#############################################################################
burn3 := BurnsideSignedSections(3);
burn5 := BurnsideSignedSections(5);
burn9 := BurnsideSignedSections(9);
productBurn3 := FullSupportProductBurnside(3);
productBurn5 := FullSupportProductBurnside(5);
productBurn9 := FullSupportProductBurnside(9);
signProducts9 := List(SL2Matrices(9),g->Product(SignedActionData(g,9,PairReps(9))[2]));
checks.burnside_q3_control_is_7 := burn3.orbits=7;
checks.burnside_q3_full_support_control_is_2 := burn3.fullSupportOrbits=2;
checks.q3_product_fibres_are_the_two_full_support_orbits :=
  productBurn3=[[0,0],[1,1],[2,1]];
checks.q5_full_support_burnside_is_exact := burn5.fullSupportSections=4^12 and
  burn5.fullSupportOrbits=139904;
checks.q5_product_refinement_sums_to_full_support :=
  Sum(productBurn5,x->x[2])=burn5.fullSupportOrbits;
checks.z9_sl2_order_648 := burn9.groupOrder=648;
checks.z9_has_40_antipodal_pairs := burn9.pairCount=40;
checks.z9_section_space_is_9_power_40 := burn9.sectionCount=9^40;
checks.z9_burnside_is_positive_integer := IsInt(burn9.orbits) and burn9.orbits>0;
checks.z9_signed_action_is_even := Set(signProducts9)=[1];
checks.z9_product_refinement_sums_to_full_support :=
  Sum(productBurn9,x->x[2])=burn9.fullSupportOrbits;

allChecks := RecNames(checks);
status := ForAll(allChecks,k->checks.(k));
if status then statusText := "PASS"; else statusText := "FAIL"; fi;

#############################################################################
# Compact GAP-owned JSON certificate.
#############################################################################
stream := OutputTextFile(OUT,false);
SetPrintFormattingStatus(stream,false);
Emit := function(arg)
  local x;
  for x in arg do WriteAll(stream,String(x)); od;
end;
WitnessJSON := function(w)
  if w=fail then return "null"; fi;
  return String(w);
end;

Emit("{\n");
Emit("  \"schema\":\"w33.pass540.symplectic_separator_chainring.v1\",\n");
Emit("  \"status\":\"",statusText,"\",\n");
Emit("  \"q3\":{\n");
Emit("    \"group_order\":",Length(sp3),",\n");
Emit("    \"orbit_count\":",Length(canon3),",\n");
Emit("    \"full_support_orbit_representatives\":",String(full3),",\n");
Emit("    \"coordinate_products\":",String(prod3),",\n");
Emit("    \"coordinate_product_frame\":\"lexicographic PairReps frame; reorienting one antipodal representative multiplies every product label by -1\",\n");
Emit("    \"orientation_kappa\":",kappa3,",\n");
Emit("    \"reoriented_first_pair_kappa\":",reorientedKappa3,",\n");
Emit("    \"reoriented_first_orbit_coordinate_product\":",CoordinateProduct(reorientedFull3,p3),",\n");
Emit("    \"moore_dickson_scalar\":",(kappa3*CoordinateProduct(full3[1],p3)) mod p3,",\n");
Emit("    \"lex_ordered_six_bracket_scalar\":",BracketProduct(full3[1],p3,reps3),",\n");
Emit("    \"full_support_orbits_by_product\":",String(productBurn3),",\n");
Emit("    \"stabiliser_sizes\":",String(List(full3,s->StabilizerSize(s,sp3,p3,reps3))),",\n");
Emit("    \"projective_permutation_image_order\":",Length(pairPerms3),",\n");
Emit("    \"det_minus_one_swap_matrix\":",String(glSwap3),",\n");
Emit("    \"GL_product_character_by_determinant\":",String(glProductCharacter3),",\n");
Emit("    \"shared_characteristic_polynomial\":\"",cp3[1],"\",\n");
Emit("    \"theorem\":\"In the fixed PairReps frame, the two merged full-support orbits are separated exactly by coordinate-product parity. Intrinsically the separator is kappa_R times the oriented coordinate product. In the certificate's lexicographic (even-oriented) projective ordering it also equals the q=3 six-bracket scalar; an odd reordering flips that alternating bracket but not the Moore-Dickson coefficient. Reorienting a representative swaps the bare product labels while preserving the coefficient and unordered two-orbit split. The 16 full-support sections are Q4 sign words and the two fibers are its 8-vertex demicubes, equivalently the D4 spinor and conjugate-spinor weight sets. The symplectic action lies in W(D4), while charpoly(D) forgets this chirality.\"\n");
Emit("  },\n");
Emit("  \"q5\":{\n");
Emit("    \"group_order\":",Length(sp5),",\n");
Emit("    \"full_support_orbits_sampled\":",Length(canon5),",\n");
Emit("    \"draw_attempts\":",attempts,",\n");
Emit("    \"distinct_charpolys\":",Length(cpMap5),",\n");
Emit("    \"sample_orbit_merges\":",Length(mergeKeys5),",\n");
Emit("    \"all_full_support_sections\":",burn5.fullSupportSections,",\n");
Emit("    \"all_full_support_orbits_exact\":",burn5.fullSupportOrbits,",\n");
Emit("    \"full_support_orbits_by_coordinate_product\":",String(productBurn5),",\n");
Emit("    \"zero_offset_GL_equivalent_merge_classes\":",zeroOffsetMerges5,",\n");
Emit("    \"shift_required_affine_equivalent_merge_classes\":",shiftRequiredMerges5,",\n");
Emit("    \"zero_offset_witness_determinants\":",String(zeroOffsetWitnessDeterminants5),",\n");
Emit("    \"GL_product_character_by_determinant\":",String(glProductCharacter5),",\n");
Emit("    \"affine_equivalent_merge_classes\":",affineMerges5,",\n");
Emit("    \"affine_inequivalent_merge_classes\":",genuineMerges5,",\n");
Emit("    \"valuation_profiles\":",Length(profileMap5),",\n");
Emit("    \"splitting_valuation_profiles\":",Length(splitProfiles5),",\n");
Emit("    \"ambiguous_profile_plus_feature_classes\":",Length(ambiguousFeature5),",\n");
Emit("    \"valuation_profile_collision_debt\":",profileDebt5,",\n");
Emit("    \"profile_plus_feature_collision_debt\":",featureDebt5,",\n");
if Length(mergeRecords5)>0 then
  Emit("    \"first_merge\":{\"section_a\":",String(mergeRecords5[1][2]),
       ",\"section_b\":",String(mergeRecords5[1][3]),
       ",\"shared_characteristic_polynomial\":\"",mergeRecords5[1][1],"\"",
       ",\"feature_a\":",String(mergeRecords5[1][4]),
       ",\"feature_b\":",String(mergeRecords5[1][5]),
       ",\"zero_offset_GL_witness\":",WitnessJSON(mergeRecords5[1][6]),
       ",\"affine_witness\":",WitnessJSON(mergeRecords5[1][7]),
       ",\"stabiliser_a\":",mergeRecords5[1][8],
       ",\"stabiliser_b\":",mergeRecords5[1][9],"},\n");
fi;
if firstGenuineMerge5<>fail then
  Emit("    \"affine_inequivalent_merge\":{\"section_a\":",String(firstGenuineMerge5[2]),
       ",\"section_b\":",String(firstGenuineMerge5[3]),
       ",\"shared_characteristic_polynomial\":\"",firstGenuineMerge5[1],"\"",
       ",\"shared_raw_block_characteristic_polynomial\":\"",rawCpGenuine5[1],"\"",
       ",\"faithful_degree10_rational_factor\":\"",String(rationalNormGenuine5),"\"",
       ",\"full_graph_characteristic_polynomial\":\"(x-24)(x+1)^24 times faithful_degree10_rational_factor^10\"",
       ",\"feature_a\":",String(firstGenuineMerge5[4]),
       ",\"feature_b\":",String(firstGenuineMerge5[5]),
       ",\"same_affine_pair_as_pass456\":",sameAffinePairAsPass456,
       ",\"outside_eight_explicit_pre540_affine_pairs\":",newPairOutsideEightExplicitPre540Pairs5,
       ",\"mechanism\":\"sheet coincidence (Pass 481 mechanism)\"",
       ",\"pass456_pair_orientation\":\"",pass456Orientation5,"\"",
       ",\"to_pass456_affine_witnesses\":",String(pass456Witnesses5),
       ",\"nonneighbor_common_neighbor_profiles\":",String(newLocalProfiles5),
       ",\"nonunit_smith_invariant_factors\":",String(newCriticalGroupProfiles5),
       ",\"pass456_profiles_for_comparison\":",String(pass456LocalProfiles5),
       ",\"stabiliser_a\":",firstGenuineMerge5[8],
       ",\"stabiliser_b\":",firstGenuineMerge5[9],"},\n");
fi;
if separatorWitness5<>fail then
  Emit("    \"separator_witness\":{\"profile\":",String(separatorWitness5[1][3]),
       ",\"feature_a\":",String(separatorWitness5[1][4]),
       ",\"feature_b\":",String(separatorWitness5[2][4]),"},\n");
fi;
Emit("    \"feature\":\"fixed-PairReps coordinate product, three ratio classes under r maps to -1/r counted across six projective lines, and two squared pair-product classes\",\n");
Emit("    \"boundary\":\"Exact on 3000 distinct sampled full-support Sp(2,5)-orbits, not an exhaustive spectral statement about all 139,904 full-support orbits (or all 2,034,735 section orbits). Finding a merge overturns Pass 538's zero-in-300 sample as a global heuristic, but does not estimate the full image cardinality. Each sampled merge is classified separately under zero-offset determinant-twisted GL(2,5) and under the complete 12000-element GL(2,5)-by-linear-offset action. A shift-required affine relation alone does not explain equality for D_c=B_c-B_0 because it moves the flat reference.\"\n");
Emit("  },\n");
Emit("  \"z9_burnside\":{\n");
Emit("    \"group\":\"SL(2,Z/9Z)\",\n");
Emit("    \"group_order\":",burn9.groupOrder,",\n");
Emit("    \"antipodal_pairs\":",burn9.pairCount,",\n");
Emit("    \"sections\":\"",burn9.sectionCount,"\",\n");
Emit("    \"orbits\":\"",burn9.orbits,"\",\n");
Emit("    \"full_support_sections\":\"",burn9.fullSupportSections,"\",\n");
Emit("    \"full_support_orbits\":\"",burn9.fullSupportOrbits,"\",\n");
Emit("    \"full_support_orbits_by_coordinate_product\":",String(productBurn9),",\n");
Emit("    \"primitive_shell_orbits\":\"",burn9.primitiveShellOrbits,"\",\n");
Emit("    \"deep_shell_orbits\":",burn9.deepShellOrbits,",\n");
Emit("    \"positive_cycle_profile\":",String(burn9.positiveCycleProfile),",\n");
Emit("    \"primitive_deep_joint_cycle_profile\":",String(burn9.jointShellCycleProfile),",\n");
Emit("    \"method\":\"For every signed cycle, net sign minus forces c=0 because 2 is a unit mod 9; each positive cycle contributes 9 choices. Burnside over all 648 matrices is exact.\"\n");
Emit("  },\n");
Emit("  \"checks\":{\n");
for i in [1..Length(allChecks)] do
  Emit("    \"",allChecks[i],"\":",checks.(allChecks[i]));
  if i<Length(allChecks) then Emit(","); fi;
  Emit("\n");
od;
Emit("  },\n");
Emit("  \"boundary\":\"All algebra, orbit actions, exact cyclotomic characteristic polynomials, invariant checks, and Burnside counts were computed in GAP 4.12.1. The q3 and Z/9 results and the q5 full-support Burnside count are exhaustive. Only the q5 spectral search is a deterministic 3,000-orbit sample, explicitly bounded against the 139,904 full-support orbit universe.\"\n");
Emit("}\n");
CloseStream(stream);

Print("Pass 540: ",statusText," (",Length(Filtered(allChecks,k->checks.(k))),"/",Length(allChecks),")\n");
Print("q3 products=",prod3," shared cp=",cp3[1],"\n");
Print("q5 sampled orbits=",Length(canon5)," merges=",Length(mergeKeys5),
      " split profiles=",Length(splitProfiles5)," residual feature ambiguities=",Length(ambiguousFeature5),"\n");
Print("Z/9 Burnside orbits=",burn9.orbits,"\n");
if not status then QUIT_GAP(1); fi;
QUIT_GAP(0);
