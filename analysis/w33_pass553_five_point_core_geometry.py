#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from collections import Counter
from pathlib import Path
from w33_pass543_547_common import classes,cp,charpoly_prime

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass553_five_point_core_geometry.json'
A=(1,1,2,2,2,3,3,2,3,2,3,2)
BASIS=(0x001,0x002,0x07c,0x0f8,0x120,0x3d0,0x440,0xf80)
CORE=((0,0,0,0),(0,0,1,0),(0,0,1,1),(1,0,0,0),(1,1,0,0))
FREE=(0,1,2,7)

def f2rank_int(rows):
    b=[]
    for x in rows:
        y=x
        for p in b:y=min(y,y^p)
        if y:
            q=1<<(y.bit_length()-1)
            b=[z^y if z&q else z for z in b];b.append(y);b.sort(reverse=True)
    return len(b)

def bits(v):return sum((x&1)<<i for i,x in enumerate(v))
def from_y(y):
    x=0
    for i,b in enumerate(BASIS):
        if (y>>i)&1:x^=b
    return x

def core_component(core):
    out=set()
    for f in range(16):
        y=0
        for j,i in enumerate(FREE):y|=((f>>j)&1)<<i
        for j,i in enumerate((3,4,5,6)):y|=core[j]<<i
        out.add(from_y(y))
    return frozenset(out)

def mat_vec(cols,x):
    y=0
    for i,c in enumerate(cols):
        if (x>>i)&1:y^=c
    return y

def solve_cols(src,dst):
    lookup={mat_vec(src,x):x for x in range(16)}
    return tuple(mat_vec(dst,lookup[1<<i]) for i in range(4))

def affine_simplex_maps():
    P=[bits(x) for x in CORE];src=tuple(P[i]^P[0] for i in range(1,5));maps=[];restr=[]
    for perm in itertools.permutations(range(5)):
        t=P[perm[0]];dst=tuple(P[perm[i]]^t for i in range(1,5));cols=solve_cols(src,dst)
        image=tuple(mat_vec(cols,x)^t for x in P)
        if image!=tuple(P[i] for i in perm):raise AssertionError((perm,image))
        if f2rank_int(cols)!=4:raise AssertionError('singular')
        maps.append((cols,t));restr.append(perm)
    return maps,restr

def signed_magnitude_actions():
    C=classes(5);idx={v:i for i,v in enumerate(C)};actions=set()
    for a,b,c,d in itertools.product(range(5),repeat=4):
        det=(a*d-b*c)%5
        if det not in (1,4):continue
        perm=[None]*12;flip=0;ok=True
        for i,v in enumerate(C):
            w=((a*v[0]+b*v[1])%5,(c*v[0]+d*v[1])%5);can=cp(w,5);j=idx[can]
            sgn=1 if w==can else 4
            if A[i]*A[i]%5 != A[j]*A[j]%5:ok=False;break
            ratio=sgn*A[i]*pow(A[j],-1,5)%5
            perm[j]=i
            if ratio==4:flip|=1<<j
        if ok:actions.add((tuple(perm),flip))
    return sorted(actions)

def apply_action(m,action):
    p,f=action
    return sum(((m>>p[j])&1)<<j for j in range(12))^f

def intrinsic_cosets(S):
    base=next(iter(S));T=frozenset(x^base for x in S if all((y^(x^base)) in S for y in S))
    unseen=set(S);cosets=[]
    while unseen:
        x=next(iter(unseen));co=frozenset(x^t for t in T);cosets.append(co);unseen-=co
    return T,cosets

def induced_core_group(actions,S):
    T,comps=intrinsic_cosets(S);ci={x:i for i,x in enumerate(comps)};ind=[]
    for g in actions:
        q=[]
        for C in comps:q.append(ci[frozenset(apply_action(x,g) for x in C)])
        ind.append(tuple(q))
    return sorted(set(ind)),comps,T

