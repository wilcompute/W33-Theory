#!/usr/bin/env python3
"""Pass 471: uniform cover-law witnesses over odd prime and prime-square fields.

The explicit q=3 Lean model of Pass 465 is generalized computationally to
q=3,5,7 and q=9=3^2.  The exact bulk graph has intersection array
{q^2-1,q(q-1),1;1,q,q^2-1} and shell sizes
1,q^2-1,(q-1)(q^2-1),q-1.
"""
from __future__ import annotations
import argparse,itertools,json
from collections import deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass471_uniform_cover_prime_power_witness.json'

class PrimeField:
    def __init__(self,p:int):self.p=p;self.q=p;self.name=f'F_{p}'
    def add(self,a,b):return (a+b)%self.p
    def neg(self,a):return (-a)%self.p
    def sub(self,a,b):return (a-b)%self.p
    def mul(self,a,b):return (a*b)%self.p
    def inv(self,a):return pow(a,-1,self.p)

class Fp2:
    def __init__(self,p:int,d:int):self.p=p;self.d=d;self.q=p*p;self.name=f'F_{p}^2[u^2=-{d}]'
    def ab(self,x):return x%self.p,x//self.p
    def enc(self,a,b):return (a%self.p)+self.p*(b%self.p)
    def add(self,x,y):a,b=self.ab(x);c,e=self.ab(y);return self.enc(a+c,b+e)
    def neg(self,x):a,b=self.ab(x);return self.enc(-a,-b)
    def sub(self,x,y):return self.add(x,self.neg(y))
    def mul(self,x,y):
        a,b=self.ab(x);c,e=self.ab(y)
        return self.enc(a*c-self.d*b*e,a*e+b*c)
    def inv(self,x):
        if x==0:raise ZeroDivisionError
        for y in range(1,self.q):
            if self.mul(x,y)==1:return y
        raise AssertionError

def vec_add(F,x,y):return tuple(F.add(a,b) for a,b in zip(x,y))
def vec_scale(F,a,x):return tuple(F.mul(a,b) for b in x)
def canonical(F,v):
    for a in v:
        if a!=0:return vec_scale(F,F.inv(a),v)
    raise ValueError('zero vector')
def symp(F,x,y):
    return F.add(F.sub(F.mul(x[0],y[2]),F.mul(x[2],y[0])),F.sub(F.mul(x[1],y[3]),F.mul(x[3],y[1])))
def projective_points(F):
    pts=set()
    for v in itertools.product(range(F.q),repeat=4):
        if any(v):pts.add(canonical(F,v))
    return sorted(pts)
def zact(F,t,x,p0):return vec_add(F,x,vec_scale(F,F.mul(t,symp(F,x,p0)),p0))

def distances(adj,start):
    d={start:0};Q=deque([start])
    while Q:
        u=Q.popleft()
        for v in adj[u]:
            if v not in d:d[v]=d[u]+1;Q.append(v)
    return d

