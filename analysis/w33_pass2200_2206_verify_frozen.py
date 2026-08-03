#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=[
 'data/w33_pass2201_2202_all_q_regular_spread_scheme.json',
 'data/w33_pass2203_ree_tits_nonregular_control.json',
 'data/w33_pass2200_2204_2205_quadratic_controller_audit.json',
 'data/w33_pass2206_rtl_reference.json']
EXPECTED=['4b8b08837e00d7f440950fa29049d49409986355568ed5cf9bb860aa4220b939','7e1eaac9fec07d0dcb821855c12722177485cdc524df49f6c1448f17b30a03db','f385072260077f141cb89ad75c1657b5d238ec7646ea3c0ef7862c647955fece','7df0ec9e6ca32be581725a480ae22cdd623f5e3cce663cacb693aae4bd103a1c']
seen=[]
for path,want in zip(FILES,EXPECTED):
 d=json.loads((ROOT/path).read_text());got=d['sha256_without_hash_field'];assert got==want,(path,got,want);seen.append(got)
aggregate=hashlib.sha256(''.join(seen).encode()).hexdigest()
assert aggregate=='fce0e00046b9553a0ed8d5786b6157fa2342c7ca64893dac7f0ef5621d308fa0'
print('Passes 2200-2206 frozen certificates: PASS (4/4)')
print('aggregate semantic SHA-256:',aggregate)
