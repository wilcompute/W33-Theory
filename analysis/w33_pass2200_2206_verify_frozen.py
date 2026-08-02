#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=[
 'data/w33_pass2201_2202_all_q_regular_spread_scheme.json',
 'data/w33_pass2203_ree_tits_nonregular_control.json',
 'data/w33_pass2200_2204_2205_quadratic_controller_audit.json',
 'data/w33_pass2206_rtl_reference.json']
EXPECTED=['4b8b08837e00d7f440950fa29049d49409986355568ed5cf9bb860aa4220b939','7e1eaac9fec07d0dcb821855c12722177485cdc524df49f6c1448f17b30a03db','f385072260077f141cb89ad75c1657b5d238ec7646ea3c0ef7862c647955fece','a20a186134409abe976b84312785435fe5906a72dc38b6071251810fa657180d']
seen=[]
for path,want in zip(FILES,EXPECTED):
 d=json.loads((ROOT/path).read_text());got=d['sha256_without_hash_field'];assert got==want,(path,got,want);seen.append(got)
aggregate=hashlib.sha256(''.join(seen).encode()).hexdigest()
assert aggregate=='84af8784ec8c3109632e519d9a5278a26735466d358b46453016bf03b895b3c7'
print('Passes 2200-2206 frozen certificates: PASS (4/4)')
print('aggregate semantic SHA-256:',aggregate)
