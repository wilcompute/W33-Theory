#!/usr/bin/env python3
"""Pass 4743 (outside box): an exact commuting parity Hamiltonian from the 270 residues.

Put one classical/Z qubit on each of the forty W33 lines and one commuting term
S_R=prod_{i in R} Z_i for every four-line involution residue R.  Define

    H = - sum_R S_R.

The check matrix is exactly the 40x270 residue incidence matrix B.  Since
rank_2(B)=30, the +1 ground space has dimension 2^(40-30)=2^10 and, in the Z
basis, is precisely H10=im(A_*).

The syndrome code im(B^T) is [270,30,27].  A MILP proves d=27.  A second exact
MILP excludes every syndrome of weight <=27 except the forty incidence rows,
so the complete minimum shell is exactly the forty single-line syndromes.
Therefore the Hamiltonian gap is 2*27=54 and the first excited eigenspace has
40*2^10=40960 computational basis states.

Two-line defects already read the W33 geometry: skew lines share exactly three
residue checks and violate 48 terms; meeting lines share none and violate 54.
The 540 weight-3 dependencies from Pass 4742 are operator identities
S_a S_b S_c=I.  The 27 Petersen parallel classes from Pass 4741 schedule all
270 four-body terms in the optimal 27 disjoint-support measurement layers.

This is a finite commuting-check/statistical-mechanics theorem.  No claim is
made that it is a realistic microscopic physical Hamiltonian.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy import sparse

from w33_pass4495_4502_distance_prism_reconstruction import geometry

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4743_RESIDUE_PARITY_HAMILTONIAN.json'

def gf2_basis(vals):
    piv={};out=[]
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;out.append(y);break
    return out

def solve_syndrome_min(G,exclude_rows=None,max_weight=None,time_limit=60):
    # G is 270 x 30 over F2; variables are x_30, y_270, integer carries k_270.
    nr,nc=G.shape;N=nc+nr+nr
    rr=[];cc=[];dd=[]
    for j in range(nr):
        for i in np.flatnonzero(G[j]):rr.append(j);cc.append(int(i));dd.append(1.)
        rr.extend((j,j));cc.extend((nc+j,nc+nr+j));dd.extend((-1.,-2.))
    M=sparse.coo_matrix((dd,(rr,cc)),shape=(nr,N)).tocsr()
    lb=np.zeros(N);ub=np.ones(N);ub[nc+nr:]=15
    cons=[LinearConstraint(M,np.zeros(nr),np.zeros(nr))]
    nz=sparse.csr_matrix(([1.]*nc,([0]*nc,list(range(nc)))),shape=(1,N))
    cons.append(LinearConstraint(nz,[1],[nc]))
    if max_weight is not None:
        wy=sparse.csr_matrix(([1.]*nr,([0]*nr,list(range(nc,nc+nr)))),shape=(1,N))
        cons.append(LinearConstraint(wy,[-np.inf],[max_weight]))
    if exclude_rows is not None:
        for row in exclude_rows:
            ones=set(np.flatnonzero(row));vals=[];cols=[]
            for j in range(nr):cols.append(nc+j);vals.append(-1. if j in ones else 1.)
            Q=sparse.csr_matrix((vals,([0]*nr,cols)),shape=(1,N))
            cons.append(LinearConstraint(Q,[1-len(ones)],[np.inf]))
    c=np.zeros(N);c[nc:nc+nr]=1
    if max_weight is not None:c[:]=0
    return milp(c,integrality=np.ones(N),bounds=Bounds(lb,ub),constraints=cons,
                options={'time_limit':time_limit,'presolve':True})

def main():
    _pts,_pidx,_lines,Astar,_aps,_am,_H=geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(Astar[:,C],axis=1)&1):residues.append(tuple(C))
    assert len(residues)==270
    B=np.zeros((40,270),dtype=np.uint8)
    for j,R in enumerate(residues):B[list(R),j]=1
    row_masks=[sum(int(B[i,j])<<j for j in range(270)) for i in range(40)]
    basis=gf2_basis(row_masks);assert len(basis)==30
    G=np.array([[(b>>j)&1 for b in basis] for j in range(270)],dtype=np.uint8)

    opt=solve_syndrome_min(G,time_limit=60)
    assert opt.success and round(opt.fun)==27
    uniqueness=solve_syndrome_min(G,exclude_rows=B,max_weight=27,time_limit=60)
    assert not uniqueness.success and 'infeasible' in uniqueness.message.lower()

    # Exact two-line syndrome weights from the 2-(partial) incidence law.
    pair=Counter()
    for R in residues:
        for a,b in itertools.combinations(R,2):pair[tuple(sorted((a,b)))]+=1
    two=Counter()
    for a,b in itertools.combinations(range(40),2):
        w=int(B[a].sum()+B[b].sum()-2*pair[(a,b)])
        two['meeting' if Astar[a,b] else 'skew'] += (w==54 if Astar[a,b] else w==48)
        assert w==(54 if Astar[a,b] else 48)
    assert two==Counter({'skew':540,'meeting':240})

    # Verify all forty row syndromes are distinct minima and every line is in 27 checks.
    assert len(set(row_masks))==40 and {x.bit_count() for x in row_masks}=={27}
    assert set(B.sum(axis=1).tolist())=={27}

    # The computational ground-state code is H10.
    arows=[sum(int(Astar[i,j])<<j for j in range(40)) for i in range(40)]
    assert len(gf2_basis(arows))==10
    out={'pass':4743,'hamiltonian':'H = - sum_{R in 270 residues} prod_{i in R} Z_i',
      'checks':270,'check_weight':4,'check_rank':30,
      'ground_space':{'dimension_log2':10,'degeneracy':1024,'classical_Z_basis_code':'H10=[40,10,12]','ground_energy':-270},
      'syndrome_code':{'parameters':'[270,30,27]','minimum_distance_MILP':27,
                       'complete_minimum_shell':40,'minimum_words':'the forty line-incidence syndrome rows'},
      'spectral_floor':{'gap':54,'first_excited_degeneracy':40960},
      'defects':{'single_line_violated_terms':27,'two_skew_lines_violated_terms':48,
                 'two_meeting_lines_violated_terms':54},
      'operator_redundancy':{'weight3_check_identities':540,'identity':'S_a S_b S_c = I'},
      'measurement_schedule':{'layers':27,'terms_per_layer':10,'support_disjoint_within_layer':True,'optimal':True},
      'boundary':'Exact commuting parity-check Hamiltonian and syndrome theorem; no microscopic implementation or thermodynamic-limit claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
