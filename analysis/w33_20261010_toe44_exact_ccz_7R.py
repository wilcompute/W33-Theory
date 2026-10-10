"""TOE44: EXACT native ternary CCZ through a nine-root single-qutrit phase."""
import json,itertools,cmath
from pathlib import Path
R=Path(__file__).resolve().parents[1]
root=R/"data/w33_20261010_toe44_ternary_ccz_compiler.json"
native=json.loads((R/"artifacts/canonical_su3_gauge_and_cubic.json").read_text())["solution"]["d_triples"]
assert len(native)==45
# R|x>=exp(2pi i*x**3/9)|x> and SUM: (a,b)->(a,b+a mod3).
# Inclusion-exclusion cubic polynomial identity in Z/9Z for a,b,c in F3.
# f(a+b+c)-f(a+b)-f(a+c)-f(b+c)+f(a)+f(b)+f(c)=6abc (mod9).
def f(x):return (x%3)**3%9
def S(x):
 a,b,c=x
 return (f(a+b+c)-f(a+b)-f(a+c)-f(b+c)+f(a)+f(b)+f(c))%9
for x in itertools.product(range(3),repeat=3):assert S(x)==6*x[0]*x[1]*x[2]%9,(x,S(x))
# An exact 7-R diagonal implementation of CCZ^sign uses -sign*S(x).
# Each multi-site linear input L=sum subset values mod3 is computed
# in-place to the first register by SUM from the remaining registers,
# then R^k, then inverse SUM to restore data.
patterns=[((0,1,2),-1),((0,1),1),((0,2),1),((1,2),1),
          ((0,),-1),((1,),-1),((2,),-1)]
def expand(sign):
 ops=[]
 for inds,k in patterns:
  tgt=inds[0]
  for src in inds[1:]:ops.append(("SUM",src,tgt,1))
  ops.append(("R",tgt,sign*k))
  for src in reversed(inds[1:]):ops.append(("SUM",src,tgt,-1))
 return ops
def evaluate(sign,x):
 a=list(x);phase=0
 for op in expand(sign):
  if op[0]=="SUM":
   _,s,t,k=op;a[t]=(a[t]+k*a[s])%3
  else:phase=(phase+op[2]*f(a[op[1]]))%9
 assert a==list(x)
 return phase
for sign in (-1,1):
 for x in itertools.product(range(3),repeat=3):
  assert evaluate(sign,x)==3*sign*x[0]*x[1]*x[2]%9
 assert len([op for op in expand(sign) if op[0]=="R"])==7
 assert len([op for op in expand(sign) if op[0]=="SUM"])==10
