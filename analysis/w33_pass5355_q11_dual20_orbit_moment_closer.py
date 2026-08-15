#!/usr/bin/env python3
"""Pass5355: if Pass5349 or Pass5354 finds a q11 dual20 witness, try to close primal d=121 by the full PSp4(11) pair-orbital moment method.

For a transitive G-orbit of weight-w dual checks, let v_i be the valency of an
unordered pair orbital and c_i the number of seed pairs in that orbital. If N
is the check-orbit size, coordinate replication is r=Nw/n and pair codegree is
lambda_i=2Nc_i/(n v_i), hence
  r/lambda_i = w v_i/(2 c_i).
The unknown orbit size N cancels. Therefore we need only the carrier action,
its unordered pair orbitals, and one verified dual20 seed. If the minimum ratio
is 120, the even-intersection moment lemma gives primal weight >=121; point
footprints have weight121, closing [7381,671,121]_2.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
from analysis.w33_pass5304_q11_dual20_density_wall import carriers
from analysis.w33_pass5293_allodd_rank_reduction_q11 import norm,sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5355_Q11_DUAL20_ORBIT_MOMENT.json'
Q=11

def load_seed():
    for p in (ROOT/'data/PART_W33_PASS5349_Q11_DUAL20_DOUBLECOVER_XORSAT.json',
              ROOT/'data/PART_W33_PASS5354_Q11_CYCLIC_CAYLEY_DUAL20_SEARCH.json'):
        if not p.exists():continue
        d=json.loads(p.read_text())
        if d.get('status')=='THEOREM_Q11_DUAL20_EQUALITY_WITNESS':return d['selected_carriers'],str(p)
        if d.get('status')=='THEOREM_Q11_CYCLIC_CAYLEY_DUAL20_EQUALITY_WITNESS':return d['witness']['selected_carriers'],str(p)
    return None,None

def main():
    seed,source=load_seed()
    if seed is None:
        out={'pass':5355,'status':'SKIPPED_NO_Q11_DUAL20_WITNESS','boundary':'Moment closure requires a verified dual20 seed.'}
        OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));return
    P,C=carriers(Q);pi={p:i for i,p in enumerate(P)};bk={c:i for i,c in enumerate(C)};n=len(C)
    bits=[]
    for B in C:
        z=0
        for p in B:z|=1<<p
        bits.append(z)
    z=0
    for j in seed:z^=bits[j]
    assert len(seed)==20 and z==0
    def trans_perm(v,a=1):
        pp=[]
        for x in P:
            s=a*sp(x,v,Q)%Q
            y=tuple((x[k]+s*v[k])%Q for k in range(4))
            pp.append(pi[norm(y,Q)])
        return [bk[tuple(sorted(pp[p] for p in B))] for B in C]
    vs=[((1,0,0,0),1),((0,1,0,0),1),((0,0,1,0),1),((0,0,0,1),1),
        ((1,1,0,0),1),((1,0,0,1),1),((1,0,1,0),1),((0,1,0,1),1),
        ((1,0,0,0),2),((0,1,0,0),2)]
    gens=[Permutation(trans_perm(v,a)) for v,a in vs]
    G=PermutationGroup(gens);want=Q**4*(Q**4-1)*(Q**2-1)//2
    order=G.order();assert order==want,(order,want)
    base,strong=G.schreier_sims_incremental(base=[0]);sg=[g for g in strong if g(0)==0]
    rem=set(range(n));orbs=[]
    while rem:
        s=next(iter(rem));O={s};todo=[s];rem.remove(s)
        while todo:
            u=todo.pop()
            for g in sg:
                v=g(u)
                if v in rem:rem.remove(v);O.add(v);todo.append(v)
        orbs.append(O)
    zero=next(i for i,O in enumerate(orbs) if 0 in O);assert len(orbs[zero])==1
    rid={x:i for i,O in enumerate(orbs) for x in O}
    tr={zero:zero}
    for i,O in enumerate(orbs):
        if i==zero:continue
        j=next(iter(O));g=G.orbit_rep(j,0);tr[i]=rid[g(0)]
    # fuse transpose suborbits into unordered pair classes
    classes=[];seen={zero}
    for i in range(len(orbs)):
        if i in seen:continue
        j=tr[i];S={i,j};seen|=S;classes.append(tuple(sorted(S)))
    cid={i:k for k,S in enumerate(classes) for i in S}
    val=[sum(len(orbs[i]) for i in S) for S in classes]
    counts=Counter()
    for a,b in itertools.combinations(seed,2):
        g=G.orbit_rep(a,0);counts[cid[rid[g(b)]]]+=1
    rec=[];rat=[]
    for k,S in enumerate(classes):
        c=counts[k];v=val[k]
        ratio=None if c==0 else Fraction(20*v,2*c)
        if ratio is not None:rat.append(ratio)
        rec.append({'suborbit_indices':list(S),'unordered_valency':v,'seed_pairs':c,
                    'r_over_lambda':None if ratio is None else (str(ratio.numerator) if ratio.denominator==1 else f'{ratio.numerator}/{ratio.denominator}')})
    m=min(rat);assert sum(counts.values())==190
    point_weight=121
    if m>=120:
        # A ratio >120 would contradict the known primal point row of weight121, so exact closure must hit 120.
        assert m==120
        status='THEOREM_Q11_FOOTPRINT_CODE_7381_671_121'
        conclusion='The dual20 orbit gives r/lambda_max=120, hence every nonzero primal word has weight>=121; point footprints attain121.'
    else:
        status='Q11_DUAL20_ORBIT_MOMENT_INSUFFICIENT'
        conclusion=f'The witness exists but its worst pair orbital gives r/lambda={m}<120, so this orbit alone does not close d=121.'
    out={'pass':5355,'status':status,'seed_source':source,'PSp4_11_order':order,'P_components':n,
         'point_footprint_weight':point_weight,'point_stabilizer_suborbits':len(orbs),'unordered_pair_orbits':len(classes),
         'pair_orbitals':rec,'minimum_r_over_lambda':str(m),'conclusion':conclusion,
         'boundary':'If insufficient, no claim about d=121 follows; additional dual orbits/fused moment constraints may still close it.'}
    if status.startswith('THEOREM_'):out['footprint_code']='[7381,671,121]_2'
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
