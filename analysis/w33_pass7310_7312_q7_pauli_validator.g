# Passes 7310--7312: GAP-owned replay of the q=7 partial-ovoid certificate.
# Packet-owned source: data/PART_W33_PASS7310_Q7_HARDWARE_WITNESS.json,
# field `points`; its provenance points back to the upstream q=7 LNS witness.
# This verifies a 33-point lower-bound witness and its Pauli commutators.  It
# does not prove maximality, synthesize a quantum state, or model dynamics.

points := [
  [0,1,0,5], [0,1,1,3], [0,1,2,4], [0,1,2,5], [0,1,3,3],
  [0,1,6,2], [1,0,2,4], [1,0,5,5], [1,0,6,0], [1,1,2,4],
  [1,1,3,5], [1,1,5,4], [1,1,5,5], [1,2,0,0], [1,3,1,0],
  [1,3,3,6], [1,3,5,1], [1,3,5,4], [1,3,6,6], [1,4,0,3],
  [1,4,1,1], [1,4,1,5], [1,4,3,2], [1,5,0,3], [1,5,1,1],
  [1,5,1,2], [1,5,2,3], [1,5,2,6], [1,5,6,0], [1,6,0,2],
  [1,6,1,2], [1,6,1,5], [1,6,6,3]
];

expectedPacked := [
  2568,1608,2184,2696,1736,1416,2177,2881,385,2185,2761,
  2377,2889,17,89,3289,857,2393,3481,1569,609,2657,1249,
  1577,617,1129,1705,3241,425,1073,1137,2673,1969
];

SymplecticQ7 := function(x,y)
  local s;
  s := (x[1]*y[2] - x[2]*y[1] + x[3]*y[4] - x[4]*y[3]) mod 7;
  return s;
end;

CommutatorHistogram := function(ps)
  local histogram,i,j,s;
  histogram := [0,0,0,0,0,0,0];
  for i in [1..Length(ps)-1] do
    for j in [i+1..Length(ps)] do
      s := SymplecticQ7(ps[i],ps[j]);
      histogram[s+1] := histogram[s+1] + 1;
    od;
  od;
  return histogram;
end;

PackPoint := function(p)
  return p[1] + 8*p[2] + 64*p[3] + 512*p[4];
end;

if Length(points) <> 33 then Error("certificate must contain 33 points"); fi;
if not ForAll(points,p -> Length(p)=4 and ForAll(p,x -> x>=0 and x<7)) then
  Error("certificate coordinates must be four GF(7) residues");
fi;
if not ForAll(points,p -> ForAny(p,x -> x<>0)) then
  Error("certificate contains the zero vector");
fi;

canonicalHistogram := CommutatorHistogram(points);
scaledPoints := List([1..Length(points)],i ->
  List(points[i],x -> ((((i-1) mod 6)+1)*x) mod 7));
scaledHistogram := CommutatorHistogram(scaledPoints);
packed := List(points,PackPoint);

if canonicalHistogram <> [0,88,90,94,90,90,76] then
  Error("canonical commutator histogram drifted");
fi;
if scaledHistogram <> [0,73,120,80,81,88,86] then
  Error("rescaled commutator histogram drifted");
fi;
if packed <> expectedPacked then Error("12-bit packing drifted"); fi;
if Sum(canonicalHistogram) <> 528 or Sum(scaledHistogram) <> 528 then
  Error("pair count must be binomial(33,2)=528");
fi;
if canonicalHistogram[1] <> 0 or scaledHistogram[1] <> 0 then
  Error("a commuting pair was found");
fi;

SizeScreen([4096,4096]);
Print("{\"schema\":\"w33.pass7310_7312.q7_pauli_validator.gap.v1\",",
      "\"q\":7,\"points\":33,\"pairs\":528,",
      "\"canonical_histogram\":",canonicalHistogram,",",
      "\"rescaled_histogram\":",scaledHistogram,",",
      "\"zero_count_invariant\":true,\"all_pass\":true}\n");
QUIT_GAP(0);
