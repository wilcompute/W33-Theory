"""Exact product-family W33 Levi x Z^d return-heat-kernel spectral dimension.

Product is explicitly SUPPLIED, so this diagnoses nonselection of 3-space.
Graph Laplacian: L_W=(4I-A_Levi), lattice L_Z=2I-shift-shift^-1.
"""
from pathlib import Path
from math import exp,sqrt
from scipy.special import i0e,i1e
import json
ROOT=Path(__file__).resolve().parents[1]
SQ6=sqrt(6)
SPECTRUM=[(0,1),(4-SQ6,24),(4,30),(4+SQ6,24),(8,1)]
def internal(t):
    weights=[m*exp(-l*t) for l,m in SPECTRUM]
    s=sum(weights)
    hazard=sum(l*w for (l,m),w in zip(SPECTRUM,weights))/s
    return s/80,2*t*hazard
def lattice_one(t):
    return float(i0e(2*t)),float(4*t*(1-i1e(2*t)/i0e(2*t)))
def product(d,t):
    assert isinstance(d,int) and d>=0 and t>0
    a,na=internal(t);b,nb=lattice_one(t)
    return dict(d=d,t=t,return_probability=a*b**d,
        native_spectral_dimension=na,
        supplied_lattice_spectral_dimension=d*nb,
        total_spectral_dimension=na+d*nb)
def certificate():
    assert sum(m for l,m in SPECTRUM)==80
    rows=[product(d,t) for d in (0,1,2,3,4) for t in (0.1,1,5,20,100,500)]
    for d in (0,1,2,3,4):
        result=product(d,500)
        assert abs(result['total_spectral_dimension']-d)<.003*max(d,1)
    return dict(status='PASS',schema='w33.20261009.spatial_product_heat.v1',
        graph='W33 Levi 80-vertex connected 4-regular graph x Z^d',
        finite_internal_laplacian_eigenvalues='0^1,(4-sqrt6)^24,4^30,(4+sqrt6)^24,8^1',
        formula='P(t)=(1+24e^(-(4-sqrt6)t)+30e^(-4t)+24e^(-(4+sqrt6)t)+e^(-8t))/80 * [e^(-2t) I0(2t)]^d',
        asymptotic='P(t) ~ 1/[80*(4*pi*t)^(d/2)]; d_s -> d as t -> infinity; dimension d is a supplied product parameter.',
        speed='Long-wave dispersion of weighted Z^d lattice is sum c_i^2 k_i^2, with c_i supplied, not selected by native W33.',
        samples=rows,boundary='Does not derive 3+1 dimensions, physical c, continuum dynamics or Einstein equations.')
if __name__=='__main__':
    r=certificate();(ROOT/'data/w33_20261009_spatial_product_spectral_dimension.json').write_text(json.dumps(r,indent=2)+'\n')
    for d in range(5):print(d,product(d,100),product(d,500)['total_spectral_dimension'])
