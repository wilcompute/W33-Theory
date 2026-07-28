#!/usr/bin/env python3
"""
Pass 1155 (Step 3): Wire the degree-540 species separator into ALIAS_REGISTRY.json.
Patches registry so each degree-540 species carries (rank, TOM id, normalizer order).
Outputs: data/ALIAS_REGISTRY.json (updated), data/REGISTRY_WIRE_2026_07_27.json
"""
import json, pathlib
from datetime import datetime
REPO_ROOT = pathlib.Path(__file__).parent.parent
SPECIES = [
    {'canonical': 'W33_degree540_species_point_nonedge',
     'aliases': ['TOM_77','point-nonedge','degree540_species_1'],
     'tom': 77, 'rank': 25, 'normalizer': 96, 'separator': [25,77,96], 'status': 'confirmed'},
    {'canonical': 'W33_degree540_species_double_six_nonincident',
     'aliases': ['TOM_78','double-six-nonincident','cubic-line-nonincidence','degree540_species_2'],
     'tom': 78, 'rank': 28, 'normalizer': 96, 'separator': [28,78,96], 'status': 'confirmed'},
    {'canonical': 'W33_degree540_species_gq42_arc',
     'aliases': ['TOM_79','gq42-arc','Hashimoto-arc','degree540_species_3'],
     'tom': 79, 'rank': 27, 'normalizer': 96, 'separator': [27,79,96], 'status': 'confirmed'},
    {'canonical': 'W33_degree540_species_outer_4c',
     'aliases': ['TOM_80','outer-4c','restricted-outer-4c','degree540_species_4'],
     'tom': 80, 'rank': 21, 'normalizer': 96, 'separator': [21,80,96], 'status': 'confirmed'},
    {'canonical': 'W33_degree540_species_line_nonedge',
     'aliases': ['TOM_81','line-nonedge','skew-frame','degree540_species_5'],
     'tom': 81, 'rank': 32, 'normalizer': 48, 'separator': [32,81,48], 'status': 'confirmed'},
]
def main():
    reg_path = REPO_ROOT / 'data' / 'ALIAS_REGISTRY.json'
    registry = json.loads(reg_path.read_text())
    existing = {obj['canonical'] for obj in registry['objects']}
    added = []
    for sp in SPECIES:
        if sp['canonical'] not in existing:
            registry['objects'].append(sp); added.append(sp['canonical'])
        else:
            for obj in registry['objects']:
                if obj['canonical'] == sp['canonical']: obj.update(sp)
    registry['version'] = '2026-07-27-v2'
    reg_path.write_text(json.dumps(registry, indent=2))
    diff = {'timestamp': datetime.utcnow().isoformat()+'Z',
        'schema': 'w33.pass1155.separator_registry_wire.v1', 'status': 'PASS',
        'added_entries': added, 'total_entries': len(registry['objects']),
        'separator_policy': 'Each degree-540 object carries (rank, TOM id, normalizer order).'}
    (REPO_ROOT / 'data' / 'REGISTRY_WIRE_2026_07_27.json').write_text(json.dumps(diff, indent=2))
    print('PASS 1155 separator wired, entries total:', len(registry['objects']))
    return diff
if __name__ == '__main__': main()
