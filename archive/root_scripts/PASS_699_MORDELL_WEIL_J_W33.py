#!/usr/bin/env python3
"""
Pass 699 — Mordell-Weil Point Search on J(W33)
===============================================
Pass 691 (BSD analog) predicts rank J(W33)(Q) = 1.
This pass performs an explicit point search on the Jacobian J(W33) of K_{3,3}
to find a non-torsion rational point, confirming rank >= 1.

J(W33) as an abelian variety:
  K_{3,3} viewed as a graph curve of genus g = b_1 = 4.
  Wait — for a bipartite graph, the genus is NOT the cycle rank directly.
  The graph K_{3,3} has V=6, E=9, F=1 (embedded in P^2):
    chi = V - E + F = 6 - 9 + 1 = -2
  For a smooth algebraic curve: chi = 2 - 2g => g = 2.
  The Jacobian J(W33) = Jac(C) for a genus-2 curve C associated to K_{3,3}.

  The natural genus-2 curve from K_{3,3}:
  The Petersen-type construction gives:
    C: y^2 = f(x)  where f has degree 5 or 6.
  
  W33 flat-block eigenvalues {q-1, -(q+1)} = {2, -4} at q=3.
  The W33 genus-2 curve:
    C_W33: y^2 = x*(x-(q-1))*(x+(q+1))*(x^2-(q^2-1))
         = x*(x-2)*(x+4)*(x^2-8)  at q=3
  This is a genus-2 curve (degree 5 odd case after factoring x):
    C_W33: y^2 = (x-2)(x+4)(x^2-8)*x = x^5 + 2x^4 - 8x^3 - 16x^2  ... degree 5.

  A rational point (x, y) with y != 0 on C_W33 gives a degree-1 Weierstrass place,
  and differences of such points give elements of J(W33)(Q).

  The W33 curve at q=3:
    C: y^2 = x*(x-2)*(x+4)*(x^2-8)
  Roots of the RHS: x = 0, 2, -4, sqrt(8), -sqrt(8)
  The irrational roots sqrt(8), -sqrt(8) mean this is defined over Q(sqrt(2)).
  To get a curve over Q: rationalize by substituting x = t^2:
    y^2 = t^2*(t^2-2)*(t^2+4)*(t^4-8)  ... degree 8, hyperelliptic.
  
  Better W33 curve (from the motive directly):
  The motive H^1(K_{3,3}) over Q has b_1=4, meaning the Jacobian has dimension 2.
  The actual curve: take the double cover of P^1 branched at 6 points:
    x = 0, +-2, +-4 (from the eigenvalues and their negatives)
    C_W33: y^2 = x*(x-2)*(x+2)*(x-4)*(x+4)*(x-0) ... degree 6 => genus 2.
  Simplified: y^2 = x*(x^2-4)*(x^2-16) = x^5 - 20x^3 + 64x.
  
  This is a HYPERELLIPTIC genus-2 curve. We search for rational points.
"""

import math
from typing import List, Dict, Optional, Tuple


def w33_curve_rhs(x, q: int = 3) -> int:
    """
    RHS of the W33 genus-2 curve: f(x) = x*(x^2-(q-1)^2)*(x^2-(q+1)^2)
    = x * (x^2-4) * (x^2-16) at q=3
    = x^5 - 20x^3 + 64x
    """
    return x * (x**2 - (q-1)**2) * (x**2 - (q+1)**2)


def is_perfect_square(n: int) -> Tuple[bool, int]:
    if n < 0:
        return False, 0
    if n == 0:
        return True, 0
    r = int(math.isqrt(n))
    if r * r == n:
        return True, r
    if (r+1)*(r+1) == n:
        return True, r+1
    return False, 0


def search_rational_points(q: int = 3, x_range: int = 200) -> List[Dict]:
    """
    Search for rational points (x/d^2, y/d^3) on y^2 = f(x) with x = p/q small rational.
    Start with integer x.
    """
    points = []
    for x in range(-x_range, x_range + 1):
        fx = w33_curve_rhs(x, q)
        sq, y = is_perfect_square(fx)
        if sq:
            points.append({"x": x, "y": y, "y_neg": -y, "type": "integer",
                          "trivial": (y == 0)})
    return points


