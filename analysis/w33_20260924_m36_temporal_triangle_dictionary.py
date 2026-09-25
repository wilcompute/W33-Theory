#!/usr/bin/env python3
from __future__ import annotations

import json, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_m36_temporal_triangle_dictionary.json"

from exploration.w33_witting_srg_bridge import (
    witting_to_symplectic_isomorphism,
    construct_symplectic_points,
    build_witting_adjacency,
)
from analysis.w33_20260924_history_bigcell_q43_compactification import (
    all_points, canon, symp, line_from_basis,
)
from analysis.w33_20260924_history_invariant_cycle_orientation import (
    HS, HL, TRIS,
)

def jrotate(v):
    a,b,c,d=v
    return canon((c,d,-a,-b))

def m36_witting_index(family,mu,nu):
    return 4 + 4*(3*mu+nu) + family
def main():
    mapping=witting_to_symplectic_isomorphism()
    sp=construct_symplectic_points()
    wadj=build_witting_adjacency()

    B=set(line_from_basis((1,0,0,0),(0,1,0,0)))
    assert len(B)==4

    axes={jrotate(sp[mapping[i]]) for i in range(4)}
    assert axes==B

    tri_source=json.loads(
        (ROOT/"data/w33_20260924_history_invariant_cycle_orientation.json").read_text()
    )
    labels=tri_source["PSp_invariant_triangle_chain"]["triangle_labels"]
    tri_by_point={tuple(row["common_W33_point"]):row for row in labels}
    assert len(tri_by_point)==36

    points=set(all_points())
    assert len(points)==40
    assert set(tri_by_point)==points-B

    family_nearest={}
    rows=[]
    seen_points=set()

    for ray_id in range(36):
        family=ray_id//9
        rem=ray_id%9
        mu,nu=divmod(rem,3)
        widx=m36_witting_index(family,mu,nu)
        point=jrotate(sp[mapping[widx]])
        assert point not in B
        seen_points.add(point)

        nearest=[q for q in B if symp(point,q)==0]
        assert len(nearest)==1
        nearest=nearest[0]
        family_nearest.setdefault(family,set()).add(nearest)

        tri=tri_by_point[point]
        tv=tuple(tri["triangle"])
        histories=[HS[i] for i in tv]

        through=[
            i for i,L in enumerate(HL)
            if point in L
        ]
        assert tuple(sorted(through))==tv
        assert len(through)==3

        rows.append({
          "ray_id":ray_id,
          "family":family,
          "mu":mu,
          "nu":nu,
          "witting_index":widx,
          "w33_point":list(point),
          "nearest_B_point":list(nearest),
          "temporal_triangle_indices":list(tv),
          "temporal_histories":[list(x) for x in histories],
          "orientation_coefficient":tri["orientation_coefficient"],
        })

    assert len(seen_points)==36
    assert all(len(v)==1 for v in family_nearest.values())
    family_map={
      str(k):list(next(iter(v)))
      for k,v in sorted(family_nearest.items())
    }
    assert len(set(map(tuple,family_map.values())))==4

    # Full graph compatibility after the explicit symplectic gauge rotation.
    point_rows=[tuple(r["w33_point"]) for r in rows]
    for i in range(36):
        wi=rows[i]["witting_index"]
        for j in range(i+1,36):
            wj=rows[j]["witting_index"]
            w_orth=wj in wadj[wi]
            s_orth=symp(point_rows[i],point_rows[j])==0
            assert w_orth==s_orth

    # Temporal incidence is the residual GQ after deleting B:
    # 36 off-line points, 27 lines disjoint from B, 108 incidences.
    point_degree=Counter()
    line_degree=Counter()
    for p,row in tri_by_point.items():
        for li in row["triangle"]:
            point_degree[p]+=1
            line_degree[li]+=1
    assert set(point_degree.values())=={3}
    assert set(line_degree.values())=={4}
    assert sum(point_degree.values())==108

    orient=Counter(int(r["orientation_coefficient"]) for r in rows)

    out={
      "schema":"w33.20260924.m36_temporal_triangle_dictionary.v1",
      "status":"PASS_M36_IS_OBJECTWISE_THE_36_ORIENTED_TEMPORAL_TRIANGLES",
      "gauge_alignment":{
        "source_witting_axes":"indices 0..3 in explicit Witting bridge",
        "symplectic_rotation":"J:(a,b,c,d)->(c,d,-a,-b)",
        "target_Bell_line":[list(x) for x in sorted(B)],
        "axes_map_exactly_to_Bell_line":True,
      },
      "residual_geometry":{
        "W33_points_total":40,
        "deleted_Bell_line_points":4,
        "off_line_points":36,
        "history_lines_disjoint_from_Bell":27,
        "temporal_triangles":36,
        "point_degree_into_history_lines":3,
        "history_line_degree_into_off_line_points":4,
        "incidences":108,
        "configuration":"36_3,27_4 residual point-line geometry",
      },
      "M36_dictionary":{
        "ray_id_rule":"family*9 + 3*mu + nu",
        "witting_index_rule":"4 + 4*(3*mu+nu) + family",
        "family_to_unique_Bell_point":family_map,
        "rows":rows,
      },
      "checks":{
        "all_36_magic_rays_biject_to_off_Bell_points":True,
        "all_36_points_biject_to_temporal_triangles":True,
        "witting_orthogonality_equals_symplectic_collinearity":True,
        "triangle_is_exactly_three_history_lines_through_point":True,
        "orientation_histogram":{str(k):v for k,v in sorted(orient.items())},
      },
      "theorem":(
        "After one explicit symplectic gauge rotation, the four computational "
        "Witting axes are exactly the Bell line B of the temporal W33 chart. "
        "Consequently the 36 M36 Witting rays are objectwise the 36 W33 points "
        "off B.  Each such point lies on exactly three of the 27 history lines "
        "disjoint from B, and those three lines are exactly one temporal triangle. "
        "Thus M36 ray_id -> W33 point -> oriented temporal triangle is a certified "
        "bijection, not a cardinality match.  The four M36 nine-ray families are "
        "the four nearest-point fibres over the four Bell-line points."
      ),
      "boundary":(
        "This is an exact finite-geometry dictionary.  It does not identify the "
        "two-qubit/ququart M36 magic resource with a qutrit magic state, and it "
        "does not imply that temporal history itself supplies non-Clifford magic. "
        "Those resource theories remain separately typed."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "family_to_Bell":family_map,
      "orientation_histogram":out["checks"]["orientation_histogram"],
      "residual":out["residual_geometry"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
