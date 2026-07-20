#!/usr/bin/env python3
"""Pass 497: optical distinguishability no-go and Galois phase-cycle protocol."""
from __future__ import annotations
import argparse,json,math,random
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass497_optical_depth_observable.json'
class Z9:
 name='Z/9';p=3;size=9;char_order=9;elems=list(range(9));zero=0;one=1;exact_depth=12
 add=staticmethod(lambda a,b:(a+b)%9);neg=staticmethod(lambda a:(-a)%9);mul=staticmethod(lambda a,b:(a*b)%9);smul=staticmethod(lambda n,a:(n*a)%9);chi_exp=staticmethod(lambda a:a)
class F9:
 name='F_9';p=3;size=9;char_order=3;elems=[(a,b) for a in range(3) for b in range(3)];zero=(0,0);one=(1,0);exact_depth=8
 add=staticmethod(lambda u,v:((u[0]+v[0])%3,(u[1]+v[1])%3));neg=staticmethod(lambda u:((-u[0])%3,(-u[1])%3))
 mul=staticmethod(lambda u,v:((u[0]*v[0]+2*u[1]*v[1])%3,(u[0]*v[1]+u[1]*v[0])%3));smul=staticmethod(lambda n,u:((n*u[0])%3,(n*u[1])%3));chi_exp=staticmethod(lambda u:(2*u[0])%3)
class Dual9:
 name='F_3[e]/(e^2)';p=3;size=9;char_order=3;elems=[(a,b) for a in range(3) for b in range(3)];zero=(0,0);one=(1,0);exact_depth=8
 add=staticmethod(lambda u,v:((u[0]+v[0])%3,(u[1]+v[1])%3));neg=staticmethod(lambda u:((-u[0])%3,(-u[1])%3))
 mul=staticmethod(lambda u,v:((u[0]*v[0])%3,(u[0]*v[1]+u[1]*v[0])%3));smul=staticmethod(lambda n,u:((n*u[0])%3,(n*u[1])%3));chi_exp=staticmethod(lambda u:u[1]%3)
class NumHeis:
 def __init__(self,R):
  self.R=R;self.q=R.size;E=R.elems;self.idx={e:i for i,e in enumerate(E)};self.root=np.exp(2j*np.pi/R.char_order)
  vecs=[(a,b) for a in E for b in E if (a,b)!=(R.zero,R.zero)];pairs=[];used=set()
  for v in vecs:
   nv=(R.neg(v[0]),R.neg(v[1]));key=tuple(sorted((v,nv)))
   if key not in used:used.add(key);pairs.append(key)
  self.pairs=pairs
 def full_sec(self,offs):
  f={};R=self.R
  for (v,nv),c in zip(self.pairs,offs):f[v]=c;f[nv]=R.neg(c)
  return f
 def block(self,fsec,noise=None):
  R=self.R;q=self.q;two=R.smul(2,R.one);B=np.zeros((q,q),complex)
  for vi,((a,b),c) in enumerate(fsec.items()):
   ab=R.mul(a,b);eta=0.0 if noise is None else noise[vi]
   for xi,x in enumerate(R.elems):
    z=R.add(c,R.add(R.mul(two,R.mul(x,b)),ab));j=self.idx[R.add(x,a)]
    B[j,xi]+=self.root**R.chi_exp(z)*np.exp(1j*eta)
  return B
def summary(a):
 a=np.asarray(a,float)
 return {k:round(float(v),12) for k,v in {'mean':a.mean(),'std':a.std(),'q10':np.quantile(a,.1),'median':np.median(a),'q90':np.quantile(a,.9)}.items()}
def effect(a,b):
 a=np.asarray(a);b=np.asarray(b);return float((a.mean()-b.mean())/math.sqrt((a.var(ddof=1)+b.var(ddof=1))/2))
def ks(a,b):
 a=np.sort(np.asarray(a));b=np.sort(np.asarray(b));v=np.sort(np.concatenate((a,b)))
 return float(np.max(np.abs(np.searchsorted(a,v,'right')/len(a)-np.searchsorted(b,v,'right')/len(b))))