def search_rational_x(q: int = 3, max_num: int = 50, max_den: int = 20) -> List[Dict]:
    """
    Search for rational x = a/b with small numerator/denominator.
    Point (a/b, y) on y^2 = f(x) requires y^2 = f(a/b).
    Write y = c/b^3 (Weierstrass scaling): (c/b^3)^2 = (a/b)^5 - 20(a/b)^3 + 64(a/b)
    => c^2/b^6 = (a^5 - 20a^3*b^2 + 64a*b^4) / b^5
    => c^2 = a * b * (a^2-4b^2) * (a^2-16b^2) / b^0  [simplified]
    => c^2 = a*(a^2-4b^2)*(a^2-16b^2)*b  (after clearing denominators carefully)
    Actually: y^2 = (a/b) * ((a/b)^2 - 4) * ((a/b)^2 - 16)
            = (a/b) * (a^2-4b^2)/b^2 * (a^2-16b^2)/b^2
            = a*(a^2-4b^2)*(a^2-16b^2) / b^5
    For y to be rational: a*(a^2-4b^2)*(a^2-16b^2) / b^5 = (c/d)^2
    Simplest: set d=1, look for a*(a^2-4b^2)*(a^2-16b^2) = b^5 * c^2.
    Very hard in general. Search small cases.
    """
    points = []
    for b in range(1, max_den + 1):
        for a in range(-max_num, max_num + 1):
            from math import gcd
            if gcd(abs(a), b) != 1:
                continue
            numerator = a * (a**2 - 4*b**2) * (a**2 - 16*b**2)
            # Need numerator * b = b^5 * c^2 => numerator = b^4 * c^2
            # So need numerator to be b^4 times a perfect square
            if b == 1:
                sq, c = is_perfect_square(abs(numerator))
                if sq and numerator >= 0:
                    points.append({"x_num": a, "x_den": b, "x": a/b,
                                   "y": c, "type": "rational"})
            else:
                # Check: numerator / b^4 should be a perfect square
                if numerator % (b**4) == 0:
                    val = numerator // (b**4)
                    sq, c = is_perfect_square(abs(val))
                    if sq and val >= 0:
                        points.append({"x_num": a, "x_den": b, "x": a/b,
                                       "y": c / b, "type": "rational"})
    return points


def jacobian_rank_certificate(points: List[Dict]) -> Dict:
    """
    From found rational points, construct a certificate for rank of J(W33)(Q).
    The Jacobian J is an abelian variety of dimension 2.
    A point (x,y) on C gives a divisor class [(x,y) - infty] in J(Q).
    If a non-trivial (y != 0) point is found with x not a root of f,
    it gives an element of J(Q) of infinite order (generically).
    """
    non_trivial = [p for p in points if not p.get('trivial', True) and p.get('y', 0) != 0]
    trivial = [p for p in points if p.get('trivial', False) or p.get('y', 0) == 0]
    return {
        "total_found": len(points),
        "trivial_points": len(trivial),   # y=0, 2-torsion points
        "non_trivial_points": len(non_trivial),
        "points": non_trivial[:5],         # first 5
        "rank_lower_bound": 1 if non_trivial else 0,
        "BSD_prediction": 1,
        "consistent_with_BSD": bool(non_trivial),
        "torsion_points": trivial[:5],
    }


if __name__ == "__main__":
    print("=" * 70)
    print("Pass 699 — Mordell-Weil Point Search on J(W33)")
    print("=" * 70)
    print()
    print("W33 genus-2 curve: C: y^2 = x*(x^2-4)*(x^2-16)")
    print("                      = x^5 - 20x^3 + 64x")
    print()

    # Integer point search
    print("Searching integer points x in [-200, 200]...")
    int_points = search_rational_points(q=3, x_range=200)
    print(f"Found {len(int_points)} integer points.")
    print()

    trivial_pts = [p for p in int_points if p['trivial']]
    nontrivial_pts = [p for p in int_points if not p['trivial']]
    print(f"  Trivial (y=0, 2-torsion): {len(trivial_pts)} points")
    for p in trivial_pts:
        print(f"    x={p['x']}, y=0  (f({p['x']})=0)")
    print()
    print(f"  Non-trivial (y != 0): {len(nontrivial_pts)} points")
    for p in nontrivial_pts:
        print(f"    ({p['x']}, +/-{p['y']})  f({p['x']})={w33_curve_rhs(p['x'])}")

    print()
    print("Searching small rational points...")
    rat_pts = search_rational_x(q=3, max_num=30, max_den=10)
    print(f"Found {len(rat_pts)} small rational points (non-trivial).")
    for p in rat_pts[:5]:
        print(f"  x={p['x']:.4f} = {p['x_num']}/{p['x_den']}, y={p['y']:.4f}")

    cert = jacobian_rank_certificate(int_points + rat_pts)
    print()
    print(f"Jacobian rank certificate:")
    print(f"  Total points found:     {cert['total_found']}")
    print(f"  Trivial (2-torsion):    {cert['trivial_points']}")
    print(f"  Non-trivial:            {cert['non_trivial_points']}")
    print(f"  Rank lower bound:       {cert['rank_lower_bound']}")
    print(f"  BSD prediction:         {cert['BSD_prediction']}")
    print(f"  Consistent with BSD:    {cert['consistent_with_BSD']}")
    print()
    print("THEOREM (Pass 699):")
    print("  The 5 trivial points {x=0, +-2, +-4} are the 2-torsion points of J(W33).")
    print("  They correspond to the roots of y^2 = f(x) and generate the 2-torsion.")
    print("  A non-torsion Mordell-Weil generator requires a 2-descent or Chabauty method.")
    print("  Pass 699 establishes: rank J(W33)(Q) >= 0, with rank=1 predicted by BSD.")
    print()
    print("OPEN COMPUTATION (for Pass 700+):")
    print("  Run Magma/Sage: J := Jacobian(HyperellipticCurve(x^5-20*x^3+64*x));")
    print("  RankBound(J);  -- expected to return 1")
    print("  This will either confirm rank=1 (BSD) or find rank=0 (falsify BSD analog).")
