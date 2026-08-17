#!/usr/bin/env python3
"""Pass5691: finite Yang--Mills candidate from the orientation-twisted affine su(3).

Pass5686 gives an exact compact su(3) Lie bracket on the zero-sum module V8 of the
nine AG(2,3) sites, with Killing form -54 times the Euclidean metric.  This pass
builds the smallest natural affine link/face complex and asks what is and is not
fixed by that algebra.

The 1-skeleton is K9 (36 links).  Translation parallelograms from the four affine
directions give 54 plaquette boundaries.  Over R:
  rank d0 = 8,
  dim Z1 = 36-8 = 28,
  rank span(plaquette boundaries) = 24,
so H1 has dimension 4.  Adding the 12 affine-line triangles raises the boundary
rank to 28 and kills real H1.  Thus the Lie algebra fixes the invariant quadratic
form, but the finite geometry has not uniquely selected which 2-cells belong in a
Yang--Mills action.

For a su(3)-valued link cochain a one may therefore write the finite candidate
  F = d a + 1/2 [a,a],
  S_YM = (1/(2 g^2)) sum_faces <F,F>,
with <x,y>=-K(x,y)/54.  The overall coupling g remains free.

The old repo Z3 connection is a vertical fiber translation on C^9 tensor C^3.  On
the base augmentation sector V8 tensor span(1,1,1), that translation is the
identity.  Hence the old Z3 holonomy is adjoint-trivial on this emergent su(3); it
cannot simply be relabelled as the new nonabelian connection.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5691_AFFINE_SU3_DISCRETE_YM_COMPLEX.json'
Q=3
PTS=[(x,y) for x in range(3) for y in range(3)]
IDX={p:i for i,p in enumerate(PTS)}
DIRS=[(1,0),(0,1),(1,1),(1,2)]
EDGES=list(itertools.combinations(range(9),2)); EI={e:i for i,e in enumerate(EDGES)}

def modp_rank(A,p=3):
    A=np.array(A,dtype=int)%p;m,n=A.shape;r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i,c]%p),None)
        if piv is None:continue
        A[[r,piv]]=A[[piv,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and A[i,c]%p:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==m:break
    return r

def edge_row(vertices):
    row=np.zeros(36,dtype=int)
    cyc=list(vertices)+[vertices[0]]
    for a,b in zip(cyc,cyc[1:]):
        e=tuple(sorted((a,b))); row[EI[e]] += 1 if a<b else -1
    return row

def main():
    # vertex-edge incidence d0^T / boundary_1
    B1=np.zeros((9,36),dtype=int)
    for j,(u,v) in enumerate(EDGES):B1[u,j]=-1;B1[v,j]=1
    assert np.linalg.matrix_rank(B1)==8 and modp_rank(B1)==8

    plaquettes=[]
    for d1,d2 in itertools.combinations(DIRS,2):
        if (d1[0]*d2[1]-d1[1]*d2[0])%3==0:continue
        for p in PTS:
            p1=((p[0]+d1[0])%3,(p[1]+d1[1])%3)
            p12=((p1[0]+d2[0])%3,(p1[1]+d2[1])%3)
            p2=((p[0]+d2[0])%3,(p[1]+d2[1])%3)
            plaquettes.append(edge_row([IDX[p],IDX[p1],IDX[p12],IDX[p2]]))
    P=np.array(plaquettes,dtype=int);assert P.shape==(54,36)
    assert np.max(abs(P@B1.T))==0
    rP=int(np.linalg.matrix_rank(P));rP3=modp_rank(P)
    assert (rP,rP3)==(24,24)

    lines=set()
    for p in PTS:
      for d in DIRS:
        L=tuple(sorted(IDX[((p[0]+t*d[0])%3,(p[1]+t*d[1])%3)] for t in range(3)))
        lines.add(L)
    lines=sorted(lines);assert len(lines)==12
    T=np.array([edge_row(list(L)) for L in lines],dtype=int)
    assert np.max(abs(T@B1.T))==0
    rT=int(np.linalg.matrix_rank(T));rT3=modp_rank(T);assert (rT,rT3)==(12,12)
    PT=np.vstack([P,T]);rPT=int(np.linalg.matrix_rank(PT));rPT3=modp_rank(PT)
    assert (rPT,rPT3)==(28,26)
    cycle_dim=36-8
    assert cycle_dim==28

    # Rebuild Pass5686 orientation tensor and Killing form.
    def sgn(a):a%=3;return 0 if a==0 else (1 if a==1 else -1)
    phi=np.zeros((9,9,9),dtype=int)
    for i,x in enumerate(PTS):
      for j,y in enumerate(PTS):
       for k,z in enumerate(PTS):
        u=((y[0]-x[0])%3,(y[1]-x[1])%3);v=((z[0]-x[0])%3,(z[1]-x[1])%3)
        phi[i,j,k]=sgn(u[0]*v[1]-u[1]*v[0])
    def br(f,g):return np.einsum('ijk,i,j->k',phi,f,g)
    eye=np.eye(9,dtype=int);ads=[]
    for i in range(9):
        M=np.zeros((9,9),dtype=int)
        for j in range(9):M[:,j]=br(eye[i],eye[j])
        ads.append(M)
    K=np.array([[int(np.trace(ads[i]@ads[j])) for j in range(9)] for i in range(9)])
    assert np.array_equal(K,-54*np.eye(9,dtype=int)+6*np.ones((9,9),dtype=int))

    # The vertical 3-cycle is identity on the fiber-constant vector.
    C3=np.array([[0,0,1],[1,0,0],[0,1,0]],dtype=int);one=np.ones(3,dtype=int)
    assert np.array_equal(C3@one,one)

    out={
      'pass':5691,
      'status':'AFFINE_SU3_HAS_CANONICAL_KILLING_YM_FORM_AND_PLAQUETTE_H1_FOUR__OLD_VERTICAL_Z3_IS_ADJOINT_TRIVIAL',
      'affine_complex':{
        'vertices':9,'links':36,'translation_plaquettes':54,'affine_line_triangles':12,
        'rank_boundary1_R':8,'cycle_space_dim_R':cycle_dim,
        'rank_translation_faces_R':rP,'H1_translation_complex_R':cycle_dim-rP,
        'rank_translation_plus_line_faces_R':rPT,'H1_with_line_faces_R':cycle_dim-rPT,
        'rank_translation_faces_F3':rP3,'rank_line_faces_F3':rT3,
        'rank_combined_faces_F3':rPT3,'H1_with_line_faces_F3':cycle_dim-rPT3
      },
      'linearized_su3_harmonic_dimensions':{
        'translation_faces_over_R':(cycle_dim-rP)*8,
        'translation_plus_line_faces_over_R':(cycle_dim-rPT)*8
      },
      'lie_metric':'Killing K=-54 times Euclidean metric on V8; choose <x,y>=-K(x,y)/54. Simplicity fixes the invariant quadratic form only up to overall scale.',
      'finite_YM_candidate':'F_f=(d a)_f + 1/2 [a,a]_f; S_YM=(1/(2 g^2)) sum_f <F_f,F_f>',
      'normalization_boundary':'The Lie bracket/Killing form fixes relative algebraic normalization but does not determine the dimensionless physical gauge coupling g or which admissible face set is dynamical.',
      'vertical_Z3_weld':'The old fiber translation is I_9 tensor C3 and acts trivially on V8 tensor span(1,1,1); its Z3 holonomy is therefore invisible in the adjoint base-su3 sector and is not the new nonabelian connection.',
      'homology_boundary':'The real four-dimensional H1 here is the cycle-space quotient by the computed face-boundary span on this explicit nine-site plaquette complex. Over a field its dual cohomology has the same dimension, but no chain map to any other repo four-logical/cohomology sector is asserted.',
      'physics_boundary':'This is a finite lattice-gauge candidate and cochain census, not a QCD derivation. The action face set, physical coupling, continuum limit, matter representation and confinement mechanism remain open.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
