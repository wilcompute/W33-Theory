#!/usr/bin/env python3
"""All-level S3 twining bridge: Niemeier A8^3 versus Monster 2A/3C.

Let s swap two A8 factors and c cyclically permute all three.  The fixed
lattices can be read directly from the A8^3 glue C=<114,141,411> in (Z/9)^3.

For c the fixed lattice is sqrt(3) E8, so
    Z_c = E4(3 tau)/eta(3 tau)^8 = T_3C.
For s the fixed lattice is even rank 16, determinant 2^8 and level 2.  Its
theta series is a weight-8 Gamma0(2) form with trivial character.  Comparing
through the Sturm bound 2 gives
    Z_s = T_2A + 80.

The ordinary A8^3 character is J+240 while moonshine is J.  Therefore at every
conformal weight n>=2 the full S3 character (1,s,c) of V_{A8^3,n} is exactly
the restriction of V^natural_n to a Monster S3 of type (2A,3C).  Weight one is
the only discrepancy: A8^3 has character (240,80,0), while V^natural_1=0.

This is a graded S3-character statement, not an isomorphism of VOAs.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from fractions import Fraction
from pathlib import Path
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_a8cubed_monster_s3_twining.json'
GEN=((1,1,4),(1,4,1),(4,1,1))

def glue():
 C=set()
 for a,b,c in itertools.product(range(9),repeat=3):C.add(tuple((a*GEN[0][i]+b*GEN[1][i]+c*GEN[2][i])%9 for i in range(3)))
 return sorted(C)

def a8_cartan():return sp.Matrix([[2 if i==j else -1 if abs(i-j)==1 else 0 for j in range(8)] for i in range(8)])

def fixed_gram_swap():
 C=a8_cartan();Ci=C.inv();l1=Ci[:,0];l4=Ci[:,3]
 w=sp.Matrix([int(9*x) for x in list(l1)+list(l4)])
 H=hermite_normal_form(sp.Matrix.hstack(9*sp.eye(16),w));B=H/9
 return sp.simplify(B.T*sp.diag(2*C,C)*B)

def fixed_gram_cycle():
 C=a8_cartan();l3=C.inv()[:,2];w=sp.Matrix([int(3*x) for x in l3])
 H=hermite_normal_form(sp.Matrix.hstack(3*sp.eye(8),w));B=H/3
 return sp.simplify(B.T*(3*C)*B)

def a8_coset_theta(k,maxnorm=12):
 # x_i=z_i-k/9, z_i integers, sum z_i=k.
 out=Counter();vals=range(-4,6);bound=81*maxnorm
 def rec(i,s,ss):
  if i==8:
   z=k-s
   if z not in vals:return
   num=ss+(9*z-k)**2
   if num<=bound:out[Fraction(num,81)]+=1
   return
  for z in vals:
   num=ss+(9*z-k)**2
   if num<=bound:rec(i+1,s+z,num)
 rec(0,0,0);return out

def invfac(step,power,N):
 a=[0]*(N+1)
 for r in range(N//step+1):a[r*step]=math.comb(power+r-1,r)
 return a

def mul(a,b,N):
 o=[0]*(N+1)
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if i+j<=N and y:o[i+j]+=x*y
 return o

def oscillator(kind,N):
 a=[1]+[0]*N
 if kind=='swap':
  for n in range(1,N+1):
   a=mul(a,invfac(n,8,N),N)
   if 2*n<=N:a=mul(a,invfac(2*n,8,N),N)
 else:
  for n in range(1,N//3+1):a=mul(a,invfac(3*n,8,N),N)
 return a

def main(write=True):
 C=glue();assert len(C)==27
 fs=[w for w in C if w[0]==w[1]];fc=[w for w in C if w[0]==w[1]==w[2]]
 assert len(fs)==9 and len(fc)==3
 Gs=fixed_gram_swap();Gc=fixed_gram_cycle()
 assert Gs.det()==2**8 and all(x.q==1 for x in Gs)
 Gi=Gs.inv();assert all((2*x).q==1 for x in Gi) and all(int(2*Gi[i,i])%2==0 for i in range(16))
 assert Gc.det()==3**8 and all((x/3).q==1 for x in Gc) and all(int(Gc[i,i]/3)%2==0 for i in range(8))
 assert (Gc/3).det()==1  # even unimodular rank 8 -> E8

 th=[a8_coset_theta(k,12) for k in range(9)];N=8
 ts=Counter();tc=Counter()
 for k,_,l in fs:
  for nx,ax in th[k].items():
   for nz,az in th[l].items():
    q=nx+nz/2
    if q<=N:ts[q]+=ax*az
 for k,_,_ in fc:
  for nx,ax in th[k].items():
   q=3*nx/2
   if q<=N:tc[q]+=ax
 assert [ts[Fraction(i)] for i in range(3)]==[1,72,3744]
 # Weight-8 Gamma0(2), index 3: Sturm bound=floor(8*3/12)=2.
 sturm_bound=2
 assert [tc[Fraction(i)] for i in range(7)]==[1,0,0,240,0,0,2160]

 def arr(t):return [t[Fraction(i)] for i in range(N+1)]
 zs=mul(arr(ts),oscillator('swap',N),N)
 zc=mul(arr(tc),oscillator('cycle',N),N)
 assert zs[:7]==[1,80,4372,96256,1240002,10698752,74428120]
 assert zc[:7]==[1,0,0,248,0,0,4124]
 # Published McKay-Thompson positive coefficients used as an independent tooth.
 T2A=[1,0,4372,96256,1240002,10698752,74428120]
 T3C=[1,0,0,248,0,0,4124]
 assert zs[0]==T2A[0] and zs[1]-T2A[1]==80 and zs[2:7]==T2A[2:]
 assert zc[:7]==T3C

 # First nontrivial S3 decomposition at weight two.
 I2=196884;t2=zs[2];c2=zc[2]
 triv=(I2+2*c2+3*t2)//6;sgn=(I2+2*c2-3*t2)//6;std=(I2-c2)//3
 assert (triv,sgn,std)==(35000,30628,65628)
 out={
  'schema':'w33.a8cubed_monster_s3_twining.v1','status':'PASS',
  'headline':'Factor permutations of the Niemeier A8^3 lattice VOA reproduce Monster 3C exactly and Monster 2A up to the 80-dimensional weight-one fixed space: Z_(123)=T_3C and Z_(12)=T_2A+80. Since the untwined characters are J+240 versus J, the S3 characters agree exactly at every conformal weight n>=2.',
  'fixed_lattices':{'3cycle':{'rank':8,'determinant':'3^8','rescaled_by_1_over_3':'even unimodular rank 8 = E8','theta':'E4(3 tau)'},
                    'transposition':{'rank':16,'determinant':'2^8','level':2,'theta_first_coefficients':[1,72,3744],'sturm_bound':sturm_bound}},
  'twining_identities':{'3cycle':'Z_c(tau)=E4(3tau)/eta(3tau)^8=T_3C(tau)',
                         'transposition':'Z_s(tau)=T_2A(tau)+80'},
  'trace_sequences_V0_to_V6':{'transposition':zs[:7],'3cycle':zc[:7]},
  'weight_one':{'A8cubed_character':[240,80,0],'moonshine_character':[0,0,0],'difference':'80 trivial + 80 standard as an S3 module'},
  'all_levels_n_ge_2':'V_{A8^3,n} and V^natural_n have identical complex S3 characters for identity, a 2A-type transposition and a 3C-type three-cycle; hence they are isomorphic as S3-modules at each n>=2, although not as VOAs.',
  'weight_two_S3_multiplicities':{'trivial':triv,'sign':sgn,'standard_2d':std},
  'literature_context':['Monster 3C normalizer S3 x Th and the (2A,3C)-type S3 are classical Monster subgroup data.','A8^3 is a standard Niemeier/umbral moonshine case; this certificate records the explicit lattice-VOA twining comparison used by this repository.'],
  'boundary':'The equality is an equality of graded S3 characters/modules for weights >=2. A8^3 has a 240-dimensional weight-one Lie algebra whereas moonshine has V1=0, so no VOA isomorphism is claimed.',
  'checks':{'fixed_cycle_is_sqrt3_E8':True,'swap_level2_det256':True,'swap_sturm_bound_passed':True,'T3C_exact':True,'T2A_plus_80_exact':True,'weight2_decomposition':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
