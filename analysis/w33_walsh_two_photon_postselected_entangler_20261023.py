#!/usr/bin/env python3
"""Two-photon, eight-rail PASSIVE linear-optical postselected qutrit entangler.

Four rails per Walsh qutrit. A single cross-bank directional coupler acts on
physical rail A0/B0. Two indistinguishable bosons transform by the permanent:
K[(a,b),(j,k)] = U[a,j]U[4+b,4+k]+U[a,4+k]U[4+b,j].
Postselect one photon in each 4-rail bank, then Walsh CODE subspace.
At theta=pi/2, a full physical rail exchange yields mathematical heralded
qutrit state entanglement negativity 1/4, code success probability 1/2,
and whole-bank coincidence probability 5/8 for one logical product input.

This is POSTSELECTED STATE GENERATION, NOT a deterministic or heralded
non-destructive composable CZ3 gate. Photon-number detection generally
destroys the photons; QND/heralded ancilla needed for downstream use.
No actual photon measurements or PIC layout of this coupler.
"""
import hashlib,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def encoder():
    H=np.array([[1,1],[1,-1]],dtype=float)/math.sqrt(2)
    return np.kron(H,H)[:,1:4]

def eight_mode_coupler(theta):
    U=np.eye(8,dtype=complex)
    c,s=math.cos(theta),math.sin(theta)
    U[0,0]=U[4,4]=c
    U[0,4]=U[4,0]=1j*s
    assert np.linalg.norm(U.conj().T@U-np.eye(8))<1e-12
    return U

def coincidence_kraus(U):
    K=np.zeros((16,16),complex)
    for a in range(4):
        for b in range(4):
            for j in range(4):
                for k in range(4):
                    K[4*a+b,4*j+k]=U[a,j]*U[4+b,4+k]+U[a,4+k]*U[4+b,j]
    return K

def state_stats(vec):
    p=float(np.vdot(vec,vec).real)
    if p<=0:raise ValueError('zero event')
    ψ=vec/np.sqrt(p)
    sing=np.linalg.svd(ψ.reshape(3,3),compute_uv=False)
    entropy=float(-sum(z*z*math.log2(z*z) for z in sing if z>1e-12))
    neg=float(((sum(sing))**2-1)/2)
    return {'probability':p,'schmidt_coefficients':sing.tolist(),
        'entanglement_entropy_bits':entropy,'partial_transpose_negativity':neg}

def scan():
    V=encoder()
    E=np.kron(V,V) # 16 physical two-bank coincidence modes, 9 logical inputs
    assert np.linalg.norm(E.conj().T@E-np.eye(9))<1e-12
    rows=[]
    for theta in (0,math.pi/8,math.pi/4,math.pi*3/8,math.pi/2):
        U=eight_mode_coupler(theta)
        K=coincidence_kraus(U)
        projected=E.conj().T@K@E
        input00=np.eye(9)[:,0]
        rail=E@input00
        full_bank_coincidence=float(np.linalg.norm(K@rail)**2)
        stats=state_stats(projected@input00)
        assert 0<=stats['probability']<=full_bank_coincidence+1e-12<=1+1e-12
        rows.append({'coupler_angle_rad':theta,
            'coherent_rail_coupling_power':math.sin(theta)**2,
            'whole_bank_coincidence_probability':full_bank_coincidence,
            'qutrit_code_postselected_success_probability':stats['probability'],
            'logical_input':'|Walsh logical 0> A tensor |Walsh logical 0> B',
            **{key:val for key,val in stats.items() if key!='probability'}})
    end=rows[-1]
    assert abs(end['whole_bank_coincidence_probability']-5/8)<1e-12
    assert abs(end['qutrit_code_postselected_success_probability']-.5)<1e-12
    assert abs(end['partial_transpose_negativity']-.25)<1e-12
    assert rows[0]['partial_transpose_negativity']<1e-12
    return {'schema':'w33.walsh.two_photon_postselected_beamsplitter_entangler.v1',
      'photon_count':2,'optical_rails':8,'Walsh_logical_qutrits':2,
      'physical_primitive':'cross-bank 2x2 directional coupler on rail A0 and rail B0',
      'mathematical_model':'indistinguishable bosonic creation operators; two-photon permanent, condition one photon per bank then each Walsh-qutrit code',
      'postselection':'destructive output-coincidence and code projections generally, not heralded nondemolition quantum gate',
      'angles':rows,
      'ideal_full_swap_end_state':end,
      'potential_significance':'Passive optical interference and postselection CAN entangle the two encoded Walsh qutrits as states without an optical Kerr nonlinearity.',
      'not_claimed':['composable deterministic CZ3','complete qutrit unitary gate','heralded QND source','fabricated coupler','measured entanglement','fault-tolerant operation'],
      'experiment_gates':['two indistinguishable single-photon sources each prepared in a four-rail Walsh character',
        'coherent cross-bank rail-A0/rail-B0 tunable beamsplitter',
        'resolve one photon in each output bank and project away uniform auxiliary Walsh modes',
        'two-qutrit coincidence tomography and source indistinguishability controls',
        'pre-registered entanglement witness with loss/accidental confidence bounds']}
if __name__=='__main__':
    x=scan()
    x['sha256']=hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    p=ROOT/'data/w33_walsh_two_photon_postselected_entangler_20261023.json'
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
    print('PASS two-photon passive entangled qutrit postselection',
        x['ideal_full_swap_end_state']['partial_transpose_negativity'],
        x['ideal_full_swap_end_state']['qutrit_code_postselected_success_probability'])
