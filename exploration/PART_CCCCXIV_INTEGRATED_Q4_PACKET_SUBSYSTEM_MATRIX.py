#!/usr/bin/env python3
"""PART CCCCXIV -- Integrated Q4 Packet Subsystem Matrix.

CCCCXIII identified the 16-slot tomotope/chirality packet with Q4, the 4-cube.
This part builds the explicit global subsystem matrix for the 81-packet layer and
keeps the W33 attachment map alongside it.

Packet model:
  - one Q4/Bacon-Shor packet per independent W33 line-star matter representative;
  - 81 packets total;
  - 16 physical slots per packet;
  - total n = 1296;
  - each packet is [[16,1,4]] subsystem;
  - global independent packet layer is [[1296,81,4]] subsystem;
  - line-star replacement target is d >= 3*4 = 12 once the attachment is used as
    a true replacement of each W33 weight-3 matter representative.

This compiler constructs:
  - global X gauge rows;
  - global Z gauge rows;
  - global X stabilizer-center rows;
  - global Z stabilizer-center rows;
  - selected 81 independent W33 line-star representatives;
  - attachment records mapping each W33 representative's 3 base edges to 3 Q4
    packet columns of weight 4, with a fourth closure column.

Honesty boundary:
This file proves the global packet-layer subsystem ranks and distance.  It also
constructs the attachment metadata.  It does not yet prove the full combined
W33+packet subsystem distance under all allowed dressed logicals; that requires
the next dressed-logical verifier.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
ROWS=4
COLS=4
SLOTS=16
PACKETS=81
Vector=Tuple[int,int,int,int]

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
        if omega(pts[i],pts[j])==0:
            adj[i].add(j); adj[j].add(i)
    return pts,adj
def edges(adj): return [(i,j) for i in range(len(adj)) for j in sorted(adj[i]) if i<j]
def bit(indices):
    x=0
    for i in indices: x ^= (1<<i)
    return x
def gf2_basis(rows):
    basis={}
    for row in rows:
        x=row
        while x:
            p=x.bit_length()-1
            if p not in basis:
                basis[p]=x; break
            x ^= basis[p]
    return basis
def reduce_by_basis(row,basis):
    x=row
    while x:
        p=x.bit_length()-1
        if p not in basis: return x
        x ^= basis[p]
    return 0
def commute_xz(xrows,zrows): return all(((x&z).bit_count()%2)==0 for x in xrows for z in zrows)

def global_slot(packet,r,c): return packet*SLOTS + r*COLS + c
def column_support(packet,c): return [global_slot(packet,r,c) for r in range(ROWS)]
def row_support(packet,r): return [global_slot(packet,r,c) for c in range(COLS)]

def packet_layout(packet=0):
    return [{"global_slot":global_slot(packet,r,c),"packet":packet,"chart_row":r,"column":c,"orientation":c//2,"chirality":c%2,"q4_bits":q4_bits_from_row_col(r,c)} for r in range(ROWS) for c in range(COLS)]

def q4_bits_from_row_col(r,c):
    # Packet axis convention from CCCCXIII: orientation bit, two chart bits, chirality bit.
    return ((c//2)&1, (r>>1)&1, r&1, c&1)

def packet_x_gauge(packet):
    return [bit([global_slot(packet,r,c),global_slot(packet,r,c+1)]) for r in range(ROWS) for c in range(COLS-1)]
def packet_z_gauge(packet):
    return [bit([global_slot(packet,r,c),global_slot(packet,r+1,c)]) for r in range(ROWS-1) for c in range(COLS)]
def packet_x_center(packet):
    return [bit(global_slot(packet,r,c0) for r in range(ROWS) for c0 in (c,c+1)) for c in range(COLS-1)]
def packet_z_center(packet):
    return [bit(global_slot(packet,r0,c) for r0 in (r,r+1) for c in range(COLS)) for r in range(ROWS-1)]
def global_matrices():
    Xg=[]; Zg=[]; Xs=[]; Zs=[]
    for p in range(PACKETS):
        Xg.extend(packet_x_gauge(p)); Zg.extend(packet_z_gauge(p)); Xs.extend(packet_x_center(p)); Zs.extend(packet_z_center(p))
    return Xg,Zg,Xs,Zs

def x_centralizer_basis_packet(packet):
    return [bit(column_support(packet,c)) for c in range(COLS)]
def z_centralizer_basis_packet(packet):
    return [bit(row_support(packet,r)) for r in range(ROWS)]
def min_packet_logical_weight():
    # Same for every packet. Enumerate centralizer spans modulo center rows.
    Xc=x_centralizer_basis_packet(0); Zc=z_centralizer_basis_packet(0); Xs=packet_x_center(0); Zs=packet_z_center(0)
    bx=gf2_basis(Xs); bz=gf2_basis(Zs)
    def min_w(cent,basis):
        best=None; witness=None
        for mask in range(1,1<<len(cent)):
            v=0
            for i,row in enumerate(cent):
                if (mask>>i)&1: v^=row
            if reduce_by_basis(v,basis)!=0:
                w=v.bit_count()
                if best is None or w<best: best=w; witness=v
        return best,witness
    dx,xw=min_w(Xc,bx); dz,zw=min_w(Zc,bz)
    return {"d_X":dx,"d_Z":dz,"d":min(dx,dz),"x_witness_weight":xw.bit_count(),"z_witness_weight":zw.bit_count()}

def k4_lines(adj):
    return sorted(tuple(q) for q in itertools.combinations(range(len(adj)),4) if all(j in adj[i] for i,j in itertools.combinations(q,2)))
def vertex_x_rows(adj,eidx):
    return [bit(eidx[tuple(sorted((v,w)))] for w in adj[v]) for v in range(len(adj))]
def line_star_rows(adj,eidx):
    rows=[]; meta=[]
    for line in k4_lines(adj):
        for center in line:
            others=[u for u in line if u!=center]
            eds=[tuple(sorted((center,u))) for u in others]
            rows.append(bit(eidx[e] for e in eds))
            meta.append({"line":line,"center":center,"other_vertices":others,"edges":eds})
    return rows,meta
def select_81_line_stars():
    pts,adj=build_graph(); E=edges(adj); eidx={e:i for i,e in enumerate(E)}; Hx=vertex_x_rows(adj,eidx); L,meta=line_star_rows(adj,eidx)
    basis=gf2_basis(Hx); selected=[]
    for row,m in zip(L,meta):
        if reduce_by_basis(row,basis)!=0:
            # add to basis
            x=row
            while x:
                p=x.bit_length()-1
                if p not in basis:
                    basis[p]=x; break
                x^=basis[p]
            selected.append({"row":row,"meta":m})
        if len(selected)==81: break
    return {"E":E,"selected":selected,"initial_rank":39,"final_rank":len(basis),"k4_lines":len(k4_lines(adj)),"all_line_stars":len(L)}

def attachment_map():
    sel=select_81_line_stars(); out=[]
    for i,item in enumerate(sel['selected']):
        edge_columns=[]
        for col,e in enumerate(item['meta']['edges']):
            edge_columns.append({"base_edge":e,"packet_column":col,"support":column_support(i,col),"support_weight":4})
        out.append({"matter_index":i,"packet_index":i,"line_star":item['meta'],"edge_columns":edge_columns,"closure_column":{"packet_column":3,"support":column_support(i,3),"support_weight":4}})
    return out

def build_results():
    Xg,Zg,Xs,Zs=global_matrices(); lg=min_packet_logical_weight(); sel=select_81_line_stars(); attachments=attachment_map(); center_rank=len(gf2_basis(Xs))+len(gf2_basis(Zs)); gauge_row_rank=len(gf2_basis(Xg))+len(gf2_basis(Zg)); gauge_qubits=(gauge_row_rank-center_rank)//2; k=PACKETS*SLOTS-center_rank-gauge_qubits
    checks=[]
    checks.append(ok('global physical slots = 1296',PACKETS*SLOTS==1296,PACKETS*SLOTS))
    checks.append(ok('global center rank = 486',center_rank==486,center_rank))
    checks.append(ok('global gauge row rank = 1944',gauge_row_rank==1944,gauge_row_rank))
    checks.append(ok('global gauge qubits = 729',gauge_qubits==729,gauge_qubits))
    checks.append(ok('global protected k = 81',k==81,k))
    checks.append(ok('packet distance = 4',lg['d']==4 and lg['d_X']==4 and lg['d_Z']==4,lg))
    checks.append(ok('center commutes',commute_xz(Xs,Zs),True))
    checks.append(ok('81 independent W33 line-stars selected',len(sel['selected'])==81 and sel['final_rank']==120,{"selected":len(sel['selected']),"final_rank":sel['final_rank']}))
    checks.append(ok('81 attachments built',len(attachments)==81,len(attachments)))
    checks.append(ok('each attachment has replacement weight 12',all(sum(e['support_weight'] for e in a['edge_columns'])==12 for a in attachments),attachments[0]))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCCXIV","title":"Integrated Q4 Packet Subsystem Matrix","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"global_packet_subsystem":{"n":1296,"k":k,"d_packet_layer":lg['d'],"gauge_qubits":gauge_qubits,"center_rank":center_rank,"gauge_row_rank":gauge_row_rank,"notation":"[[1296,81,4]] packet subsystem layer"},"matrix_counts":{"X_gauge_rows":len(Xg),"Z_gauge_rows":len(Zg),"X_center_rows":len(Xs),"Z_center_rows":len(Zs),"X_gauge_rank":len(gf2_basis(Xg)),"Z_gauge_rank":len(gf2_basis(Zg)),"X_center_rank":len(gf2_basis(Xs)),"Z_center_rank":len(gf2_basis(Zs))},"attachment_summary":{"selected_line_star_reps":len(sel['selected']),"k4_lines":sel['k4_lines'],"all_line_stars":sel['all_line_stars'],"attachments":len(attachments),"replacement_weight_target":12,"sample_attachments":attachments[:2]},"packet_layout_sample":packet_layout(0),"architecture_upgrade":"Builds the explicit global 81-packet Q4/Bacon-Shor subsystem matrices and attaches the selected W33 line-star matter representatives to packet columns. This realizes the [[1296,81,4]] packet layer and the 12-weight line-star replacement target at the matrix/metadata level.","theorem":"The 81 independent Q4/Bacon-Shor packets have 1296 physical slots, center rank 486, gauge-row rank 1944, 729 gauge qubits, and 81 protected logical degrees. Each selected W33 line-star matter representative attaches to three weight-4 packet columns, giving replacement weight 12.","honesty_boundary":"This proves the independent packet subsystem matrix and attachment map. The final claim [[1296,81,>=12]] requires the next dressed-logical verifier over the integrated attachment model.","checks":checks}

def main():
    r=build_results(); out=ROOT/'PART_CCCCXIV_integrated_q4_packet_subsystem_matrix_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"notation":r['global_packet_subsystem']['notation'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
