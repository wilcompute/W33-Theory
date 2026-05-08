#!/usr/bin/env python3
"""PART CCCCXII -- Toroidal Knight Packet Attachment Compiler.

CCCCXI constructed the 16-slot tomotope/chirality packet as a 4x4 Bacon-Shor
subsystem code:

    rows    = 4 tetrahedral chart vertices,
    columns = 2 orientations x 2 chiralities.

This part adds the requested 4x4 toroidal-boundary knight board as the packet's
routing/syndrome schedule, then attaches the W33 line-star matter basis to the
81 packet copies.

Key points:
  - The 4x4 toroidal knight graph has 16 vertices, degree 4, and 32 edges.
  - It admits a closed Hamilton tour through all 16 packet slots.
  - The tour gives a native cyclic measurement/routing order for each packet.
  - The W33 line-star sector modulo vertex checks has rank 81.
  - We choose 81 independent line-star representatives and attach each to one
    16-slot packet.
  - Each weight-3 line-star representative is replaced by three full packet
    columns of weight 4, giving a target representative weight 12.

This is the integrated attachment compiler target.  It still does not claim the
full global subsystem distance proof; it constructs the attachment map and the
packet routing schedule that the next global-distance compiler must verify.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
BOARD=4
PACKET_SLOTS=16
PACKETS=81
Vector=Tuple[int,int,int,int]
KNIGHT_TOUR=[(0,0),(1,2),(2,0),(3,2),(1,1),(0,3),(3,1),(2,3),(0,2),(1,0),(2,2),(3,0),(1,3),(0,1),(3,3),(2,1)]

def ok(name, cond, value=None): return {"name":name,"passed":bool(cond),"value":value}
def mul(a,u): return tuple((a*u[i])%MOD for i in range(4))
def omega(x,y): return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%MOD
def canon(v):
    for a in v:
        if a%MOD: return mul(1 if a==1 else 2,v)
    raise ValueError('zero')
def points():
    pts=[]; seen=set()
    for v in itertools.product(range(MOD), repeat=4):
        if v==(0,0,0,0): continue
        c=canon(v)
        if c not in seen: seen.add(c); pts.append(c)
    return pts
def build_graph():
    pts=points(); adj=[set() for _ in pts]
    for i,j in itertools.combinations(range(len(pts)),2):
        if omega(pts[i],pts[j])==0: adj[i].add(j); adj[j].add(i)
    return pts,adj
def edges(adj): return [(i,j) for i in range(len(adj)) for j in sorted(adj[i]) if i<j]
def bit(indices):
    x=0
    for i in indices: x ^= (1<<i)
    return x
def add_to_basis(basis,row):
    x=row
    while x:
        p=x.bit_length()-1
        if p not in basis:
            basis[p]=x; return True
        x ^= basis[p]
    return False
def reduce_by_basis(row,basis):
    x=row
    while x:
        p=x.bit_length()-1
        if p not in basis: return x
        x ^= basis[p]
    return 0
def gf2_basis(rows):
    b={}
    for r in rows: add_to_basis(b,r)
    return b
def k4_lines(adj):
    return sorted(tuple(q) for q in itertools.combinations(range(len(adj)),4) if all(j in adj[i] for i,j in itertools.combinations(q,2)))
def line_star_rows(adj,eidx):
    rows=[]; meta=[]
    for line in k4_lines(adj):
        for center in line:
            others=[u for u in line if u!=center]
            eds=[tuple(sorted((center,u))) for u in others]
            rows.append(bit(eidx[e] for e in eds))
            meta.append({"line":line,"center":center,"other_vertices":others,"edges":eds})
    return rows,meta
def vertex_x_rows(adj,eidx):
    return [bit(eidx[tuple(sorted((v,w)))] for w in adj[v]) for v in range(len(adj))]
def select_81_line_star_basis():
    pts,adj=build_graph(); E=edges(adj); eidx={e:i for i,e in enumerate(E)}; Hx=vertex_x_rows(adj,eidx); L,meta=line_star_rows(adj,eidx)
    basis=gf2_basis(Hx); selected=[]
    initial_rank=len(basis)
    for row,m in zip(L,meta):
        if reduce_by_basis(row,basis)!=0:
            add_to_basis(basis,row)
            selected.append({"row":row,"meta":m})
        if len(selected)==81: break
    return {"E":E,"adj":adj,"selected":selected,"initial_rank":initial_rank,"final_rank":len(basis),"k4_lines":len(k4_lines(adj)),"all_line_stars":len(L)}
def packet_slot(row,col): return row*BOARD+col
def packet_layout():
    return [{"slot":packet_slot(r,c),"row_chart_vertex":r,"column":c,"orientation":c//2,"chirality":c%2} for r in range(BOARD) for c in range(BOARD)]
def knight_moves():
    return sorted({(1,2),(3,2),(2,1),(2,3)})
def knight_adj():
    moves=knight_moves(); adj={}
    for r,c in itertools.product(range(BOARD),repeat=2):
        adj[(r,c)]=sorted({((r+dr)%BOARD,(c+dc)%BOARD) for dr,dc in moves})
    return adj
def knight_edges():
    adj=knight_adj(); seen=set()
    for a,ns in adj.items():
        for b in ns:
            seen.add(tuple(sorted((a,b))))
    return sorted(seen)
def is_knight_edge(a,b):
    return b in knight_adj()[a]
def tour_slots(): return [packet_slot(r,c) for r,c in KNIGHT_TOUR]
def tour_valid():
    return len(KNIGHT_TOUR)==16 and len(set(KNIGHT_TOUR))==16 and all(is_knight_edge(KNIGHT_TOUR[i],KNIGHT_TOUR[(i+1)%16]) for i in range(16))
def column_support(col): return [packet_slot(r,col) for r in range(BOARD)]
def attachment_map():
    sel=select_81_line_star_basis(); attachments=[]
    for i,item in enumerate(sel['selected']):
        edge_to_column=[]
        for col,e in enumerate(item['meta']['edges']):
            edge_to_column.append({"base_edge":e,"packet_column":col,"packet_support":column_support(col)})
        attachments.append({"matter_index":i,"line_star":item['meta'],"packet_index":i,"edge_to_column":edge_to_column,"closure_column":{"packet_column":3,"role":"orientation/chirality closure column","packet_support":column_support(3)},"knight_tour_slots":tour_slots()})
    return attachments
def build_results():
    sel=select_81_line_star_basis(); kadj=knight_adj(); kedges=knight_edges(); attachments=attachment_map(); checks=[]
    checks.append(ok('4x4 toroidal knight board has 16 vertices',len(kadj)==16,len(kadj)))
    checks.append(ok('toroidal knight degree is 4',sorted({len(v) for v in kadj.values()})==[4],sorted({len(v) for v in kadj.values()})))
    checks.append(ok('toroidal knight edge count is 32',len(kedges)==32,len(kedges)))
    checks.append(ok('closed Hamilton knight tour valid',tour_valid(),KNIGHT_TOUR))
    checks.append(ok('packet layout has 16 slots',len(packet_layout())==16,packet_layout()))
    checks.append(ok('selected 81 line-star representatives',len(sel['selected'])==81,len(sel['selected'])))
    checks.append(ok('line-star quotient rank raises basis from 39 to 120',sel['initial_rank']==39 and sel['final_rank']==120,{"initial":sel['initial_rank'],"final":sel['final_rank']}))
    checks.append(ok('attachment count = 81',len(attachments)==81,len(attachments)))
    checks.append(ok('each attachment maps 3 base edges to 3 packet columns',all(len(a['edge_to_column'])==3 for a in attachments),attachments[0]))
    checks.append(ok('replacement support target weight = 12',sum(len(x['packet_support']) for x in attachments[0]['edge_to_column'])==12,attachments[0]['edge_to_column']))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCCXII","title":"Toroidal Knight Packet Attachment Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"toroidal_knight_board":{"vertices":16,"degree":4,"edges":32,"closed_hamilton_tour":KNIGHT_TOUR,"tour_slots":tour_slots(),"role":"packet routing/syndrome schedule on the 4x4 orientation-chart-chirality board"},"packet_layout":packet_layout(),"line_star_basis_summary":{"k4_lines":sel['k4_lines'],"all_line_stars":sel['all_line_stars'],"selected_matter_representatives":len(sel['selected']),"vertex_rank":sel['initial_rank'],"final_rank_with_selected":sel['final_rank']},"attachment_summary":{"packets":len(attachments),"slots_per_packet":16,"total_slots":16*len(attachments),"base_edges_per_matter_degree":3,"packet_column_weight":4,"replacement_weight_target":12,"sample_attachments":attachments[:3]},"architecture_upgrade":"Adds the integrated W33-to-tomotope packet attachment map: choose 81 independent line-star matter representatives, attach each to one 16-slot 4x4 packet, and use a closed toroidal knight tour as the packet routing/syndrome schedule.","theorem":"The 4x4 toroidal knight graph is 4-regular on 16 packet slots and has a closed Hamilton tour. The W33 line-star sector admits 81 independent representatives modulo vertex checks. Mapping each representative's three base edges to three weight-4 packet columns gives a 12-slot replacement target per matter degree, with the fourth column serving as the orientation/chirality closure column.","honesty_boundary":"This constructs the attachment map and routing schedule. It still must be promoted into a full global subsystem stabilizer/gauge matrix before claiming an integrated distance proof.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCCXII_toroidal_knight_packet_attachment_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"total_slots":r['attachment_summary']['total_slots'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
