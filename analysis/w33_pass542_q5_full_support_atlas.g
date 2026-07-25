#############################################################################
# Pass 542 -- exact q=5 full-support SL(2,5) orbit and spectral atlas.
#
# Every mathematical computation in this witness is performed in GAP.  The
# key enumeration is not a scan of 4^12 sections.  Write each nonzero F_5
# coordinate uniquely as
#
#        c_i = epsilon_i m_i,   m_i in {1,2}, epsilon_i in {+1,-1}.
#
# The signed SL(2,5) action permutes the twelve magnitude coordinates through
# PSL(2,5)=A5.  For each magnitude orbit representative we then enumerate the
# sign words under the full signed stabilizer of that magnitude.  This is an
# exact disjoint decomposition of the full-support section space.
#############################################################################

ROOT := DirectoryCurrent();
OUT := Filename(ROOT, "data/w33_pass542_q5_full_support_atlas.json");

if not IsBound(W33_PASS542_SPECTRAL) then
  W33_PASS542_SPECTRAL := true;
fi;
if not IsBound(W33_PASS542_TRACE_CUTOFF) then
  W33_PASS542_TRACE_CUTOFF := 491;
fi;
if not IsBound(W33_PASS542_CEGAR_CUTOFF) then
  W33_PASS542_CEGAR_CUTOFF := 1200;
fi;

NegVec := function(v, n)
  return List(v, x -> (-x) mod n);
end;

MatVec := function(g, v, n)
  return [ (g[1][1]*v[1]+g[1][2]*v[2]) mod n,
           (g[2][1]*v[1]+g[2][2]*v[2]) mod n ];
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
  return [[g[2][2] mod n,(-g[1][2]) mod n],
          [(-g[2][1]) mod n,g[1][1] mod n]];
end;

DetMod := function(g, n)
  return (g[1][1]*g[2][2]-g[1][2]*g[2][1]) mod n;
end;

GL2Matrices := function(n)
  local ans, a, b, c, d;
  ans := [];
  for a in [0..n-1] do
    for b in [0..n-1] do
      for c in [0..n-1] do
        for d in [0..n-1] do
          if (a*d-b*c) mod n<>0 then Add(ans,[[a,b],[c,d]]); fi;
        od;
      od;
    od;
  od;
  return ans;
end;

InverseGL2 := function(g, n)
  local det, inv;
  det := DetMod(g,n);
  inv := PowerModInt(det,n-2,n);
  return [[(inv*g[2][2]) mod n,(-inv*g[1][2]) mod n],
          [(-inv*g[2][1]) mod n,(inv*g[1][1]) mod n]];
end;

PairReps := function(n)
  local reps, a, b, v, nv;
  reps := [];
  for a in [0..n-1] do
    for b in [0..n-1] do
      if not (a=0 and b=0) then
        v := [a,b];
        nv := NegVec(v,n);
        if v<nv then Add(reps,v); fi;
      fi;
    od;
  od;
  Sort(reps);
  return reps;
end;

ValueAt := function(sec, v, n, reps)
  local nv, r, pos;
  nv := NegVec(v,n);
  if v<nv then r := v; else r := nv; fi;
  pos := Position(reps,r);
  if v=r then return sec[pos]; fi;
  return (-sec[pos]) mod n;
end;

ActSectionDetTwist := function(sec, g, n, reps)
  local gi, det;
  gi := InverseGL2(g,n);
  det := DetMod(g,n);
  return List(reps,r->
    (det*ValueAt(sec,MatVec(gi,r,n),n,reps)) mod n);
end;

AffineWitness := function(left, right, n, reps, gl)
  local g, base, a, b, shifted, i;
  for g in gl do
    base := ActSectionDetTwist(left,g,n,reps);
    for a in [0..n-1] do
      for b in [0..n-1] do
        shifted := [];
        for i in [1..Length(reps)] do
          Add(shifted,(base[i]+a*reps[i][1]+b*reps[i][2]) mod n);
        od;
        if shifted=right then return [g,a,b]; fi;
      od;
    od;
  od;
  return fail;
end;

SignedActionData := function(g, n, reps)
  local gi, perm, signs, i, u, nu, r;
  gi := InverseSL2(g,n);
  perm := [];
  signs := [];
  for i in [1..Length(reps)] do
    u := MatVec(gi,reps[i],n);
    nu := NegVec(u,n);
    if u<nu then
      r := u;
      Add(signs,0);
    else
      r := nu;
      Add(signs,1);
    fi;
    Add(perm,Position(reps,r));
  od;
  return [perm,signs];
end;

ActMagnitude := function(magnitude, action)
  return List([1..Length(magnitude)],i->magnitude[action[1][i]]);
end;

ActSignBits := function(bits, action)
  return List([1..Length(bits)],
    i->(bits[action[1][i]]+action[2][i]) mod 2);
end;

SectionFromMagnitudeAndSigns := function(magnitude, bits)
  return List([1..Length(magnitude)],i->
    (magnitude[i]*([1,-1][bits[i]+1])) mod 5);
end;

MagnitudeSignData := function(sec)
  local magnitude, bits, x;
  magnitude := [];
  bits := [];
  for x in sec do
    if x=1 then Add(magnitude,1); Add(bits,0);
    elif x=4 then Add(magnitude,1); Add(bits,1);
    elif x=2 then Add(magnitude,2); Add(bits,0);
    elif x=3 then Add(magnitude,2); Add(bits,1);
    else Error("full-support canonicalizer received a zero coordinate");
    fi;
  od;
  return [magnitude,bits];
end;

