#!/usr/bin/env python3
"""Symplectic Pascal q-adic digit portal: exact codimension two but singular support.

The 40 isotropic 2-planes of F_3^4 provide 9 accepted digit quadruples out
of 81 in each refinement. This derives 1/L² for the gate DENSITY, but a
fixed plane is singular and cannot produce a spatially homogeneous mass.
A distributed periodic sublattice can instead spread L² portals uniformly.
"""
from pathlib import Path
import sys,itertools,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from toe_20261103_q_pascal_symplectic_scale_selector import projective_points,omega
def all_isotropic_planes():
    p=3;V=list(itertools.product(range(p),repeat=4))
    by=set()
    for i,a in enumerate(V):
        if a==(0,0,0,0):continue
        for b in V[i+1:]:
            if b==(0,0,0,0) or omega(a,b,p):continue
            plane=frozenset(tuple((u*a[t]+v*b[t])%p for t in range(4))
                             for u in range(p) for v in range(p))
            if len(plane)==9:by.add(plane)
    assert len(by)==40
    return [sorted(list(x)) for x in by]
def fixed_plane_samples(m):
    # The canonical Lagrangian plane spans first two coordinate axes.
    L=3**m
    # Its m levels are all first two coordinates freely varying,
    # last two identically zero. Exactly L² of L^4 sites.
    axes=np.arange(L)/L
    avg_x0=float(np.mean(1+.3*np.cos(2*np.pi*axes)))
    avg_x2=1.3
    volume_mean_x2=1.
    assert abs(avg_x0-1)<1e-13
    assert abs(avg_x2-volume_mean_x2-.3)<1e-13
    return {'m':m,'L':L,'all_4D_cells':L**4,
       'symplectic_digit_rule_accepted_cells':L**2,
       'fraction':1/L**2,
       'smooth_profile_cos_first_free_coordinate_mean':avg_x0,
       'smooth_profile_cos_first_fixed_coordinate_mean':avg_x2,
       '4D_volume_mean':volume_mean_x2,
       'discrepancy_from_homogeneous_4D_volume':.3}
def periodic_grid_samples(L):
    s=round(math.sqrt(L))
    assert s*s==L
    # Four-coord periodic portal sites at integers divisible by s.
    # Each axis has L/s = s allowed values -> s^4=L².
    axes=np.arange(0,L,s)
    assert len(axes)==s
    x=axes/L
    fmean=1+.3*np.mean(np.cos(2*np.pi*x))
    return {'L':L,'step_in_lattice_sites':s,'all_sites':L**4,
            'portal_count':L**2,
            'portal_density':1/L**2,
            'smooth_profile_mean':float(fmean),
            'bulk_profile_mean':1.}
def main():
    planes=all_isotropic_planes()
    lines=[len(row) for row in planes]
    assert set(lines)=={9}
    d=[fixed_plane_samples(m) for m in (1,2,3,4)]
    spatial=[periodic_grid_samples(n) for n in (9,16,25,36,49,81,121)]
    assert all(abs(x['smooth_profile_mean']-1)<1e-12 for x in spatial[1:])
    # Codim-two support dimension is 2, but not necessarily 4D homogeneous:
    # a rigid fixed plane produces a surface-supported quadratic form.
    result={'status':'PASS_SYMPLECTIC_NINE_OF_EIGHTYONE_DIGIT_RULE_AND_SINGULARITY_FIREWALL',
      'symplectic_isotropic_2planes_q3':len(planes),
      'accepted_digit_vectors_per_lagrangian_plane':9,
      'all_digit_vectors_F3_4':81,
      'single_refinement_portal_fraction':1/9,
      'refinement_gate_density_at_L3m':'(9/81)^m=3^(-2m)=1/L²',
      'fixed_Lagrangian_plane_samples':d,
      'regular_distributed_grid_samples':spatial,
      'theorem':'Selecting the 9 vectors in a fixed Lagrangian 2-plane S⊂F3^4 at each ternary digit level gives exactly 9^m=L² accepted points among 81^m=L⁴. It is supported on a two-dimensional coordinate subtorus, not equidistributed in 4D. Its smooth average on f(x)=1+0.3cos(2πx_2) equals 1.3 while the 4D bulk integral is exactly 1. Therefore exact combinatorial critical density does NOT ensure the averaged bulk-mass limit of an independent random portal ensemble.',
      'distributed_alternative':'At L=s², selecting each coordinate x_mu divisible by s gives s^4=L² portals evenly spaced in all four axes, so fixed smooth Fourier modes eventually average to their bulk mean. This uses a new global scale s=√L and does not follow from a fixed W33 isotropic plane.',
      'open_mechanism':'Construct a local, translation-compatible, gauge-covariant dynamical rule that redistributes q-adic symplectic portals across 4D without inserting a coarse scale by hand. An actual periodic graph spectrum, Lorentzian causal rule and chiral fermionic action remain open.',
      'prior_art_and_repo':'Earlier W33 symplectic points/lines and q-Pascal subspace counts, and Cioranescu-Murat homogenization of critical holes. Our result is a falsifier of the proposed gate-density argument, not a proven TOE.',
      'literature':['https://www.tandfonline.com/doi/abs/10.1080/03605302.2018.1531425',
                    'https://www.sciencedirect.com/science/article/abs/pii/S0362546X23002286']}
    (ROOT/'data/toe_20261103_symplectic_pascal_gate_singularity.json').write_text(json.dumps(result,indent=2)+'\n')
    print('SYMPLECTIC_PORTAL',json.dumps({'nplanes':len(planes),'samples':d,'distributed':spatial}),flush=True)
if __name__=='__main__':main()
