#!/usr/bin/env python3
"""Exact hull and quantum-distance audit of the ramified affine VM code.

Parent: w33_affine_holonomy_vm_code_architecture.py. The AG(2,3) geometry is
classical (Artebani-Dolgachev, arXiv:math/0611590); no novelty is claimed for
Hesse incidence or the parent [45,12,6] parameters. This certifies the private
triple lift, its hull shell, and an obstruction to useful CSS distance.
"""
from pathlib import Path
from itertools import product, combinations
import json
import numpy as np
from w33_affine_holonomy_vm_code_architecture import gf3_rank, enumerate_weights
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_affine_holonomy_hull.json'

def main(write=True):
    parent=json.loads((ROOT/'data/w33_ramified_hesse_cubic_holonomy_bridge.json').read_text())
    records=parent['lifted_code']['fiber_point_to_tritangent']
    points=[tuple(r['AG23_point']) for r in records]
    # Directions are normals. Their three level sets are the parallel lines.
    directions=[(1,0),(0,1),(1,1),(1,2)]
    A=np.array([[int((a*x+b*y)%3==t) for x,y in points]
                for a,b in directions for t in range(3)],dtype=np.int16)
    bytrit={r['tritangent_index']:i for i,r in enumerate(records)}
    parent_lines={tuple(sorted(bytrit[e['tritangent_index']] for e in r['fiber_tritangents']))
                  for r in parent['lifted_code']['relation_records']}
    assert parent_lines=={tuple(np.flatnonzero(row)) for row in A}
    G=np.concatenate((2*A,np.repeat(np.eye(12,dtype=np.int16),3,axis=1)),axis=1)%3
    gram=(G@G.T)%3
    expected=np.kron(np.ones((4,4),dtype=np.int16)-np.eye(4,dtype=np.int16),np.ones((3,3),dtype=np.int16))%3
    assert np.array_equal(gram,expected)
    assert gf3_rank(gram.tolist())==3
    # Eight within-direction differences and one equal-direction-sum vector.
    R=[]
    for d in range(4):
        for j in (1,2):
            v=np.zeros(12,dtype=np.int16);v[3*d]=1;v[3*d+j]=2;R.append(v)
    v=np.zeros(12,dtype=np.int16);v[::3]=1;R.append(v)
    R=np.array(R);H=(R@G)%3
    assert gf3_rank(H.tolist())==9 and not np.any(H@G.T%3)
    weights=enumerate_weights(H.tolist())
    assert min(w for w in weights if w)==12 and weights[12]==24
    shell={tuple((s*(G[3*d+i]-G[3*d+j])%3).tolist())
           for d in range(4) for i,j in combinations(range(3),2) for s in (1,2)}
    assert len(shell)==24 and all(sum(x!=0 for x in w)==12 for w in shell)
    # Quotient basis: one line from each of the first three directions.
    Q=gram[np.ix_([0,3,6],[0,3,6])]
    isotropic=[]
    for v in product(range(3),repeat=3):
        if not any(v) or next(x for x in v if x)!=1:continue
        z=np.array(v)
        if int(z@Q@z)%3==0:isotropic.append(list(v))
    assert sorted(isotropic)==[[0,0,1],[0,1,0],[1,0,0],[1,1,1]]
    # Every hull column is nonzero: dual has no weight-one words. A private
    # triple difference is orthogonal to the hull but not in the hull (d=12).
    assert all(np.any(H[:,j]) for j in range(45))
    witness=np.zeros(45,dtype=np.int16);witness[9:11]=[1,2]
    assert not np.any(H@witness%3)
    # The punctured core dual has an independent point-star parity basis.
    dual21=np.concatenate((np.eye(9,dtype=np.int16),A.T),axis=1)
    G21=np.concatenate((2*A,np.eye(12,dtype=np.int16)),axis=1)%3
    assert not np.any(dual21@G21.T%3)
    w21=enumerate_weights(dual21.tolist())
    assert min(w for w in w21 if w)==5 and w21[5]==18
    out={'schema':'w33.affine_holonomy_hull.v1','status':'PASS',
         'hull':{'parameters':'[45,9,12]_3','generator':H.tolist(),
                 'weight_enumerator':{str(k):v for k,v in weights.items()},
                 'minimum_words':24,'minimum_shell':'signed differences of parallel-line generators'},
         'quotient':{'dimension':3,'gram':Q.tolist(),'isotropic_projective_points':isotropic,
                     'interpretation':'four parallel direction classes modulo their common sum'},
         'punctured_dual':{'parameters':'[21,9,5]_3','weight_enumerator':{str(k):v for k,v in w21.items()},
                           'minimum_words':18,'minimum_shell':'signed point-star parity checks'},
         'CSS':{'parameters':'[[45,27,2]]_3','distance_two_witness':witness.tolist(),
                'boundary':'distance two detects but does not correct an arbitrary single-qutrit error'},
         'parents':['data/w33_ramified_hesse_cubic_holonomy_bridge.json','data/w33_affine_holonomy_vm_code_architecture.json'],
         'checks':{'parent_affine_lines_match':True,'gram_rank3':True,'hull_rank9':True,
                   'hull_orthogonal_to_full_code':True,'complete_hull_enumerator':True,
                   'four_isotropic_directions':True,'CSS_distance_exactly2':True,
                   'punctured_dual_distance5':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    return out
if __name__=='__main__':print(json.dumps(main(),indent=2))
