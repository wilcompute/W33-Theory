#!/usr/bin/env python3
"""W33 40-bus PIC reference GDS and XOR-vs-Walsh S-matrix tradeoff.

REF geometry uses generic layers and symbolic MZI/coupler footprints. It is
NOT a connected, PDK-qualified photonic design: the stage-2 0<->2 and 1<->3
couplings are flagged UNROUTED, and no DRC, LVS or tapeout claim is made.
"""
from __future__ import annotations
import argparse,hashlib,json,math,os,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_linebus_switch_matrix_20261023 import permutation_matrix

def gp():
    hint=os.environ.get('W33_GDSTK_PATH')
    if hint and hint not in sys.path:sys.path.insert(0,hint)
    import gdstk
    return gdstk

def H4():
    h=np.array([[1,1],[1,-1]],float)/math.sqrt(2)
    return np.kron(h,h)

def target(mask):
    if mask not in range(4):raise ValueError('mask')
    return permutation_matrix(mask).astype(complex)

def walsh_target(mask,phase_errors=None):
    """Fixed Walsh interferometers around a four-point signed phase mask."""
    W=H4()
    eps=np.zeros(4) if phase_errors is None else np.asarray(phase_errors,dtype=float)
    if eps.shape!=(4,):raise ValueError('four diagonal errors')
    signs=np.array([(-1)**(int(s&mask).bit_count()) for s in range(4)],complex)
    U=W@np.diag(signs*np.exp(1j*eps))@W
    return U

def xor_target(mask,angle_errors=None):
    from w33_linebus_xor2_photonic_compiler_20261023 import design
    e=np.zeros(4) if angle_errors is None else np.asarray(angle_errors,dtype=float)
    return design(mask,phase_errors=e)['compensated_U']

def gate_score(U,P):
    ov=abs(np.trace(P.conj().T@U))**2/16.
    basis=np.abs(U)**2
    good=[float(basis[np.argmax(abs(P[:,i])),i]) for i in range(4)]
    return {'unitary_process_overlap':float(ov),
      'minimum_basis_correct_power':min(good),
      'average_basis_correct_power':float(np.mean(good)),
      'worst_input_wrong_port_power':float(max(1-z for z in good))}

def monte_carlo(seed=301023,draws=400,phase_sigma=.06):
    rng=np.random.default_rng(seed)
    if draws<1 or phase_sigma<0:raise ValueError('parameters')
    summary={}
    for family,fn in [('four_MZI_XOR',xor_target),('fixed_Walsh_binary_phase',walsh_target)]:
        fidelities=[];minport=[];leak=[]
        for mask in range(4):
            ideal=fn(mask)
            assert np.linalg.norm(ideal-target(mask))<1e-12
            for _ in range(draws):
                err=rng.normal(0,phase_sigma,4)
                score=gate_score(fn(mask,err),target(mask))
                fidelities.append(score['unitary_process_overlap'])
                minport.append(score['minimum_basis_correct_power'])
                leak.append(score['worst_input_wrong_port_power'])
        summary[family]={
            'mean_unitary_overlap':float(np.mean(fidelities)),
            'p05_unitary_overlap':float(np.quantile(fidelities,.05)),
            'min_unitary_overlap':float(min(fidelities)),
            'mean_worst_port_wrong_probability':float(np.mean(leak)),
            'p95_worst_port_wrong_probability':float(np.quantile(leak,.95)),
            'sample_count':len(fidelities)}
    return summary

def device_loss_scenarios():
    # Hypothetical only; do not misrepresent these as published/measured PDK.
    samples=[
      {'label':'low passive coupling loss hypothetical','mzi_db':.2,
       'passive_coupler_db':.05,'binary_phase_db':.15,'routing_cross_db':.10},
      {'label':'high passive coupling loss hypothetical','mzi_db':.2,
       'passive_coupler_db':.15,'binary_phase_db':.15,'routing_cross_db':.10},
      {'label':'high active MZI loss hypothetical','mzi_db':.45,
       'passive_coupler_db':.05,'binary_phase_db':.15,'routing_cross_db':.10}]
    for x in samples:
        # XOR: two active MZI passes. Walsh: two H4s, each two splitter layers.
        x['xor_selected_path_db']=2*x['mzi_db']+x['routing_cross_db']
        x['walsh_selected_path_db']=4*x['passive_coupler_db']+x['binary_phase_db']+x['routing_cross_db']
        x['preferred_by_simple_path_loss']='Walsh' if x['walsh_selected_path_db']<x['xor_selected_path_db'] else 'XOR'
        x['warning']='no actual compact models, fabricated footprint, waveguide crossings or driver cost'
    return samples

