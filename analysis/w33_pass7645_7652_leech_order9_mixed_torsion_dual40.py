#!/usr/bin/env python3
"""Pass7645-7652: exact Leech order-9 quotient is mixed 3/9 torsion.

This pass removes the remaining ambiguity in the Leech d=9 quotient without GAP.
It downloads the official ATLAS 24-dimensional integral representation of
2.Co1=Co0, pins the two generator matrices by normalized SHA256, evaluates a
fixed deterministic word in A,B,A^-1,B^-1, and computes the exact Smith normal
form of I-g.

The resulting order-9 element has trace -3 and characteristic polynomial
Phi_3^3 Phi_9^3, but coker(I-g) is NOT F3^6.  It is
    (Z/3)^2 + (Z/9)^2.
Thus the earlier 364-point PG(5,3)/W(5,3) candidate is refuted.  The corrected
module has canonical top C/3C and socle C[3], both F3^4 and hence both carrying
40 projective 1-spaces.  The Leech bridge therefore returns a dual 40+40 shell
at the first/last layers of a genuinely length-two 3-adic module, not a single
364-point vector geometry.
"""
from __future__ import annotations
import ast,hashlib,json,re,urllib.request
from collections import Counter
from pathlib import Path
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7645_7652_LEECH_ORDER9_MIXED_TORSION_DUAL40.json'
URL='https://brauer.maths.qmul.ac.uk/Atlas/spor/Co1/gap0/2Co1G1-Zr24B0.g'
GEN_HASH={
 'A':'a7f0744314646b31b2fb66066cc890049c40822a93257cb4e69279c71c8db965',
 'B':'f7fd56fe41812a32600cfccaedcc9886457829c72afea9793cf41b5f8b9f5b9a'}
WORD=(
 'BbBabBbBbbaAbAaBabaBAabAbabbbBaBaaBBBaaBaabABbbbAbbaaabbbbAbbBbbBBbaab'
 'bBbBBBAaaabbBaABBAaabaABBaAAAbbAABABbBBBBAbbbAAbAbaaBAAbbbaAAAbbBBbbBB'
 'bBabBAABabABBaBBBaABAbbaaBBABAbaaBAAbBAbAbBBbABBaABbbaBbBABaaAabaAABaB')
CAND_HASH='7516b51c4f97a093a65b13dff9c3506375b20d84ac4eee9acbdf91f6343a4374'

def nhash(M):
    return hashlib.sha256(','.join(str(int(x)) for x in list(M)).encode()).hexdigest()

