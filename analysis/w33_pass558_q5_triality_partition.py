#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from collections import Counter,defaultdict
from pathlib import Path
from w33_pass543_547_common import charpoly_prime
from w33_pass553_five_point_core_geometry import A
from w33_pass555_all_fixed_magnitude_fibres import f2rank,translation_space

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass558_q5_triality_partition.json'

def basis(rows):
    b=[]
    for x in rows:
        y=x
        for p in b:y=min(y,y^p)
        if y:
            q=1<<(y.bit_length()-1)
            b=[z^y if z&q else z for z in b];b.append(y);b.sort(reverse=True)
    return tuple(b)

def reduce_mod(x,b):
    y=x
    for p in b:y=min(y,y^p)
    return y

def span(b):
    s={0}
    for x in b:s|={y^x for y in tuple(s)}
    return frozenset(s)

def mv(cols,x):
    y=0
    for i,c in enumerate(cols):
        if (x>>i)&1:y^=c
    return y

def comp(f,g):return tuple(mv(f,c) for c in g)
ID=(1,2,4,8)

def order(g):
    x=ID
    for n in range(1,121):
        x=comp(g,x)
        if x==ID:return n
    raise AssertionError('order overflow')

def inverse(g,G):return next(h for h in G if comp(g,h)==ID and comp(h,g)==ID)

def closure(gens):
    H={ID};changed=True
    while changed:
        changed=False
        for a in tuple(H):
            for b in tuple(gens)+tuple(H):
                c=comp(a,b)
                if c not in H:H.add(c);changed=True
    return frozenset(H)

def five_cube_fibres():
    fibres=defaultdict(set)
    for m in range(4096):
        offs=tuple(a*(4 if (m>>i)&1 else 1)%5 for i,a in enumerate(A))
        fibres[tuple(charpoly_prime(5,offs)[0])].add(m)
    out=[]
    for idx,(cpv,S0) in enumerate(sorted(fibres.items(),key=lambda kv:json.dumps(kv[0],separators=(',',':')))):
        S=frozenset(S0);T=translation_space(S)
        if len(S)==80 and f2rank(T)==4 and len(S)//len(T)==5:
            out.append((idx,cpv,S,T))
    return out

def quotient_partition(rows):
    T=rows[0][3];Tb=basis(T)
    blocks=[]
    for _,_,S,_ in rows:blocks.append(frozenset(reduce_mod(x,Tb) for x in S))
    U=frozenset().union(*blocks);Ub=basis(U);L=span(Ub);missing=next(iter(L-U))
    P=frozenset(x^missing for x in U);B=basis(P)
    coord={}
    for mask in range(16):
        x=0
        for i,b in enumerate(B):
            if (mask>>i)&1:x^=b
        coord[x]=mask
    blocks4=[frozenset(coord[x^missing] for x in block) for block in blocks]
    return T,Tb,blocks,U,missing,B,blocks4

def gl4():
    return [g for g in itertools.permutations(range(1,16),4) if f2rank(g)==4]

def cycle_type(p):
    seen=set();out=[]
    for i in range(len(p)):
        if i not in seen:
            j=i;n=0
            while j not in seen:seen.add(j);n+=1;j=p[j]
            out.append(n)
    return tuple(sorted(out))

def quadratic_zero_set(coeff):
    z=set()
    for x in range(1,16):
        bits=[(x>>i)&1 for i in range(4)];v=0;k=0
        for i in range(4):v^=((coeff>>k)&1)&bits[i];k+=1
        for i in range(4):
            for j in range(i+1,4):v^=((coeff>>k)&1)&bits[i]&bits[j];k+=1
        if v==0:z.add(x)
    return frozenset(z)

