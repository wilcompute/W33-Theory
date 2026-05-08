#!/usr/bin/env python3
"""PART CCCCXIII -- Toroidal Knight = Q4 Hypercube Packet.

The user caught the key structural upgrade: the 4x4 toroidal-boundary knight
graph used in CCCCXII is the hypercube graph Q4 in disguise.

This matters because the tomotope/chirality packet has exactly 16 slots:

    16 = 2 orientations × 4 tetrahedral chart vertices × 2 chiralities
       = 2 × 2^2 × 2
       = 2^4.

So the packet is naturally a 4-bit hypercube packet.  The toroidal knight tour is
a Gray-code Hamilton cycle on Q4, giving a native hypercube clock/routing order
for packet syndrome extraction.

This compiler verifies:
  - the 4x4 toroidal knight graph has 16 vertices, degree 4, and 32 edges;
  - an explicit labeling identifies it with Q4;
  - every knight edge maps to Hamming distance 1;
  - each hypercube bit dimension contributes exactly 8 edges;
  - the CCCCXII knight tour is a closed Gray-code Hamilton cycle.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BOARD=4
# Explicit graph isomorphism from 4x4 toroidal knight board vertices to Q4 bits.
KNIGHT_TO_Q4={
    (0,0):(0,0,0,0), (2,3):(0,0,0,1), (3,2):(0,0,1,0), (1,1):(0,0,1,1),
    (1,2):(0,1,0,0), (3,1):(0,1,0,1), (2,0):(0,1,1,0), (0,3):(0,1,1,1),
    (2,1):(1,0,0,0), (0,2):(1,0,0,1), (1,3):(1,0,1,0), (3,0):(1,0,1,1),
    (3,3):(1,1,0,0), (1,0):(1,1,0,1), (0,1):(1,1,1,0), (2,2):(1,1,1,1),
}
KNIGHT_TOUR=[(0,0),(1,2),(2,0),(3,2),(1,1),(0,3),(3,1),(2,3),(0,2),(1,0),(2,2),(3,0),(1,3),(0,1),(3,3),(2,1)]
def ok(name, cond, value=None): return {"name":name,"passed":bool(cond),"value":value}
def knight_moves():
    return {(1,2),(3,2),(2,1),(2,3)}
def knight_adj():
    adj={}
    for r,c in itertools.product(range(BOARD), repeat=2):
        adj[(r,c)]=sorted({((r+dr)%BOARD,(c+dc)%BOARD) for dr,dc in knight_moves()})
    return adj
def knight_edges():
    seen=set(); adj=knight_adj()
    for a,ns in adj.items():
        for b in ns: seen.add(tuple(sorted((a,b))))
    return sorted(seen)
def hamming(a,b): return sum(x!=y for x,y in zip(a,b))
def q4_vertices(): return list(itertools.product([0,1], repeat=4))
def q4_edges():
    seen=set()
    for v in q4_vertices():
        for i in range(4):
            w=list(v); w[i]^=1; seen.add(tuple(sorted((v,tuple(w)))))
    return sorted(seen)
def mapped_edges():
    return sorted(tuple(sorted((KNIGHT_TO_Q4[a],KNIGHT_TO_Q4[b]))) for a,b in knight_edges())
def bit_dimension(edge):
    a,b=edge
    dif=[i for i in range(4) if a[i]!=b[i]]
    return dif[0] if len(dif)==1 else None
def dimension_edge_counts():
    counts={i:0 for i in range(4)}
    for e in mapped_edges(): counts[bit_dimension(e)] += 1
    return counts
def tour_bits(): return [KNIGHT_TO_Q4[v] for v in KNIGHT_TOUR]
def tour_flip_sequence():
    bits=tour_bits(); seq=[]
    for i in range(len(bits)):
        dif=[j for j in range(4) if bits[i][j]!=bits[(i+1)%len(bits)][j]]
        seq.append(dif[0] if len(dif)==1 else None)
    return seq
def tour_is_gray_cycle():
    bits=tour_bits()
    return len(bits)==16 and len(set(bits))==16 and all(hamming(bits[i],bits[(i+1)%16])==1 for i in range(16))
def packet_axis_interpretation():
    return {
        "bit_0":"macro orientation/tour half axis",
        "bit_1":"first tetrahedral chart bit",
        "bit_2":"second tetrahedral chart bit",
        "bit_3":"Clifford chirality/local closure bit",
        "factorization":"Q4 bits realize 2 orientation x 2 chart-bit x 2 chart-bit x 2 chirality = 16 slots"
    }
def build_results():
    k_edges=knight_edges(); q_edges=q4_edges(); m_edges=mapped_edges(); checks=[]
    checks.append(ok('4x4 toroidal knight graph has 16 vertices',len(knight_adj())==16,len(knight_adj())))
    checks.append(ok('4x4 toroidal knight graph is 4-regular',sorted({len(v) for v in knight_adj().values()})==[4],sorted({len(v) for v in knight_adj().values()})))
    checks.append(ok('4x4 toroidal knight graph has 32 edges',len(k_edges)==32,len(k_edges)))
    checks.append(ok('Q4 has 16 vertices and 32 edges',len(q4_vertices())==16 and len(q_edges)==32,{"V":len(q4_vertices()),"E":len(q_edges)}))
    checks.append(ok('explicit map is bijective onto Q4 vertices',set(KNIGHT_TO_Q4.values())==set(q4_vertices()) and len(KNIGHT_TO_Q4)==16,KNIGHT_TO_Q4))
    checks.append(ok('mapped knight edges equal Q4 edges',m_edges==q_edges,{"mapped":len(m_edges),"q4":len(q_edges)}))
    checks.append(ok('every knight edge maps to Hamming distance 1',all(hamming(KNIGHT_TO_Q4[a],KNIGHT_TO_Q4[b])==1 for a,b in k_edges),True))
    checks.append(ok('each Q4 bit dimension has 8 edges',dimension_edge_counts()=={0:8,1:8,2:8,3:8},dimension_edge_counts()))
    checks.append(ok('CCCCXII knight tour is a Gray Hamilton cycle',tour_is_gray_cycle(),tour_bits()))
    checks.append(ok('tour flip sequence is hypercube clock',tour_flip_sequence()==[1,2,1,3,1,2,1,0,1,2,1,3,1,2,1,0],tour_flip_sequence()))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCCXIII","title":"Toroidal Knight = Q4 Hypercube Packet","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"hypercube_isomorphism":{"knight_to_q4":{str(k):v for k,v in KNIGHT_TO_Q4.items()},"dimension_edge_counts":dimension_edge_counts(),"packet_axis_interpretation":packet_axis_interpretation()},"gray_cycle":{"knight_tour":KNIGHT_TOUR,"q4_tour":tour_bits(),"flip_sequence":tour_flip_sequence()},"architecture_upgrade":"Corrects and strengthens CCCCXII: the 4x4 toroidal knight routing graph is Q4, so the 16-slot tomotope/chirality packet is a true 4-bit hypercube packet with a Gray-code syndrome/routing clock.","theorem":"The 4x4 toroidal knight graph is isomorphic to the 4-cube Q4 under the explicit labeling in this file. The CCCCXII closed knight tour maps to a Gray-code Hamilton cycle on Q4, with bit-flip sequence 1,2,1,3,1,2,1,0 repeated twice.","honesty_boundary":"This identifies the packet routing graph and hypercube clock. The global W33-to-packet subsystem distance still requires constructing and checking the integrated stabilizer/gauge matrix.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCCXIII_toroidal_knight_hypercube_packet_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
