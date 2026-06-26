# BT1810: W(E6)/Schlaefli stabilizer test for the three-table hinged defect.
# Run from repository root with:
#   sage analysis/bt1810_we6_hinged_path_orbit_test.sage
from pathlib import Path
import json

edges=[]
for line in Path('data/bt1806_schlafli_graph.dimacs').read_text().splitlines():
    if line.startswith('e '):
        _,u,v=line.split(); edges.append((int(u)-1,int(v)-1))

tritangent_supports = [[0,1,2],[9,10,11],[18,19,20],[0,3,6],[0,4,8],[0,5,7],[1,16,22],[1,17,21],[1,15,23],[2,14,26],[2,12,25],[2,13,24],[9,12,15],[18,21,24],[9,13,17],[18,22,26],[9,14,16],[18,23,25],[3,13,23],[3,10,26],[3,16,20],[4,14,21],[4,10,25],[4,15,20],[5,12,22],[5,10,24],[5,17,20],[6,17,25],[6,11,22],[6,14,19],[8,16,24],[8,11,23],[8,12,19],[7,15,26],[7,11,21],[7,13,19],[0,9,18],[1,10,19],[2,11,20],[3,12,21],[4,13,22],[5,14,23],[6,15,24],[7,16,25],[8,17,26]]

bt1795_image = [5,7,10,12,15,18,20,22,29,30,34,36,37,38,40,41,42,44]
defect = tuple(sorted([10,22,44]))
table_support = {'T010':10, 'T210':22, 'T222':44}

G=Graph(edges)
A=G.automorphism_group()
lookup={tuple(sorted(t)):i for i,t in enumerate(tritangent_supports)}

def support_action(g, idx):
    img=tuple(sorted([g(v) for v in tritangent_supports[idx]]))
    return lookup[img]

stab=[]
for g in A:
    image=set(support_action(g,i) for i in bt1795_image)
    if image==set(bt1795_image):
        stab.append(g)

defect_orbit=sorted(set(tuple(sorted(support_action(g,i) for i in defect)) for g in stab))

payload={
  'bt':'BT1810',
  'title':'W(E6) stabilizer orbit test for hinged defect path',
  'schlaefli_aut_order': int(A.order()),
  'bt1795_image_size': len(bt1795_image),
  'stabilizer_size': len(stab),
  'defect_table_support_indices': table_support,
  'defect_support_set': list(defect),
  'defect_orbit_size_under_image_stabilizer': len(defect_orbit),
  'defect_orbit': [list(x) for x in defect_orbit],
  'interpretation': 'If the orbit size is tiny, the hinged defect is distinguished by the transported Schlaefli/E6 stabilizer. If it is large or generic among 3-subsets of the 18-image, the defect is transport gauge rather than the missing fibre law.'
}
Path('data').mkdir(exist_ok=True)
Path('data/bt1810_we6_hinged_path_orbit_test.json').write_text(json.dumps(payload, indent=2, sort_keys=True))
print(json.dumps(payload, indent=2, sort_keys=True))