MagnitudeCode := function(magnitude)
  return 1+Sum([1..Length(magnitude)],
    i->(magnitude[i]-1)*2^(i-1));
end;

CanonicalFullSupportSection := function(sec, canonicalData, actions)
  local data, magnitudeData, canonicalMagnitude, actionIndices,
        canonicalBits;
  magnitudeData := MagnitudeSignData(sec);
  data := canonicalData[MagnitudeCode(magnitudeData[1])];
  canonicalMagnitude := data[1];
  actionIndices := data[2];
  canonicalBits := Minimum(List(actionIndices,
    i->ActSignBits(magnitudeData[2],actions[i])));
  return SectionFromMagnitudeAndSigns(canonicalMagnitude,canonicalBits);
end;

CoordinateProduct := function(sec, n)
  local ans, x;
  ans := 1;
  for x in sec do ans := (ans*x) mod n; od;
  return ans;
end;

IncrementCounter := function(counter, key, amount)
  local pos;
  pos := PositionProperty(counter,x->x[1]=key);
  if pos=fail then Add(counter,[key,amount]);
  else counter[pos][2] := counter[pos][2]+amount; fi;
end;

BlockForSection := function(sec, p, reps)
  local z, B, i, v, nv, c, a, x, e, row, col;
  z := E(p);
  B := NullMat(p,p,Cyclotomics);
  for i in [1..Length(reps)] do
    for a in [1..2] do
      if a=1 then
        v := reps[i];
        c := sec[i];
      else
        nv := NegVec(reps[i],p);
        v := nv;
        c := (-sec[i]) mod p;
      fi;
      for x in [0..p-1] do
        e := (c+2*x*v[2]+v[1]*v[2]) mod p;
        row := ((x+v[1]) mod p)+1;
        col := x+1;
        B[row][col] := B[row][col]+z^e;
      od;
    od;
  od;
  return B;
end;

ValuationInt := function(x, p)
  local n, v;
  if x=0 then return 1000000000; fi;
  n := AbsInt(NumeratorRat(x));
  v := 0;
  while n mod p=0 do
    n := QuoInt(n,p);
    v := v+1;
  od;
  return v;
end;

LambdaValuation := function(x, p)
  local norm, k;
  if x=0 then return 1000000000; fi;
  norm := 1;
  for k in [1..p-1] do norm := norm*GaloisCyc(x,k); od;
  if not IsRat(norm) then Error("cyclotomic norm did not land in Q"); fi;
  return ValuationInt(norm,p);
end;

# Exact fast path at the totally ramified prime 5.  Put lambda=1-zeta_5.
# Since Z[zeta_5]=Z[lambda] and 5 is a unit times lambda^4, every algebraic
# integer x=b_0+b_1 lambda+b_2 lambda^2+b_3 lambda^3 satisfies
#
#   v_lambda(x)=min_j (4 v_5(b_j)+j).
#
# The four candidate valuations have distinct residues modulo 4, so their
# minimum cannot cancel.  CoeffsCyc uses five zeta powers; eliminating zeta^4
# and substituting zeta=1-lambda gives the b_j below.
LambdaBasisValuation5 := function(x)
  local cycCoeffs, zetaCoeffs, lambdaCoeffs;
  if x=0 then return 1000000000; fi;
  cycCoeffs := CoeffsCyc(x,5);
  if Length(cycCoeffs)<>5 then
    Error("unexpected CoeffsCyc length in the q=5 lambda-basis valuation");
  fi;
  zetaCoeffs := List([1..4],i->cycCoeffs[i]-cycCoeffs[5]);
  lambdaCoeffs := [
    zetaCoeffs[1]+zetaCoeffs[2]+zetaCoeffs[3]+zetaCoeffs[4],
    -zetaCoeffs[2]-2*zetaCoeffs[3]-3*zetaCoeffs[4],
    zetaCoeffs[3]+3*zetaCoeffs[4],
    -zetaCoeffs[4]
  ];
  if not ForAll(lambdaCoeffs,IsInt) then
    Error("trace is not integral in the q=5 lambda basis");
  fi;
  return Minimum(List([1..4],
    i->4*ValuationInt(lambdaCoeffs[i],5)+(i-1)));
end;

CoefficientProfile := function(coeffs, p)
  local q, ans, k, pos;
  q := Length(coeffs)-1;
  ans := [];
  for k in [2..q] do
    pos := q-k+1;
    Add(ans,LambdaValuation(coeffs[pos],p));
  od;
  return ans;
end;

PowerSumsFromCoefficients := function(coeffs, cutoff)
  local q, a, sums, n, j, acc;
  q := Length(coeffs)-1;
  a := List([1..q],j->coeffs[q-j+1]);
  sums := [];
  for n in [1..cutoff] do
    acc := 0;
    if n<=q then
      for j in [1..n-1] do acc := acc+a[j]*sums[n-j]; od;
      acc := acc+n*a[n];
    else
      for j in [1..q] do acc := acc+a[j]*sums[n-j]; od;
    fi;
    Add(sums,-acc);
  od;
  return sums;
end;

V5Factorial := function(n)
  local ans, d;
  ans := 0;
  d := 5;
  while d<=n do
    ans := ans+QuoInt(n,d);
    d := 5*d;
  od;
  return ans;
end;

OldFactorialPredictionQ5 := function(n)
  return 4+n+(n mod 2)+4*V5Factorial(n);
end;

Base5DigitSum := function(n)
  local ans;
  ans := 0;
  while n>0 do
    ans := ans+(n mod 5);
    n := QuoInt(n,5);
  od;
  return ans;
end;

