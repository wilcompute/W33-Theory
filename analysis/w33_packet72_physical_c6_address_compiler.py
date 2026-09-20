#!/usr/bin/env python3
"""Compile the physical flagship C6 holonomy into the 72-slot packet ABI.

Parents:
  data/w33_packet18_external_regular_holonomy_action.json
  analysis/w33_architecture_control_plane_abi.py

The packet ABI exposes
  hesse_bin h = 3*rho + a,   rho,a in F3,
  hashimoto_sector b in F2,
  probe_slot p in Z4,
with frame tick
  tick = 8*h + 4*b + p.

The exact external packet18 holonomy theorem proves that the physical C6
generator is
  (rho,a,b) -> (rho,a+1,b+1),
i.e. one ternary a-translation followed by the unique G-equivariant deck swap.

Therefore on the full 72-slot frame (retaining p) the scheduler permutation is
  h' = 3*(h//3) + ((h%3)+1 mod3),
  b' = 1-b,
  p' = p.

It has:
  * order 6,
  * cycle profile 6^12 on the 72 frame slots,
  * square = pure order-three translation by +2 in a,
  * cube = pure binary sheet/deck parity,
  * fourth power = pure order-three translation by +1 in a,
  * sixth power = identity.

This is a LOOKUP-FREE CONTROL-PLANE compiler.  It does not claim that changing
these address fields by itself performs the microscopic E8 holonomy on a
physical quantum state.  It compiles the exact finite holonomy labels into the
runtime scheduler coordinates already exposed by the ABI.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_packet72_physical_c6_address_compiler.json'

def decode_tick(tick:int):
    assert 0<=tick<72
    h=tick//8
    r=tick%8
    b=r//4
    p=r%4
    rho=h//3
    a=h%3
    return rho,a,b,p

def encode_tick(rho:int,a:int,b:int,p:int):
    h=3*(rho%3)+(a%3)
    return 8*h+4*(b%2)+(p%4)

def step(tick:int):
    rho,a,b,p=decode_tick(tick)
    return encode_tick(rho,(a+1)%3,1-b,p)

def power(tick:int,n:int):
    x=tick
    for _ in range(n):x=step(x)
    return x

def profile(perm):
    seen=set();c=Counter()
    for i in range(len(perm)):
        if i in seen:continue
        u=i;n=0
        while u not in seen:
            seen.add(u);n+=1;u=perm[u]
        c[n]+=1
    return dict(sorted(c.items()))

def main(write=True):
    parent=json.loads((ROOT/'data/w33_packet18_external_regular_holonomy_action.json').read_text())
    assert parent['status']=='PASS_EXTERNAL_REGULAR_HOLONOMY_ACTION'

    perm=[step(i) for i in range(72)]
    assert sorted(perm)==list(range(72))
    assert profile(perm)=={6:12}

    # Probe and selector rho remain invariant under the compiled physical C6.
    for i in range(72):
        rho,a,b,p=decode_tick(i)
        rho1,a1,b1,p1=decode_tick(step(i))
        assert rho1==rho and p1==p
        assert a1==(a+1)%3 and b1==1-b

    # Exact power laws.
    for i in range(72):
        rho,a,b,p=decode_tick(i)
        r2=decode_tick(power(i,2))
        r3=decode_tick(power(i,3))
        r4=decode_tick(power(i,4))
        r6=decode_tick(power(i,6))
        assert r2==(rho,(a+2)%3,b,p)
        assert r3==(rho,a,1-b,p)
        assert r4==(rho,(a+1)%3,b,p)
        assert r6==(rho,a,b,p)

    # At packet18 resolution (drop p), there are three 6-cycles.
    packet18=[(rho,a,b) for rho in range(3) for a in range(3) for b in range(2)]
    idx={x:i for i,x in enumerate(packet18)}
    p18=[]
    for rho,a,b in packet18:
        p18.append(idx[(rho,(a+1)%3,1-b)])
    assert profile(p18)=={6:3}

    # One explicit orbit for each selector rho and probe p.
    orbits=[]
    for rho in range(3):
      for p in range(4):
        start=encode_tick(rho,0,0,p)
        orb=[decode_tick(power(start,n)) for n in range(6)]
        assert len(set(orb))==6
        orbits.append({'rho':rho,'probe_slot':p,
                       'states':[{'rho':r,'a':a,'b':b,'p':pp,
                                  'tick':encode_tick(r,a,b,pp)}
                                 for r,a,b,pp in orb]})

    out={
      'schema':'w33.packet72_physical_c6_address_compiler.v1',
      'status':'PASS_LOOKUP_FREE_CONTROL_PLANE_COMPILER',
      'headline':'The physical flagship C6 holonomy compiles exactly into the existing 72-slot packet address word as a->a+1 mod3, sector b->1-b, with selector rho and probe slot p fixed. The resulting scheduler permutation has order 6 and cycle profile 6^12. Its cube is the pure deck/sector parity; its square and fourth power are the two nontrivial order-three translations.',
      'address_word':{
        'hesse_bin':'h=3*rho+a',
        'sector':'b in F2',
        'probe':'p in Z4',
        'frame_tick':'8*h+4*b+p'},
      'compiled_generator':{
        'rho':'unchanged',
        'a':'a+1 mod3',
        'b':'1-b',
        'p':'unchanged',
        'tick_formula':"8*(3*(h//3)+((h%3+1)%3))+4*(1-b)+p"},
      'cycle_profiles':{
        'packet18':{'6_cycles':3},
        'packet72':{'6_cycles':12}},
      'power_laws':{
        'g2':'a->a+2, b fixed',
        'g3':'a fixed, b->1-b (pure deck parity)',
        'g4':'a->a+1, b fixed',
        'g6':'identity'},
      'orbits':orbits,
      'hardware_read':'no lookup table is required; one ternary increment plus one binary XOR updates the control-plane address, while the four-slot probe rotation is untouched',
      'physical_boundary':'This is a scheduler/address compiler for certified holonomy labels, not a claim that address mutation alone realizes the microscopic E8 unitary on a photonic or material state.',
      'parents':['data/w33_packet18_external_regular_holonomy_action.json',
                 'analysis/w33_architecture_control_plane_abi.py'],
      'checks':{
        '72_slot_permutation':True,
        'profile_6pow12':True,
        'rho_invariant':True,
        'probe_invariant':True,
        'square_is_order3_translation':True,
        'cube_is_deck_parity':True,
        'sixth_power_identity':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':main(True)
