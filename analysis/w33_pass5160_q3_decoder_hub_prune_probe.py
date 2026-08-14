#!/usr/bin/env python3
"""Pass5160: symmetry-preserving hub-prune repair of the minimal q=3 decoder obstruction.

Pass5136's first failure is a false apartment that ties the true errors because
three charts through it each carry a locally equivalent two-error pattern.  The
false center is a hub inside the tied max-vote set.  Keep the exact local ROM
and global vote symmetry, but among max-vote candidates retain only those of
minimum induced degree in the chart-sharing graph.

We exhaust the complete previously certified connected radius-five domain and
the complete centered 2+2+2 weight-six obstruction family through a fixed false
center.  Apartment transitivity makes those centered motifs complete up to the
choice of center.  This proves preservation of radius five and repair of that
entire minimal obstruction family, but not a global radius-six theorem.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5160_Q3_DECODER_HUB_PRUNE_PROBE.json'
PAIRS=list(itertools.combinations(range(4),2));POS={e:i for i,e in enumerate(PAIRS)}
SYN=list(itertools.combinations(range(1,4),2))

def syndrome(m):
    s=0
    for b,(i,j) in enumerate(SYN):s|=((((m>>POS[(0,i)])&1)^((m>>POS[(0,j)])&1)^((m>>POS[(i,j)])&1))<<b)
    return s

def leaders():
    B={s:[] for s in range(8)}
    for m in range(64):B[syndrome(m)].append(m)
    out=[]
    for s in range(8):
        w=min(x.bit_count() for x in B[s]);z=[x for x in B[s] if x.bit_count()==w]
        out.append(z[0] if len(z)==1 else 0)
    return out

def connected_sets(adj,k):
    L={frozenset((0,))}
    for _ in range(1,k):
        N=set()
        for S in L:
            B=set()
            for v in S:B|=adj[v]
            for u in B-S:N.add(frozenset(set(S)|{u}))
        L=N
    return L

def main():
    G=build_W(3);n=len(G['apartments']);lead=leaders();coords=[[loc[p] for p in PAIRS] for _,loc in G['charts']]
    ach=[[] for _ in range(n)];adj=[set() for _ in range(n)]
    for ci,C in enumerate(coords):
        for pos,a in enumerate(C):ach[a].append((ci,pos))
        for a,b in itertools.combinations(C,2):adj[a].add(b);adj[b].add(a)
    def votes(E):
        masks={}
        for a in E:
            for ci,pos in ach[a]:masks[ci]=masks.get(ci,0)^(1<<pos)
        V={}
        for ci,m in masks.items():
            lm=lead[syndrome(m)]
            if lm:
                p=lm.bit_length()-1;a=coords[ci][p];V[a]=V.get(a,0)+1
        return V
    def sweep(E):
        V=votes(E)
        if not V:return frozenset(),0,{},frozenset()
        z=max(V.values());M=frozenset(a for a,v in V.items() if v==z)
        deg={a:len(adj[a]&M) for a in M};md=min(deg.values())
        corr=frozenset(a for a in M if deg[a]==md)
        return corr,z,deg,M

    radius5={'tested':{},'failures':[],'max_sweeps':0}
    for k in range(1,6):
        SS=connected_sets(adj,k);radius5['tested'][str(k)]=len(SS)
        for E0 in SS:
            E=E0;steps=0
            while E and steps<12:
                corr,z,deg,M=sweep(E)
                if not corr or not corr<=E:
                    radius5['failures'].append({'k':k,'E':sorted(E0),'residual':sorted(E),'corr':sorted(corr),'max_vote':z,'tie':sorted(M),'tie_deg':deg});break
                E=E^corr;steps+=1
            if E and not radius5['failures']:radius5['failures'].append({'k':k,'E':sorted(E0),'reason':'did_not_clear','residual':sorted(E)})
            radius5['max_sweeps']=max(radius5['max_sweeps'],steps)
            if radius5['failures']:break
        if radius5['failures']:break
    assert radius5['tested']=={'1':1,'2':20,'3':490,'4':13269,'5':381480}
    assert not radius5['failures'] and radius5['max_sweeps']==3

    center=0;incident=[ci for ci,_ in ach[center]];pair_options={}
    for ci in incident:
        C=coords[ci];opts=[]
        for a,b in itertools.combinations([x for x in C if x!=center],2):
            m=(1<<C.index(a))|(1<<C.index(b));lm=lead[syndrome(m)]
            if lm and C[lm.bit_length()-1]==center:opts.append((a,b))
        pair_options[ci]=opts
    motif_count=motif_repaired=motif_cleared=0;motif_failures=[];examples=[]
    for cis in itertools.combinations(incident,3):
        for triples in itertools.product(*(pair_options[ci] for ci in cis)):
            flat=[x for ab in triples for x in ab]
            if len(set(flat))<6 or center in flat:continue
            E0=frozenset(flat);motif_count+=1;corr,z,deg,M=sweep(E0)
            ok=(center not in corr and bool(corr) and corr<=E0)
            if ok:motif_repaired+=1
            if len(examples)<5:examples.append({'errors':sorted(E0),'corr':sorted(corr),'max_vote':z,'tie':sorted(M),'tie_deg':deg})
            E=E0;good=True;steps=0
            while E and steps<12:
                c,_,_,_=sweep(E)
                if not c or not c<=E:good=False;break
                E=E^c;steps+=1
            if good and not E:motif_cleared+=1
            elif len(motif_failures)<10:motif_failures.append({'errors':sorted(E0),'residual':sorted(E),'steps':steps})
    assert len(incident)==4 and all(len(v)==2 for v in pair_options.values())
    assert motif_count==motif_repaired==motif_cleared==32 and not motif_failures
    witness=next(x for x in examples if x['errors']==[1,2,3,6,27,54])
    assert witness['corr']==[1,2,3,6,27,54] and witness['tie_deg'][0]==6
    assert all(witness['tie_deg'][x]==2 for x in witness['errors'])

    out={'pass':5160,'status':'THEOREM_Q3_HUB_PRUNE_PRESERVES_RADIUS5_AND_REPAIRS_CENTERED_WEIGHT6_FAMILY','q':3,
      'rule':'Keep the original local ROM and global max-vote set; among tied max-vote candidates correct only those with minimum induced degree in the apartment chart-sharing graph.',
      'radius5_replay':radius5,
      'centered_2plus2plus2':{'false_center':center,'incident_charts':incident,'pair_options_per_chart':{str(k):len(v) for k,v in pair_options.items()},'motifs_tested':motif_count,'first_step_repaired':motif_repaired,'fully_cleared':motif_cleared,'failures':motif_failures,'examples':examples},
      'original_failure_repair':'For errors {1,2,3,6,27,54}, the old max-vote tie is {0,1,2,3,6,27,54}. In the induced tie graph false center 0 has degree 6 and each true error degree 2, so the hub-pruned correction is exactly the six true errors.',
      'conclusion':'The modified rule preserves the proven radius-five monotonicity/three-sweep guarantee and repairs every centered 2+2+2 minimal false-center obstruction (32 representatives through a fixed center, hence all centers by apartment transitivity).',
      'boundary':'This is NOT yet a global radius-six theorem. Non-centered connected weight-six configurations still require an orbit-complete census or structural proof. Finite hard-decision decoder only; no ML/code-distance or noise claim.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
