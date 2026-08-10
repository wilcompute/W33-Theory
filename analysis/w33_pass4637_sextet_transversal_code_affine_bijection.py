#!/usr/bin/env python3
"""Pass 4637 -- the 64 sextet transversals and 64 section codewords are the same K-set.

Let K (order 2160, Pass4633) stabilize the chosen six-zero-coordinate transversal
inside the corrected Golay sextet.  The 64 choices of one point from each tetrad
split under K as 1+18+45.  The 64 words of the embedded C6 section split as
1+18+45 by weights 0,12,8.

For each nontrivial orbit, an equivariant bijection is determined by the image of
one basepoint.  Exact stabilizer-fixed-point tests give exactly one permissible
image on the 18-orbits and exactly one on the 45-orbits.  Together with Z->0 this
gives a unique K-equivariant bijection of all 64 points and transports the F2^6
addition of C6 to the transversal set.
"""
from __future__ import annotations
import json
from collections import deque
from pathlib import Path
import w33_pass4633_m24_sextet_section_stabilizer as p4633
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4637_SEXTET_TRANSVERSAL_CODE_AFFINE_BIJECTION.json'

def orbits(items,K,action):
    unseen=set(items);out=[]
    while unseen:
        x=min(unseen,key=lambda z:repr(z));O={action(x,g) for g in K};out.append(O);unseen-=O
    return sorted(out,key=len)
def build_map(X,Y,K,ax,ay):
    x=min(X,key=lambda z:repr(z));stab=[g for g in K if ax(x,g)==x]
    fixed=[y for y in Y if all(ay(y,g)==y for g in stab)];assert len(fixed)==1;y=fixed[0]
    phi={}
    for g in K:
        a=ax(x,g);b=ay(y,g)
        if a in phi:assert phi[a]==b
        else:phi[a]=b
    assert set(phi)==set(X) and set(phi.values())==set(Y)
    return phi,len(stab),len(fixed)
def main()->int:
    d=p4633.build();K=d['K'];Z=d['Z'];C6=d['C6'];trans=d['transversal_orbit']
    TX=orbits(trans,K,p4633.act_set);CY=orbits(C6,K,p4633.act_word)
    assert list(map(len,TX))==list(map(len,CY))==[1,18,45]
    assert TX[0]=={Z} and CY[0]=={0}
    phi={Z:0};cert=[]
    for X,Y in zip(TX[1:],CY[1:]):
        m,stab,fixed=build_map(X,Y,K,p4633.act_set,p4633.act_word);phi.update(m);cert.append({'orbit_size':len(X),'base_stabilizer_order':stab,'admissible_fixed_targets':fixed})
    assert len(phi)==64 and len(set(phi.values()))==64
    for g in d['Kgens']:
        assert all(phi[p4633.act_set(x,g)]==p4633.act_word(phi[x],g) for x in trans)
    weights={len(O):{phi[x].bit_count() for x in O} for O in TX};assert weights=={1:{0},18:{12},45:{8}}
    inv={v:k for k,v in phi.items()}
    # transported XOR is a genuine elementary abelian group law.
    assert all(inv[phi[x]^phi[x]]==Z for x in trans)
    out={'pass':4637,'section_group_order':len(K),'transversal_orbits':[1,18,45],'codeword_orbits':[1,18,45],'equivariant_bijection_certificates':cert,'shell_correspondence':{'fixed':'zero transversal <-> zero codeword','18':'transversal orbit <-> weight-12 codewords','45':'transversal orbit <-> weight-8 octads'},'theorem':'There is a unique K-equivariant bijection from the 64 sextet transversals in the chosen orbit to the 64 C6 section codewords, sending the chosen zero transversal to 0. Transporting XOR gives the transversal orbit an F2^6 affine structure.','boundary':'The affine structure is canonical relative to the chosen Golay section/transversal and its K-action; it is not an M24-invariant vector-space structure on all 4096 sextet transversals.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
