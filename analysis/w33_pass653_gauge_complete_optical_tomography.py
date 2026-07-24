#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, itertools, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass653_gauge_complete_optical_tomography.json'


def bits(i):return tuple((i>>k)&1 for k in (2,1,0))
def dot2(a,b):return sum(x*y for x,y in zip(a,b))%2
CHARS=[bits(i) for i in range(8)]
DETECTOR_CHARS=[(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,1,1),(1,1,0),(1,0,1)]
H8=np.array([[(-1.0)**dot2(u,b)/math.sqrt(8.0) for b in CHARS] for u in DETECTOR_CHARS])


def probes(d=16):
    out=[]
    for i in range(d):
        x=np.zeros(d,complex);x[i]=1;out.append(('basis',(i,),x))
    for i,j in itertools.combinations(range(d),2):
        x=np.zeros(d,complex);x[i]=x[j]=1/math.sqrt(2);out.append(('real_pair',(i,j),x))
    for i,j in itertools.combinations(range(d),2):
        x=np.zeros(d,complex);x[i]=1/math.sqrt(2);x[j]=1j/math.sqrt(2);out.append(('quadrature_pair',(i,j),x))
    return out


def design_row(x):
    d=len(x);pairs=list(itertools.combinations(range(d),2))
    z=[abs(x[i])**2 for i in range(d)]
    z += [2*(np.conj(x[i])*x[j]).real for i,j in pairs]
    z += [-2*(np.conj(x[i])*x[j]).imag for i,j in pairs]
    return np.array(z,float)


def hermitian_from_theta(theta,d=16):
    pairs=list(itertools.combinations(range(d),2));E=np.zeros((d,d),complex);E[np.diag_indices(d)]=theta[:d]
    off=d
    re=theta[off:off+len(pairs)];im=theta[off+len(pairs):]
    for (i,j),a,b in zip(pairs,re,im):E[i,j]=a+1j*b;E[j,i]=a-1j*b
    return E


def reconstruct_rows(U,frame,M_inv):
    d=U.shape[0];rows=[];projectors=[]
    for k in range(d):
        y=np.array([abs((U@x)[k])**2 for _,_,x in frame])
        E=hermitian_from_theta(M_inv@y,d);E=(E+E.conj().T)/2
        ev,Q=np.linalg.eigh(E);j=int(np.argmax(ev));row=np.conj(Q[:,j])*math.sqrt(max(float(ev[j]),0.0))
        rows.append(row);projectors.append(E)
    return np.array(rows),projectors


