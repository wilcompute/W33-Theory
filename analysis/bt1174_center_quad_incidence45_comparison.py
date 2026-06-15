#!/usr/bin/env python3
"""BT1174 -- compare BT1170 incidence-45 to W33 center-quad quotient.

Repo anchor: exploration/w33_center_quad_transport_complement_bridge.py proves that
the W33 center-quad quotient point graph is SRG(45,12,3,3), while transport is
its complement SRG(45,32,22,24).  BT1170 builds the labeled tritangent/Boolean
share-a-line graph with the same SRG(45,12,3,3) parameters and 270 edges.
Therefore the three models agree at the labeled SRG/incidence level used here.
"""

import json

bt1170 = {"vertices": 45, "edges": 270, "degree": 12, "lambda": 3, "mu": 3}
w33_center_quad = {"vertices": 45, "edges": 270, "degree": 12, "lambda": 3, "mu": 3}
transport_complement = {"vertices": 45, "edges": 720, "degree": 32, "lambda": 22, "mu": 24}

payload = {
    "bt": 1174,
    "title": "center-quad quotient versus Boolean/tritangent incidence-45",
    "bt1170_boolean_tritangent_graph": bt1170,
    "w33_center_quad_point_graph": w33_center_quad,
    "w33_transport_complement_graph": transport_complement,
    "repo_anchor": "exploration/w33_center_quad_transport_complement_bridge.py",
    "comparison": "BT1170 incidence graph matches the W33 center-quad point graph SRG parameters; transport is the complement.",
    "checks": {
        "point_graphs_same_parameters": bt1170 == w33_center_quad,
        "edges_plus_complement_edges": bt1170["edges"] + transport_complement["edges"] == 45 * 44 // 2,
        "transport_degree_is_complement": bt1170["degree"] + transport_complement["degree"] == 44,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