def witness(F)->dict:
    q=F.q;pts=projective_points(F);p0=(0,0,0,1)
    rim=[x for x in pts if symp(F,p0,x)==0]
    bulk=[x for x in pts if symp(F,p0,x)!=0];bulk_set=set(bulk)
    full={x:set() for x in pts}
    for i,x in enumerate(pts):
        for y in pts[i+1:]:
            if symp(F,x,y)==0:full[x].add(y);full[y].add(x)
    badj={x:full[x]&bulk_set for x in bulk}
    expected_shell=[1,q*q-1,(q-1)*(q*q-1),q-1]
    expected_b=[q*q-1,q*(q-1),1,0]
    expected_c=[0,1,q,q*q-1]
    shell_ok=True;intersection_ok=True;connected_ok=True
    all_dist={}
    for x in bulk:
        d=distances(badj,x);all_dist[x]=d
        if len(d)!=len(bulk):connected_ok=False;continue
        shells=[sum(v==i for v in d.values()) for i in range(max(d.values())+1)]
        if shells!=expected_shell:shell_ok=False
        for y,dy in d.items():
            prev=sum(d[z]==dy-1 for z in badj[y]) if dy>0 else 0
            nxt=sum(d[z]==dy+1 for z in badj[y]) if dy<3 else 0
            if prev!=expected_c[dy] or nxt!=expected_b[dy]:intersection_ok=False
    fiber_ok=True;l1_ok=True;l4_ok=True;fiber_sizes=[]
    seen=set();fibers=[]
    for x in bulk:
        if x in seen:continue
        fib={zact(F,t,x,p0) for t in range(q)};fibers.append(fib);seen|=fib;fiber_sizes.append(len(fib))
        if len(fib)!=q or any((y in badj[x]) for y in fib if y!=x):fiber_ok=False
    for x in bulk:
        for t in range(1,q):
            y=zact(F,t,x,p0)
            common=full[x]&full[y]
            if len(common)!=q+1 or any(z in bulk_set for z in common):l1_ok=False
            if any(all_dist[x][z]!=2 for z in badj[y]):l4_ok=False
            if len(badj[y])!=q*q-1:l4_ok=False
    checks={
      'projective_point_count':len(pts)==(q+1)*(q*q+1),
      'rim_point_count':len(rim)==q*q+q+1,
      'bulk_point_count_q_cubed':len(bulk)==q**3,
      'bulk_regular_degree_q2_minus1':set(map(len,badj.values()))=={q*q-1},
      'fiber_partition_q2_fibers_of_q':len(fibers)==q*q and set(fiber_sizes)=={q},
      'fibers_are_independent':fiber_ok,
      'bulk_connected_diameter_three':connected_ok and max(max(d.values()) for d in all_dist.values())==3,
      'uniform_shell_profile':shell_ok,
      'uniform_intersection_array':intersection_ok,
      'L1_qplus1_rim_zero_bulk':l1_ok,
      'L4_fiber_mate_neighbors_in_shell2':l4_ok,
    }
    return {
      'field':F.name,'q':q,'projective_points':len(pts),'rim_points':len(rim),'bulk_points':len(bulk),
      'fibers':len(fibers),'fiber_size':q,'bulk_degree':q*q-1,
      'intersection_array':{'b':[q*q-1,q*(q-1),1],'c':[1,q,q*q-1]},
      'shell_sizes':expected_shell,'checks':checks,
    }

def build_payload()->dict:
    cases=[witness(PrimeField(3)),witness(PrimeField(5)),witness(PrimeField(7)),witness(Fp2(3,1))]
    checks={
      'all_witnesses_pass':all(all(c['checks'].values()) for c in cases),
      'includes_nonprime_q9':any(c['q']==9 for c in cases),
      'q3_recovers_pass465_array':next(c for c in cases if c['q']==3)['intersection_array']=={'b':[8,6,1],'c':[1,3,8]},
      'q9_shells_1_80_640_8':next(c for c in cases if c['q']==9)['shell_sizes']==[1,80,640,8],
      'symbolic_shell_sum_q3':all(sum(c['shell_sizes'])==c['q']**3 for c in cases),
    }
    return {
      'schema':'w33.pass471.uniform_cover_prime_power_witness.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'uniform_theorem':(
        'For the central-elation bulk chart of W(3,q), the q-point fibers are independent and the '
        'bulk collinearity graph is distance-regular with intersection array '
        '{q^2-1,q(q-1),1;1,q,q^2-1}.  Its distance shells are '
        '1,q^2-1,(q-1)(q^2-1),q-1 and sum to q^3.  Distinct fiber mates have exactly q+1 '
        'projective common neighbors, all in the rim, and every bulk neighbor of a nontrivial '
        'fiber mate lies in shell two from the original point.'),
      'exact_witnesses':cases,
      'boundary':(
        'The formulas are verified exhaustively over F3,F5,F7 and the nonprime field F9.  This closes '
        'the executable prime-power witness frontier; replacing the q=3 native_decide proof by one '
        'uniform finite-field cardinality proof in Lean remains a formal-library task.'),
      'checks':checks,
    }

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 471 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
