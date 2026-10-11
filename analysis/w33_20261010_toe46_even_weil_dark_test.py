"""TOE46: audit whether 15 dark incidence modes equal Sym²(even Weil 5).

Compares characters of the actual Sp(4,3) point permutation minus4
eigenspace with the symmetric square of the even 5D two-qutrit Weil
matrix representation, on exact finite-group generator words.
"""
import sys,itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass11897_11898_kahler_moduli_two_qutrit_weil as K
OUT=ROOT/"data/w33_20261010_toe46_even_weil_dark_rep_test.json"
canon=lambda v:min(v,tuple(-a%3 for a in v))
pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
idx={p:i for i,p in enumerate(pts)}
sp=lambda u,v:(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3
A=np.array([[int(i!=j and sp(u,v)==0) for j,v in enumerate(pts)] for i,u in enumerate(pts)])
Pm=(A-12*np.eye(40))@(A-2*np.eye(40))/96
assert np.linalg.matrix_rank(Pm)==15
E=K.even_basis()
assert E.shape==(9,5)
Q,_=np.linalg.qr(E)
g9=list(K.GENS.items())
gpairs=[]
for name,g in g9:
 g5=Q.conj().T@g@Q
 assert np.max(abs(g5@g5.conj().T-np.eye(5)))<1e-12
 M=K.symplectic_image(g)
 assert M.shape==(4,4)
 P=np.zeros((40,40))
 for j,p in enumerate(pts):
  transformed=canon(tuple((M@np.array(p))%3))
  P[idx[transformed],j]=1
 assert np.max(abs(P@A-A@P))==0
 gpairs.append((name,g5,M,P))
def stats(g5,P):
 chardark=np.trace(Pm@P)
 char15=(np.trace(g5)**2+np.trace(g5@g5))/2
 return [float(chardark.real),float(abs(char15)),float(abs(abs(chardark)-abs(char15)))]
individual={}
for name,g5,_,P in gpairs:
 individual[name]=stats(g5,P)
# Random words across all generator types; projective overall phases on
# even-Weil U5 cannot change the magnitude of Sym² characters.
rng=np.random.default_rng(46005)
words={}
for k in range(32):
 word=tuple(int(i) for i in rng.integers(0,len(gpairs),size=int(rng.integers(2,12))))
 u5=np.eye(5,dtype=complex);p40=np.eye(40)
 for i in word:
  _,e,_,p=gpairs[i]
  u5=u5@e;p40=p40@p
 words[str(k)]={"word":[gpairs[i][0] for i in word],"char_stats":stats(u5,p40)}
max_err=max([v[2] for v in individual.values()]+[v["char_stats"][2] for v in words.values()])
# If this fails, a DIMENSION match (15=Sym²5) is NOT a representation match.
out={"status":"EVEN_WEIL_5_SYMMETRIC_SQUARE_VS_W33_DARK_15_CHARACTER_TEST",
 "comparand":"W33 point permutation -4 eigenspace, dim15, versus Sym^2 of Kähler two-qutrit even Weil 5, dim15",
 "generator_character_absolute_tests":individual,"random_word_character_tests":words,
 "max_absolute_character_magnitude_difference":max_err,
 "projective_equivalence_rejected_if_nonzero":bool(max_err>1e-8),
 "conclusion":"If max error>1e-8, the representations cannot be projectively equivalent under the canonical Sp4(3) symplectic action. Similar dimension alone does not imply a 15=Sym²5 bridge. If errors vanish, this is a necessary but NOT sufficient isomorphism test; explicit intertwiner and all group characters still needed.",
 "basis_and_action":"E=K.even_basis() in computational 9-space; g5=Qdag g9 Q using orthonormalized columns, p40 from symplectic_image(g9), P-4=(A-12I)(A-2I)/96"}
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"chars":individual,"max_err":max_err,"rejected":out["projective_equivalence_rejected_if_nonzero"]}))
