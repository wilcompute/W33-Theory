#!/usr/bin/env python3
"""Five-track Holonet engineering front: interference, route optimization, qutrit bridge,
Walsh alternative, and fail-closed physical PIC handoff. NO fabricated hardware.
"""
from __future__ import annotations
import argparse,heapq,hashlib,json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_linebus_switch_matrix_20261023 import (
    LINES,ADJ,THROUGH,EDGE_LINE,linebus_neighbors,linebus_route,permutation_matrix,bus_index
)
from w33_linebus_coherent_path_phase_frame_20261023 import route_frame,transport
from w33_linebus_xor2_photonic_compiler_20261023 import design,cells

def measure_interference(path_a=(0,4,7),path_b=(0,14,7),
                         shots_per_phase=10000,visibility=.85,seed=20261023):
    """Synthetic four-phase interference; not a real experiment."""
    if not 0<visibility<=1 or shots_per_phase<1:raise ValueError('invalid experimental inputs')
    ideal_delta=(route_frame(path_a)-route_frame(path_b))%4
    true_phase=math.pi*ideal_delta/2
    rng=np.random.default_rng(seed)
    scan=[0,math.pi/2,math.pi,3*math.pi/2]
    prob=[.5*(1+visibility*math.cos(true_phase+t)) for t in scan]
    obs=[int(rng.binomial(shots_per_phase,p)) for p in prob]
    rates=[x/shots_per_phase for x in obs]
    x=rates[0]-rates[2] # visibility*cos(delta)
    y=rates[3]-rates[1] # visibility*sin(delta)
    est=math.atan2(y,x)
    vhat=math.hypot(x,y)
    sigma=math.sqrt(max(1e-30,1-vhat*vhat/2)/(2*shots_per_phase))/max(vhat,1e-12)
    # Sigma is only an approximate shot-noise scale; not a calibrated CI.
    return {'model':'independent binomial photon count surrogate; no device data',
       'routes':[list(path_a),list(path_b)],
       'ideal_phase_exponent':ideal_delta,'ideal_relative_phase_rad':true_phase,
       'scan_phase_rad':scan,'predicted_probability':prob,
       'sample_counts':obs,'shots_per_phase':shots_per_phase,'seed':seed,
       'estimated_phase_rad':est,'estimated_visibility':vhat,
       'approximate_phase_uncertainty_scale_rad':sigma,
       'controls':['physical delay scan','relative coherence and polarization',
          'stable source and detectors','phase reference','dark count and drift',
          'balanced recombiner and detector efficiency asymmetry'],
       'fail_if':'uncontrolled path phase or source-detector preparation dominates signal'}

def edge_info(a,b):
    a,b=tuple(a),tuple(b)
    if b not in linebus_neighbors(a):raise ValueError('illegal linebus hop')
    idx=[i for i,(u,v) in enumerate(zip(a,b)) if u!=v]
    assert idx
    i=idx[0]
    line=bus_index(a[i],b[i])
    loc=LINES[line]
    mask=loc.index(a[i])^loc.index(b[i])
    return {'line':line,'slot':mask-1,'mask':mask,'hamming':mask.bit_count(),
        'hierarchy_coordinate':i,'interchild':i<len(a)-1}

def edge_loss(info,failed=(),uniform_mzi_db=.2,base_cross_db=.1):
    if info['line'] in failed:return math.inf
    # Explicitly assumed per-stage loss + hypothetical nonuniform line/mask penalty.
    # This is NOT a measured insertion loss; constant deterministic bias
    # makes constrained shortest paths genuinely comparable.
    return 2*uniform_mzi_db+base_cross_db+.025*(info['line']%7)+.08*(info['mask']==3)+(.1 if info['interchild'] else 0)

