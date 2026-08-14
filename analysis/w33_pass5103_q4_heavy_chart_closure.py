#!/usr/bin/env python3
"""Pass5103: close the q=4 heavy-chart wall and minimum shell.

Pass5090 proved: if every active K5 chart is a minimum 1|4 cut, a nonzero
word is a chamber star.  Here we condition one heavy 2|3 cut and minimize
weight exactly.  A fixed apartment has four chart roles.  In each role the
PGL(2,4) stabilizer of the selected projective-line edge is S3 and is
transitive on the six heavy cuts crossing that edge, so one heavy pattern per
role suffices.  All four MILPs have exact optimum 384.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.optimize import milp,Bounds,LinearConstraint
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5103_Q4_HEAVY_CHART_CLOSURE.json'

def fixed_chart_min(G,ci,smallside,seconds=120):
    n=len(G['apartments']);theta=[]
    for _,loc in G['charts']:
        for i,j,k in itertools.combinations(range(5),3):
            theta.append((loc[tuple(sorted((i,j)))],loc[tuple(sorted((i,k)))],loc[tuple(sorted((j,k)))]))
    nt=len(theta);rr=[];cc=[];vv=[];lo=[];hi=[];r=0
    for k,(i,j,l) in enumerate(theta):
        rr += [r]*4;cc += [i,j,l,n+k];vv += [1.,1.,1.,-2.];lo.append(0.);hi.append(0.);r+=1
    S=set(smallside);typ,loc=G['charts'][ci]
    for e,a in loc.items():
        bit=int((e[0] in S)^(e[1] in S));rr.append(r);cc.append(a);vv.append(1.);lo.append(bit);hi.append(bit);r+=1
    A=sparse.coo_matrix((vv,(rr,cc)),shape=(r,n+nt)).tocsr();c=np.zeros(n+nt);c[:n]=1.
    res=milp(c=c,integrality=np.ones(n+nt,dtype=np.int8),bounds=Bounds(np.zeros(n+nt),np.ones(n+nt)),
             constraints=LinearConstraint(A,np.array(lo),np.array(hi)),options={'time_limit':seconds,'mip_rel_gap':0.0})
    return res

def gf4_mul(a,b):
    a0,a1=a&1,(a>>1)&1;b0,b1=b&1,(b>>1)&1
    c0=a0*b0;c1=(a0*b1)^(a1*b0);c2=a1*b1
    return (c0^c2)|((c1^c2)<<1)
def gf4_inv(a):return next(b for b in range(1,4) if gf4_mul(a,b)==1)
def pgl2_edge_stabilizer_check():
    P=[(x,1) for x in range(4)]+[(1,0)]
    def act(M,p):
        a,b,c,d=M;x,y=p;u=gf4_mul(a,x)^gf4_mul(b,y);v=gf4_mul(c,x)^gf4_mul(d,y)
        return (gf4_mul(u,gf4_inv(v)),1) if v else (1,0)
    perms=set()
    for M in itertools.product(range(4),repeat=4):
        a,b,c,d=M
        if gf4_mul(a,d)^gf4_mul(b,c):perms.add(tuple(P.index(act(M,p)) for p in P))
    assert len(perms)==60
    pair=frozenset((0,1));stab=[p for p in perms if frozenset((p[0],p[1]))==pair];assert len(stab)==6
    heavy={frozenset((e,r)) for e in pair for r in range(2,5)};S=next(iter(heavy));orb={frozenset(p[i] for i in S) for p in stab}
    assert orb==heavy
    return {'PGL2_4_order':60,'selected_edge_stabilizer_order':6,'heavy_patterns':6,'heavy_pattern_orbit_size':6}

def main():
    G=build_W(4);stars=chamber_stars(G);star_index={z:i for i,z in enumerate(stars)}
    # Deterministic representatives of the four fixed-apartment chart roles from Pass5090.
    representatives=[0,64,2720,2784];records=[]
    for ci in representatives:
        typ,loc=G['charts'][ci];base_pair=next(e for e,a in loc.items() if a==0);i,j=base_pair;r=next(x for x in range(5) if x not in base_pair)
        res=fixed_chart_min(G,ci,{i,r});assert res.success and int(round(res.fun))==384 and float(res.mip_gap)==0.0
        xb=np.rint(res.x[:len(G['apartments'])]).astype(np.int8);word=sum(int(v)<<a for a,v in enumerate(xb));pair=None
        for s,z in enumerate(stars):
            t=star_index.get(word^z)
            if t is not None:pair=(s,t,G['flags'][s],G['flags'][t]);break
        assert pair is not None
        records.append({'chart_index':ci,'type':typ,'selected_apartment_local_edge':list(base_pair),'heavy_small_side':[i,r],
                        'objective':384,'mip_gap':0.0,'mip_nodes':int(getattr(res,'mip_node_count',-1)),
                        'two_star_witness':[pair[0],pair[1]],'two_star_flags':[list(pair[2]),list(pair[3])]})
    out={'pass':5103,'status':'THEOREM_Q4_COMPLETE_MINIMUM_SHELL_AND_ACTIVE_EXPANSION','q':4,
         'local_symmetry':pgl2_edge_stabilizer_check(),'four_chart_role_milps':records,'heavy_chart_global_minimum':384,
         'minimum_shell':{'code':'[13600,256,256]_2','minimum_words':425,'identification':'exactly the 425 chamber stars'},
         'active_chart_theorem':'Every nonzero q4 word has A(y)>=256=4q^3. Chamber stars attain equality.',
         'proof':'No-heavy words are chamber stars by Pass5090. A heavy 2|3 chart forces wt>=384. Since every q4 local cut has weight <=6, 4wt=sum local weights<=6A, so every heavy word has A>=256.',
         'boundary':'This closes q4, not q>=5 or arbitrary-q distance.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