CandidateMinimumQ5 := function(n)
  local digitSum, threshold, residual;
  digitSum := Base5DigitSum(n);
  threshold := 4+(n mod 2);
  if n mod 5<>0 then
    residual := Maximum(0,threshold-digitSum);
  elif digitSum<threshold then
    residual := 4;
  else
    residual := 0;
  fi;
  return 2*n+residual;
end;

FiniteOrMinusOne := function(value)
  if value<1000000000 then return value; fi;
  return -1;
end;

GapOrMinusOne := function(value, prediction)
  if value<1000000000 then return value-prediction; fi;
  return -1;
end;

RepresentativeOrEmpty := function(index, rows)
  if index>0 then return rows[index].representative; fi;
  return [];
end;

WitnessOrEmpty := function(witness)
  if witness=fail then return []; fi;
  return witness;
end;

Emit := fail;

#############################################################################
# Exact magnitude/sign orbit decomposition.
#############################################################################
p := 5;
reps := PairReps(p);
sl := SL2Matrices(p);
actions := List(sl,g->SignedActionData(g,p,reps));
permutationActions := Set(List(actions,a->a[1]));
binaryWords := Tuples([0,1],Length(reps));
magnitudeWords := List(binaryWords,b->List(b,x->x+1));
magnitudeOrbits := Set(List(magnitudeWords,m->
  Minimum(List(permutationActions,a->List([1..Length(m)],i->m[a[i]])))));

# Precompute the exact factorized canonicalizer for all 2^12 magnitude words.
# Each entry stores the canonical A5 magnitude representative and every signed
# SL2 action carrying the input word to it.  Minimizing the corresponding sign
# images then reproduces exactly the representatives enumerated below.
magnitudeCanonicalData := List([1..2^Length(reps)],i->fail);
for magnitude in magnitudeWords do
  canonicalMagnitude := Minimum(List(permutationActions,
    a->List([1..Length(magnitude)],i->magnitude[a[i]])));
  canonicalActionIndices := Filtered([1..Length(actions)],
    i->ActMagnitude(magnitude,actions[i])=canonicalMagnitude);
  magnitudeCanonicalData[MagnitudeCode(magnitude)] :=
    [canonicalMagnitude,canonicalActionIndices];
od;

orbitCount := 0;
sectionMass := 0;
productOrbitCounts := [];
productSectionMasses := [];
stabilizerDistribution := [];
orbitSizeDistribution := [];
magnitudeRows := [];
representativeChecksum := 0;
representativeSquareChecksum := 0;

if W33_PASS542_SPECTRAL then
  flat := BlockForSection(List([1..Length(reps)],i->0),p,reps);
  cpDictionary := NewDictionary("",true);
  profileDictionary := NewDictionary("",true);
  cpRows := [];
  profileRows := [];
  orbitRows := [];
  orbitDictionary := NewDictionary("",true);
else
  flat := fail;
  cpDictionary := fail;
  profileDictionary := fail;
  cpRows := [];
  profileRows := [];
  orbitRows := [];
  orbitDictionary := fail;
fi;

for magnitudeIndex in [1..Length(magnitudeOrbits)] do
  magnitude := magnitudeOrbits[magnitudeIndex];
  stabilizerIndices := Filtered([1..Length(actions)],
    i->ActMagnitude(magnitude,actions[i])=magnitude);
  permutationStabilizer := Filtered(permutationActions,
    a->List([1..Length(magnitude)],i->magnitude[a[i]])=magnitude);
  signOrbits := Set(List(binaryWords,bits->
    Minimum(List(stabilizerIndices,i->ActSignBits(bits,actions[i])))));
  Add(magnitudeRows,[magnitude,Length(permutationStabilizer),
    Length(stabilizerIndices),Length(signOrbits)]);

  for bits in signOrbits do
    sec := SectionFromMagnitudeAndSigns(magnitude,bits);
    stabilizerSize := Number(stabilizerIndices,
      i->ActSignBits(bits,actions[i])=bits);
    orbitSize := QuoInt(Length(sl),stabilizerSize);
    productValue := CoordinateProduct(sec,p);
    orbitCount := orbitCount+1;
    sectionMass := sectionMass+orbitSize;
    IncrementCounter(stabilizerDistribution,stabilizerSize,1);
    IncrementCounter(orbitSizeDistribution,orbitSize,1);
    IncrementCounter(productOrbitCounts,productValue,1);
    IncrementCounter(productSectionMasses,productValue,orbitSize);
    code := Sum([1..Length(sec)],i->sec[i]*5^(i-1));
    representativeChecksum := representativeChecksum+code;
    representativeSquareChecksum := representativeSquareChecksum+code^2;

    if W33_PASS542_SPECTRAL then
      orbitIndex := Length(orbitRows)+1;
      cp := CharacteristicPolynomial(BlockForSection(sec,p,reps)-flat);
      coeffs := CoefficientsOfUnivariatePolynomial(cp);
      cpKey := String(cp);
      cpIndex := LookupDictionary(cpDictionary,cpKey);
      profile := CoefficientProfile(coeffs,p);
      profileKey := String(profile);
      profileIndex := LookupDictionary(profileDictionary,profileKey);
      if profileIndex=fail then
        Add(profileRows,rec(key:=profileKey,profile:=profile,
          orbitCount:=0,charpolyCount:=0));
        profileIndex := Length(profileRows);
        AddDictionary(profileDictionary,profileKey,profileIndex);
      fi;
      profileRows[profileIndex].orbitCount :=
        profileRows[profileIndex].orbitCount+1;
      if cpIndex=fail then
        Add(cpRows,rec(key:=cpKey,coeffs:=coeffs,profile:=profile,
          representative:=sec,orbitCount:=1,sectionMass:=orbitSize,
          orbitIndices:=[orbitIndex]));
        cpIndex := Length(cpRows);
        AddDictionary(cpDictionary,cpKey,cpIndex);
        profileRows[profileIndex].charpolyCount :=
          profileRows[profileIndex].charpolyCount+1;
      else
        cpRows[cpIndex].orbitCount := cpRows[cpIndex].orbitCount+1;
        cpRows[cpIndex].sectionMass := cpRows[cpIndex].sectionMass+orbitSize;
        Add(cpRows[cpIndex].orbitIndices,orbitIndex);
      fi;
      Add(orbitRows,rec(representative:=sec,cpIndex:=cpIndex,
        stabilizerSize:=stabilizerSize,orbitSize:=orbitSize,
        productValue:=productValue));
      AddDictionary(orbitDictionary,String(sec),orbitIndex);
    fi;
  od;
  if magnitudeIndex mod 8=0 or magnitudeIndex=Length(magnitudeOrbits) then
    Print("Pass 542 atlas: magnitude ",magnitudeIndex,"/",
      Length(magnitudeOrbits),"; orbit reps=",orbitCount,"\n");
  fi;
