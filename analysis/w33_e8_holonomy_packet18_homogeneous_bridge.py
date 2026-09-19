#!/usr/bin/env python3
"""E8 holonomy-character / 18-probe homogeneous-space bridge.

There are three commuting physical grading labels in the current E8/A8 picture:
  rho in C3  : selects A8 inside E8,
  a   in C3  : the order-three Wilson line,
  b   in C2  : physical theta^3 parity.
Their character labels form the abelian group K=C3 x C3 x C2, |K|=18.

The Holonet packet has 72 group-native frame words
  G = F3^2 semidirect D8,
  word=(translation, S^sector R^probe).
Collapsing the four probe rotations is exactly the right-coset space
  X = G/<R>, |X|=72/4=18.
X is NOT an order-18 group quotient because <R> is not normal in G.

Exact obstruction:
* every 3-subgroup of G lies in the normal translation kernel T=F3^2, so T is
  the unique Sylow-3 subgroup;
* the D8 action on T is faithful, hence C_G(T)=T;
* therefore G contains no abelian subgroup C3^2 x C2 of order 18.
So the 18=18 cardinality cannot be promoted to a group identification.

Positive bridge:
T acts on X in exactly two regular orbits of size 9, indexed by the reflection
sector D8/<R> as a set.  Thus X is a two-sheet F3^2 torsor.  Forgetting the
group multiplication on K, its underlying T-set (translations on the first two
C3 labels, b fixed) is likewise two regular 9-point torsors.  A T-equivariant
bijection exists after choosing origins and which packet sheet is b=0.

The E8 adjoint joint eigenspace dimensions over the 18 characters are also
computed exactly.  Their Fourier transform gives integer traces
248,-8,14,-2,-4,4,5,1 on the 18 holonomy elements, a compact fingerprint for
future cross-checks.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_e8_holonomy_packet18_homogeneous_bridge.json'
I=(1,0,0,1);R=(0,2,1,0);S=(1,0,0,2)

def mm(A,B):
    return tuple(sum(A[2*i+k]*B[2*k+j] for k in range(2))%3
                 for i in range(2) for j in range(2))
def mv(A,v):
    return ((A[0]*v[0]+A[1]*v[1])%3,(A[2]*v[0]+A[3]*v[1])%3)
def mpow(A,n):
    o=I
    for _ in range(n):o=mm(o,A)
    return o

D8=[mm(mpow(S,s),mpow(R,p)) for s in range(2) for p in range(4)]
assert len(set(D8))==8
C4={mpow(R,p) for p in range(4)}
T=list(itertools.product(range(3),repeat=2))

def mul(g,h):
    t,L=g;u,M=h
    Lu=mv(L,u)
    return (((t[0]+Lu[0])%3,(t[1]+Lu[1])%3),mm(L,M))

G=[(t,L) for t in T for L in D8]
assert len(G)==72

def sector_of(L):
    return 0 if L in C4 else 1

def right_coset(rep):
    return frozenset(mul(rep,((0,0),C)) for C in C4)

def cyclo_pow(k):
    # a+b*w with w^2=-1-w
    return ((1,0),(0,1),(-1,-1))[k%3]
def cadd(x,y):return (x[0]+y[0],x[1]+y[1])

def main(write=True):
    # 18 right C4 cosets; coordinate is exactly (translation, reflection sector).
    cosets={}
    for g in G:
        C=right_coset(g)
        t,L=g
        key=(t,sector_of(L))
        cosets.setdefault(key,C)
        assert cosets[key]==C
    assert len(cosets)==18
    assert len(set(cosets.values()))==18
    assert all(len(C)==4 for C in cosets.values())

    # C4 is not normal: conjugating a pure rotation by a translation produces
    # a nonzero translation component.
    witness=mul(mul(((1,0),I),((0,0),R)),(((-1)%3,0),I))
    assert witness[0]!=(0,0)

    # D8 action on T is faithful; only I fixes every translation.
    kernel=[L for L in D8 if all(mv(L,t)==t for t in T)]
    assert kernel==[I]

    # Centralizer of T is exactly T: any (u,L) commuting with all (t,I) needs L t=t.
    centralizer_T=[g for g in G if all(mul(g,(t,I))==mul((t,I),g) for t in T)]
    assert len(centralizer_T)==9
    assert all(L==I for t,L in centralizer_T)

    # Translation action on X has two regular 9-orbits.
    keys=list(cosets)
    def Tact(u,key):
        t,s=key
        C=cosets[key]
        image=frozenset(mul((u,I),x) for x in C)
        return next(k for k,v in cosets.items() if v==image)
    orbits=[]
    seen=set()
    for k in keys:
        if k in seen:continue
        O={Tact(u,k) for u in T}
        seen|=O;orbits.append(O)
    assert sorted(map(len,orbits))==[9,9]
    assert sorted({next(iter({s for t,s in O})) for O in orbits})==[0,1]

    # Rebuild the 18 E8 eigenspace dimensions from the certified fundamental
    # joint multiplicities. rho=0 on A8, +1 on Lambda3, +2 on Lambda6.
    joint=[((0,0),3),((0,1),2),((1,0),1),((1,1),1),((2,0),1),((2,1),1)]
    chars=[]
    for ch,n in joint:chars += [ch]*n
    cnt=Counter()
    # A8 roots
    for i in range(9):
      for j in range(9):
        if i!=j:
          cnt[(0,(chars[i][0]-chars[j][0])%3,(chars[i][1]-chars[j][1])%2)]+=1
    # Lambda3 + Lambda6
    for sub in itertools.combinations(range(9),3):
        a=sum(chars[i][0] for i in sub)%3
        b=sum(chars[i][1] for i in sub)%2
        cnt[(1,a,b)]+=1
        cnt[(2,(-a)%3,(-b)%2)]+=1
    cnt[(0,0,0)]+=8
    assert sum(cnt.values())==248

    expected={
      (0,0,0):16,(0,0,1):16,(0,1,0):12,(0,1,1):12,(0,2,0):12,(0,2,1):12,
      (1,0,0):14,(1,0,1):16,(1,1,0):13,(1,1,1):14,(1,2,0):13,(1,2,1):14,
      (2,0,0):14,(2,0,1):16,(2,1,0):13,(2,1,1):14,(2,2,0):13,(2,2,1):14}
    assert dict(cnt)==expected

    # DFT character traces. Represent cube-root phases exactly as a+b omega and
    # verify the omega coefficient cancels in every trace.
    traces={}
    for u in range(3):
      for v in range(3):
       for w in range(2):
        z=(0,0)
        for (rho,a,b),m in cnt.items():
            ph=cyclo_pow(u*rho+v*a)
            if w*b: ph=(-ph[0],-ph[1])
            z=cadd(z,(m*ph[0],m*ph[1]))
        assert z[1]==0
        traces[(u,v,w)]=z[0]
    assert set(traces.values())=={248,-8,14,-2,-4,4,5,1}

    e8parent=json.loads((ROOT/'data/w33_e8_a8_selector_holonomy_triple_intersection.json').read_text())
    assert e8parent['status']=='PASS_A8_SELECTOR_TRIPLE_CENTRALIZER'
    frame=json.loads((ROOT/'data/w33_qutrit_hamming_cz_frame_bundle.json').read_text())
    assert frame['status']=='PASS_Q3_LOCAL_FRAME_PHASE_LOCK'

    out={
      'schema':'w33.e8_holonomy_packet18_homogeneous_bridge.v1',
      'status':'PASS_TORSOR_BRIDGE__GROUP_IDENTIFICATION_KILLED',
      'headline':'The 18 E8 holonomy characters form the abelian group C3^2 x C2, but the 18 runtime probe blocks are the homogeneous space (F3^2 semidirect D8)/C4, not an order-18 group. G contains no abelian subgroup of order18. The surviving exact bridge is T=F3^2-equivariant: both objects are two regular nine-point T-torsors after forgetting the holonomy group multiplication.',
      'negative_result':{
        'holonomy_character_group':'C3 x C3 x C2',
        'packet_group':'F3^2 semidirect D8',
        'unique_sylow3':'T=F3^2 because every 3-subgroup maps trivially to D8',
        'centralizer_of_T_order':9,
        'centralizer_of_T':'T',
        'abelian_order18_subgroup_exists':False,
        'consequence':'no group-equivariant 18=18 identification inside the 72-element packet group'},
      'positive_bridge':{
        'packet_18':'right cosets G/<R>, <R>=C4','coset_count':18,'coset_size':4,
        'C4_normal':False,
        'translation_orbits':[9,9],
        'interpretation':'two regular F3^2 torsors, matching the underlying translation-set type of C3^2 x C2 after b is treated as a sheet label',
        'coordinate_bijection_candidate':'(rho,a,b) -> (hesse_bin=3*rho+a, hashimoto_sector=b), defined only after origin/sheet conventions'},
      'E8_joint_sector_dimensions':{
        f'{r},{a},{b}':cnt[(r,a,b)] for r in range(3) for a in range(3) for b in range(2)},
      'E8_holonomy_trace_fingerprint':{
        f'{u},{v},{w}':traces[(u,v,w)] for u in range(3) for v in range(3) for w in range(2)},
      'trace_values':sorted(set(traces.values())),
      'boundary':'Exact group/G-set and E8 character arithmetic. The T-equivariant bijection is a control/address bridge, not a physical identification of E8 root spaces with optical frequency bins; the full abelian holonomy group law is explicitly not present on packet18.',
      'checks':{
        '18_right_cosets':True,'C4_not_normal':True,'D8_faithful_on_T':True,
        'centralizer_T_is_T':True,'no_abelian_C3sq_x_C2_subgroup':True,
        'two_regular_translation_orbits':True,'E8_sector_sum248':True,
        'all_holonomy_traces_integral':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__':main(True)
