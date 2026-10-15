"""TOE94 Witting 13-point polar boundary as a typed erasure guard.

Distinguished isotropic point gives W33 27 affine +13 polar.
Enumerate 40 tetrads by polar count, H27 boundary orbits,
all 480 detector substitution events by typed affine/polar source and
destination. Gate a partial affine H27 chain-channel only on AA events.
"""
from __future__ import annotations
import json,collections
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from analysis.w33_20261015_toe93_affine_H27_chain import graph,construct_dst
from analysis.w33_20261015_toe86_geometry_integral_routing import H
from tools.bt1408_witting_contextual_communication_bridge import construct_witting_40_rays,find_tetrads
def certificate():
    points,address,aa,ap,pp,mapping=graph()
    A=set(address);P=set(range(40))-A
    rays=construct_witting_40_rays()
    inv={ray:p for ray,p in mapping.items()}
    T=[tuple(inv[i] for i in b) for b in find_tetrads(rays)]
    assert len(T)==40
    signature=collections.Counter(len(set(t)&P) for t in T)
    assert sum(signature.values())==40
    orbits=[]; unseen=set(P)
    while unseen:
        point=min(unseen)
        orbit={construct_dst(points,point,g) for g in H}
        assert orbit<=P
        orbits.append(sorted(orbit))
        unseen-=orbit
    orbits.sort(key=lambda s:(len(s),s))
    groups=collections.Counter()
    for t in T:
        for a in t:
            for b in t:
                if a==b:continue
                src='affine' if a in A else 'polar'
                dst='affine' if b in A else 'polar'
                groups[src+'->'+dst]+=1
    assert sum(groups.values())==480
    assert groups=={'affine->affine':216,'affine->polar':108,'polar->affine':108,'polar->polar':48}
    assert signature=={1:36,4:4}
    assert sorted(map(len,orbits))==[1,3,3,3,3]
    # The observed outcome channel is typed: AA edges translate via
    # TOE93 F1; all other events emit erasure+public basis/slot flag.
    guarded=groups['affine->affine']/480
    assert guarded==.45
    p_aff=27/40
    # For maximally mixed state and uniformly random basis, each ray
    # occurs in exactly 4 tetrads, hence 13/40 polar clicks.
    counts=collections.Counter(x for t in T for x in t)
    assert all(n==4 for n in counts.values()) and len(counts)==40
    hub=next(i for i,p in enumerate(points) if p==(1,0,0,0))
    assert hub in P
    hub_bases=sum(hub in t for t in T)
    assert hub_bases==4
    return {'space_decomposition':{'affine':27,'polar_guard':13},
      'polar_H27_orbit_sizes':sorted(map(len,orbits)),
      'polar_H27_orbits_symplectic_indices':orbits,
      'tetrad_count_by_polar_membership':{str(k):v for k,v in sorted(signature.items())},
      'one_polar_three_affine_bases':36,'four_polar_zero_affine_bases':4,
      'directed_detector_event_types':dict(sorted(groups.items())),
      'typed_accepted_affine_affine_events':216,'typed_erasure_detector_events':264,
      'directed_event_admission_fraction':guarded,
      'maximally_mixed_single_ray_affine_probability':p_aff,
      'maximally_mixed_single_ray_polar_erasure_probability':13/40,
      'all_polar_tetrad_setting_fraction':4/40,
      'H27_fixed_polar_hub':hub,
      'guard_algorithm':'Given trusted tetrad and source/destination ray slots, mark affine->affine as graph-chain transferable and all other substitutions as typed erasures; do not pretend the erased 264 events yield physical H27 CSS syndromes.',
      'interpretation':'Finite-geometric sector guard only. Conditional acceptance is basis/outcome dependent, so cannot be substituted into unqualified QKD security or a postselected entanglement witness.'}
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261015_toe94_polar_guard.json').write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
 print('POLAR94',d['polar_H27_orbit_sizes'],d['tetrad_count_by_polar_membership'],d['directed_detector_event_types'],flush=True)
