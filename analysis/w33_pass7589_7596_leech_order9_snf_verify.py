#!/usr/bin/env python3
"""Pass7589-7596: exact Smith audit of a fixed-point-free order-9 Co0 witness.

A determinant of 729 alone does NOT imply L/(1-g)L = F3^6; 9-torsion is a
logical possibility.  This verifier reads the actual integral Co0 matrix emitted
by the companion GAP pass and decides the quotient group by Smith normal form.
If it is elementary abelian, the standard linking pairing for a fixed-point-free
isometry of an odd unimodular lattice makes the quotient a nondegenerate
symplectic F3-space, hence its projectivization is W(5,3).
"""
from __future__ import annotations
import ast,hashlib,json,math
from collections import Counter
from pathlib import Path
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

ROOT=Path(__file__).resolve().parents[1]
MAT=ROOT/'data/PART_W33_PASS7589_7596_LEECH_ORDER9_MATRIX.txt'
OUT=ROOT/'data/PART_W33_PASS7589_7596_LEECH_ORDER9_SNF.json'

def rank_mod(A,p):
    M=[[int(x)%p for x in row] for row in A.tolist()];m=len(M);n=len(M[0]);r=0
    for c in range(n):
        z=next((i for i in range(r,m) if M[i][c]),None)
        if z is None:continue
        M[r],M[z]=M[z],M[r];u=pow(M[r][c],-1,p);M[r]=[(u*x)%p for x in M[r]]
        for i in range(m):
            if i!=r and M[i][c]:
                q=M[i][c];M[i]=[(M[i][j]-q*M[r][j])%p for j in range(n)]
        r+=1
    return r

def main():
    raw=MAT.read_bytes(); M=sp.Matrix(ast.literal_eval(raw.decode().strip()))
    assert M.shape==(24,24) and M**9==sp.eye(24) and M**3!=sp.eye(24)
    A=sp.eye(24)-M
    det=abs(int(A.det()));assert det==729
    D=smith_normal_form(A,domain=ZZ)
    diag=[abs(int(D[i,i])) for i in range(24)]
    assert all(d>0 for d in diag) and math.prod(diag)==729
    tors=[d for d in diag if d>1]; snf=Counter(tors)
    elementary=(snf==Counter({3:6}))
    r3=rank_mod(A,3);null3=24-r3
    # For an SNF with 3-primary factors, dim coker/3 coker equals number of
    # nontrivial invariant factors.  This is an independent consistency check.
    assert null3==len(tors)
    out={
      'schema':'w33.pass7589_7596.leech_order9_snf.v1','status':'PASS','passes':'7589-7596',
      'matrix_sha256':hashlib.sha256(raw).hexdigest(),'order':9,'trace':int(sp.trace(M)),
      'det_I_minus_g':det,'smith_diagonal':diag,'nontrivial_smith_invariants':dict(sorted(snf.items())),
      'rank_mod_3_I_minus_g':r3,'coker_mod3_dimension':null3,'elementary_F3_6':elementary,
      'audit_result':('L/(1-g)L is exactly F3^6; the earlier 364-point projectivization is justified.' if elementary else 'The quotient has higher 3-power torsion; determinant 729 does not give F3^6 and the earlier 364-point projectivization must be corrected.'),
      'linking_form_theorem':('For a fixed-point-free isometry g of a unimodular integral lattice, b([x],[y])=< (1-g)^(-1)x,y > mod Z is perfect. Since (1-g)^-* = 1-(1-g)^(-1), its odd-primary part is alternating. Thus an elementary F3^6 cokernel carries a canonical nondegenerate alternating form.'),
      'geometry_if_elementary':('W(5,3) on all 364 projective 1-spaces of F3^6' if elementary else None),
      'claim_boundary':'The Smith computation is representation/lattice arithmetic. The polar-space identification is conditional only on the verified elementary cokernel plus the standard unimodular linking-pairing lemma; no Monster or physics claim follows.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','snf':dict(snf),'rank_mod3':r3,'elementary_F3_6':elementary,'geometry':out['geometry_if_elementary']}))
if __name__=='__main__':main()
