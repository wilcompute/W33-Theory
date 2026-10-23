#!/usr/bin/env python3
"""2026-10-23: exact U(16) Givens gauge reduction and logical photonic I/O manifest.

This is an optical/electrical SCHEMATIC CONTRACT, not a PDK cell, GDS, DRC,
electrode pad assignment, interferometer decomposition or measured calibration.
The source v5 Reck/Givens sequence is NOT silently mapped onto v5's Clements-
style GDS placement rectangles.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from w33_levi_next5_v5_hybrid import ACTIVE, halmos, givens_decompose, synthesize

N=16
TAU=2*math.pi
def wrap(x):
    return float(np.angle(np.exp(1j*float(x))))

def reduce_gauge(rotations, terminal_phases, n=N):
    """Eliminate one diagonal SU(2) gauge phase per two-mode rotation.

    G(theta,phi,alpha)=diag(exp(i alpha),exp(-i alpha)) R(theta,phi).
    In U=G0^H ... Gm^H D, commute each accumulated diagonal P through Rk^H:
       P Rk^H(theta,phi) = Rk^H(theta,phi+p_i-p_j) P.
    Thus alpha is absorbed into later phi coordinates and the rightmost D.
    """
    pending=np.zeros(n)
    gates=[]
    for k,(i,j,theta,phi,alpha) in enumerate(rotations):
        new_phi=wrap(phi+pending[i]-pending[j])
        gates.append({'gate_id':f'MZI_{k:03d}', 'algebraic_index':k,
                      'modes':[int(i),int(j)],'theta_rad':float(theta),
                      'phi_rad':new_phi,'eliminated_alpha_rad':float(alpha)})
        pending[i]-=float(alpha)
        pending[j]+=float(alpha)
    last=[wrap(terminal_phases[i]+pending[i]) for i in range(n)]
    return gates,last

def construct():
    scale,C,U=halmos(ACTIVE)
    assert U.shape==(N,N)
    rotations,terminal=givens_decompose(U)
    assert len(rotations)==120 and len(terminal)==16
    original=synthesize([(x[0],x[1]) for x in rotations],
                        np.array([x[2] for x in rotations]),
                        np.array([x[3] for x in rotations]),
                        np.array([x[4] for x in rotations]),terminal)
    gates,terminal_reduced=reduce_gauge(rotations,terminal)
    reduced=synthesize([g['modes'] for g in gates],
                       np.array([g['theta_rad'] for g in gates]),
                       np.array([g['phi_rad'] for g in gates]),
                       np.zeros(len(gates)),np.array(terminal_reduced))
    residual_original=float(np.linalg.norm(U-original))
    residual_reduced=float(np.linalg.norm(U-reduced))
    gauge_equivalence=float(np.linalg.norm(original-reduced))
    # The upstream floating-point Halmos square root has ~5e-9 residual.
    # Gauge elimination must agree much more tightly with ORIGINAL synthesize.
    assert residual_original<1e-7 and residual_reduced<1e-7 and gauge_equivalence<1e-11, (residual_original,residual_reduced,gauge_equivalence)
    assert float(np.max(np.abs(U.imag)))<1e-12

    # The rightmost diagonal acts on INPUT rails in column-vector convention.
    # The physical propagation order is D, G(m-1)^H, ..., G0^H.
    controls=[]
    optical_paths={i:f'IN_{i:02d}' for i in range(N)}
    terminal_cells=[]
    for i in range(N):
        terminal_cells.append({'cell_id':f'INPUT_PHASE_{i:02d}',
            'optical_input':optical_paths[i],'optical_output':f'PHASE_OUT_{i:02d}',
            'phase_rad':terminal_reduced[i]})
        controls.append({'control_id':f'PHASE_IN_{i:02d}','role':'input_diagonal_phase',
            'cell_id':f'INPUT_PHASE_{i:02d}','driver_channel':f'VIRTUAL_DRV_IN_{i:02d}',
            'phase_rad':terminal_reduced[i],'calibration':'COHERENT_TRANSFER_COLUMNS'})
        optical_paths[i]=f'PHASE_OUT_{i:02d}'
    wired=[]
    for stage,g in enumerate(reversed(gates)):
        i,j=g['modes']
        wired.append({'cell_id':g['gate_id'],'physical_sequence_index':stage,
            'algebraic_index':g['algebraic_index'],'modes':[i,j],
            'inputs':[optical_paths[i],optical_paths[j]],
            'outputs':[f'{g["gate_id"]}_OUT_{i:02d}',f'{g["gate_id"]}_OUT_{j:02d}'],
            'operation':'G(theta,phi,alpha=0)^H in U reconstruction',
            'terminal_phase_location':'at physical input (rightmost matrix factor)'})
        optical_paths[i]=wired[-1]['outputs'][0]
        optical_paths[j]=wired[-1]['outputs'][1]
        for role in ('theta','phi'):
            controls.append({'control_id':f'{g["gate_id"]}_{role.upper()}',
                'role':f'two_mode_{role}','cell_id':g['gate_id'],
                'driver_channel':f'VIRTUAL_DRV_{g["algebraic_index"]:03d}_{role.upper()}',
                'phase_rad':g[f'{role}_rad'],'calibration':'COHERENT_TRANSFER_COLUMNS'})
    assert len(controls)==256 and len(set(c['control_id'] for c in controls))==256
    assert len(set(c['driver_channel'] for c in controls))==256
    assert len(wired)==120 and len(terminal_cells)==16
    assert all(c['inputs'][0]!=c['inputs'][1] for c in wired)
    assert len(set(optical_paths.values()))==16

    # Input basis powers (|U|^2) cannot identify a rightmost input phase,
    # even in a mathematically perfect lossless mesh. Coherent reference
    # transfer measurements are required for those phases.
    pert=np.array(terminal_reduced)
    pert[0]+=0.3141592653589793
    transformed=synthesize([g['modes'] for g in gates],
            np.array([g['theta_rad'] for g in gates]),
            np.array([g['phi_rad'] for g in gates]),
            np.zeros(len(gates)),pert)
    intensity_ambiguity=float(np.max(np.abs(np.abs(transformed)**2-np.abs(reduced)**2)))
    coherent_signal=float(np.max(np.abs(transformed-reduced)))
    assert intensity_ambiguity<1e-12 and coherent_signal>0.1

    # Algebraic two-balanced-coupler identity, not a foundry MZI claim.
    H=np.array([[1.,1.],[1.,-1.]])/math.sqrt(2)
    def D(t):return np.diag([np.exp(1j*t),np.exp(-1j*t)])
    balanced_errors=[]
    for g in gates:
        t,p=g['theta_rad'],g['phi_rad']
        ct,st=math.cos(t),math.sin(t)
        target=np.array([[ct,-st*np.exp(1j*p)],[st*np.exp(-1j*p),ct]],complex)
        gamma=(p+math.pi/2)/2
        physical_surrogate=D(gamma)@H@D(t)@H@D(-gamma)
        balanced_errors.append(float(np.linalg.norm(target-physical_surrogate)))
    max_coupler_identity_error=max(balanced_errors)
    assert max_coupler_identity_error<1e-12

    # For this REAL target, all reduced nonmixing phases lie at 0/pi.
    distance_binary=lambda x:min(abs(wrap(x)),abs(wrap(x-math.pi)))
    phi_binary_error=max(distance_binary(g['phi_rad']) for g in gates)
    terminal_binary_error=max(distance_binary(x) for x in terminal_reduced)
    assert phi_binary_error<1e-10 and terminal_binary_error<1e-10

    observables=[
        {'probe_id':f'BASIS_{k:02d}','preparation':f'coherent input in mode {k}',
         'readout':'16 output powers','samples':16,
         'limitation':'insensitive to input phase for this isolated input'}
        for k in range(N)
    ]
    observables.extend([
        {'probe_id':f'COHERENT_{k:02d}','preparation':f'phase-referenced coherent input mode {k}',
         'readout':'16 output complex amplitudes relative to stable local oscillator',
         'samples':'16 complex transfer elements',
         'requirement':'external phase reference + calibrated SPAM, source loss and detector response'}
        for k in range(N)
    ])
    model={'schema':'w33.photonic.logical_control_manifest.v1',
      'date':'2026-10-23','scope':'Reck-order abstract unitary mesh; no PDK/foundry/layout/physical drive binding',
      'upstream':'analysis/w33_levi_next5_v5_hybrid.py',
      'source_target':{'n_modes':N,'real_orthogonal':True,
                       'mathematical_reck_givens':120,'raw_angles':376,
                       'reduced_unitary_coordinates':256,
                       'structural_fixed_phase_candidate':True},
      'checks':{'original_reconstruction_norm':residual_original,
                'gauge_reduced_reconstruction_norm':residual_reduced,
                'gauge_equivalence_to_original_norm':gauge_equivalence,
                'U_unitary_norm':float(np.linalg.norm(U.conj().T@U-np.eye(N))),
                'binary_phi_distance_max_rad':phi_binary_error,
                'balanced_coupler_factorization_max_residual':max_coupler_identity_error,
                'binary_terminal_distance_max_rad':terminal_binary_error,
                'basis_intensity_input_phase_ambiguity':intensity_ambiguity,
                'coherent_matrix_input_phase_difference':coherent_signal},
      'logical_nets':{'input_ports':[f'IN_{i:02d}' for i in range(N)],
                      'output_ports':[optical_paths[i] for i in range(N)],
                      'input_phase_cells':terminal_cells,'two_mode_cells':wired},
      'controls':controls,'measurements':observables,
      'unresolved':[
        'MZI two-angle physical scattering matrix and phase convention',
        'PDK optical cells, bends, crossings, electro-optic phase shifters',
        'real electrode pads, driver range, pin number, routing and cross-talk',
        'quantitative measurement Jacobian and phase-reference stabilization',
        'Clements-to-Reck re-synthesis if rectangular geometry is desired',
        'foundry DRC/LVS, optical loss, device fabrication and bench validation']}

    # Hash all executable contract fields without a circular self-reference.
    canonical=json.dumps(model,sort_keys=True,separators=(',',':'),allow_nan=False)
    model['sha256']=hashlib.sha256(canonical.encode()).hexdigest()
    return model

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=ROOT/'data/w33_photonic_control_netlist_20261023.json')
    args=parser.parse_args()
    obj=construct()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n',encoding='utf-8')
    print('PASS controls=',len(obj['controls']),'devices=',len(obj['logical_nets']['two_mode_cells']),
       'residual=',obj['checks']['gauge_reduced_reconstruction_norm'],'sha256=',obj['sha256'])
