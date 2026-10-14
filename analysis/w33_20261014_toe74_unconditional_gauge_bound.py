"""TOE74 unconditional rational FULL unbounded native two-loop rotor E0 bracket.

All P Gershgorin bounds and 2-state Rayleigh variational upper estimates
use integer coefficients. The Q lower and interface Gram upper are
recomputed using TOE72's exhaustive exact-integer certificate. This
CERTIFIES a coarse ground-energy interval with NO numerical eigsh input.
It does NOT certify the ordered spectral gap or the previous 0.9228
conditional gap estimate.
"""
from __future__ import annotations
import itertools,json,sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_two_octagon_covariance import patch,exact_gauss_electric
from w33_20261014_toe72_gauge_gram_bound import certificate as exact_Q

def certificate():
    p=patch();Q=exact_Q()
    assert Q["rigorous_Q_spectral_lower"]==14.165
    assert Q["exact_KKT_max_abs_row_sum_integer"]==12822
    qlower=F(28330,2000)
    ksq=F(12822,6400)
    L=3
    fluxes=list(itertools.product(range(-L,L+1),repeat=2))
    flux_lookup=set(fluxes)
    shifts=[tuple(map(int,x)) for x in p["P"][:,p["chords"]]]
    chord={e:i for i,e in enumerate(p["chords"])}
    states=[x for x in range(1<<11) if x.bit_count()==5]
    # Identify exact lowest diagonal and exact lowest diagonal-minus
    # permitted P-space off-diagonal abs row sum.
    min_d=(10**30,None,None)
    min_row=(10**30,None,None)
    local={}
    for bits in states:
        occ=np.array([(bits>>j)&1 for j in range(11)])
        stagger=int((1-2*p["background"])@occ)
        hop_moves=[]
        for e,(a,b) in enumerate(p["p_ed"]):
            if occ[a]==occ[b]:continue
            s=1 if occ[a] else -1
            dx=[0,0]
            if e in chord:dx[chord[e]]=-s
            hop_moves.append((bits^(1<<a)^(1<<b),tuple(dx),1400))
        for flux in fluxes:
            electric=exact_gauss_electric(occ,np.array(flux),p)
            d=640*int(electric@electric)+600*stagger+3750
            if d<min_d[0]:min_d=(d,bits,flux)
            n_hops=sum(tuple(flux[j]+dx[j] for j in range(2)) in flux_lookup
                       for _,dx,_ in hop_moves)
            n_mag=sum(tuple(flux[j]+direction*dx[j] for j in range(2)) in flux_lookup
                      for dx in shifts for direction in (-1,1))
            row=d-1400*n_hops-625*n_mag
            if row<min_row[0]:min_row=(row,bits,flux)
            local[bits,flux]=d
    P_lower=F(min_row[0],2000)
    # Exact one- or two-basis variational Rayleigh upper, no Ritz assumptions.
    d0,bits0,f0=min_d
    occ=np.array([(bits0>>j)&1 for j in range(11)])
    choices=[F(d0,2000)]
    upper_witness={"kind":"one_basis","state_bitmask":bits0,"flux":list(f0)}
    for e,(a,b) in enumerate(p["p_ed"]):
        if occ[a]==occ[b]:continue
        dx=[0,0]
        if e in chord:dx[chord[e]]=-(1 if occ[a] else -1)
        dest=bits0^(1<<a)^(1<<b)
        df=tuple(f0[j]+dx[j] for j in range(2))
        if (dest,df) not in local:continue
        d1=local[dest,df]
        for t in (F(1,8),F(1,4),F(1,2),F(1),F(2)):
            # Choose relative sign of basis amplitudes so hopping
            # contribution is -2*t*.7. Fermion sign is absorbable.
            ray=F(d0+t*t*d1-2*t*1400,2000*(1+t*t))
            if ray<min(choices):
                upper_witness={"kind":"two_basis","states":[bits0,dest],
                   "fluxes":[list(f0),list(df)],"amplitude_ratio":str(t),
                   "offdiagonal_absolute_rational":"7/10"}
            choices.append(ray)
    # Magnetic source 2-basis trial gives more options with abs 5/16.
    for dx in shifts:
        for dr in (-1,1):
            df=tuple(f0[j]+dr*dx[j] for j in range(2))
            if (bits0,df) not in local:continue
            d1=local[bits0,df]
            for t in (F(1,8),F(1,4),F(1,2),F(1)):
                ray=F(d0+t*t*d1-2*t*625,2000*(1+t*t))
                if ray<min(choices):
                    upper_witness={"kind":"two_basis_magnetic",
                       "fluxes":[list(f0),list(df)],
                       "amplitude_ratio":str(t),
                       "offdiagonal_absolute_rational":"5/16"}
                choices.append(ray)
    upper=min(choices)
    # For t<P_lower and t<q_lower, block Schur inequality:
    # (P_lower-t)(Q_lower-t)>=||K||^2 guarantees H>=t I.
    # Find a fraction t=P_lower - n/10000 *by exact integer search*.
    k=1
    while F(k,10000)*(qlower-P_lower+F(k,10000))<ksq:
        k+=1
        assert k<10**6
    lower=P_lower-F(k,10000)
    assert (P_lower-lower)*(qlower-lower)>=ksq
    assert lower<=P_lower<qlower
    assert lower<upper
    return {
      "status":"PASS_TOE74_UNCONDITIONAL_TWO_LOOP_ROTOR_GROUND_ENCLOSURE",
      "native_Gauss_sites_links_fermions":[11,12,5],
      "P_cutoff":3,"P_dimension":22638,
      "P_exact_gershgorin_row_numerator_units_2000":min_row[0],
      "P_row_min_native_occupation_flux":[min_row[1],list(min_row[2])],
      "P_min_diagonal_units_2000":d0,
      "Q_exact_gershgorin_spectral_lower":str(qlower),
      "interface_exact_squared_norm_upper":str(ksq),
      "unconditional_full_rotor_E0_lower_fraction":str(lower),
      "unconditional_full_rotor_E0_upper_fraction":str(upper),
      "numeric_display_only_E0_interval":[float(lower),float(upper)],
      "upper_bound_witness":upper_witness,
      "proof":"Exact 22,638 row census gives P>=pI; separately verified infinite Q>=qI, ||PHQ||²<=k². For lower rational t<p<q with (p-t)(q-t)>=k², H-tI is PSD by Schur complement. Exact one-/two-basis Rayleigh quotient supplies upper. Neither calculation uses sparse Ritz eigenvalue ordering.",
      "spectral_gap_certified":False,
      "scope":"Unconditional but potentially loose E0 interval for one finite native two-loop model with unbounded electric integer flux; NOT a spectral gap certificate or field-theory result."
    }

if __name__=="__main__":
    obj=certificate()
    (ROOT/"data/w33_20261014_toe74_unconditional_gauge_bound.json").write_text(
        json.dumps(obj,indent=2)+"\n")
    print(obj["status"],obj["numeric_display_only_E0_interval"])
