from __future__ import annotations
import json,time
from pathlib import Path
from fractions import Fraction
from collections import deque

class Eis:
    """Exact Q(omega), omega^2+omega+1=0, stored as a+b*omega."""
    __slots__=('a','b')
    def __init__(self,a=0,b=0): self.a=Fraction(a); self.b=Fraction(b)
    def __add__(self,o): o=coerce(o); return Eis(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return Eis(-self.a,-self.b)
    def __sub__(self,o): return self+(-coerce(o))
    def __rsub__(self,o): return coerce(o)-self
    def __mul__(self,o):
        o=coerce(o)
        return Eis(self.a*o.a-self.b*o.b, self.a*o.b+self.b*o.a-self.b*o.b)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=coerce(o); norm=o.a*o.a-o.a*o.b+o.b*o.b
        return self*Eis((o.a-o.b)/norm,(-o.b)/norm)
    def __eq__(self,o): o=coerce(o); return self.a==o.a and self.b==o.b
    def __hash__(self): return hash((self.a,self.b))
    def iszero(self): return self.a==0 and self.b==0
    def text(self):
        if self.b==0:return str(self.a)
        if self.a==0:return 'omega' if self.b==1 else ('-omega' if self.b==-1 else f'{self.b}*omega')
        sign='+' if self.b>0 else '-'; bb=abs(self.b)
        bt='omega' if bb==1 else f'{bb}*omega'
        return f'{self.a}{sign}{bt}'

def coerce(x): return x if isinstance(x,Eis) else Eis(x)
OMEGA=Eis(0,1); ZERO=Eis(); ONE=Eis(1)

def ident(n): return [[ONE if i==j else ZERO for j in range(n)] for i in range(n)]
def mm(A,B): return [[sum((A[i][k]*B[k][j] for k in range(len(B))),ZERO) for j in range(len(B[0]))] for i in range(len(A))]
def sub(A,B): return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def mpow(A,n):
    out=ident(len(A));base=A
    while n:
        if n&1:out=mm(out,base)
        base=mm(base,base);n//=2
    return out

def rank(A):
    M=[row[:] for row in A];r=0;cols=len(M[0])
    for c in range(cols):
        p=next((i for i in range(r,len(M)) if not M[i][c].iszero()),None)
        if p is None:continue
        M[r],M[p]=M[p],M[r]; inv=ONE/M[r][c];M[r]=[x*inv for x in M[r]]
        for i in range(len(M)):
            if i!=r and not M[i][c].iszero():
                f=M[i][c];M[i]=[x-f*y for x,y in zip(M[i],M[r])]
        r+=1
    return r

def reflection(direction):
    n=len(direction);R=ident(n);den=sum(x*x for x in direction)
    for i in range(n):
        for j in range(n):R[i][j]=R[i][j]+(OMEGA-ONE)*Eis(direction[i]*direction[j])/den
    return R

def block3(A): return [row[:3] for row in A[:3]]
def embed3(A):
    R=ident(4)
    for i in range(3):
        for j in range(3):R[i][j]=A[i][j]
    return R

def mat_text(A): return [[x.text() for x in row] for row in A]

def mod7(x):
    a=(x.a.numerator*pow(x.a.denominator,-1,7))%7
    b=(x.b.numerator*pow(x.b.denominator,-1,7))%7
    return (a+2*b)%7 # omega -> 2, a primitive cube root modulo 7

def tupmod(A): return tuple(mod7(x) for row in A for x in row)
def mt(A,B,n): return tuple(sum(A[n*i+k]*B[n*k+j] for k in range(n))%7 for i in range(n) for j in range(n))
def group_mod7(gens,n):
    I=tuple(1 if i==j else 0 for i in range(n) for j in range(n));seen={I};front=deque([I])
    while front:
        x=front.popleft()
        for g in gens:
            y=mt(g,x,n)
            if y not in seen:seen.add(y);front.append(y)
    return seen

def main():
    directions=[(0,0,-1,0),(1,1,1,0),(0,1,0,0),(1,-1,0,-1)]
    R=[reflection(v) for v in directions]
    r=[block3(x) for x in R[:3]]
    I4=ident(4);I3=ident(3)
    adjacent=[(0,1),(1,2),(2,3)]; nonadjacent=[(0,2),(0,3),(1,3)]

    exact_relations={
      'all_G32_generators_have_order3':all(mpow(x,3)==I4 and x!=I4 for x in R),
      'all_G25_generators_have_order3':all(mpow(x,3)==I3 and x!=I3 for x in r),
      'G32_adjacent_braid_relations':all(mm(mm(R[i],R[j]),R[i])==mm(mm(R[j],R[i]),R[j]) for i,j in adjacent),
      'G32_nonadjacent_generators_commute':all(mm(R[i],R[j])==mm(R[j],R[i]) for i,j in nonadjacent),
      'G25_chain_braid_relations':all(mm(mm(r[i],r[j]),r[i])==mm(mm(r[j],r[i]),r[j]) for i,j in [(0,1),(1,2)]),
      'G25_end_generators_commute':mm(r[0],r[2])==mm(r[2],r[0]),
      'each_G32_generator_is_rank1_reflection':all(rank(sub(x,I4))==1 for x in R),
      'each_G25_generator_is_rank1_reflection':all(rank(sub(x,I3))==1 for x in r),
      'first_three_G32_generators_are_block_G25':all(embed3(r[i])==R[i] for i in range(3)),
    }

    G25=group_mod7([tupmod(x) for x in r],3)
    G32=group_mod7([tupmod(x) for x in R],4)
    # Embed the enumerated 3x3 residue matrices block-diagonally into dimension four.
    emb25=set()
    for A in G25:
        B=[0]*16
        for i in range(4):B[4*i+i]=1
        for i in range(3):
            for j in range(3):B[4*i+j]=A[3*i+j]
        emb25.add(tuple(B))
    fix_e4={A for A in G32 if tuple(A[4*i+3] for i in range(4))==(0,0,0,1)}

    J=[[ONE if i==j else ZERO for j in range(3)] for i in range(4)]
    intertwining=all(mm(R[i],J)==mm(J,r[i]) for i in range(3))
    checks={
      **exact_relations,
      'G25_mod7_order_is_648':len(G25)==648,
      'G32_mod7_order_is_155520':len(G32)==155520,
      'degree_products_match_orders':6*9*12==648 and 12*18*24*30==155520,
      'pointwise_e4_stabilizer_has_order648':len(fix_e4)==648,
      'pointwise_e4_stabilizer_equals_embedded_G25':fix_e4==emb25,
      'explicit_inclusion_intertwines_generators':intertwining,
    }
    assert all(checks.values()),checks

    return {
      'schema':'w33.pass1068.chevie_g25_g32_matrices.v1','status':'PASS',
      'headline':'The CHEVIE G25 and G32 models admit an explicit generator-level parabolic inclusion. In the standard CHEVIE basis, the first three G32 reflections fix e4 pointwise and their upper-left 3x3 blocks are exactly the G25 generators; the inclusion matrix is the coordinate embedding J: C^3 -> C^4.',
      'field':'Q(omega), omega^2+omega+1=0',
      'reflection_formula':'R_v = I + (omega-1) v v*/<v,v>',
      'G25':{'degrees':[6,9,12],'order':648,'generators_3x3':[mat_text(x) for x in r]},
      'G32':{'degrees':[12,18,24,30],'order':155520,'generators_4x4':[mat_text(x) for x in R]},
      'inclusion_matrix_J_4x3':mat_text(J),
      'conjugator':'Identity in the standard CHEVIE basis: R_i J = J r_i for i=1,2,3. Equivalently diag(r_i,1)=R_i.',
      'parabolic_statement':'<R1,R2,R3> = Stab_G32(e4) pointwise and is the embedded Shephard-Todd G25.',
      'finite_field_certificate':{'prime':7,'omega_residue':2,'G25_order':len(G25),'G32_order':len(G32),'e4_pointwise_stabilizer_order':len(fix_e4)},
      'check_count':len(checks),'checks':checks,
      'scope':'Exact Q(omega) relation checks plus faithful good-prime reduction modulo 7 for finite enumeration. The matrices are the CHEVIE standard reflection model; no numerical fitting is involved.'
    }

if __name__=='__main__':
    started=time.time();result=main()
    output=Path(__file__).resolve().parents[1]/'data'/'w33_pass1068_chevie_g25_g32_matrices.json'
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'check_count':result['check_count'],'seconds':round(time.time()-started,3),'output':str(output)},indent=2))
