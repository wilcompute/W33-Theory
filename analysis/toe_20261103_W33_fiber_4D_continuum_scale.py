#!/usr/bin/env python3
"""Exact W(3,3) internal fiber x 4D toroidal base spectral-separation test.

Separate base continuum limit from internal-mode masses. The bare W(3,q)
point-graph normalized gap does not vanish at large q. The Cartesian product
has low-lying base modes but does not derive spacetime or particle spectra.
"""
from pathlib import Path
import itertools,math,json
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1]
def w33():
 pts=[];seen=set()
 for x in itertools.product(range(3),repeat=4):
  if x==(0,0,0,0):continue
  k=min(tuple(x),tuple((-n)%3 for n in x))
  if k not in seen:seen.add(k);pts.append(k)
 assert len(pts)==40
 omega=lambda a,b:(a[0]*b[2]-a[2]*b[0]+a[1]*b[3]-a[3]*b[1])%3
 A=np.array([[int(i!=j and omega(p,q)==0) for j,q in enumerate(pts)] for i,p in enumerate(pts)],dtype=int)
 assert (A==A.T).all() and np.all(A.sum(axis=1)==12)
 assert np.array_equal(A@A,8*np.eye(40,dtype=int)-2*A+4*np.ones((40,40),dtype=int))
 assert sorted(zip(*np.unique(np.round(np.linalg.eigvalsh(A)).astype(int),return_counts=True)))==[(-4,15),(2,24),(12,1)]
 return A
def ring_lap(L):
 j=np.arange(L)
 A=sparse.coo_matrix((np.ones(2*L),(np.r_[j,j],np.r_[(j+1)%L,(j-1)%L])),shape=(L,L)).tocsr()
 A.sum_duplicates()
 return (2*sparse.eye(L,format='csr')-A).tocsr()
def torus_lap(L,dimension=4):
 lp=ring_lap(L);id=sparse.eye(L,format='csr')
 terms=[]
 for axis in range(dimension):
  fac=[lp if a==axis else id for a in range(dimension)]
  T=fac[0]
  for f in fac[1:]:T=sparse.kron(T,f,format='csr')
  terms.append(T)
 return sum(terms)
def spectral(L):
 # exact Cartesian-product eigenvalues of graph Laplacian:
 # internal: {0,10x24,16x15}; base 4D torus 2 sum(1-cos(2pi n/L)).
 b=2-2*math.cos(2*math.pi/L)
 internal_gap=10
 # total degree 12+8 =20
 full_gap=b/20
 mass_ratio=internal_gap/b
 return {'L_per_spatial_coordinate':L,'4D_base_vertices':L**4,
  'product_graph_vertices':40*L**4,'base_first_nonzero_Laplacian_eigenvalue':b,
  'normalized_product_first_eigenvalue':full_gap,
  'internal_W33_24d_carrier_Laplacian_eigenvalue':internal_gap,
  'internal_W33_15d_carrier_Laplacian_eigenvalue':16,
  'internal_over_base_first_gap':mass_ratio,
  'physical_internal_mass_squared_if_a_phys_length_over_L_and_standard_kinetic_operator':10*L*L,
  'physical_base_first_mass_squared_if_a_phys_length_over_L':b*L*L}
def main():
 A=w33()
 ls=[4,6,8,12,16,24,48]
 rows=[spectral(n) for n in ls]
 # Verify 4D base spectrum numerically without building 40x tensor product.
 B=torus_lap(4)
 low=np.linalg.eigvalsh(B.toarray())[:10]
 assert max(abs(sorted(low)[i]-(0 if i==0 else 2)) for i in range(9))<1e-7
 assert np.all(np.linalg.eigvalsh(12*np.eye(40)-A)>-1e-9)
 # Old W33 GQ normalized gap=1 -2/12 =5/6.
 gap_W33_norm=(12-2)/12
 assert abs(gap_W33_norm-5/6)<1e-12
 # q general, A k=q(q+1), theta=q-1, normalized gap 1-theta/k->1.
 qrows=[{'q':q,'vertices':(q+1)*(q*q+1),'degree':q*(q+1),
    'normalized_point_graph_gap':1-(q-1)/(q*(q+1)),
    'diameter_upper_bound':2} for q in (3,5,7,9,11,19,31)]
 out={'status':'PASS_EXACT_W33_INTERNAL_FIBER_4D_BASE_SPECTRAL_SCALE_SEPARATION',
  'construction':'Cartesian product of finite symplectic GQ W(3,3) point graph 40 vertices degree12, with a supplied periodic 4D LxLxLxL nearest-neighbor torus degree8. Combinatorial Laplacian kronecker sum; not a direct physical Kaluza–Klein model.',
  'exact_srg_polynomial':'A_W33^2 = 8 I - 2 A_W33 +4 J',
  'adjacency_spec':{'12':1,'2':24,'-4':15},
  'lap_spec':{'0':1,'10':24,'16':15},
  'regular_graph_normalized_gap':gap_W33_norm,
  'q_GQ_bare_graph_normalized_gap_tower':qrows,
  'rows':rows,
  'numeric_4D_L4_lap_low_eigs':sorted(low.tolist()),
  'asymptotic_claim':'With spatial coordinate length held fixed and a=1/L, continuum base Lap first gap scales (2pi)^2/L² and physical base eigen tends (2pi)^2, but if internal W33 links have same a^-2 kinetic strength, their positive 24-sector physical eigen=10 L² -> infinity. To retain finite 24-sector masses, independently scale internal link weight as a² relative to base, or provide a distinct internal geometric radius. This is a parametric scale separation, NOT a no-go against any weighted/tuned unified spectral action.',
  'topology_boundary':'The torus and its 4D topology were supplied; no W33 adjacency alone generated a four-dimensional manifold or chiral index, and no Einstein action derived.',
  'literature':['https://doi.org/10.1007/s11005-026-02080-w',
                'https://doi.org/10.3390/universe12070205']}
 (ROOT/'data/toe_20261103_W33_fiber_4D_continuum_scale.json').write_text(json.dumps(out,indent=2)+'\n')
 print('SPECTRAL_BRIDGE',json.dumps({'q3gap':gap_W33_norm,'Lrows':rows,'lowL4':sorted(low.tolist())}),flush=True)
if __name__=='__main__':main()
