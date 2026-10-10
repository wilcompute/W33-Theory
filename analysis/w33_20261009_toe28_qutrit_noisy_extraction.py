"""Round28 gate-level Pauli-frame simulation: sequential qutrit SUM circuits
to measure 80 Wilson-Z and 79 Gauss-X checks for [[160,1,8]]_3.

Faults: iid site Pauli, gate-after-SUM 2-qutrit Pauli, ancilla-prep
Pauli and readout flips. Symplectic qutrit SUM propagation is exact.
This is circuit-level *Pauli-channel* simulation with explicitly chosen
sequential extraction circuits, not full coherent quantum hardware or FT.
"""
from pathlib import Path
import sys,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson,selected_basis,MATCHES
from w33_20261009_toe27_qutrit_ideal_decoder import Radius3
OUT=ROOT/'data/w33_20261009_toe28_noisy_qutrit_extraction.json'
def prep():
 ed,D,C=wilson()
 f=np.zeros(160,dtype=np.int16);f[MATCHES[8]]=1
 S=C[(C.astype(np.int16)@f)%3==0]
 I=selected_basis(S)
 HZ=np.asarray(S[I],dtype=np.int16)%3 # for data X errors
 HX=np.asarray(D[:-1],dtype=np.int16)%3 # for data Z errors
 assert HZ.shape==(80,160) and HX.shape==(79,160)
 return C.astype(np.int16),D.astype(np.int16),f,HZ,HX
def nontrivial(rng,count=1):
 q=rng.integers(1,81,size=count)
 # enumerate 80 nonzero vectors (x_data,z_data,x_anc,z_anc)
 x=[]
 for n in np.ravel(q):
  t=int(n);v=[]
  for _ in range(4):v.append(t%3);t//=3
  x.append(v)
 return x
def measure(HZ,HX,x,z,rng,p_gate,p_prep,p_meas):
 nw=0;gates=0;prep_faults=0;read_faults=0;gate_faults=0
 sw=[];sg=[]
 for H,kind in ((HZ,'WilsonZ'),(HX,'GaussX')):
  for row in H:
   ax=az=0
   if rng.random()<p_prep:
    if kind=='WilsonZ':ax=int(rng.integers(1,3))
    else:az=int(rng.integers(1,3))
    prep_faults+=1
   for j in np.flatnonzero(row):
    h=int(row[j])
    if kind=='WilsonZ':
     # SUM^h data_j -> anc
     ax=(ax+h*int(x[j]))%3
     z[j]=(int(z[j])-h*az)%3
    else:
     # SUM^h anc -> data_j
     x[j]=(int(x[j])+h*ax)%3
     az=(az-h*int(z[j]))%3
    gates+=1
    if rng.random()<p_gate:
     fx,fz,fax,faz=nontrivial(rng)[0]
     x[j]=(int(x[j])+fx)%3;z[j]=(int(z[j])+fz)%3
     ax=(ax+fax)%3;az=(az+faz)%3
     gate_faults+=1
   result=(ax if kind=='WilsonZ' else -az)%3
   if rng.random()<p_meas:
    result=(result+int(rng.integers(1,3)))%3;read_faults+=1
   if kind=='WilsonZ':sw.append(result)
   else:sg.append(result)
   nw+=1
 assert gates==int(np.count_nonzero(HZ)+np.count_nonzero(HX))
 return np.array(sw,dtype=np.int16),np.array(sg,dtype=np.int16),dict(
  physical_SUM_gates=gates,ancilla_preparations=nw,ancilla_measurements=nw,
  gate_faults=gate_faults,preparation_faults=prep_faults,measurement_faults=read_faults)
def logical_ok(x,z,xhat,zhat,C,D,f):
 if xhat is None or zhat is None:return False
 xr=(x.astype(np.int16)-xhat.astype(np.int16))%3
 zr=(z.astype(np.int16)-zhat.astype(np.int16))%3
 return bool((not np.any(C@xr%3)) and (not np.any(D@zr%3)) and int(f@zr)%3==0)
