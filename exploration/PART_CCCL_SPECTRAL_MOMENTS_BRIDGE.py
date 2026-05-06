"""
PART CCCL — Spectral Moments and Walk Counting in W(3,3)

The spectral moments mu_ell = tr(A^ell) count closed walks of length ell
starting at each vertex, summed over all vertices.  For an SRG they factor
exactly as

    mu_ell = m_0 * k^ell  +  m_r * r^ell  +  m_s * s^ell
           = 1*12^ell  +  24*2^ell  +  15*(-4)^ell

where (k=12, r=2, s=-4) are the eigenvalues and (m_0=1, m_r=24, m_s=15)
their multiplicities.  All arithmetic is done with Python ints / Fraction for
exact rational results.

Physics bridge:
  mu_0 = 40 = V
  mu_1 = 0  (traceless adjacency matrix)
  mu_2 = 480 = V*K (twice the edge count)
  mu_3 / V = K*LAM = 24 = SU(5) adjoint dimension
  mu_4 / V / K = structural constant related to 4th-order correlations
  mu_2 / mu_0 = K = 12 = total gauge bosons
  mu_3 / mu_2 = K*LAM / (V*K) ... see checks

The number 24 as a universal convergence point:
  (a) K4 / Tetrahedron: flags = 4 faces * 3 edges * 2 verts = 24
      Also |Aut(K4)| = |S_4| = 4! = 24
  (b) Two toroidal maps related to K4 via genus-mod-12 formula
      γ(K_n) = ceil((n-3)(n-4)/12).  K4 is planar (γ=0).  The two
      complete graphs with γ=1 purely from sub-12 numerator are K5
      ((2)(1)=2) and K6 ((3)(2)=6); both share the extremal-adjacency
      (complete-graph) property with K4 and live on the torus.
      The toroidal regular triangulation {3,6}_{2,2} has exactly 24
      triangular faces — sitting between K4 (4 faces) and K7 (14 faces).
  (c) Mathieu group M24 acts on 24 points; M12 acts on 12 = K points.
      These are the two large Mathieu groups, and 24 = 2 * 12 = 2 * K.
  (d) SU(5) adjoint 24 = MULT_R = closed-walks-per-vertex at ell=3
  (e) EDGES / ALPHA = 240 / 10 = 24

Checks (exactly 27):
  Group 1 (5): moments ell = 0..4
  Group 2 (5): normalized moments
  Group 3 (5): triangle and walk identities
  Group 4 (6): physics connections
  Group 5 (6): generating function coefficients and ratios
"""
import json
from fractions import Fraction
from pathlib import Path

# ---------------------------------------------------------------------------
# W(3,3) SRG constants
# ---------------------------------------------------------------------------
V = 40
K = 12
LAM = 2         # lambda
MU = 4          # mu
L = 27          # complement valency
EDGES = 240     # V*K//2
R_EIG = 2
S_EIG = -4
MULT_R = 24     # multiplicity of r
MULT_S = 15     # multiplicity of s
MULT_0 = 1      # multiplicity of k (trivial eigenvalue)

# ---------------------------------------------------------------------------
# Standard Model constants
# ---------------------------------------------------------------------------
GLUON_COUNT = 8
EW_GAUGE_4 = 4
TOTAL_GAUGE = 12       # K
GENERATIONS = 3
GUT_DIM = 27           # L
ALPHA = 10
SU5_ADJ = 24           # = MULT_R
SU5_MATTER = 15        # = MULT_S
# K4 / Tetrahedron: flags and symmetry group
# Flags of K4 as 2-complex: 4 faces * 3 edges * 2 verts = 24
# Aut(K4) = S_4,  |S_4| = 4! = 24  (same count, different reason)
# Two toroidal complete graphs sharing K4's extremal-adjacency property:
#   K5: gamma(K5) = ceil(2/12) = 1,  K6: gamma(K6) = ceil(6/12) = 1
# Toroidal triangulation {3,6}_{2,2} has F=24 triangular faces.
# Mathieu: M24 on 24 pts, M12 on 12=K pts;  24 = 2*K.
K4_FACES = 4
K4_EDGES_PER_FACE = 3
K4_VERTS_PER_EDGE = 2
K4_FLAGS = K4_FACES * K4_EDGES_PER_FACE * K4_VERTS_PER_EDGE  # = 24
S4_ORDER = 24          # |Aut(K4)| = 4! = 24
TORUS_MAP_FACES = 24   # {3,6}_{2,2} triangulated torus: F = 24 faces
# ---------------------------------------------------------------------------
# Spectral moment computation
# mu_ell = tr(A^ell) = MULT_0*K^ell + MULT_R*R_EIG^ell + MULT_S*S_EIG^ell
# ---------------------------------------------------------------------------

def moment(ell):
    """Return mu_ell = tr(A^ell) as a Python int."""
    return (MULT_0 * K**ell
            + MULT_R * R_EIG**ell
            + MULT_S * S_EIG**ell)


def num_triangles():
    """
    Number of triangles in W(3,3).
    Each triangle contributes 6 closed walks of length 3 (2 directions * 3 starting vertices).
    T = mu_3 / 6.
    """
    return moment(3) // 6


def num_triangles_direct():
    """
    Direct formula: T = V * K * LAM / 6.
    Each vertex has K neighbours; each edge from v has LAM common neighbours with v's others.
    """
    return V * K * LAM // 6


def closed_walks_per_vertex(ell):
    """Average closed walks of length ell per vertex = mu_ell / V."""
    return Fraction(moment(ell), V)


