#!/usr/bin/env python3
"""Pass5704: finite adjoint-SU(3) transport and the unresolved face-selection problem.

Pass5686/5696 gives an exact compact su(3) bracket on the augmentation V8 of the
nine AG(2,3) sites. Pass5691 gave the infinitesimal Yang--Mills candidate. Here we
exponentiate adjoint operators to finite transporters and ask which 2-cells are
actually selected by existing repo geometry.

Two exact support facts coexist:
  * the E6 allowed36 cubics project to 12 affine lines, three lifts per line;
  * translation locality supplies 54 parallelogram plaquettes.
The line triangles alone span rank 12 of the 28-dimensional K9 cycle space;
translation plaquettes span rank 24; together they span all 28 over R. Thus E6
cubic incidence selects the twelve line faces, but it does not by itself select
the extra translation faces needed to remove all real harmonic 1-modes.

We also construct finite adjoint transporters U=exp(theta ad_X). A pure-gauge
triangle has identity holonomy, while two noncommuting affine generators give a
nontrivial finite group commutator. This is an honest PSU(3)=Ad(SU(3)) Wilson
carrier; the fundamental 3 and a physical coupling are not yet selected.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5704_AFFINE_SU3_WILSON_FACE_SELECTION.json'
PTS=[(x,y) for x in range(3) for y in range(3)]; IDX={p:i for i,p in enumerate(PTS)}
DIRS=[(1,0),(0,1),(1,1),(1,2)]
EDGES=list(itertools.combinations(range(9),2)); EI={e:i for i,e in enumerate(EDGES)}

def edge_row(vertices):
    r=np.zeros(36,dtype=int);cyc=list(vertices)+[vertices[0]]
    for a,b in zip(cyc,cyc[1:]):
        e=tuple(sorted((a,b)));r[EI[e]]+=1 if a<b else -1
    return r

def sgn3(a):a%=3;return 0 if a==0 else (1 if a==1 else -1)

def bracket_tensor():
    phi=np.zeros((9,9,9),dtype=int)
    for i,x in enumerate(PTS):
      for j,y in enumerate(PTS):
       for k,z in enumerate(PTS):
        u=((y[0]-x[0])%3,(y[1]-x[1])%3);v=((z[0]-x[0])%3,(z[1]-x[1])%3)
        phi[i,j,k]=sgn3(u[0]*v[1]-u[1]*v[0])
    return phi

def main():
    B1=np.zeros((9,36),dtype=int)
    for j,(u,v) in enumerate(EDGES):B1[u,j]=-1;B1[v,j]=1
    cycle_dim=36-int(np.linalg.matrix_rank(B1));assert cycle_dim==28
    pla=[]
    for d1,d2 in itertools.combinations(DIRS,2):
      if (d1[0]*d2[1]-d1[1]*d2[0])%3==0:continue
      for p in PTS:
        p1=((p[0]+d1[0])%3,(p[1]+d1[1])%3)
        p12=((p1[0]+d2[0])%3,(p1[1]+d2[1])%3)
        p2=((p[0]+d2[0])%3,(p[1]+d2[1])%3)
        pla.append(edge_row([IDX[p],IDX[p1],IDX[p12],IDX[p2]]))
    P=np.array(pla);assert P.shape==(54,36)
    lines=set()
    for p in PTS:
      for d in DIRS:lines.add(tuple(sorted(IDX[((p[0]+t*d[0])%3,(p[1]+t*d[1])%3)] for t in range(3))))
    lines=sorted(lines);assert len(lines)==12
    T=np.array([edge_row(L) for L in lines])
    ranks={'line_triangles':int(np.linalg.matrix_rank(T)),'translation_plaquettes':int(np.linalg.matrix_rank(P)),'combined':int(np.linalg.matrix_rank(np.vstack([T,P])))}
    assert ranks=={'line_triangles':12,'translation_plaquettes':24,'combined':28}

    phi=bracket_tensor()
    def br(x,y):return np.einsum('ijk,i,j->k',phi,x,y)
    basis=[]
    for i in range(8):
      v=np.zeros(9);v[i]=1;v[8]=-1;basis.append(v)
    def ad(x):
      M=np.zeros((8,8))
      for j,y in enumerate(basis):
        z=br(x,y);assert abs(z.sum())<1e-10;M[:,j]=z[:8]
      return M
    X,Y=basis[0],basis[1];AX,AY=ad(X),ad(Y)
    assert np.linalg.norm(br(X,Y))>1e-8
    theta=0.125
    Ux=expm(theta*AX);Uy=expm(theta*AY)
    W=Ux@Uy@np.linalg.inv(Ux)@np.linalg.inv(Uy)
    nonabelian_res=float(np.linalg.norm(W-np.eye(8)))
    assert nonabelian_res>1e-8

    # Pure gauge: G_i=exp(theta f_i ad_X), U_ij=G_i^-1 G_j.
    f=np.array([x+2*y for x,y in PTS],float)
    G=[expm(theta*f[i]*AX) for i in range(9)]
    tri=lines[0];hol=np.eye(8)
    cyc=list(tri)+[tri[0]]
    for a,b in zip(cyc,cyc[1:]):hol=hol@(np.linalg.inv(G[a])@G[b])
    pure_res=float(np.linalg.norm(hol-np.eye(8)));assert pure_res<1e-9

    out={
      'pass':5704,'status':'FINITE_ADJOINT_SU3_WILSON_TRANSPORT_CONSTRUCTED__E6_SELECTS_LINES_BUT_FULL_FACE_SET_REMAINS_UNDERDETERMINED',
      'carrier':{'sites':9,'links':36,'cycle_space_dimension_R':28,'representation':'8D adjoint, hence PSU(3)=Ad(SU(3))'},
      'face_support':{'E6_horizontal_cubics':36,'E6_base_affine_lines':12,'lifts_per_line':3,'translation_parallelograms':54,'boundary_ranks_R':ranks,'harmonic_dim_line_only':16,'harmonic_dim_translation_only':4,'harmonic_dim_combined':0},
      'finite_transport':'U_e=exp(ad_a_e); Wilson loop is trace/product in the adjoint representation',
      'tests':{'theta':theta,'noncommuting_generator_bracket_norm':float(np.linalg.norm(br(X,Y))),'nonabelian_commutator_distance_from_identity':nonabelian_res,'pure_gauge_triangle_holonomy_residual':pure_res,'adjoint_commutator_trace':float(np.trace(W).real)},
      'selection_result':'E6 cubic support canonically singles out the 12 affine-line triangles. Translation geometry independently supplies 54 parallelograms. The combined 66-face complex kills real H1, but no existing theorem uniquely derives that combined face action or its relative face weights.',
      'Linfinity_boundary':'The firewall/collision deformation selects vertical deleted cubic supports and does not supply the missing translation plaquettes or a unique Yang-Mills face weighting.',
      'physics_boundary':'This constructs finite nonabelian adjoint transport. It does not identify the affine su3 with QCD, choose a fundamental 3, fix g, derive confinement, or establish a continuum limit.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
