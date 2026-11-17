"""Five-dimensional FORMAL reduction of the 11D C3 wedge G4 wedge G4 term.

M6=S²_x x S²_y x T²_(a,b), integral cohomology classes:
x,y degree2, a,b degree1 and t=a b degree2.
Background G4 = Nxy*x*y + Nxt*x*a*b + Nyt*y*a*b.
Decompose C3 as external C3, A_x*x+A_y*y+A_t*a*b
plus B_a*a+B_b*b, and scalar modes. The LOCAL expansion
of C3 G4 G4 in one flux background contains:
 C3(5D) wedge F_A  with charge vector Q=(Nyt,Nxt,Nxy)
 A wedge F_C3 by integration by parts,
 B_a wedge dB_b - B_b wedge dB_a with coefficient Nxy.
The non-flux cubic 5D CS tensor has only C_xyt=1.

The exact degrees and wedge pairings establish which operators
are ALLOWED, not the global integral BF level: C_bg is not a
globally defined potential when the flux is nonzero and it also
contributes to the full differential C-field CS functional.
Page current J7=*G4+1/2 C3 G4 is formally closed on shell,
but is gauge dependent under large gauge transformations.
"""
import sys,json
from pathlib import Path
from math import gcd
from functools import reduce
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_M5_graded_G4_wedge_complex import product_form,case,BASIS
OUT=ROOT/"data"/"toe_20261116_M5_5D_local_CS_Page_sector_control.json"
x=("x",);y=("y",);a=("a",);b=("b",);t=("a","b")
vol=("x","y","a","b")
def coef(forms):
    v=()
    sign=1
    for f in forms:
        p=product_form(v,f)
        if p is None:return 0
        sg,v=p
        sign*=sg
    return sign*int(v==vol)

def pairings(Nxy,Nxt,Nyt):
    flux=[(Nxy,("x","y")),(Nxt,("x","a","b")),(Nyt,("y","a","b"))]
    def eval_wedge(*forms):
        return sum(n*coef((*forms,g)) for n,g in flux)
    z=[x,y,t]
    Q=[eval_wedge(f) for f in z]
    eps=sp.Matrix([[eval_wedge(f,g) for g in (a,b)] for f in (a,b)])
    cub=sp.MutableDenseNDimArray.zeros(3,3,3)
    for i,f in enumerate(z):
        for j,g in enumerate(z):
            for k,h in enumerate(z):
                cub[i,j,k]=coef((f,g,h))
    assert Q==[Nyt,Nxt,Nxy]
    assert eps==sp.Matrix([[0,Nxy],[-Nxy,0]])
    assert sum(cub[i,j,k] for i in range(3) for j in range(3) for k in range(3))==6
    g=reduce(gcd,map(abs,Q))
    graded=case(Nxy,Nxt,Nyt)["smith_invariants"]
    return {"background_G4_periods":[Nxy,Nxt,Nyt],
        "five_D_external_C3_vector_F2_pairing":Q,
        "five_D_twoform_B2_pairing_matrix":[list(map(int,eps.row(i))) for i in range(2)],
        "five_D_zero_flux_A_F_F_Chern_Simons_tensor_nonzero_entries":6,
        "rank_C3_to_A_flux_matrix":int(any(Q)),
        "rank_B2_twisted_pairing":int(eps.rank()),
        "integer_Smith_Q_gcd":g,
        "B2_pairing_Smith_invariants":([abs(Nxy),abs(Nxy)] if Nxy else []),
        "cohomology_Smith_grading":graded}

def verify():
    rows=[pairings(*s) for s in [(5,6,6),(6,6,6),(100,101,100),(0,7,8),(0,0,0)]]
    assert rows[0]["integer_Smith_Q_gcd"]==1
    assert rows[0]["B2_pairing_Smith_invariants"]==[5,5]
    assert rows[2]["integer_Smith_Q_gcd"]==1
    assert rows[2]["B2_pairing_Smith_invariants"]==[100,100]
    assert rows[3]["rank_C3_to_A_flux_matrix"]==1
    assert rows[3]["rank_B2_twisted_pairing"]==0
    return {
     "status":"PASS_FORMAL_5D_CS_DECOMPOSITION_C3_A_AND_B2_PAIRINGS",
     "background_and_local_reduction":"C3=(C3_5d)+(A_x*x+A_y*y+A_t*t)+(B_a*a+B_b*b)+3form_internal_scalars; G=dC+Gbg",
     "C3_A_CS_sector":"Term C3_5d wedge F_Ai with period vector Q_i=integral omega_i Gbg; companion A_i wedge F_C3 modulo 5D total derivatives.",
     "B2_CS_sector":"Term epsilon_ab B_a wedge dB_b, epsilon_ab=Nxy*[[0,1],[-1,0]], independent of mixed periods.",
     "STU_pure_Chern_Simons":"C_xyz=1 and its five other symmetric permutations.",
     "physical_globally_nontrivial":"Local expansion is not sufficient to fix quantum CS/BF levels because Cbg is a non-global differential cocycle and the C-field action has shifted quantization and quadratic refinements.",
     "Page_current":"With dG4=0 and EOM d(*G4)+(1/2)G4 wedge G4=0, J_Page=*G4+(1/2)C3 wedge G4 is locally closed; large C3 gauge shifts can change its integral.",
     "M2_M5_charge_candidates":"A_i couples to M2 wrapped on each H2 generator (particle in 5D); B_a couples to M2 wrapped on T2 one-cycle (string in 5D); C3_5d couples to unwrapped M2 (membrane in 5D); magnetic duals involve M5.",
     "explicit_cases":rows}
if __name__=="__main__":
    cert=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(cert["status"],cert["explicit_cases"][2]["B2_pairing_Smith_invariants"])
