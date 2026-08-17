#!/usr/bin/env python3
"""Replay all eight Pass5725--5732 producers and freeze an aggregate summary."""
from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'analysis/w33_pass5726_exact_firewall_jacobiator_rank.py',
 'analysis/w33_pass5725_torsion_center_pairing.py',
 'analysis/w33_pass5727_5730_torsion_family_heisenberg.py',
 'analysis/w33_pass5728_ramanujan_switching_selector.py',
 'analysis/w33_pass5729_family_breaking_lattice.py',
 'analysis/w33_pass5731_5732_mixed_topology_arithmetic.py']
FILES={
 '5725':'PART_W33_PASS5725_TORSION_CENTER_PAIRING.json',
 '5726':'PART_W33_PASS5726_EXACT_FIREWALL_JACOBIATOR_RANK.json',
 '5727':'PART_W33_PASS5727_TORSION_E8_FAMILY_HEISENBERG_INTERTWINER.json',
 '5728':'PART_W33_PASS5728_RAMANUJAN_SWITCHING_INVARIANT_SELECTOR.json',
 '5729':'PART_W33_PASS5729_FAMILY_SYMMETRY_BREAKING_LATTICE.json',
 '5730':'PART_W33_PASS5730_HEISENBERG_QUTRIT_GL23_EXTENDED_CLIFFORD.json',
 '5731':'PART_W33_PASS5731_Z3_Z2_MIXED_EXTENSION_TOPOLOGY.json',
 '5732':'PART_W33_PASS5732_P2_P3_DETERMINANT_ARITHMETIC_BRIDGE.json'}
OUT=ROOT/'data/PART_W33_PASS5725_5732_TORSION_CENTER_HIGHERALGEBRA_SUMMARY.json'
def main():
 for s in SCRIPTS:
  print('===',s,'===',flush=True);subprocess.run([sys.executable,str(ROOT/s)],check=True,cwd=ROOT)
 results={k:json.loads((ROOT/'data'/v).read_text()) for k,v in FILES.items()}
 assert [results[str(p)]['pass'] for p in range(5725,5733)]==list(range(5725,5733))
 out={'passes':list(range(5725,5733)),'status':'EIGHT_PASS_TORSION_CENTER_HIGHERALGEBRA_FAMILY_PACKET_REPLAYED',
  'headline':'Affine (Z/3)^2 torsion has no canonical scalar center character, but its Heisenberg central extension is exactly the qutrit X/Z subgroup already used on the E8 family C^3 factor. The finite family bridge is real; the affine-Lie-SU3 identification remains unproved.',
  'results':results,
  'physics_boundary':'All claims are finite algebra/graph/representation statements. No observed masses, particle identities, confinement, QCD, continuum spacetime, or laboratory result is claimed.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
