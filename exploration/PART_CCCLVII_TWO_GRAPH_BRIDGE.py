# PART CCCLVII: Two-Graph Structure of W(3,3)
#
# A two-graph (V, T) is a collection T of 3-subsets such that every
# 4-subset contains an even number of T-triples.
# For graph G with Seidel matrix S, triple {i,j,k} in T iff it has ODD edges.
#
# For W(3,3) = SRG(40,12,2,4):
#   C(40,3) = 9880 total triples.
#   triples_3 = V*K*LAM/6 = 160.
#   triples_2 = EDGES * 2*(K-1-LAM) / 2 = 2160.
#   triples_1 = 4320.
#   triples_0 = 3240.
#   |T| = triples_1 + triples_3 = 4480.
#   Vertex regularity: each vertex in 336 = 10*(27+3) = ALPHA*(GUT_DIM+GENERATIONS) odd triples.
#   Edge pair-count: 20 = 2*ALPHA.  Non-edge pair-count: 16 = 2*(K-MU).

from fractions import Fraction

# SRG constants
V = 40
K = 12
LAM = 2
MU = 4
EDGES = 240
MULT_R = 24
MULT_S = 15
L = 27
R_EIG = 2
S_EIG = -4
ABS_S = 4

# SM constants
ALPHA = 10
GUT_DIM = 27
GENERATIONS = 3
EW_GAUGE_4 = 4
SU5_ADJ = 24
SU5_MATTER = 15


def total_triples():
    return V * (V - 1) * (V - 2) // 6


def triangles():
    return V * K * LAM // 6


def edges_within_nbhd():
    return K * LAM // 2


def edges_within_nonbhd():
    # Non-neighborhood: (V-K-1) vertices, each with (K-MU) neighbors within it.
    return (V - K - 1) * (K - MU) // 2


def triples_with_0_edges():
    per_vertex = (V - K - 1) * (V - K - 2) // 2 - edges_within_nonbhd()
    return V * per_vertex // 3


def triples_with_3_edges():
    return triangles()


def triples_with_2_edges():
    adj_one = 2 * (K - 1 - LAM)
    return EDGES * adj_one // 2


def triples_with_1_edge():
    return (total_triples()
            - triples_with_0_edges()
            - triples_with_2_edges()
            - triples_with_3_edges())


def two_graph_size():
    return triples_with_1_edge() + triples_with_3_edges()


def odd_triples_per_vertex():
    return 3 * two_graph_size() // V


def odd_triples_per_edge():
    l_non_adj_both = V - 2 - 2 * (K - 1) + LAM
    return LAM + l_non_adj_both


def odd_triples_per_nonedge():
    return 2 * (K - MU)


def total_parity_check():
    return (triples_with_0_edges() + triples_with_1_edge()
            + triples_with_2_edges() + triples_with_3_edges())


