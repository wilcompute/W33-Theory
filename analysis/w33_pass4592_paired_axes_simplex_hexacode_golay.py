#!/usr/bin/env python3
"""Pass 4592 -- the two Pass4575 self-orthogonal axes fuse to simplex/Hamming and enter Golay through the hexacode.

Pass4575 gives two rank-six binary evaluation codes from the same natural
O^-(6,2) module U6:
  C36=[36,6,16] on anisotropic vectors,
  C27=[27,6,12] on nonzero singular vectors.
This pass keeps the SAME x in U6 on both axes and concatenates the evaluations.
Every nonzero x has total weight 32, so the paired code is the binary simplex
[63,6,32], dual to Hamming [63,57,3]. Its 63 coordinates are literally all
nonzero vectors of F2^6; the 27|36 split is the minus-quadratic coloring.

For the Golay comparison we use only repository-explicit constructions.  A
standard F4 structure on F2^6 writes a message as (a,b,c) in F4^3 with the
minus quadratic q equal to parity of its F4 Hamming weight.  The standard
hexacode H6=[6,3,4]_4 is encoded by
  (a,b,c,a+b+c,a+w b+w^2 c,a+w^2 b+w c).
Concatenating every F4 symbol with the binary inner simplex [3,2,2] gives a
binary [18,6,8] code with enumerator 1+45 z^8+18 z^12.

The repo's own cyclic extended-Golay constructor (tools/golay_clifford.py) has
an exact six-generator subcode: messages supported on its first six message
bits.  Those 64 G24 words vanish on coordinates 17..22 and restrict on the
remaining 18 coordinates to the same [18,6,8] code.  A frozen 18-coordinate
permutation maps it word-for-word onto the binary hexacode concatenation.
Thus the structural bridge is
  paired cubic axes -> simplex [63,6,32] -> choose compatible F4 structure
  -> hexacode -> binary [18,6,8] -> shortened subcode of G24.
The last six Golay coordinates are not filled by this 6D layer; they are the
extra six MOG positions needed to reach the full 12D Golay code.
"""
from __future__ import annotations
import json,itertools,math
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4592_PAIRED_AXES_SIMPLEX_HEXACODE_GOLAY.json'

# F4 = F2[w]/(w^2+w+1), encoded a+b*w as a+2b.
def f4_add(x,y): return x^y
def f4_mul(x,y):
    a,b=x&1,(x>>1)&1; c,d=y&1,(y>>1)&1
    return (a*c ^ b*d) | (((a*d)^(b*c)^(b*d))<<1)
W=2; W2=f4_mul(W,W)

def qminus_f4_message(m):
    vals=[(m>>(2*i))&3 for i in range(3)]
    return sum(v!=0 for v in vals)&1

def polar(x,y): return qminus_f4_message(x^y)^qminus_f4_message(x)^qminus_f4_message(y)

def eval_word(x,coords):
    z=0
    for j,y in enumerate(coords):
        if polar(x,y): z|=1<<j
    return z

def rank_bits(rows,n):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def enum_code(rows):
    C=set()
    for m in range(1<<len(rows)):
        z=0
        for i,r in enumerate(rows):
            if (m>>i)&1:z^=r
        C.add(z)
    return C

def gf2_mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        a<<=1;b>>=1
    return z

def golay24():
    n=23;g=(1<<11)|(1<<9)|(1<<7)|(1<<6)|(1<<5)|(1<<1)|1
    out=[]
    for msg in range(1<<12):
        cw=gf2_mul(msg,g)
        while cw.bit_length()>n:
            k=cw.bit_length()-1;cw^=1<<k;cw^=1<<(k-n)
        cw|=(cw.bit_count()&1)<<23;out.append(cw)
    return out

def hexaword(a,b,c):
    return (a,b,c,a^b^c,a^f4_mul(W,b)^f4_mul(W2,c),a^f4_mul(W2,b)^f4_mul(W,c))
def inner3(x):
    a,b=x&1,(x>>1)&1;return (a,b,a^b)
def hexacode18():
    out=set();f4weights=Counter()
    for a,b,c in itertools.product(range(4),repeat=3):
        h=hexaword(a,b,c);f4weights[sum(v!=0 for v in h)]+=1
        bits=[]
        for v in h:bits.extend(inner3(v))
        out.add(sum(bit<<i for i,bit in enumerate(bits)))
    return out,f4weights

