# BT1806 Sage orbit export. Run from repository root with: sage analysis/bt1806_schlafli_orbit_export.sage
from pathlib import Path
edges=[]
for line in Path('data/bt1806_schlafli_graph.dimacs').read_text().splitlines():
    if line.startswith('e '):
        _,u,v=line.split(); edges.append((int(u)-1,int(v)-1))
tritangent_supports = [[0,1,2],[9,10,11],[18,19,20],[0,3,6],[0,4,8],[0,5,7],[1,16,22],[1,17,21],[1,15,23],[2,14,26],[2,12,25],[2,13,24],[9,12,15],[18,21,24],[9,13,17],[18,22,26],[9,14,16],[18,23,25],[3,13,23],[3,10,26],[3,16,20],[4,14,21],[4,10,25],[4,15,20],[5,12,22],[5,10,24],[5,17,20],[6,17,25],[6,11,22],[6,14,19],[8,16,24],[8,11,23],[8,12,19],[7,15,26],[7,11,21],[7,13,19],[0,9,18],[1,10,19],[2,11,20],[3,12,21],[4,13,22],[5,14,23],[6,15,24],[7,16,25],[8,17,26]]
bt1795_image = [5,7,10,12,15,18,20,22,29,30,34,36,37,38,40,41,42,44]
G = Graph(edges)
print('Schlaefli order/size/aut_order:', G.order(), G.size(), G.automorphism_group().order())
# Next: induce the automorphism action on tritangent_supports and compute the orbit/stabilizer of set(bt1795_image).
