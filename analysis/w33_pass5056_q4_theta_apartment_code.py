#!/usr/bin/env python3
"""Pass 5056: exact q=4 theta/apartment binary-code anchor."""
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.optimize import Bounds,LinearConstraint,milp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5056_Q4_THETA_APARTMENT_CODE.json'

def add(a,b): return a^b

def mul(a,b):
    a0,a1=a&1,(a>>1)&1;b0,b1=b&1,(b>>1)&1
    c0=a0*b0;c1=(a0*b1)^(a1*b0);c2=a1*b1
    return (c0^c2)|((c1^c2)<<1)
INV={a:next(b for b in range(1,4) if mul(a,b)==1) for a in range(1,4)}
def smul(a,v): return tuple(mul(a,x) for x in v)
def vadd(x,y): return tuple(add(a,b) for a,b in zip(x,y))
def normalize(v):
    for x in v:
        if x:return smul(INV[x],v)
    raise ValueError('zero vector')
def projective_points():
    return sorted({normalize(v) for v in itertools.product(range(4),repeat=4) if any(v)})
def symp(x,y):
    return add(add(mul(x[0],y[2]),mul(x[2],y[0])),add(mul(x[1],y[3]),mul(x[3],y[1])))
def line_span(x,y):
    out={normalize(vadd(x,smul(t,y))) for t in range(4)};out.add(normalize(y));return frozenset(out)
def gf2_rank(rows):
    piv={}
    for r0 in rows:
        r=r0
        while r:
            p=r.bit_length()-1
            if p in piv:r^=piv[p]
            else:piv[p]=r;break
    return len(piv)

def build_geometry():
    pts=projective_points();assert len(pts)==85
    pidx={p:i for i,p in enumerate(pts)};nbr=[set() for _ in pts];lineset=set()
    for i,j in itertools.combinations(range(85),2):
        if symp(pts[i],pts[j])==0:
            nbr[i].add(j);nbr[j].add(i);lineset.add(frozenset(pidx[z] for z in line_span(pts[i],pts[j])))
    assert {len(x) for x in nbr}=={20}
    lines=sorted(lineset,key=lambda s:tuple(sorted(s)));assert len(lines)==85 and {len(L) for L in lines}=={5}
    pair_line={}
    for li,L in enumerate(lines):
        for a,b in itertools.combinations(sorted(L),2):pair_line[(a,b)]=li
    flags=[(p,li) for li,L in enumerate(lines) for p in sorted(L)];assert len(flags)==425
    fidx={f:i for i,f in enumerate(flags)}
    apt_points=set();opposite_point_pairs=[]
    for p,q in itertools.combinations(range(85),2):
        if q not in nbr[p]:
            common=sorted(nbr[p]&nbr[q]);assert len(common)==5;opposite_point_pairs.append((p,q,common))
            for a,b in itertools.combinations(common,2):
                S=frozenset((p,q,a,b));assert sum(1 for x,y in itertools.combinations(S,2) if y in nbr[x])==4;apt_points.add(S)
    assert len(opposite_point_pairs)==2720 and len(apt_points)==13600
    apartments=sorted(apt_points,key=lambda s:tuple(sorted(s)));apt_index_by_points={S:i for i,S in enumerate(apartments)}
    apt_line_sets=[];apt_cycle_rows=[]
    for S in apartments:
        edges=[(a,b) for a,b in itertools.combinations(sorted(S),2) if b in nbr[a]];assert len(edges)==4
        ls=frozenset(pair_line[tuple(sorted(e))] for e in edges);assert len(ls)==4;apt_line_sets.append(ls)
        bits=0
        for a,b in edges:
            li=pair_line[tuple(sorted((a,b)))];bits^=1<<fidx[(a,li)];bits^=1<<fidx[(b,li)]
        assert bits.bit_count()==8;apt_cycle_rows.append(bits)
    apt_index_by_lines={S:i for i,S in enumerate(apt_line_sets)};assert len(apt_index_by_lines)==13600
    theta=[]
    for p,q,common in opposite_point_pairs:
        local={(i,j):apt_index_by_points[frozenset((p,q,common[i],common[j]))] for i,j in itertools.combinations(range(5),2)}
        for i,j,k in itertools.combinations(range(5),3):theta.append(tuple(sorted((local[(i,j)],local[(i,k)],local[(j,k)]))))
    assert len(theta)==27200
    line_nbr=[set() for _ in lines]
    for i,j in itertools.combinations(range(85),2):
        if lines[i]&lines[j]:assert len(lines[i]&lines[j])==1;line_nbr[i].add(j);line_nbr[j].add(i)
    assert {len(x) for x in line_nbr}=={20}
    opposite_line_pairs=[]
    for l,m in itertools.combinations(range(85),2):
        if m not in line_nbr[l]:
            common=sorted(line_nbr[l]&line_nbr[m]);assert len(common)==5;opposite_line_pairs.append((l,m,common))
            local={(i,j):apt_index_by_lines[frozenset((l,m,common[i],common[j]))] for i,j in itertools.combinations(range(5),2)}
            for i,j,k in itertools.combinations(range(5),3):theta.append(tuple(sorted((local[(i,j)],local[(i,k)],local[(j,k)]))))
    assert len(opposite_line_pairs)==2720 and len(theta)==54400 and len(set(theta))==54400
    return {'points':pts,'nbr':nbr,'lines':lines,'flags':flags,'apartments':apartments,'apartment_line_sets':apt_line_sets,'apt_index_by_points':apt_index_by_points,'apt_index_by_lines':apt_index_by_lines,'apartment_cycle_rows':apt_cycle_rows,'theta':theta,'opposite_point_pairs':opposite_point_pairs,'opposite_line_pairs':opposite_line_pairs,'fidx':fidx,'pair_line':pair_line}

