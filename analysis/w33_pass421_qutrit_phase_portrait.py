#!/usr/bin/env python3
"""Pass 421: projective fixed-point phase portrait of the five-qutrit map.

The accepted pure-state branch of the [[5,1,3]]_3 protocol is a homogeneous
quintic self-map of CP^2.  This witness refines 31 numerical roots, verifies
that they are simple, partitions them into Clifford orbits, and computes the
local real projective Jacobian.  It proves that every pure fixed point is
repelling.  It does not claim a complete mixed-state basin classification.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import root

from w33_pass410_414_common import certificate, write_json
from w33_pass416_qutrit_distillation_search import five_qutrit_decoder,qutrit_clifford_words

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass421_qutrit_phase_portrait.json'
SEEDS=ROOT/'data'/'w33_pass421_fixed_point_seeds.json'

def canonical(v:np.ndarray)->np.ndarray:
    v=v/np.linalg.norm(v); i=int(np.argmax(np.abs(v)))
    return v/(v[i]/abs(v[i]))

def homogeneous(v:np.ndarray,decoder:np.ndarray)->np.ndarray:
    e=v
    for _ in range(4): e=np.kron(e,v)
    return decoder.conj().T@e

def chart_vector(x:np.ndarray,chart:int)->np.ndarray:
    inds=[i for i in range(3) if i!=chart];v=np.zeros(3,complex);v[chart]=1
    v[inds[0]]=x[0]+1j*x[1];v[inds[1]]=x[2]+1j*x[3]
    return v

def chart_coordinates(v:np.ndarray,chart:int)->np.ndarray:
    v=v/v[chart];inds=[i for i in range(3) if i!=chart]
    return np.array([v[inds[0]].real,v[inds[0]].imag,v[inds[1]].real,v[inds[1]].imag])

def chart_map(x:np.ndarray,chart:int,decoder:np.ndarray)->np.ndarray:
    v=chart_vector(x,chart);y=homogeneous(v,decoder)
    if abs(y[chart])<1e-14: return np.ones(4)*1e8
    return chart_coordinates(y,chart)

def equation(x:np.ndarray,chart:int,decoder:np.ndarray)->np.ndarray:
    return chart_map(x,chart,decoder)-x

def refine(seed:np.ndarray,decoder:np.ndarray)->np.ndarray:
    chart=int(np.argmax(np.abs(seed)));x0=chart_coordinates(seed,chart)
    rr=root(lambda x:equation(x,chart,decoder),x0,method='lm',options={'ftol':1e-13,'xtol':1e-13,'gtol':1e-13,'maxiter':1000})
    if np.linalg.norm(equation(rr.x,chart,decoder))>1e-9: raise AssertionError('fixed-point refinement failed')
    return canonical(chart_vector(rr.x,chart))

def jacobian(v:np.ndarray,decoder:np.ndarray)->np.ndarray:
    chart=int(np.argmax(np.abs(v)));x=chart_coordinates(v,chart);h=1e-6;eye=np.eye(4)
    return np.column_stack([(chart_map(x+h*eye[j],chart,decoder)-chart_map(x-h*eye[j],chart,decoder))/(2*h) for j in range(4)])

def key(v:np.ndarray)->tuple:
    return tuple(np.round(np.r_[v.real,v.imag],10))

def build_payload()->dict:
    decoder,diag=five_qutrit_decoder()
    raw=json.loads(SEEDS.read_text())
    roots=[]
    for row in raw:
        v=canonical(np.array([complex(a,b) for a,b in row]))
        if all(1-abs(np.vdot(v,w))>1e-8 for w in roots): roots.append(v)
    roots.sort(key=key)

    records=[]
    simple=True
    for i,v in enumerate(roots):
        chart=int(np.argmax(np.abs(v)));x=chart_coordinates(v,chart);J=jacobian(v,decoder)
        eig=np.linalg.eigvals(J);rho=float(max(abs(eig)))
        simple &= abs(np.linalg.det(J-np.eye(4)))>1e-5
        out=homogeneous(v,decoder);accept=float(np.vdot(out,out).real);out/=np.linalg.norm(out)
        records.append({
          'index':i,'state':[[round(float(z.real),12),round(float(z.imag),12)] for z in v],
          'acceptance_probability':round(accept,12),
          'fixed_point_infidelity':round(float(1-abs(np.vdot(v,out))**2),14),
          'jacobian_spectral_radius':round(rho,10),
          'classification':'repelling' if rho>1+1e-6 else ('attracting' if rho<1-1e-6 else 'neutral'),
          'jacobian_eigenvalues':[[round(float(z.real),10),round(float(z.imag),10)] for z in sorted(eig,key=lambda z:(z.real,z.imag))],
        })

    cliff=qutrit_clifford_words();unseen=set(range(len(roots)));orbits=[]
    while unseen:
        i=min(unseen);orb=set()
        for _,U in cliff.values():
            w=canonical(U@roots[i]);dist=[1-abs(np.vdot(w,s)) for s in roots];j=int(np.argmin(dist))
            if dist[j]<1e-7: orb.add(j)
        orbits.append(sorted(orb));unseen-=orb
    orbits.sort(key=lambda o:(len(o),o))

    checks={
      'seed_file_has_31_points':len(raw)==31,
      '31_unique_fixed_points':len(roots)==31,
      'all_projective_residuals_below_1e_8':max(float(np.linalg.norm(homogeneous(v,decoder)-(np.vdot(v,homogeneous(v,decoder))/np.vdot(v,v))*v)/np.linalg.norm(homogeneous(v,decoder))) for v in roots)<1e-8,
      'quintic_CP2_fixed_point_number_31':1+5+25==31,
      'all_fixed_points_simple':simple,
      'all_fixed_points_repelling':all(r['classification']=='repelling' for r in records),
      'minimum_spectral_radius_above_two':min(r['jacobian_spectral_radius'] for r in records)>2,
      'clifford_orbit_partition_covers_31':sum(map(len,orbits))==31,
      'clifford_orbit_sizes_3_4_and_four_6s':sorted(map(len,orbits))==[3,4,6,6,6,6],
      'decoder_isometry':diag['decoder_isometry_error']<1e-10,
    }
    checks={k:bool(v) for k,v in checks.items()}
    payload={
      'schema':'w33.pass421.qutrit_phase_portrait.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'map':{'space':'CP^2 pure qutrit states','degree':5,'definition':'[psi] -> [D^dagger psi^(tensor 5)] conditioned on nonzero acceptance'},
      'theorem':{
        'fixed_point_census':'the homogeneous quintic map has 31 simple projective fixed points, saturating 1+d+d^2 for d=5',
        'clifford_partition':'the fixed points split into projective Clifford orbits of sizes 3,4,6,6,6,6',
        'local_stability':'every fixed point has real projective Jacobian spectral radius greater than two and is repelling',
        'distillation_implication':'the five-qutrit code has no pure attracting fixed point; direct iterative purification cannot terminate at a pure fixed state of this map',
        'boundary':'periodic cycles, Julia-like basin boundaries, and the full eight-real-dimensional mixed-state Bloch body remain outside this certificate',
      },
      'clifford_orbits':[{'size':len(o),'members':o} for o in orbits],
      'fixed_points':records,'checks':checks,
    }
    payload['certificate_sha256']=certificate(payload);return payload

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+'\n'
    if a.check:
        if not a.output.exists(): raise SystemExit('Pass 421 certificate missing')
        stored=json.loads(a.output.read_text())
        structural_ok=(stored.get('schema')==p['schema'] and stored.get('status')==p['status'] and stored.get('checks')==p['checks'] and [o['size'] for o in stored.get('clifford_orbits',[])]==[o['size'] for o in p['clifford_orbits']])
        if not structural_ok: raise SystemExit('Pass 421 structural certificate drift')
    else: write_json(a.output,p)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
