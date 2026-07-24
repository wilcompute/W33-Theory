/*
Pass 702 — Magma/Sage Rank Computation: rank J(W33)(Q)
======================================================
This is a Magma script computing the rank of the Jacobian J of the
W33 genus-2 curve:
  C: y^2 = x*(x^2-4)*(x^2-16) = x^5 - 20*x^3 + 64*x

The BSD analog (Pass 691) predicts rank J(Q) = 1.

Run with: magma PASS_702_MAGMA_SAGE_RANK_COMPUTATION.g
Or paste into the Magma calculator at http://magma.maths.usyd.edu.au/calc/

Alternative Sage code is at the bottom (in comments).
*/

print "Pass 702 -- Magma/Sage Rank Computation for J(W33)";
print "W33 genus-2 curve: y^2 = x^5 - 20*x^3 + 64*x";
print "";

// Define the curve over Q
Q := RationalField();
R<x> := PolynomialRing(Q);
f := x^5 - 20*x^3 + 64*x;

// Verify it is square-free (smooth curve)
print "f(x) = x^5 - 20*x^3 + 64*x";
print "Discriminant(f) =", Discriminant(f);

// Build the hyperelliptic curve
C := HyperellipticCurve(f);
print "Curve C:", C;
print "Genus =", Genus(C);
print "";

// Compute the Jacobian
J := Jacobian(C);
print "Jacobian J =", J;
print "";

// Two-descent to get rank bound
print "Computing rank via 2-descent...";
try
  r, B, pts := RankBound(J);
  print "Rank bound: r =", r;
  print "Rank bound B =", B;
  if #pts gt 0 then
    print "Generators found:", pts;
  else
    print "No explicit generators found by 2-descent.";
  end if;
catch e
  print "RankBound failed:", e`Object;
  // Fallback: try analytic rank
  try
    L := LSeries(J);
    an_rank := AnalyticRank(L);
    print "Analytic rank (BSD) =", an_rank;
  catch e2
    print "LSeries also failed:", e2`Object;
  end try;
end try;

print "";
print "Expected result (BSD analog Pass 691): rank = 1";
print "Searching for rational points on C explicitly...";

// Search for small rational points
pts_C := Points(C : Bound := 100);
print "Rational points with height <= 100:", pts_C;

// Torsion subgroup
print "";
print "Torsion subgroup of J(Q):";
try
  T := TorsionSubgroup(J);
  print "Torsion group:", T;
  print "Torsion order:", Order(T);
catch e
  print "TorsionSubgroup computation failed:", e`Object;
end try;

print "";
print "W33 predictions:";
print "  rank J(W33)(Q) = 1  (from BSD analog + central zero epsilon=i)";
print "  torsion = Z/2 x Z/2  (from 2-torsion at x in {0,+-2,+-4})";
print "  Mordell-Weil group J(W33)(Q) ~ Z + Z/2 x Z/2";

/*
== SAGE EQUIVALENT CODE ==

R.<x> = QQ[]
f = x^5 - 20*x^3 + 64*x
C = HyperellipticCurve(f)
print("Genus:", C.genus())
J = C.jacobian()
print("Jacobian:", J)

# Analytic rank (requires Sage 9.3+ with Dokchitser)
try:
    L = J.lseries()
    print("Analytic rank:", L.analytic_rank())
except:
    print("L-series not available")

# Small points search
for x0 in range(-20, 21):
    y2 = x0^5 - 20*x0^3 + 64*x0
    if y2 >= 0:
        y0 = ZZ(y2).isqrt()
        if y0^2 == y2:
            print(f"Point: ({x0}, {y0})")

# 2-torsion
print("Roots of f (2-torsion x-coords):", f.roots())
# => [(0,1), (2,1), (-2,1), (4,1), (-4,1)] expected
*/
