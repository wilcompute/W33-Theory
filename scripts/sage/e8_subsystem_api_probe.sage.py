#!/usr/bin/env sage
"""Probe available subsystem APIs for E8 and print outputs for inspection."""

import json
from pathlib import Path

from sage.all_cmdline import *

E8 = RootSystem(["E", 8])
out = {}
try:
    out["root_system_has_subsystems"] = hasattr(E8, "subsystems")
    try:
        out["subsystems_call"] = str(E8.subsystems())
    except Exception as e:
        out["subsystems_call_error"] = str(e)
except Exception as e:
    out["root_system_error"] = str(e)

try:
    RS = E8.root_system()
    out["RS_has_subsystems"] = hasattr(RS, "subsystems")
    try:
        out["RS_subsystems_call"] = str(RS.subsystems())
    except Exception as e:
        out["RS_subsystems_call_error"] = str(e)
except Exception as e:
    out["RS_error"] = str(e)

try:
    RL = E8.root_lattice()
    out["RL_has_subsystems"] = hasattr(RL, "subsystems")
    try:
        out["RL_subsystems_call"] = str(RL.subsystems())
    except Exception as e:
        out["RL_subsystems_call_error"] = str(e)
except Exception as e:
    out["RL_error"] = str(e)

try:
    out["attempt_subsystem_E6"] = None
    try:
        sub = E8.subsystem("E6")
        out["attempt_subsystem_E6"] = "ok"
    except Exception as e:
        out["attempt_subsystem_E6_error"] = str(e)
except Exception as e:
    out["attempt_subsystem_outer_error"] = str(e)

Path("PART_CVII_e8_subsystem_api_probe.json").write_text(json.dumps(out, indent=2))
print("Wrote PART_CVII_e8_subsystem_api_probe.json")
print(json.dumps(out, indent=2))
