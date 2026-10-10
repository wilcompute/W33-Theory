"""TOE42 independent verifications of W33 pure-state spectrum and E6 scheduling."""
import itertools,json,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def producer(py,certificate):
 proc=subprocess.run([sys.executable,str(ROOT/"analysis"/py)],cwd=ROOT,
                     text=True,capture_output=True,timeout=90)
 assert proc.returncode==0,(proc.stdout[-2000:],proc.stderr[-2000:])
 return json.loads((ROOT/"data"/certificate).read_text())
def test_pure_two_qutrit_W33_graph_eigenprojection():
 d=producer("w33_20261010_toe42_purity_W33_spectral_identity.py",
    "w33_20261010_toe42_w33_purity_variance_spectral.json")
 assert d["incidence_shape"]==[90,40]
 assert d["W33_A_spectrum"]=={"12":1,"2":24,"-4":15}
 assert d["forbidden_minus_pure_max_norm_from_50_random"]<1e-12
 assert d["pure_graph_identity_max_residual_50_random"]<1e-12
 for record in d["cases"].values():
  assert abs(record["mean"]-.6)<1e-12
  assert abs(record["variance"]-record["variance_from_W33_eigenspaces"])<1e-12
  assert abs(record["norm_squared_lambda_minus4"])<1e-12
def test_density_purity_witness_and_bound():
 d=json.loads((ROOT/"data/w33_20261010_toe42_w33_purity_variance_spectral.json").read_text())
 assert d["mixed_example_tr_rho2"]==.52
 assert abs(d["mixed_exact_deficit_sum_minus_90_one_minus_tr_rho2"]+43.2)<1e-12
 assert d["mixed_example_minus_norm"]>.8
 assert d["mixed_example_all_40_graph_deficits_nonpositive"]
 assert abs(d["cases"]["stabilizer_00"]["variance"]-8/75)<1e-12
 assert d["cases"]["random_pure"]["variance"]<8/75
def test_native_E6_full_spread_parallelism_enumeration_and_counts():
 d=producer("w33_20261010_toe42_native_e6_spread_census.py",
    "w33_20261010_toe42_native_e6_spreads.json")
 assert d["native_triads"]==45 and d["points"]==27
 spreads=d["all_200_spreads"];parallel=d["all_520_parallelisms"]
 assert len(spreads)==200 and len(parallel)==520
 assert d["spread_disjoint_degree_distribution"]=={"31":160,"40":40}
 assert d["classical_spread_count_in_five_layer_parallelisms"]=={"1":520}
 assert all(len(set(s))==9 for s in spreads)
 assert all(len(set(p))==5 and
            sorted(i for j in p for i in spreads[j])==list(range(45))
            for p in parallel)
 assert d["appearances_per_classical_spread"]=={"13":40}
 assert d["appearances_per_nonclassical_spread"]=={"13":160}
def test_signed_E6_schedule_optimality_against_existing_commit():
 d=json.loads((ROOT/"data/w33_20261010_toe42_native_e6_spreads.json").read_text())
 old=json.loads((ROOT/"data/w33_20261010_toe41_e6_45_ccz_compiler.json").read_text())
 native=old["native_triples"]
 opt=d["optimal_native_five_layer_schedule"]["triad_layers"]
 assert sorted(i for layer in opt for i in layer)==list(range(45))
 assert all(len(layer)==9 and len({v for j in layer for v in native[j]["sites"]})==27 for layer in opt)
 def sign_cost(layers):
  seq=[]
  for layer in layers:
   v={}
   for j in layer:
    for site in native[j]["sites"]:
     assert site not in v
     v[site]=native[j]["sign"]
   assert len(v)==27
   seq.append(v)
  return sum(seq[i][x]!=seq[i+1][x] for i in range(4) for x in range(27))
 assert sign_cost(opt)==38
 assert sign_cost(old["native_layer_indices"])==57
 assert d["minimum_site_pulse_sign_switches"]==38
 assert d["original_TOE41_native_order_site_switches"]==57
 assert d["signed_switch_cost_distribution_over_520_parallelisms"]["38"]==2
