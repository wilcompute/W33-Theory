"""Character exact test of whether NONTRIVIAL group-action ancillas evade
the four-identical-boson W33->E6 copy-number obstruction.

Use the existing 25920-element PSp4(3) Molien class fingerprints.
A nontrivial ancilla transforming as 6, 20 or 40 point permutation is
not a G-neutral ancillary register. A=40 with d=1 corresponds to two
DISTINGUISHABLE labeled 40-mode carriers V⊗V, including the exterior
square, unlike identical bosons Sym²(V).
"""
from collections import defaultdict
from pathlib import Path
import math,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_W33_Molien_sympower_branching import symchar
OLD=ROOT/"data"/"toe_20261116_W33_sym_power_Molien_characters.json"
OUT=ROOT/"data"/"toe_20261116_W33_ancilla_irrep_Schlafli_antisym2.json"

def run():
    raw=json.loads(OLD.read_text())
    G=raw["group_size"];assert G==25920
    classes=raw["class_fingerprints"]
    ans={}
    exterior=[0,0,0]
    symmetric=[0,0,0]
    for anc in ("trivial1","Schlafli6","Schlafli20","output27","W33point40"):
        levels=[]
        for d in range(5):
            acc=[0,0,0]
            for row in classes:
                cyc=row["cycle_partition"];m=row["group_element_count"]
                c6=row["character6"];c20=row["character20"];c27=row["character27"]
                cA={"trivial1":1,"Schlafli6":c6,
                    "Schlafli20":c20,"output27":c27,
                    "W33point40":cyc.count(1)}[anc]
                coeff=symchar(cyc,maxd=4)[d]
                for i,cT in enumerate((1,c20,c6)):
                    acc[i]+=m*coeff*cA*cT
            assert all(x%G==0 for x in acc)
            dims=[x//G for x in acc]
            assert min(dims)>=0
            levels.append(dict(d=d,Hom_to_1_20_6=dims,
                               full_output_permutation_representation_possible=all(x>0 for x in dims)))
        ans[anc]=levels
    for row in classes:
        cyc=row["cycle_partition"];count=row["group_element_count"]
        cT=(1,row["character20"],row["character6"])
        chiV=cyc.count(1)
        chiVg2=cyc.count(1)+2*cyc.count(2)
        chiS=(chiV*chiV+chiVg2)//2
        chiA=(chiV*chiV-chiVg2)//2
        assert chiS+chiA==chiV*chiV
        for i,c in enumerate(cT):
            exterior[i]+=count*chiA*c
            symmetric[i]+=count*chiS*c
    assert all(x%G==0 for x in exterior+symmetric)
    ext=[x//G for x in exterior]
    sym=[x//G for x in symmetric]
    assert sym==ans["trivial1"][2]["Hom_to_1_20_6"]
    assert [a+b for a,b in zip(ext,sym)]==ans["W33point40"][1]["Hom_to_1_20_6"]
    ans["V40_antisymmetric2"]={"Hom_to_1_20_6":ext,
                               "dimension":780,
                               "nonzero_six_sector":ext[2]>0}
    ans["V40_symmetric2"]={"Hom_to_1_20_6":sym,"dimension":820}
    distinguished=[]
    for copies in range(6):
        acc=[0,0,0]
        for row in classes:
            count=row["group_element_count"]
            fixed=row["cycle_partition"].count(1)
            chars=(1,row["character20"],row["character6"])
            for j in range(3):acc[j]+=count*fixed**copies*chars[j]
        assert all(x%G==0 for x in acc)
        dims=[x//G for x in acc]
        distinguished.append(dict(labeled_copies=copies,Hom_to_1_20_6=dims,
                    all_27_target_sectors_present=all(x>0 for x in dims)))
    assert distinguished[2]["Hom_to_1_20_6"]==[3,2,0]
    ans["V40_tensor_power_labeled"] = distinguished
    result={
      "status":"EXACT_PSP43_ANCILLA_IRREP_AND_DISTINGUISHABLE_TWO_PHOTON_BRANCHING",
      "full_group_elements":G,
      "modules":ans,
      "statement":"Four-copy minimality holds for identical boson Sym^d V with neutral ancillas. A nontrivial G-representation ancillary register can alter multiplicities, and two distinguishable 40-mode carriers have spatial V tensor V, with exterior-square sector absent from Sym²V.",
      "trivial_ancilla_does_not_change_sector_presence":True,
      "scope":"Representation-theoretic existence of equivariant linear operators only, not a physical LOQC implementation, photon-loss bound or energy-efficient device. Nontrivial ancillas need their own covariant physical encoding."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result
if __name__=="__main__":
    v=run()
    for a in ("Schlafli6","Schlafli20","W33point40"):
        print(a,[x["Hom_to_1_20_6"] for x in v["modules"][a][:3]])
    print("V tensor V antisymmetric:",v["modules"]["V40_antisymmetric2"])
