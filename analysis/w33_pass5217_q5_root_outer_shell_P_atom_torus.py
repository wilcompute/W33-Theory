#!/usr/bin/env python3
"""Pass5217: explicit q=5 root-controller outer-shell -> P-atom torus map.

Choose the canonical U(5)-fixed chamber from Pass5129 and use state coordinates
u(a,b,c,d)=x0(a)x1(b)x2(c)x3(d).  The 625 apartments through that chamber are
partitioned by Pass5180/5214 into 25 P-minimum atoms of weight 25.

Objectwise computation shows that this atom partition is exactly the coordinate
projection (a,b,c,d)->(a,c): every atom has fixed a,c and all 25 choices of b,d.
Pass5181's q=5 distance-four root shell consists of
(a,b,2ab,2a^2b), a,b nonzero.  Therefore its atom image is exactly the 16
nonzero pairs (a,c) in (F5^*)^2, one outer-shell apartment per atom.  The other
nine chamber-star atoms are the coordinate cross a=0 or c=0.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5129_allq_intrinsic_unipotent_controller import roots,mm,mv,norm,I4
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment,atoms
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5217_Q5_ROOT_OUTER_SHELL_P_ATOM_TORUS.json'

def main():
    q=5;G=build_W(q);U,H,F=roots(q);pidx={p:i for i,p in enumerate(G['pts'])}
    gens=[z for h in H for z in h[1:]]
    fp=[i for i,p in enumerate(G['pts']) if all(pidx[norm(mv(g,p,F),F)]==i for g in gens)]
    fl=[]
    for li,L in enumerate(G['lines']):
        if all(frozenset(pidx[norm(mv(g,G['pts'][p],F),F)] for p in L)==L for g in gens):fl.append(li)
    fixed=[(p,l) for p in fp for l in fl if p in G['lines'][l]];assert len(fixed)==1
    fi=G['flags'].index(fixed[0]);support=[a for a,es in enumerate(G['apt_edges']) if fi in es];assert len(support)==625
    lookup={G['apartments'][a]:a for a in support};base=G['apartments'][support[0]]
    def elem(a,b,c,d):return mm(mm(mm(H[0][a],H[1][b],F),H[2][c],F),H[3][d],F)
    coord_to_ap={}
    for a,b,c,d in itertools.product(range(q),repeat=4):
        g=elem(a,b,c,d);A=frozenset(pidx[norm(mv(g,G['pts'][p],F),F)] for p in base)
        coord_to_ap[(a,b,c,d)]=lookup[A]
    assert len(set(coord_to_ap.values()))==625
    acid,nc=p_component_assignment(G);A,meta,byflag=atoms(G,acid)
    # P atoms lying in the fixed chamber star.
    starset=set(support);SA=[i for i,S in enumerate(A) if S<=starset]
    assert len(SA)==25 and sum(len(A[i]) for i in SA)==625
    ap_to_atom={a:i for i in SA for a in A[i]};assert len(ap_to_atom)==625
    atom_coords=defaultdict(list)
    for x,ap in coord_to_ap.items():atom_coords[ap_to_atom[ap]].append(x)
    assert len(atom_coords)==25
    fiber_to_atom={}
    for u,X in atom_coords.items():
        ac={(x[0],x[2]) for x in X};bd={(x[1],x[3]) for x in X}
        assert len(ac)==1 and len(bd)==25 and len(X)==25
        z=next(iter(ac));assert z not in fiber_to_atom;fiber_to_atom[z]=u
    assert set(fiber_to_atom)==set(itertools.product(range(5),repeat=2))
    outer=[]
    for a in range(1,5):
        for b in range(1,5):
            c=2*a*b%5;d=2*a*a*b%5;x=(a,b,c,d);ap=coord_to_ap[x];u=ap_to_atom[ap]
            outer.append({'state':list(x),'apartment':ap,'atom':u,'atom_fiber':[a,c]})
    assert len({x['atom'] for x in outer})==16
    assert {tuple(x['atom_fiber']) for x in outer}==set(itertools.product(range(1,5),repeat=2))
    cross=set(fiber_to_atom)-set(itertools.product(range(1,5),repeat=2));assert len(cross)==9
    out={'pass':5217,'status':'THEOREM_Q5_ROOT_OUTER_SHELL_IS_NONZERO_P_ATOM_TORUS',
      'q':5,'fixed_chamber':list(fixed[0]),'fixed_chamber_index':fi,
      'apartment_carrier':625,'P_atoms_in_star':25,'atom_weight':25,
      'atom_coordinate_projection':'(a,b,c,d) -> (a,c); each atom fixes (a,c) and contains all 25 (b,d) pairs.',
      'outer_shell_formula':'(a,b,c,d)=(a,b,2ab,2a^2 b), a,b in F5^*',
      'outer_shell_apartments':16,'outer_shell_distinct_atoms':16,
      'outer_atom_image':'exactly (a,c) in (F5^*)^2',
      'complement_atoms':9,'complement_description':'the coordinate cross a=0 or c=0 in F5^2',
      'outer_states':outer,
      'connection':'The first q=5 distance-four controller shell has an explicit image in the chamber-star equality coordinates: a 4x4 nonzero atom torus inside the 5x5 P-atom grid. This is an actual coordinate map, not a cardinality coincidence.',
      'boundary':'The torus/cross decomposition is an exact finite controller/code-coordinate theorem. It does not imply that the outer shell causes the q5 distance difficulty, nor does it by itself classify nonstar weight-625 words or establish a physical identification.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
