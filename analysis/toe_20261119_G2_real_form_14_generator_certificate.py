"""Exact rational 14-generator real G2 stabilizer of the positive 3-form.
This is a consistency check of established G2 facts, not an independent proof
of the exceptional complex E6 stabilizer of Grigorian's critical cubic.
"""
from pathlib import Path
import json,itertools
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/toe_20261119_G2_real_form_14_generator_certificate.json'
TERMS=((0,1,2,1),(0,3,4,1),(0,5,6,1),(1,3,5,1),
       (1,4,6,-1),(2,3,6,-1),(2,4,5,-1))
phi=np.zeros((7,7,7),int)
for a,b,c,sign in TERMS:
    for p in itertools.permutations((a,b,c)):
        inv=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        phi[p]=sign*(-1)**inv

def equations():
    rows=[]
    for a,b,c in itertools.combinations(range(7),3):
        row=[int((i==a)*phi[j,b,c]+(i==b)*phi[a,j,c]+(i==c)*phi[a,b,j])
             for i in range(7) for j in range(7)]
        rows.append(row)
    return s.Matrix(rows)

def run():
    A=equations()
    null=A.nullspace()
    assert A.shape==(35,49) and A.rank()==35 and len(null)==14
    mats=[s.Matrix(7,7,list(v)) for v in null]
    assert all(M+M.T==s.zeros(7) for M in mats)
    Mflat=s.Matrix.hstack(*[s.Matrix(49,1,list(M)) for M in mats])
    comm_max=0
    for M,N in itertools.combinations(mats,2):
        C=M*N-N*M
        solution,params=Mflat.gauss_jordan_solve(s.Matrix(49,1,list(C)))
        assert len(params)==0
        comm_max=max(comm_max,float(max(abs(x) for x in (Mflat*solution-s.Matrix(49,1,list(C))))))
    # Real g2 acts on traceless symmetric 7x7 tensors h via
    # h -> R h R^T. Verify both cubic invariants numerically.
    rng=np.random.default_rng(271119)
    def C0(h):return float(np.trace(h@h@h))
    def Cp(h):return float(np.einsum('abc,def,ad,be,cf->',phi,phi,h,h,h,optimize=True))
    err0=0.;errp=0.
    for _ in range(5):
        R=rng.normal(size=(7,7));h=(R+R.T)/2
        h-=np.trace(h)/7*np.eye(7)
        for M in mats:
            mat=np.array(M,dtype=float)
            d=mat@h+h@mat.T
            dh=1e-6
            err0=max(err0,abs((C0(h+dh*d)-C0(h-dh*d))/(2*dh)))
            errp=max(errp,abs((Cp(h+dh*d)-Cp(h-dh*d))/(2*dh)))
    assert err0<1e-7 and errp<1e-7,(err0,errp)
    # Complex critical pencil is nonreal for real parameter. The proof that
    # the common real stabilizer of the two cubics is g2 comes from the
    # established invariant-cubic theorem, NOT just this 7x7 computation.
    out={'real_positive_G2_form_oriented_triples':7,
      'independent_phi_stabilization_equations':35,
      'unknown_7x7_real_Lie_generator_entries':49,
      'exact_matrix_rank':int(A.rank()),
      'exact_Lie_algebra_dimension':len(null),
      'every_generator_skew_symmetric':True,
      'pairwise_commutator_span_checks':91,
      'max_commutator_span_residual':comm_max,
      'numerical_real_cubic_variation_max_C0':err0,
      'numerical_real_cubic_variation_max_Cphi':errp,
      'complex_exceptional_parameters':['(1-i*sqrt(7))/8','(1+i*sqrt(7))/8'],
      'interpretation':'Real positive 3-form G2 Lie algebra 14 embeds in SO7 and acts on 27 real traceless symmetric tensors preserving both C0 and Cphi. The author Grigorian separately proves the complex E6 stabilizer dimension 78 of one critical complex cubic.',
      'qualification':'No charged Dirac index, compact 7D G2 manifold, real E6 gauge boson, kinetic terms or 4D chiral family spectrum derived.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print('G2 REAL GENERATORS',len(null),'CUBIC ERR',err0,errp)
    return out
if __name__=='__main__':run()