od;

Sort(productOrbitCounts,function(a,b) return a[1]<b[1]; end);
Sort(productSectionMasses,function(a,b) return a[1]<b[1]; end);
Sort(stabilizerDistribution,function(a,b) return a[1]<b[1]; end);
Sort(orbitSizeDistribution,function(a,b) return a[1]<b[1]; end);

checks := rec();
checks.sl2_order_120 := Length(sl)=120;
checks.twelve_antipodal_pairs := Length(reps)=12;
checks.projective_image_is_A5_order_60 := Length(permutationActions)=60;
checks.ninety_six_magnitude_orbits := Length(magnitudeOrbits)=96;
checks.exact_full_support_orbit_count := orbitCount=139904;
checks.orbit_stabilizer_mass_is_4_power_12 := sectionMass=4^12;
checks.product_orbit_fibres_are_equal :=
  productOrbitCounts=[[1,34976],[2,34976],[3,34976],[4,34976]];
checks.product_section_fibres_are_equal :=
  productSectionMasses=[[1,4^11],[2,4^11],[3,4^11],[4,4^11]];
checks.every_full_section_stabilizer_divides_120 :=
  ForAll(stabilizerDistribution,x->120 mod x[1]=0);
checks.magnitude_rows_sum_to_all_orbits :=
  Sum(magnitudeRows,x->x[4])=orbitCount;

