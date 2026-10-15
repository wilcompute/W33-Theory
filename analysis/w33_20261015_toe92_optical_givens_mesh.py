"""TOE92 deterministic 40-setting ququart optical mesh compilation.

Complex 4x4 Givens QR eliminates each Witting analyzer to a
diagonal phase matrix. Freeze a compact per-basis circuit of two-mode
beam splitter operations and four terminal rail phases, with exact
reconstruction tests, not a hardware prototype or bill of materials.
"""
from __future__ import annotations
import math,json,collections,numpy as np
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from tools.bt1408_witting_contextual_communication_bridge import construct_witting_40_rays,find_tetrads
def decompose(U):
    a=np.array(U,dtype=complex).copy();steps=[]
    for j in range(3):
        for i in range(3,j,-1):
            x,y=a[i-1,j],a[i,j]
            if abs(y)<1e-10:continue
            r=math.hypot(abs(x),abs(y))
            G=np.array([[x.conjugate()/r,y.conjugate()/r],
                        [-y/r,x/r]],dtype=complex)
            a[[i-1,i],:]=G@a[[i-1,i],:]
            steps.append((i-1,i,G))
    assert np.max(abs(a-np.diag(np.diag(a))))<1e-10
    assert np.max(abs(abs(np.diag(a))-1))<1e-10
    reconstruction=np.diag(np.diag(a))
    for x,y,G in reversed(steps):
        replacement=np.eye(4,dtype=complex)
        replacement[np.ix_([x,y],[x,y])]=G.conj().T
        reconstruction=replacement@reconstruction
    assert np.max(abs(reconstruction-U))<1e-9
    return a,steps
def certificate():
    R=np.array(construct_witting_40_rays(),dtype=complex)
    B=[tuple(q) for q in find_tetrads(list(R))]
    circuits=[];prof=collections.Counter();worst=0.
    for bid,b in enumerate(B):
        U=R[list(b)].conj()
        diag,steps=decompose(U)
        recom=np.diag(np.diag(diag))
        depth=[0]*4
        seq=[]
        for x,y,g in steps:
            d=max(depth[x],depth[y])+1
            depth[x]=depth[y]=d
            seq.append({'rails':[x,y],
              'unitary_real':[[round(float(z.real),12) for z in row] for row in g],
              'unitary_imag':[[round(float(z.imag),12) for z in row] for row in g],
              'dagger_applied_on_reconstruction':True})
        for x,y,g in reversed(steps):
            embedding=np.eye(4,dtype=complex)
            embedding[np.ix_([x,y],[x,y])]=g.conj().T
            recom=embedding@recom
        err=float(np.max(abs(recom-U)))
        worst=max(worst,err)
        assert err<1e-9
        m=len(steps)
        prof[m]+=1
        assert m<=6 and max(depth)<=m
        circuits.append({'basis_index':bid,'rays':list(b),'two_mode_couplers':m,
         'coupler_operations':seq,
         'outgoing_diagonal_phase_rad':[round(float(np.angle(z)),12) for z in np.diag(diag)],
         'max_path_coupler_depth':max(depth),
         'max_U4_reconstruction_error':round(err,12)})
    # Shared programmable mesh can implement each setting with <=6 Givens
    # with settings switched; no need 40 separate 6-mixer chips.
    eta_component=.98; eta_det=.85
    worst_depth=max(c['max_path_coupler_depth'] for c in circuits)
    per_side=eta_det*eta_component**worst_depth
    ideal_two_side=per_side*per_side
    assert len(circuits)==40 and worst<1e-9
    print('OPTICAL',dict(prof),'max depth',worst_depth,'coincidence',ideal_two_side,flush=True)
    return {'meaning':'Four-mode lossless SU4/U4 analyzer decomposition via two-mode Givens elimination; phase calibration and component loss are design assumptions, not experimental data.',
     'basis_count':40,'rays_each':4,'total_preparation_bases':40,
     'Givens_coupler_counts':{str(k):v for k,v in sorted(prof.items())},
     'maximum_two_mode_couplers_per_setting':max(prof),
     'maximum_per_path_coupler_depth':worst_depth,
     'shared_reconfigurable_mesh_upper_bound_couplers':6,
     'per_side_loss_assumptions':{'each_coupler_intensity_transmission':eta_component,'photon_detector_efficiency':eta_det},
     'pessimistic_single_photon_survival_assuming_max_depth_each_side':round(per_side,12),
     'pessimistic_pair_coincidence_survival_ignoring_source_and_switch':round(ideal_two_side,12),
     'max_unitary_reconstruction_residual':round(worst,12),
     'circuits':circuits,
     'technical_limit':'Does not establish physical layout, absolute optical phase reference, number of MZI actuators, rail crosstalk, thermal settling, herald timing, entangled source or measured visibility.'}
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261015_toe92_optical_givens_mesh.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
