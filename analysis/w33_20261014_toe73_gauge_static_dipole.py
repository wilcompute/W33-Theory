"""TOE73 static external-dipole response of the actual overlapping W33 gauge patch.

Two backgrounds: the native alternating Gauss charge and one nearest-
neighbor charge transfer b_a->b_a-1, b_b->b_b+1. Fermion number fixed 5;
mass term set to zero so changes are ONLY in Gauss-law background.
This is a finite-patch static source response, not confinement or a
thermodynamic screening length. Q row bounds use exact integer arithmetic.
"""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_two_octagon_covariance import patch,diagonalize,exact_gauss_electric

def source_patches():
    native=patch()
    charged={k:(v.copy() if isinstance(v,np.ndarray) else v)
             for k,v in native.items()}
    a,b=native["p_ed"][0]
    assert (native["background"][a],native["background"][b])==(1,0)
    charged["background"][a]-=1
    charged["background"][b]+=1
    assert (sum(charged["background"]),sum(native["background"]))==(5,5)
    return native,charged,[int(a),int(b)]

def exact_complement_row_bound(p,L=2):
    # H=0.32 sum E²+1.875, hopping magnitude .7, three magnetic
    # plaquettes each with +/- shift magnitude .3125. All integers in
    # units 1/2000. Q = integer pairs outside square |m1|,|m2|<=2.
    fock=[b for b in range(1<<11) if b.bit_count()==5]
    O=np.asarray([[(bits>>j)&1 for j in range(11)] for bits in fock],int)
    offsets=np.asarray([exact_gauss_electric(o,np.array([0,0]),p)
                        for o in O])
    basis=np.asarray([exact_gauss_electric(O[0],np.array(f),p)-offsets[0]
                      for f in ((1,0),(0,1))]).T
    chord={e:j for j,e in enumerate(p["chords"])}
    shifts=[tuple(int(x) for x in row) for row in p["P"][:,p["chords"]]]
    best=(10**15,None,None)
    for index,occ in enumerate(O):
        hop=[]
        for e,(a,b) in enumerate(p["p_ed"]):
            if occ[a]==occ[b]:continue
            d=[0,0]
            if e in chord:d[chord[e]]=-1 if occ[a] else 1
            hop.append(tuple(d))
        for f in itertools.product(range(-9,10),repeat=2):
            if max(abs(f[0]),abs(f[1]))<=L:continue
            E=offsets[index]+basis@np.asarray(f)
            diagonal=640*int(E@E)+3750
            hc=sum(max(abs(f[0]+dx),abs(f[1]+dy))>L for dx,dy in hop)
            mc=sum(max(abs(f[0]+s*dx),abs(f[1]+s*dy))>L
                   for dx,dy in shifts for s in (-1,1))
            row=diagonal-1400*hc-625*mc
            if row<best[0]:best=(int(row),tuple(f),int(fock[index]))
    tail=640*100+3750-1400*12-625*6
    assert tail==47200 and best[0]<tail
    # Chord fluxes are among E, so if |mi|>=10, E²>=100; bound holds
    # for *every* excluded state, independent of nearby occupations.
    return {"exact_Gershgorin_Q_lower_units_2000":best[0],
       "Q_lower":best[0]/2000,
       "minimum_attaining_flux":list(best[1]),
       "minimum_occupation_bitmask":best[2],
       "far_flux_tail_lower_units_2000":tail}

def certificate():
    neutral,dipole,link=source_patches()
    by_bg={}
    for label,p in (("native_background",neutral),("nearest_neighbor_dipole",dipole)):
        runs=[diagonalize(L,p,mass=0) for L in (1,2)]
        assert all(run["dimension"]==462*(2*run["L"]+1)**2 for run in runs)
        assert runs[1]["ground"]<=runs[0]["ground"]+1e-9
        assert all(z["numerical_ritz_residual"]<1e-7 for z in runs)
        by_bg[label]={"runs":runs,"omitted_flux_row_bound_L2":exact_complement_row_bound(p,L=2)}
    diff=[by_bg["nearest_neighbor_dipole"]["runs"][i]["ground"]
          -by_bg["native_background"]["runs"][i]["ground"] for i in range(2)]
    assert all(np.isfinite(diff))
    return {
       "status":"PASS_TOE73_NATIVE_TWO_LOOP_STATIC_DIPOLE",
       "native_patch_sites_links":[11,12],
       "fixed_fermion_number":5,
       "Gauss_nearest_neighbor_transfer_edge_local":0,
       "Gauss_transfer_site_indices":link,
       "total_background_charge_before_after":[5,5],
       "Hamiltonian_parameters":{"g":0.8,"kappa":0.7,"magnetic_beta":0.4,"mass":0},
       "backgrounds":by_bg,
       "dipole_minus_native_ground_energy_at_L1_L2":diff,
       "scope":"Exact Gauss-preserving source transfer and exact integer complementary Gershgorin bound, finite L=1,2 eigensolver responses. Because external b is changed, this is a finite static source energy difference; it is not a confinement potential, continuum screening, mass gap, or certified untruncated energy."}

if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe73_dipole_response.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],c["dipole_minus_native_ground_energy_at_L1_L2"])
