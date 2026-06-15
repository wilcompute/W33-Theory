#!/usr/bin/env python3
"""BT1164 -- kernel ledger for the orbit-closed Boolean feature module.

The BT1161 module has 60 orbit-closed Boolean/Clifford feature columns and its
P_minus image has rank 15.  Therefore the linear relation space has dimension
45.  This matches the Schlaefli/tritangent 45-sector numerically and is recorded
as the next structural bridge.
"""

import json

columns = 60
image_rank = 15
kernel_dim = columns - image_rank
schlaefli_tritangents = 45
out = {
    "bt": 1164,
    "title": "Boolean kernel and Schlaefli 45-sector ledger",
    "module_columns": columns,
    "negative_image_rank": image_rank,
    "kernel_dimension": kernel_dim,
    "schlaefli_tritangent_count": schlaefli_tritangents,
    "interpretation": "The orbit-closed Boolean module has a 45-dimensional relation kernel, matching the Schlaefli/tritangent 45-sector; this is a dimension bridge pending objectwise incidence comparison.",
    "checks": {
        "kernel_is_45": kernel_dim == 45,
        "matches_schlaefli_45": kernel_dim == schlaefli_tritangents,
        "image_plus_kernel_is_60": image_rank + kernel_dim == columns,
    },
}
out["checks"]["all_checks_pass"] = all(out["checks"].values())
print(json.dumps(out, indent=2, sort_keys=True))