def route_opt(start,finish,*,failed=(),frame_target=None,slot_penalty=0.,
              max_depth=2,uniform_mzi_db=.2):
    """Dijkstra over (address, scalar frame) where coherent endpoint frames can be constrained."""
    start,finish=tuple(start),tuple(finish)
    if len(start)!=len(finish) or not 1<=len(start)<=max_depth:raise ValueError('invalid depth')
    if frame_target is not None and frame_target not in range(4):raise ValueError('frame target 0..3')
    initial=(start,0);pq=[(0.,0,initial)];dist={initial:0.};parents={}
    order=0;found=None
    while pq:
        cost,_,state=heapq.heappop(pq)
        if cost>dist[state]+1e-12:continue
        addr,frame=state
        if addr==finish and (frame_target is None or frame==frame_target):
            found=state;break
        for nb in linebus_neighbors(addr):
            info=edge_info(addr,nb)
            loss=edge_loss(info,failed,uniform_mzi_db=uniform_mzi_db)
            if not math.isfinite(loss):continue
            next_state=(nb,(frame+info['hamming'])%4)
            new=cost+loss+slot_penalty*info['slot']+.0001 # strictly positive weights
            if new+1e-12<dist.get(next_state,math.inf):
                dist[next_state]=new;parents[next_state]=state;order+=1
                heapq.heappush(pq,(new,order,next_state))
    if found is None:
        return {'reachable':False,'failed_line_buses':sorted(set(failed))}
    states=[found]
    while states[-1]!=initial:states.append(parents[states[-1]])
    states.reverse()
    path=[list(a) for a,_ in states]
    terms=[edge_info(a,b) for a,b in zip(path,path[1:])]
    insertion=sum(edge_loss(i,failed,uniform_mzi_db=uniform_mzi_db) for i in terms)
    return {'reachable':True,'path':path,'hops':len(terms),'loss_db':insertion,
       'conditional_path_survival':10**(-insertion/10),
       'frame_exponent':found[1],'frame_matches_constraint':frame_target is None or frame_target==found[1],
       'slot_histogram':{str(s):sum(i['slot']==s for i in terms) for s in range(3)},
       'faulted_buses':sorted(set(failed)),
       'optimization':'Dijkstra state=leaf address x Z4; scalar loss + synthetic slot penalty',
       'loss_provenance':'synthetic deterministic assumptions; not physical device data'}

def route_casebook():
    queries=[((0,0),(39,39)),((0,4),(7,22)),((12,17),(31,2))]
    cases=[]
    for a,b in queries:
        base=route_opt(a,b)
        framed=route_opt(a,b,frame_target=0)
        fail=route_opt(a,b,failed=(0,))
        cases.append({'start':a,'end':b,'loss_optimized':base,'frame_zero':framed,'bus0_failed':fail})
    return cases

def qutrit_bridge():
    w=np.exp(2j*math.pi/3)
    F=np.array([[w**(i*j) for j in range(3)] for i in range(3)],complex)/math.sqrt(3)
    target=np.eye(4,dtype=complex);target[:3,:3]=F
    assert np.linalg.norm(F.conj().T@F-np.eye(3))<1e-12
    leakage=[]
    for mask in range(4):
        P=permutation_matrix(mask).astype(complex)
        block=P[:3,:3]
        s=np.linalg.svd(block,compute_uv=False)
        per_basis=[float(np.linalg.norm(P[:3,j])**2) for j in range(3)]
        leakage.append({'mask':mask,'success_by_computational_basis':per_basis,
                       'mean_basis_survival':float(np.mean(per_basis)),
                       'worst_case_basis_survival':float(min(per_basis)),
                       'singular_values_qutrit_subblock':s.tolist(),
                       'distance_to_embedded_F3':float(np.linalg.norm(P-target))})
    # Complex Givens left-QR: each 2x2 G in SU(2) eliminates one entry.
    work=target.copy();gates=[]
    for col in range(4):
        for row in range(3,col,-1):
            x,y=work[row-1,col],work[row,col]
            if abs(y)<1e-12:continue
            rho=math.hypot(abs(x),abs(y))
            G=np.array([[np.conj(x)/rho,np.conj(y)/rho],
                        [-y/rho,x/rho]],dtype=complex)
            R=np.eye(4,dtype=complex)
            R[np.ix_([row-1,row],[row-1,row])]=G
            work=R@work
            gates.append({'modes':[row-1,row],'G_real':[[float(z.real) for z in q] for q in G],
                          'G_imag':[[float(z.imag) for z in q] for q in G]})
    diag=np.diag(work)
    assert np.linalg.norm(work-np.diag(diag))<1e-10
    reconstruction=np.diag(diag)
    for cell in reversed(gates):
        G=np.array(cell['G_real'])+1j*np.array(cell['G_imag'])
        R=np.eye(4,dtype=complex)
        R[np.ix_(cell['modes'],cell['modes'])]=G
        reconstruction=R.conj().T@reconstruction
    residual=float(np.linalg.norm(target-reconstruction))
    assert residual<1e-11 and len(gates)==3
    assert all(3 not in g['modes'] for g in gates)
    # Outside-box: all XOR switches can be diagonalized at once by H2 tensor H2.
    H=np.array([[1,1],[1,-1]],dtype=float)/math.sqrt(2)
    W=np.kron(H,H)
    walsh=[]
    for m in range(4):
        P=permutation_matrix(m)
        diagonal=W@P@W
        phases=[int(round(z)) for z in np.diag(diagonal)]
        err=float(np.linalg.norm(W@np.diag(phases)@W-P))
        assert err<1e-12 and np.linalg.norm(diagonal-np.diag(phases))<1e-12
        walsh.append({'mask':m,'diagonal_signs':phases,'reconstruction_residual':err})
    return {'qutrit_F3_real':F.real.tolist(),'qutrit_F3_imag':F.imag.tolist(),
       'embedded_4mode_gate':'diag(F3,1); auxiliary mode physically idle in gate core',
       'xor_projected_qutrit_leakage':leakage,
       'exact_givens_cell_count':len(gates),'givens':gates,
       'terminal_phase_rad':np.angle(diag).tolist(),'reconstruction_residual':residual,
       'walsh_alternative':{
           'identity':'P_mask=(H2 tensor H2) diag(two-bit Fourier characters) (H2 tensor H2)',
           'fixed_four_port_mixer_count':2,
           'dynamic_binary_phase_words':2,
           'mzi_equivalent_for_fixed_2level_H4_network':'8 static 50:50 couplers plus diagonal phase elements, not 4 tunable MZIs',
           'phase_tables':walsh,
           'tradeoff':'passive couplers vs active MZIs; real loss/crossings and power are unknown'},
       'separation':'the XOR bus is NOT a deterministic qutrit gate: for nonzero mask worst-case basis survival 0'}
