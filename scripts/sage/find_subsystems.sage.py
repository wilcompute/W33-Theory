#!/usr/bin/env sage
"""Search E8 for subroot systems isomorphic to E6/D5/etc using SageRootSystem utilities."""
from sage.all_cmdline import *
import json
from pathlib import Path

E8 = RootSystem(['E',8])
RS = E8.root_system()
# try to find subsystems
candidates = {}
for t in ['A5','D5','E6']:
    try:
        subs = RS.subsystem(t)
        candidates[t] = {'found': True, 'info': str(type(subs))}
    except Exception as e:
        candidates[t] = {'found': False, 'error': str(e)}

Path('PART_CVII_e8_subsystems_probe.json').write_text(json.dumps(candidates, indent=2))
print('Wrote PART_CVII_e8_subsystems_probe.json')
print(json.dumps(candidates, indent=2))
