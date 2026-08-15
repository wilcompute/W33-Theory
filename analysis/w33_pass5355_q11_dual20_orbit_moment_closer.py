#!/usr/bin/env python3
"""Pass5355: close the q=11 footprint distance from the Pass5354b dual20 seed.

Avoid constructing the full degree-7381 PSp4(11) permutation group.  A carrier
is an unordered symplectic decomposition V=H orthogonal-sum H^perp.  Fixing a
base carrier, its stabilizer is generated explicitly by SL2(11) on each summand
and the summand swap.  Its seven carrier suborbits have sizes
  1,660,1320,1320,1320,1320,1440.
They are separated by trace(S_A S_B)^2, where S_A is +1 on H and -1 on H^perp.

For a transitive orbit of dual checks of weight w, an unordered pair orbital of
valency v containing c seed pairs has r/lambda = w*v/(2*c).  The Pass5354b seed
has pair counts giving ratios 660,440,1320,2640,120,880.  Hence the maximum pair
codegree satisfies r/lambda_max=120.  Even dual intersections then give primal
weight >=121; point footprint rows have weight121.  Therefore q11 is exactly
[7381,671,121]_2.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5304_q11_dual20_density_wall import carriers,null2
from analysis.w33_pass5293_allodd_rank_reduction_q11 import line_bases,norm,sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5355_Q11_DUAL20_ORBIT_MOMENT.json'
Q=11

def matmul(A,B):return [[sum(A[i][k]*B[k][j] for k in range(4))%Q for j in range(4)] for i in range(4)]
def matvec(A,x):return tuple(sum(A[i][k]*x[k] for k in range(4))%Q for i in range(4))
def transpose(A):return [list(x) for x in zip(*A)]
def invmat(A):
    n=4;M=[[(A[i][j]%Q) for j in range(n)]+[1 if i==j else 0 for j in range(n)] for i in range(n)]
    r=0
    for c in range(n):
        k=next(i for i in range(r,n) if M[i][c]);M[r],M[k]=M[k],M[r]
        iv=pow(M[r][c],-1,Q);M[r]=[(x*iv)%Q for x in M[r]]
        for i in range(n):
            if i!=r and M[i][c]:
                f=M[i][c];M[i]=[(M[i][j]-f*M[r][j])%Q for j in range(2*n)]
        r+=1
    return [row[n:] for row in M]
def trace(A):return sum(A[i][i] for i in range(4))%Q

def linepts(u,v,pi):
    S={pi[norm(v,Q)]}
    for a in range(Q):S.add(pi[norm(tuple((u[k]+a*v[k])%Q for k in range(4)),Q)])
    return tuple(sorted(S))

def carrier_bases(P,C):
    pi={p:i for i,p in enumerate(P)};have={}
    for u,v in line_bases(Q):
        if sp(u,v,Q)==0:continue
        H=linepts(u,v,pi)
        a,b=null2([(u[2],u[3],-u[0],-u[1]),(v[2],v[3],-v[0],-v[1])],Q)
        Hp=linepts(a,b,pi);key=tuple(sorted(set(H)|set(Hp)))
        if key not in have:have[key]=(u,v)
    assert len(have)==len(C);return have

def involution(basis):
    # Build symplectic projection P_H using a normalized symplectic basis of H.
    u,v=basis;s=sp(u,v,Q);v=tuple(pow(s,-1,Q)*x%Q for x in v)
    a,b=null2([(u[2],u[3],-u[0],-u[1]),(v[2],v[3],-v[0],-v[1])],Q)
    # Projection formula in the symplectic basis (u,v,a,b): first two coords.
    s2=sp(a,b,Q);b=tuple(pow(s2,-1,Q)*x%Q for x in b)
    E=[[u[i],v[i],a[i],b[i]] for i in range(4)];Ei=invmat(E)
    D=[[1,0,0,0],[0,1,0,0],[0,0,Q-1,0],[0,0,0,Q-1]]
    return matmul(matmul(E,D),Ei),E

def main():
    seedj=json.loads((ROOT/'data/PART_W33_PASS5354B_Q11_MOD4_TWOFACTOR_CAYLEY_SEARCH.json').read_text())
    assert seedj['status']=='THEOREM_Q11_MOD4_CAYLEY_DUAL20_EQUALITY_WITNESS'
    seed=seedj['selected_carriers'];assert len(seed)==20
    P,C=carriers(Q);assert len(P)==1464 and len(C)==7381
    pi={p:i for i,p in enumerate(P)};bk={c:i for i,c in enumerate(C)}
    bits=[]
    for B in C:
        z=0
        for p in B:z|=1<<p
        bits.append(z)
    z=0
    for j in seed:z^=bits[j]
    assert z==0
    bases=carrier_bases(P,C);Sm=[]
    for c in C:Sm.append(involution(bases[c])[0])
    S0,E=involution(bases[C[0]])
    Ei=invmat(E);I2=[[1,0],[0,1]];U=[[1,1],[0,1]];L=[[1,0],[1,1]]
    def block(A,B):return [[(A if i<2 and j<2 else B if i>=2 and j>=2 else [[0,0],[0,0]])[i%2][j%2] if (i<2)==(j<2) else 0 for j in range(4)] for i in range(4)]
    Z2=[[0,0],[0,0]];SW=[[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]]
    Bad=[block(U,I2),block(L,I2),block(I2,U),block(I2,L),SW]
    Mgens=[matmul(matmul(E,B),Ei) for B in Bad]
    perms=[]
    for M in Mgens:
        pp=[pi[norm(matvec(M,x),Q)] for x in P]
        perm=[bk[tuple(sorted(pp[p] for p in B))] for B in C]
        assert perm[0]==0;perms.append(perm)
    rem=set(range(len(C)));orbs=[]
    while rem:
        s=next(iter(rem));O={s};todo=[s];rem.remove(s)
        while todo:
            u=todo.pop()
            for g in perms:
                v=g[u]
                if v in rem:rem.remove(v);O.add(v);todo.append(v)
        orbs.append(O)
    assert sorted(map(len,orbs))==[1,660,1320,1320,1320,1320,1440]
    invval={}
    for O in orbs:
        vals={(trace(matmul(S0,Sm[i]))**2)%Q for i in O};assert len(vals)==1
        t=next(iter(vals))
        if 0 in O:assert t==5 and len(O)==1
        else:invval[t]=len(O)
    assert invval=={0:660,1:1320,3:1320,4:1320,5:1440,9:1320}
    pc=Counter()
    for a,b in itertools.combinations(seed,2):
        t=(trace(matmul(Sm[a],Sm[b]))**2)%Q;pc[t]+=1
    assert pc==Counter({5:120,1:30,9:15,3:10,0:10,4:5})
    ratios={t:Fraction(20*invval[t],2*c) for t,c in pc.items()}
    assert min(ratios.values())==120
    out={'pass':5355,'status':'THEOREM_Q11_FOOTPRINT_CODE_7381_671_121',
      'seed_source':'Pass5354b C10|(C5+C5) dual20 equality witness',
      'carrier_stabilizer_suborbit_sizes':sorted(map(len,orbs)),
      'pair_orbit_invariant':'trace(S_A S_B)^2 in F_11; S_A acts +1/-1 on the two polar symplectic summands.',
      'nontrivial_orbital_valencies':{str(k):v for k,v in sorted(invval.items())},
      'seed_pair_counts':{str(k):v for k,v in sorted(pc.items())},
      'r_over_lambda':{str(k):(str(v.numerator) if v.denominator==1 else f'{v.numerator}/{v.denominator}') for k,v in sorted(ratios.items())},
      'minimum_r_over_lambda':'120',
      'moment_bound':'Every dual20 intersection with a primal support is even; first/second moment comparison gives w_primal >= 1+120=121.',
      'point_footprint_weight':121,'rank_F2':671,'footprint_code':'[7381,671,121]_2',
      'conclusion':'q11 footprint distance is exactly121. Exact d=q^2 is now closed for q=3,5,7,9,11.',
      'boundary':'This proves the q11 row-footprint code distance. It does not by itself prove an all-odd distance-q^2 theorem beyond the verified q<=11 anchors.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