def pdk_handoff():
    # Fail-closed technology-neutral optical port map. No gdsfactory/PDK on user host.
    nets=[]
    for bus in range(40):
        for c in cells(bus):
            nets.append({'device':c['cell_id'],'in':c['optical_input'],
               'out':c['optical_output'],'pair':c['pair'],
               'stage':c['stage'],'ctrl':c['control_word'],
               'electrode':c['physical_driver'],'process_cell':None,
               'physical_port_geometries':None,'optical_lengths_um':None})
    return {'status':'SCHEMATIC_ONLY',
       'gdsfactory_installed':False,
       'foundry_pdk_selected':False,
       'DRC_passed':False,'optical_LVS_passed':False,
       'foundry_tapeout_ready':False,
       '40bus_cell_count':160,'logical_control_words':80,
       'electrical_driver_allocations_resolved':0,
       'cells':nets,
       'required_fabrication_inputs':['PDK process selection and licenses','optical cells with complex S-parameters',
          'layer stack and min bend/crossing constraints','electrode/driver netlist and pads',
          '4-mode input-output ports and actual crossing routing',
          'process DRC deck and optical connectivity extraction','measured loss, phase bias and thermal crosstalk'],
       'script_binding':'Use these explicit ports/control IDs to lower into a foundry PDK; do not report a fabricated chip'}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,default=ROOT/'data/w33_fractal_all5_engineering_20261023.json')
    a=ap.parse_args()
    obj={'schema':'w33.fractal.all5.engineering.v1','status':'simulation and executable logic only',
      'tracks':{
        'foundry_port_handoff':pdk_handoff(),
        'two_arm_interference':measure_interference(),
        'loss_phase_fault_router':route_casebook(),
        'qutrit_processing_bridge':qutrit_bridge()},
      'outside_box':['Hadamard diagonalization of all 4 XOR states and static/dynamic tradeoff',
        'state-augmented shortest path on address x Z4',
        'qutrit leakage no-go for coordinate subspace under XOR-only switches']}
    s=json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)
    obj['sha256']=hashlib.sha256(s.encode()).hexdigest()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n')
    print('PASS all5',obj['sha256'],
       'gate_count',obj['tracks']['qutrit_processing_bridge']['exact_givens_cell_count'],
       'measurement',obj['tracks']['two_arm_interference']['estimated_phase_rad'],
       'paths',len(obj['tracks']['loss_phase_fault_router']))
if __name__=='__main__':main()
