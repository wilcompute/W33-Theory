#!/usr/bin/env python3
"""Exact volume-runaway no-go for fixed T4 integer 3-flux toy model.

The common four M6/IIB5 coordinate directions are physical directions
in the shared 9D description. If one additionally compactifies them on
a flat T4, the external dimension is FIVE, not nine.

The positive three-form kinetic term on T4 with metric R² gbar gives
a coordinate-frame reduction factor R^{4-6}=R^{-2}. Rescaling the
external FIVE-dimensional metric to Einstein frame contributes
R^{-4*5/(5-2)}=R^{-20/3}; total potential R^{-26/3} E(tau).
For nonzero transverse integer flux rank2 E_min(tau)=2sqrt D>0:
there is no critical point in the volume R: d/dlog R V= -26/3 V.
This kills any claim that the previous flux-doublet shape minimum is a
fully stabilized EFT or string compactification vacuum.
"""
from pathlib import Path
from fractions import Fraction
import json,sys
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261114_E6_9D_flux_doublet_moduli_stabilizer import det_invariant
OUT=ROOT/"data/toe_20261114_E6_flux_shape_vs_volume_runaway_nogo.json"

def main():
    n=4;D=5;p=3
    factor_raw=Fraction(n-2*p)
    factor_einstein=Fraction(-D*n,D-2)
    exponent=factor_raw+factor_einstein
    assert exponent==Fraction(-26,3)
    assert exponent==Fraction(-2*p)-Fraction(2*n,D-2)
    R=sp.symbols("R",positive=True)
    x=sp.symbols("x",real=True)
    y=sp.symbols("y",positive=True)
    F=[1,1,0,0]
    H=[0,1,1,0]
    FF,HH,FH,disc=det_invariant(F,H)
    assert (FF,HH,FH,disc)==(2,2,1,3)
    E=(FF-2*x*FH+(x*x+y*y)*HH)/y
    V=R**sp.Rational(exponent.numerator,exponent.denominator)*E
    xs=sp.Rational(FH,HH)
    ys=sp.sqrt(disc)/HH
    assert sp.simplify(E.subs({x:xs,y:ys})-2*sp.sqrt(3))==0
    d_x=sp.diff(V,x).subs({x:xs,y:ys})
    d_y=sp.diff(V,y).subs({x:xs,y:ys})
    assert sp.simplify(d_x)==0
    assert sp.simplify(d_y)==0
    d_logR=sp.simplify(R*sp.diff(V,R))
    assert sp.simplify(d_logR-sp.Rational(-26,3)*V)==0
    assert sp.simplify(d_logR.subs({x:xs,y:ys})+
                       sp.Rational(52,3)*sp.sqrt(3)*R**sp.Rational(-26,3))==0
    hessian=sp.hessian(E,(x,y)).subs({x:xs,y:ys}).applyfunc(sp.simplify)
    assert hessian==sp.sqrt(3)*sp.Rational(8,3)*sp.eye(2)
    volumes=[sp.Rational(k,1) for k in (1,2,3,10)]
    vals=[sp.simplify(V.subs({x:xs,y:ys,R:r})) for r in volumes]
    assert all(float(a)>float(b)>0 for a,b in zip(vals,vals[1:]))
    result=dict(status="PASS_EXACT_FLUX_SHAPE_POSITIVE_HESSIAN_BUT_VOLUME_RUNAWAY",
        physical_dimension_correction="Shared four ExFT internal coordinates are 9D physical directions (5 external+4 internal); compactifying those four on T4 leaves five external dimensions.",
        assumed_metric_ansatz="unwarped block diagonal R^2 T4 metric, fixed normalized flat shape, no other fluxes/sources",
        external_dimension=D,internal_compact_dimension=n,threeform_degree=p,
        raw_integrated_flux_radius_power=str(factor_raw),
        external_Einstein_Weyl_radius_power=str(factor_einstein),
        Einstein_frame_total_radius_power=str(exponent),
        exact_shape_star="tau=(1+i sqrt3)/2",
        flux_discriminant=disc,flux_shape_minimal_energy="2sqrt3",
        shape_Hessian_at_minimum=[["8 sqrt3 / 3","0"],["0","8 sqrt3 / 3"]],
        exact_volume_gradient_relation="dV/dlogR=-(26/3)V",
        no_simultaneous_finite_volume_and_shape_critical_point=True,
        sample_shape_minimized_volume_potential=[
            {"R":str(r),"V":str(z)} for r,z in zip(volumes,vals)],
        original_E6_section_selector_status="NOT OBTAINED",
        necessary_additional_physics="sources, higher curvature, negative/competing energy terms, warping/Einstein constraints, global flux/tadpole consistency, and consistent ExFT generalized Scherk-Schwarz twist or another genuine solution of field equations",
        scholarly_basis=[
            "https://arxiv.org/abs/1312.0614",
            "https://link.springer.com/article/10.1007/JHEP01%282015%29131",
            "https://www.classe.cornell.edu/~pt267/files/talks/RSKS.pdf"])
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ("status","Einstein_frame_total_radius_power",
        "flux_shape_minimal_energy","exact_volume_gradient_relation",
        "no_simultaneous_finite_volume_and_shape_critical_point")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
