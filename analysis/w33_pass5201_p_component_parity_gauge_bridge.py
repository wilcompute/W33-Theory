#!/usr/bin/env python3
"""Pass5201: P-component parity is a gauge-invariant point-footprint quotient.

Pass5177 decomposes the P side into tensor components and Pass5180 proves that
a chamber star restricts to one weight-q^2 minimum atom in each of q^2 P
components.  For odd q, q^2 is odd, so taking total coordinate parity inside
each P component sends every chamber-star atom to 1.

Pass5186 identifies the q^2-component footprint of a chamber star with its W
point p, and every P component C with a 2(q+1)-point block B_C inducing
K_{q+1,q+1}.  Let F be the point/component incidence matrix F[p,C]=1 iff
p in B_C.  If a_p is the parity of the number of selected chamber generators
based at point p, then the P-component parity vector of the apartment word is

    s = F^T a  (over F2).

The integer Gram matrix is determined by the Pass5186 two-intersection law:

    FF^T = (q^2-1) I + (q-1) A_W + J.

At q=5 this is 24 I + 4 A_W + J, hence FF^T=J over F2.

Every W-line meets every component block B_C in 0 or 2 points.  Indeed if p is
in B_C, its q+1 neighbors inside the induced K_{q+1,q+1} lie on the q+1 distinct
W-lines through p, one per line.  Therefore every W-line incidence vector lies
in ker(F^T).

This has an exact chamber-gauge interpretation.  Toggling the chamber cut at a
line vertex flips the point-parity vector by that W-line incidence vector, while
toggling a point-vertex cut leaves point parity unchanged because q+1 is even.
Thus s is invariant under the chamber dependency/cut gauge and is an intrinsic
linear observable of the apartment-code word.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5201_P_COMPONENT_PARITY_GAUGE_BRIDGE.json'


def point_graph_multiplicities(q):
    v=(q+1)*(q*q+1);k=q*(q+1);r=q-1;s=-(q+1)
    # 1+f+g=v and k+f r+g s=0.
    f=(-k-(v-1)*s)//(r-s);g=v-1-f
    assert 1+f+g==v and k+f*r+g*s==0
    return v,k,r,s,f,g


def main():
    anchors={}
    for q in (3,5,7,9):
        v,k,r,s,f,g=point_graph_multiplicities(q)
        # Real spectrum of the footprint Gram from the two-intersection law.
        lam0=(q*q-1)+(q-1)*k+v
        lamr=(q*q-1)+(q-1)*r
        lams=(q*q-1)+(q-1)*s
        assert lam0==2*q*q*(q+1)
        assert lamr==2*q*(q-1)
        assert lams==0
        anchors[str(q)]={'W_points':v,'P_components':q*q*(q*q+1)//2,
          'footprint_size':q*q,'component_block_size':2*(q+1),
          'integer_Gram':'(q^2-1)I+(q-1)A+J',
          'real_Gram_eigenvalues':[lam0,lamr,lams],
          'real_Gram_multiplicities':[1,f,g]}

    q=5;v,k,r,s,f,g=point_graph_multiplicities(q)
    assert (v,k,r,s,f,g)==(156,30,4,-6,90,65)
    out={'pass':5201,'status':'THEOREM_ODD_Q_P_COMPONENT_PARITY_GAUGE_BRIDGE',
      'domain':'odd q; q=5 is the live application',
      'parity_map':'For chamber-generator coefficients y, set a_p=sum_{flags f based at p} y_f mod2. The parity of every P-component restriction is s=F^T a.',
      'footprint_Gram':'FF^T=(q^2-1)I+(q-1)A_W+J over the integers; for odd q this reduces to J over F2.',
      'line_kernel':'Every W-line incidence vector lies in ker(F^T), because each P-component K_{q+1,q+1} point block meets a W-line in 0 or 2 points.',
      'gauge_invariance':'A line-panel chamber cut adds its W-line incidence vector to a; a point-panel chamber cut does not change a when q is odd because q+1 is even. Hence s is invariant under the full chamber cut gauge.',
      'q5':{'points':156,'components':325,'footprint_weight':25,
        'component_block':'K_6,6 on 12 W-points','integer_Gram':'24I+4A+J',
        'mod2_Gram':'J','real_Gram_spectrum':'300^1 + 40^90 + 0^65'},
      'connection':'If s is nonzero, its Hamming support is a lower bound on the number of active P components, each of which has apartment weight at least 25 by Pass5179. If s=0, the word lies in the even-parity P-component sector. Determining the minimum nonzero weight of the footprint code im(F^T), and whether ker(F^T) equals the W-line incidence code, are now concrete finite-geometric subproblems.',
      'boundary':'This is a linear parity/gauge theorem, not a proof that every nonzero footprint parity has weight at least 25. The binary rank/minimum distance of im(F^T) and the even-parity residual sector remain open here; no q5 minimum-distance theorem is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
