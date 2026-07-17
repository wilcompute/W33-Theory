import sys
from pathlib import Path
from collections import Counter

ROOT = Path("C:/Repos/Theory of Everything")
sys.path.append(str(ROOT))

from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (
    build_w33,
    generate_projective_symplectic_group,
)
from analysis.w33_BREAKTHROUGH_360_selector_zmin_sheet_design import (
    selector_failure_edge_supports,
    sheet_orbit,
)

def get_double_cover_stab():
    points, edges, edge_index, lines, adj = build_w33()
    # PSp(4,3) on 40 points
    group = generate_projective_symplectic_group(points)
    
    # We need a Z_min quadrangle.
    # An ordinary quadrangle in GQ(3,3).
    # adjacency[i][j] is True if adjacent.
    def find_q():
        for i in range(40):
            for j in range(i+1, 40):
                if adj[i][j]:
                    for k in range(j+1, 40):
                        if adj[j][k] and not adj[i][k]:
                            for l in range(k+1, 40):
                                if adj[k][l] and adj[i][l] and not adj[j][l]:
                                    return (i, j, k, l)
    
    q_tuple = find_q()
    q_set = frozenset(q_tuple)
    
    # Stabilizer in PSp(4,3)
    # This is a bit slow to compute stabilizers of sets in large groups.
    # But PSp(4,3) is only 25920.
    
    # Just list elements and check.
    stab_elements = []
    for g in group.elements:
        # g is a permutation.
        image = frozenset(g[p] for p in q_set)
        if image == q_set:
            stab_elements.append(g)
    
    print(f"PSp Stabilizer order: {len(stab_elements)}")
    
    # Sp(4,3) is the double cover.
    # We can model it by adding a center bit.
    # Or just know that |Stab_Sp| = 2 * |Stab_PSp|.
    # Since 16 is a power of 2, 32 is a power of 2.
    
    return len(stab_elements)

if __name__ == "__main__":
    get_double_cover_stab()