def payload():
    rows=five_cube_fibres();T,Tb,blocks,U,missing,B,blocks4=quotient_partition(rows)
    mats=gl4();part=frozenset(blocks4)
    G=[];acts={}
    for g in mats:
        image=frozenset(frozenset(mv(g,x) for x in b) for b in blocks4)
        if image==part:
            G.append(g)
            acts[g]=tuple(next(j for j,c in enumerate(blocks4) if frozenset(mv(g,x) for x in blocks4[i])==c) for i in range(3))
    inv={g:inverse(g,G) for g in G};K=[g for g in G if acts[g]==(0,1,2)]
    comms={comp(comp(comp(g,h),inv[g]),inv[h]) for g in G for h in G};derived=closure(tuple(comms))
    r=next(g for g in G if order(g)==15)
    s=next(g for g in G if order(g)==4 and comp(comp(g,r),inv[g])==comp(r,r))
    generated=closure((r,s))
    qforms=[]
    for b in blocks4:
        hits=[c for c in range(1<<10) if quadratic_zero_set(c)==b]
        qforms.append(hits[0] if len(hits)==1 else None)
    caps=[all((x^y) not in b for x,y in itertools.combinations(b,2)) for b in blocks4]
    cap_stabs=[sum({mv(g,x) for x in b}==set(b) for g in mats) for b in blocks4]
    quartic=[cpv[4] for _,cpv,_,_ in rows]
    quartic_sum=tuple(sum(v[i] for v in quartic) for i in range(4))
    centered=[tuple(3*v[i]-quartic_sum[i] for i in range(4)) for v in quartic]
    checks={
      'exactly_three_five_cube_fibres':len(rows)==3,
      'common_translation_space_dimension4':all(x[3]==T for x in rows) and len(T)==16 and f2rank(T)==4,
      'quotient_has_fifteen_distinct_cosets':len(U)==15,
      'quotient_is_pg32_nonzero_points':len(span(basis(U)))==16 and len(span(basis(U))-U)==1,
      'three_blocks_partition_pg32':len(set().union(*map(set,blocks4)))==15 and sum(map(len,blocks4))==15,
      'each_block_is_five_cap':all(caps),
      'each_block_unique_elliptic_quadric':all(x is not None for x in qforms),
      'each_cap_stabilizer_is_s5_order120':cap_stabs==[120,120,120],
      'partition_stabilizer_order60':len(G)==60,
      'full_s3_triality_on_blocks':len(set(acts.values()))==6,
      'triality_kernel_is_d10':len(K)==10 and Counter(order(g) for g in K)==Counter({2:5,5:4,1:1}),
      'derived_subgroup_is_c15':len(derived)==15 and Counter(order(g) for g in derived)==Counter({15:8,5:4,3:2,1:1}),
      'semidirect_generators_c15_c4_action2':order(r)==15 and order(s)==4 and comp(comp(s,r),inv[s])==comp(r,r) and len(generated)==60,
      'element_order_census_exact':Counter(order(g) for g in G)==Counter({4:30,6:10,15:8,2:5,5:4,3:2,1:1}),
      'quartic_levels_form_three_point_orbit':len(set(quartic))==3 and len(set(acts.values()))==6,
      'centered_quartic_vectors_sum_zero':all(sum(v[i] for v in centered)==0 for i in range(4)),
    }
    return {
      'schema':'w33.pass558.q5_triality_partition.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'fibre_ids':[x[0] for x in rows],
      'common_translation_space':{'dimension':4,'size':len(T),'basis':[hex(x) for x in Tb]},
      'pg32_partition':{'missing_origin_representative':hex(missing),'coordinate_basis':[hex(x) for x in B],'blocks':[[format(x,'04b') for x in sorted(b)] for b in blocks4],'quadratic_form_masks':[hex(x) for x in qforms],'interpretation':'The 15 quotient cosets are PG(3,2); the three spectral fibres are a partition into three elliptic quadrics Q^-(3,2), each a five-cap.'},
      'partition_stabilizer':{'order':len(G),'isomorphism':'C15 semidirect C4, with the C4 generator acting by r -> r^2','generator_r_columns':[format(x,'04b') for x in r],'generator_s_columns':[format(x,'04b') for x in s],'derived_subgroup':'C15','block_action':'S3','block_action_kernel':'D10','kernel_order':len(K),'element_order_histogram':dict(sorted(Counter(order(g) for g in G).items())),'individual_cap_stabilizers':cap_stabs},
      'quartic_covariant':{'levels':quartic,'centered_integer_vectors':centered,'representation':'The three quartic values carry the S3 permutation module 1+2. The order-three subgroup cyclically permutes them. They are one quartic covariant orbit, not a Z3 grading by polynomial degree.'},
      'checks':checks,
      'boundary':'The triality theorem is exact inside the fixed Pass-540 magnitude cube after quotienting by the common translation space. The S3 action is an intrinsic quotient symmetry; it is not asserted to be an unrestricted physical Clifford gate on the original section space.'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 558 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'group_order':p['partition_stabilizer']['order']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
