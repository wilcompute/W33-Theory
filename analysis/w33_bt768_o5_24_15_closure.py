#!/usr/bin/env python3
"""BT768 closure: the missing 15-sector is the 36-spread O(5,3) polar frame.

BT768 constructed 45 intrinsic W33 K4,4 octets, with point/octet incidence M,
and proved

    M M^T = 8I + J + 2A,
    spec(MM^T) = 72^1, 12^24, 0^15.

It ended by asking for the missing 15-sector object killed by M. This verifier
answers that question intrinsically from W33, without importing Holotrade data.

Put the 40 W33 lines into the 5D orthogonal module

    W = ker(omega : Lambda^2 F_3^4 -> F_3)

by Pluecker coordinates. The 121 projective points of W split by the Pfaffian
quadratic form Q into 40 isotropic, 45 square, and 36 nonsquare points.

For isotropic line-coordinate y define polar incidence with the two nonzero
orbits:

    D[y,c]=1 iff B_Q(y,c)=0, c square,       D is 40x45,
    C[y,z]=1 iff B_Q(y,z)=0, z nonsquare,    C is 40x36.

The square polar section has 16 W33 lines. Incidence through W33 points has
multiplicity 4 on exactly eight points and 1 on the other 32; those eight-point
sets are exactly BT768's intrinsic K4,4 octets. The nonsquare polar section has
ten W33 lines, pairwise disjoint and covering all 40 points; the 36 sections are
exactly all 36 spreads by independent exact-cover enumeration.

After centering columns,

    D0 D0^T = 18 P_24,
    C0 C0^T = 18 P_15,
    P_24 P_15 = 0,
    P_24 + P_15 = I - J/40.

If N is W33 point-line incidence and M is the point/octet matrix, then

    N D = J + 3M,       N D0 = 3M0,
    N C = J,            N C0 = 0.

Therefore the exact object in BT768's killed 15-dimensional sector is the
centered spread/nonsquare polar frame. The 24- and 15-dimensional eigenspaces
are complementary orthogonal-orbit channels, and point-line incidence is the
map that transmits the square channel while annihilating the spread channel.
"""
from __future__ import annotations
import itertools,json,sys
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
Q=3;D4=4;PAIR=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))

def norm(v):
    v=tuple(int(x)%Q for x in v);i=next(i for i,x in enumerate(v) if x);z=pow(v[i],-1,Q);return tuple(z*x%Q for x in v)
def form(u,v):return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%Q
def wedge(a,b):return tuple((a[i]*b[j]-a[j]*b[i])%Q for i,j in PAIR)
def omega(b):return (b[1]+b[4])%Q
def qf(b):return (b[0]*b[5]-b[1]*b[4]+b[2]*b[3])%Q
def polar(a,b):return (qf(tuple((a[i]+b[i])%Q for i in range(6)))-qf(a)-qf(b))%Q

def geometry():
    P=sorted({norm(v) for v in itertools.product(range(Q),repeat=4) if any(v)});pi={p:i for i,p in enumerate(P)};L=set()
    for i,j in itertools.combinations(range(40),2):
        if form(P[i],P[j]):continue
        S=frozenset(pi[norm(tuple(a*P[i][k]+b*P[j][k] for k in range(4)))] for a,b in itertools.product(range(Q),repeat=2) if (a,b)!=(0,0))
        if len(S)==4:L.add(S)
    return P,sorted(L,key=lambda s:tuple(sorted(s)))
def line_coord(P,L):
    a,b=(P[i] for i in sorted(L)[:2]);p=wedge(a,b);assert omega(p)==qf(p)==0;return norm(p)
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A):return list(map(list,zip(*A)))
def rank(A):
    M=[[F(x) for x in r] for r in A];m=len(M);n=len(M[0]);r=0
    for c in range(n):
        p=next((i for i in range(r,m) if M[i][c]),None)
        if p is None:continue
        M[r],M[p]=M[p],M[r];z=M[r][c];M[r]=[x/z for x in M[r]]
        for i in range(m):
            if i!=r and M[i][c]:
                z=M[i][c];M[i]=[M[i][j]-z*M[r][j] for j in range(n)]
        r+=1
    return r
def fmm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def centered(M,a):return [[F(x)-a for x in r] for r in M]

def binary_min_octets(P):
    rows=[]
    for i in range(40):
        x=0
        for j in range(40):
            if i!=j and form(P[i],P[j])==0:x|=1<<j
        rows.append(x)
    span={0}
    for r in rows:span|={x^r for x in tuple(span)}
    mins={frozenset(i for i in range(40) if x>>i&1) for x in span if x.bit_count()==8}
    assert len(span)==2**16 and len(mins)==45
    return mins

def spreads_exact(L):
    inc={p:[i for i,l in enumerate(L) if p in l] for p in range(40)};out=[]
    def rec(ch,used):
        if len(used)==40:out.append(frozenset(ch));return
        p=next(i for i in range(40) if i not in used)
        for li in inc[p]:
            if not(set(L[li])&used):rec(ch+[li],used|set(L[li]))
    rec([],set());return set(out)

