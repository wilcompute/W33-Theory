"""Exact renormalizable Spin10 messenger-tree source for B/CD/EG1/AD Higgs terms.
Conditional 4D field theory; heavy 10 messenger modes not derived from G2.
"""
from pathlib import Path
import json
import sympy as s
OUT=Path(__file__).resolve().parents[1]/"data/toe_20261119_five_pair_Spin10_tree_certificate.json"

def messenger_tree():
    q={"16H":(1,0,0),"bar16H":(-1,0,0),"10_34":(-1,-1,0),
       "10_24":(-1,0,-1),"A":(1,-1,0),"B":(-1,1,0),
       "C":(1,0,-1),"D":(2,1,1),"E":(-2,-1,-1),"G1":(1,1,2),
       "T":(-2,0,0),"Tb":(2,0,0),"R":(0,1,1),"Rb":(0,-1,-1),
       "U":(2,0,0),"Ub":(-2,0,0),"V":(1,0,1),"Vb":(-1,0,-1),
       "W":(1,1,0),"Wb":(-1,-1,0)}
    R={name:(2 if name in ("10_34","10_24","T","R","U","V","W")
          else 0) for name in q}
    terms=[("T","Tb"),("16H","16H","T"),("Tb","B","10_34"),
         ("Tb","E","R"),("R","Rb"),("Rb","G1","10_24"),
         ("U","Ub"),("bar16H","bar16H","U"),("Ub","C","V"),
         ("V","Vb"),("Vb","D","10_34"),("Ub","A","W"),
         ("W","Wb"),("Wb","D","10_24")]
    for term in terms:
        assert [sum(q[name][i] for name in term) for i in range(3)]==[0,0,0],term
        assert sum(R[name] for name in term)%4==2,term
    M,S,P,B,E,G1,H34,H24,C,D,A=s.symbols("M S P B E G1 H34 H24 C D A",nonzero=True)
    T,Tb,Rm,Rb,U,Ub,V,Vb,W,Wb=s.symbols("T Tb Rm Rb U Ub V Vb W Wb")
    Wuv=(M*T*Tb+S*T+Tb*(B*H34+E*Rm)+M*Rm*Rb+Rb*G1*H24+
         M*U*Ub+P*U+Ub*(C*V+A*W)+M*V*Vb+Vb*D*H34+
         M*W*Wb+Wb*D*H24)
    heavy=(T,Tb,Rm,Rb,U,Ub,V,Vb,W,Wb)
    sol={Rm:-G1*H24/M,Rb:S*E/M**2,
         V:-D*H34/M,Vb:P*C/M**2,W:-D*H24/M,Wb:P*A/M**2,
         Tb:-S/M,Ub:-P/M,T:-(B*H34-E*G1*H24/M)/M,
         U:(C*D*H34+A*D*H24)/M**2}
    assert all(s.simplify(s.diff(Wuv,x).subs(sol,simultaneous=True))==0 for x in heavy)
    eff=s.expand(Wuv.subs(sol,simultaneous=True))
    goal=-S*B*H34/M+S*E*G1*H24/M**2+P*C*D*H34/M**2+P*A*D*H24/M**2
    assert s.expand(eff-goal)==0
    pairs=[("T","Tb"),("R","Rb"),("U","Ub"),("V","Vb"),("W","Wb")]
    assert all(all(q[a][i]+q[b][i]==0 for i in range(3)) and
        (R[a],R[b])==(2,0) for a,b in pairs)
    return {"renormalizable_cubic_and_mass_vertices":[list(t) for t in terms],
       "all_14_vertices_gauge_neutral_and_R2":True,
       "heavy_Spin10_ten_vectorlike_pairs":5,
       "heavy_Spin10_ten_chiral_superfield_components":100,
       "heavy_charge_vectors":{z:list(q[z]) for pair in pairs for z in pair},
       "heavy_R_charge":{z:R[z] for pair in pairs for z in pair},
       "symbolic_UV_superpotential":str(Wuv),
       "heavy_F_terms_zero_identically":True,
       "symbolic_heavy_field_solution":{str(k):str(v) for k,v in sol.items()},
       "integrated_out_exact_superpotential":str(eff),
       "four_B_CD_EG1_AD_ops_recovered":True,
       "pairwise_U1_gauge_anomaly_and_U1sqR_cancel":True,
       "dangerous_matter_Higgs_degeneracy":"Higgs16_H and original chiral family16_1 have identical U1 and proposed R charge; interactions with heavy 10 T not distinguished by gauge/R symmetry. A physical localized selection or extra symmetry needed.",
       "scope":"Exact 4D renormalizable superpotential algebra only; heavy 10 messenger zero modes and nonzero overlap couplings not derived in singular G2. Original strict punctured S3 bulk cubic cup=0, so this does not bypass its physical overlap obstruction. Original anomalous U1 and discrete R inflow remain unresolved."}

def run():
    result=messenger_tree()
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print("PASS 14 exact gauge/R vertices, 5 heavy vectorlike pairs, F=0, four operators")
    print(OUT)
    return result
if __name__=="__main__":run()