# Exact one-ancilla R^k gate injection. Prepare magic
# |M_k>=R^{-k}|+>, apply SUM(data -> magic), measure magic in Z,
# then apply qutrit Clifford diagonal feed-forward conditioned on m.
# Conditional phase before feed-forward = zeta9^(-k*f(m-x)).
# Relative to desired zeta9^(k*f(x)), the difference up to
# outcome-global zeta9^(-k*f(m)) is omega^q_mk(x), a quadratic.
def injection_correction(k,m):
 q=[]
 for x in range(3):
  numerator=-k*f(m-x)-k*f(x)+k*f(m)
  assert numerator%3==0,(k,m,x,numerator)
  q.append((numerator//3)%3)
 a=(2*q[1]-q[2])%3
 b=(q[2]-q[1])%3
 assert all(q[x]==(a*x*x+b*x)%3 for x in range(3))
 return dict(measurement=m,magic_state="R^"+str(-k)+"|+>",
    phase_correction_omega_exponents=[(-j)%3 for j in q],
    Clifford_quadratic_coeff_a=int((-a)%3),
    Clifford_linear_coeff_b=int((-b)%3))
inj={str(k):[injection_correction(k,m) for m in range(3)] for k in (-1,1)}
# Check coherent gate action for every computational value and all
# three equally likely measurement outcomes (up to global phase).
for k in (-1,1):
 for m in range(3):
  corr=inj[str(k)][m]["phase_correction_omega_exponents"]
  for x in range(3):
   lhs=(-k*f(m-x)+3*corr[x])%9
   assert (lhs+k*f(m))%9==(k*f(x))%9
# Checks actual native signs and explicit E6 phase on random 27-qutrit words.
assert all(t["sign"] in (-1,1) for t in native)
import numpy as np
rng=np.random.default_rng(44044)
for trial in range(120):
 word=rng.integers(0,3,size=27)
 cubic=sum(int(t["sign"])*int(word[t["triple"][0]])*
           int(word[t["triple"][1]])*int(word[t["triple"][2]]) for t in native)%3
 compiled=sum(evaluate(int(t["sign"]),tuple(int(word[i]) for i in t["triple"]))
              for t in native)%9
 assert compiled==3*cubic,(trial,compiled,cubic)
# Explicit five-layer native circuit stays disjoint and covers each term.
native_layers=json.loads((R/"data/w33_20261010_toe42_native_e6_spreads.json").read_text())[
 "optimal_native_five_layer_schedule"]["triad_layers"]
assert len(native_layers)==5
assert sorted(i for layer in native_layers for i in layer)==list(range(45))
for layer in native_layers:
 assert len(layer)==9
 assert len({v for i in layer for v in native[i]["triple"]})==27
totals={"R_ninth_root_gates":7*45,"SUM_two_qutrit_Clifford_gates":10*45,
        "naive_serial_primitive_count":17*45,
        "ideal_45_term_5_layer_bundled_primitive_depth":17*5,
        "three_qutrit_CCZ_terms":45,
        "logical_ancillas_required_before_magic_injection":0,
        "consumed_R_magic_states":315,
        "injection_SUM_gates":315,
        "injection_Z_measurements":315,
        "adaptive_single_qutrit_Clifford_corrections":315,
        "total_SUM_with_magic_injections":765,
        "max_concurrent_magic_ancillas_in_ideal_disjoint_layer":9}
# Explicit physical-resource firewall: R is non-Clifford 9th-root phase.
out={"status":"EXACT_COMPUTATIONAL_BASIS_CCZ_DECOMPOSITION",
"R_gate":"diag(1,zeta9,zeta9**8) where zeta9=exp(2pi i/9)",
"Clifford_SUM":"|src,target> -> |src,target+src mod3>",
"phase_identity_mod9":"-sign*[f(a+b+c)-f(a+b)-f(a+c)-f(b+c)+f(a)+f(b)+f(c)]=3*sign*a*b*c (mod9)",
"phase_polynomial_pattern":[[list(i),k] for i,k in patterns],
"magic_injection_correction_tables":inj,
"magic_injection_exact_proof":"For R^k use |M>=R^-k|+> on one ancilla, SUM(data->ancilla), measure ancilla outcome m, then diagonal Clifford C_m=diag(omega^{-q_mk(x)}), q_mk(x)=(-k f(m-x)-k f(x)+k f(m))/3. The output equals R^k applied to data up to the outcome-global zeta9^-k*f(m). Each m has probability 1/3, independent of data.",
"example_positive_ops":expand(1),"example_negative_ops":expand(-1),
"total_native_gate_resources":totals,
"native_sign_count":{"positive":sum(t["sign"]==1 for t in native),
                     "negative":sum(t["sign"]==-1 for t in native)},
"verification":"Exact integer arithmetic modulo 9 on all 27 basis states for each sign; all 45 native triads are sign-verified.",
"boundary":"R is non-Clifford, and its ideal injection consumes one exactly prepared magic state, an extra SUM, one Z measurement, and a feed-forward Clifford correction per gate. The cost of preparing/fault-tolerantly distilling 315 magic states and photonic loss, feed-forward latency, routing, crosstalk and QEC is not established. Native depth 85 counts only the pre-injection abstract primitive schedule, NOT physical injected circuit depth."}
root.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":out["status"],"resources":totals,"sign_count":out["native_sign_count"]}))
