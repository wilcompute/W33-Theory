#!/usr/bin/env python3
"""Exact symmetry of the native W33 T(10) fibres and the HJ10 boundary.

The native T(10) pass produced ten nonsingular F2^6 coordinate pairs {x,x+4}.
This pass computes their intrinsic finite symmetry rather than choosing an
arbitrary labeling.

The 36 orthogonal symmetries x -> x + beta(x,r)r generate the full 51,840
isometry group of the frozen six-dimensional quadratic form.  The stabilizer
of the singular translation vector 4 has order 1,920 and acts on the ten
{x,x+4} fibres with image order 120 and kernel order 16.  Intrinsically the
ten fibres carry SRG(10,6,3,4)=T(5): its five maximal K4s are a canonical
five-set, and every fibre belongs to two K4s, giving an explicit bijection with
the ten duads C(5,2).  The action on the five K4s is all S5.

This is exactly the ten-dimensional K5-edge/duad target used by the repository's
older S6->S5 branching gauge, so that old representation-theoretic carrier and
the new code-stratum T(10) carrier are now literally coordinatized together.

For HJ10, the certified residual C2 has cycle profile 1^2 2^4.  In the native
S5 action this is exactly the double-transposition class (15 elements).  Hence
C2-equivariant bijections exist: for any selected target double transposition
there are 2!*4!*2^4=768, and 15*768=11,520 if the target involution is not
selected.  No one of these is canonical from the current HJ data.

The natural P1(F9) projective extension is still obstructed.  Its split
involution centralizer contains an order-eight rotation (D16/C8), while S5 has
no element of order eight.  Thus the exact shared structure currently stops at
the residual C2 unless extra non-normalizer data is supplied.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260828_T10_S5_HJ_INTERTWINER.json'
S=4

def bits(x,n=6):return [(x>>i)&1 for i in range(n)]
def qform(x):
    b=bits(x);return (b[0]*b[1]+b[2]*b[3]+b[4]*b[5]+b[4]+b[5])&1
def beta(x,y):return qform(x^y)^qform(x)^qform(y)
def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def cycle_type(p):
    seen=set();out=[]
    for i in range(len(p)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=p[j]
        out.append(n)
    return tuple(sorted(out))
def order(p):
    z=1
    for n in cycle_type(p):z=math.lcm(z,n)
    return z

def srg(G):
    deg={len(x) for x in G};la=set();mu=set()
    for i,j in itertools.combinations(range(len(G)),2):
        c=len(G[i]&G[j]);(la if j in G[i] else mu).add(c)
    return [len(G),sorted(deg),sorted(la),sorted(mu)]

def main():
    nons=[x for x in range(1,64) if qform(x)]
    assert len(nons)==36 and qform(S)==0
    fibres=sorted({tuple(sorted((x,x^S))) for x in nons if qform(x^S)})
    assert fibres==[(3,7),(16,20),(17,21),(18,22),(32,36),(33,37),(34,38),(48,52),(49,53),(50,54)]
    fi={frozenset(z):i for i,z in enumerate(fibres)}

    def reflection(r):return tuple(x^(r if beta(x,r) else 0) for x in range(64))
    gens=[reflection(r) for r in nons]
    ident=tuple(range(64));grp={ident};q=deque([ident])
    while q:
        p=q.popleft()
        for g in gens:
            h=compose(g,p)
            if h not in grp:grp.add(h);q.append(h)
    assert len(grp)==51840
    stab=[g for g in grp if g[S]==S];assert len(stab)==1920
    image=set()
    for g in stab:
        p=tuple(fi[frozenset((g[a],g[b]))] for a,b in fibres)
        image.add(p)
    assert len(image)==120 and len(stab)//len(image)==16
    assert {p for p in image if all(p[i]==i for i in range(10))}=={tuple(range(10))}

    # Intrinsic T(5) graph on fibres.  The chosen representative is the smaller
    # label; beta is unchanged under the induced S5 action on these ten pairs.
    A=[set() for _ in range(10)]
    for i,j in itertools.combinations(range(10),2):
        if beta(fibres[i][0],fibres[j][0]):A[i].add(j);A[j].add(i)
    assert srg(A)==[10,[6],[3],[4]]
    assert all(all((j in A[i])==(p[j] in A[p[i]]) for i,j in itertools.combinations(range(10),2)) for p in image)
    P=[set(range(10))-{i}-A[i] for i in range(10)];assert srg(P)==[10,[3],[0],[1]]

    K4=[]
    for z in itertools.combinations(range(10),4):
        if all(j in A[i] for i,j in itertools.combinations(z,2)):K4.append(z)
    assert K4==[(0,2,5,8),(0,3,6,9),(1,4,8,9),(1,5,6,7),(2,3,4,7)]
    contain={i:[] for i in range(10)}
    for k,C in enumerate(K4):
        for i in C:contain[i].append(k)
    assert {len(v) for v in contain.values()}=={2}
    duad={i:tuple(sorted(contain[i])) for i in range(10)}
    assert len(set(duad.values()))==10 and set(duad.values())==set(itertools.combinations(range(5),2))
    ki={frozenset(C):i for i,C in enumerate(K4)};act5=set()
    for p in image:
        act5.add(tuple(ki[frozenset(p[i] for i in C)] for C in K4))
    assert act5==set(itertools.permutations(range(5)))

    # The historical S6->S5 gauge literally targets the ten K5 edges.
    branch=(ROOT/'analysis/w33_s6_to_s5_branching_gauge.py').read_text()
    assert 'k5_edges=list(combinations(range(5),2)); n10=10' in branch

    cprof=Counter(cycle_type(p) for p in image)
    expected={
      (1,1,1,1,1,1,1,1,1,1):1,
      (1,1,1,1,2,2,2):10,
      (1,1,2,2,2,2):15,
      (1,3,3,3):20,
      (1,3,6):20,
      (2,4,4):30,
      (5,5):24}
    assert cprof==Counter(expected)
    odist=Counter(order(p) for p in image);assert odist==Counter({1:1,2:25,3:20,4:30,5:24,6:20})
    st0=[p for p in image if p[0]==0];seen=set();sub=[]
    for x in range(10):
        if x in seen:continue
        o={p[x] for p in st0};seen|=o;sub.append(len(o))
    assert sorted(sub)==[1,3,6]

    hj=json.loads((ROOT/'data/PART_W33_PASS10869_10876_HJ10_P1F9_TEST.json').read_text())
    hp={int(k):int(v) for k,v in hj['residual_outer_C2_on_10']['profile'].items()}
    assert hp=={1:2,2:4}
    target_type=(1,1,2,2,2,2)
    matches=[p for p in image if cycle_type(p)==target_type];assert len(matches)==15
    fixed=next(p for p in matches if p==min(matches))
    assert sum(fixed[i]==i for i in range(10))==2
    c2_bijections=math.factorial(2)*math.factorial(4)*(2**4);assert c2_bijections==768
    assert max(odist)<8

    out={
      'schema':'w33.20260828.t10-s5-hj-intertwiner.v1','status':'PASS',
      'quadratic_carrier':{'isometry_group_order':51840,'translation_vector':4,
                           'translation_stabilizer_order':1920,'ten_fibre_image_order':120,
                           'kernel_order':16,'fibres':[list(x) for x in fibres]},
      'intrinsic_ten_state_geometry':{
        'graph':'T(5)=SRG(10,6,3,4)','complement':'Petersen=SRG(10,3,0,1)',
        'five_maximal_K4s':[list(x) for x in K4],
        'duad_labels':{str(i):list(duad[i]) for i in range(10)},
        'action_on_five_K4s':'full S5','point_stabilizer_subdegrees':[1,3,6],
        'image_order_distribution':dict(sorted(odist.items())),
        'ten_point_cycle_profiles':{' '.join(map(str,k)):v for k,v in sorted(cprof.items())}},
      'existing_S6_to_S5_fusion':{
        'source':'analysis/w33_s6_to_s5_branching_gauge.py',
        'literal_target':'k5_edges=C(5,2), n10=10',
        'identification':'native T(10) fibre i maps to the K5 edge given by duad_labels[i]'},
      'HJ10':{
        'certified_residual_C2_profile':'1^2 2^4',
        'matching_S5_class':'double transpositions','matching_elements':15,
        'equivariant_bijections_per_selected_double_transposition':c2_bijections,
        'equivariant_bijections_without_selected_target':15*c2_bijections,
        'canonical_bijection_from_current_data':False},
      'projective_extension_no_go':{
        'native_image_group':'S5','native_image_order':120,'native_has_order8':False,
        'P1F9_split_centralizer':'D16 contains C8','full_natural_extension':False,
        'reason':'an equivariant extension of the split C2 to its natural projective centralizer would require an order-eight action, absent from S5'},
      'theorem':'The ten native W33 T(10) fibres are canonically the ten duads of a five-set under a 2^4:S5 stabilizer of the singular translation vector. This is exactly the K5-edge carrier in the existing S6->S5 branching gauge. HJ10 residual C2 embeds as the S5 double-transposition class, giving 768 C2 intertwiners for a selected involution but no canonical choice and no extension to the natural P1(F9) D16/C8 projective centralizer.',
      'boundary':'This proves the W33 S5 carrier and classifies all residual-C2 identifications allowed by current HJ data. It does not construct an HJ S5 action or a projective-line structure on HJ10.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','stab':1920,'image':'S5','kernel':16,'HJ_C2_maps':768,'projective_extension':False}))
if __name__=='__main__':main()
