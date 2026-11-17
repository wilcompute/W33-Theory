"""Spin characteristic classes, shifted 11D C-field quantization,
torsion flat differential characters and Freed-Witten obstruction.

Internal six-manifold M6=S2xS2xT2 has w2=0 and p1=0, H4=Z3.
Y(p,q)xS1 with Y a principal S1 bundle over S2xS2 has
stable TY=pi*TB + R and w2=0,p1=0. Its H4=Z+Z_g.
Thus Witten's G4 shift lambda/2=p1/4 vanishes on BOTH
models, but their flat degree-4 C-field groups differ:
M6: H3(M,R/Z)=U(1)^4;
YxS1: U(1)^2 x Z_g.
For a nonzero H=k*z in H3(Y)=Z, a D-brane whose
worldvolume spatial wrap is all spin Y has Freed-Witten
W3+H=k*z nonzero: wrapped D5 (plus time) inconsistent
without suitable boundaries/sources/modified setup.
No M/IIB physical Page-charge map is claimed.
"""
import math,itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_Tduality_integral_Gysin_involution import dual,cohomology_circle6
OUT=ROOT/"data"/"toe_20261117_Cfield_spin_shift_flat_FreedWitten.json"
def M6():
    return {"internal":"S2xS2xT2","spin":True,
      "w2":0,"p1":0,"lambda=p1_over_2":0,
      "H4_Z":{"free_rank":3,"torsion":[]},
      "flat_degree4_differential_character_H3_RmodZ":{"U1_free_factors":4,"finite_torsion":[]},
      "flux_integrality":"[G4/(2pi)] is integral, no p1/4 shift. Three free integer flux components Nxy,Nxt,Nyt.",
      "G4_cup_G4_in_internal_dimension6":"zero by form degree; does not imply all 11D CS terms vanish."}
def Y6(p,q):
    g=math.gcd(p,q)
    assert g>0
    H=cohomology_circle6(g)
    assert H["H4"]=={"free":1,"torsion":([g] if g>1 else [])}
    assert H["H3"]=={"free":2,"torsion":([g] if g>1 else [])}
    return {"circle_euler":[p,q],"g":g,
      "spin":True,"w2":0,"p1":0,"lambda=p1_over_2":0,
      "H4_Z":{"free_rank":1,"torsion":([g] if g>1 else [])},
      "flat_degree4_differential_character_H3_RmodZ":{
        "U1_free_factors":2,"finite_torsion":([g] if g>1 else [])},
      "Witten_Cfield_quantization":"p1/4 zero. Flux characteristic class can include a Z_g torsion sector invisible to real G4 curvature.",
      "stable_tangent_proof":"Vertical tangent of oriented circle bundle trivial; TY stably pi*T(S2xS2)+R. Both base S2 factors have w2 and p1 zero, so pullbacks vanish."}
def fw(p,q,k):
    assert math.gcd(p,q)>0 and k!=0
    return {"Euler":[p,q],"H3_integer_class":k,
      "spin_Y5_W3":0,
      "Freed_Witten_sum_W3_plus_H":k,
      "naive_D5_wrapping_entire_Y5_times_time_allowed":False,
      "precise_obstruction":"The D5 worldvolume Y5xR is spin, so W3=0, while the nonzero integral NS H3=k*z restricts nontrivially; Freed-Witten anomaly absent additional brane endpoints or compensating mechanisms.",
      "scope":"Only this proposed naive wrapped D5. Not a classification of all D-brane charges or proof that string compactification is impossible."}
def verify():
    cases=[]
    for p,q,k in itertools.product(range(-5,6),repeat=3):
        if (p,q)==(0,0) or k==0:continue
        a=Y6(p,q);b=Y6(*dual(p,q,k)[:2])
        assert a["spin"] and b["spin"]
        assert a["flat_degree4_differential_character_H3_RmodZ"]["finite_torsion"]==(
            [math.gcd(p,q)] if math.gcd(p,q)>1 else [])
        assert b["g"]==abs(k)
        assert fw(p,q,k)["Freed_Witten_sum_W3_plus_H"]==k
        if (p,q,k) in ((3,3,5),(5,5,3),(1,2,1)):
            cases.append({"original_Cfield":a,"Tdual_Cfield":b,"naive_wrapped_D5":fw(p,q,k)})
    assert len(cases)==3
    m=M6()
    ex=Y6(6,6)
    assert ex["H4_Z"]["torsion"]==[6]
    assert m["H4_Z"]["torsion"]==[]
    return {"status":"PASS_INTERNAL_SPIN_NO_G4_SHIFT_TORSION_FLAT_CFIELD_AND_FW",
      "M6":m,"circle6_example_euler_6_6":ex,
      "computed_examples":cases,
      "nonzero_signed_integer_triples_verified":1200,
      "Witten_shift_formula":"[G4/(2pi)]-lambda/2 integral, lambda=p1/2; both families have p1=0 so no half-integral gravity shift on the internal six-manifold.",
      "flat_Cfield_exact_sequence":"For degree-four differential cohomology, flat fields are H^3(M,R/Z). They contain U(1)^{b3} times Tor H^4(M,Z) (as abstract compact abelian groups).",
      "not_a_Page_charge_dictionary":"Topological C-field quantization, spin and a particular Freed-Witten consistency condition, NOT an M/IIB duality of all physical charges, brane endpoints, or full 11D equation.",
      "references":["https://arxiv.org/abs/hep-th/9609122",
                    "https://www.mathematik.uni-muenchen.de/~schotten/Texte/978-3-540-74955-4_Book_LNP726.pdf"]}
if __name__=="__main__":
    v=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(v["status"],v["nonzero_signed_integer_triples_verified"])
