#!/usr/bin/env python3
"""Pass5114: exact natural-order ladder in Q(sqrt(17))."""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5114_SQRT17_ORDER_LADDER.json'

def main():
    # lambda^2=lambda+4.  Column-vector multiplication matrices in natural bases.
    M1=sp.Matrix([[0,4],[1,1]])                 # lambda on (1,lambda)
    M2=sp.Matrix([[0,16],[1,2]])                # alpha=2lambda on (1,2lambda)
    B4=sp.Matrix([[0,64],[1,4]])                # beta=4lambda on (1,4lambda)
    Mmu=B4+10*sp.eye(2)                         # mu=10+4lambda
    P12=sp.diag(1,2);P24=sp.diag(1,2);P14=sp.diag(1,4)
    x=sp.symbols('x')
    assert M1.charpoly(x).as_expr()==x**2-x-4
    assert M2.charpoly(x).as_expr()==x**2-2*x-16
    assert Mmu.charpoly(x).as_expr()==x**2-24*x+76
    assert 2*M1*P12==P12*M2
    assert 2*M2*P24==P24*B4
    assert P12*P24==P14
    discs=[17,4*17,16*17]
    global12=2**15;global24=2**15;global14=4**15
    out={'pass':5114,'status':'THEOREM_EXACT_CONDUCTOR_1_2_4_ORDER_LADDER',
         'field':'Q(sqrt(17))','lambda':'(1+sqrt(17))/2','relation':'lambda^2=lambda+4',
         'orders':[
           {'conductor':1,'basis':['1','lambda'],'generator':'lambda','matrix':M1.tolist(),'discriminant':discs[0]},
           {'conductor':2,'basis':['1','2 lambda'],'generator':'alpha=2 lambda','matrix':M2.tolist(),'discriminant':discs[1],'repo_role':'global theta quadratic companion from Pass5087/5104'},
           {'conductor':4,'basis':['1','4 lambda'],'generator':'mu=10+4 lambda','matrix':Mmu.tolist(),'discriminant':discs[2],'repo_role':'q3 recurrence polynomial x^2-24x+76 from Pass5091'}],
         'inclusions':{'O2_into_O1':P12.tolist(),'index_O1_over_O2':2,'O4_into_O2':P24.tolist(),'index_O2_over_O4':2,'O4_into_O1':P14.tolist(),'index_O1_over_O4':4},
         'intertwining_identities':['(2 M1) P12 = P12 M2','(2 M2) P24 = P24 B4','Mmu=B4+10 I'],
         'global_15_lane_indices':{'O1_over_O2':global12,'O2_over_O4':global24,'O1_over_O4':global14},
         'synthesis':'The discriminant ladder 17->68->272 is literally the nested order chain Z+4 O_K subset Z+2 O_K subset O_K. Pass5104 supplies the minimal index-2 integral Hecke-to-theta intertwiner on each lane; this pass adds the natural conductor-four recurrence lattice and both inclusion matrices.',
         'boundary':'This is an exact quadratic-order/lattice identification. It does not identify the historical transfer construction geometrically with W33 apartments.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
