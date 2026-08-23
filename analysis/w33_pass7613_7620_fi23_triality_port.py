#!/usr/bin/env python3
"""Pass7613-7620: an exact Fi23 port through O8+(3):S3.

External input is the ATLAS rank-3 action of Fi23 on 137632 points, whose point
stabilizer is O8+(3):S3 and permutation character is 1+30888+106743. Everything
else below is exact arithmetic plus the four-letter S4 subgroup calculation.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7613_7620_FI23_TRIALITY_PORT.json'
ATLAS='https://brauer.maths.qmul.ac.uk/Atlas/v3/permrep/F23G1-p137632B0'

def compose(p,q):return tuple(p[q[i]] for i in range(4))
def main():
    v,k,f,g=137632,28431,30888,106743
    # Rank-3 adjacency eigenvalues from trace(A)=0 and trace(A^2)=vk.
    # The integral solution is r=279, s=-81.
    r,s=279,-81
    assert f*r+g*s==-k
    assert k*k+f*r*r+g*s*s==v*k
    mu=k+r*s;lam=mu+r+s
    assert (lam,mu)==(6030,5832)
    assert k*(k-lam-1)==(v-k-1)*mu

    o8p3=4952179814400;o8p3s3=o8p3*6;e8proj=348364800
    assert o8p3s3==29713078886400 and o8p3s3%e8proj==0 and o8p3s3//e8proj==85293

    # The projective-E8 image in the Pass7517 carrier has outer image C2, a
    # transposition in S4. Count the point-stabilizer S3s of S4 containing it.
    S4=list(itertools.permutations(range(4)));t=(1,0,2,3)
    s3s=[]
    for fixed in range(4):
        H={p for p in S4 if p[fixed]==fixed}
        assert len(H)==6
        if t in H:s3s.append(fixed)
    assert s3s==[2,3]

    out={'schema':'w33.pass7613_7620.fi23_triality_port.v1','status':'PASS','passes':'7613-7620',
      'external_source':ATLAS,'Fi23_action':{'degree':v,'rank':3,'subdegrees':[1,28431,109200],'permutation_character':'1 + 30888 + 106743','point_stabilizer':'O8+(3):S3'},
      'rank3_orbital_srg':{'parameters':[v,k,lam,mu],'spectrum':{'28431':1,'279':f,'-81':g}},
      'projective_E8_port':{'chain':'O8+(2):2 < O8+(3):S3 < Fi23','index_in_O8p3S3':85293,'index_factorization':'3^8 * 13'},
      'outer_choice':{'ambient':'S4','fixed_E8_outer_image':'a transposition','S3_point_stabilizers_containing_it':2,'canonical':False},
      'steinberg_spectral_echo':'The negative rank-3 eigenvalue is exactly -81, the negative of the W33 H1/Steinberg dimension. This is an exact equality but no representation identification is inferred from the number alone.',
      'theorem':'The same D4(3) triality carrier supporting the Monster O8+(3):S4 port has an O8+(3):S3 subport which occurs as the point stabilizer in the ATLAS rank-3 Fi23 action. A fixed projective-E8 outer C2 lies in exactly two such S3 point stabilizers, so the Fi23 port exists but is two-valued rather than canonical.',
      'claim_boundary':'ATLAS subgroup/action data plus exact finite arithmetic. No claim that W33 generates Fi23, and no physical interpretation of -81.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','srg':[v,k,lam,mu],'spectrum':[k,r,s],'S3_choices':2}))
if __name__=='__main__':main()
