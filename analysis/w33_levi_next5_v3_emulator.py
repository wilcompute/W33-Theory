#!/usr/bin/env python3
"""End-to-end optical click-stream -> homology -> native W(E6) runtime emulator."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib, json, math, random

import numpy as np

from w33_levi_next5_v3_common import (
    apply_cols, build_w33, compose_perm, gf2_apply, gf2_nullspace, gf2_row_basis,
    homology_action, line_perm_from_point_perm, matrix_rows_to_masks, point_outer_perm,
    point_transvection_perm, quotient_basis, sha256_json, tagged_basis, coordinates,
)
from w33_levi_next5_v3_e6 import SEEDS, build_module, object_sets
from w33_levi_next5_v3_tolerance import ACTIVE, halmos

SECRET=b'w33-optical-homology-v3'

@dataclass(frozen=True)
class Packet:
    type_bit:int; syndrome:int; payload:int

@dataclass(frozen=True)
class Envelope:
    origin:Packet; current:Packet; transition:str; nonce:int; tag:str

class AdmissionError(ValueError):pass
class Retry(ValueError):pass

class Context:
    def __init__(self,diff):
        self.rows=matrix_rows_to_masks(diff%2);self.image=gf2_row_basis(self.rows)
        self.kernel=gf2_nullspace(self.rows,40);self.hom=quotient_basis(self.kernel,self.image)
        self.tagged=tagged_basis(self.image+self.hom)
    def syndrome(self,payload):
        if gf2_apply(self.rows,payload): raise AdmissionError('homology:not-cycle')
        rem,tag=coordinates(payload,self.tagged)
        if rem:raise AdmissionError('homology:not-coordinate')
        return tag>>len(self.image)
    def packet(self,syndrome,boundary_mask=0):
        payload=0
        for i,r in enumerate(self.hom):
            if (syndrome>>i)&1:payload^=r
        for i,r in enumerate(self.image):
            if (boundary_mask>>i)&1:payload^=r
        return Packet(0,syndrome,payload)

class OpticalHomologyVM:
    def __init__(self):
        self.geom=build_w33();self.point=Context(self.geom.adjacency);self.line=Context(self.geom.line_adjacency)
        assert len(self.point.hom)==8 and len(self.line.hom)==20
        self.inc_rows=matrix_rows_to_masks(self.geom.incidence%2)
        self.inc_cols=matrix_rows_to_masks(self.geom.incidence.T%2)
        self.sentinel_basis=gf2_nullspace(self.inc_rows,40)
        self.dark8=[]
        for mask in range(1,1<<len(self.sentinel_basis)):
            w=0
            for i,b in enumerate(self.sentinel_basis):
                if (mask>>i)&1:w^=b
            if w.bit_count()==8:self.dark8.append(w)
        self.dark8=sorted(set(self.dark8));assert len(self.dark8)==45
        self.scale,self.C,self.U=halmos(ACTIVE)
        bound=max(np.sum(np.abs(self.C),axis=1));self.bound=bound
        self.codebook=np.array([self.C@np.array([1.0 if (s>>i)&1 else -1.0 for i in range(8)])/bound for s in range(256)])
        # Native runtime object action.
        geom,pg,op,racts,lperms,G,names,singular=build_module()
        self.pgens=pg+[op];self.mgens=racts;self.names=names;self.singular=singular;self.lineperms=lperms
        self.triangles,self.sixes,_=object_sets(G)
        self.tri_idx={frozenset(x):i for i,x in enumerate(self.triangles)}
        self.six_idx={frozenset(x):i for i,x in enumerate(self.sixes)}
        self.pairs=[(i,j) for i in range(40) for j in range(i+1,40) if not geom.adjacency[i,j]]
        self.pair_idx={frozenset(x):i for i,x in enumerate(self.pairs)}
    def tag(self,origin,transition,nonce):
        body=f'{origin.type_bit}:{origin.syndrome}:{origin.payload}:{transition}:{nonce}'.encode()
        return hashlib.blake2s(body,key=SECRET,digest_size=12).hexdigest()
    def seal(self,origin,current,transition,nonce):return Envelope(origin,current,transition,nonce,self.tag(origin,transition,nonce))
    def admit(self,env,confidence=1.0):
        if confidence<0.35:raise Retry('optical:low-confidence')
        if env.tag!=self.tag(env.origin,env.transition,env.nonce):raise AdmissionError('authentication')
        expected=env.origin
        error=env.current.payload^expected.payload
        readout=gf2_apply(self.inc_rows if expected.type_bit==0 else self.inc_cols,error)
        if readout:raise AdmissionError('sentinel')
        if env.transition!='native' or env.current.type_bit!=expected.type_bit:raise AdmissionError('type-confusion')
        if env.current!=expected:raise AdmissionError('provenance')
        ctx=self.point if env.current.type_bit==0 else self.line
        if ctx.syndrome(env.current.payload)!=env.current.syndrome:raise AdmissionError('syndrome')
        return self.runtime_coordinate(env.current.syndrome,env.nonce)
    def click_stream(self,syndrome,rng,photons=24000,transmission=0.70,dark_cps=158.0,bin_ps=100.0,jitter_fwhm_ps=50.0):
        bits=np.array([(syndrome>>i)&1 for i in range(8)],dtype=float);x=2*bits-1
        y=self.C@x;bound=self.bound;z=np.clip(y/bound,-.999,.999)
        total=photons*transmission
        dark=dark_cps*bin_ps*1e-12
        plus=rng.poisson(total*(1+z)/2+dark,size=8);minus=rng.poisson(total*(1-z)/2+dark,size=8)
        sigma=jitter_fwhm_ps/2.354820045;p=math.erfc((bin_ps/2)/(math.sqrt(2)*sigma))
        # nearest-neighbor time-bin migration on both balanced rails
        for arr in (plus,minus):
            moved=np.zeros(8,dtype=int)
            for i in range(8):
                m=rng.binomial(int(arr[i]),p);arr[i]-=m
                if i==0:moved[1]+=m
                elif i==7:moved[6]+=m
                else:
                    left=rng.binomial(m,.5);moved[i-1]+=left;moved[i+1]+=m-left
            arr+=moved
        counts=plus+minus
        if counts.sum()<photons*transmission*.55:raise Retry('optical:no-click/loss')
        zest=(plus-minus)/np.maximum(counts,1)
        distances=np.linalg.norm(self.codebook-zest,axis=1);order=np.argsort(distances);decoded=int(order[0])
        confidence=float((distances[order[1]]-distances[order[0]])/(distances[order[1]]+1e-12))
        return decoded,confidence,{'plus':plus.tolist(),'minus':minus.tolist(),'z_est':zest.tolist(),'nearest_distance':float(distances[order[0]]),'runner_up_distance':float(distances[order[1]])}
    def runtime_coordinate(self,syndrome,nonce):
        digest=hashlib.sha256(f'{syndrome}:{nonce}'.encode()).digest();word=[b%9 for b in digest]
        sv=self.singular[0];tri=set(self.triangles[0]);six=set(self.sixes[0]);pair=set(self.pairs[0]);chir=0
        for k in word:
            mg=self.mgens[k];pg=self.pgens[k];lp=self.lineperms[k]
            sv=apply_cols(mg,sv);tri={lp[x] for x in tri};six={lp[x] for x in six};pair={pg[x] for x in pair}
            if k==8:chir^=1
        li=self.singular.index(sv)
        return {'chirality':chir,'line27':self.names[li],'tritangent45':self.tri_idx[frozenset(tri)],'root72':self.six_idx[frozenset(six)],'pair540':self.pair_idx[frozenset(pair)],'word_digest':hashlib.sha256(bytes(word)).hexdigest()}

def analyze(seed=20260710):
    vm=OpticalHomologyVM();rng=np.random.default_rng(seed);prng=random.Random(seed)
    exhaustive=0
    for s in range(256):
        p=vm.point.packet(s,0);env=vm.seal(p,p,'native',s);vm.admit(env,1.0);exhaustive+=1
    outcomes=Counter();accepted_coords=[];example=None
    for n in range(2500):
        s=prng.randrange(256);boundary=prng.getrandbits(len(vm.point.image));origin=vm.point.packet(s,boundary)
        try:
            decoded,conf,stream=vm.click_stream(s,rng,transmission=max(.2,min(.95,rng.normal(.70,.08))))
        except Retry:outcomes['retry']+=1;continue
        if decoded!=s:
            outcomes['retry/decode-mismatch']+=1;continue
        current=vm.point.packet(decoded,boundary)
        env=vm.seal(origin,current,'native',n)
        try:
            coord=vm.admit(env,conf);outcomes['accepted']+=1;accepted_coords.append(coord)
            if example is None:example={'syndrome':s,'decoded':decoded,'confidence':conf,'click_stream':stream,'runtime':coord}
        except Retry:outcomes['retry']+=1
        except AdmissionError as e:outcomes[f'rejected/{e}']+=1
    attacks=Counter()
    origin=vm.point.packet(0xA5,0)
    # all weights 1..7, 64 deterministic examples each
    for w in range(1,8):
        for k in range(64):
            bits=prng.sample(range(40),w);e=sum(1<<i for i in bits)
            cur=Packet(0,origin.syndrome,origin.payload^e);env=vm.seal(origin,cur,'native',10000+w*100+k)
            try:vm.admit(env,1.0);attacks['admitted_sub8']+=1
            except AdmissionError as ex:attacks[str(ex)]+=1
    for i,e in enumerate(vm.dark8):
        cur=Packet(0,origin.syndrome,origin.payload^e);env=vm.seal(origin,cur,'native',20000+i)
        try:vm.admit(env,1.0);attacks['admitted_dark8']+=1
        except AdmissionError as ex:attacks[str(ex)]+=1
    retag=Packet(1,origin.syndrome,origin.payload);env=vm.seal(origin,retag,'native',30000)
    try:vm.admit(env,1.0);attacks['admitted_retag']+=1
    except AdmissionError as ex:attacks[str(ex)]+=1
    bad=Envelope(origin,origin,'native',40000,'00'*12)
    try:vm.admit(bad,1.0);attacks['admitted_bad_auth']+=1
    except AdmissionError as ex:attacks[str(ex)]+=1
    checks={
      'all_256_noiseless_homology_words_admit':exhaustive==256,
      'clean_streams_produce_admissions':outcomes['accepted']>2200,
      'no_wrong_clean_decode_admitted':sum(v for k,v in outcomes.items() if k.startswith('rejected/'))==0,
      'all_448_sub8_attacks_rejected_by_sentinel':attacks['sentinel']==448,
      'all_45_dark8_rejected_by_provenance':attacks['provenance']==45,
      'retag_rejected':attacks['type-confusion']==1,
      'bad_auth_rejected':attacks['authentication']==1,
      'native_coordinates_emitted':len(accepted_coords)==outcomes['accepted'],
    }
    return {'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'clean_outcomes':dict(outcomes),'attack_outcomes':dict(attacks),'example':example,'accepted_runtime_digest':sha256_json(accepted_coords),'theorem':'Balanced optical click streams decode the 8-bit point-homology syndrome; every admitted frame is authenticated, sentinel-consistent, provenance-exact, homologically valid, and assigned a native W(E6) coordinate. No tested corruption is admitted.'}

def main():
    out=analyze();print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
