#!/usr/bin/env python3
"""Pass5445: exact q=3 redundancy-versus-conditioning theorem.

Compare two signed apartment synthesis systems for the 81-dimensional Levi cycle
space.

FULL FRAME (Pass5396/5428): 1620 apartment columns, redundancy 20.  All 81
nonzero singular values equal sqrt(160), hence spectral condition number 1 and
||C^+||_2=1/sqrt(160).

DETERMINISTIC BFS BASIS (Pass5439/5443): 81 apartment columns.  Its exact Gram
polynomial has minimum eigenvalue 1 and maximum 160, hence singular condition
sqrt(160) and ||F^{-1}||_2=1.  Its Gram determinant is tau=2^83*5^23.

Thus deleting the 20-fold redundancy down to this cardinality-minimal basis
costs exactly sqrt(160) in worst-direction inverse norm/condition number.  This
is a theorem for the deterministic BFS basis, not an optimality theorem over all
81-apartment bases.
"""
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5445_Q3_REDUNDANCY_CONDITIONING_TRADEOFF.json'

def main():
    full_cols=1620;r=81;N=160
    basis_cols=81;lam_min=1;lam_max=160
    redundancy=full_cols//r
    assert redundancy==20
    full_cond=1.0
    basis_cond=math.sqrt(lam_max/lam_min)
    full_pinv=1/math.sqrt(N);basis_inv=1/math.sqrt(lam_min)
    assert abs((basis_inv/full_pinv)-math.sqrt(160))<1e-12
    out={
      'pass':5445,'status':'THEOREM_Q3_DETERMINISTIC_BFS_BASIS_REDUNDANCY_CONDITIONING_TRADEOFF',
      'full_oriented_apartment_frame':{
        'columns':full_cols,'rank':r,'redundancy':redundancy,
        'nonzero_singular_value':'sqrt(160)','condition_number':1,
        'pseudoinverse_operator_norm':'1/sqrt(160)',
        'cycle_gram_pseudodeterminant':'160^81'},
      'deterministic_BFS_apartment_basis':{
        'columns':basis_cols,'rank':r,
        'gram_min_eigenvalue':lam_min,'gram_max_eigenvalue':lam_max,
        'singular_condition_number':'sqrt(160)','inverse_operator_norm':1,
        'gram_determinant':'2^83*5^23',
        'gram_charpoly':'(x-160)(x-40)^4(x-4)^12(x-1)^28(x^2-17x+40)^12(x^2-8x+10)^6'},
      'exact_penalty':'basis inverse norm / full-frame pseudoinverse norm = sqrt(160)',
      'volume_ratio':'160^81/(2^83*5^23)=2^322*5^58',
      'interpretation':'The full 20-fold apartment redundancy isotropizes the cycle-space singular spectrum completely; the chosen cardinality-minimal BFS basis is anisotropic by sqrt(160).',
      'boundary':'No claim that sqrt(160) is the best possible condition number among all 81-apartment bases. This compares the deterministic Pass5443 BFS basis to the canonical full frame.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