def make_layout(gds_path,svg_path):
    gdstk=gp()
    lib=gdstk.Library(unit=1e-6,precision=1e-9)
    wg_layer,dev_layer,heater_layer,unrouted_layer=1,10,20,99
    pitch=20.; width=.5
    mzi=gdstk.Cell('W33_FOUR_MZI_SYMBOL')
    walsh=gdstk.Cell('W33_WALSH_SYMBOL')
    # Straight waveguide rails are REAL polygons but only form a schematic
    # connectivity skeleton. Coupling volumes are marked in a DIFFERENT layer.
    for cell in (mzi,walsh):
        for k in range(4):
            y=k*pitch
            cell.add(gdstk.rectangle((0,y-width/2),(450,y+width/2),layer=wg_layer))
            cell.add(gdstk.Label(f'IN{k}',(0,y),layer=50))
            cell.add(gdstk.Label(f'OUT{k}',(450,y),layer=50))
    symbolic_mzi=[]
    for stage,(x,pairs) in enumerate(((95.,((0,1),(2,3))),(310.,((0,2),(1,3))))):
        for j,(a,b) in enumerate(pairs):
            lo,hi=a*pitch,b*pitch
            mzi.add(gdstk.rectangle((x,lo-2),(x+65,hi+2),layer=dev_layer))
            mzi.add(gdstk.rectangle((x+18,lo+3),(x+53,lo+6),layer=heater_layer))
            mzi.add(gdstk.Label(f'MZI_S{stage}_{j}_PAIR_{a}{b}',(x+1,lo+9),layer=51))
            if stage==1:
                mzi.add(gdstk.rectangle((x-4,lo-3),(x+69,hi+3),layer=unrouted_layer))
            symbolic_mzi.append({'stage':stage,'index':j,'modes':[a,b],'x_um':x,'needs_real_coupler':True,'unrouted':stage==1})
    # Walsh design: two H4 interferometers: each has four static
    # balanced 2x2 couplers (eight total). Phase bank between the mixers.
    static_couplers=[]
    for block,x0 in enumerate((65.,305.)):
        for layerpair,pairs in enumerate((((0,1),(2,3)),((0,2),(1,3)))):
            for j,(a,b) in enumerate(pairs):
                x=x0+layerpair*58
                walsh.add(gdstk.rectangle((x,a*pitch-2),(x+30,b*pitch+2),layer=dev_layer))
                if layerpair==1:
                    walsh.add(gdstk.rectangle((x-3,a*pitch-3),(x+33,b*pitch+3),layer=unrouted_layer))
                static_couplers.append({'block':block,'layer':layerpair,'pair':[a,b]})
    for k in range(4):
        walsh.add(gdstk.rectangle((227,k*pitch+3),(273,k*pitch+6),layer=heater_layer))
    top=gdstk.Cell('W33_40BUS_PHOTONIC_REF')
    for k in range(40):
        y=100*(k%10);x=550*(k//10)
        top.add(gdstk.Reference(mzi,(x,y)))
        top.add(gdstk.Label(f'BUS_{k:02d}',(x+5,y-7),layer=51))
    # Single Walsh comparator macro placed beside four banks.
    top.add(gdstk.Reference(walsh,(2350,0)))
    lib.add(mzi,walsh,top)
    gds_path.parent.mkdir(parents=True,exist_ok=True)
    lib.write_gds(str(gds_path))
    top.write_svg(str(svg_path))
    read=gdstk.read_gds(str(gds_path))
    loaded={c.name:c for c in read.cells}
    assert len([ref for ref in loaded['W33_40BUS_PHOTONIC_REF'].references
                if ref.cell.name=='W33_FOUR_MZI_SYMBOL'])==40
    assert len(symbolic_mzi)==4 and len(static_couplers)==8
    return {'gds_path':str(gds_path),
        'svg_path':str(svg_path),
        'gds_size_bytes':gds_path.stat().st_size,
        'gds_sha256':hashlib.sha256(gds_path.read_bytes()).hexdigest(),
        'cell_names':sorted(loaded),
        'forty_macro_references':40,'one_walsh_comparator_reference':1,
        'symbolic_mzi_per_bus':4,'symbolic_mzi_total':160,
        'symbolic_passive_couplers_per_walsh':8,
        'gds_layers':{'waveguide_rails':wg_layer,'symbolic_couplers':dev_layer,
                      'symbolic_heaters':heater_layer,
                      'UNROUTED_STAGE2_MARKERS':unrouted_layer},
        'port_pitch_um':pitch,'waveguide_width_um':width,
        'unrouted_second_stage_pairs':[[0,2],[1,3]],
        'status':'GDS_READBACK_PASSED; OPTICAL_NETLIST_INCOMPLETE; DRC_LVS_NOT_RUN',
        'pdk':'NONE; technology-neutral geometry only'}
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--gds',type=Path,default=ROOT/'hardware/generated/w33_40bus_switch_ref_20261023.gds')
    p.add_argument('--svg',type=Path,default=ROOT/'hardware/generated/w33_40bus_switch_ref_20261023.svg')
    p.add_argument('--out',type=Path,default=ROOT/'data/w33_pic_xor_walsh_pareto_20261023.json')
    a=p.parse_args()
    proof={'schema':'w33.fractal.pic_xor_walsh_reference.v1','physics':'ideal lossless MZI and Walsh unitary targets',
           'independent_errors':{'phase_sigma_rad':.06,'draws_per_mask':400},
           'monte_carlo':monte_carlo(),'loss_scenarios':device_loss_scenarios(),
           'layout':make_layout(a.gds,a.svg),
           'fabrication_gate':['choose licensed real PDK','construct actual crossed second-stage coupling and waveguide bends',
              'instantiate real directional couplers, physical phase shifters and electrode contacts',
              'verify complex S-parameters at wavelength and polarization',
              'run foundry DRC/LVS and packaging/optical port extraction']}
    canonical=json.dumps(proof,sort_keys=True,separators=(',',':'))
    proof['sha256']=hashlib.sha256(canonical.encode()).hexdigest()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(proof,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
    print('PASS GDS',proof['layout']['gds_size_bytes'],
      'PCR',[(x['label'],x['preferred_by_simple_path_loss']) for x in proof['loss_scenarios']],
      'sha256',proof['sha256'])
if __name__=='__main__':main()
