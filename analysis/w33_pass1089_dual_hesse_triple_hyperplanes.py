from __future__ import annotations
import itertools,json,time
from collections import Counter,deque
from pathlib import Path
import numpy as np
from w33_pass1084_g32_g25_parabolic_normalizer import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1089_dual_hesse_triple_hyperplanes.json'
PMOD=43;OMOD=6

def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,x):return sum((a[i]*x[i] for i in range(3)),Z)
def incidence_profile(lines):
    pts={}
    for i,j in itertools.combinations(range(len(lines)),2):
        p=normE(cross(lines[i],lines[j]));pts[p]=tuple(k for k,l in enumerate(lines) if dot(l,p).z())
    return pts,Counter(len(v) for v in pts.values())
def vecset(xs):return {tuple(z.txt() for z in x) for x in xs}
def refl_mod(v):
    n=len(v);den=sum(x*x for x in v)%PMOD;c=(OMOD-1)*pow(den,-1,PMOD)%PMOD
    return tuple(((1 if i==j else 0)+c*v[i]*v[j])%PMOD for i in range(n) for j in range(n))
def mmod(A,B,n):return tuple(sum(A[n*i+k]*B[n*k+j] for k in range(n))%PMOD for i in range(n) for j in range(n))
def ident(n):return tuple(1 if i==j else 0 for i in range(n) for j in range(n))
def invmod(A,n):
    M=np.array(A,dtype=np.int64).reshape(n,n)%PMOD;aug=np.concatenate([M,np.eye(n,dtype=np.int64)],axis=1);r=0
    for c in range(n):
        q=next(i for i in range(r,n) if aug[i,c]);aug[[r,q]]=aug[[q,r]];aug[r]=aug[r]*pow(int(aug[r,c]),-1,PMOD)%PMOD
        for i in range(n):
            if i!=r and aug[i,c]:aug[i]=(aug[i]-aug[i,c]*aug[r])%PMOD
        r+=1
    return tuple(int(x) for x in aug[:,n:].flat)
def group(gens,n):
    I0=ident(n);seen={I0};q=deque([I0])
    while q:
        x=q.popleft()
        for g in gens:
            y=mmod(g,x,n)
            if y not in seen:seen.add(y);q.append(y)
    return list(seen)
def normmod(v):
    v=tuple(int(x)%PMOD for x in v)
    for x in v:
        if x:return tuple(y*pow(x,-1,PMOD)%PMOD for y in v)
    raise ValueError
def emod(x):return (x.a.numerator*pow(x.a.denominator,-1,PMOD)+OMOD*x.b.numerator*pow(x.b.denominator,-1,PMOD))%PMOD
def covact(h,A):
    Ai=np.array(invmod(A,3),dtype=np.int64).reshape(3,3);return normmod(np.array(h,dtype=np.int64)@Ai%PMOD)

