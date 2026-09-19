#!/usr/bin/env python3
"""Qutrit Hamming/CZ frame theorem behind the 11-bin punctured-Hesse ABI.

Parent:
  data/w33_punctured_hesse_packet_group.json
  data/w33_cz_hashimoto_orbit_weld.json
  data/w33_cz_zero_phase_su5_hypercharge.json

For a prime q, the setwise stabilizer in PGL(3,q) of the two deleted infinity
points Ex=[1:0:0], Ey=[0:1:0] acts on the affine chart as
    (x,y) -> (a x+b, c y+d)
or the coordinate-swapped version, with a,c != 0.
Hence
    G_q ~= AGL(1,q) wr C2
and |G_q|=2 q^2 (q-1)^2.

At q=3, AGL(1,3)=S3, so
    G_3 = S3 wr C2 = Aut H(2,3),
the FULL automorphism group of the 3x3 rook/Hamming graph on the nine
two-qutrit computational-basis bins.  This full-local-frame coincidence is
special among odd primes because
    |AGL(1,q)|=q(q-1)=q!
iff (q-2)!=1, so q=3 for odd prime q.

CZ FRAME.
Let f_0(x,y)=xy.  Its zero-phase support is the five-point cross
    Z_0={xy=0}.
The stabilizer of Z_0 inside G_3 is exactly the linear monomial D8, order 8.
The full orbit of Z_0 consists of the nine translated crosses
    Z_(a,b)={(x,y):(x-a)(y-b)=0},
one centered on each affine Hesse bin.  Thus
    G_3 / D8 ~= F3^2
is exactly the nine-center bundle already used by the packet compiler.

PHASE / INFINITY LOCK.
For L=diag(alpha,beta), possibly followed by coordinate swap,
    f_0(L(x,y)) = chi(L) f_0(x,y),   chi=alpha*beta.
So chi=+1 preserves CZ_3 and chi=-1 swaps CZ_3 <-> CZ_3^{-1}.

The two surviving infinity points are
    I_+=[1:1:0], I_-=[1:-1:0].
Under the same linear monomial L, their slope transforms by beta/alpha
(up to inversion under coordinate swap).  At q=3, alpha^{-1}=alpha and
beta^{-1}=beta for every nonzero scalar, hence
    beta/alpha = alpha*beta = chi(L).
Therefore the infinity pair swaps EXACTLY when CZ_3 is inverted.

This identifies the existing 11-bin punctured-Hesse alphabet equivariantly as
    9 affine CZ-frame centers  +  2 nonzero CZ phase sectors.

For q>3 the ratio character beta/alpha and product character alpha*beta are
generically distinct, so this exact sideband/phase lock is q=3-specific.

Boundary:
* the finite group, Hamming graph, translated-cross orbit and phase/infinity
  character equality are exact;
* assigning the two sideband labels to omega versus omega^{-1} has one global
  swap convention;
* this is control/frame semantics, not a claim that optical hardware enacts
  every element of Aut H(2,3) dynamically.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_qutrit_hamming_cz_frame_bundle.json'

def perms(q):
    return list(itertools.permutations(range(q)))

def is_affine_perm(p,q):
    for a in range(1,q):
        for b in range(q):
            if tuple((a*x+b)%q for x in range(q))==p:
                return True
    return False

def cross(center,q):
    a,b=center
    return frozenset((x,y) for x in range(q) for y in range(q)
                     if ((x-a)*(y-b))%q==0)

def hamming_adj(u,v):
    return sum(a!=b for a,b in zip(u,v))==1

def q3_group():
    q=3
    affine=[p for p in perms(q) if is_affine_perm(p,q)]
    assert len(affine)==6
    G=[]
    for px in affine:
        for py in affine:
            for sw in (0,1):
                G.append((px,py,sw))
    assert len(G)==72
    return G

def act(g,p):
    px,py,sw=g
    x,y=p
    return (px[y],py[x]) if sw else (px[x],py[y])

def cz_phase(p): return (p[0]*p[1])%3

def main(write=True):
    q=3
    G=q3_group()
    pts=list(itertools.product(range(q),repeat=2))

    # Full H(2,3) automorphism check.
    assert all(
        hamming_adj(u,v)==hamming_adj(act(g,u),act(g,v))
        for g in G for u in pts for v in pts
    )
    # Every permutation of coordinates/labels is already affine only at q=3.
    assert all(is_affine_perm(p,3) for p in perms(3))
    q_controls={}
    for qq in (3,5,7):
        lhs=qq*(qq-1)
        # equality with |S_q| tests AGL(1,q)=S_q by order
        import math
        q_controls[str(qq)]={'AGL1_order':lhs,'S_q_order':math.factorial(qq),
                             'equal':lhs==math.factorial(qq)}
    assert q_controls['3']['equal']
    assert not q_controls['5']['equal'] and not q_controls['7']['equal']

    Z0=cross((0,0),3)
    assert len(Z0)==5
    stabilizer=[g for g in G if frozenset(act(g,p) for p in Z0)==Z0]
    assert len(stabilizer)==8

    crosses={cross(c,3) for c in pts}
    orbit={frozenset(act(g,p) for p in Z0) for g in G}
    assert orbit==crosses and len(orbit)==9

    # Exact phase/infinity character on the linear D8 = cross stabilizer.
    # Extract affine maps fixing the origin; they are precisely the 8 stabilizer elements.
    linear=[g for g in stabilizer if act(g,(0,0))==(0,0)]
    assert len(linear)==8
    inf=[(1,1),(1,2)]  # [1:s:0], s=+/-1

    rows=[]
    exact_preserve=0
    invert=0
    for g in linear:
        vals=[]
        for p in pts:
            if cz_phase(p):
                qv=cz_phase(act(g,p))*pow(cz_phase(p),-1,3)%3
                vals.append(qv)
        assert len(set(vals))==1
        chi=vals[0]
        assert chi in (1,2)
        if chi==1: exact_preserve+=1
        else: invert+=1

        # Derive the induced linear matrix from images of basis vectors.
        e1=act(g,(1,0)); e2=act(g,(0,1))
        # Projective action on the two surviving infinity directions.
        imgs=[]
        for p in inf:
            x=(e1[0]*p[0]+e2[0]*p[1])%3
            y=(e1[1]*p[0]+e2[1]*p[1])%3
            inv=pow(x,-1,3)
            imgs.append((1,y*inv%3))
        swapped=(imgs==[inf[1],inf[0]])
        assert swapped==(chi==2)
        rows.append({'chi':chi,'infinity_swapped':swapped,
                     'e1':list(e1),'e2':list(e2)})
    assert (exact_preserve,invert)==(4,4)

    parent=json.loads((ROOT/'data/w33_punctured_hesse_packet_group.json').read_text())
    assert parent['status']=='PASS_TWO_PUNCTURE_PACKET_GROUP'
    assert parent['q3_group']['order']==72
    assert parent['q3_group']['orbit_sizes']==[2,9]

    cz=json.loads((ROOT/'data/w33_cz_zero_phase_su5_hypercharge.json').read_text())
    assert cz['status']=='PASS'
    assert cz['CZ3']['multiplicities']==[5,2,2]

    out={
      'schema':'w33.qutrit_hamming_cz_frame_bundle.v1',
      'status':'PASS_Q3_LOCAL_FRAME_PHASE_LOCK',
      'headline':'The 72-slot punctured-Hesse packet group is Aut H(2,3)=S3 wr C2, the full local classical relabeling group of the 3x3 two-qutrit computational grid. Its D8 stabilizer fixes one five-state CZ zero-phase cross; the 9 cosets are exactly the 9 translated CZ crosses centered on the affine Hesse bins. The two punctured-plane infinity points transform by exactly the CZ inversion character, so the existing 11=9+2 runtime alphabet is equivariantly 9 CZ-frame centers plus the two nonzero CZ phase sectors.',
      'group':{
        'packet_group':'F3^2 semidirect D8',
        'isomorphism':'AGL(1,3) wr C2 = S3 wr C2 = Aut H(2,3)',
        'order':72,
        'vertices':9,
        'meaning':'full local classical basis-label symmetry of two qutrits'},
      'CZ_frame':{
        'phase':'f(x,y)=xy mod 3',
        'zero_support':'five-state cross xy=0',
        'cross_stabilizer':'D8',
        'stabilizer_order':8,
        'translated_crosses':9,
        'coset_space':'G/D8 ~= F3^2',
        'exact_phase_preservers':4,
        'phase_inverters':4},
      'punctured_plane':{
        'affine_orbit':9,
        'infinity_orbit':2,
        'infinity_labels':['[1:1:0]','[1:2:0]'],
        'equivariance':'the infinity pair swaps iff CZ_3 is sent to CZ_3^{-1}',
        'global_convention':'which infinity point is called omega versus omega^{-1} may be swapped once'},
      'q3_speciality':{
        'reason_1':'AGL(1,3)=S3, so the affine packet group is the full Hamming local-frame group',
        'reason_2':'every nonzero scalar is self-inverse, so beta/alpha=alpha*beta and the infinity slope character equals the CZ phase-scaling character',
        'controls':q_controls},
      'physics_bridge':{
        'SU5':'each CZ zero-phase cross is 5-dimensional and carries the SU(5) block of the separate flagship theorem',
        'runtime':'9 Hesse bins select translated CZ frames; the two sidebands carry the nonzero phase-sector doublet'},
      'boundary':'Exact finite control/frame semantics. No claim that current optical hardware dynamically implements the whole 72-element group.',
      'checks':{
        'group_order72':True,'full_H23_automorphism_action':True,
        'cross_stabilizer_D8':True,'nine_cross_orbit':True,
        'four_preserve_four_invert':True,'infinity_swap_equals_phase_inversion':True,
        'q3_full_affine_equals_symmetric':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':main(True)