def restrict_word(x,pos): return sum(((x>>p)&1)<<i for i,p in enumerate(pos))
def permute18(x,p):
    y=0
    for i,j in enumerate(p):
        if (x>>i)&1:y|=1<<j
    return y

def main():
    singular=[x for x in range(1,64) if qminus_f4_message(x)==0]
    anis=[x for x in range(1,64) if qminus_f4_message(x)==1]
    assert (len(singular),len(anis))==(27,36)
    rows36=[];rows27=[];rows63=[]
    for i in range(6):
        x=1<<i; a=eval_word(x,anis);s=eval_word(x,singular)
        rows36.append(a);rows27.append(s);rows63.append(a|(s<<36))
    assert rank_bits(rows36,36)==rank_bits(rows27,27)==rank_bits(rows63,63)==6
    C36,C27,C63=map(enum_code,(rows36,rows27,rows63))
    W36=Counter(x.bit_count() for x in C36);W27=Counter(x.bit_count() for x in C27);W63=Counter(x.bit_count() for x in C63)
    assert W36==Counter({20:36,16:27,0:1})
    assert W27==Counter({12:36,16:27,0:1})
    assert W63==Counter({32:63,0:1})
    # Simplex self-orthogonality and dual minimum 3 are explicit: all 63 nonzero
    # six-bit columns occur once, so no 1/2-column dependency and every x,y,x+y
    # is a weight-3 dependency.
    assert all((u&v).bit_count()%2==0 for u in C63 for v in C63)

    H18,F4W=hexacode18();assert F4W==Counter({4:45,6:18,0:1})
    assert Counter(x.bit_count() for x in H18)==Counter({8:45,12:18,0:1})
    G24=golay24();assert Counter(x.bit_count() for x in G24)==Counter({12:2576,8:759,16:759,0:1,24:1})
    gbasis=[G24[1<<i] for i in range(12)];sub=enum_code(gbasis[:6]);assert len(sub)==64
    zeros=[j for j in range(24) if all(((x>>j)&1)==0 for x in sub)]
    active=[j for j in range(24) if j not in zeros]
    assert zeros==[17,18,19,20,21,22] and len(active)==18
    sub18={restrict_word(x,active) for x in sub}
    assert Counter(x.bit_count() for x in sub18)==Counter({8:45,12:18,0:1})
    # Frozen coordinate equivalence found by exact minimum-word incidence graph isomorphism.
    p=[0,12,2,15,16,11,14,1,9,5,6,3,8,17,4,7,13,10]
    assert sorted(p)==list(range(18))
    assert {permute18(x,p) for x in sub18}==H18

    gl6=(2**6-1)*(2**6-2)*(2**6-4)*(2**6-8)*(2**6-16)*(2**6-32)
    assert gl6==20158709760
    out={'pass':4592,
      'paired_axes':{'C36':'[36,6,16]','C27':'[27,6,12]','same_message_concatenation':'[63,6,32] binary simplex','weight_enumerator':{'0':1,'32':63},'dual':'[63,57,3] binary Hamming','coordinates':'all 63 nonzero vectors of F2^6','quadratic_partition':'27 nonzero singular + 36 anisotropic','simplex_automorphism_group':'GL(6,2)','GL6_2_order':gl6},
      'hexacode':{'parameters':'[6,3,4]_4','codewords':64,'weight_enumerator':{'0':1,'4':45,'6':18},'binary_inner_code':'[3,2,2] simplex per F4 symbol','binary_concatenation':'[18,6,8]','binary_weight_enumerator':{'0':1,'8':45,'12':18}},
      'golay_embedding':{'repo_constructor':'tools/golay_clifford.py cyclic G24','golay_parameters':'[24,12,8]','first_six_message_generators_subcode_dimension':6,'zero_coordinates':zeros,'active_coordinates':active,'shortened_subcode':'[18,6,8]','explicit_active_coordinate_permutation_to_binary_hexacode':p,'word_for_word_verified':True},
      'structural_chain':'paired cubic axes -> simplex/Hamming 63-point geometry -> chosen F4^3 message structure -> hexacode -> binary [18,6,8] -> exact shortened subcode of repo G24',
      'boundary':'The simplex fusion is canonical from the paired axes. The F4/hexacode step requires a choice of compatible F4 structure on the six-space; it is not claimed O^-(6,2)-canonical. The 6D Golay subcode is not the full 12D Golay code.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
