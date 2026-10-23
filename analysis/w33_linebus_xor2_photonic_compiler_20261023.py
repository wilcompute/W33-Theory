#!/usr/bin/env python3
"""Exact restricted 4x4 XOR photonic switch compiler for the 40 W33 line buses.

Four 2x2 MZIs in two balanced stages:
 stage L: optical pairs (0,1) and (2,3), same low address bit.
 stage H: optical pairs (0,2) and (1,3), same high address bit.
For each XOR mask 0..3, its transfer is i**popcount(mask) * P(mask).
A global phase-frame tracked modulo 4 restores exactly P(mask).
This 4-state restricted network is NOT a general nonblocking 4x4 crossbar.
Loss and phase errors below are synthetic, NOT measured or PDK qualified.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from w33_fractal_linebus_switch_matrix_20261023 import (
    LINES,THROUGH,EDGE_LINE,bus_schedule,permutation_matrix,counts
)

PAIRS=((0,1),(2,3),(0,2),(1,3))
STAGES=(('LOW', (0,1)), ('HIGH', (2,3)))
MODES=4
BUS_COUNT=len(LINES)

def mzi(theta):
    """A convenient ideal balanced 2x2 MZI gauge: bar=I, cross=i X."""
    c,s=math.cos(theta/2),math.sin(theta/2)
    return np.array([[c,1j*s],[1j*s,c]],dtype=np.complex128)

def embed_2x2(C,a,b):
    U=np.eye(MODES,dtype=np.complex128)
    U[np.ix_((a,b),(a,b))]=C
    return U

def design(mask, *, phase_errors=None, mzi_loss_db=0.0,
           crossing_loss_db=0.0):
    """Produce a 4x4 field transfer and coherent amplitude diagnostics.

    In this surrogate, every optical route passes through two MZI cells.
    The interstage waveguide crossing loss is a uniform phenomenological
    assumption: this is not a placement or optical extraction.
    """
    if mask not in range(4):raise ValueError("mask must be 0..3")
    if mzi_loss_db<0 or crossing_loss_db<0:raise ValueError("losses must be nonnegative")
    errors=np.zeros(4) if phase_errors is None else np.asarray(phase_errors,dtype=float)
    if errors.shape!=(4,) or not np.all(np.isfinite(errors)):raise ValueError("four finite phase errors required")
    low,high=(mask&1),((mask>>1)&1)
    target_angles=[math.pi*low,math.pi*low,math.pi*high,math.pi*high]
    U=np.eye(4,dtype=complex)
    cell_matrices=[]
    for k,(a,b) in enumerate(PAIRS):
        M=embed_2x2(mzi(target_angles[k]+errors[k]),a,b)
        cell_matrices.append(M)
        # k=0,1 are disjoint stage LOW; 2,3 are disjoint stage HIGH
        U=M@U
    assert np.linalg.norm(U.conj().T@U-np.eye(4))<1e-12
    phase_exp=mask.bit_count() % 4
    frame=(1j)**phase_exp
    corrected=U/frame
    P=permutation_matrix(mask)
    amp=10**(-(2*mzi_loss_db+crossing_loss_db)/20.0)
    T=amp*U
    powers=np.abs(T)**2
    expected=[int(i^mask) for i in range(4)]
    desired=[float(powers[expected[i],i]) for i in range(4)]
    unwanted=[float(powers[:,i].sum()-desired[i]) for i in range(4)]
    return {
        'mask':mask,'two_bit_control':[low,high],
        'phase_frame_exponent_mod4':phase_exp,
        'ideal_permutation':expected,
        'raw_U':U,'compensated_U':corrected,'transfer_T':T,
        'desired_port_power':desired,'wrong_port_power':unwanted,
        'unitary_residual':float(np.linalg.norm(U.conj().T@U-np.eye(4))),
        'ideal_permutation_residual':float(np.linalg.norm(corrected-P)),
        'phase_commands_rad':[float(a) for a in target_angles],
        'stage_depth_per_route':2,
        'power_loss_db_uniform':2*mzi_loss_db+crossing_loss_db}

def cells(bus_id):
    if not 0<=bus_id<BUS_COUNT:raise ValueError("bus 0..39")
    line=LINES[bus_id]
    inputs=[f'BUS_{bus_id:02d}/IN_{k}' for k in range(4)]
    outputs=[f'BUS_{bus_id:02d}/S0_{k}' for k in range(4)]
    final=[f'BUS_{bus_id:02d}/OUT_{k}' for k in range(4)]
    result=[]
    for k,(a,b) in enumerate(PAIRS):
        first=k<2
        result.append({
            'cell_id':f'BUS_{bus_id:02d}/MZI_{k}',
            'stage':0 if first else 1,
            'logical_address_bit':'LOW' if first else 'HIGH',
            'control_word':f'BUS_{bus_id:02d}/CTRL_{0 if first else 1}',
            'physical_driver':f'UNASSIGNED_ELECTRODE_BUS_{bus_id:02d}_MZI_{k}',
            'pair':[a,b],
            'optical_input':[inputs[a],inputs[b]] if first else [outputs[a],outputs[b]],
            'optical_output':[outputs[a],outputs[b]] if first else [final[a],final[b]],
            'child_nodes':[int(line[a]),int(line[b])],
            'PDK_cell':'UNSELECTED',
            'optical_crossings':'OPEN: second stage pairs (0,2),(1,3)',
            'calibration':'measured bar/cross bias, coherent phase, MZI leakage and loss'
        })
    return result

def stage_frame(mask):
    r=design(mask)
    return {'mask':mask,'low_bit':mask&1,'high_bit':(mask>>1)&1,
      'raw_bus_scalar_phase_exponent_mod4':r['phase_frame_exponent_mod4'],
      'bus_frame_correction':f'i^(-{r["phase_frame_exponent_mod4"]})',
      'ideal_permutation':r['ideal_permutation']}

def virtual_phase_of_route(masks):
    """Ideal bus-global-phase bookkeeping only, not full modal phase tracking."""
    v=sum(m.bit_count() for m in masks)%4
    return {'exponent_mod4':v,'raw_phase_complex':[int(round((1j**v).real)),int(round((1j**v).imag))],
            'correction':'(-i)^%d'%v,
            'requires_path_phase_reference':True}

def compile_manifest(mzi_loss_db=.2,crossing_loss_db=.1,phase_error_rad=.05):
    circuits=[cells(i) for i in range(BUS_COUNT)]
    flat=[c for sub in circuits for c in sub]
    assert len(flat)==160 and len({x['cell_id'] for x in flat})==160
    assert len({x['control_word'] for x in flat})==80
    demands=bus_schedule()
    schedule=[stage_frame(x) for x in (1,2,3)]
    models=[]
    for mask in (0,1,2,3):
        ideal=design(mask)
        assert ideal['ideal_permutation_residual']<1e-14
        faulty=design(mask,phase_errors=[phase_error_rad]*4,
                      mzi_loss_db=mzi_loss_db,crossing_loss_db=crossing_loss_db)
        models.append({
           'mask':mask,'ideal_unitary_residual':ideal['unitary_residual'],
           'ideal_compensated_residual':ideal['ideal_permutation_residual'],
           'frame_exponent':ideal['phase_frame_exponent_mod4'],
           'desired_port_powers':faulty['desired_port_power'],
           'wrong_port_powers':faulty['wrong_port_power'],
           'hypothetical_transmission_loss_db':faulty['power_loss_db_uniform'],
           'phase_error_rad':phase_error_rad
        })
    # An unrestricted S4 has 24 permutations. Only the four XOR masks are
    # controllable here; a nonblocking arbitrary 4x4 crossbar is NOT implied.
    perms={tuple(design(k)['ideal_permutation']) for k in range(4)}
    assert len(perms)==4
    assert len({tuple(p) for p in itertools.permutations(range(4))})==24
    manifest={
       'schema':'w33.photonic.forty_bus_xor2_mzi_compiler.v1',
       'date':'2026-10-23','scope':'exact restricted 4x4 XOR family, ideal MZI; hypothetical model only',
       'source':'analysis/w33_fractal_linebus_switch_matrix_20261023.py',
       'external_prior_art':[
          {'title':'Silicon nitride based polarization-independent 4x4 optical matrix switch',
           'url':'https://www.sciencedirect.com/science/article/abs/pii/S0030399219300702',
           'finding':'2019 reported a fabricated 4x4 switch based on four 2x2 MZIs; topology novelty NOT claimed'},
          {'title':'Calibration-Free Mach-Zehnder Silicon-Photonic Switch',
           'url':'https://opg.optica.org/abstract.cfm?URI=OFC-2021-Tu5B.3',
           'finding':'measured nonzero crosstalk and phase error require device calibration'}],
       'bus_count':40,'bus_optical_ports':160,'bus_cell_inventory':flat,
       'target_family_size':4,'full_S4_permutations':24,
       'physical_MZI_cell_count':160,
       'generic_U4_mesh_baseline_MZI_cells':240,
       'reduction_fraction_vs_generic_mesh':1-160/240,
       'continuous_phase_coordinates_to_target_these_three_permutations':'not arbitrary U4; two binary stage control bits per bus',
       'independent_stage_control_words':80,
       'per_cell_independent_trim_possible':160,
       'unassigned_electrode_terminals':160,
       'per_path_cells_traversed':2,'phase_frame':'i^(popcount(mask)) is global per ideal isolated bus; relative phase across buses requires tracking',
       'global_slot_commands':schedule,
       'per_bus_photon_pair_schedule_count':len(demands),
       'per_slot_pair_count':{str(slot):sum(len(x['pairs']) for x in demands if x['slot']==slot) for slot in (0,1,2)},
       'synthetic_parameters':{'mzi_loss_db':mzi_loss_db,'crossing_loss_db':crossing_loss_db,
                               'all_cell_phase_error_rad':phase_error_rad},
       'loss_phase_sweep':models,
       'modeling_gates':[
           'fixed second-stage optical pairings (0,2),(1,3) require routing/crossings in a real planar PIC',
           'uniform crossing loss is illustrative; actual optical path mismatch and coupler insertion loss may vary',
           'MZI cross state carries relative global phase i, requiring tracked phase reference for quantum-coherent routing',
           'binary control words may broadcast, yet fabrication drift requires independently characterized per-cell trim',
           '4 reachable XOR permutations out of 24 S4 permutations; this is a restricted switch, not a general 4x4 crossbar',
           'every child touches four line buses simultaneously; physical sources, modes, switch arbitration and quantum protocols remain unresolved',
           'no gdsfactory, PDK, physical waveguides, DRC, electrodes, measurements, optical power budget or chip fabrication'] }
    canonical=json.dumps(manifest,sort_keys=True,separators=(',',':'),allow_nan=False)
    manifest['digest_sha256']=hashlib.sha256(canonical.encode()).hexdigest()
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--mzi-loss-db',type=float,default=.2)
    p.add_argument('--crossing-loss-db',type=float,default=.1)
    p.add_argument('--phase-error-rad',type=float,default=.05)
    p.add_argument('--out',type=Path,default=ROOT/'data/w33_linebus_xor2_photonic_compiler_20261023.json')
    args=p.parse_args()
    obj=compile_manifest(args.mzi_loss_db,args.crossing_loss_db,args.phase_error_rad)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n',encoding='utf-8')
    print('PASS buses',obj['bus_count'],'cells',obj['physical_MZI_cell_count'],
          'stage_control_words',obj['independent_stage_control_words'],
          'frames',[(v['mask'],v['raw_bus_scalar_phase_exponent_mod4']) for v in obj['global_slot_commands']],
          'digest',obj['digest_sha256'])