def rank_mod(M,p):
    A=[[int(x)%p for x in row] for row in M.tolist()];m=len(A);n=len(A[0]);r=0
    for c in range(n):
        z=next((i for i in range(r,m) if A[i][c]),None)
        if z is None:continue
        A[r],A[z]=A[z],A[r];u=pow(A[r][c],-1,p);A[r]=[(u*x)%p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                q=A[i][c];A[i]=[(A[i][j]-q*A[r][j])%p for j in range(n)]
        r+=1
    return r

def parse_generators(raw):
    txt=raw.decode('ascii')
    m1=re.search(r'g1:=(\[\[.*?\]\]);;',txt,re.S);m2=re.search(r'g2:=(\[\[.*?\]\]);;',txt,re.S)
    assert m1 and m2
    return sp.Matrix(ast.literal_eval(m1.group(1))),sp.Matrix(ast.literal_eval(m2.group(1)))

def main():
    with urllib.request.urlopen(URL,timeout=60) as r:raw=r.read()
    A,B=parse_generators(raw);assert A.shape==B.shape==(24,24)
    assert nhash(A)==GEN_HASH['A'] and nhash(B)==GEN_HASH['B']
    assert A.det()==B.det()==1 and A**4==sp.eye(24) and B**3==sp.eye(24)
    D={'A':A,'B':B,'a':A.inv(),'b':B.inv()};g=sp.eye(24)
    for c in WORD:g=g*D[c]
    assert nhash(g)==CAND_HASH and g**9==sp.eye(24) and g**3!=sp.eye(24)
    tr=int(sp.trace(g));char=sp.factor(g.charpoly().as_expr());det=abs(int((sp.eye(24)-g).det()))
    x=sp.Symbol('lambda');expected=(x**2+x+1)**3*(x**6+x**3+1)**3
    assert tr==-3 and sp.expand(char-expected)==0 and det==729
    Aop=sp.eye(24)-g;S=smith_normal_form(Aop,domain=ZZ);diag=[abs(int(S[i,i])) for i in range(24)]
    tors=Counter(d for d in diag if d>1);assert tors==Counter({3:2,9:2})
    r3=rank_mod(Aop,3);assert r3==20

    # C = (Z/3)^2 + (Z/9)^2.  Its canonical 3-adic filtration is determined by
    # the invariant factors alone; no choice of basis/splitting is needed for the
    # cardinalities below.
    order=3**2*9**2;exponent=9
    socle_order=3**4       # C[3]
    top_order=3**4         # C/3C
    threeC_order=3**2      # 3C
    middle_order=socle_order//threeC_order
    projective=lambda n:(3**n-1)//2
    assert order==729 and socle_order==top_order==81 and projective(4)==40
    out={
      'schema':'w33.pass7645_7652.leech_order9_mixed_torsion_dual40.v1','status':'PASS','passes':'7645-7652',
      'atlas_source':URL,'atlas_source_sha256':hashlib.sha256(raw).hexdigest(),'normalized_generator_sha256':GEN_HASH,
      'deterministic_word_alphabet':'A,B,a=A^-1,b=B^-1','deterministic_word':WORD,'word_length':len(WORD),'candidate_matrix_sha256':CAND_HASH,
      'order':9,'trace':tr,'characteristic_polynomial':'Phi3^3 * Phi9^3','det_I_minus_g':det,
      'smith_diagonal':diag,'nontrivial_smith_invariants':{'3':2,'9':2},'rank_mod3_I_minus_g':r3,'coker_mod3_dimension':24-r3,
      'cokernel':'(Z/3)^2 x (Z/9)^2','cokernel_order':order,'cokernel_exponent':exponent,
      'refutation':'The order-729 cokernel is not elementary abelian F3^6. Therefore it has no 364-point projectivization PG(5,3), and the proposed Leech W(5,3) identification is false.',
      'canonical_3_adic_filtration':{
        '3C':{'order':threeC_order,'F3_dimension':2,'projective_points':projective(2)},
        'C[3]':{'order':socle_order,'F3_dimension':4,'projective_points':projective(4)},
        'C[3]/3C':{'order':middle_order,'F3_dimension':2,'projective_points':projective(2)},
        'C/3C':{'order':top_order,'F3_dimension':4,'projective_points':projective(4)}},
      'dual40_observation':'The top C/3C and socle C[3] are canonical four-dimensional F3 spaces, so each has exactly 40 projective 1-spaces. This recovers a 40+40 projective shell count at the two ends of the 3-adic filtration, but no W(3,3) incidence/polarity is claimed without an explicit induced alternating form.',
      'linking_pairing_boundary':'Because the Leech lattice is unimodular and g is fixed-point-free, the standard finite linking pairing on coker(1-g) is perfect and alternating at odd primary torsion. Determining its objectwise matrix and the induced geometry on the top/socle is the next problem; the Smith form alone does not identify W(3,3).',
      'novelty_boundary':'Pass7325 corrected the order-9 characteristic polynomial and found 729 classes by random ATLAS/GAP census. Pass7589 prepared an SNF audit but had no committed witness/output. This pass gives a deterministic official-ATLAS matrix word and proves the non-elementary Smith type, thereby correcting the 364-point interpretation.',
      'claim_boundary':'Exact integral lattice/module theorem. The two 40 counts are canonical projective-space counts only, not a physical or W33 identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','SNF':dict(tors),'rank_mod3':r3,'top_socle_projective':[40,40]}))
if __name__=='__main__':main()
