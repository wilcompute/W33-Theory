from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXXVI_DOILY_E15_PACKET_SPECTRUM_results.json'

from analysis.w33_sp42_doily_s6_closure import main as doily_main
from analysis.w33_pg32_e15_coordinate_gauge import build_w33, pg32


def bxor(a,b): return tuple(x^y for x,y in zip(a,b))
def bform(B,x,y): return sum(x[i]*B[i][j]*y[j] for i in range(4) for j in range(4))%2

def eig_round(M): return Counter(int(round(x)) for x in np.linalg.eigvalsh(np.array(M,dtype=float)))

def main():
    prev=doily_main()
    A=build_w33(); I40=np.eye(40); J40=np.ones((40,40)); E15n=8*I40+J40-4*A
    vals,vecs=np.linalg.eigh(E15n)
    idx=np.argsort(vals)[-15:]
    U=vecs[:,idx]
    for k in range(U.shape[1]):
        m=np.argmax(np.abs(U[:,k]))
        if U[m,k]<0: U[:,k]*=-1
    pgpts,planes,affines,N,H=pg32()
    G=N.T@N
    ev,Q=np.linalg.eigh(G.astype(float))
    O=N@Q@np.diag(1/np.sqrt(ev))@Q.T
    X=U*np.sqrt(24)@O.T

    B=((0,1,1,1),(1,0,1,1),(1,1,0,1),(1,1,1,0))
    label_to_idx={tuple(v):i for i,v in enumerate(pgpts)}
    labels=list(label_to_idx)
    iso=[]; non=[]
    for a,b in combinations(labels,2):
        c=bxor(a,b)
        L=tuple(sorted(label_to_idx[z] for z in (a,b,c)))
        if bform(B,a,b)==0: iso.append(L)
        else: non.append(L)
    iso=sorted(set(iso)); non=sorted(set(non))

    D=np.zeros((15,15),dtype=int)
    T=np.zeros((20,15),dtype=int)
    for r,L in enumerate(iso):
        for i in L: D[r,i]=1
    for r,L in enumerate(non):
        for i in L: T[r,i]=1
    Dpack=X@D.T; Tpack=X@T.T
    DG=Dpack.T@Dpack; TG=Tpack.T@Tpack
    DD=D@D.T; TT=T@T.T

    line_intersections=Counter(int(np.dot(D[i],D[j])) for i,j in combinations(range(15),2))
    non_intersections=Counter(int(np.dot(T[i],T[j])) for i,j in combinations(range(20),2))
    col_doily=Counter(int(x) for x in D.sum(axis=0))
    col_non=Counter(int(x) for x in T.sum(axis=0))

    # Doily line-intersection adjacency on the 15 isotropic lines.
    Adj=(DD-np.diag(np.diag(DD))).astype(int)
    A2=Adj@Adj; J15=np.ones((15,15),dtype=int); I15=np.eye(15,dtype=int)
    srg_doily=np.array_equal(A2,6*I15 + 1*Adj + 3*(J15-I15-Adj))

    # Non-isotropic triangle-line overlap graph: intersection size 1 iff triangles share a K6 edge.
    Nadj=((TT-np.diag(np.diag(TT)))>0).astype(int)
    N2=Nadj@Nadj; J20=np.ones((20,20),dtype=int); I20=np.eye(20,dtype=int)
    # This is the triangular graph T(6) on 20 triangles of K6, srg(20,9,4,6).
    srg_non=np.array_equal(N2,9*I20 + 4*Nadj + 6*(J20-I20-Nadj))

    checks={
      'inherits_doily_closure':prev['n_verified']==prev['n_checks']==18,
      'coordinate_gauge_xxt':np.allclose(X@X.T,E15n,atol=1e-8),
      'coordinate_gauge_xtx':np.allclose(X.T@X,24*np.eye(15),atol=1e-8),
      'line_split_15_20':len(iso)==15 and len(non)==20,
      'doily_incidence_shape':D.shape==(15,15),
      'noniso_incidence_shape':T.shape==(20,15),
      'doily_lines_size_3':Counter(D.sum(axis=1))==Counter({3:15}),
      'noniso_lines_size_3':Counter(T.sum(axis=1))==Counter({3:20}),
      'doily_points_on_3_lines':col_doily==Counter({3:15}),
      'noniso_points_on_4_lines':col_non==Counter({4:15}),
      'doily_line_intersections_45_60':line_intersections==Counter({0:60,1:45}),
      'doily_srg_15_6_1_3':srg_doily,
      'doily_incidence_gram_spectrum_9_4x9_0x5':eig_round(DD)==Counter({0:5,4:9,9:1}),
      'doily_packet_gram_spectrum_216_96x9_0x5':eig_round(DG)==Counter({0:5,96:9,216:1}),
      'doily_packet_rank_10':np.linalg.matrix_rank(DG,tol=1e-8)==10,
      'noniso_triangle_intersections':non_intersections==Counter({0:100,1:90}),
      'noniso_srg_20_9_4_6':srg_non,
      'noniso_incidence_gram_spectrum_12_6x5_2x9':eig_round(T.T@T)==Counter({2:9,6:5,12:1}),
      'noniso_packet_gram_spectrum_288_144x5_48x9':eig_round(TG)==Counter({48:9,144:5,288:1}),
      'noniso_packet_rank_15':np.linalg.matrix_rank(TG,tol=1e-8)==15,
      'packet_45_matches_csaszar_sum':int(D.sum())==45,
      'packet_60_skew_matches_15x4':line_intersections[0]==60,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXXVI',
      'theorem':'Doily/E15 packet spectrum',
      'coordinate_gauge':{'identity':'X X^T = 24 E15','column_gram':'X^T X = 24 I15'},
      'doily_packets':{'lines':15,'line_size':3,'incidences':45,'skew_line_pairs':60,'intersecting_line_pairs':45,'packet_rank':10,'packet_gram_spectrum':{'216':1,'96':9,'0':5}},
      'nonisotropic_packets':{'lines':20,'line_size':3,'incidences':60,'packet_rank':15,'packet_gram_spectrum':{'288':1,'144':5,'48':9}},
      'readings':{
        'doily':'The 15 isotropic doily lines define 15 three-column E15 packets. Their Gram has rank 10 and spectrum 216^1 + 96^9 + 0^5, so the doily packet system compresses the 15 E15 directions onto the 10-dimensional K5 mutation-edge carrier.',
        'nonisotropic':'The 20 non-isotropic triangle lines define a full-rank 15-dimensional packet system with spectrum 288^1 + 144^5 + 48^9, preserving the full E15 carrier.'
      },
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['doily_packets'], r['nonisotropic_packets'])
