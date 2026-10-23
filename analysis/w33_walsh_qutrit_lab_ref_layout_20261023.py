#!/usr/bin/env python3
"""Process-neutral 4-rail Walsh-qutrit experiment PIC floorplan and optical S target.

The GDS contains STRAIGHT RAILS plus SYMBOLIC component keep-outs,
NOT functional couplers, electrodes, optical S-matrix or foundry DRC/LVS.
The 3-cycle and F3 blocks are NOT implemented as waveguide layouts.
"""
import argparse,hashlib,json,math,os,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pic_xor_walsh_pareto_20261023 import H4
from w33_walsh_qutrit_s4_affine_bridge_20261023 import four_rail_perm
from w33_fractal_linebus_switch_matrix_20261023 import permutation_matrix

def gds_module():
    loc=os.environ.get('W33_GDSTK_PATH')
    if loc and loc not in sys.path:sys.path.insert(0,loc)
    import gdstk
    return gdstk

def optical_target(mask=0,rail_threecycle=False):
    W=H4().astype(complex)
    w=np.exp(2j*math.pi/3)
    F=np.array([[w**(i*j) for j in range(3)] for i in range(3)],complex)/math.sqrt(3)
    core=np.eye(4,dtype=complex)
    core[1:4,1:4]=F
    Uenc=W@core@W
    G=four_rail_perm([0,2,3,1]) if rail_threecycle else np.eye(4)
    P=permutation_matrix(mask).astype(complex)
    total=W@Uenc@G@P@W
    assert np.linalg.norm(total.conj().T@total-np.eye(4))<1e-12
    assert np.linalg.norm(total[:1,1:])<1e-12
    assert np.linalg.norm(total[1:,:1])<1e-12
    assert abs(total[0,0]-1)<1e-12
    return total

def make(out_dir):
    gdstk=gds_module()
    out_dir.mkdir(parents=True,exist_ok=True)
    lib=gdstk.Library(unit=1e-6,precision=1e-9)
    cell=lib.new_cell('W33_WALSH_QUTRIT_LAB_REF')
    width,pitch,length=.5,20.,850.
    for i in range(4):
        y=i*pitch
        cell.add(gdstk.rectangle((0,y-width/2),(length,y+width/2),layer=1))
        cell.add(gdstk.Label('OPT_IN_'+str(i),(0,y+2),layer=60))
        cell.add(gdstk.Label(('AUX0' if i==0 else 'QUTRIT'+str(i))+'_OUT',(length-90,y+3),layer=60))
        cell.add(gdstk.rectangle((18,y+2),(46,y+7),layer=20))
        cell.add(gdstk.Label('PHASECAL'+str(i),(18,y+11),layer=61))
    stages=[
      {'block':'WALSH_ENCODER','x0':72,'x1':154,'requires':'H2 tensor H2 4-mode couplers'},
      {'block':'XOR_V4_SWITCH','x0':184,'x1':282,'requires':'four tunable MZI or two fixed Walsh mixers and phase bank'},
      {'block':'S4_RAIL_3CYCLE','x0':320,'x1':430,'requires':'additional two rail swaps; not a V4 mode'},
      {'block':'ENCODED_F3','x0':474,'x1':635,'requires':'W diag(1,F3) W; 3 Givens plus phases within 3-mode tile'},
      {'block':'WALSH_DECODER','x0':685,'x1':760,'requires':'H2 tensor H2; aux monitoring'}]
    for i,b in enumerate(stages):
        # 99 means SPECIFICATION ONLY: NOT TECHNOLOGY-COMPLIANT LAYOUT.
        cell.add(gdstk.rectangle((b['x0'],-8),(b['x1'],68),layer=99))
        cell.add(gdstk.Label(b['block'],(b['x0']+1,66),layer=61))
    lib.write_gds(str(out_dir/'w33_walsh_qutrit_lab_ref_20261023.gds'))
    cell.write_svg(str(out_dir/'w33_walsh_qutrit_lab_ref_20261023.svg'))
    rec=gdstk.read_gds(str(out_dir/'w33_walsh_qutrit_lab_ref_20261023.gds'))
    assert rec.cells[0].name==cell.name
    assert len(rec.cells[0].polygons)>=13
    spectra=[]
    for mask in range(4):
        for cycle in (False,True):
            U=optical_target(mask,cycle)
            spectra.append({'xor_mask':mask,'rail_threecycle':cycle,
               'decoded_aux_coherence_loss_exact':float(np.linalg.norm(U[0,1:])),
               'decoded_qutrit_unitarity_residual':float(np.linalg.norm(U[1:,1:].conj().T@U[1:,1:]-np.eye(3)))})
    gds=out_dir/'w33_walsh_qutrit_lab_ref_20261023.gds'
    return {'schema':'w33.walsh.qutrit.lab_ref_layout.v1',
      'gds_relative_path':str(gds.relative_to(ROOT) if gds.is_relative_to(ROOT) else gds).replace('\\','/'),
      'gds_bytes':gds.stat().st_size,'gds_sha256':hashlib.sha256(gds.read_bytes()).hexdigest(),
      'cell_name':cell.name,'optical_input_modes':4,'optical_output_modes':4,
      'rail_pitch_um':pitch,'reference_width_um':width,'device_length_um':length,
      'stages':stages,'numerical_unitary_targets':spectra,
      'layer_99':'SYMBOLIC BLOCK. No physical optical coupling implemented.',
      'photonic_nets_status':'SCHEMATIC_NOT_CONNECTED_FUNCTIONALLY',
      'PDK_selected':False,'DRC_passed':False,'LVS_passed':False,'tapeout_ready':False,
      'experimental_aux_port':'output rail 0 after Walsh decoder (uniform character)',
      'necessary_next_steps':['choose licensed PDK and process wavelength/polarization',
         'replace each symbolic marker with optical compact-model backed MZI/directional coupler/crossing/cavity devices',
         'physically route 3-cycle and 3-Givens F3 network',
         'electrode driver/pad and thermal cross-talk extraction',
         'calibrate all 4x4 complex S matrices over wavelength and temperature',
         'foundry DRC/LVS and post-fabrication auxiliary leakage/tomography']}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--outdir',type=Path,default=ROOT/'hardware/generated')
    args=p.parse_args()
    obj=make(args.outdir)
    dst=ROOT/'data/w33_walsh_qutrit_lab_ref_layout_20261023.json'
    dst.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
    print('PASS GDS four-rail lab reference',obj['gds_bytes'],'B, 8 unitary targets; NOT PDK')
