#!/usr/bin/env python3
"""Independent E6 cubic normal-form and synthetic clock/optical/pulse checks.
No claim that the 27-label gauge matches the W33 canonical artifact.
"""
import itertools,json,math,cmath
import numpy as np
from sympy import Matrix

def sign(p):return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
def index(g,r,c):return 9*g+3*r+c
def cubic():
 d={}
 for g in range(3):
  for p in itertools.permutations(range(3)):
   d[tuple(sorted(index(g,r,p[r]) for r in range(3)))]=sign(p)
 for i,j,k in itertools.product(range(3),repeat=3):
  d[tuple(sorted((index(0,i,j),index(1,j,k),index(2,k,i))))]=-1
 assert len(d)==45
 v=np.array([(n+1)**2 for n in range(81)],dtype=np.int64)
 A=np.zeros((81,81),dtype=np.int64);count=0
 for triple,s in d.items():
  for u,x,o in itertools.permutations(triple):
   for a,b in itertools.product(range(3),repeat=2):
    c=3-a-b
    if c in range(3) and len({a,b,c})==3:
     A[3*o+c,3*x+b]+=s*sign((a,b,c))*v[3*u+a];count+=1
 assert count==1620 and np.array_equal(A,-A.T) and not np.any(A@v)
 null=Matrix(A.tolist()).nullspace()
 assert len(null)==3 and all(not any(Matrix(A.tolist())*q) for q in null)
 return {'signed_triads':45,'ordered_bracket_records':count,'quadratic_background':'v_n=(n+1)^2','exact_kernel_dimension':len(null),'exact_rank':81-len(null),'scope':'Independent 3x3 determinant-plus-trace E6 normal form; gauge matching and Fourier-54 projection remain open.'}

def other():
 h={0:80,1:27,3:2,4:27,5:27,6:2,7:27,8:27,9:2,11:27}
 traces=[round(sum(v*cmath.exp(2j*math.pi*k*t/12) for k,v in h.items()).real) for t in range(12)]
 assert traces==[248,51,105,132,5,51,24,51,5,132,105,51]
 I=np.eye(36,dtype=complex);P=I.copy();P[0,0]=1j
 overlap=lambda M:float(abs(np.trace(M))**2/(36*np.vdot(M,M).real))
 assert abs(overlap(.8*I)-1)<1e-12 and abs(overlap(P)-1226/1296)<1e-12
 return {'c12_traces':traces,'phi6_multiplicity':0,'fi_u4_dimensions':[86,81,81],'optical_common_loss_overlap':overlap(.8*I),'optical_one_mode_phase_overlap':overlap(P),'pulse_survival_at_saturated_bounds':.9**8*.98**12,'uniform_primitive_loss_cap_for_90pct':1-.9**(1/20),'laboratory_data':False}

def run():return {'schema':'w33.local.e6_normal_form.v1','e6':cubic(),'other':other(),'open':['Actual Fourier-54 target alignment','Independent replay of W33 E8 structure-constants JSON','Laboratory hardware calibration']}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
