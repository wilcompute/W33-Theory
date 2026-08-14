#!/usr/bin/env python3
"""Pass5184: all-q quadratic-form bridge for the gallery-distance-three count.

For a selected chamber set Y in W(3,q), let x and y be its selected degree
vectors on points and lines, A_P and A_L the point and line collinearity
adjacency matrices, and N_i the numbers of selected chamber pairs at gallery
distance i.  Then

  (x^T A_P x + y^T A_L y)/2 = N1 + 2 N2 + N3.

A distance-one pair is counted once (by the opposite endpoint graph), a
distance-two pair twice (both cross incidences), a distance-three pair once,
and a distance-four pair not at all.  The absence of Levi 4- and 6-cycles
prevents hidden double counts.

The point and line graphs are SRG((q+1)(q^2+1),q(q+1),q-1,q+1), with
nontrivial eigenvalues q-1 and -(q+1).  Therefore, for any degree vector z of
sum m,

 z^T A z <= (q-1)||z||^2 + m^2/(q+1).

At q=5 and m=33, define the upper spectral defect

 D(z)=4||z||^2 + m^2/6 - z^T A z.

Since z^T A z is even, 4||z||^2 is divisible by four, and 33^2/6=363/2,
D(z) belongs to 3/2+2 Z_{>=0}.  Thus D(x)+D(y)>=3, which sharpens the ordinary
spectral upper bound by an extra integer unit after halving.  Using
||x||^2+||y||^2=2m+2N1 gives

 N1+2N2+N3 <= 4m+4N1+m^2/6-3/2 = 312+4N1

for m=33,q=5.  The current dense layers therefore have exact integer caps
532,536,540,544 at N1=55,56,57,58.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5184_ALLQ_N3_QUADRATIC_FORM_BRIDGE.json'


def point_graph_params(q):
    return ((q+1)*(q*q+1),q*(q+1),q-1,q+1)


def q5_m33_cap(N1):
    m=33
    # half of the two vector upper bounds, using D_x+D_y>=3
    z=Fraction(4*m+4*N1)+Fraction(m*m,6)-Fraction(3,2)
    assert z.denominator==1
    return z.numerator


def main():
    anchors={}
    for q in (2,3,4,5,7,9):
        v,k,lam,mu=point_graph_params(q)
        r=q-1;s=-(q+1)
        # SRG quadratic for the two nontrivial eigenvalues:
        # x^2-(lambda-mu)x-(k-mu)=(x-r)(x-s).
        assert r+s==lam-mu and r*s==-(k-mu)
        anchors[str(q)]={'v':v,'k':k,'lambda':lam,'mu':mu,
                         'nontrivial_eigenvalues':[r,s],
                         'upper_quadratic_form':'zAz <= (q-1)||z||^2 + m^2/(q+1)'}
    caps={str(W):q5_m33_cap(W) for W in (55,56,57,58)}
    assert caps=={'55':532,'56':536,'57':540,'58':544}
    out={'pass':5184,'status':'THEOREM_ALL_Q_GALLERY_N3_QUADRATIC_FORM_BRIDGE',
      'identity':'(x^T A_P x + y^T A_L y)/2 = N1 + 2 N2 + N3',
      'pair_count_proof':'Distance 1 contributes once, distance 2 twice, distance 3 once, distance 4 zero; Levi girth eight prevents a second distance-2 cross incidence or simultaneous point/line witnesses at distance 3.',
      'point_line_graph_parameters':'SRG((q+1)(q^2+1), q(q+1), q-1, q+1)',
      'spectral_upper':'z^T A z <= (q-1)||z||^2 + m^2/(q+1)',
      'anchors':anchors,
      'q5_m33_defect_quantization':'D(z)=4||z||^2+33^2/6-zAz lies in 3/2+2 Z_{>=0}; hence D(x)+D(y)>=3.',
      'q5_m33_integer_cap':'N1+2N2+N3 <= 312+4N1',
      'q5_m33_dense_caps':caps,
      'connection':'This couples the chamber association-scheme coordinate N3 directly to the two generalized-quadrangle point/line SRG quadratic forms and adds an arithmetic eigenlattice defect at the odd m=33 frontier.',
      'boundary':'The all-q identity and spectral bound are exact. The displayed 3/2 defect quantization is the q=5,m=33 arithmetic specialization. It improves but does not by itself close leader 33.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