def run(R,samples,eps,seed):
 H=NumHeis(R);rng=random.Random(seed+R.char_order);nr=np.random.default_rng(seed+R.size+R.char_order)
 F=H.block(H.full_sec(tuple(R.zero for _ in H.pairs)));detF=np.linalg.det(F)
 raw={k:[] for k in ('log_condition','smallest_singular','phase_noise_gain','log10_det_gap')};norm_checks=[];target=R.size*(R.size**2-1)
 for _ in range(samples):
  offs=tuple(rng.choice(R.elems) for _ in H.pairs);fs=H.full_sec(offs);B=H.block(fs);s=np.linalg.svd(B,compute_uv=False)
  raw['log_condition'].append(math.log10(s[0]/max(s[-1],1e-14)));raw['smallest_singular'].append(s[-1]);raw['log10_det_gap'].append(math.log10(max(abs(np.linalg.det(B)-detF),1e-300)))
  norm_checks.append(abs(np.linalg.norm(B,'fro')**2-target)<1e-7)
  eta=nr.normal(0,1,size=len(fs));Bn=H.block(fs,noise=eps*eta)
  raw['phase_noise_gain'].append(np.linalg.norm(Bn-B,'fro')/(eps*np.linalg.norm(B,'fro')))
 return {'ring':R.name,'exact_arithmetic_depth':R.exact_depth,'character_order':R.char_order,'weyl_frobenius_norm_exact':all(norm_checks),'metrics':{k:summary(v) for k,v in raw.items()}},raw
def real_galois_reps(m):
 units=[a for a in range(1,m) if math.gcd(a,m)==1];seen=set();reps=[]
 for a in units:
  if a in seen:continue
  reps.append(a);seen.add(a);seen.add((-a)%m)
 return reps
def main_payload(samples=500):
 results={};raw={}
 for R in (F9,Dual9,Z9):results[R.name],raw[R.name]=run(R,samples,1e-4,497)
 comparisons=[]
 for a,b in [('F_9','Z/9'),('F_3[e]/(e^2)','Z/9'),('F_9','F_3[e]/(e^2)')]:
  metrics={k:{'cohen_d':round(effect(raw[a][k],raw[b][k]),12),'ks':round(ks(raw[a][k],raw[b][k]),12)} for k in raw[a]};comparisons.append({'a':a,'b':b,'metrics':metrics})
 maxd=max(abs(v['cohen_d']) for c in comparisons for v in c['metrics'].values());maxks=max(v['ks'] for c in comparisons for v in c['metrics'].values())
 protocols=[{'character_order':m,'real_embedding_settings':real_galois_reps(m),'settings_count':len(real_galois_reps(m))} for m in (9,25)]
 checks={'all_section_norms_exact':all(r['weyl_frobenius_norm_exact'] for r in results.values()),'iid_noise_gain_near_one':all(abs(r['metrics']['phase_noise_gain']['mean']-1)<0.08 for r in results.values()),'ordinary_metrics_small_effect':maxd<0.2,'ordinary_metrics_small_KS':maxks<0.15,'real_phase_cycle_halves_settings':all(2*x['settings_count']==sum(math.gcd(a,x['character_order'])==1 for a in range(1,x['character_order'])) for x in protocols)}
 return {'schema':'w33.pass497.optical_depth_observable.v1','status':'PASS' if all(checks.values()) else 'FAIL','theorem':'Weyl orthogonality fixes ||B||_F^2=q(q^2-1) and makes normalized iid first-order phase-noise gain equal to one in expectation.','no_go':'Ordinary one-embedding conditioning and iid phase-jitter response do not expose lambda-adic determinant depth.','replacement_protocol':'Cycle the central phase over Gal(K+/Q), measure determinant gaps, multiply to obtain the relative norm, then square for the full norm and recover lambda depth by p-divisibility.','samples_per_ring':samples,'rings':results,'comparisons':comparisons,'max_abs_cohen_d':round(maxd,12),'max_ks':round(maxks,12),'galois_phase_cycles':protocols,'boundary':'The orthogonality/noise statement is analytic. The small-separation statement is a deterministic numerical census, not a universal theorem about every hardware noise model.','checks':checks}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=500);ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();pl=main_payload(a.samples);text=json.dumps(pl,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 497 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':pl['status'],'checks':sum(pl['checks'].values()),'total':len(pl['checks']),'max_d':pl['max_abs_cohen_d'],'max_ks':pl['max_ks']}));return 0 if pl['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