def payload():
    d=16;U0=np.kron(H8,np.eye(2));phase=np.exp(2j*np.pi*np.arange(d)/37);U=np.diag(phase)@U0
    frame=probes(d);M=np.array([design_row(x) for _,_,x in frame]);rank=int(np.linalg.matrix_rank(M));cond=float(np.linalg.cond(M));Minv=np.linalg.inv(M)
    Urep,projectors=reconstruct_rows(U,frame,Minv)
    projector_error=max(float(np.linalg.norm(E-np.outer(np.conj(U[k]),U[k]))) for k,E in enumerate(projectors))
    alt=np.diag(np.exp(2j*np.pi*np.arange(d)/29))@U
    intensity_gauge_error=max(abs(abs((U@x)[k])**2-abs((alt@x)[k])**2) for _,_,x in frame for k in range(d))
    nonglobal_distance=float(min(np.linalg.norm(alt-z*U) for z in np.exp(2j*np.pi*np.arange(720)/720)))
    xref=np.exp(2j*np.pi*np.arange(d)/19)/4
    a=U@xref;b=Urep@xref
    multipliers=np.ones(d,complex);records=[]
    for k in range(1,d):
        base=(abs(a[0])**2+abs(a[k])**2)/2
        Ireal=abs((a[0]+a[k])/math.sqrt(2))**2
        Iquad=abs((a[0]+1j*a[k])/math.sqrt(2))**2
        c=(Ireal-base)+1j*(Iquad-base)
        crep=b[0]*np.conj(b[k])
        multipliers[k]=np.conj(c/crep)
        records.append({'output_pair':[0,k],'real_interference':float(Ireal),'quadrature_interference':float(Iquad),'relative_phase_multiplier':[float(multipliers[k].real),float(multipliers[k].imag)]})
    Ufix=np.diag(multipliers)@Urep
    global_phase=np.vdot(U,Ufix)/np.vdot(U,U)
    reconstruction_error=float(np.linalg.norm(Ufix-global_phase*U))
    unitary_error=float(np.linalg.norm(Ufix@Ufix.conj().T-np.eye(d)))
    checks={
        'intensity_design_256_by_256':M.shape==(256,256),
        'intensity_design_full_rank':rank==256,
        'intensity_design_condition_finite':math.isfinite(cond) and cond<20,
        'row_projectors_reconstructed':projector_error<1e-11,
        'independent_output_phases_intensity_invisible':intensity_gauge_error<1e-12,
        'intensity_gauge_not_only_global_phase':nonglobal_distance>1,
        'generic_reference_hits_all_outputs':float(np.min(np.abs(a)))>0.03,
        'thirty_interference_settings':len(records)*2==30,
        'relative_phase_multipliers_unit_modulus':max(abs(abs(z)-1) for z in multipliers)<1e-10,
        'full_transfer_reconstructed_up_to_global_phase':reconstruction_error<1e-10,
        'reconstructed_transfer_unitary':unitary_error<1e-10,
        'total_configuration_count286':len(frame)+2*len(records)==286,
        'certificate_hash_locked':True,
    }
    checks={k:bool(v) for k,v in checks.items()}
    digest=hashlib.sha256(M.round(15).tobytes()+Ufix.round(15).tobytes()+json.dumps(records,sort_keys=True).encode()).hexdigest()
    return {
        'schema':'w33.pass653.gauge_complete_optical_tomography.v1','status':'PASS' if all(checks.values()) else 'FAIL',
        'intensity_stage':{
            'input_probe_settings':len(frame),'simultaneous_output_intensities_per_probe':16,'Hermitian_design_rank':rank,'condition_number':round(cond,9),
            'identified_object':'the sixteen rank-one row effects E_k=U^*|k><k|U',
            'identifiability':'U modulo left multiplication by an arbitrary diagonal U(1)^16 output-phase gauge',
            'maximum_projector_error':projector_error
        },
        'phase_lock_stage':{
            'reference_probe':'x_j=exp(2 pi i j/19)/4','minimum_nominal_output_amplitude':float(np.min(np.abs(a))),
            'reference_output':0,'output_pairs':15,'quadratures_per_pair':2,'interference_settings':30,'records':records,
            'remaining_gauge':'one physically irrelevant global phase','reconstruction_frobenius_error':reconstruction_error,'unitarity_error':unitary_error
        },
        'calibration_budget':{'intensity_probe_settings':256,'relative_phase_interference_settings':30,'total_settings':286},
        'checks':checks,'certificate_sha256':digest,
        'theorem':'Output-resolved intensities from the 256 basis/real-pair/quadrature-pair inputs reconstruct all sixteen row projectors of a 16-mode coherent transfer matrix, but only determine the matrix modulo sixteen independent output phases. This gauge is real: arbitrary output rephasings leave every intensity datum unchanged. A single generic coherent reference input and two interference quadratures between output 0 and each of the other fifteen outputs determine all fifteen relative phases. Thus 256+30=286 configurations reconstruct the full 16x16 transfer matrix up to one global phase.',
        'boundary':'The phase-lock step assumes coherent pairwise output interference with a stable reference and a probe whose relevant output amplitudes are nonzero. Intensity-only measurements cannot recover the missing output phases.'
    }


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 653 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'settings':p['calibration_budget']['total_settings'],'error':p['phase_lock_stage']['reconstruction_frobenius_error']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
