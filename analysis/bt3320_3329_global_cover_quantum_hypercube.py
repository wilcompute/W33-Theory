#!/usr/bin/env python3
"""Passes 3320-3329: global cover reconciliation, exact dual compression,
proof-sound chromatic refinement, quantum Hamming walk, and hypercube boundary.

All computations are exact except the explicitly labelled numerical display of
Szegedy eigenphases. No timeout or queued workflow is promoted as a theorem.
"""
from __future__ import annotations
import collections,hashlib,importlib.util,itertools,json,math
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT3320_BT3329_GLOBAL_COVER_QUANTUM_HYPERCUBE_results.json'
VECTORS=ROOT/'data/PART_BT3323_S3_DECODER_VECTOR_CONTRACT.json'
SHARDS=ROOT/'data/PART_BT3324_DEPTH4_UNKNOWN_SHARDS.json'
QWALK=ROOT/'data/PART_BT3325_SZEGEDY_PHASE_LEDGER.json'
HYPER=ROOT/'data/PART_BT3328_BT3329_Q15_HYPERCUBE_HOST.json'
def loadmod(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
ORB=loadmod('orb',ROOT/'analysis/bt3296_3297_cover_hamming_orbifold.py')
DEC=loadmod('dec',ROOT/'analysis/bt3300_s3_standard_decoder.py')
CUBE=loadmod('cube',ROOT/'analysis/bt3256_adaptive_chromatic_cube.py')
def canonical_hash(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def cover_reconciliation():
 G=25920;gh={2:228,4:84,8:15};sh={2:108,4:27,8:0};ext={s:gh[s]-sh.get(s,0) for s in gh};os={s:G//s for s in gh}
 go,so,eo=sum(gh.values()),sum(sh.values()),sum(ext.values());gc=sum(gh[s]*os[s] for s in gh);sc=sum(sh[s]*os[s] for s in sh);ec=sum(ext[s]*os[s] for s in ext)
 assert (go,so,eo)==(327,135,192) and (gc,sc,ec)==(3547800,1574640,1973160) and sc+ec==gc
 return {'global_exact_census':{'PSp_order':G,'orbits':go,'covers':gc,'stabilizer_histogram':{str(k):v for k,v in gh.items()},'orbit_size_by_stabilizer':{str(k):v for k,v in os.items()},'source_certificate_sha256':'0dc832c0a6cc363b05b58cef31870d6464447bba3167c7a93a5009b218871bf2'},'closed_hamming_component':{'orbits':so,'covers':sc,'stabilizer_histogram':{str(k):v for k,v in sh.items()}},'exterior_complement':{'orbits':eo,'covers':ec,'stabilizer_histogram':{str(k):v for k,v in ext.items()},'cover_contributions':{str(s):ext[s]*os[s] for s in ext}},'identities':['327=135+192','3547800=1574640+1973160','1973160=120*12960+57*6480+15*3240'],'boundary':'The subtraction is an exact reconciliation of independently certified PSp orbit censuses. It does not by itself provide switch paths for the 192 exterior orbit classes.'}
def rational_dual_compression():
 d=json.loads((ROOT/'data/PART_BT3298_BT3299_RATIONAL_CHROMATIC_DUAL_results.json').read_text());surf=d['profile_aware_multi_matrix_surface'];hist={int(k):int(v) for k,v in surf['profile_matrix_orbit_histogram'].items()};profiles=sum(hist.values());om=sum(k*v for k,v in hist.items());coords=19*om;nm=55*profiles;nc=19*nm
 assert profiles==195490 and nc==204287050 and coords==98191335
 assert {19*k:int(v) for k,v in hist.items()}=={int(k):int(v) for k,v in surf['profile_coordinate_histogram'].items()}
 return {'profiles':profiles,'block_coordinates_per_matrix':19,'naive_matrices':nm,'orbit_compressed_matrices':om,'naive_rational_coordinates':nc,'orbit_compressed_rational_coordinates':coords,'coordinates_eliminated':nc-coords,'exact_fraction_retained':str(sp.Rational(coords,nc)),'exact_fraction_eliminated':str(1-sp.Rational(coords,nc)),'average_matrix_orbits_per_profile':str(sp.Rational(om,profiles)),'minimum_matrix_orbits':min(hist),'maximum_matrix_orbits':max(hist),'balanced_profile':{'matrix_orbits':2,'coordinates':38,'multiplicity':hist[2]},'histogram':{str(k):hist[k] for k in sorted(hist)},'boundary':'This is exact symmetry compression of the certificate search surface. It does not produce a rational dual excluding ten colours.'}
def rtl_model(valid,syndrome,r):
 z={'valid_input':bool(valid),'detected':False,'invalid_symbol':False,'tie':False,'edge':0,'correction':0,'sideinfo_correction_valid':False}
 if not valid:return z
 if syndrome>5:z['invalid_symbol']=True;return z
 z['detected']=syndrome!=0;mx=max(r);e=next(i for i,x in enumerate(r) if x==mx);z['edge']=e;z['tie']=z['detected'] and sum(x==mx for x in r)>1;z['correction']=(DEC.IDX[DEC.inv(DEC.S3[syndrome])] if e==2 else syndrome) if z['detected'] else 0;z['sideinfo_correction_valid']=z['detected'] and not z['tie'];return z
def decoder_contract():
 h=hashlib.sha256();counts=collections.Counter();samples=[];n=0
 for valid in (0,1):
  for syndrome in range(8):
   for r in itertools.product(range(8),repeat=3):
    got=rtl_model(valid,syndrome,r)
    if valid and syndrome<=5:
     ref=DEC.decode(syndrome,r);assert got['detected']==ref['detected'] and got['tie']==ref['tie'] and got['edge']==ref['edge'] and got['correction']==ref['correction'] and got['sideinfo_correction_valid']==ref['sideinfo_correction_valid']
    elif valid:assert got['invalid_symbol'] and not got['sideinfo_correction_valid']
    else:assert not got['detected'] and not got['invalid_symbol']
    key='invalid' if got['invalid_symbol'] else 'tie' if got['tie'] else 'correctable' if got['sideinfo_correction_valid'] else 'idle_or_detected_no_correction';counts[key]+=1;rec={'valid':valid,'syndrome':syndrome,'reliability':r,**got};h.update((json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n').encode());n+=1
    if len(samples)<12 and n%337==0:samples.append(rec)
 assert n==8192;rtl=ROOT/'rtl/w33_pass3300_s3_fourier_decoder.sv';text=rtl.read_text()
 for token in ('s3_inverse','standard_three_cycle_visible','sideinfo_correction_valid','blind_guarantee'):assert token in text
 data={'schema':'w33.pass3323.s3_decoder_vector_contract.v1','status':'PASS_8192_CASE_SPEC_RTL_BEHAVIORAL_CONTRACT','cases':n,'reliability_alphabet':'0..7 on each of three edges','status_histogram':dict(counts),'vector_stream_sha256':h.hexdigest(),'rtl_source_sha256':hashlib.sha256(rtl.read_bytes()).hexdigest(),'samples':samples,'boundary':'The exhaustive Python behavioral contract is exact. Icarus equivalence remains a separate workflow observation because no local simulator is installed.'};VECTORS.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n');return data
def depth4_unknown_tree():
 m=CUBE.manifest();edges=m['pairwise_frame_disjoint_split_edges'];records=[]
 for c,d in itertools.product(range(10),repeat=2):
  r=CUBE.cube_record((0,3,c,d),edges);r.update(parent=[0,3,c],child_color=d,status='UNSOLVED_EXACT_SHARD');records.append(r)
 assert len(records)==100 and len({r['sha256'] for r in records})==100
 for c in range(10):
  g=[r for r in records if r['parent']==[0,3,c]];assert {r['child_color'] for r in g}==set(range(10)) and len(g)==10
 data={'schema':'w33.pass3324.depth4_unknown_shards.v1','status':'PASS_EXACT_100_GRANDCHILD_PARTITION_WITHOUT_TERMINAL_DECISION','base_dimacs_sha256':m['base_dimacs_sha256'],'root_parent':[0,3],'depth3_unknown_parents':10,'depth4_grandchildren':100,'next_split_edge':4,'records':records,'external_run_observation':{'run_id':30941349999,'observed':'shards 0,1,2,3 completed their 1800-second workflow jobs; shard 4 was in progress; later shards remained queued','promotion':'NONE: workflow success and artifact upload do not reveal a checked SAT/UNSAT status without importing status.json'},'proof_composition':{'SAT':'one independently model-checked grandchild','UNSAT':'all ten independently proof-checked grandchildren for one parent','UNKNOWN':'all other cases, including timeout and unavailable status artifact'},'live_boundary':'10 <= chi(H) <= 11'};data['sha256_without_hash_field']=canonical_hash(data);SHARDS.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n');return data
def szegedy_walk():
 orbits,w=ORB.hamming_quotient();assert np.all(w.sum(axis=1)==10);vals=[sp.Rational(1),sp.Rational(7,10),sp.Rational(2,5),sp.Rational(1,10),sp.Rational(-1,5),sp.Rational(-1,2)];phase=[]
 for lam in vals:
  c=4*lam*lam-2;t=2*math.acos(float(lam));phase.append({'lambda':str(lam),'walk_quadratic':f'z^2-({c})z+1','phase_radians':t,'phase_degrees':t*180/math.pi})
 nz=int(np.count_nonzero(w));wa=int(w.sum());assert nz==1242 and wa==1350
 data={'schema':'w33.pass3325.szegedy_phase_ledger.v1','status':'PASS_EXACT_REVERSIBLE_SZEGEDY_PHASE_COMPILER','classical_states':135,'transition_rule':'P=W/10','nonzero_directed_transitions':nz,'weighted_directed_arc_tokens':wa,'discriminant_eigenvalues':[str(x) for x in vals],'convention':'U=(2 Pi_B-I)(2 Pi_A-I); z=exp(+-2 i arccos(lambda))','exact_phase_quadratics':phase,'smallest_positive_eigenphase':'2 arccos(7/10)','stationary_state':'amplitude proportional to sqrt(|tau-orbit|/243)','boundary':'This is an exact finite-dimensional quantum-walk spectral compiler. It proves neither a speedup nor a physical implementation.'};data['sha256_without_hash_field']=canonical_hash(data);QWALK.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n');return data
def hamming_fourier_and_hypercube():
 states=list(itertools.product(range(3),repeat=5));idx={x:i for i,x in enumerate(states)};n=len(states);A=np.zeros((n,n),dtype=np.int16)
 for x in states:
  i=idx[x]
  for k in range(5):
   for v in range(3):
    if v!=x[k]:y=list(x);y[k]=v;A[i,idx[tuple(y)]]=1
 T=np.zeros((n,n),dtype=np.int8)
 for x in states:T[idx[ORB.tau(x)],idx[x]]=1
 assert np.array_equal(T@T,np.eye(n,dtype=np.int8)) and np.array_equal(T@A,A@T)
 eig=[10,7,4,1,-2,-5];full=[1,10,40,80,80,32];tr=[];P=np.eye(n,dtype=np.int64);AA=A.astype(np.int64)
 for _ in range(6):tr.append(int(np.trace(T@P)));P=P@AA
 tau_tr=list(map(int,sp.Matrix([[l**k for l in eig] for k in range(6)]).LUsolve(sp.Matrix(tr))));inv=[(m+t)//2 for m,t in zip(full,tau_tr)];anti=[m-i for m,i in zip(full,inv)];assert tau_tr==[1,2,4,8,4,8] and inv==[1,6,22,44,42,20]
 def enc(x):
  b=[0]*15
  for k,v in enumerate(x):b[3*k+v]=1
  return tuple(b)
 code=[enc(x) for x in states];assert len(set(code))==243 and all(sum(z)==5 for z in code);dhist=collections.Counter()
 for i in range(n):
  for j in range(i+1,n):
   dh=sum(a!=b for a,b in zip(states[i],states[j]));dq=sum(a!=b for a,b in zip(code[i],code[j]));assert dq==2*dh;dhist[dq]+=1
 assert dhist[2]==1215;bp=[None]*15;maps=[(3,lambda v:(-v)%3),(2,lambda v:(1-v)%3),(1,lambda v:(1-v)%3),(0,lambda v:(-v)%3),(4,lambda v:v)]
 for ob,(ib,f) in enumerate(maps):
  for v in range(3):bp[3*ib+v]=3*ob+f(v)
 assert sorted(bp)==list(range(15))
 def pbits(b):
  out=[0]*15
  for old,new in enumerate(bp):out[new]=b[old]
  return tuple(out)
 assert all(pbits(enc(x))==enc(ORB.tau(x)) for x in states)
 data={'schema':'w33.pass3327_3329.ternary_fourier_q15_host.v1','status':'PASS_EXACT_TAU_FOURIER_AND_Q15_DISTANCE_TWO_HOST','ternary_hamming':{'graph':'H(5,3)=K3 Cartesian-power 5','vertices':243,'degree':10,'edges':1215,'eigenvalues':eig,'full_multiplicities':full,'tau_traces':tau_tr,'tau_invariant_multiplicities':inv,'tau_anti_invariant_multiplicities':anti,'quotient_species':sum(inv)},'q15_host':{'encoding':'each trit is one of 100,010,001 in a dedicated 3-bit block','binary_length':15,'binary_weight':5,'codewords':243,'distance_identity':'d_Q15(enc(x),enc(y))=2 d_H(5,3)(x,y)','edge_rule':'H(5,3) adjacency equals binary Hamming distance two on the block-weight-one code','distance_histogram':{str(k):v for k,v in sorted(dhist.items())},'tau_bit_permutation':bp},'ordinary_hypercube_no_go':{'reason':'H(5,3) contains K3 triangles while every Q_n is bipartite','conclusion':'H(5,3) is not a subgraph of any ordinary hypercube; the exact host uses the distance-two relation of Q15'},'cube_separation':{'Q4_knight':'intrinsic 16-node toroidal-knight/controller network from Passes 3308-3319','Q4_codec':'secondary product-codec relation on 16 complement flags; raw Levi adjacency remains 4K4','Q15_cover_host':'intrinsic block-one-hot host of the 243-state ternary Hamming cover cube','no_claim':'No canonical graph morphism identifies the 16 Q4 controller states with the 135 cover-orbit species.'},'boundary':'Q15 is a combinatorial host in a distance-two graph, not a claim that the cover dynamics physically occupy fifteen qubits.'};data['sha256_without_hash_field']=canonical_hash(data);HYPER.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n');return data
def exterior_192_falsifier(c):
 e=c['exterior_complement'];assert sum(e['stabilizer_histogram'].values())==192
 return {'shared_count':192,'exterior_intrinsic_partition':e['stabilizer_histogram'],'tomotope_reference':'192 flags','test_result':'COUNT_ONLY_ANALOGY_FAILS_CANONICITY_TEST','reason':'The exterior object is a set of PSp orbit classes with three invariant stabilizer labels (120,57,15). The numerical equality 192 supplies no equivariant map to tomotope flags and forgetting the labels discards certified structure.','boundary':'This does not prove that no later construction can introduce a tomotope-labelled model; it rejects identification from cardinality alone.'}
def certificate():
 c=cover_reconciliation();du=rational_dual_compression();de=decoder_contract();sh=depth4_unknown_tree();qw=szegedy_walk();hy=hamming_fourier_and_hypercube();ex=exterior_192_falsifier(c)
 data={'schema':'w33.pass3320_3329.global_cover_quantum_hypercube.v1','status':'PASS_EXACT_EIGHT_FRONT_GLOBAL_COVER_QUANTUM_HYPERCUBE_PACKET','pass3320_3321_global_cover_reconciliation':c,'pass3322_rational_dual_orbit_compression':du,'pass3323_decoder_contract':{k:v for k,v in de.items() if k!='samples'},'pass3324_unknown_refinement':{k:v for k,v in sh.items() if k!='records'},'pass3325_quantum_walk':qw,'pass3326_exterior_192_test':ex,'pass3327_tau_fourier':hy['ternary_hamming'],'pass3328_3329_hypercube':{k:v for k,v in hy.items() if k not in ('ternary_hamming','sha256_without_hash_field')},'live_chromatic_boundary':'10 <= chi(H) <= 11','checks':{'global_cover_arithmetic':True,'exterior_histogram':True,'dual_compression':True,'decoder_8192':True,'depth4_100_shards':True,'szegedy_phase_compiler':True,'tau_fourier':True,'q15_distance_host':True,'ordinary_hypercube_no_go':True},'evidence_boundary':{'proved':'exact finite counts, spectra, graph embeddings/no-go, vector hashes and proof-tree partitions','not_proved':'chi(H) decision, terminal status of queued shards, quantum speedup, physical Q15 implementation, tomotope equivariance, RTL synthesis/placement, PDFs or laboratory claims'}};data['sha256_without_hash_field']=canonical_hash(data);OUT.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n');return data
if __name__=='__main__':
 d=certificate();print(json.dumps({'status':d['status'],'global_covers':d['pass3320_3321_global_cover_reconciliation']['global_exact_census']['covers'],'exterior':d['pass3320_3321_global_cover_reconciliation']['exterior_complement'],'dual_coordinates':d['pass3322_rational_dual_orbit_compression']['orbit_compressed_rational_coordinates'],'decoder_cases':d['pass3323_decoder_contract']['cases'],'shards':d['pass3324_unknown_refinement']['depth4_grandchildren'],'q15':d['pass3328_3329_hypercube']['q15_host'],'sha256':d['sha256_without_hash_field']},indent=2))
