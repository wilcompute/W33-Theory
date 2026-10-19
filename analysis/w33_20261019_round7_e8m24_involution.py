"""A concrete E8(-24) conjugate-linear involution in the existing
SU9 / sl9+Lambda3+Lambda3* E8 bracket.

Reconciles with repo Pass10949's prior E8(-24) root twist.
"""
from __future__ import annotations
import json,itertools
import numpy as np
from pathlib import Path
import w33_pass11681_e8_from_two_qutrits as E
from w33_pass11687_11691_two_qutrit_e8_dictionary import E8Data
from w33_20261019_round6_chevalley_realform import gr
from w33_20261019_nextfive_optics_su9 import GENERATORS
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round7_e8m24_involution.json"
rng=np.random.default_rng(20261019)
D=np.diag([1.]*7+[-1.]*2).astype(complex)
def compact_conj(g):
    a,x,y=g
    return (-a.conj().T,y.conj(),x.conj())
def theta(g):
    return E8Data.act(D,g)
def twisted_conj(g):
    return theta(compact_conj(g))
def randg():
    a=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
    a-=np.trace(a)*np.eye(9)/9
    return (a,rng.normal(size=84)+1j*rng.normal(size=84),
            rng.normal(size=84)+1j*rng.normal(size=84))
def norm(g):return float(np.linalg.norm(E._vec(g)))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(c,a):return tuple(c*x for x in a)
def compact_fixed(g):return mul(.5,add(g,compact_conj(g)))
def real_fixed(g):return mul(.5,add(g,twisted_conj(g)))
def root_counts():
    K=np.eye(8,dtype=int)*2
    for j in range(6):K[j,j+1]=K[j+1,j]=-1
    K[2,7]=K[7,2]=-1
    roots=gr(K)
    # D acts as -1 on the 7th sl9 simple generator e_6=E_(6,7)
    # and +1 on all other simple generators including e_7=dual 012.
    even=sum(r[6]%2==0 for r in roots)
    return {"roots_total":len(roots),"even_theta_roots":even,
            "odd_theta_roots":len(roots)-even,
            "theta_plus_dim":even+8,"theta_minus_dim":len(roots)-even}
def check():
    ev=[]
    for _ in range(20):
        a,b=randg(),randg()
        j=E.bracket(a,b)
        x,y=real_fixed(a),real_fixed(b)
        cc=E.bracket(compact_conj(a),compact_conj(b))
        tt=E.bracket(theta(a),theta(b))
        jj=E.bracket(twisted_conj(a),twisted_conj(b))
        ev.append({
          "compact_conjugation_automorphism":norm(sub(compact_conj(j),cc)),
          "D_is_bracket_involution":norm(sub(theta(j),tt)),
          "twisted_conjugation_automorphism":norm(sub(twisted_conj(j),jj)),
          "twisted_conjugation_square":norm(sub(twisted_conj(twisted_conj(a)),a)),
          "fixed_point_bracket_closure":norm(sub(twisted_conj(E.bracket(x,y)),E.bracket(x,y))),
          "fixed_point_residual":max(norm(sub(twisted_conj(x),x)),norm(sub(twisted_conj(y),y)))})
    triples=list(itertools.combinations(range(9),3))
    n3minus=sum(sum(k>=7 for k in tr)%2 for tr in triples)
    nAminus=2*7*2
    dimplus=(80-nAminus)+2*(84-n3minus)
    dimminus=nAminus+2*n3minus
    roots=root_counts()
    maxerr=max(max(x.values()) for x in ev)
    # The 5 two-qutrit Cliffords were SU9 automorphisms of the complex E8.
    # For this PARTICULAR real E8(-24), only those commuting with D
    # preserve the conjugate-linear fixed algebra. Do not silently
    # identify all Clifford gates with real-form automorphisms.
    clifford={}
    probe=randg()
    for name,U in GENERATORS.items():
        V=U*np.exp(-1j*np.angle(np.linalg.det(U))/9)
        conjugated=V@D@V.conj().T
        residual=float(np.linalg.norm(conjugated-D))
        left=twisted_conj(E8Data.act(V,probe))
        right=E8Data.act(V,twisted_conj(probe))
        comm=float(norm(sub(left,right)))
        clifford[name]={"D_commutation_residual":residual,
            "real_form_intertwiner_residual":comm,
            "preserves_this_E8m24_fixed_real_structure":bool(residual<1e-10 and comm<1e-10)}
    checks={
      "SU9_D_det_plus_one":abs(np.linalg.det(D)-1)<1e-12,
      "compact_conjugation_is_Lie_antilinear_automorphism":max(x["compact_conjugation_automorphism"] for x in ev)<1e-10,
      "theta_involutive_Lie_automorphism":max(x["D_is_bracket_involution"] for x in ev)<1e-10,
      "twisted_conjugation_is_real_structure":maxerr<1e-10,
      "Killing_signature_from_compact_twist":dimplus==136 and dimminus==112,
      "root_parity_matches_compact_decomposition":roots["theta_plus_dim"]==dimplus and roots["theta_minus_dim"]==dimminus,
      "E7_plus_A1_compact_dimension":roots["even_theta_roots"]==128,
      "five_Clifford_real_form_automorphism_screen":len(clifford)==5 and sum(x["preserves_this_E8m24_fixed_real_structure"] for x in clifford.values())==2}
    out={"schema":"w33.round7.e8minus24_su9_involution.v1",
      "theorem":"In E8_C=sl9+Lambda3(V)+Lambda3(V)* with the committed gamma=-1 bracket, let sigma_c(A,x,y)=(-A^dagger,conj(y),conj(x)) and D=diag(1^7,-1^2) in SU9. theta=Ad_D on sl9 and Lambda3 action on x,y. sigma24=theta∘sigma_c is a conjugate-linear involutive Lie automorphism. Its fixed real Lie algebra has Killing signature (112 positive,136 negative) and maximal compact fixed theta algebra E7_compact+A1_compact; it is the real form E8(-24).",
      "explicit_9x9_D_diagonal":[1]*7+[-1]*2,
      "action_on_grade_zero":"X -> -D X^dagger D",
      "action_on_grade_plus_minus":"(x,y) -> (Lambda3(D) conj(y), Lambda3(D) conj(x))",
      "theta_graded_248_dimensions":{"compact_plus":dimplus,"noncompact_minus":dimminus,
        "sl9_minus":nAminus,"Lambda3_complex_minus":n3minus,
        "Lambda3_real_minus":2*n3minus},
      "root_parity_at_simple_node6":roots,
      "five_Clifford_generator_real_structure_screen":clifford,
      "max_numeric_bracket_realstructure_residual":maxerr,
      "physics_boundary":"This is an explicit mathematical REAL FORM; it does not uniquely choose gravity/matter, fix a vacuum, or prove Standard Model embeddings. Choosing the D involution is external, not dynamically selected.",
      "prior_art":"Repo Pass 10949 already certified E8(-24) via tick line alpha8 parity and full Chevalley-root formulas. This is a NEW simpler implementation in the repo's SU9 elementary tensor coordinates, same real-form isomorphism class, NOT discovery of E8(-24).",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"error":maxerr,
    "dims":out["theta_graded_248_dimensions"]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":check()
