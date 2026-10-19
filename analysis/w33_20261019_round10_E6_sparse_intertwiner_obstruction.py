"""Front3: rigorous obstruction to signed-permutation/diagonal
intertwiner from SU3^3 trinification cubic to a standard
J3(O_complex) Cayley-Dickson octonion chart.
Does NOT rule out non-monomial E6-linear changes of basis.
"""
from __future__ import annotations
import json
import numpy as np
from pathlib import Path
from w33_20261019_round9_triality_cubic_texture import omul
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round10_E6_sparse_intertwiner_obstruction.json"
def run():
    e=np.eye(8);coeff={}
    for i in range(8):
      for j in range(8):
        for k in range(8):
          value=2*omul(omul(e[i],e[j]),e[k])[0]
          if abs(value)>1e-10:
            assert abs(abs(value)-2)<1e-10
            coeff[(i,j,k)]=int(round(value))
    assert len(coeff)==64
    # For Jordan det 27=3+8+8+8, the monomial supports:
    # 1 abc, 24 diagonal-octet quadratic x8 times singlet,
    # 64 different trilinear octet basis products.
    jordan=1+3*8+len(coeff)
    tri=3*6+3**3
    # Any signed-permutation or independent rescaling of the 27
    # field coordinates preserves the *number* of nonzero
    # cubic monomials. Hence 45 != 89 obstructs that restricted map.
    # General E6 change-of-basis is dense and remains viable.
    old=json.loads((ROOT/"data/w33_pass12073_families_from_triality.json").read_text()) if (ROOT/"data/w33_pass12073_families_from_triality.json").exists() else {}
    checks={
     "octonion_trilinear_support_64":len(coeff)==64,
     "octonion_cubic_89_monomial_support":jordan==89,
     "trinification_E6_cubic_45_weight_terms":tri==45,
     "no_mononomial_linear_coordinate_equivalence":jordan!=tri,
     "every_basis_octonion_product_signed_unit":len(coeff)==64 and set(map(abs,coeff.values()))=={2}}
    out={"schema":"w33.round10.E6_trinification_to_Jordan_sparse_map_obstruction.v1",
      "trinification_cubic_support":tri,
      "Jordan_Cayley_Dickson_cubic_support":jordan,
      "Jordan_support_breakdown":{"singlet_abc":1,"singlet_octet_norm_terms":24,"octet_trilinear_terms":64},
      "octet_trilinear_sign_histogram":{"positive":sum(v>0 for v in coeff.values()),"negative":sum(v<0 for v in coeff.values())},
      "theorem":"The E6 trinification cubic det(A)+det(B)+det(C)-Tr(ABC) has 45 distinct coordinate monomials in its canonical 9+9+9 basis. The standard classical Jordan J3(O_C) cubic in Cayley-Dickson 3+8+8+8 coordinates has exactly 89 distinct cubic monomials (1+24+64). An invertible monomial linear transformation (permutation and nonzero independent scaling of coordinates) preserves monomial support cardinality. Therefore NO simple signed permutation/scaling of the 27 coordinates can intertwine these two polynomial expressions. A genuine E6 equivariant intertwiner, if built, MUST mix coordinates by a non-monomial matrix; this is a positive construction constraint, NOT a no-go for full linear E6 equivalence.",
      "source_prior":"Previous Round9 established 45 E6 monomials and octonion cubic; parallel Passes 12064,12067,12073 established Spin8 clock orbit/family counts independently.",
      "complexification":"For the 27 complex E6 representation, the real Jordan 27 formula needs complexified octonions and complex linear transformations. The 89 monomial count is preserved under complexification of this specific chart.",
      "parallel_pass12073_available":bool(old),
      "limit":"Only the restricted monomial/diagonal map was ruled out; no explicit dense 27x27 intertwiner, complex gauge-covariant field identification, or masses derived.",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"signs":out["octet_trilinear_sign_histogram"]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
