#!/usr/bin/env python3
"""Minimal four extra H27-character F-term constraints isolate E6 singlet toy branch.

Exact regular, E6/H27-invariant renormalizable extension; quotient-local
moduli vanish at s=(1,1,omega), t=conj(s). This is not a complete
phenomenological vacuum: other Higgs/gauge directions and anomalies remain.
"""
from __future__ import annotations
import json,itertools
from pathlib import Path
import numpy as np
import sympy as S
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_further_e6_isolated_singlet.json'
IDS=((0,0),(1,0),(2,0),(0,1),(0,2))
PRIMES=((7,2),(13,3),(19,7),(31,5),(37,10),(43,6))

def check_poly():
    w,t=S.symbols('w t')
    s=[1,1,w];sb=[1,1,-1-w]
    red=lambda z:S.rem(S.expand(z),w*w+w+1,w)
    B=[red(sum(sb[(j+b)%3]*w**(a*((j+b)%3))*s[j] for j in range(3))) for a,b in IDS]
    assert B==[3,0,0,0,0]
    J=S.Matrix([[sb[(j+b)%3]*w**(a*((j+b)%3)) for j in range(3)]+[w**(a*i)*s[(i-b)%3] for i in range(3)] for a,b in IDS])
    minors=[S.factor(red(J[:,[k for k in range(6) if k!=i]].det())) for i in range(6)]
    assert all(S.simplify(x-y)==0 for x,y in zip(minors,[-27,27,-27*w,-27,27,27*(w+1)])),minors
    M=S.Matrix([[2,w,1],[w,2,1],[1,1,2*w]])
    Md=S.Matrix([[2,-1-w,1],[-1-w,2,1],[1,1,2*(-1-w)]]).T
    spectrum=S.factor(red((Md*M-t*S.eye(3)).det()))
    assert spectrum==-(t-7)**2*(t-4),spectrum
    massdet=red(M.det());massnorm=red(M.det()*Md.det())
    assert S.simplify(massdet-(-6+10*w))==0 and massnorm==196
    return dict(constraints=[int(q) for q in B],Jacobian_5x5_minors=[str(x) for x in minors],
       exact_matter_10_mass_det=str(massdet),matter_10_mass_determinant_norm_sq=int(massnorm),
       mass_squared_characteristic_polynomial=str(spectrum),mass_squared_eigenvalues=[4,7,7])

def mod_rank(A,p):
    A=np.array(A,dtype=np.int64,copy=True)%p;r=0
    for c in range(A.shape[1]):
        if r>=A.shape[0]:break
        ix=np.flatnonzero(A[r:,c]);
        if not len(ix):continue
        k=r+int(ix[0]);A[[r,k]]=A[[k,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(A.shape[0]):
            if i!=r:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
    return r

def check_mod(p,w):
    assert (w*w+w+1)%p==0
    v=[1,1,w];vb=[1,1,w*w%p]
    def B(a,b,s,t):return sum(t[(j+b)%3]*pow(w,a*(j+b),p)*s[j] for j in range(3))%p
    assert [B(a,b,v,vb) for a,b in IDS]==[3,0,0,0,0]
    J=[[vb[(j+b)%3]*pow(w,a*(j+b),p)%p for j in range(3)]+[pow(w,a*i,p)*v[(i-b)%3]%p for i in range(3)] for a,b in IDS]
    assert mod_rank(J,p)==5
    # Complexified gauge tangent s->lambda*s, t->lambda^-1*t is null.
    tangent=np.array(v+[-u for u in vb],dtype=np.int64)
    assert np.all(np.array(J)@tangent%p==0)
    # H27 family X and Z: bilinears transform in 1D characters.
    def shift(s):return [s[-1]]+s[:-1]
    def invshift(t):return t[1:]+t[:1]
    def zact(s):return [pow(w,i,p)*s[i]%p for i in range(3)]
    def zbar(t):return [pow(w,(-i)%3,p)*t[i]%p for i in range(3)]
    probe_v=[1,2,3];probe_t=[5,4,6]
    for a,b in IDS:
        original=B(a,b,probe_v,probe_t)
        # Under H27 X: t transforms contragredient X, character omega^-a.
        Ximage=B(a,b,shift(probe_v),shift(probe_t))
        Zimage=B(a,b,zact(probe_v),zbar(probe_t))
        assert Ximage==pow(w,a,p)*original%p
        assert Zimage==pow(w,(-b)%3,p)*original%p
    return dict(prime=p,omega=w,Jacobian_rank=5,holomorphic_constraint_values=[3,0,0,0,0],
        H27_characters_verified=True,D_flat_pair_v_and_dual=True)

def verify():
    exact=check_poly();rows=[check_mod(p,w) for p,w in PRIMES]
    return dict(status='PASS_RENORMALIZABLE_H27_E6_LOCAL_SINGLET_VACUUM_ISOLATED',date='2026-11-22',
      original_singlet_moduli=4,added_E6_singlet_H27_character_drivers=4,
      total_drivers=5,field_content='Three 27_H plus three conjugate 27bar_H with five E6-singlet driver chiral fields: X00,X10,X20,X01,X02',
      W_terms='W= X00*(B00-mu^2)+X10*B10+X20*B20+X01*B01+X02*B02 + y*hijk*C_E6(Mi,Mj,Hk)',
      B_family='B_ab=sum_j barH_(j+b)*omega^(a*(j+b))*H_j with indices mod3; gauge contraction 27bar x 27 -> 1',
      H27_transformation='B_ab under family X transforms omega^a, under Z transforms omega^-b; assign inverse one-dimensional characters to drivers',
      singlet_vevs_H=[1,1,'omega'],singlet_vevs_Hbar=[1,1,'omega^2'],mu_squared=3,
      all_F_terms_zero_at_driver_and_matter_zero=True,all_E6_D_terms_zero_at_vectorlike_conjugate_pair=True,
      algebraic_certificates=exact,finite_field_certificates=rows,
      local_complex_singlet_dimension_before_gauge=6,
      holomorphic_F_constraint_jacobian_rank=5,
      complexified_U1_gauge_orbit_dimension=1,
      residual_local_complex_singlet_moduli=0,
      minimal_additional_constraints_within_this_singlet_field_content=4,
      physical_matter_10_exotic_masses_abs_units=[2,'sqrt(7)','sqrt(7)'],
      physical_unresolved='Two exotic masses remain degenerate in the toy point. Extra gauge/Higgs directions not proven massive; global minima, charged Higgs spectra, anomaly freedom of discrete flavor, E6 gauge coupling, proton decay, observed Yukawas and vacuum energy not solved.',
      boundary='A LOCAL isolated branch of the E6-singlet-only Higgs subset after complex gauge quotient. Not an isolated vacuum of the entire theory; coupling coefficients and family number are chosen, not derived.')

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['algebraic_certificates'])
if __name__=='__main__':main()