if W33_PASS542_SPECTRAL then
  charpolyMultiplicityHistogram := Collected(List(cpRows,r->r.orbitCount));
  charpolySectionMassHistogram := Collected(List(cpRows,r->r.sectionMass));
  profileCharpolyCountHistogram := Collected(List(profileRows,r->r.charpolyCount));
  profileOrbitCountHistogram := Collected(List(profileRows,r->r.orbitCount));
  collisionClasses := Number(cpRows,r->r.orbitCount>1);
  collisionDebt := Sum(cpRows,r->r.orbitCount-1);
  maximumCollisionBucket := Maximum(List(cpRows,r->r.orbitCount));
  splittingProfiles := Number(profileRows,r->r.charpolyCount>1);
  checks.every_charpoly_has_one_profile :=
    Sum(profileRows,r->r.charpolyCount)=Length(cpRows);
  checks.charpoly_orbit_multiplicities_sum_to_atlas :=
    Sum(cpRows,r->r.orbitCount)=orbitCount;
  checks.profile_orbit_multiplicities_sum_to_atlas :=
    Sum(profileRows,r->r.orbitCount)=orbitCount;

  ###########################################################################
  # Exact determinant/Galois covariance and residual-collision census.
  #
  # diag(2,1) has nonsquare determinant 2 and generates
  # GL(2,5)/SL(2,5) = F_5^x = C4.  Its square diag(4,1) has determinant -1.
  # The square fixes the real-sheet characteristic polynomial and supplies
  # the universal two-orbit baseline.  A size-four polynomial bucket can
  # therefore contain exactly two such determinant--1 pairs.
  ###########################################################################
  gl := GL2Matrices(p);
  outerGenerator := [[2,0],[0,1]];
  outerGeneratorDeterminant := DetMod(outerGenerator,p);
  outerGeneratorIndices := [];
  outerProductTransitions := [];
  for orbitIndex in [1..Length(orbitRows)] do
    sec := ActSectionDetTwist(orbitRows[orbitIndex].representative,
      outerGenerator,p,reps);
    sec := CanonicalFullSupportSection(sec,magnitudeCanonicalData,actions);
    outerIndex := LookupDictionary(orbitDictionary,String(sec));
    if outerIndex=fail then
      Error("outer generator left the exact full-support orbit atlas");
    fi;
    Add(outerGeneratorIndices,outerIndex);
    IncrementCounter(outerProductTransitions,
      [orbitRows[orbitIndex].productValue,
       orbitRows[outerIndex].productValue],1);
    if orbitIndex mod 10000=0 or orbitIndex=Length(orbitRows) then
      Print("Pass 542 outer action: orbit ",orbitIndex,"/",
        Length(orbitRows),"\n");
    fi;
  od;
  Sort(outerProductTransitions,function(a,b) return a[1]<b[1]; end);
  outerSquareIndices := List([1..orbitCount],
    i->outerGeneratorIndices[outerGeneratorIndices[i]]);
  outerCubeIndices := List([1..orbitCount],
    i->outerGeneratorIndices[outerSquareIndices[i]]);
  outerFourthIndices := List([1..orbitCount],
    i->outerGeneratorIndices[outerCubeIndices[i]]);
  determinantMinusOnePairRepresentatives := Filtered([1..orbitCount],
    i->i<outerSquareIndices[i]);
  outerC4OrbitRepresentatives := Filtered([1..orbitCount],i->
    i=Minimum([i,outerGeneratorIndices[i],outerSquareIndices[i],
      outerCubeIndices[i]]));

  cpOuterTargets := [];
  cpOuterTargetSets := [];
  for cpIndex in [1..Length(cpRows)] do
    targetSet := Set(List(cpRows[cpIndex].orbitIndices,
      i->orbitRows[outerGeneratorIndices[i]].cpIndex));
    Add(cpOuterTargetSets,targetSet);
    if Length(targetSet)=1 then Add(cpOuterTargets,targetSet[1]);
    else Add(cpOuterTargets,0); fi;
  od;
  galoisFixedCpCount := Number([1..Length(cpRows)],
    i->cpOuterTargets[i]=i);
  galoisCpPairRepresentatives := Filtered([1..Length(cpRows)],
    i->i<cpOuterTargets[i]);
  outerGeneratorWeightedChecksum := Sum([1..orbitCount],
    i->i*outerGeneratorIndices[i]);
  outerSquareWeightedChecksum := Sum([1..orbitCount],
    i->i*outerSquareIndices[i]);

  sizeTwoCpIndices := Filtered([1..Length(cpRows)],
    i->cpRows[i].orbitCount=2);
  sizeFourCpIndices := Filtered([1..Length(cpRows)],
    i->cpRows[i].orbitCount=4);
  sizeTwoBaselinePairs := Number(sizeTwoCpIndices,cpIndex->
    Set(cpRows[cpIndex].orbitIndices)=
      Set([cpRows[cpIndex].orbitIndices[1],
        outerSquareIndices[cpRows[cpIndex].orbitIndices[1]]]));
  sizeFourTwoPairBuckets := Number(sizeFourCpIndices,cpIndex->
    Set(List(cpRows[cpIndex].orbitIndices,
      i->outerSquareIndices[i]))=Set(cpRows[cpIndex].orbitIndices) and
    ForAll(cpRows[cpIndex].orbitIndices,
      i->outerSquareIndices[i]<>i));

  residualBucketRecords := [];
  residualZeroOffsetAffine := 0;
  residualShiftRequiredAffine := 0;
  residualAffineInequivalent := 0;
  residualPairPartitionOK := true;
  for cpIndex in sizeFourCpIndices do
    bucketIds := Set(cpRows[cpIndex].orbitIndices);
    pairA := Set([bucketIds[1],outerSquareIndices[bucketIds[1]]]);
    remainder := Filtered(bucketIds,i->not i in pairA);
    if Length(remainder)<>2 then residualPairPartitionOK := false; fi;
    pairB := Set([remainder[1],outerSquareIndices[remainder[1]]]);
    if Set(Concatenation(pairA,pairB))<>bucketIds then
      residualPairPartitionOK := false;
    fi;
    affineWitness := AffineWitness(
      orbitRows[pairA[1]].representative,
      orbitRows[pairB[1]].representative,p,reps,gl);
    if affineWitness=fail then
      residualAffineInequivalent := residualAffineInequivalent+1;
      affineClass := "inequivalent";
    elif affineWitness[2]=0 and affineWitness[3]=0 then
      residualZeroOffsetAffine := residualZeroOffsetAffine+1;
      affineClass := "zero_offset";
    else
      residualShiftRequiredAffine := residualShiftRequiredAffine+1;
      affineClass := "shift_required";
    fi;
    Add(residualBucketRecords,[cpIndex,cpOuterTargets[cpIndex],pairA,pairB,
      orbitRows[pairA[1]].representative,
      orbitRows[pairB[1]].representative,affineClass,
      WitnessOrEmpty(affineWitness)]);
  od;
  residualAffineHistogram := [
    ["zero_offset",residualZeroOffsetAffine],
    ["shift_required",residualShiftRequiredAffine],
    ["inequivalent",residualAffineInequivalent]
  ];

  checks.outer_nonsquare_generator_has_determinant_two :=
    outerGeneratorDeterminant=2;
  checks.outer_generator_has_exact_order_four_on_SL2_orbits :=
    ForAll([1..orbitCount],i->outerFourthIndices[i]=i) and
    ForAll([1..orbitCount],i->outerSquareIndices[i]<>i);
  checks.outer_C4_has_34976_full_support_orbits :=
    Length(outerC4OrbitRepresentatives)=34976;
  checks.det_minus_one_square_action_has_69952_free_pairs :=
    Length(determinantMinusOnePairRepresentatives)=69952;
  checks.det_minus_one_square_preserves_every_characteristic_polynomial :=
    ForAll([1..orbitCount],i->
      orbitRows[i].cpIndex=orbitRows[outerSquareIndices[i]].cpIndex);
  checks.nonsquare_generator_is_real_Galois_conjugation :=
    ForAll([1..Length(cpRows)],i->Length(cpOuterTargetSets[i])=1) and
    ForAll([1..Length(cpRows)],i->
      cpRows[cpOuterTargets[i]].coeffs=
        List(cpRows[i].coeffs,c->GaloisCyc(c,2)));
  checks.real_Galois_action_is_an_involution_on_charpolys :=
    ForAll([1..Length(cpRows)],i->
      cpOuterTargets[cpOuterTargets[i]]=i);
  checks.every_size_two_bucket_is_exactly_one_outer_square_pair :=
    sizeTwoBaselinePairs=Length(sizeTwoCpIndices) and
    Length(sizeTwoCpIndices)=69808;
  checks.every_size_four_bucket_is_exactly_two_outer_square_pairs :=
    sizeFourTwoPairBuckets=Length(sizeFourCpIndices) and
    Length(sizeFourCpIndices)=72 and residualPairPartitionOK;
  checks.collision_histogram_is_complete_two_or_four_law :=
    charpolyMultiplicityHistogram=[[2,69808],[4,72]] and
    2*69808+4*72=orbitCount;
  checks.residual_affine_classification_covers_all_72_buckets :=
    Sum(residualAffineHistogram,x->x[2])=72;

  cutoff := W33_PASS542_TRACE_CUTOFF;
  lambdaBasisSmallAuditPassed := true;
  lambdaBasisSmallAuditCases := 0;
  zeta5 := E(5);
  for auditA in [-3..3] do
    for auditB in [-3..3] do
      for auditC in [-3..3] do
        for auditD in [-3..3] do
          auditValue := auditA+auditB*zeta5+auditC*zeta5^2+
            auditD*zeta5^3;
          if LambdaBasisValuation5(auditValue)<>
             LambdaValuation(auditValue,5) then
            lambdaBasisSmallAuditPassed := false;
          fi;
          lambdaBasisSmallAuditCases := lambdaBasisSmallAuditCases+1;
        od;
      od;
    od;
  od;
  realizedAuditCpIndices := Set(List([0..15],k->
    1+QuoInt(k*(Length(cpRows)-1),15)));
  realizedAuditExponents := Filtered(
    [2,3,4,5,6,7,11,25,49,96,202,491],m->m<=cutoff);
  lambdaBasisRealizedAuditPassed := true;
  lambdaBasisRealizedAuditCases := 0;
  for rowIndex in realizedAuditCpIndices do
    powerSums := PowerSumsFromCoefficients(cpRows[rowIndex].coeffs,cutoff);
    for m in realizedAuditExponents do
      if LambdaBasisValuation5(powerSums[m])<>
         LambdaValuation(powerSums[m],5) then
        lambdaBasisRealizedAuditPassed := false;
      fi;
      lambdaBasisRealizedAuditCases := lambdaBasisRealizedAuditCases+1;
    od;
  od;
  checks.lambda_basis_formula_matches_norm_on_all_7_power_4_small_inputs :=
    lambdaBasisSmallAuditPassed and lambdaBasisSmallAuditCases=7^4;
  checks.lambda_basis_formula_matches_realized_power_sum_audit :=
    lambdaBasisRealizedAuditPassed and
    lambdaBasisRealizedAuditCases=
      Length(realizedAuditCpIndices)*Length(realizedAuditExponents);

  minima := List([1..cutoff],i->1000000000);
  minimumCharpolyCounts := List([1..cutoff],i->0);
  minimumOrbitCounts := List([1..cutoff],i->0);
  minimumCpIndices := List([1..cutoff],i->0);
  for rowIndex in [1..Length(cpRows)] do
    row := cpRows[rowIndex];
    powerSums := PowerSumsFromCoefficients(row.coeffs,cutoff);
    for m in [1..cutoff] do
      value := LambdaBasisValuation5(powerSums[m]);
      if value<minima[m] then
        minima[m] := value;
        minimumCharpolyCounts[m] := 1;
        minimumOrbitCounts[m] := row.orbitCount;
        minimumCpIndices[m] := rowIndex;
      elif value=minima[m] then
        minimumCharpolyCounts[m] := minimumCharpolyCounts[m]+1;
        minimumOrbitCounts[m] := minimumOrbitCounts[m]+row.orbitCount;
      fi;
    od;
    if rowIndex mod 5000=0 or rowIndex=Length(cpRows) then
      Print("Pass 542 recurrence: charpoly ",rowIndex,"/",Length(cpRows),
        " through m=",cutoff,"\n");
    fi;
  od;
  traceRows := List([1..cutoff],m->[m,FiniteOrMinusOne(minima[m]),
    OldFactorialPredictionQ5(m),
    GapOrMinusOne(minima[m],OldFactorialPredictionQ5(m)),
    CandidateMinimumQ5(m),minimumCharpolyCounts[m],minimumOrbitCounts[m],
    RepresentativeOrEmpty(minimumCpIndices[m],cpRows)]);
  candidateExceptions := Filtered([2..cutoff],
    m->minima[m]<>CandidateMinimumQ5(m));
  retainedAttainerIndices := Set(Filtered(minimumCpIndices,i->i>0));
  retainedAttainerSections := List(retainedAttainerIndices,
    i->cpRows[i].representative);
  cegarCutoff := W33_PASS542_CEGAR_CUTOFF;
  cegarMinima := List([1..cegarCutoff],i->1000000000);
  for rowIndex in retainedAttainerIndices do
    powerSums := PowerSumsFromCoefficients(cpRows[rowIndex].coeffs,cegarCutoff);
    for m in [1..cegarCutoff] do
      value := LambdaBasisValuation5(powerSums[m]);
      if value<cegarMinima[m] then cegarMinima[m] := value; fi;
    od;
  od;
  cegarExceptions := Filtered([2..cegarCutoff],
    m->cegarMinima[m]<>CandidateMinimumQ5(m));
  checks.trace_one_vanishes_for_every_full_support_section := minima[1]>=1000000000;
  checks.recurrence_table_has_requested_cutoff := Length(traceRows)=cutoff;
  checks.full_atlas_matches_candidate_through_cutoff :=
    Length(candidateExceptions)=0;
  checks.retained_attainers_match_candidate_through_cegar_cutoff :=
    Length(cegarExceptions)=0;
