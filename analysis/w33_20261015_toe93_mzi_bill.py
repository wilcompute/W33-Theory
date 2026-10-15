"""TOE93: exact lossless Mach-Zehnder factorization of all 40 Witting analyzers.

Each complex SU(2) Givens uses two balanced couplers, a tunable
relative internal phase and diagonal rail phases. This is a circuit
bill of *ideal components*, NOT a vendor-qualified photonic layout.
"""
from __future__ import annotations
import json,math,collections
import numpy as np
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from analysis.w33_20261015_toe92_optical_givens_mesh import decompose
from tools.bt1408_witting_contextual_communication_bridge import construct_witting_40_rays,find_tetrads
H=np.array([[1,1],[1,-1]],complex)/math.sqrt(2)
def factor(U):
    a,b=U[0]
    theta=math.atan2(abs(b),abs(a))
    alpha=np.angle(a) if abs(a)>1e-10 else 0.0
    beta=np.angle(b) if abs(b)>1e-10 else alpha
    DL=np.diag(np.exp(1j*np.array([alpha,-beta])))
    DR=np.diag(np.exp(1j*np.array([0.,beta-alpha])))
    M=np.diag([1,1j])@H@np.diag(np.exp(1j*np.array([theta,-theta])))@H@np.diag([1,-1j])
    V=DL@M@DR
    assert np.max(abs(U-V))<1e-10
    return theta,[alpha,-beta],[0.,beta-alpha]
def certificate():
    R=np.array(construct_witting_40_rays(),complex)
    B=find_tetrads(list(R))
    designs=[];counts=collections.Counter();maxerr=0
    for bid,b in enumerate(B):
        U=R[list(b)].conj()
        diag,steps=decompose(U)
        mesh=np.diag(np.diag(diag))
        depth=[0]*4
        records=[]
        for x,y,G in steps:
            theta,l,r=factor(G)
            d=max(depth[x],depth[y])+1
            depth[x]=depth[y]=d
            records.append({'rails':[x,y],'internal_half_phase_rad':round(theta,12),
                'tunable_relative_phase_rad':round(2*theta,12),
                'left_rail_phases_rad':[round(float(i),12) for i in l],
                'right_rail_phases_rad':[round(float(i),12) for i in r],
                'balanced_50_50_couplers':2})
        for x,y,G in reversed(steps):
            block=np.eye(4,dtype=complex)
            block[np.ix_([x,y],[x,y])]=G.conj().T
            mesh=block@mesh
        err=float(np.max(abs(mesh-U)))
        assert err<1e-10
        maxerr=max(maxerr,err)
        counts[len(steps)]+=1
        designs.append({'basis_id':bid,'rays':list(b),'MZI_count':len(steps),
          'balanced_couplers_count':2*len(steps),'maximum_50_50_couplers_per_path':2*max(depth),
          'MZI_stages':records,'final_rail_phases_rad':[round(float(np.angle(v)),12) for v in np.diag(diag)]})
    depth=max(d['maximum_50_50_couplers_per_path'] for d in designs)
    # Assumptions, not measurements.
    coupler_T=.98;det_eff=.85;connector_T=.97
    perarm=connector_T*det_eff*coupler_T**depth
    return {'setting_count':40,'basis_MZI_counts':{str(i):n for i,n in sorted(counts.items())},
       'MZI_upper_per_setting':max(counts),'balanced_50_50_couplers_upper_per_setting':12,
       'worst_balanced_couplers_per_photon_path':depth,
       'theoretical_4mode_programmable_circuit':'Six two-port MZI positions with electronically tunable relative phase, local rail input/output phases, and four rail-resolved photon detectors per receiver',
       'phase_convention':'For G=[[a,b],[-b*,a*]], choose |a|=cos(theta),|b|=sin(theta), phases alpha=arg(a),beta=arg(b); G=D_left R(theta) D_right, R(theta)=diag(1,i) H diag(e^{i theta},e^{-i theta}) H diag(1,-i).',
       'perarm_loss_assumptions':{'balanced_coupler_intensity_transmission':coupler_T,'detector_efficiency':det_eff,'one_connector_transmission':connector_T},
       'pessimistic_per_arm_survival':round(perarm,12),
       'pessimistic_two_photon_survival':round(perarm**2,12),
       'all_40_reconstruction_error_max_rounded':round(maxerr,12),'basis_circuits':designs,
       'hardware_unknowns':'MZI switch insertion loss, tuning speed, OAM/polarization/time-bin conversion, source herald rate, detector dead time, calibrated joint-basis POVMs, alignment and classical authentication. These must be measured.'}
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261015_toe93_mzi_bill.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
 print('MZI',d['basis_MZI_counts'],d['pessimistic_two_photon_survival'])
