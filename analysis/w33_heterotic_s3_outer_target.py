#!/usr/bin/env python3
"""Exact heterotic S3 target for the W33 outer C2 extension law.

Konopka, JHEP 07 (2013) 023, Sec. 6, gives an explicit heterotic toroidal
orbifold with point group S3.  In the published lattice basis,

sigma =
[[ 0,-1, 0, 0, 0, 0],
 [ 1,-1, 0, 0, 0, 0],
 [ 0, 0,-1, 1, 0, 0],
 [ 0, 0,-1, 0, 0, 0],
 [ 0, 0, 0, 0, 1, 0],
 [ 0, 0, 0, 0, 0, 1]]

tau =
[[ 1,-1, 0, 0, 0, 0],
 [ 0,-1, 0, 0, 0, 0],
 [ 0, 0, 1,-1, 0, 0],
 [ 0, 0, 0,-1, 0, 0],
 [ 0, 0, 0, 0,-1, 0],
 [ 0, 0, 0, 0, 0,-1]].

They satisfy tau^2=sigma^3=(tau sigma)^2=I, equivalently
  tau sigma tau^-1 = sigma^-1.

This is exactly the extension law of the certified W33 pair
  s^2=z^3=1,  s z s^-1=z^-1.

Therefore the previous Z6-II no-go does not kill the heterotic bridge; it
redirects it to a non-Abelian S3 point group.  The group extension matches
exactly.  What remains open is a physically meaningful representation-level
intertwiner between the heterotic S3 sectors/gauge embedding and the W33
Heisenberg central-character doublet.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_heterotic_s3_outer_target.json'

S=[
[0,-1,0,0,0,0],
[1,-1,0,0,0,0],
[0,0,-1,1,0,0],
[0,0,-1,0,0,0],
[0,0,0,0,1,0],
[0,0,0,0,0,1]]
T=[
[1,-1,0,0,0,0],
[0,-1,0,0,0,0],
[0,0,1,-1,0,0],
[0,0,0,-1,0,0],
[0,0,0,0,-1,0],
[0,0,0,0,0,-1]]
I=[[1 if i==j else 0 for j in range(6)] for i in range(6)]
def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(6)) for j in range(6)] for i in range(6)]
def pw(A,n):
    R=I
    for _ in range(n):R=mm(R,A)
    return R
def main(write=True):
    assert pw(T,2)==I and pw(S,3)==I and pw(mm(T,S),2)==I
    Sinv=pw(S,2)
    assert mm(mm(T,S),T)==Sinv
    out={'schema':'w33.heterotic_s3_outer_target.v1','status':'PASS_EXACT_EXTENSION_LAW_MATCH',
      'source':'Sebastian J.H. Konopka, Non-Abelian orbifold compactifications of the heterotic string, JHEP 07 (2013) 023, Sec.6',
      'heterotic_point_group':{
        'presentation':'S3=<tau,sigma | tau^2=sigma^3=(tau sigma)^2=e>',
        'order2':'tau','order3':'sigma',
        'inversion':'tau sigma tau^-1=sigma^-1',
        'published_lattice_sigma':S,'published_lattice_tau':T},
      'W33':{
        'presentation_fragment':'<s,z | s^2=z^3=1, s z s^-1=z^-1>',
        'map_of_extension_law':{'tau':'s','sigma':'z'},
        'generated_subgroup':'S3'},
      'bridge_status':'The abstract semidirect extension law matches exactly, unlike cyclic Z6-II.',
      'representation_boundary':'sigma is a geometric point-group generator whereas z is the Heisenberg center phase. No representation/gauge-spectrum intertwiner is yet constructed, so they are not identified as the same physical operator.',
      'next_target':'Compare irreducible sector projectors and centralizer actions of the heterotic S3 model with the W33 V1+V2 induced module, looking for a common two-dimensional defining representation.',
      'checks':{'tau2':True,'sigma3':True,'tausigma2':True,'inversion_relation':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