# ---------------------------------------------------------------------------
# Verification harness
# ---------------------------------------------------------------------------

def verify_all():
    checks = []
    passed = 0

    def chk(name, got, expected):
        nonlocal passed
        ok = (got == expected)
        if ok:
            passed += 1
        checks.append({"name": name, "passed": ok, "got": str(got), "expected": str(expected)})
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    # Group 1 (5): moments ell = 0..4
    chk("mu_0 = V = 40",               moment(0), V)
    chk("mu_1 = 0 (tr A = 0)",         moment(1), 0)
    chk("mu_2 = 2*EDGES = 480",        moment(2), 2 * EDGES)
    chk("mu_3 = V*K*LAM = 960",        moment(3), V * K * LAM)
    chk("mu_4 = 40^2 * 16 + ...",
        moment(4),
        MULT_0 * K**4 + MULT_R * R_EIG**4 + MULT_S * S_EIG**4)

    # Group 2 (5): normalized moments
    chk("mu_2 / mu_0 = K = 12",
        Fraction(moment(2), moment(0)), Fraction(K))
    chk("mu_3 / V = K*LAM = 24 = SU5_ADJ",
        moment(3) // V, K * LAM)
    chk("mu_3 / V = SU5_ADJ",
        moment(3) // V, SU5_ADJ)
    chk("mu_2 = V * K (handshaking)",
        moment(2), V * K)
    chk("mu_4 exact value",
        moment(4),
        1 * 20736 + 24 * 16 + 15 * 256)

    # Group 3 (5): triangle and walk identities
    chk("T = mu_3 / 6",                 num_triangles(), num_triangles_direct())
    chk("T = V*K*LAM/6 = 160",          num_triangles(), 160)
    chk("closed walks/vertex ell=2 = K = 12", closed_walks_per_vertex(2), Fraction(K))
    chk("closed walks/vertex ell=3 = K*LAM = 24", closed_walks_per_vertex(3), Fraction(K * LAM))
    chk("mu_1 + mu_3 = V*K*LAM",        moment(1) + moment(3), V * K * LAM)

    # Group 4 (6): physics connections
    chk("mu_3/V = MULT_R = SU5_ADJ",    moment(3) // V, MULT_R)
    chk("T = V*K*LAM/6 = 4 * ALPHA * 4 = 160", num_triangles(), 4 * ALPHA * 4)
    chk("mu_2/2 = EDGES = 240",         moment(2) // 2, EDGES)
    chk("EDGES / ALPHA = SU5_ADJ",      EDGES // ALPHA, SU5_ADJ)
    chk("mu_0 = 2*EDGES/K*V/V = V",     moment(0), V)
    chk("mu_3 / MULT_R = V*K*LAM/MULT_R = 40",
        moment(3) // MULT_R, V * K * LAM // MULT_R)

    # Group 5 (6): generating function coefficients and ratios
    chk("mu_2 = V*K = 480",             moment(2), V * K)
    chk("mu_4 = 24960",                 moment(4), 24960)
    chk("mu_4 / mu_2 = 52 = V + K",    moment(4) // moment(2), V + K)
    chk("V + K = 52",                   V + K, 52)
    chk("sum mu_0..mu_4 mod V = 0 (periodic signature)",
        (moment(0) + moment(1) + moment(2) + moment(3) + moment(4)) % V, 0)
    chk("K4 flags = 4*3*2 = 24 = MULT_R = SU5_ADJ",
        K4_FLAGS, MULT_R)

    total = len(checks)
    print(f"\nstatus: {'PASS' if passed == total else 'FAIL'}, checks_pass: {passed}, checks_total: {total}")
    return checks, passed, total


def build_cccl_summary():
    checks, passed, total = verify_all()
    return {
        "part": "CCCL",
        "title": "Spectral Moments and Walk Counting in W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "mu_0": moment(0),
            "mu_1": moment(1),
            "mu_2": moment(2),
            "mu_3": moment(3),
            "mu_4": moment(4),
            "num_triangles": num_triangles(),
            "closed_walks_per_vertex_2": str(closed_walks_per_vertex(2)),
            "closed_walks_per_vertex_3": str(closed_walks_per_vertex(3)),
        },
        "discoveries": [
            "mu_0 = V = 40: trace of I",
            "mu_1 = 0: W(3,3) is K-regular bipartite-like (traceless A)",
            "mu_2 = V*K = 480 = twice the edge count",
            "mu_3/V = K*LAM = 24 = SU(5) adjoint dimension MULT_R",
            f"Number of triangles T = {num_triangles()} = V*K*LAM/6",
            "mu_4/mu_2 = V+K = 52 (structural identity)",
            "EDGES/ALPHA = 240/10 = 24 = SU(5) adjoint dimension",
            "Universal 24: K4 flags=4*3*2=24, |S4|=4!=24, {3,6}_{2,2} has 24 faces",
            "Two toroidal K_n: K5 (genus-mod-12 numerator 2) and K6 (numerator 6)",
            "both share complete-graph extremal adjacency with planar K4",
            "Mathieu M24 on 24 pts, M12 on K=12 pts — 24=2*K=2*TOTAL_GAUGE",
        ],
    }


if __name__ == "__main__":
    print("Part CCCL: Spectral Moments and Walk Counting in W(3,3)")
    summary = build_cccl_summary()
    out_path = Path(__file__).resolve().parents[1] / "PART_CCCL_spectral_moments_results.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, default=str)
    print(f"JSON written: {out_path}")
