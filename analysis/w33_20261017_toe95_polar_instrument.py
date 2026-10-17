"""TOE95 polar-sector flagged CPTP measurement instrument and exact frame law.

The 13 polar rays form a tight frame with one distinguished hub ray:
    sum_{r in polar} |r><r| = 4I_4 - 3|hub><hub|.
Uniformly selecting one of 40 tetrads gives the polar flag effect
Epolar=0.4 I_4 - 0.3 P_hub, eigenvalues [0.1,0.4,0.4,0.4].
The per-tetrad classical outcome+flag Kraus instrument is CPTP, but
entanglement-breaking; it is NOT a coherent quantum erasure decoder.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from analysis.w33_20261015_toe93_affine_H27_chain import graph,construct_dst
from analysis.w33_20261015_toe86_geometry_integral_routing import H
from tools.bt1408_witting_contextual_communication_bridge import (
    construct_witting_40_rays,find_tetrads)
ROOT=Path(__file__).resolve().parents[1]

def certificate():
    R=np.asarray(construct_witting_40_rays(),dtype=complex)
    tetrads=find_tetrads(list(R))
    points,address,_,_,_,ray_to_point=graph()
    affine=set(address)
    polar=[ray for ray,p in sorted(ray_to_point.items()) if p not in affine]
    hub_point=next(j for j,p in enumerate(points) if p==(1,0,0,0))
    hub_ray=next(ray for ray,p in ray_to_point.items() if p==hub_point)
    assert len(polar)==13 and hub_ray in polar and len(tetrads)==40
    I=np.eye(4,dtype=complex)
    proj=[np.outer(r,r.conj()) for r in R]
    Ph=proj[hub_ray]
    frame=sum((proj[i] for i in polar),np.zeros((4,4),complex))
    frame_law_residual=float(np.max(abs(frame-(4*I-3*Ph))))
    assert frame_law_residual<1e-12
    E=frame/10
    eig=np.linalg.eigvalsh(E)
    assert np.allclose(eig,[.1,.4,.4,.4],atol=1e-12)
    overlap=sorted(len(set(t)&set(polar)) for t in tetrads)
    assert overlap==[1]*36+[4]*4
    average=np.zeros((4,4),complex)
    max_completeness=0.
    max_output_offdiagonal=0.
    mix=I/4
    witness_densities=[mix,Ph,(I-Ph)/3]
    for b,t in enumerate(tetrads):
        completeness=np.zeros((4,4),complex)
        K=[]
        for slot,ray in enumerate(t):
            flag=int(ray in polar)
            k=np.zeros((8,4),complex)
            k[4*flag+slot,:]=R[ray].conj()
            assert np.max(abs(k.conj().T@k-proj[ray]))<1e-12
            completeness+=k.conj().T@k
            K.append(k)
            if flag:average+=proj[ray]/40
        max_completeness=max(max_completeness,float(np.max(abs(completeness-I))))
        for rho in witness_densities:
            rho_out=sum((k@rho@k.conj().T for k in K),np.zeros((8,8),complex))
            assert abs(np.trace(rho_out)-1)<1e-12
            assert np.linalg.eigvalsh(rho_out).min()>-1e-12
            max_output_offdiagonal=max(max_output_offdiagonal,float(
                np.max(abs(rho_out-np.diag(np.diag(rho_out))))))
    assert max_completeness<1e-12 and max_output_offdiagonal<1e-12
    assert np.max(abs(average-E))<1e-12
    orbits=[];unseen=set(points.index(points[p]) if False else p for p in range(40) if p not in affine)
    while unseen:
        p=min(unseen)
        orbit={construct_dst(points,p,g) for g in H}
        assert orbit<=unseen|set().union(*(set(o) for o in orbits))
        orbits.append(sorted(orbit))
        unseen-=orbit
    assert sorted(map(len,orbits))==[1,3,3,3,3]
    phub=float(np.real(np.trace(E@Ph)))
    pperp=float(np.real(np.trace(E@(I-Ph)/3)))
    pmix=float(np.real(np.trace(E@mix)))
    assert np.allclose([phub,pperp,pmix],[.1,.4,13/40],atol=1e-12)
    return {
      'tetrad_count':len(tetrads),'polar_ray_count':len(polar),
      'polar_ray_indices':polar,'fixed_hub_ray_index':hub_ray,
      'H27_orbit_sizes':sorted(map(len,orbits)),
      'polar_tetrad_membership_histogram':{'1':36,'4':4},
      'exact_polar_frame_identity':'sum_polar P_r = 4 I4 - 3 P_hub',
      'exact_averaged_polar_flag_effect':'Eflag = (4 I4 - 3 P_hub)/10',
      'polar_frame_law_max_residual':round(frame_law_residual,12),
      'flag_effect_eigenvalues':[round(float(x),12) for x in eig],
      'flag_probability_on_hub_state':round(phub,12),
      'flag_probability_on_uniform_hub_orthogonal_mixture':round(pperp,12),
      'flag_probability_on_maximally_mixed_ququart':round(pmix,12),
      'Kraus_completeness_max_residual_40_settings':round(max_completeness,12),
      'measured_outcome_flag_density_max_offdiagonal':round(max_output_offdiagonal,12),
      'instrument':'For a chosen tetrad b with four rays r_i, K_{b,i}=|slot=i,flag=is_polar(r_i)><r_i| as a map C4->C8. The four Kraus operators obey sum K†K=I. Separate Kraus outcomes give a diagonal classical result+flag state.',
      'physical_limit':'This is an exact trace-preserving and entanglement-breaking ququart measurement instrument, not an erasure-channel encoder, a quantum-preserving code, an H27 CSS stabilizer decoder, or quantum key security.',
      'security_consequence':'The polar flag probability depends on input state (10% hub vs 40% orthogonal); discarding flagged trials is not fair-sampling-neutral. Count flags and losses in the original event denominator.'
    }
if __name__=='__main__':
    z=certificate()
    print('TOE95 CPTP',z['flag_effect_eigenvalues'],z['flag_probability_on_maximally_mixed_ququart'])
    (ROOT/'data/w33_20261017_toe95_polar_instrument.json').write_text(json.dumps(z,sort_keys=True,indent=2)+'\n')
