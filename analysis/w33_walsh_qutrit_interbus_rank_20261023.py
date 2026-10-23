#!/usr/bin/env python3
"""Walsh qutrit interbus transfer: exact 40-mode shared-vertex overlap ranks.

Assumptions: each of 40 W33 points is ONE orthogonal photonic spatial mode.
This is a mathematical address model. Existing hardware bus incidence has
160 optical port incidents and may give each incidence a DISTINCT waveguide!
Hence direct overlap is only a diagnostic, not the verified hardware transfer.

For distinct W33 lines L,L': they share 0 or 1 point. Their 3D Walsh codes
have direct-overlap rank 0 (skew) or 1 (intersecting); never rank 3.
A 40-mode rail permutation can nonetheless transfer all 4 coherent rails:
3 pair swaps if one point is shared, else 4 swaps. NOT a fabricated switch.
"""
from __future__ import annotations
import collections,hashlib,itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_linebus_switch_matrix_20261023 import LINES,N
from w33_pic_xor_walsh_pareto_20261023 import H4

def code_for_line(index,order=None):
    line=LINES[index]
    perm=tuple(line if order is None else order)
    if set(perm)!=set(line) or len(perm)!=4:raise ValueError("order must be a permutation of line")
    code=np.zeros((N,3))
    code[list(perm),:]=H4()[:,1:4]
    return code

def interbus_isometry(a,b):
    """Exact rail permutation (multiple spatial moves) for a given line pair."""
    if not 0<=a<len(LINES) or not 0<=b<len(LINES) or a==b:raise ValueError("distinct lines 0..39")
    src=set(LINES[a]);dst=set(LINES[b])
    shared=sorted(src&dst)
    assert len(shared) in (0,1)
    src_only=sorted(src-dst);dst_only=sorted(dst-src)
    assert len(src_only)==len(dst_only)==4-len(shared)
    order_src=shared+src_only;order_dst=shared+dst_only
    V_src=code_for_line(a,order_src)
    V_dst=code_for_line(b,order_dst)
    sigma=list(range(N))
    swaps=[]
    for x,y in zip(src_only,dst_only):
        sigma[x],sigma[y]=sigma[y],sigma[x]
        swaps.append((x,y))
    P=np.eye(N)[sigma] # permutation is a product of disjoint transpositions
    assert np.linalg.norm(P@V_src-V_dst)<1e-12
    assert np.linalg.norm(P.T@P-np.eye(N))<1e-12
    assert np.linalg.norm(P@P-np.eye(N))<1e-12
    return {'source_line':a,'destination_line':b,
       'shared_point':shared[0] if shared else None,
       'moved_rail_swaps':[list(x) for x in swaps],
       'moved_rail_count':len(swaps),
       'logical_qutrit_transfer_error':float(np.linalg.norm(P@V_src-V_dst)),
       'phase_convention':'aligned port ordering: shared point first, sorted others',
       'hardware_warning':'40-mode mathematical permutation, not PDK routing or physical crossbar'}

def census():
    sizes=collections.Counter()
    singular_hist=collections.Counter()
    examples={}
    rank_bad=0
    for i,j in itertools.combinations(range(40),2):
        intersection=len(set(LINES[i])&set(LINES[j]))
        assert intersection in (0,1)
        sizes[intersection]+=1
        C=code_for_line(i).T@code_for_line(j)
        s=np.linalg.svd(C,compute_uv=False)
        rank=int(np.sum(s>1e-10))
        assert rank==intersection
        assert (abs(s[0]-.75)<1e-12 if intersection else s[0]<1e-12)
        singular_hist[rank]+=1
        if intersection not in examples:
            examples[intersection]=interbus_isometry(i,j)
    assert sizes=={1:240,0:540}
    assert singular_hist=={1:240,0:540}
    assert examples[1]['moved_rail_count']==3
    assert examples[0]['moved_rail_count']==4
    return {'schema':'w33.walsh.qutrit.interbus_rank.v1',
       'model':'40 spatial modes indexed by W33 points; exact linear-algebra hypothesis',
       'distinct_line_pairs':780,
       'line_intersection_distribution':dict(sorted(sizes.items())),
       'direct_qutrit_overlap_rank_distribution':dict(sorted(singular_hist.items())),
       'intersecting_direct_overlap_singular_values':[.75,0,0],
       'disjoint_direct_overlap_singular_values':[0,0,0],
       'rank_no_go':'Direct code-space overlap cannot carry a full qutrit between two distinct line buses. Rank <=1.',
       'explicit_full_qutrit_permutation_transfer':{
          'intersecting':examples[1],'skew':examples[0],
          'number_of_moved_rail_pair_swaps':'3 for intersecting lines, 4 for skew lines, under this permutation implementation'},
       'scope':['Overlap is NOT optical scattering transfer; it assumes one rail per W33 point.',
         'Actual W33 bus circuit has 160 incidence ports; distinct incident rails may be separate physical waveguides',
         'The 3- or 4-swap 40-mode permutation is a mathematical target, not a physical circuit and not optimized',
         'Coherent arrival time, insertion loss, phase matching, optical crossing routing and control still needed',
         'No quantum error correction or general two-qutrit gate implied']}
def run():
    obj=census()
    obj['sha256']=hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return obj
if __name__=='__main__':
    obj=run()
    file=ROOT/'data/w33_walsh_qutrit_interbus_rank_20261023.json'
    file.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print('PASS interbus',obj['line_intersection_distribution'],obj['direct_qutrit_overlap_rank_distribution'],
          obj['explicit_full_qutrit_permutation_transfer']['intersecting']['moved_rail_count'])
