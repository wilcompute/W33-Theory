#!/usr/bin/env python3
"""Idealized passive optical switch surrogate for W33 sparse four-lane Holonet.

Three output modes are selected by two ideal two-mode MZIs. Models coherent
linear-optical amplitudes and hypothetical attenuation/phase offsets.
NOT a foundry-verified cell, quantum process benchmark or 1550nm waveguide.
"""
from __future__ import annotations
import argparse,hashlib,json,math,random,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_four_lane_scheduler_20261023 import (
    ADJ,LINE,ANCHOR,COLOR,sparse_route,lane_for,color_for,build as schedule_build)

def mzi(theta):
    # H diag(exp(+i theta/2),exp(-i theta/2)) H: bar/cross power
    return np.array([[math.cos(theta/2),1j*math.sin(theta/2)],
                     [1j*math.sin(theta/2),math.cos(theta/2)]],dtype=complex)

def embed(coupler,i,j):
    x=np.eye(3,dtype=complex)
    x[np.ix_((i,j),(i,j))]=coupler
    return x

def tree_transfer(port:int,phase_error_rad=0.0,mzi_loss_db=0.0):
    """3x3 scattering surrogate and one-source 3-output power/readout.

    Port 0 traverses one MZI, port 1/2 traverse two.
    A represents first split (modes 0,1); B splits branch (1,2).
    """
    if port not in (0,1,2):raise ValueError('port 0,1,2')
    if mzi_loss_db<0:raise ValueError('loss cannot be negative')
    err=float(phase_error_rad)
    angle_A=(0 if port==0 else math.pi)+err
    angle_B=(math.pi if port==2 else 0)+err
    A=embed(mzi(angle_A),0,1)
    B=embed(mzi(angle_B),1,2)
    U=B@A
    assert np.linalg.norm(U.conj().T@U-np.eye(3))<1e-12
    amp=10**(-mzi_loss_db/20)
    attenuation_A=np.diag([amp,amp,1.0])
    attenuation_B=np.diag([1.0,amp,amp])
    T=attenuation_B@B@attenuation_A@A
    power=np.abs(T[:,0])**2
    assert 0<=power.sum()<=1+1e-12
    return {'chosen_port':port,'powers':[float(p) for p in power],
       'target_probability':float(power[port]),
       'wrong_port_probability':float(sum(power)-power[port]),
       'absorbed_probability':float(1-sum(power)),
       'unitary_surrogate_residual':float(np.linalg.norm(U.conj().T@U-np.eye(3)))}

def single_link_budget(slot:int,phase_error_rad=0.0,mzi_loss_db=0.2,link_loss_db=0.1):
    if slot not in (0,1,2):raise ValueError('slot')
    if link_loss_db<0:raise ValueError('link loss')
    # Two endpoint switches are assumed reciprocal and equal here, which
    # remains a physical-design hypothesis, not an LVS/S-parameter fact.
    endpoint=tree_transfer(slot,phase_error_rad,mzi_loss_db)
    selected=(endpoint['target_probability']**2)*10**(-link_loss_db/10)
    return {'slot':slot,'switch_mzi_stages_across_both_endpoints':2 if slot==0 else 4,
      'correct_link_power_probability':selected,
      'selected_link_loss_db':-10*math.log10(max(selected,1e-300)),
      'one_endpoint':endpoint,
      'assumptions':'Two identical reciprocal selections, one isolated input, ideal H couplers; no time-guard, bends, polarization, layout or detector loss'}

def route_budget(path,mzi_loss_db=0.2,link_loss_db=0.1,local_hop_db=0.05,phase_error_rad=0.0):
    if any(x<0 for x in (mzi_loss_db,link_loss_db,local_hop_db)):raise ValueError('negative loss')
    kinds={'local_hops':0,'interchild_hops':0,'switch_cells_traversed':0,
           'interchild_slots':{0:0,1:0,2:0}}
    total_db=0.0
    for a,b in zip(path,path[1:]):
        i=next(k for k,(x,y) in enumerate(zip(a,b)) if x!=y)
        if i==len(a)-1:
            kinds['local_hops']+=1
            total_db+=local_hop_db
        else:
            slot=color_for(a[i],b[i])//4
            kinds['interchild_hops']+=1
            kinds['interchild_slots'][slot]+=1
            link=single_link_budget(slot,phase_error_rad,mzi_loss_db,link_loss_db)
            total_db+=link['selected_link_loss_db']
            kinds['switch_cells_traversed']+=link['switch_mzi_stages_across_both_endpoints']
    return {'hops':len(path)-1,'selected_path_survival':10**(-total_db/10),
        'selected_path_loss_db':total_db,**kinds}

def build(depth=3,losses=(0.2,0.1,0.05),phase_error_rad=0.05):
    rng=random.Random(20261023)
    traces=[]
    for j in range(20):
        a=tuple(rng.randrange(40) for _ in range(depth))
        b=tuple(rng.randrange(40) for _ in range(depth))
        route=sparse_route(a,b)
        estimate=route_budget(route,*losses,phase_error_rad=phase_error_rad)
        traces.append({'origin':a,'destination':b,'route_length':len(route)-1,
                       'loss_surrogate':estimate})
    vals=[t['loss_surrogate']['selected_path_loss_db'] for t in traces]
    out={'schema':'w33.fractal.optical_switch_surrogate.v1',
      'status':'HYPOTHETICAL optical switch and link loss model; no measured or PDK-validated parameters',
      'source':'analysis/w33_fractal_four_lane_scheduler_20261023.py',
      'depth':depth,'assumptions':{
         'ideal_two_coupler_MZI_transfer':'H diag(exp(+i theta/2),exp(-i theta/2)) H',
         'mzi_insertion_loss_db':losses[0],'one_interchild_link_loss_db':losses[1],
         'one_local_graph_hop_db':losses[2],'equal_phase_error_rad_per_MZI':phase_error_rad,
         'tree':'one root MZI followed by a second MZI on one branch',
         'network_physics':'no coherent multi-path, SPAM, timing, nonlinearities, contention, mode mismatch or feed-forward included'},
      'three_ports':[tree_transfer(p,phase_error_rad,losses[0]) for p in range(3)],
      'link_choices':[single_link_budget(s,phase_error_rad,losses[0],losses[1]) for s in range(3)],
      'paths':traces,
      'path_loss_db_summary':{'minimum':min(vals),'maximum':max(vals),'mean':sum(vals)/len(vals)},
      'evidence_boundary':['graph schedule exact','3x3 lossless U unitary numerical',
                           'selected-power estimates hypothetical; not quantum process fidelity',
                           'no foundry device nor routing layout']}
    canonical=json.dumps(out,sort_keys=True,separators=(',',':'))
    out['sha256']=hashlib.sha256(canonical.encode()).hexdigest()
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--depth',type=int,default=3)
    ap.add_argument('--out',type=Path,default=ROOT/'data/w33_fractal_optical_switch_budget_20261023.json')
    ap.add_argument('--mzi-loss-db',type=float,default=0.2)
    ap.add_argument('--link-loss-db',type=float,default=0.1)
    ap.add_argument('--local-hop-db',type=float,default=0.05)
    ap.add_argument('--phase-error-rad',type=float,default=0.05)
    a=ap.parse_args()
    obj=build(a.depth,(a.mzi_loss_db,a.link_loss_db,a.local_hop_db),a.phase_error_rad)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n')
    print('PASS optical surrogate',obj['path_loss_db_summary'],obj['sha256'])
