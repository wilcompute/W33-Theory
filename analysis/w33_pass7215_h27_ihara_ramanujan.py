#!/usr/bin/env python3
"""Pass7215: exact Ramanujan/Ihara/spanning-tree closure of the H27 matter graph."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7215_H27_IHARA_RAMANUJAN.json'

def main():
    n=27;k=8;m=n*k//2
    spec={8:1,2:12,-1:8,-4:6};assert sum(spec.values())==n and sum(lam*r for lam,r in spec.items())==0
    assert sum(lam*lam*r for lam,r in spec.items())==n*k
    # Strict Ramanujan: every nontrivial |lambda| <= 2 sqrt(k-1); here max=4 and 4^2<28.
    assert max(abs(x) for x in spec if x!=k)==4 and 16<4*(k-1)
    beta1=m-n+1; bass_exp=m-n
    assert m==108 and beta1==82 and bass_exp==81
    # Matrix-tree theorem: tau=(1/n) product_{lambda != k}(k-lambda)^mult.
    # = 6^12 9^8 12^6 / 27 = 2^24 3^31.
    tau=(6**12)*(9**8)*(12**6)//27
    assert tau==2**24*3**31
    # From intersection array {8,6,1;1,3,8}, a1=k-b1-c1=1; triangles=n*k*a1/6=36.
    triangles=n*k*(k-6-1)//6;assert triangles==36
    out={'schema':'w33.pass7215.h27_ihara_ramanujan.v1','status':'PASS',
      'graph':{'vertices':27,'degree':8,'edges':108,'spectrum':{'8':1,'2':12,'-1':8,'-4':6},'intersection_array':'{8,6,1;1,3,8}'},
      'Ramanujan':{'strict':True,'largest_nontrivial_absolute_eigenvalue':4,'bound':'2*sqrt(7)','squared_check':'16 < 28'},
      'Ihara_inverse':'(1-u^2)^81 (1-8u+7u^2) (1-2u+7u^2)^12 (1+u+7u^2)^8 (1+4u+7u^2)^6',
      'Bass_exponent_m_minus_n':81,'cycle_space_dimension_m_minus_n_plus_1':82,
      'spanning_trees':str(tau),'spanning_tree_factorization':'2^24 * 3^31','triangles':36,
      'prior_art_firewall':'The bare 27-vertex distance-transitive antipodal 3-cover of K9 is classical. The repo-specific result is its objectwise appearance as the E8/W33 matter-fibre graph and its compatibility with the determinant/H27/Hesse structures.',
      'boundary':'Exact finite graph theorem. Bass exponent 81 is m-n and must not be confused with H1 dimension 82.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','beta1':82,'trees':out['spanning_tree_factorization']}))
if __name__=='__main__':main()
