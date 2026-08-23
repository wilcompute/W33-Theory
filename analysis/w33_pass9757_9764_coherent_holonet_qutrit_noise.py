#!/usr/bin/env python3
"""Pass9757-9764: coherent W33 x qutrit Holonet stress model.

This upgrades the intensity-only transfer envelope to complex amplitudes on
40 W33 ports x 3 internal qutrit/OAM-time-bin modes.  W33 coupling is unitary
exp(-i theta A/12); every stage adds bounded random port phase, loss, and a
random small 3x3 internal unitary.  Finite detector shots and a noisy dark
monitor are included.  A phase-tag model tests the new A2/Golay orientation bit.

This is a deterministic seeded stress simulation, not a physical Hamiltonian
fit to measured hardware.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9757_9764_COHERENT_HOLONET_QUTRIT_NOISE.json'
P=3

def canon(v):
 v=tuple(int(x)%P for x in v)
 for x in v:
  if x:
   z=pow(x,-1,P);return tuple(z*y%P for y in v)
 raise ValueError

def geometry():
 pts=sorted({canon(v) for v in itertools.product(range(P),repeat=4) if any(v)})
 J=np.block([[np.zeros((2,2),dtype=int),np.eye(2,dtype=int)],[-np.eye(2,dtype=int),np.zeros((2,2),dtype=int)]])%P
 A=np.zeros((40,40),dtype=float)
 for i,u in enumerate(pts):
  for j,v in enumerate(pts):
   if i!=j and int(np.array(u)@J@np.array(v))%P==0:A[i,j]=1.0
 assert set(A.sum(axis=1))=={12.0}
 e0=np.array([1,0,0,0]);e1=np.array([0,1,0,0])
 line=sorted({canon((a*e0+b*e1)%P) for a,b in itertools.product(range(P),repeat=2) if a or b})
 idx=[pts.index(x) for x in line];assert len(idx)==4
 return A,idx

def profile(seed,theta,stages,phase_bound,loss_low,shots,rho,ntrials):
 A,line=geometry();rng=np.random.default_rng(seed);Uport=expm(-1j*theta*A/12.0)
 out={}
 for carrier in ('E8','E6','A2'):
  vals=[]
  for _ in range(ntrials):
   psi=np.zeros((40,3),dtype=complex)
   if carrier=='E8':psi[:,0]=1/np.sqrt(40)
   else:
    # Conditional phase-tag realization of the A2 orientation bit.
    tag=np.array([1,1,1,1] if carrier=='E6' else [1,1,1,-1],dtype=complex)/2
    psi[line,0]=tag
   for _ in range(stages):
    ph=rng.uniform(-phase_bound,phase_bound,40);loss=rng.uniform(loss_low,1.0,40)
    psi*= (np.sqrt(loss)*np.exp(1j*ph))[:,None]
    psi=Uport@psi
    H=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));H=(H+H.conj().T)/2
    hn=np.linalg.norm(H);Uint=expm(-1j*0.12*H/(hn if hn else 1.0));psi=psi@Uint.T
   probs=(np.abs(psi)**2).sum(axis=1);probs/=probs.sum()
   counts=rng.multinomial(shots,probs);linefrac=float(counts[line].sum()/shots)
   plus=np.array([1,1,1,1])@psi[line,:];minus=np.array([1,1,1,-1])@psi[line,:]
   den=4*np.sum(np.abs(psi[line,:])**2)+1e-15
   orient=float((np.linalg.norm(minus)**2-np.linalg.norm(plus)**2)/den)
   dtrue=.25 if carrier=='E6' else 0.0;pdark=rho+(1-2*rho)*dtrue
   dark=float(rng.binomial(shots,pdark)/shots)
   pred='E8' if linefrac<.5 else ('E6' if dark>.17 else 'A2')
   vals.append((linefrac,dark,orient,pred==carrier))
  X=np.array([[a,b,c] for a,b,c,_ in vals])
  out[carrier]={'line_min':float(X[:,0].min()),'line_max':float(X[:,0].max()),'dark_min':float(X[:,1].min()),'dark_max':float(X[:,1].max()),'orientation_score_min':float(X[:,2].min()),'orientation_score_max':float(X[:,2].max()),'classifier_correct':int(sum(v[3] for v in vals)),'trials':ntrials}
 return out

def main():
 moderate=profile(9757,.35,3,.30,.85,5000,.05,500)
 heavy=profile(9758,.50,4,.60,.70,2000,.10,500)
 assert all(moderate[c]['classifier_correct']==500 for c in moderate)
 assert all(heavy[c]['classifier_correct']==500 for c in heavy)
 assert moderate['E8']['line_max']<.5<min(moderate['E6']['line_min'],moderate['A2']['line_min'])
 assert heavy['E8']['line_max']<.5<min(heavy['E6']['line_min'],heavy['A2']['line_min'])
 assert moderate['A2']['orientation_score_min']>0>moderate['E6']['orientation_score_max']
 # Under the heavy phase/loss profile the optional phase tag is intentionally allowed to fail.
 assert heavy['A2']['orientation_score_min']<0 and heavy['E6']['orientation_score_max']>0
 out={'schema':'w33.pass9757_9764.coherent_holonet_qutrit_noise.v1','status':'PASS','passes':'9757-9764',
 'model':{'state_space':'40 W33 ports x 3 internal qutrit/OAM-time-bin modes','W33_unitary':'exp(-i theta A_W33/12)','stage_noise':'bounded per-port phase and loss + random small 3x3 internal unitary','finite_shots':True,'dark_monitor':'binary confusion rho+(1-2rho)d'},
 'classifier':'line fraction <0.5 => E8; otherwise dark fraction >0.17 => E6; else A2',
 'moderate_profile':{'parameters':{'seed':9757,'theta':.35,'stages':3,'phase_bound_rad':.30,'loss_intensity_floor':.85,'shots':5000,'dark_confusion':.05},'results':moderate,'orientation_phase_tag':'perfect sign separation in all 1000 line-carrier trials'},
 'heavy_profile':{'parameters':{'seed':9758,'theta':.50,'stages':4,'phase_bound_rad':.60,'loss_intensity_floor':.70,'shots':2000,'dark_confusion':.10},'results':heavy,'carrier_classifier':'1500/1500 correct','orientation_phase_tag':'not robust; score intervals overlap and change sign'},
 'result':'The line+dark carrier classifier survives coherent W33 mixing, qutrit-mode mixing, phase disorder, loss and finite shots in both seeded stress profiles. The optional direct phase realization of the A2 orientation bit survives the moderate profile but fails under the heavy profile before the line+dark carrier identity fails.',
 'boundary':'Seeded numerical stress test, not an exact probability theorem and not a fit to measured Holonet hardware. The +++- phase tag is a conditional encoding model for the abstract A2 orientation bit; the mathematics does not yet derive that optical encoding uniquely.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','moderate_correct':1500,'heavy_correct':1500,'heavy_orientation_tag':False}));return 0
if __name__=='__main__':raise SystemExit(main())