def exact_distance_milp(theta,napt):
    m=len(theta);nvar=napt+m;rr=[];cc=[];vv=[]
    for r,(i,j,k) in enumerate(theta):rr += [r,r,r,r];cc += [i,j,k,napt+r];vv += [1.,1.,1.,-2.]
    A=sparse.coo_matrix((vv,(rr,cc)),shape=(m,nvar)).tocsr();c=np.zeros(nvar);c[:napt]=1.;lb=np.zeros(nvar);ub=np.ones(nvar);lb[0]=ub[0]=1.
    res=milp(c=c,integrality=np.ones(nvar,dtype=np.int8),bounds=Bounds(lb,ub),constraints=LinearConstraint(A,np.zeros(m),np.zeros(m)),options={'mip_rel_gap':0.0})
    assert res.success;val=int(round(res.fun));x=np.rint(res.x[:napt]).astype(np.int8)
    assert int(x.sum())==val and all((int(x[i])+int(x[j])+int(x[k]))%2==0 for i,j,k in theta)
    return {'objective':val,'mip_gap':float(getattr(res,'mip_gap',0.0)),'mip_node_count':int(getattr(res,'mip_node_count',-1)),'status':int(res.status),'message':str(res.message)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-milp',action='store_true');ap.add_argument('--out',type=Path,default=OUT);args=ap.parse_args()
    G=build_geometry();apt_rows=G['apartment_cycle_rows'];theta=G['theta'];napt=len(apt_rows)
    cycle_rank=gf2_rank(apt_rows);theta_rows=[(1<<i)^(1<<j)^(1<<k) for i,j,k in theta];theta_rank=gf2_rank(theta_rows);per=Counter()
    for t in theta:per.update(t)
    assert cycle_rank==256 and theta_rank==napt-cycle_rank==13344 and set(per.values())=={12}
    assert all((apt_rows[i]^apt_rows[j]^apt_rows[k])==0 for i,j,k in theta)
    distance=None if args.skip_milp else exact_distance_milp(theta,napt)
    if distance is not None:assert distance['objective']==256 and distance['mip_gap']==0.0
    result={'pass':5056,'status':'PASS','field':'GF(4)=F2[a]/(a^2+a+1)','q':4,'geometry':{'points':85,'lines':85,'chambers_flags':425,'point_degree':20,'levi_cycle_rank':256,'opposite_point_pairs':2720,'opposite_line_pairs':2720},'apartments':13600,'apartment_cycle_weight':8,'apartment_cycle_rank_f2':cycle_rank,'theta_checks':54400,'theta_check_weight':3,'theta_check_rank_f2':theta_rank,'dual_dimension':napt-cycle_rank,'theta_checks_per_apartment':12,'theta_checks_span_full_dual':True,'code_without_distance':[13600,256],'distance_milp':distance,'distance_milp_normalization':'fixed apartment x_0=1; valid by strong/apartment transitivity of the type-C2 building','code':[13600,256,256] if distance else None,'formula_checks':{'apartments':'q^4(q+1)^2(q^2+1)/8 = 13600','theta_checks':'q^3(q+1)(q^2+1) C(q+1,3) = 54400','checks_per_apartment':'4(q-1) = 12','dimension':'q^4 = 256'},'boundary':'This closes the Pass5051 conjectural code/distance statement at q=4 only. The local theta presentation is compatible with the symplectic Steinberg module, but arbitrary-q full-dual generation and distance q^4 remain open.'}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
