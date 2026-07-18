#!/usr/bin/env python3
"""Pass 426: deterministic mixed-state phase portrait for the five-qutrit map."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np

from w33_pass410_414_common import certificate,write_json
from w33_pass416_qutrit_distillation_search import five_qutrit_decoder,mixed_protocol

def round_floats(x,digits=12):
    if isinstance(x,float): return round(x,digits)
    if isinstance(x,list): return [round_floats(v,digits) for v in x]
    if isinstance(x,tuple): return [round_floats(v,digits) for v in x]
    if isinstance(x,dict): return {k:round_floats(v,digits) for k,v in x.items()}
    return x

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass426_mixed_qutrit_phase_portrait.json'
SEEDS=ROOT/'data'/'w33_pass421_fixed_point_seeds.json'


def gell_mann()->list[np.ndarray]:
    z=np.zeros((3,3),complex)
    mats=[]
    for i,j in ((0,1),(0,2),(1,2)):
        a=z.copy();a[i,j]=a[j,i]=1;mats.append(a)
        b=z.copy();b[i,j]=-1j;b[j,i]=1j;mats.append(b)
    mats.insert(2,np.diag([1,-1,0]).astype(complex))
    mats.append(np.diag([1,1,-2]).astype(complex)/np.sqrt(3))
    return mats


def iterate(rho:np.ndarray,D:np.ndarray,max_steps:int=30,tol:float=1e-11)->dict:
    target=np.eye(3)/3;history=[];amin=1.0;positive=True
    for step in range(max_steps):
        out,acc=mixed_protocol(rho,D);amin=min(amin,acc)
        out=(out+out.conj().T)/2;out/=np.trace(out).real
        positive &= float(np.linalg.eigvalsh(out).min())>-1e-10
        history.append(out.copy())
        if np.linalg.norm(out-target)<tol:
            return {'classification':'maximally_mixed','steps':step+1,'distance':float(np.linalg.norm(out-target)),'minimum_acceptance':amin,'positive':positive}
        rho=out
    periods={p:float(np.linalg.norm(history[-1]-history[-1-p])) for p in range(1,min(6,len(history)-1)+1)}
    purity=float(np.trace(rho@rho).real)
    classification='boundary_purifying' if purity>0.95 else 'unresolved'
    return {'classification':classification,'steps':max_steps,'distance':float(np.linalg.norm(rho-target)),'purity':purity,'minimum_acceptance':amin,'positive':positive,'period_residuals':periods}


def build_payload()->dict:
    D,diag=five_qutrit_decoder();mix=np.eye(3)/3;basis=gell_mann();h=1e-5
    J=np.zeros((8,8))
    for j,L in enumerate(basis):
        plus,_=mixed_protocol(mix+h*L,D);minus,_=mixed_protocol(mix-h*L,D)
        delta=(plus-minus)/(2*h)
        for i,M in enumerate(basis): J[i,j]=np.trace(M@delta).real/2
    je=np.linalg.eigvals(J);jrho=float(max(abs(je)))

    rng=np.random.default_rng(426);local=[]
    for index in range(12):
        A=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));X=(A+A.conj().T)/2;X-=np.trace(X).real*np.eye(3)/3;X/=np.linalg.norm(X)
        d=[];sec=[]
        for eps in (0.04,0.02,0.01):
            plus,_=mixed_protocol(mix+eps*X,D);minus,_=mixed_protocol(mix-eps*X,D)
            d.append(float(np.linalg.norm(plus-mix)))
            sec.append(float(np.linalg.norm(plus+minus-2*mix)/(eps*eps)))
        orders=[math.log(d[i]/d[i+1],2) for i in range(2)]
        local.append({'direction':index,'response_norms':d,'halving_orders':orders,'second_difference_quotients':sec})

    p0=np.diag([1,0,0]).astype(complex);axis=[]
    for r in (0.0,0.1,0.25,0.5,0.75,0.9,1.0):
        rho=(1-r)*mix+r*p0;out,acc=mixed_protocol(rho,D);expected=(1-r**5)*mix+r**5*p0
        axis.append({'r':r,'output_r':r**5,'matrix_error':float(np.max(np.abs(out-expected))),'acceptance':acc})

    roots=json.loads(SEEDS.read_text());basins=[]
    for idx,row in enumerate(roots):
        v=np.array([complex(a,b) for a,b in row]);v/=np.linalg.norm(v);P=np.outer(v,v.conj())
        for r in (0.1,0.5,0.9):
            result=iterate((1-r)*mix+r*P,D)
            basins.append({'family':'depolarized_pure_fixed_point','seed_index':idx,'radius':r,**result})
    for idx in range(48):
        A=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));rho=A@A.conj().T;rho/=np.trace(rho).real;rho=.75*rho+.25*mix
        result=iterate(rho,D)
        basins.append({'family':'seeded_hilbert_schmidt_interior','seed_index':idx,'initial_purity':float(np.trace(rho@rho).real),**result})
    exceptional={8,9,16,17,27,28}
    boundary=[r for r in basins if r['classification']=='boundary_purifying']
    unresolved=[r for r in basins if r['classification']=='unresolved']
    v=np.array([complex(a,b) for a,b in roots[8]]);v/=np.linalg.norm(v);P=np.outer(v,v.conj());ray=[]
    for r in np.linspace(.80,.98,37):
        result=iterate((1-r)*mix+r*P,D,max_steps=30,tol=1e-10)
        ray.append({'radius':round(float(r),6),**result})
    labels=[x['classification'] for x in ray]
    transitions=sum(labels[i]!=labels[i-1] for i in range(1,len(labels)))
    checks={
      'maximally_mixed_fixed':np.linalg.norm(mixed_protocol(mix,D)[0]-mix)<1e-13,
      'maximally_mixed_acceptance_one_over_81':abs(mixed_protocol(mix,D)[1]-1/81)<1e-14,
      'jacobian_zero_to_1e_8':jrho<1e-8,
      'generic_local_order_is_cubic':all(min(x['halving_orders'])>2.9 and max(x['halving_orders'])<3.1 for x in local),
      'quadratic_term_vanishes_numerically':max(x['second_difference_quotients'][-1] for x in local)<1e-3,
      'computational_axis_exact_r_fifth':max(x['matrix_error'] for x in axis)<1e-12,
      'computational_axis_constant_acceptance':max(abs(x['acceptance']-1/81) for x in axis)<1e-13,
      'deterministic_census_has_141_seeds':len(basins)==141,
      'exactly_six_boundary_purifying_seeds':len(boundary)==6 and {x['seed_index'] for x in boundary}==exceptional,
      'remaining_135_converge_to_mixed':sum(x['classification']=='maximally_mixed' for x in basins)==135,
      'all_random_interior_seeds_converge':all(x['classification']=='maximally_mixed' for x in basins if x['family']=='seeded_hilbert_schmidt_interior'),
      'no_unresolved_census_seeds':not unresolved,
      'all_iterates_remain_positive':all(x['positive'] for x in basins),
      'ray_has_interleaved_outcomes':transitions>=3 and 'maximally_mixed' in labels and 'boundary_purifying' in labels,
      'pure_boundary_still_31_points':len(roots)==31,
      'decoder_isometry':diag['decoder_isometry_error']<1e-10,
    };checks={k:bool(v) for k,v in checks.items()}
    payload={'schema':'w33.pass426.mixed_qutrit_phase_portrait.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{
       'interior_fixed_point':'I/3 is fixed with acceptance 1/81 and vanishing linearization',
       'local_order':'generic traceless perturbations return with cubic order; the computational-axis invariant family is exceptionally quintic with r_out=r^5',
       'basin_census':'135 of 141 deterministic full-rank seeds converge to I/3; the six members of one Clifford orbit at radius 0.9 purify toward the pure boundary',
       'pure_boundary':'the 31 pure projective fixed points remain repelling boundary points from Pass 421',
       'boundary':'the interleaved one-ray outcomes are a numerical Julia-like signature, not a proof of a fractal boundary; near-pure long iterates require interval or exact arithmetic'},
      'maximally_mixed':{'acceptance_probability':mixed_protocol(mix,D)[1],'jacobian_spectral_radius':jrho,'jacobian_eigenvalues':[[float(z.real),float(z.imag)] for z in je]},
      'local_cubic_directions':local,'computational_axis':axis,
      'basin_summary':{'seed_count':len(basins),'mixed_attractor_count':sum(x['classification']=='maximally_mixed' for x in basins),'boundary_purifying_count':len(boundary),'exceptional_clifford_orbit':sorted(exceptional),'maximum_steps':max(x['steps'] for x in basins),'minimum_acceptance':min(x['minimum_acceptance'] for x in basins),'unresolved_count':len(unresolved),'families':{'depolarized_pure_fixed_point':93,'seeded_hilbert_schmidt_interior':48}},
      'exceptional_ray_scan':{'representative_seed':8,'sample_count':len(ray),'outcome_transitions':transitions,'samples':ray},
      'selected_basin_records':basins[:6]+basins[90:99]+basins[-6:],
      'checks':checks}
    payload=round_floats(payload);payload['certificate_sha256']=certificate(payload);return payload


def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 426 certificate drift')
 else:write_json(a.output,p)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