def main():
    P,L=geometry();assert len(P)==len(L)==40
    N=[[int(x in L[l]) for l in range(40)] for x in range(40)]
    Ap=[[int(i!=j and form(P[i],P[j])==0) for j in range(40)] for i in range(40)]
    Al=[[int(i!=j and bool(set(L[i])&set(L[j]))) for j in range(40)] for i in range(40)]
    PW=sorted({norm(v) for v in itertools.product(range(Q),repeat=6) if any(v) and omega(v)==0});iso=[v for v in PW if qf(v)==0];sq=[v for v in PW if qf(v)==1];ns=[v for v in PW if qf(v)==2]
    byiso={line_coord(P,l):i for i,l in enumerate(L)};assert set(byiso)==set(iso)
    iso_by_line=[None]*40
    for y,l in byiso.items():iso_by_line[l]=y
    D=[[int(polar(iso_by_line[l],c)==0) for c in sq] for l in range(40)]
    C=[[int(polar(iso_by_line[l],z)==0) for z in ns] for l in range(40)]
    ND=mm(N,D);NC=mm(N,C)

    # Recover octets directly from the multiplicity-4 entries of ND.
    assert set(x for r in ND for x in r)=={1,4}
    octets={frozenset(i for i in range(40) if ND[i][j]==4) for j in range(45)}
    intrinsic=binary_min_octets(P)

    # Recover spreads directly from nonsquare polar sections and compare to exact cover.
    polar_spreads=set();spread_valid=True
    for j,z in enumerate(ns):
        lis=frozenset(i for i in range(40) if C[i][j]);used=set()
        for li in lis:
            spread_valid &= not bool(used&set(L[li]));used|=set(L[li])
        spread_valid &= len(lis)==10 and len(used)==40;polar_spreads.add(lis)
    exact_spreads=spreads_exact(L)

    M=[[int(i in frozenset(i2 for i2 in range(40) if ND[i2][j]==4)) for j in range(45)] for i in range(40)]
    D0=centered(D,F(2,5));C0=centered(C,F(1,4));M0=centered(M,F(1,5));Dg=fmm(D0,tr(D0));Cg=fmm(C0,tr(C0));zero=[[F(0)]*40 for _ in range(40)]
    I=[[F(int(i==j)) for j in range(40)] for i in range(40)];center_sum=[[Dg[i][j]+Cg[i][j] for j in range(40)] for i in range(40)];want_sum=[[F(18)*(I[i][j]-F(1,40)) for j in range(40)] for i in range(40)]
    ND0=fmm([[F(x) for x in r] for r in N],D0);NC0=fmm([[F(x) for x in r] for r in N],C0)
    checks={
      'orthogonal_projective_partition_40_45_36':(len(iso),len(sq),len(ns))==(40,45,36),
      'all_isotropic_points_are_W33_line_plueckers':len(byiso)==40,
      'square_polar_heavy_sets_are_45_distinct_octets':len(octets)==45 and all(len(o)==8 for o in octets),
      'square_polar_octets_equal_intrinsic_binary_min_octets':octets==intrinsic,
      'nonsquare_polar_sections_are_spreads':spread_valid and len(polar_spreads)==36,
      'nonsquare_polar_spreads_equal_independent_exact_cover':polar_spreads==exact_spreads and len(exact_spreads)==36,
      'D0_rank_24':rank(D0)==24,
      'C0_rank_15':rank(C0)==15,
      'D0_C0_projectors_orthogonal':fmm(Dg,Cg)==zero,
      'centered_frames_resolve_all_39_nontrivial_dimensions':center_sum==want_sum,
      'ND_equals_J_plus_3M':ND==[[1+3*M[i][j] for j in range(45)] for i in range(40)],
      'NC_equals_J':NC==[[1]*36 for _ in range(40)],
      'ND0_equals_3M0':ND0==[[F(3)*x for x in r] for r in M0],
      'NC0_equals_zero':NC0==[[F(0)]*36 for _ in range(40)],
      'BT768_octet_Gram_recovered':mm(M,tr(M))==[[8*int(i==j)+1+2*Ap[i][j] for j in range(40)] for i in range(40)],
    }
    out={'schema':'w33.bt768-o5-24-15-closure.v1','status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
      'BT768Question':'Find the missing 15-sector object killed by the 1+24 intrinsic-octet incidence filter.',
      'answer':'The missing 15-sector is the centered 40-line x 36-spread incidence frame, equivalently the nonsquare O(5,3) polar-incidence frame C0. It has rank 15, C0C0^T=18 P15, and W33 point-line incidence annihilates it exactly: N C0=0.',
      'companion24':'The square polar frame D0 has rank 24 and D0D0^T=18 P24. Point-line incidence transmits it to the centered intrinsic-octet matrix by N D0=3 M0.',
      'resolution':'D0D0^T + C0C0^T = 18(I-J/40), giving an exact tight-frame resolution of all 39 nontrivial dimensions into 24+15.',
      'boundary':'Exact q=3 finite geometry. The orthogonal 40-set is the W33 LINE set. No equivariant identification with the distinct W33 POINT set is assumed.'}
    if '--write' in sys.argv:(ROOT/'data'/'w33_bt768_o5_24_15_closure.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
