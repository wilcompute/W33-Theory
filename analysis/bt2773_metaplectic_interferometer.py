#!/usr/bin/env python3
"""Pass 2773: physical two-shot metaplectic sensor and shot-noise budget."""
from __future__ import annotations
import json, math
from collections import deque,Counter
from pathlib import Path
import numpy as np
from bt2772_2776_core import *
ROOT=Path(__file__).resolve().parents[1]

def conjugacy_classes(group):
    gs=generators(); unseen=set(group); out=[]
    while unseen:
        seed=min(unseen);orb={seed};q=deque([seed])
        while q:
            x=q.popleft()
            for s in gs:
                y=mm(mm(inv(s),x),s)
                if y not in orb:orb.add(y);q.append(y)
        unseen-=orb;out.append(sorted(orb))
    out.sort(key=lambda c:(len(c),c[0]));assert len(out)==34
    return out

def unitary_generators():
    w=np.exp(2j*np.pi/3);F=np.array([[w**(j*k) for k in range(3)] for j in range(3)],dtype=complex)/np.sqrt(3);S=np.diag([w**((2*j*j)%3) for j in range(3)]).astype(complex);I=np.eye(3,dtype=complex);SUM=np.zeros((9,9),dtype=complex)
    for p in range(3):
        for f in range(3):SUM[3*p+(f+p)%3,3*p+f]=1
    out=[]
    for U in [np.kron(F,I),np.kron(I,F),np.kron(S,I),np.kron(I,S),SUM]:
        out.append(U);Ui=U.conj().T
        if np.max(abs(Ui-U))>1e-10:out.append(Ui)
    assert len(out)==len(generators());return out

def phase_code(z,tol=1e-5):
    if abs(z)<tol:return (1,0,0)
    phase=int(round(2*np.angle(z)/np.pi))%4;exp=int(round(2*math.log(abs(z),3)));recon=(1j**phase)*(3**(exp/2));assert abs(z-recon)<tol*max(1,abs(z));return (0,phase,exp)

def main():
    group,parent=group_closure(with_parent=True);UG=unitary_generators();Umap={I4:np.eye(9,dtype=complex)}
    for g,(prev,j) in parent.items():
        if g!=I4:Umap[g]=Umap[prev]@UG[j]
    classes=conjugacy_classes(group);class_of={g:i for i,c in enumerate(classes) for g in c};codes={}
    for g in group:
        U=Umap[g];code=[]
        for k in (1,2):
            Uk=np.linalg.matrix_power(U,k);code.append(phase_code(np.trace(Uk)**9/np.linalg.det(Uk)))
        i=class_of[g];code=tuple(code)
        if i in codes:assert codes[i]==code
        else:codes[i]=code
    assert len(set(codes.values()))==33
    nonzero=[];raw_rows=[]
    for i,c in enumerate(classes):
        U=Umap[c[0]];row={'class_id':i,'class_size':len(c),'shots':[]}
        for k in (1,2):
            Uk=np.linalg.matrix_power(U,k);t=np.trace(Uk)/9;det=np.linalg.det(Uk);code=phase_code(np.trace(Uk)**9/det)
            if abs(t)>1e-10:nonzero.append(abs(t))
            row['shots'].append({'k':k,'normalized_trace_re':round(float(t.real),15),'normalized_trace_im':round(float(t.imag),15),'normalized_trace_abs':round(float(abs(t)),15),'determinant_phase_rad':round(float(np.angle(det)),15),'theta_zero':code[0],'theta_phase_mod4':code[1],'theta_twice_log3_magnitude':code[2]})
        raw_rows.append(row)
    rmin=min(nonzero);epsilon=rmin*math.sin(math.pi/8)/2;delta=.01;n=math.ceil(2*math.log(8/delta)/(epsilon**2))
    out={'schema':'w33.pass2773.metaplectic_interferometer.v1','status':'EXACT_CODEBOOK_CONSERVATIVE_SHOT_BUDGET','architecture':{'register':'nine-mode two-qutrit register randomized uniformly over computational modes','ancilla':'phase-stable path qubit','shot_1':'controlled-path U, X/Y path readout estimates Tr(U)/9','shot_2':'controlled-path U^2, X/Y path readout estimates Tr(U^2)/9','determinant':'tracked from the programmed Clifford word and calibrated phase plates','decoder':'combine tracked determinant with the ninth power of each measured trace; fuse with the existing W33 projective packet'},'class_count':34,'theta_pair_count':33,'minimum_nonzero_normalized_trace_magnitude':rmin,'conservative_quadrature_tolerance':epsilon,'confidence':1-delta,'shots_per_quadrature_hoeffding':n,'total_detector_events_four_quadratures':4*n,'rows':raw_rows,'boundary':'The shot count is a worst-case Hoeffding design point assuming independent binary path measurements, exact determinant tracking, and no drift. Loss, phase diffusion, visibility, and detector imbalance must be calibrated experimentally; black-box modular DQC1 without a phase reference gives only trace modulus and is insufficient for the full class sensor.'}
    path=ROOT/'data/PART_BT2773_METAPLECTIC_INTERFEROMETER.json';path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');summary={k:out[k] for k in ('schema','status','class_count','theta_pair_count','minimum_nonzero_normalized_trace_magnitude','conservative_quadrature_tolerance','confidence','shots_per_quadrature_hoeffding','total_detector_events_four_quadratures','architecture','boundary')};(ROOT/'data/PART_BT2773_METAPLECTIC_INTERFEROMETER_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print('wrote',path)
if __name__=='__main__':main()