else
  charpolyMultiplicityHistogram := [];
  charpolySectionMassHistogram := [];
  profileCharpolyCountHistogram := [];
  profileOrbitCountHistogram := [];
  collisionClasses := -1;
  collisionDebt := -1;
  maximumCollisionBucket := -1;
  splittingProfiles := -1;
  gl := [];
  outerGenerator := [];
  outerGeneratorDeterminant := -1;
  outerGeneratorIndices := [];
  outerSquareIndices := [];
  outerProductTransitions := [];
  outerGeneratorWeightedChecksum := -1;
  outerSquareWeightedChecksum := -1;
  determinantMinusOnePairRepresentatives := [];
  outerC4OrbitRepresentatives := [];
  cpOuterTargets := [];
  galoisFixedCpCount := -1;
  galoisCpPairRepresentatives := [];
  sizeTwoBaselinePairs := -1;
  sizeFourTwoPairBuckets := -1;
  residualBucketRecords := [];
  residualAffineHistogram := [];
  lambdaBasisSmallAuditPassed := false;
  lambdaBasisSmallAuditCases := 0;
  realizedAuditCpIndices := [];
  realizedAuditExponents := [];
  lambdaBasisRealizedAuditPassed := false;
  lambdaBasisRealizedAuditCases := 0;
  cutoff := 0;
  minima := [];
  traceRows := [];
  candidateExceptions := [];
  retainedAttainerIndices := [];
  retainedAttainerSections := [];
  cegarCutoff := 0;
  cegarExceptions := [];