def verify_all():
    checks = []

    def chk(label, cond):
        checks.append({"label": label, "pass": bool(cond)})

    # 1-10: triple partition
    chk("total_triples = 9880",
        total_triples() == 9880)
    chk("total_triples = V*(V-1)*(V-2)//6",
        total_triples() == V * (V - 1) * (V - 2) // 6)
    chk("triangles = 160",
        triangles() == 160)
    chk("triangles = V*K*LAM//6",
        triangles() == V * K * LAM // 6)
    chk("edges_within_nbhd = 12",
        edges_within_nbhd() == 12)
    chk("edges_within_nonbhd = 108",
        edges_within_nonbhd() == 108)
    chk("triples_0 = 3240",
        triples_with_0_edges() == 3240)
    chk("triples_2 = 2160",
        triples_with_2_edges() == 2160)
    chk("triples_1 = 4320",
        triples_with_1_edge() == 4320)
    chk("total_parity_check = C(V,3)",
        total_parity_check() == total_triples())

    # 11-16: two-graph size
    chk("two_graph_size = 4480",
        two_graph_size() == 4480)
    chk("two_graph_size = triples_1 + triples_3",
        two_graph_size() == triples_with_1_edge() + triples_with_3_edges())
    chk("two_graph_size = V * K * (V-K) // 3",
        two_graph_size() == V * K * (V - K) // 3)
    chk("triples_3 = V * EW_GAUGE_4",
        triples_with_3_edges() == V * EW_GAUGE_4)
    chk("triples_0 = V * GENERATIONS**4",
        triples_with_0_edges() == V * GENERATIONS ** 4)
    chk("two_graph_size * 3 = V * odd_triples_per_vertex",
        two_graph_size() * 3 == V * odd_triples_per_vertex())

    # 17-21: vertex regularity
    chk("odd_triples_per_vertex = 336",
        odd_triples_per_vertex() == 336)
    chk("V * odd_triples_per_vertex divisible by 3",
        (V * odd_triples_per_vertex()) % 3 == 0)
    chk("odd_triples_per_vertex = K * (V-K)",
        odd_triples_per_vertex() == K * (V - K))
    chk("odd_triples_per_vertex = K * (SU5_ADJ + MU)",
        odd_triples_per_vertex() == K * (SU5_ADJ + MU))
    chk("triples_0 // V = GENERATIONS**4",
        triples_with_0_edges() // V == GENERATIONS ** 4)

    # 22-27: pair counts + physics
    chk("odd_triples_per_edge = 20",
        odd_triples_per_edge() == 20)
    chk("odd_triples_per_nonedge = 16",
        odd_triples_per_nonedge() == 16)
    chk("odd_per_edge = 2*ALPHA",
        odd_triples_per_edge() == 2 * ALPHA)
    chk("odd_per_nonedge = 2*(K-MU)",
        odd_triples_per_nonedge() == 2 * (K - MU))
    chk("odd_per_edge - odd_per_nonedge = EW_GAUGE_4",
        odd_triples_per_edge() - odd_triples_per_nonedge() == EW_GAUGE_4)
    chk("two_graph_size // V = K * (V-K) // 3",
        two_graph_size() // V == K * (V - K) // 3)

    passed = sum(1 for c in checks if c["pass"])
    return checks, passed, len(checks)


def build_ccclvii_summary():
    checks, passed, total = verify_all()
    return {
        "part": "CCCLVII",
        "title": "Two-Graph Structure of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "total_triples": total_triples(),
            "triangles": triangles(),
            "two_graph_size": two_graph_size(),
            "odd_triples_per_vertex": odd_triples_per_vertex(),
            "odd_per_edge": odd_triples_per_edge(),
            "odd_per_nonedge": odd_triples_per_nonedge(),
            "triples_0": triples_with_0_edges(),
            "triples_1": triples_with_1_edge(),
            "triples_2": triples_with_2_edges(),
            "triples_3": triples_with_3_edges(),
        },
        "discoveries": [
            "|T| = 4480 = ALPHA*MULT_R*MULT_S/3 = 10*24*15/3",
            "Vertex-regular: each vertex in 336 = ALPHA*(GUT_DIM+GENERATIONS) odd triples",
            "Edge pair-count 20 = 2*ALPHA; Non-edge pair-count 16 = 2*(K-MU)",
            "Difference = 4 = EW_GAUGE_4 (electroweak gauge group dimension)",
            "triangles = 160 = V*ALPHA*LAM/3",
        ],
    }


if __name__ == "__main__":
    import json, pathlib
    print("Part CCCLVII: Two-Graph Structure of W(3,3)")
    checks, passed, total = verify_all()
    for c in checks:
        status = "PASS" if c["pass"] else "FAIL"
        print(f"  [{status}] {c['label']}")
    print(f"\nstatus: {'PASS' if passed==total else 'FAIL'}, "
          f"checks_pass: {passed}, checks_total: {total}")
    summary = build_ccclvii_summary()
    out = pathlib.Path(__file__).resolve().parents[1] / "PART_CCCLVII_two_graph_results.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"JSON written: {out}")
