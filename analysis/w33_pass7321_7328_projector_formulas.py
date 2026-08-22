#!/usr/bin/env python3
"""Pass7321-7328: exact double-six/tritangent primitive-projector formulas."""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
import networkx as nx
from w33_pass4992_4999_common import build_base
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7321_7328_PROJECTOR_FORMULAS.json'

def main():
    b=build_base(); N=1-np.asarray(b['M'],dtype=np.int64)
    A36=nx.to_numpy_array(b['H36'],nodelist=range(36),dtype=np.int64)
    A45=np.zeros((45,45),dtype=np.int64)
    for i,j in itertools.combinations(range(45),2):
        if set(b['tritangents'][i])&set(b['tritangents'][j]): A45[i,j]=A45[j,i]=1
    X3=3*N-np.ones((45,36),dtype=np.int64)
    I36=np.eye(36,dtype=np.int64); I45=np.eye(45,dtype=np.int64)
    E36n=(20*I36-A36)@(A36+4*I36)
    E45n=(12*I45-A45)@(A45+3*I45)
    assert np.array_equal(2*(X3.T@X3),3*E36n)
    assert np.array_equal(X3@X3.T,3*E45n)
    assert np.array_equal(2*(A45@X3),3*(X3@A36))
    # E36=E36n/108 and E45=E45n/54, while X=X3/3.
    assert np.array_equal(E36n@E36n,108*E36n)
    assert np.array_equal(E45n@E45n,54*E45n)
    assert np.array_equal(E45n@X3,54*X3)
    assert np.array_equal(X3@E36n,108*X3)
    out={
      'schema':'w33.pass7321_7328.projector_formulas.v1','status':'PASS','passes':'7321-7328',
      'E36':'(20I-A36)(A36+4I)/108','E45':'(12I-A45)(A45+3I)/54','X':'N-J/3',
      'identities':['X^T X = 18 E36','X X^T = 18 E45','2 A45 X = 3 X A36','E45 X = X = X E36'],
      'integer_identities':['2 X3^T X3 = 3(20I-A36)(A36+4I)','X3 X3^T = 3(12I-A45)(A45+3I)'],
      'rank':20,
      'boundary':'Characteristic-zero projector theorem. This realizes the same 20-dimensional permutation constituent as the Pass7184 binary V20 dictionary, but does not identify vectors across characteristics without a change-of-field map.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps({'status':'PASS','rank':20}))
if __name__=='__main__': main()
