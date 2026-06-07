#!/usr/bin/env python3
"""BT499: Corrected Seven-Realization Metric Heptad Theorem.

BT498 restored the correct Szilassi coordinate edge carrier from
Toroidal-Polyhedra-Realizations.txt. This reruns the seven-realization edge
metric programme with:
  * 5 Csaszar K7 carriers from the TXT file coordinates/faces
  * 2 Szilassi Heawood carriers from the TXT file coordinates/faces

It explicitly separates true corrected invariants from old parser artifacts.
"""
from __future__ import annotations

import itertools, json, math
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np

CS_FACES=[(0,1,2),(0,2,5),(0,5,4),(0,4,6),(0,6,3),(0,3,1),(1,3,4),(1,4,5),(1,5,6),(1,6,2),(2,6,4),(2,4,3),(2,3,5),(5,3,6)]
SZ_FACES=[(0,1,13,8,7,4),(0,4,3,2,10,12),(0,12,9,6,5,1),(11,3,4,7,6,9),(11,9,12,10,8,13),(11,13,1,5,2,3),(2,5,6,7,8,10)]

# TXT coordinates, with radicals evaluated where needed.
C1={0:(3,-3,-7.5),1:(-3,3,-7.5),2:(3,3,-6.5),3:(-3,-3,-6.5),4:(1,2,-4.5),5:(-1,-2,-4.5),6:(0,0,7.5)}
C0=4*math.sqrt(15)
C2={0:(C0,0,-10),1:(-C0,0,-10),2:(0,8,-6),3:(0,-8,-6),4:(-1,2,1),5:(1,-2,1),6:(0,0,10)}
C0=6*math.sqrt(2)
C3={0:(12,0,-C0),1:(-12,0,-C0),2:(0,C0,0),3:(0,-C0,0),4:(3,-3,-3),5:(-3,3,-3),6:(0,0,C0)}
C0=math.sqrt(2)/2; C1v=8*math.sqrt(2)/3; C2v=6*math.sqrt(2)
C4={0:(12,0,-C2v),1:(-12,0,-C2v),2:(0,12,C2v),3:(0,-12,C2v),4:(-4,-3,C0),5:(4,3,C0),6:(0,0,C1v)}
C0=2*math.sqrt(2); C1v=6*math.sqrt(2)
C5={0:(12,0,-C1v),1:(-12,0,-C1v),2:(0,12,C1v),3:(0,-12,C1v),4:(-3,3,C0),5:(3,-3,C0),6:(0,0,-C0)}
S1={0:(12,0,12),1:(-12,0,12),2:(0,12.6,-12),3:(0,-12.6,-12),4:(2,-5,-8),5:(-2,5,-8),6:(3.75,3.75,-3),7:(-3.75,-3.75,-3),8:(4.5,-2.5,2),9:(-4.5,2.5,2),10:(7,0,2),11:(-7,0,2),12:(7,2.5,2),13:(-7,-2.5,2)}
C0=8/3; C1v=20/3
S2={0:(12,0,12),1:(-12,0,12),2:(0,12,-12),3:(0,-12,-12),4:(1.5,-5.25,-9),5:(-1.5,5.25,-9),6:(C0,4,-4),7:(-C0,-4,-4),8:(C1v,-2,4),9:(-C1v,2,4),10:(8,0,4),11:(-8,0,4),12:(8,2,4),13:(-8,-2,4)}

REALIZATIONS=[('Csaszar TXT v1',C1,CS_FACES),('Csaszar TXT v2',C2,CS_FACES),('Csaszar TXT v3',C3,CS_FACES),('Csaszar TXT v4',C4,CS_FACES),('Csaszar TXT v5',C5,CS_FACES),('Szilassi TXT v1',S1,SZ_FACES),('Szilassi TXT v2',S2,SZ_FACES)]

def edges_from_faces(faces):
    c=Counter()
    for face in faces:
        for i in range(len(face)):
            a,b=face[i],face[(i+1)%len(face)]
            c[tuple(sorted((a,b)))] += 1
    return c

def cs_edges_from_triangles(faces):
    e=set()
    for face in faces:
        for a,b in itertools.combinations(face,2):
            e.add(tuple(sorted((a,b))))
    return Counter({edge:2 for edge in e})

def sq(V,a,b):
    return sum((V[a][i]-V[b][i])**2 for i in range(3))

def packet(name,V,faces):
    if name.startswith('Csaszar'):
        ec=cs_edges_from_triangles(faces)
        expected_graph='K7'
    else:
        ec=edges_from_faces(faces)
        expected_graph='Heawood'
    edges=sorted(ec)
    G=nx.Graph(); G.add_nodes_from(V.keys()); G.add_edges_from(edges)
    vals=[sq(V,a,b) for a,b in edges]
    rounded=[round(v,10) for v in vals]
    if expected_graph=='K7':
        assert len(edges)==21 and nx.is_isomorphic(G,nx.complete_graph(7))
    else:
        assert len(edges)==21 and nx.is_isomorphic(G,nx.heawood_graph()) and Counter(ec.values())==Counter({2:21})
    return {
        'name':name,
        'graph':expected_graph,
        'vertex_count':len(V),
        'edge_count':len(edges),
        'sum_L2':round(sum(vals),10),
        'norm2_L2':round(sum(v*v for v in vals),10),
        'min_L2':round(min(vals),10),
        'max_L2':round(max(vals),10),
        'distinct_L2_count':len(set(rounded)),
        'multiplicity_profile':{str(k):v for k,v in sorted(Counter(rounded).items(), key=lambda kv: float(kv[0]))},
    }

def main():
    packets=[packet(*r) for r in REALIZATIONS]
    all_values=set()
    for p in packets:
        all_values.update(float(k) for k in p['multiplicity_profile'].keys())
    cs_values=set()
    sz_values=set()
    for p in packets[:5]: cs_values.update(float(k) for k in p['multiplicity_profile'].keys())
    for p in packets[5:]: sz_values.update(float(k) for k in p['multiplicity_profile'].keys())
    assert all(p['edge_count']==21 for p in packets)
    assert packets[5]['distinct_L2_count']==12
    assert packets[6]['distinct_L2_count']==11
    results={
        'theorem':'BT499 Corrected Seven-Realization Metric Heptad Theorem',
        'source':'data/Toroidal-Polyhedra-Realizations.txt coordinates and face cycles',
        'correction':'Uses TXT Szilassi faces, not the old 31-edge EDGE_LENGTH_ANALYSIS.py S_FACES parser',
        'realization_packets':packets,
        'heptad_counts':{
            'realizations':7,
            'edge_instances':7*21,
            'corrected_distinct_L2_values_all':len(all_values),
            'corrected_distinct_L2_values_csaszar':len(cs_values),
            'corrected_distinct_L2_values_szilassi':len(sz_values),
            'csaszar_szilassi_intersection_count':len(cs_values & sz_values),
        },
        'comparison_to_old_claims':{
            'old_35_distinct_integer_L2_claim':'parser-dependent; old Szilassi parser was not closed',
            'corrected_all_distinct_L2_count':len(all_values),
            'safe_core':'all seven corrected carriers have 21 edges; Csaszar=K7, Szilassi=Heawood',
        },
        'substrate_reading':{
            '147':'7 corrected realizations times 21 edges',
            '5_plus_2':'five Csaszar K7 metrics plus two Szilassi Heawood metrics',
            'metric_heptad':'coordinate spectra now separated from incidence repair artifacts',
        }
    }
    out=Path('data/PART_BT499_CORRECTED_SEVEN_REALIZATION_METRIC_HEPTAD_results.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))
    return results
if __name__=='__main__': main()
