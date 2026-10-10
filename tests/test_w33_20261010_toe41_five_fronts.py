"""TOE41 five-front regression against prior native W33 code and certificates."""
import sys,json,subprocess,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def replay(src,cert):
 cmd=[sys.executable,str(ROOT/"analysis"/src)]
 p=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                 text=True,timeout=120)
 assert p.returncode==0,(src,p.stderr[-2500:])
 return json.loads((ROOT/"data"/cert).read_text())
def test_modular_90_frame_no_go_and_variance():
 d=replay("w33_20261010_toe41_clifford_purity_nogo.py",
          "w33_20261010_toe41_clifford_purity_no_go.json")
 assert d["nondegenerate_planes"]==90 and d["incidence_per_nonzero_pauli"]==[9]
 assert all(abs(x["mean"]-.6)<1e-11 for x in d["cases"].values())
 assert abs(d["cases"]["product_theta"]["variance"]-
            d["cases"]["CZ_sheared_theta"]["variance"])<1e-12
 assert abs(d["cases"]["generic_random"]["variance"]-
            d["cases"]["product_theta"]["variance"])>1e-4
def test_native_maxwell_full_acoustic_tensor():
 d=replay("w33_20261010_toe41_maxwell_acoustic_tensor.py",
          "w33_20261010_toe41_maxwell_acoustic_tensor.json")
 assert d["P0_rank"]==78 and d["joint_P_and_divergence_rank"]==157
 C=np.array(d["acoustic_tensor_real_3x3x3x3"])+1j*np.array(d["acoustic_tensor_imag_3x3x3x3"])
 assert C.shape==(3,3,3,3)
 assert np.max(abs(C-np.conj(C.transpose(1,0,3,2))))<1e-8
 assert d["acoustic_speeds"]["x"]["polarization_ratio"]>1.03
 assert abs(d["acoustic_speeds"]["y"]["polarization_ratio"]-
            d["acoustic_speeds"]["z"]["polarization_ratio"])<1e-8
def test_gauge_covariant_overlap_zero_index_all_singular_pairs():
 d=replay("w33_20261010_toe41_w33_overlap_index_nogo.py",
          "w33_20261010_toe41_w33_overlap_index_obstruction.json")
 assert d["full_gauge_covariance_defect"]<1e-10
 assert d["spectral_pairing_defect"]<1e-10
 for k in ("zero_gauge","random_link_phases","gauge_transformed"):
  assert d[k]["index"]==0 and d[k]["plus"]==d[k]["minus"]==40
  assert d[k]["gw_defect"]<1e-10
def test_signed_e6_native_cubic_optimal_5_layer_compiler():
 d=replay("w33_20261010_toe41_e6_45_ccz_compiler.py",
          "w33_20261010_toe41_e6_45_ccz_compiler.json")
 assert d["total_ccz_gates"]==45
 assert d["register_qutrits"]==27
 assert d["determinant_monomials"]==18 and d["trace_monomials"]==27
 assert d["gate_depth_degree_lower_bound"]==d["gate_depth_disjoint_upper_bound"]==5
 assert d["gate_layer_sizes"]==[9]*5
 assert d["native_gate_depth_optimum"]==5
 assert d["native_layer_sizes"]==[9]*5
 assert sorted(i for layer in d["native_layer_indices"] for i in layer)==list(range(45))
 assert all(len({v for i in layer for v in d["native_triples"][i]["sites"]})==27
            for layer in d["native_layer_indices"])
 from collections import Counter
 assert Counter(i for t in d["triples"] for i in t["sites"])=={i:5 for i in range(27)}
def test_locked_nonprospective_internal_maxwell_null():
 d=replay("w33_20261010_toe41_maxwell_birefringence_null.py",
          "w33_20261010_toe41_maxwell_anisotropy_null.json")
 assert d["status"]=="STRICT_ISOTROPIC_MAXWELL_NULL_REJECTED"
 assert d["prior_locked_null"]["tolerance_for_exact_relativistic_null"]==.001
 assert d["max_polarization_ratio_defect"]>.03
 assert d["constraint_projector"]["transverse_dimension"]==80
 assert d["constraint_projector"]["idempotence_defect"]<1e-10
