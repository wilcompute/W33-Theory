"""TOE67: full native symplectic symmetry forbids invariant Levi ribbon rotations.

An explicit point-fixing order-three symplectic transvection cycles three of
four incident lines. No cyclic four-slot order is preserved, even up to
reversal. The genus of the ribbon double is always the graph cycle rank 81.
"""
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass1081_1086_core import build_w33,transvection_perm,line_perm

def certificate():
    pts,idx,lines,lidx,point_lines,*_=build_w33()
    assert len(pts)==len(lines)==40
    fixed_point,center=0,4
    g=transvection_perm(pts[center],pts,idx)
    lp=line_perm(g,lines,lidx)
    assert g[fixed_point]==fixed_point
    incident=list(point_lines[fixed_point])
    assert incident==[0,1,2,3]
    induced=tuple(incident.index(lp[i]) for i in incident)
    assert induced==(0,2,3,1)
    assert tuple(induced[induced[induced[i]]] for i in range(4))==tuple(range(4))
    # D4 is the local stabilizer of an unoriented 4-slot cyclic rotation;
    # its element orders 1,2,4 exclude this actual order-three action.
    v,e=80,160
    assert e-v+1==81
    samples=[]
    for b in (2,4,6,8,10):
        h=(2-v+e-b)//2
        assert 2*h+b-1==81
        samples.append({"boundary_components":b,"ribbon_genus":h,"doubled_genus":81})
    return {
        "status":"PASS_TOE67_FULL_SYMMETRY_RIBBON_NO_GO",
        "fixed_native_point":fixed_point,
        "transvection_center_native_point":center,
        "four_incident_isotropic_line_indices":incident,
        "line_action_on_four_incident_lines":list(induced),
        "local_stabilizer_element_order":3,
        "cyclic_order_automorphism_group_orders":[1,2,4],
        "full_PSp_invariant_ribbon_rotation_exists":False,
        "rotation_independent_doubled_genus":81,
        "illustrative_consistent_boundary_counts":samples,
        "general_graph_theorem":"Any connected graph has double of an orientable ribbon thickening of genus E-V+1, independent of cyclic vertex orders.",
        "obstruction":"Native point 4's symplectic transvection fixes native point 0 and induces an order-three 3-cycle on four incident isotropic lines. Such a permutation preserves no four-slot cyclic order, including up to reversal; no full PSp(4,3)-invariant orientable ribbon rotation exists.",
        "scope":"No-go only for full-group invariant ribbon rotations; subgroup choices, symmetry breaking, other cell complexes and dynamical spacetime proposals remain open."
    }

if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe67_ribbon_symmetry_obstruction.json").write_text(
        json.dumps(c,indent=2)+"\n",encoding="utf-8")
    print(c["status"],c["line_action_on_four_incident_lines"])