def main():
    t=time.time();R4=[refl_exact(v) for v in DIRS];R3=[[row[:3] for row in R4[k][:3]] for k in range(3)]
    H32=cov_orbit((0,0,0,1),R4);H25=cov_orbit((0,0,1),R3);restricted=[];slice_count=0
    for h in H32:
        if all(x.z() for x in h[:3]):slice_count+=1
        else:restricted.append(normE(h[:3]))
    mult=Counter(restricted);extra=sorted([h for h,m in mult.items() if m==3],key=lambda v:tuple(x.txt() for x in v));roots=[ONE,W,-ONE-W]
    ceva={normE(v) for i,j in itertools.combinations(range(3),2) for r in roots for v in [tuple(ONE if k==i else (-r if k==j else Z) for k in range(3))]}
    epts,eprof=incidence_profile(extra);hpts,hprof=incidence_profile(H25);upts,uprof=incidence_profile(list(H25)+extra)
    extra_triples={p for p,inc in epts.items() if len(inc)==3};h25_quads={p for p,inc in hpts.items() if len(inc)==4};dual_extra_to_h25=vecset(extra_triples)==vecset(H25);dual_h25_to_extra=vecset(h25_quads)==vecset(extra)
    G25=group([refl_mod(DIRS[k][:3]) for k in range(3)],3);extraM=[normmod([emod(x) for x in h]) for h in extra];h25M=[normmod([emod(x) for x in h]) for h in H25];actions={}
    for name,S in [('extra9',extraM),('hesse12',h25M)]:
        idx={x:i for i,x in enumerate(S)};perms={tuple(idx[covact(h,A)] for h in S) for A in G25};actions[name]={'projective_image_order':len(perms),'scalar_kernel_order':len(G25)//len(perms),'transitive':len({p[0] for p in perms})==len(S),'point_stabilizer_order':len(perms)//len(S)}
    checks={'G32_hyperplanes40':len(H32)==40,'slice_unique':slice_count==1,'G25_hyperplanes12':len(H25)==12,'extra_count9':len(extra)==9,'all_extra_multiplicity3':all(mult[h]==3 for h in extra),'extra_equals_Ceva3_arrangement':set(extra)==ceva,'extra_is_9_lines_12_triple_points':len(epts)==12 and eprof==Counter({3:12}),'H25_is_12_lines_9_quadruple_12_double':len(hpts)==21 and hprof==Counter({4:9,2:12}),'mutual_projective_duality_12_triples_to_H25_lines':dual_extra_to_h25,'mutual_projective_duality_9_quads_to_extra_lines':dual_h25_to_extra,'union_profile_12_quintuple_9_quadruple_36_double':uprof==Counter({5:12,4:9,2:36}),'G25_order648':len(G25)==648,'projective_Hessian_image_order216':actions['extra9']['projective_image_order']==216 and actions['hesse12']['projective_image_order']==216,'central_scalar_kernel_C3':actions['extra9']['scalar_kernel_order']==3 and actions['hesse12']['scalar_kernel_order']==3,'both_arrangements_transitive':actions['extra9']['transitive'] and actions['hesse12']['transitive']}
    assert all(checks.values()),checks
    out={'schema':'w33.pass1089.dual_hesse_triple_hyperplanes.v1','status':'PASS','headline':'The nine multiplicity-three slice hyperplanes are identified objectwise: they are exactly the Ceva(3), equivalently dual-Hesse, arrangement x_i - omega^k x_j = 0. Their twelve triple points are precisely the twelve G25/Hesse hyperplane normals, while the nine quadruple points of the G25 Hesse arrangement are precisely the nine extra hyperplane normals. The two arrangements are mutually projectively dual.','extra_hyperplanes':[[x.txt() for x in h] for h in extra],'equations':'x_i - zeta*x_j = 0 for 1 <= i < j <= 3 and zeta in {1,omega,omega^2}','arrangements':{'extra9':{'name':'Ceva(3) / dual Hesse / reflection arrangement of G(3,3,3)','lines':9,'triple_points':12,'incidence':'(9_4,12_3)'},'G25_Hesse12':{'lines':12,'quadruple_points':9,'double_points':12,'incidence':'Hesse arrangement'},'union_intersection_profile':{str(k):v for k,v in sorted(uprof.items())}},'duality':{'extra_triple_points_equal_G25_line_normals':dual_extra_to_h25,'G25_quadruple_points_equal_extra_line_normals':dual_h25_to_extra},'group_action':{'G25_order':len(G25),**actions},'central_phase_reading':'The cube roots {1,omega,omega^2} label the three hyperplanes for each coordinate pair. G25 acts projectively through its Hessian quotient of order 216 with scalar C3 kernel. This supplies an exact central-phase geometry, but no identification with the repository nine-fiber objects is claimed without a separate equivariant map.','check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'seconds':time.time()-t,'scope':'Exact Q(omega) projective-arrangement computation plus faithful reduction modulo 43 for the group action.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