fi;

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

Emit("{\n");
Emit("  \"schema\":\"w33.pass542.q5_full_support_atlas.v2\",\n");
Emit("  \"status\":\"",statusText,"\",\n");
Emit("  \"method\":\"Exact two-stage decomposition c_i=epsilon_i*m_i: 2^12 magnitude words modulo the A5 projective image, followed by 2^12 sign words modulo each full signed SL(2,5) magnitude stabilizer. No 4^12 raw-section scan is used.\",\n");
Emit("  \"group_order\":",Length(sl),",\n");
Emit("  \"projective_image_order\":",Length(permutationActions),",\n");
Emit("  \"antipodal_pairs\":",Length(reps),",\n");
Emit("  \"magnitude_orbits\":",Length(magnitudeOrbits),",\n");
Emit("  \"full_support_sections\":",sectionMass,",\n");
Emit("  \"full_support_orbits\":",orbitCount,",\n");
Emit("  \"product_orbit_fibres\":",String(productOrbitCounts),",\n");
Emit("  \"product_section_fibres\":",String(productSectionMasses),",\n");
Emit("  \"stabilizer_distribution\":",String(stabilizerDistribution),",\n");
Emit("  \"orbit_size_distribution\":",String(orbitSizeDistribution),",\n");
Emit("  \"magnitude_rows_format\":\"[magnitude_word,A5_stabilizer_size,SL2_signed_stabilizer_size,sign_orbits]\",\n");
Emit("  \"magnitude_rows\":",String(magnitudeRows),",\n");
Emit("  \"representative_checksum\":\"",representativeChecksum,"\",\n");
Emit("  \"representative_square_checksum\":\"",representativeSquareChecksum,"\",\n");
Emit("  \"spectral\":{\n");
Emit("    \"computed\":",W33_PASS542_SPECTRAL,",\n");
Emit("    \"distinct_characteristic_polynomials\":",Length(cpRows),",\n");
Emit("    \"collision_classes\":",collisionClasses,",\n");
Emit("    \"collision_debt\":",collisionDebt,",\n");
Emit("    \"maximum_collision_bucket\":",maximumCollisionBucket,",\n");
Emit("    \"charpoly_orbit_multiplicity_histogram\":",String(charpolyMultiplicityHistogram),",\n");
Emit("    \"charpoly_section_mass_histogram\":",String(charpolySectionMassHistogram),",\n");
Emit("    \"valuation_profiles\":",Length(profileRows),",\n");
Emit("    \"splitting_valuation_profiles\":",splittingProfiles,",\n");
Emit("    \"profile_charpoly_count_histogram\":",String(profileCharpolyCountHistogram),",\n");
Emit("    \"profile_orbit_count_histogram\":",String(profileOrbitCountHistogram),"\n");
Emit("  },\n");
Emit("  \"outer_covariance\":{\n");
Emit("    \"computed\":",W33_PASS542_SPECTRAL,",\n");
Emit("    \"quotient\":\"GL(2,5)/SL(2,5) = F_5^x = C4\",\n");
Emit("    \"determinant_twisted_generator\":",String(outerGenerator),",\n");
Emit("    \"generator_determinant\":",outerGeneratorDeterminant,",\n");
Emit("    \"generator_product_transition_counts\":",String(outerProductTransitions),",\n");
Emit("    \"generator_weighted_orbit_index_checksum\":\"",outerGeneratorWeightedChecksum,"\",\n");
Emit("    \"square_weighted_orbit_index_checksum\":\"",outerSquareWeightedChecksum,"\",\n");
Emit("    \"outer_C4_orbits\":",Length(outerC4OrbitRepresentatives),",\n");
Emit("    \"determinant_minus_one_free_pairs\":",Length(determinantMinusOnePairRepresentatives),",\n");
Emit("    \"real_Galois_fixed_characteristic_polynomials\":",galoisFixedCpCount,",\n");
Emit("    \"real_Galois_characteristic_polynomial_pairs\":",Length(galoisCpPairRepresentatives),",\n");
Emit("    \"size_two_buckets_equal_one_det_minus_one_pair\":",sizeTwoBaselinePairs,",\n");
Emit("    \"size_four_buckets_equal_two_det_minus_one_pairs\":",sizeFourTwoPairBuckets,",\n");
Emit("    \"residual_pair_affine_histogram\":",String(residualAffineHistogram),",\n");
Emit("    \"residual_bucket_rows_format\":\"[charpoly_index,Galois_conjugate_charpoly_index,det_minus_one_pair_A,det_minus_one_pair_B,representative_A,representative_B,affine_class,witness_or_empty]\",\n");
Emit("    \"residual_bucket_rows\":",String(residualBucketRecords),",\n");
Emit("    \"theorem\":\"The determinant-2 generator gives the exact outer C4 action and real Galois conjugation. Its determinant-4 square is fixed-point-free on SL2 orbits and preserves every characteristic polynomial, forcing 69952 baseline pairs. All 69808 multiplicity-2 buckets are one such pair; all 72 multiplicity-4 buckets are exactly two such pairs. The affine histogram classifies the residual relation between those two pairs under all 12000 determinant-twisted GL(2,5)-by-linear-offset transformations.\",\n");
Emit("    \"sample_reinterpretation\":\"Pass 540's 34 collisions inside 3000 sampled SL2 orbits were not a global merge-rate estimator: 33 sampled both endpoints of the universal determinant-minus-one baseline, while its exceptional affine-inequivalent pair sampled one endpoint from each baseline pair in a fourfold bucket.\"\n");
Emit("  },\n");
Emit("  \"trace_recurrence\":{\n");
Emit("    \"scope\":\"minimum over the complete full-support atlas only; this is not the minimum over all 5^12 sections\",\n");
Emit("    \"order\":5,\n");
Emit("    \"cutoff\":",cutoff,",\n");
Emit("    \"valuation_method\":\"For lambda=1-zeta_5 and x=sum_{j=0}^3 b_j lambda^j in Z[zeta_5], total ramification gives v_lambda(x)=min_j(4*v_5(b_j)+j). The four terms have distinct residues modulo 4, so the minimum cannot cancel. This is exact for algebraic integers in Q(zeta_5), and the witness rejects nonintegral lambda coordinates.\",\n");
Emit("    \"lambda_basis_small_norm_audit_cases\":",lambdaBasisSmallAuditCases,",\n");
Emit("    \"lambda_basis_small_norm_audit_passed\":",lambdaBasisSmallAuditPassed,",\n");
Emit("    \"lambda_basis_realized_audit_cp_indices\":",String(realizedAuditCpIndices),",\n");
Emit("    \"lambda_basis_realized_audit_exponents\":",String(realizedAuditExponents),",\n");
Emit("    \"lambda_basis_realized_norm_audit_cases\":",lambdaBasisRealizedAuditCases,",\n");
Emit("    \"lambda_basis_realized_norm_audit_passed\":",lambdaBasisRealizedAuditPassed,",\n");
Emit("    \"candidate\":\"2m+R_5(m), where for 5 not dividing m, R_5=max(0,4+[m odd]-s_5(m)); for 5 dividing m, R_5=4 iff s_5(m)<4+[m odd], and R_5=0 otherwise\",\n");
Emit("    \"candidate_exceptions\":",String(candidateExceptions),",\n");
Emit("    \"rows_format\":\"[m,exact_full_support_min_or_minus1,old_factorial_prediction,old_gap_or_minus1,candidate,attaining_charpolys,attaining_SL2_orbits,one_attaining_section]\",\n");
Emit("    \"rows\":",String(traceRows),",\n");
Emit("    \"retained_attainer_sections\":",String(retainedAttainerSections),",\n");
Emit("    \"cegar_cutoff\":",cegarCutoff,",\n");
Emit("    \"cegar_exceptions\":",String(cegarExceptions),",\n");
Emit("    \"cegar_boundary\":\"The retained sections attain the candidate through the displayed CEGAR cutoff. Only m through the exact cutoff were minimized over all 69880 realized characteristic polynomials; beyond it, this is an attainment test, not an exhaustive lower-bound proof.\"\n");
Emit("  },\n");
Emit("  \"checks\":{\n");
for i in [1..Length(allChecks)] do
  Emit("    \"",allChecks[i],"\":",checks.(allChecks[i]));
  if i<Length(allChecks) then Emit(","); fi;
  Emit("\n");
od;
Emit("  },\n");
Emit("  \"boundary\":\"The orbit atlas, outer C4 action, determinant-minus-one pairing, residual affine classification, and stabilizer/product distributions are exhaustive on the full-support locus. When spectral.computed is true, every one of the 139904 SL(2,5) orbit representatives is evaluated by exact cyclotomic characteristic-polynomial arithmetic. The recurrence table is exact for its displayed finite window and for the full-support locus only; it is not an all-m theorem and does not include sections with zero coordinates.\"\n");
Emit("}\n");
CloseStream(stream);

Print("Pass 542 q5 atlas: ",statusText," (",
  Length(Filtered(allChecks,k->checks.(k))),"/",Length(allChecks),")\n");
Print("magnitude orbits=",Length(magnitudeOrbits),
  " full-support SL2 orbits=",orbitCount," mass=",sectionMass,"\n");
if W33_PASS542_SPECTRAL then
  Print("charpolys=",Length(cpRows)," collisions=",collisionClasses,
    " profiles=",Length(profileRows)," trace cutoff=",cutoff,"\n");
fi;
if not status then QUIT_GAP(1); fi;
QUIT_GAP(0);
