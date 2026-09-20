#!/usr/bin/env python3
"""Exact error-propagation kernels on the packet72 causal graph.

Parent:
  data/w33_packet72_cayley_causal_cone.json

The seven primitive control errors are treated symmetrically:
  +/-rho, +/-a, R, R^-1, S.

Two models are computed.

NON-LAZY CONDITIONAL WALK
Conditioned on an error occurring at every step, choose one of the seven
primitive errors uniformly.  Exact distributions are propagated on the
72-element group.

LAZY PER-TICK MODEL
At each scheduled tick:
  identity with probability 1-epsilon,
  each primitive error with probability epsilon/7.
For n<=5 the exact probability mass in every causal shell is frozen as a
polynomial in epsilon.

No hardware epsilon is invented.  A measured primitive-error probability can
be substituted directly.

Key facts:
* conditional support sizes after 0..5 errors: 1,7,24,49,67,72;
* after five primitive error events every runtime address is reachable;
* support can never outrun the deterministic causal balls
  1,8,27,52,68,72;
* for n scheduled ticks, probability of at least one primitive error is
  1-(1-epsilon)^n, while the exact shell kernel resolves where that error can
  propagate.
"""
from __future__ import annotations
import argparse,json
from collections import defaultdict,deque
from fractions import Fraction as F
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_packet72_error_spread.json'
I=(1,0,0,1);R=(0,2,1,0);S=(1,0,0,2)

def mm(A,B):return tuple(sum(A[2*i+k]*B[2*k+j] for k in range(2))%3 for i in range(2) for j in range(2))
def mv(A,v):return ((A[0]*v[0]+A[1]*v[1])%3,(A[2]*v[0]+A[3]*v[1])%3)
def mpow(A,n):
    o=I
    for _ in range(n):o=mm(o,A)
    return o
D8=[]
for s in range(2):
    for p in range(4):
        L=mm(mpow(S,s),mpow(R,p))
        if L not in D8:D8.append(L)
T=[(x,y) for x in range(3) for y in range(3)]
G=[(t,L) for t in T for L in D8]
def mul(g,h):
    t,L=g;u,M=h;Lu=mv(L,u)
    return (((t[0]+Lu[0])%3,(t[1]+Lu[1])%3),mm(L,M))
E=((0,0),I)
GENS=[((1,0),I),((2,0),I),((0,1),I),((0,2),I),((0,0),R),((0,0),mpow(R,3)),((0,0),S)]

def graph_distances():
    d={E:0};q=deque([E])
    while q:
        g=q.popleft()
        for s in GENS:
            h=mul(g,s)
            if h not in d:d[h]=d[g]+1;q.append(h)
    return d

def fstr(x):
    x=F(x)
    return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'

def main(write=True,epsilon=None):
    causal=json.loads((ROOT/'data/w33_packet72_cayley_causal_cone.json').read_text())
    assert causal['status']=='PASS_FINITE_CONTROL_CAUSAL_CONE'
    dist=graph_distances();assert len(dist)==72
    assert [sum(v<=r for v in dist.values()) for r in range(6)]==[1,8,27,52,68,72]

    # Conditional non-lazy walk.
    p={E:F(1)}
    conditional=[]
    for n in range(6):
        if n:
            q=defaultdict(F)
            for g,pg in p.items():
                for s in GENS:q[mul(g,s)]+=pg/F(7)
            p=dict(q)
        sh=defaultdict(F)
        for g,pg in p.items():sh[dist[g]]+=pg
        collision=sum(v*v for v in p.values())
        tv=F(1,2)*sum(abs(p.get(g,F(0))-F(1,72)) for g in G)
        conditional.append({
          'errors':n,'support_size':len(p),'return_probability':fstr(p.get(E,F(0))),
          'shell_probabilities':{str(r):fstr(sh[r]) for r in sorted(sh)},
          'collision_probability':fstr(collision),
          'total_variation_from_uniform':fstr(tv)})
    assert [x['support_size'] for x in conditional]==[1,7,24,49,67,72]

    # Lazy per-tick shell polynomials.
    eps=sp.symbols('epsilon')
    p={E:sp.Integer(1)}
    lazy=[]
    for n in range(6):
        if n:
            q=defaultdict(lambda:sp.Integer(0))
            for g,pg in p.items():
                q[g]+=pg*(1-eps)
                for s in GENS:q[mul(g,s)]+=pg*eps/sp.Integer(7)
            p=dict(q)
        sh=defaultdict(lambda:sp.Integer(0))
        for g,pg in p.items():sh[dist[g]]+=pg
        lazy.append({
          'ticks':n,
          'shell_probability_polynomials':{
            str(r):str(sp.factor(sp.expand(sh[r]))) for r in sorted(sh)},
          'probability_any_error':str(sp.expand(1-(1-eps)**n))})

    out={
      'schema':'w33.packet72_error_spread.v1',
      'status':'PASS_EXACT_ERROR_PROPAGATION_KERNEL',
      'headline':'The packet72 causal graph now carries exact stochastic error kernels. Conditioned on one uniformly random primitive error per step, support sizes are 1,7,24,49,67,72 and all runtime addresses become reachable after five errors. For a measured per-tick primitive-error probability epsilon, exact shell probabilities through five ticks are frozen as polynomials.',
      'primitive_error_alphabet':['+rho','-rho','+a','-a','R','R^-1','S'],
      'conditional_uniform_error_walk':conditional,
      'lazy_per_tick_model':{
        'definition':'identity with probability 1-epsilon; each of seven primitive errors with probability epsilon/7',
        'shell_kernels':lazy},
      'containment':{
        'deterministic_causal_ball_sizes':[1,8,27,52,68,72],
        'conditional_support_sizes':[1,7,24,49,67,72],
        'all72_reachable_after_five_error_events':True},
      'usage':'Insert an experimentally measured epsilon into the frozen shell polynomials to obtain the exact probability that a primitive control error has propagated to graph distance r after n<=5 scheduled ticks.',
      'boundary':'This is a classical stochastic control-error model on the finite runtime group. It does not include coherent quantum amplitudes, correlated physical noise, unequal primitive error rates, or a hardware-derived epsilon. Those can be added by replacing the seven equal transition weights.',
      'parent':'data/w33_packet72_cayley_causal_cone.json',
      'checks':{'group72':True,'support_1_7_24_49_67_72':True,'causal_containment':True,
                'exact_lazy_polynomials_through5':True,'no_invented_error_rate':True}}
    if epsilon is not None:
        val=F(epsilon)
        out['evaluated_epsilon']=fstr(val)
        # exact direct evaluation of lazy formulas
        ev=[]
        for rec in lazy:
            ev.append({'ticks':rec['ticks'],'shell_probabilities':{
              r:str(sp.Rational(sp.sympify(expr).subs(eps,sp.Rational(val.numerator,val.denominator))))
              for r,expr in rec['shell_probability_polynomials'].items()}})
        out['evaluated_shells']=ev
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--epsilon',default=None,help='optional rational value, e.g. 1/1000')
    a=ap.parse_args()
    main(True,a.epsilon)