def run(trials=160):
 C,D,f,HZ,HX=prep(); dx=Radius3(HZ);dz=Radius3(HX)
 assert int(np.count_nonzero(HZ))==640
 assert int(np.count_nonzero(HX))==316
 n=160
 rng=np.random.default_rng(20261010)
 results={}
 for p_data,p_gate,p_prep,p_meas in ((.002,0,0,0),(.002,.0001,.0001,.0001),
                                      (.002,.0003,.0003,.0003),(.002,.001,.001,.001)):
  fail=0;uncorrectable=0;faults=[0,0,0]
  for trial in range(trials):
   x=np.zeros(n,dtype=np.int16);z=np.zeros(n,dtype=np.int16)
   for j in np.flatnonzero(rng.random(n)<p_data):
    a=int(rng.integers(0,3));b=int(rng.integers(0,3))
    while not(a or b):a=int(rng.integers(0,3));b=int(rng.integers(0,3))
    x[j]=a;z[j]=b
   sZ,sX,stats=measure(HZ,HX,x,z,rng,p_gate,p_prep,p_meas)
   xhat,_=dx.decode(sZ);zhat,_=dz.decode(sX)
   if xhat is None or zhat is None:uncorrectable+=1
   if not logical_ok(x,z,xhat,zhat,C,D,f):fail+=1
   for i,key in enumerate(('gate_faults','preparation_faults','measurement_faults')):
    faults[i]+=stats[key]
  key=f'g{p_gate}_p{p_meas}'
  results[key]=dict(p_data=p_data,p_gate=p_gate,p_prep=p_prep,p_meas=p_meas,
   trials=trials,failures=fail,failure_rate=fail/trials,
   no_syndrome_decoder_result=uncorrectable,
   total_injected_gate_prep_measure_faults=faults)
  print('CIRCUIT',key,'fails',fail,'/',trials,'faults',faults,flush=True)
 # Explicit single ancilla-fault hook constructions: Z measurement has
 # ancilla Z -> Z errors on remaining target links. X measurement
 # ancilla X -> X errors on remaining data links.
 hookZ=max(np.count_nonzero(row)-1 for row in HZ)
 hookX=max(np.count_nonzero(row)-1 for row in HX)
 assert hookZ==7 and hookX==3
 noisedata=results['g0_p0']
 assert noisedata['failures']<=10
 out=dict(status='PASS',code='[[160,1,8]]_3',
  Wilson_weight8_check_count=80,Gauss_weight4_check_count=79,
  physical_SUM_gates_per_full_round=956,
  ancilla_preparations_and_measurements_per_round=159,
  noise_model='Sequential syndrome extraction: Wilson Z measured with data->ancilla SUM^h on |0> ancilla; Gauss X measured with ancilla->data SUM^h on |+> ancilla. Exact F3 Pauli conjugation x_target+=h*x_control,z_control-=h*z_target; independent two-qutrit nonidentity Pauli inserted after each SUM with probability p_gate; ancilla prep and readout flips independently per check.',
  simulation=results,maximum_single_ancilla_Z_hook_on_Wilson_data_Z=int(hookZ),
  maximum_single_ancilla_X_hook_on_Gauss_data_X=int(hookX),
  hook_consequence='A single ancilla phase error during an eight-link Wilson check can generate a correlated Z data error of weight up to seven, even though the code distance is eight. These hook faults are outside the guaranteed <=3 arbitrary-data-error correction radius. The circuit ordering must be optimized for fault tolerance.',
  correctness='Scores correction modulo X Gauss and Z Wilson stabilizer equivalence, not literal physical-error equality.',
  disclaimer='Full one-round circuit-level qutrit Pauli-channel model; NOT repeated fault-tolerant rounds, noisy gauge-fixing, leakage, coherent gate errors, or a demonstrated threshold. Zero failures in finite Monte Carlo samples does not prove fault tolerance.')
 OUT.write_text(json.dumps(out,indent=2)+'\n');return out
if __name__=='__main__':run()