def target_set():
    target=tuple(charpoly_prime(5,A)[0]);out=set()
    for m in range(1<<12):
        offs=tuple(a*(4 if (m>>i)&1 else 1)%5 for i,a in enumerate(A))
        if tuple(charpoly_prime(5,offs)[0])==target:out.add(m)
    return frozenset(out)

def cycle_type(p):
    seen=set();c=[]
    for i in range(len(p)):
        if i not in seen:
            j=i;n=0
            while j not in seen:seen.add(j);n+=1;j=p[j]
            c.append(n)
    return tuple(sorted(c))

def payload():
    maps,restr=affine_simplex_maps();actions=signed_magnitude_actions();S=target_set();ind,comps,T=induced_core_group(actions,S)
    ct=Counter(cycle_type(p) for p in ind)
    zeros=[]
    for z in itertools.product((0,1),repeat=4):
        q=(z[1]*(1^z[0]),z[0]*z[2],z[3]*(1^z[2]))
        if q==(0,0,0):zeros.append(z)
    eval_rows=[[1,*z] for z in CORE]
    eval_rank=f2rank_int([sum(v<<i for i,v in enumerate(r)) for r in eval_rows])
    checks={
      'core_has_five_points':len(CORE)==5 and len(set(CORE))==5,
      'core_is_affine_4_simplex':f2rank_int([bits(CORE[i])^bits(CORE[0]) for i in range(1,5)])==4,
      'all_120_permutations_extend_affinely':len(set(maps))==120 and len(set(restr))==120,
      'full_affine_automorphism_group_S5':len(maps)==math.factorial(5),
      'three_quadrics_cut_exactly_core':set(zeros)==set(CORE),
      'boolean_coordinate_ring_dimension5':eval_rank==5,
      'radical_primary_decomposition_five_points':len(zeros)==5,
      'signed_magnitude_stabilizer_order40':len(actions)==40,
      'intrinsic_translation_space_dimension4':len(T)==16 and f2rank_int(T)==4,
      'physical_component_action_D10':len(ind)==10,
      'D10_cycle_census':ct==Counter({(1,1,1,1,1):1,(5,):4,(1,2,2):5}),
      'five_parallel_cubes_partition_target':len(comps)==5 and all(len(x)==16 for x in comps) and frozenset().union(*comps)==S,
    }
    maximal=[{'point':z,'maximal_ideal':[f'z{i}+{v}' if v else f'z{i}' for i,v in enumerate(z)]} for z in CORE]
    return {
      'schema':'w33.pass553.five_point_core_geometry.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'core':{'points':CORE,'affine_span_dimension':4,'interpretation':'An affine 4-simplex (five-point cap) in AG(4,2).'},
      'automorphisms':{'full_affine_group':'S5','order':len(maps),'signed_fibre_stabilizer_order':len(actions),'projective_fibre_stabilizer_order':len(actions)//2,'component_image':'D10 (order 10)','component_image_order':len(ind),'component_kernel_signed':len(actions)//len(ind),'index_of_component_image_in_S5':len(maps)//len(ind),'cycle_type_census':{str(k):v for k,v in sorted(ct.items())}},
      'boolean_ideal':{'equations':['z1*(1+z0)','z0*z2','z3*(1+z2)'],'field_equations':['z0^2+z0','z1^2+z1','z2^2+z2','z3^2+z3'],'standard_function_basis':['1','z0','z1','z2','z3'],'quotient_dimension':5,'primary_decomposition':'intersection of the five point maximal ideals','maximal_ideals':maximal},
      'spectral_embedding':{'target_fibre_size':len(S),'parallel_cube_count':5,'cube_dimension':4,'free_coordinates':['y0','y1','y2','y7'],'physical_subgroup_action':'transitive D10 action on the five intrinsic translation cosets; the signed order-40 stabilizer has a four-element within-cube kernel'},
      'checks':checks,
      'boundary':'S5 is the intrinsic affine automorphism group of the five-point core. The signed physical stabilizer has order 40, its projective quotient has order 20, and its action on the five parallel cubes factors through D10 with a nontrivial within-cube kernel. Thus the physical frame realizes only an order-10 component image, not all of S5.'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 553 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
